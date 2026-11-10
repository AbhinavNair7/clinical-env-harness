"""All visits of a case in order (docs/build-v0.md, item 4).

Each visit starts the clinician afresh. What carries over is set by `Memory`: by default the
clinician's own earlier plans as notes, plus its earlier consultations written into the GP
record. Each person remembers the spoken conversation of the visits they were at. The
between-visit events are fixed in the case for v0, so no plan changes what the records say.
Plain Python, like visit.py.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from clinical_env.case_schema import Case, Person, Record, Visit
from clinical_env.locale import locale_of
from clinical_env.plan import plan_summary, plan_text
from clinical_env.simulators import GP, Utterance, render_conversation
from clinical_env.views import (
    RecordEntry,
    display_names,
    get_visit,
    visit_heading,
)
from clinical_env.visit import Clinician, Simulators, VisitLog, run_visit


class Memory(StrEnum):
    """What the clinician carries from one visit to the next."""

    NOTES = "notes"  # its own earlier plans, and its GP record entries
    # Whatever the memory, tests ordered at earlier visits are back in the chart (results land
    # in the record, not in the clinician's notes).
    TRANSCRIPTS = "transcripts"  # its full earlier consultations (what it said, read, found)
    NONE = "none"  # nothing: every visit is seen cold


class Participant(BaseModel):
    """Who played clinician in a human run. Anonymised: an ID such as P01, never a name."""

    id: str = Field(pattern=r"^[A-Za-z0-9_-]{1,32}$")
    role: str = Field(min_length=1, max_length=40, description="e.g. GP, GP trainee")
    grade: str = Field(min_length=1, max_length=40, description="e.g. GPST1, consultant")
    consent: bool


class CaseLog(BaseModel):
    case_id: str
    memory: Memory
    clinician: str | None = None  # model id or "human"; picks a judge from another lab
    # Human runs share the transcript format but are never pooled into model scores.
    run_type: Literal["model", "human"] = "model"
    participant: Participant | None = None
    visits: list[VisitLog] = []

    @model_validator(mode="after")
    def _human_runs_are_marked(self) -> CaseLog:
        # Logs saved before run_type existed mark a human run only by clinician="human".
        if self.clinician == "human":
            self.run_type = "human"
        return self


NO_PLAN = "No plan was recorded (the visit ran out of time)."
NOTES_HEADING = "Your notes from earlier visits:"
TRANSCRIPTS_HEADING = "Your earlier consultations with this patient:"


def spoken(log: VisitLog, names: dict[str, str]) -> list[Utterance]:
    """What was said aloud at a visit: what anyone present heard."""
    lines = []
    for event in log.events:
        if event.kind == "say" and event.text:
            lines.append(Utterance(GP, event.text.strip(), to=names.get(event.to or "")))
        elif event.kind in ("reply", "interjection") and event.text:
            lines.append(Utterance(names[event.actor], event.text))
    return lines


def _clinician_transcript(log: VisitLog, names: dict[str, str]) -> str:
    lines = []
    for event in log.events:
        match event.kind:
            case "say":
                lines.append(f"You (to {names.get(event.to or '', event.to)}): {event.text}")
            case "reply":
                lines.append(f"{names[event.actor]}: {event.text}")
            case "interjection" if event.text:
                lines.append(f"{names[event.actor]} (adds): {event.text}")
            case "read_record":
                lines.append(f"[You read {event.request}]")
            case "examine":
                lines.append(f"[You examined {event.request}: {event.text}]")
    lines += ["Your plan:", plan_text(log.plan) if log.plan else NO_PLAN]
    return "\n".join(lines)


def clinician_notes(case: Case, number: int, earlier: Sequence[VisitLog], memory: Memory) -> str:
    if memory == Memory.NONE or not earlier:
        return ""
    today = get_visit(case, number).day
    names = display_names(case)
    sections = [NOTES_HEADING if memory == Memory.NOTES else TRANSCRIPTS_HEADING]
    for log in earlier:
        body = (
            (plan_text(log.plan) if log.plan else NO_PLAN)
            if memory == Memory.NOTES
            else _clinician_transcript(log, names)
        )
        sections.append(f"\n{visit_heading(case, get_visit(case, log.visit), today)}\n{body}")
    return "\n".join(sections)


def gp_entries(
    case: Case, earlier: Sequence[VisitLog], memory: Memory
) -> dict[Record, tuple[RecordEntry, ...]]:
    """The clinician's earlier consultations, as entries in the GP record."""
    if memory == Memory.NONE:
        return {}
    entries = tuple(
        RecordEntry(
            day=get_visit(case, log.visit).day,
            author=locale_of(case).author,
            text=f"{locale_of(case).setting_text[log.setting].capitalize()}. "
            + (plan_summary(log.plan) if log.plan else NO_PLAN),
        )
        for log in earlier
    )
    return {Record.GP_RECORD: entries} if entries else {}


