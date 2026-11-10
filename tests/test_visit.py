"""The visit loop with a scripted clinician and fake simulator models (no provider calls)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from conftest import FakeModel, checker_reply

from clinical_env import prompts
from clinical_env.case_schema import Case, Person
from clinical_env.transcript import render_markdown
from clinical_env.visit import (
    Action,
    Examine,
    Invalid,
    ReadRecord,
    Say,
    Simulators,
    SubmitPlan,
    VisitLog,
    run_visit,
)

PLAN: dict[str, Any] = {
    "problems": ["Falls with postural hypotension"],
    "function_summary": "Walks with a stick; unsteady on turning.",
    "risks": ["Further falls"],
    "actions": [
        {
            "type": "medication_change",
            "detail": "Stop furosemide; ask pharmacy to remove it from the dosette",
            "rationale": "Postural drop, no heart failure",
            "urgency": "same_day",
        }
    ],
    "discrepancies": [
        {"description": "Dosette still has furosemide", "resolution": "Stopped it again"}
    ],
    "follow_up": "Phone in one week",
    "safety_netting": "Call 999 after a fall with injury",
}


class Scripted:
    """A clinician that plays a fixed list of actions and records what it is told."""

    def __init__(self, actions: list[Action]) -> None:
        self.actions = list(actions)
        self.system = ""
        self.briefing = ""
        self.results: list[str] = []

    async def start(self, system: str, briefing: str) -> None:
        self.system, self.briefing = system, briefing

    async def act(self) -> Action:
        return self.actions.pop(0) if self.actions else Invalid("script ended")

    async def observe(self, result: str) -> None:
        self.results.append(result)


def _sims(
    patient: str = "Oh I'm fine, love.",
    carer: str = "SILENT",
    flag_text: str | None = None,
    exam: dict[str, object] | None = None,
) -> tuple[Simulators, FakeModel, FakeModel, FakeModel]:
    patient_model = FakeModel(lambda system, user: patient)
    carer_model = FakeModel(lambda system, user: carer)
    checker = FakeModel(checker_reply(flag_text, exam))
    return Simulators(patient_model, carer_model, checker), patient_model, carer_model, checker


def _run(case: Case, actions: list[Action], sims: Simulators, visit: int = 1) -> VisitLog:
    return asyncio.run(run_visit(case, visit, Scripted(actions), sims))


def test_say_gets_a_reply_and_the_other_party_may_interject(edith: Case) -> None:
    sims, _, carer, _ = _sims(carer="She's not managing, doctor.")
    clinician = Scripted([Say("patient", "How are you?"), SubmitPlan(PLAN)])
    log = asyncio.run(run_visit(edith, 1, clinician, sims))
    kinds = [(e.kind, e.actor) for e in log.events]
    assert kinds[:3] == [("say", "clinician"), ("reply", "patient"), ("interjection", "carer")]
    assert clinician.results[0] == (
        "Edith Marsh: Oh I'm fine, love.\nJanet Price (adding): She's not managing, doctor."
    )
    # The interjecting carer heard the patient's reply.
    assert "Edith Marsh: Oh I'm fine, love." in carer.calls[0][-1].content
    assert log.ended == "plan" and log.turns_used == 2


def test_silent_interjection_is_logged_but_not_heard(edith: Case) -> None:
    sims, *_ = _sims(carer="SILENT")
    clinician = Scripted([Say("patient", "How are you?"), SubmitPlan(PLAN)])
    log = asyncio.run(run_visit(edith, 1, clinician, sims))
    interjection = next(e for e in log.events if e.kind == "interjection")
    assert interjection.text is None
    assert clinician.results[0] == "Edith Marsh: Oh I'm fine, love."


def test_flagged_reply_is_regenerated_once_and_both_drafts_kept(edith: Case) -> None:
    sims, patient, _, _ = _sims(patient="I fell three times last night.", flag_text="fell")
    log = _run(edith, [Say("patient", "Any falls?"), SubmitPlan(PLAN)], sims)
    reply = next(e for e in log.events if e.kind == "reply")
    assert len(reply.attempts) == 2  # one regenerate only, even though it is still flagged
    assert all(a.flags[0].type == "invented_fact" for a in reply.attempts)
    assert "previous draft reply was rejected" in patient.calls[1][0].content
    assert "rejected draft 1" in render_markdown(log, {"patient": "Edith", "carer": "Janet"}, {})


def test_unreadable_checker_is_logged_without_regenerating(edith: Case) -> None:
    sims, patient, _, checker = _sims()
    checker._reply = lambda system, user: "looks fine to me"
    log = _run(edith, [Say("patient", "Hello"), SubmitPlan(PLAN)], sims)
    reply = next(e for e in log.events if e.kind == "reply")
    assert len(reply.attempts) == 1
    assert reply.attempts[0].flags[0].type == "checker_error"
    assert len(patient.calls) == 1


def test_simulators_never_see_records_or_examinations(edith: Case) -> None:
    sims, patient, carer, _ = _sims(exam={"ids": ["x_postural_bp"]})
    actions: list[Action] = [
        ReadRecord("discharge_summary"),
        Examine("check her blood pressure lying and standing"),
        Say("patient", "How are you?"),
        SubmitPlan(PLAN),
    ]
    _run(edith, actions, sims)
    seen = " ".join(m.content for call in patient.calls + carer.calls for m in call)
    assert "Furosemide stopped" not in seen
    assert "standing 108/64" not in seen
    assert "blood pressure lying" not in seen


def test_examine_returns_the_case_finding_or_unremarkable(edith: Case) -> None:
    sims, *_ = _sims(exam={"ids": ["x_postural_bp"]})
    log = _run(edith, [Examine("Lying and standing blood pressure"), SubmitPlan(PLAN)], sims)
    exam = log.events[0]
    assert exam.finding_ids == ["x_postural_bp"] and "standing 108/64" in (exam.text or "")

    sims, *_ = _sims(exam={"ids": []})
    log = _run(edith, [Examine("fundoscopy"), SubmitPlan(PLAN)], sims)
    assert log.events[0].text == prompts.NO_FINDING

    sims, *_ = _sims(exam={"ids": [], "too_broad": True})
    log = _run(edith, [Examine("full examination"), SubmitPlan(PLAN)], sims)
    assert log.events[0].text == prompts.TOO_BROAD

    sims, *_ = _sims(exam={"ids": ["x_made_up"]})
    log = _run(edith, [Examine("something"), SubmitPlan(PLAN)], sims)
    assert log.events[0].text == prompts.NO_FINDING
    assert "unknown finding" in (log.events[0].error or "")


def _exam(edith: Case, reply: dict[str, object], request: str = "some obs") -> Any:
    sims, *_ = _sims(exam=reply)
    return _run(edith, [Examine(request), SubmitPlan(PLAN)], sims).events[0]


def test_one_part_of_a_set_returns_only_that_part(edith: Case) -> None:
    event = _exam(edith, {"ids": ["x_pulse"]}, "pulse")
    assert event.finding_ids == ["x_pulse"] and event.text == "Pulse 76 regular."


def test_a_set_returns_all_its_parts_in_order(edith: Case) -> None:
    event = _exam(edith, {"ids": ["x_obs"]}, "a set of obs")
    assert event.finding_ids == ["x_obs"]
    assert event.text == (
        "Pulse 76 regular. Blood pressure 130/72 sitting. Temperature 36.6 C. "
        "Respiratory rate 16. Oxygen saturation 96% on air."
    )


def test_some_parts_of_one_set_return_those_parts(edith: Case) -> None:
    event = _exam(edith, {"ids": ["x_temp", "x_sats"]}, "temperature and sats")
    assert event.finding_ids == ["x_temp", "x_sats"]
    assert event.text == "Temperature 36.6 C. Oxygen saturation 96% on air."


def test_all_parts_or_a_set_with_its_parts_count_as_the_set(edith: Case) -> None:
    every = ["x_pulse", "x_bp", "x_temp", "x_rr", "x_sats"]
    assert _exam(edith, {"ids": every}).finding_ids == ["x_obs"]
    assert _exam(edith, {"ids": ["x_obs", "x_pulse"]}).finding_ids == ["x_obs"]


def test_findings_from_different_examinations_are_too_broad(edith: Case) -> None:
    # The examiner may be generous; code holds the line at one examination per request.
    event = _exam(edith, {"ids": ["x_pulse", "x_gait"]}, "pulse and walking")
    assert event.text == prompts.TOO_BROAD and event.finding_ids == []


def test_a_single_id_reply_still_counts(edith: Case) -> None:
    assert _exam(edith, {"id": "x_pulse"}).finding_ids == ["x_pulse"]


def test_examiner_ids_must_be_a_list(edith: Case) -> None:
    event = _exam(edith, {"ids": "x_pulse"})
    assert event.text == prompts.NO_FINDING and "not a list" in (event.error or "")


def test_exact_label_needs_no_examiner_call(edith: Case) -> None:
    sims, _, _, checker = _sims()
    _run(edith, [Examine("Dix-Hallpike test"), SubmitPlan(PLAN)], sims)
    assert checker.calls == []


def test_phone_visit_cannot_examine_and_has_no_patient(edith: Case) -> None:
    sims, _, _, checker = _sims()
    log = _run(
        edith,
        [Examine("blood pressure"), Say("patient", "Hello Edith"), SubmitPlan(PLAN)],
        sims,
        visit=2,
    )
    assert log.events[0].text == prompts.PHONE_EXAM
    assert log.events[1].kind == "invalid" and "not present" in (log.events[1].error or "")
    assert checker.calls == []


def test_records_are_limited_to_those_available(edith: Case) -> None:
    sims, *_ = _sims()
    log = _run(
        edith,
        [ReadRecord("GP record"), ReadRecord("hospital letters"), SubmitPlan(PLAN)],
        sims,
    )
    assert log.events[0].kind == "read_record" and log.events[0].request == "gp_record"
    assert "Furosemide 40mg tablets - one each morning" in (log.events[0].text or "")
    assert log.events[1].kind == "invalid" and "is not a record" in (log.events[1].error or "")


def test_bad_plan_is_rejected_with_reasons_and_can_be_resubmitted(edith: Case) -> None:
    sims, *_ = _sims()
    clinician = Scripted([SubmitPlan({"problems": []}), SubmitPlan(PLAN)])
    log = asyncio.run(run_visit(edith, 1, clinician, sims))
    assert "plan rejected" in clinician.results[0] and "problems" in clinician.results[0]
    assert log.ended == "plan" and log.turns_used == 2
    assert log.plan is not None and log.plan.actions[0].urgency.value == "same_day"


def test_turn_budget_warns_then_hard_cap_ends_the_visit(edith: Case) -> None:
    sims, *_ = _sims()
    clinician = Scripted([])  # never submits
    log = asyncio.run(run_visit(edith, 2, clinician, sims, hard_cap_factor=1.5))
    assert (log.turn_budget, log.hard_cap, log.turns_used) == (20, 30, 30)
    assert log.ended == "hard_cap" and log.plan is None and log.over_budget
    assert "Submit your plan" in clinician.results[19]
    assert "Submit your plan" not in clinician.results[18]
    assert "No plan submitted" in render_markdown(log, {"carer": "Janet"}, {})


def test_transcript_shows_every_event_in_order(edith: Case) -> None:
    sims, *_ = _sims(carer="She's not managing.", exam={"ids": ["x_gait"]})
    actions: list[Action] = [
        Say("carer", "What have you noticed?"),
        ReadRecord("care_agency_notes"),
        Examine("gait"),
        SubmitPlan(PLAN),
    ]
    log = _run(edith, actions, sims)
    text = render_markdown(log, {"patient": "Edith Marsh", "carer": "Janet Price"}, {"Run": "t"})
    order = [
        "**GP → Janet Price:** What have you noticed?",
        "**Janet Price:** She's not managing.",
        "**Edith Marsh (adds):** Oh I'm fine, love.",
        "_GP reads `care_agency_notes`_",
        "_GP examines: gait_",
        "| medication_change |",
        "**Safety-netting:**",
    ]
    positions = [text.index(item) for item in order]
    assert positions == sorted(positions)


def test_too_broad_wins_over_a_chosen_finding(edith: Case) -> None:
    sims, *_ = _sims(exam={"ids": ["x_postural_bp"], "too_broad": True})
    log = _run(edith, [Examine("examine everything"), SubmitPlan(PLAN)], sims)
    assert log.events[0].text == prompts.TOO_BROAD and log.events[0].finding_ids == []


def test_silence_after_a_rejected_interjection_still_shows_the_flag(edith: Case) -> None:
    drafts = iter(["She fell down the stairs yesterday.", "SILENT"])
    sims, *_ = _sims(flag_text="fell")
    sims = Simulators(sims.patient, FakeModel(lambda s, u: next(drafts)), sims.checker)
    log = _run(edith, [Say("patient", "Hello"), SubmitPlan(PLAN)], sims)
    interjection = next(e for e in log.events if e.kind == "interjection")
    assert interjection.text is None and len(interjection.attempts) == 2
    text = render_markdown(log, {"patient": "Edith", "carer": "Janet"}, {})
    assert "Janet (stays silent after a rejected draft)" in text
    assert "rejected draft 1: _She fell down the stairs yesterday._" in text


def test_checker_and_examiner_never_see_records_or_findings(edith: Case) -> None:
    sims, _, _, checker = _sims(exam={"ids": ["x_postural_bp"]})
    actions: list[Action] = [
        ReadRecord("discharge_summary"),
        Examine("check her blood pressure lying and standing"),
        Say("patient", "How are you?"),
        SubmitPlan(PLAN),
    ]
    _run(edith, actions, sims)
    seen = " ".join(m.content for call in checker.calls for m in call)
    assert "Furosemide stopped" not in seen and "standing 108/64" not in seen


def test_rejected_plan_is_kept_for_review(edith: Case) -> None:
    sims, *_ = _sims()
    log = _run(edith, [SubmitPlan({"problems": ["Falls"]}), SubmitPlan(PLAN)], sims)
    assert log.events[0].rejected_plan == {"problems": ["Falls"]}


def test_core_does_not_import_inspect() -> None:
    import subprocess
    import sys

    code = (
        "import sys, clinical_env.visit, clinical_env.simulators, clinical_env.views;"
        "sys.exit('inspect_ai' in sys.modules)"
    )
    # Import the core modules directly, not via the package's CLI entry point.
    result = subprocess.run([sys.executable, "-c", code], check=False)
    assert result.returncode == 0


def test_investigations_are_not_available_but_exams_are_unremarkable(edith: Case) -> None:
    sims, *_ = _sims(exam={"ids": [], "investigation": True})
    log = _run(edith, [Examine("12-lead ECG"), SubmitPlan(PLAN)], sims)
    assert log.events[0].text == (
        "Not available during this home visit. If you need it, request it in your plan."
    )


def test_examiner_is_told_the_setting(edith: Case) -> None:
    # Weighing is possible in clinic but not at a home visit, so the examiner needs the setting.
    sims, *_ = _sims(exam={"ids": [], "investigation": True})
    _run(edith, [Examine("Weight"), SubmitPlan(PLAN)], sims)
    assert isinstance(sims.checker, FakeModel)
    examiner_turns = [
        c[-1].content for c in sims.checker.calls if "Request: Weight" in c[-1].content
    ]
    assert examiner_turns and examiner_turns[0].startswith("Setting: home visit\n")


def test_a_twice_leaked_fact_is_taken_out_for_a_last_draft(edith: Case) -> None:
    def checker(system: str, user: str) -> str:
        if "giddy" in user.rsplit("Reply to check:\n", 1)[-1]:
            flag = {"type": "hidden_revealed", "detail": "too early", "fact": "[p_dizzy]"}
            return json.dumps({"flags": [flag]})
        return json.dumps({"flags": []})

    def patient(system: str, user: str) -> str:
        return "I come over giddy, love." if "come over giddy" in system else "I'm fine, love."

    patient_model = FakeModel(patient)
    sims = Simulators(patient_model, FakeModel(lambda s, u: "SILENT"), FakeModel(checker))
    log = _run(edith, [Say("patient", "How are you?"), SubmitPlan(PLAN)], sims)
    reply = next(e for e in log.events if e.kind == "reply")
    assert [a.text for a in reply.attempts] == [
        "I come over giddy, love.",
        "I come over giddy, love.",
        "I'm fine, love.",
    ]
    assert reply.attempts[1].flags[0].fact == "p_dizzy"  # "[id]" tag stripped
    assert "come over giddy" not in patient_model.calls[2][0].content
    assert reply.text == "I'm fine, love."


def test_checker_sees_fact_ids_but_the_simulator_does_not(edith: Case) -> None:
    sims, patient, _, checker = _sims()
    _run(edith, [Say("patient", "Hello"), SubmitPlan(PLAN)], sims)
    assert "[p_dizzy]" in checker.calls[0][-1].content
    assert "[p_dizzy]" not in patient.calls[0][0].content


def test_persona_traits_become_habits_in_the_person_prompt(edith: Case) -> None:
    sims, patient, carer, _ = _sims()
    _run(edith, [Say(to="patient", message="How are you?")], sims)
    system = patient.calls[0][0].content
    assert prompts.TRAIT_TEXT["poor_recall"] in system
    assert prompts.TRAIT_TEXT["carer_dominates"] not in system  # Janet's trait, not Edith's
    assert prompts.TRAIT_TEXT["carer_dominates"] in carer.calls[0][0].content


def test_a_case_without_a_carer_runs(edith: Case) -> None:
    # Pilot cases have a carer only where realistic (about half to two thirds of them).
    views = {k: v for k, v in edith.views.items() if k != "carer"}
    visit = edith.visits[0].model_copy(update={"present": [Person.PATIENT]})
    alone = edith.model_copy(
        update={
            "views": views,
            "personas": edith.personas.model_copy(update={"carer": None}),
            "visits": [visit],
        }
    )
    sims, patient, carer, _ = _sims()
    actions: list[Action] = [
        Say(to="patient", message="How are you?"),
        Say(to="carer", message="And how is she?"),
        SubmitPlan(plan=PLAN),
    ]
    log = _run(alone, actions, sims)
    assert log.ended == "plan" and not carer.calls
    assert [e.kind for e in log.events] == ["say", "reply", "invalid", "plan"]


def test_harness_is_appended_to_the_clinician_prompt_and_logged(edith: Case) -> None:
    sims, *_ = _sims()
    clinician = Scripted([])
    log = asyncio.run(run_visit(edith, 1, clinician, sims, harness="  Ask the agenda first.\n"))
    assert clinician.system.endswith("\n\nAsk the agenda first.")
    assert log.clinician_system == clinician.system


def test_no_harness_leaves_the_clinician_prompt_unchanged(edith: Case) -> None:
    sims, *_ = _sims()
    clinician = Scripted([])
    asyncio.run(run_visit(edith, 1, clinician, sims, harness="  \n"))
    expected = prompts.CLINICIAN_SYSTEM.format(turn_budget=edith.visits[0].turn_budget)
    assert clinician.system == expected
