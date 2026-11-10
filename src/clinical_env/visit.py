"""One visit end to end: the clinician acts through four tools until it submits a plan.

Plain Python with no Inspect import, so the loop can be wrapped for other frameworks later.
The clinician sits behind the `Clinician` protocol (an LLM adapter or a human at a terminal).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Literal, Protocol

from pydantic import BaseModel, ConfigDict, ValidationError

from clinical_env import prompts
from clinical_env.case_schema import Case, Person, Record, Setting, Visit
from clinical_env.locale import UK, Locale, locale_of
from clinical_env.plan import ActionType, Plan
from clinical_env.roles import Generate, Message
from clinical_env.simulators import (
    GP,
    Attempt,
    Checker,
    PersonSimulator,
    Utterance,
    parse_json_object,
)
from clinical_env.views import (
    RecordEntry,
    clinician_briefing,
    get_visit,
    record_text,
)

# The turn budget is soft (a grader penalty past it). The hard cap only bounds cost and time.
HARD_CAP_FACTOR = 2.0


@dataclass(frozen=True)
class Say:
    to: str
    message: str


@dataclass(frozen=True)
class ReadRecord:
    name: str


@dataclass(frozen=True)
class Examine:
    what: str


@dataclass(frozen=True)
class SubmitPlan:
    plan: dict[str, Any]


@dataclass(frozen=True)
class Invalid:
    """Anything that is not a usable tool call; still costs a turn."""

    detail: str


Action = Say | ReadRecord | Examine | SubmitPlan | Invalid


class Clinician(Protocol):
    async def start(self, system: str, briefing: str) -> None: ...

    async def act(self) -> Action: ...

    async def observe(self, result: str) -> None: ...


EventKind = Literal["say", "reply", "interjection", "read_record", "examine", "plan", "invalid"]


class Event(BaseModel):
    model_config = ConfigDict(frozen=True)

    turn: int
    kind: EventKind
    actor: str  # "clinician", "patient" or "carer"
    to: str | None = None
    request: str | None = None  # record name or examination asked for
    text: str | None = None  # what was said, read or found
    finding_ids: list[str] = []  # an exam's findings; a set's id stands for all its parts
    attempts: list[Attempt] = []
    plan: Plan | None = None
    rejected_plan: dict[str, Any] | None = None  # a plan that failed validation, kept for review
    error: str | None = None


class ResultMatch(BaseModel):
    """One investigation the plan ordered, and what the chart shows for it at the next visit."""

    order: str
    result_ids: list[str] = []
    text: str
    error: str | None = None


class VisitLog(BaseModel):
    case_id: str
    visit: int
    setting: Setting
    present: list[Person]
    turn_budget: int
    hard_cap: int
    clinician_system: str
    briefing: str
    events: list[Event] = []
    plan: Plan | None = None
    turns_used: int = 0
    ended: Literal["plan", "hard_cap"] = "hard_cap"
    results: list[ResultMatch] = []  # tests ordered at this visit, shown at the next

    @property
    def over_budget(self) -> bool:
        return self.turns_used > self.turn_budget


@dataclass(frozen=True)
class Simulators:
    """The cheap models that run the world, by role."""

    patient: Generate
    carer: Generate
    checker: Generate


async def run_visit(
    case: Case,
    number: int,
    clinician: Clinician,
    simulators: Simulators,
    *,
    notes: str = "",
    entries: dict[Record, tuple[RecordEntry, ...]] | None = None,
    memories: dict[Person, str] | None = None,
    hard_cap_factor: float = HARD_CAP_FACTOR,
    harness: str = "",
) -> VisitLog:
    """Run one visit. From visit 2 on, case_run.py passes what carries over: the clinician's
    `notes`, record `entries` it wrote earlier, and each person's `memories` of earlier
    visits they were at. `harness` is extra guidance appended to the clinician's system
    prompt (a harness test); it is logged with the prompt."""
    visit = get_visit(case, number)
    loc = locale_of(case)
    checker = Checker(simulators.checker, loc)
    people = {
        person: PersonSimulator(
            case,
            person,
            visit,
            simulators.patient if person == Person.PATIENT else simulators.carer,
            checker,
            (memories or {}).get(person, ""),
        )
        for person in visit.present
    }
    log = VisitLog(
        case_id=case.id,
        visit=number,
        setting=visit.setting,
        present=list(visit.present),
        turn_budget=visit.turn_budget,
        hard_cap=math.ceil(visit.turn_budget * hard_cap_factor),
        clinician_system=loc.text(prompts.CLINICIAN_SYSTEM).format(turn_budget=visit.turn_budget)
        + (f"\n\n{loc.text(harness.strip())}" if harness.strip() else ""),
        briefing=clinician_briefing(case, number, notes),
    )
    loop = _VisitLoop(case, visit, people, simulators.checker, log, entries or {})
    await clinician.start(log.clinician_system, log.briefing)

    while log.turns_used < log.hard_cap:
        action = await clinician.act()
        log.turns_used += 1
        result = await loop.handle(action, log.turns_used)
        if log.plan is not None:
            log.ended = "plan"
            await clinician.observe(result)
            break
        if log.turns_used == log.turn_budget:
            result += "\n\n[You have used the turns planned for this visit. Submit your plan.]"
        await clinician.observe(result)
    last = number == max(v.number for v in case.visits)
    if visit.results is not None and log.plan is not None and not last:
        log.results = await match_results(visit, log.plan, simulators.checker, loc)
    return log


def _order_text(detail: str) -> str:
    text = " ".join(detail.split())
    return text if len(text) <= 120 else text[:117].rstrip() + "..."


async def match_results(
    visit: Visit, plan: Plan, matcher: Generate, loc: Locale = UK
) -> list[ResultMatch]:
    """Map the plan's investigation orders to the visit's listed results (one cheap call).

    A listed test returns its finding; anything else ordered comes back normal; a vague order
    is "not processed"; a referral typed as an investigation returns nothing. An unreadable or
    inconsistent reply leaves the order "not back yet" and logs the error, never a false normal.
    """
    orders = [a for a in plan.actions if a.type == ActionType.INVESTIGATION]
    if not orders:
        return []
    listed = {r.id: r for r in visit.results or []}
    if not listed:
        return [
            ResultMatch(
                order=o.detail,
                text=prompts.RESULT_ALL_NORMAL.format(order=_order_text(o.detail)),
            )
            for o in orders
        ]
    raw = await matcher(
        [
            Message("system", loc.text(prompts.RESULTS_SYSTEM)),
            Message(
                "user",
                prompts.RESULTS_TURN.format(
                    tests="\n".join(f"- {r.id}: {r.label}" for r in listed.values()),
                    orders="\n".join(f"{i}. {o.detail}" for i, o in enumerate(orders, 1)),
                ),
            ),
        ]
    )

    def unreadable(order: str, why: str) -> ResultMatch:
        text = prompts.RESULT_UNREADABLE.format(order=_order_text(order))
        return ResultMatch(order=order, text=text, error=f"results matcher: {why}")

    try:
        parsed = parse_json_object(raw)
        entries = parsed.get("orders") if isinstance(parsed, dict) else None
        if not isinstance(entries, list) or not all(isinstance(e, dict) for e in entries):
            raise ValueError("no orders list")
        by_number = {int(e["order"]): e for e in entries}
        if sorted(by_number) != list(range(1, len(orders) + 1)):
            raise ValueError(f"orders numbered {sorted(by_number)}, expected 1..{len(orders)}")
    except (ValueError, KeyError, TypeError) as exc:
        return [unreadable(o.detail, f"unreadable reply: {exc}") for o in orders]
    matches = []
    for number, order in enumerate(orders, 1):
        entry = by_number[number]
        kind = entry.get("kind", "tests")
        ids = entry.get("ids") or []
        if kind == "not_a_test":
            continue  # a referral typed as an investigation: nothing comes back from a lab
        if kind == "vague":
            text = prompts.RESULT_VAGUE.format(order=_order_text(order.detail))
            matches.append(ResultMatch(order=order.detail, text=text))
            continue
        if not isinstance(ids, list) or not all(isinstance(i, str) for i in ids):
            matches.append(unreadable(order.detail, f"ids are not a list of strings: {ids!r}"))
            continue
        unknown = [i for i in ids if i not in listed]
        if unknown:  # never turn a matcher slip into a false normal
            matches.append(unreadable(order.detail, f"unknown test {unknown[0]!r}"))
            continue
        ids = list(dict.fromkeys(ids))
        parts = [f"{listed[i].label}: {listed[i].finding}" for i in ids]
        if not ids:
            parts = [prompts.RESULT_ALL_NORMAL.format(order=_order_text(order.detail))]
        elif entry.get("other") is True:
            parts.append(prompts.RESULT_OTHER_NORMAL)
        matches.append(ResultMatch(order=order.detail, result_ids=ids, text=" ".join(parts)))
    return matches


async def match_exam(
    visit: Visit, what: str, examiner: Generate, loc: Locale = UK
) -> tuple[list[str], str, str | None]:
    """Map an examine request to (finding ids, text the clinician sees, error).

    One request earns one finding, a named set (all its parts), or some parts of one set.
    """
    if visit.setting == Setting.PHONE:
        return [], loc.text(prompts.PHONE_EXAM), None
    findings = {f.id: f for f in visit.examination}

    def text_of(ids: list[str]) -> str:
        return " ".join(findings[p].finding or "" for i in ids for p in findings[i].parts or [i])

    wanted = what.strip().lower()
    for finding in findings.values():  # exact label or id: no model call needed
        if wanted in (finding.id.lower(), finding.label.lower()):
            return [finding.id], text_of([finding.id]), None
    listing = "\n".join(
        f"- {f.id}: {f.label}" + (f" (a set of: {', '.join(f.parts)})" if f.parts else "")
        for f in findings.values()
    )
    raw = await examiner(
        [
            Message("system", loc.text(prompts.EXAMINER_SYSTEM)),
            Message(
                "user",
                prompts.EXAMINER_TURN.format(
                    setting=loc.setting_text[visit.setting],
                    findings=listing or "(none)",
                    request=what,
                ),
            ),
        ]
    )
    try:
        parsed = parse_json_object(raw)
    except ValueError as exc:
        return [], prompts.NO_FINDING, f"unreadable examiner reply: {exc}"
    if not isinstance(parsed, dict):
        return [], prompts.NO_FINDING, "examiner reply is not an object"
    # Too broad wins over any id, so a vague request never earns a finding.
    if parsed.get("too_broad") is True:
        return [], prompts.TOO_BROAD, None
    chosen = parsed.get("ids") or []
    if not chosen and isinstance(parsed.get("id"), str):  # the older one-id reply shape
        chosen = [parsed["id"]]
    if not isinstance(chosen, list) or not all(isinstance(i, str) for i in chosen):
        return [], prompts.NO_FINDING, f"examiner ids are not a list of strings: {chosen!r}"
    unknown = [i for i in chosen if i not in findings]
    if unknown:
        return [], prompts.NO_FINDING, f"examiner chose unknown finding {unknown[0]!r}"
    ids = list(dict.fromkeys(chosen))
    if len(ids) > 1:
        # Several ids must be parts of one set; anything else is several examinations.
        sets = [f for f in findings.values() if f.parts and set(ids) <= {f.id, *f.parts}]
        if not sets:
            return [], prompts.TOO_BROAD, None
        if sets[0].id in ids or set(sets[0].parts) <= set(ids):
            ids = [sets[0].id]
    if ids:
        return ids, text_of(ids), None
    if parsed.get("investigation") is True:
        return [], prompts.NOT_AVAILABLE.format(setting=loc.setting_text[visit.setting]), None
    return [], prompts.NO_FINDING, None


class _VisitLoop:
    def __init__(
        self,
        case: Case,
        visit: Visit,
        people: dict[Person, PersonSimulator],
        examiner: Generate,
        log: VisitLog,
        entries: dict[Record, tuple[RecordEntry, ...]],
    ) -> None:
        self.case = case
        self.entries = entries
        self.visit = visit
        self.people = people
        self.examiner = examiner
        self.log = log
        self.conversation: list[Utterance] = []

    def _add(self, event: Event) -> None:
        self.log.events.append(event)

    def _invalid(self, turn: int, detail: str) -> str:
        self._add(Event(turn=turn, kind="invalid", actor="clinician", error=detail))
        return f"Error: {detail}"

    async def handle(self, action: Action, turn: int) -> str:
        match action:
            case Say(to=to, message=message):
                return await self._say(turn, to, message)
            case ReadRecord(name=name):
                return self._read(turn, name)
            case Examine(what=what):
                return await self._examine(turn, what)
            case SubmitPlan(plan=raw):
                return self._submit(turn, raw)
            case Invalid(detail=detail):
                return self._invalid(turn, detail)

    async def _say(self, turn: int, to: str, message: str) -> str:
        valid = {p.value for p in self.visit.present}
        if to not in valid:
            return self._invalid(turn, f"say: '{to}' is not present; use one of {sorted(valid)}")
        if not message.strip():
            return self._invalid(turn, "say: message is empty")
        person = Person(to)
        speaker = self.people[person]
        self._add(Event(turn=turn, kind="say", actor="clinician", to=to, text=message))
        self.conversation.append(Utterance(GP, message.strip(), to=speaker.name))

        attempts = await speaker.reply(self.conversation)
        reply = attempts[-1].text or ""
        self._add(Event(turn=turn, kind="reply", actor=to, text=reply, attempts=attempts))
        self.conversation.append(Utterance(speaker.name, reply))
        heard = [f"{speaker.name}: {reply}"]

        for other, simulator in self.people.items():
            if other == person:
                continue
            attempts = await simulator.interject(self.conversation, addressed=speaker.name)
            if not attempts:
                continue
            text = attempts[-1].text
            self._add(
                Event(
                    turn=turn,
                    kind="interjection",
                    actor=other.value,
                    text=text,
                    attempts=attempts,
                )
            )
            if text:
                self.conversation.append(Utterance(simulator.name, text))
                heard.append(f"{simulator.name} (adding): {text}")
        return "\n".join(heard)

    def _read(self, turn: int, name: str) -> str:
        wanted = name.strip().lower()
        for record in self.visit.records_available:
            if wanted in (record.value, locale_of(self.case).record_titles[record].lower()):
                text = record_text(
                    self.case, record, self.visit.number, self.entries.get(record, ())
                )
                self._add(
                    Event(
                        turn=turn,
                        kind="read_record",
                        actor="clinician",
                        request=record.value,
                        text=text,
                    )
                )
                return text
        available = [r.value for r in self.visit.records_available]
        known = {r.value for r in Record}
        reason = "is not available at this visit" if wanted in known else "is not a record"
        return self._invalid(turn, f"read_record: '{name}' {reason}; available: {available}")

    async def _examine(self, turn: int, what: str) -> str:
        finding_ids, text, error = await match_exam(
            self.visit, what, self.examiner, locale_of(self.case)
        )
        self._add(
            Event(
                turn=turn,
                kind="examine",
                actor="clinician",
                request=what,
                text=text,
                finding_ids=finding_ids,
                error=error,
            )
        )
        return text

    def _submit(self, turn: int, raw: dict[str, Any]) -> str:
        try:
            plan = Plan.model_validate(raw)
        except ValidationError as exc:
            problems = "; ".join(
                f"{'.'.join(str(p) for p in e['loc']) or 'plan'}: {e['msg']}" for e in exc.errors()
            )
            detail = f"submit_plan: plan rejected, fix and resubmit: {problems}"
            self._add(
                Event(turn=turn, kind="invalid", actor="clinician", error=detail, rejected_plan=raw)
            )
            return f"Error: {detail}"
        self.log.plan = plan
        self._add(Event(turn=turn, kind="plan", actor="clinician", plan=plan))
        return "Plan submitted. The visit has ended."