RESULTS_AUTHOR = "Results"
RESULTS_DELAY_DAYS = 2  # results land in the chart a couple of days after the visit


def result_entries(
    case: Case, number: int, earlier: Sequence[VisitLog]
) -> dict[Record, tuple[RecordEntry, ...]]:
    """Tests the clinician ordered at earlier visits, back in the primary care record.

    Shown whatever the clinician's memory setting: results land in the chart, not in its notes.
    """
    today = get_visit(case, number).day
    entries = tuple(
        RecordEntry(
            day=max(log_day, min(log_day + RESULTS_DELAY_DAYS, today - 1)),
            author=RESULTS_AUTHOR,
            text=match.text,
        )
        for log in earlier
        for log_day in [get_visit(case, log.visit).day]
        for match in log.results
    )
    return {Record.GP_RECORD: entries} if entries else {}


def _merge(
    *parts: dict[Record, tuple[RecordEntry, ...]],
) -> dict[Record, tuple[RecordEntry, ...]]:
    merged: dict[Record, tuple[RecordEntry, ...]] = {}
    for part in parts:
        for record, entries in part.items():
            merged[record] = merged.get(record, ()) + entries
    return merged


def person_memories(case: Case, number: int, earlier: Sequence[VisitLog]) -> dict[Person, str]:
    """For each person, the spoken conversation of each earlier visit they were at."""
    today = get_visit(case, number).day
    names = display_names(case)
    memories: dict[Person, str] = {}
    for person in Person:
        visits = [
            f"{visit_heading(case, get_visit(case, log.visit), today)}:\n"
            + render_conversation(spoken(log, names), locale_of(case).clinician)
            for log in earlier
            if person in log.present
        ]
        if visits:
            memories[person] = "\n\n".join(visits)
    return memories


async def run_case(
    case: Case,
    make_clinician: Callable[[Visit], Clinician],
    simulators: Simulators,
    *,
    memory: Memory = Memory.NOTES,
    visits: Sequence[int] | None = None,
    earlier: Sequence[VisitLog] = (),
    harness: str = "",
) -> CaseLog:
    """Run `visits` (default all) in order. `earlier` holds logs of visits already run
    (for running one later visit on its own); only those before each visit are used."""
    numbers = sorted(visits or [v.number for v in case.visits])
    log = CaseLog(case_id=case.id, memory=memory)
    for number in numbers:
        visit = get_visit(case, number)
        before = sorted(
            [v for v in [*earlier, *log.visits] if v.visit < number], key=lambda v: v.visit
        )
        log.visits.append(
            await run_visit(
                case,
                number,
                make_clinician(visit),
                simulators,
                notes=clinician_notes(case, number, before, memory),
                entries=_merge(
                    gp_entries(case, before, memory), result_entries(case, number, before)
                ),
                memories=person_memories(case, number, before),
                harness=harness,
            )
        )
    return log
