"""The LLM clinician adapter: the model under test plays the GP through Inspect tool calling.

Tools are declared as plain schemas (no Inspect tool execution): each tool call becomes one
`Action` for the visit loop, and the loop's result goes back to the model as the tool output.
"""

from __future__ import annotations

from collections import deque
from typing import Any

from inspect_ai.model import (
    ChatMessage,
    ChatMessageSystem,
    ChatMessageTool,
    ChatMessageUser,
    GenerateConfig,
    Model,
)
from inspect_ai.tool import ToolCall, ToolInfo, ToolParam, ToolParams

from clinical_env.case_schema import Person, Record
from clinical_env.plan import ActionType, Urgency
from clinical_env.visit import Action, Examine, Invalid, ReadRecord, Say, SubmitPlan

ENDED = "Not done: the visit has ended."
NO_TOOL = "Please act through one of your tools (say, read_record, examine or submit_plan)."


def _string(description: str, enum: list[str] | None = None) -> ToolParam:
    return ToolParam(type="string", description=description, enum=enum)


def _list(items: ToolParam, description: str) -> ToolParam:
    return ToolParam(type="array", description=description, items=items)


def _object(properties: dict[str, ToolParam], description: str = "") -> ToolParam:
    return ToolParam(
        type="object",
        description=description or None,
        properties=properties,
        required=list(properties),
        additionalProperties=False,
    )


def clinician_tools(present: list[Person], records: list[Record]) -> list[ToolInfo]:
    plan_action = _object(
        {
            "type": _string("kind of action", [t.value for t in ActionType]),
            "detail": _string("exactly what will be done"),
            "rationale": _string("why, in this patient"),
            "urgency": _string("how soon", [u.value for u in Urgency]),
        }
    )
    discrepancy = _object(
        {
            "description": _string("what the sources disagreed about"),
            "resolution": _string("what you concluded and why"),
        }
    )
    plan_fields = {
        "problems": _list(_string("one problem"), "problem list; no single diagnosis needed"),
        "function_summary": _string("mobility, falls and activities of daily living"),
        "risks": _list(_string("one risk"), "current risks"),
        "actions": _list(plan_action, "management actions"),
        "discrepancies": _list(discrepancy, "disagreements between sources and how resolved"),
        "follow_up": _string("when and how you will follow up"),
        "safety_netting": _string("what should prompt urgent help, and how"),
    }
    return [
        ToolInfo(
            name="say",
            description="Say something to one person present. Ask one thing at a time.",
            parameters=ToolParams(
                properties={
                    "to": _string("who you are speaking to", [p.value for p in present]),
                    "message": _string("what you say"),
                },
                required=["to", "message"],
                additionalProperties=False,
            ),
        ),
        ToolInfo(
            name="read_record",
            description="Read one record in full.",
            parameters=ToolParams(
                properties={"name": _string("record to read", [r.value for r in records])},
                required=["name"],
                additionalProperties=False,
            ),
        ),
        ToolInfo(
            name="examine",
            description="Examine one thing, e.g. 'lying and standing blood pressure'.",
            parameters=ToolParams(
                properties={"what": _string("the examination or check")},
                required=["what"],
                additionalProperties=False,
            ),
        ),
        ToolInfo(
            name="submit_plan",
            description="Submit your management plan. This ends the visit.",
            parameters=ToolParams(
                properties=plan_fields,
                required=list(plan_fields),
                additionalProperties=False,
            ),
        ),
    ]


def to_action(call: ToolCall) -> Action:
    if call.parse_error:
        return Invalid(f"{call.function}: could not parse arguments: {call.parse_error}")
    args: dict[str, Any] = call.arguments
    try:
        match call.function:
            case "say":
                return Say(to=str(args["to"]), message=str(args["message"]))
            case "read_record":
                return ReadRecord(name=str(args["name"]))
            case "examine":
                return Examine(what=str(args["what"]))
            case "submit_plan":
                return SubmitPlan(plan=args)
    except KeyError as exc:
        return Invalid(f"{call.function}: missing argument {exc}")
    return Invalid(f"unknown tool '{call.function}'")


class LLMClinician:
    """Keeps the clinician's own chat history; one tool call is one visit-loop action."""

    def __init__(self, model: Model, tools: list[ToolInfo]) -> None:
        self.model = model
        self.tools = tools
        self.messages: list[ChatMessage] = []
        self._pending: deque[ToolCall] = deque()
        self._awaiting: ToolCall | None = None

    async def start(self, system: str, briefing: str) -> None:
        self.messages = [ChatMessageSystem(content=system), ChatMessageUser(content=briefing)]

    async def act(self) -> Action:
        if not self._pending:
            output = await self.model.generate(
                self.messages,
                tools=self.tools,
                config=GenerateConfig(parallel_tool_calls=False),
            )
            message = output.message
            self.messages.append(message)
            calls = message.tool_calls or []
            if not calls:
                self._awaiting = None
                return Invalid("replied without using a tool")
            self._pending.extend(calls)
        self._awaiting = self._pending.popleft()
        return to_action(self._awaiting)

    async def observe(self, result: str) -> None:
        if self._awaiting is None:
            # Keep the result: it may carry the turn-budget warning.
            self.messages.append(ChatMessageUser(content=f"{result}\n{NO_TOOL}"))
            return
        call, self._awaiting = self._awaiting, None
        self.messages.append(
            ChatMessageTool(content=result, tool_call_id=call.id, function=call.function)
        )

    def close(self) -> None:
        """Answer calls left in a batch after the visit ended, so the history stays well formed."""
        while self._pending:
            call = self._pending.popleft()
            self.messages.append(
                ChatMessageTool(content=ENDED, tool_call_id=call.id, function=call.function)
            )
