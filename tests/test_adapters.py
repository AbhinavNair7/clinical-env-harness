"""Clinician adapters (LLM tool calling, human terminal) and one full Inspect run on mock models."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from conftest import CASES, FakeModel, checker_reply
from inspect_ai.model import (
    ChatMessage,
    ChatMessageTool,
    GenerateConfig,
    Model,
    ModelOutput,
    get_model,
)
from inspect_ai.tool import ToolCall, ToolChoice, ToolInfo
from test_visit import PLAN

from clinical_env import prompts
from clinical_env.case_schema import Case, Person, Record
from clinical_env.cli import main
from clinical_env.human import HumanClinician
from clinical_env.llm_clinician import ENDED, NO_TOOL, LLMClinician, clinician_tools, to_action
from clinical_env.run import run_model_case
from clinical_env.validate import load_case
from clinical_env.visit import Examine, Invalid, ReadRecord, Say, Simulators, SubmitPlan, run_visit

MOCK = "mockllm/model"
Reply = Callable[[list[ChatMessage], list[ToolInfo], ToolChoice, GenerateConfig], ModelOutput]


def _mock(reply: Reply) -> Model:
    return get_model(MOCK, custom_outputs=reply, memoize=False)


def _text_model(fn: Callable[[str, str], str]) -> Model:
    def reply(
        messages: list[ChatMessage], tools: list[ToolInfo], choice: ToolChoice, c: GenerateConfig
    ) -> ModelOutput:
        return ModelOutput.from_content(MOCK, fn(messages[0].text, messages[-1].text))

    return _mock(reply)


SCRIPT: list[tuple[str, dict[str, Any]]] = [
    ("say", {"to": "patient", "message": "How have you been?"}),
    ("read_record", {"name": "discharge_summary"}),
    ("examine", {"what": "lying and standing blood pressure"}),
    ("submit_plan", PLAN),
]


def _scripted_clinician(seen: list[list[ChatMessage]]) -> Model:
    def reply(
        messages: list[ChatMessage], tools: list[ToolInfo], choice: ToolChoice, c: GenerateConfig
    ) -> ModelOutput:
        seen.append(list(messages))
        step = sum(isinstance(m, ChatMessageTool) for m in messages)
        name, args = SCRIPT[step]
        return ModelOutput.for_tool_call(MOCK, name, args, tool_call_id=f"call_{step}")

    return _mock(reply)


def test_tool_calls_map_to_actions() -> None:
    def call(function: str, arguments: dict[str, Any], error: str | None = None) -> ToolCall:
        return ToolCall(id="1", function=function, arguments=arguments, parse_error=error)

    assert to_action(call("say", {"to": "carer", "message": "Hi"})) == Say("carer", "Hi")
    assert to_action(call("read_record", {"name": "gp_record"})) == ReadRecord("gp_record")
    assert to_action(call("examine", {"what": "gait"})) == Examine("gait")
    assert to_action(call("submit_plan", PLAN)) == SubmitPlan(PLAN)
    assert to_action(call("say", {"to": "carer"})) == Invalid("say: missing argument 'message'")
    assert isinstance(to_action(call("say", {}, error="bad json")), Invalid)
    assert to_action(call("prescribe", {})) == Invalid("unknown tool 'prescribe'")


def test_tools_offer_only_people_present_and_records_available() -> None:
    tools = {t.name: t for t in clinician_tools([Person.CARER], [Record.GP_RECORD])}
    assert set(tools) == {"say", "read_record", "examine", "submit_plan"}
    assert tools["say"].parameters.properties["to"].enum == ["carer"]
    assert tools["read_record"].parameters.properties["name"].enum == ["gp_record"]
    assert set(tools["submit_plan"].parameters.required) == set(PLAN)


def test_llm_clinician_runs_a_visit_and_gets_every_tool_result(edith: Case) -> None:
    seen: list[list[ChatMessage]] = []
    tools = clinician_tools([Person.PATIENT, Person.CARER], list(Record))
    clinician = LLMClinician(_scripted_clinician(seen), tools)
    sims = Simulators(
        FakeModel(lambda s, u: "I'm fine."),
        FakeModel(lambda s, u: "SILENT"),
        FakeModel(checker_reply(exam={"ids": ["x_postural_bp"]})),
    )
    log = asyncio.run(run_visit(edith, 1, clinician, sims))
    assert log.ended == "plan" and log.turns_used == 4
    results = [m for m in clinician.messages if isinstance(m, ChatMessageTool)]
    assert [m.tool_call_id for m in results] == ["call_0", "call_1", "call_2", "call_3"]
    assert results[0].text == "Edith Marsh: I'm fine."
    assert "Furosemide 40mg OM STOPPED" in results[1].text
    assert "standing 108/64" in results[2].text


def test_llm_reply_without_a_tool_costs_a_turn_and_is_nudged(edith: Case) -> None:
    answers = iter(
        [
            ModelOutput.from_content(MOCK, "Let me think about this."),
            ModelOutput.for_tool_call(MOCK, "submit_plan", PLAN, tool_call_id="c1"),
        ]
    )
    clinician = LLMClinician(_mock(lambda *_: next(answers)), clinician_tools([Person.PATIENT], []))
    sims = Simulators(*(FakeModel(checker_reply()) for _ in range(3)))
    log = asyncio.run(run_visit(edith, 1, clinician, sims))
    assert log.turns_used == 2 and log.events[0].kind == "invalid"
    nudge = clinician.messages[3].text
    assert nudge.startswith("Error: replied without using a tool") and NO_TOOL in nudge


def test_human_clinician_commands_and_plan_entry() -> None:
    lines = iter(
        [
            "help",
            "c What have you seen her doing?",
            "plan",
            *["Falls", ""],
            "Stick indoors",
            *["Further falls", ""],
            "medication_change | Stop furosemide | Postural drop | same_day",
            "not enough parts",
            "",
            *["Dosette has furosemide | Stopped it", ""],
            "One week",
            "999 if she falls and is hurt",
        ]
    )
    shown: list[str] = []
    human = HumanClinician(read=lambda prompt: next(lines), write=shown.append)

    async def play() -> tuple[object, object]:
        first = await human.act()
        return first, await human.act()

    first, second = asyncio.run(play())
    assert first == Say("carer", "What have you seen her doing?")
    assert isinstance(second, SubmitPlan)
    assert second.plan["actions"] == [
        {
            "type": "medication_change",
            "detail": "Stop furosemide",
            "rationale": "Postural drop",
            "urgency": "same_day",
        }
    ]
    assert second.plan["problems"] == ["Falls"] and second.plan["follow_up"] == "One week"
    assert second.plan["discrepancies"] == [
        {"description": "Dosette has furosemide", "resolution": "Stopped it"}
    ]
    assert any("skipped (needs 4 parts)" in s for s in shown)


def test_inspect_run_is_one_sample_with_every_visit_in_order(tmp_path: Path) -> None:
    seen: list[list[ChatMessage]] = []
    models = {
        "clinician": _scripted_clinician(seen),
        "patient": _text_model(lambda s, u: "Oh I'm fine, love."),
        "carer": _text_model(lambda s, u: "She's not, doctor."),
        "checker": _text_model(
            lambda s, u: json.dumps(
                {"ids": ["x_postural_bp"]} if s == prompts.EXAMINER_SYSTEM else {"flags": []}
            )
        ),
        "grader": _text_model(lambda s, u: "unused"),
    }
    eval_log, logs = run_model_case(CASES / "edith_marsh.yaml", models, epochs=1, log_dir=tmp_path)
    [log] = logs
    assert eval_log.status == "success" and [v.visit for v in log.visits] == [1, 2]
    first, second = log.visits
    assert first.ended == "plan" and second.ended == "plan"
    assert [e.kind for e in first.events] == [
        "say",
        "reply",
        "interjection",
        "read_record",
        "examine",
        "plan",
    ]
    # Visit 2 is a phone call with Janet only: the scripted "say to patient" is invalid there.
    assert second.events[0].kind == "invalid" and second.events[2].text == prompts.PHONE_EXAM
    # A fresh clinician context at visit 2: it starts again from a system prompt and briefing,
    # holding its visit-1 plan as notes and none of the visit-1 conversation.
    visit_two_start = next(m for m in seen if "Visit 2:" in m[1].text)
    assert len(visit_two_start) == 2
    assert "Your notes from earlier visits:" in visit_two_start[1].text
    assert "How have you been?" not in visit_two_start[1].text
    [sample] = eval_log.samples or []
    assert sample.id == "edith_marsh"
    # The Inspect viewer shows both visits' clinician conversations, tool results included.
    assert sum(isinstance(m, ChatMessageTool) for m in sample.messages) == 8
    assert set(eval_log.stats.role_usage) >= {"clinician", "patient", "carer", "checker"}


def test_cli_run_rejects_an_invalid_case(tmp_path: Path, capsys: Any) -> None:
    bad = tmp_path / "broken.yaml"
    bad.write_text("id: broken\n")
    assert main(["run", str(bad)]) == 1
    assert "is invalid" in capsys.readouterr().out


def test_a_batch_of_tool_calls_is_one_turn_each_and_stops_at_the_plan(edith: Case) -> None:
    generates = 0

    def reply(
        messages: list[ChatMessage], tools: list[ToolInfo], choice: ToolChoice, c: GenerateConfig
    ) -> ModelOutput:
        nonlocal generates
        generates += 1
        output = ModelOutput.for_tool_call(MOCK, "read_record", {"name": "gp_record"}, "a")
        calls = [
            ToolCall(id="a", function="read_record", arguments={"name": "gp_record"}),
            ToolCall(id="b", function="submit_plan", arguments=PLAN),
            ToolCall(id="c", function="examine", arguments={"what": "gait"}),
        ]
        output.choices[0].message.tool_calls = calls
        return output

    clinician = LLMClinician(_mock(reply), clinician_tools([Person.PATIENT], list(Record)))
    sims = Simulators(*(FakeModel(checker_reply()) for _ in range(3)))
    log = asyncio.run(run_visit(edith, 1, clinician, sims))
    clinician.close()
    assert generates == 1 and log.turns_used == 2 and log.ended == "plan"
    answered = [m for m in clinician.messages if isinstance(m, ChatMessageTool)]
    assert [(m.tool_call_id, m.text == ENDED) for m in answered] == [
        ("a", False),
        ("b", False),
        ("c", True),
    ]


def test_twin_loads_with_its_base_truth() -> None:
    twin = load_case(CASES / "edith_marsh_twin.yaml")
    base = load_case(CASES / "edith_marsh.yaml")
    assert twin.id != base.id and twin.hidden_truth == base.hidden_truth
    assert twin.conflicts == []


def test_cli_run_rejects_a_missing_visit_and_bad_epochs(capsys: Any) -> None:
    case = str(CASES / "edith_marsh.yaml")
    assert main(["run", case, "--visit", "3"]) == 1
    assert "has no visit 3" in capsys.readouterr().out
    assert main(["run", case, "--epochs", "0"]) == 1
    assert "--epochs must be at least 1" in capsys.readouterr().out
