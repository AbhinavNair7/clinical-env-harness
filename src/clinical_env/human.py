"""The human clinician adapter: a person plays the GP at the terminal (case QA, human baseline).

Each command is one turn, exactly as for a model. Input and output are injectable for tests.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

from clinical_env.plan import ActionType, Urgency
from clinical_env.visit import Action, Examine, Invalid, ReadRecord, Say, SubmitPlan

HELP = """\
Commands (each one is a turn):
  p <message>      say to the patient
  c <message>      say to the carer
  read <record>    read a record, e.g. read gp_record
  exam <what>      examine, e.g. exam lying and standing blood pressure
  plan             write and submit your plan (ends the visit)
  help             show this again (free)"""

Input = Callable[[str], str]
Output = Callable[[str], None]


class HumanClinician:
    def __init__(self, read: Input = input, write: Output = print) -> None:
        self._read = read
        self._write = write

    async def _ask(self, prompt: str) -> str:
        return await asyncio.to_thread(self._read, prompt)

    async def start(self, system: str, briefing: str) -> None:
        """Called at the start of every visit; the briefing carries notes from earlier ones."""
        self._write(f"{'=' * 72}\n{system}\n\n{briefing}\n\n{HELP}\n")

    async def act(self) -> Action:
        while True:
            line = (await self._ask("\nyou> ")).strip()
            command, _, rest = line.partition(" ")
            rest = rest.strip()
            match command.lower():
                case "" | "help":
                    self._write(HELP)
                case "p":
                    return Say(to="patient", message=rest)
                case "c":
                    return Say(to="carer", message=rest)
                case "read":
                    return ReadRecord(name=rest)
                case "exam":
                    return Examine(what=rest)
                case "plan":
                    return SubmitPlan(plan=await self._plan())
                case _:
                    return Invalid(f"unknown command '{command}'; type help")

    async def observe(self, result: str) -> None:
        self._write(result)

    async def _lines(self, label: str) -> list[str]:
        self._write(f"{label} (one per line, blank line to finish):")
        items = []
        while line := (await self._ask("  - ")).strip():
            items.append(line)
        return items

    async def _plan(self) -> dict[str, Any]:
        problems = await self._lines("Problems")
        function_summary = await self._ask("Function and ADL summary: ")
        risks = await self._lines("Risks")
        self._write(
            "Actions as: type | detail | rationale | urgency\n"
            f"  types: {', '.join(t.value for t in ActionType)}\n"
            f"  urgency: {', '.join(u.value for u in Urgency)}"
        )
        actions = []
        for line in await self._lines("Actions"):
            parts = [part.strip() for part in line.split("|")]
            if len(parts) == 4:
                actions.append(
                    dict(zip(("type", "detail", "rationale", "urgency"), parts, strict=True))
                )
            else:
                self._write(f"  skipped (needs 4 parts): {line}")
        discrepancies = []
        for line in await self._lines("Discrepancies as: what disagreed | how resolved"):
            description, _, resolution = line.partition("|")
            discrepancies.append(
                {"description": description.strip(), "resolution": resolution.strip()}
            )
        return {
            "problems": problems,
            "function_summary": function_summary.strip(),
            "risks": risks,
            "actions": actions,
            "discrepancies": discrepancies,
            "follow_up": (await self._ask("Follow-up: ")).strip(),
            "safety_netting": (await self._ask("Safety-netting: ")).strip(),
        }
