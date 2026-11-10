"""The grader (docs/build-v0.md, item 5; ResidencyRL section 3.3).

Per visit, one judge call per rubric group (criticals, other must-dos, must-not-dos with
penalties, consultation quality), each returning JSON validated here. Code decides what it
can from the visit log (records read, people spoken to, examinations done, turns used), and a
judge's "met" counts only when the log shows what the item requires and its evidence quote is
really in the transcript or plan. Plain Python behind `Generate`, like the simulators.
"""

from __future__ import annotations

import asyncio
import re
from collections.abc import Sequence
from itertools import combinations
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from clinical_env import prompts
from clinical_env.case_run import CaseLog
from clinical_env.case_schema import SOURCES, Case, Country, RubricItem, RubricKind, Setting, Visit
from clinical_env.locale import Locale, locale_of
from clinical_env.plan import plan_text
from clinical_env.roles import DEFAULT_CONFIG, Generate, Message
from clinical_env.simulators import parse_json_object
from clinical_env.views import display_names, facts_at, get_visit
from clinical_env.visit import VisitLog

DEFAULT_CONSULTATION = DEFAULT_CONFIG.parents[1] / "rubrics" / "consultation.yaml"

# Penalty points (ResidencyRL: an invented clinical fact costs 2; a contraindicated action,
# missed red flag or under-triage 3). Over-provision is ours, from the M1 clinical review.
PenaltyType = Literal["invented_fact", "wrong_fact_action", "over_provision", "over_budget"]
PENALTY_WEIGHTS: dict[PenaltyType, float] = {
    "invented_fact": 2.0,
    "wrong_fact_action": 3.0,
    "over_provision": 1.0,
    "over_budget": 1.0,
}
# Every over-provision is listed, but together they cost at most this per visit, so a padded
# plan loses marks without outweighing a missed critical (weight 3).
OVER_PROVISION_CAP = 3.0
_JUDGED_PENALTIES: dict[str, PenaltyType] = {
    "invented_facts": "invented_fact",
    "wrong_fact_actions": "wrong_fact_action",
    "over_provision": "over_provision",
}

Group = Literal["critical", "must_do", "must_not_do", "consultation"]


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --- the generic consultation rubric --------------------------------------------------------


class ConsultationItem(_Model):
    id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    weight: float = Field(gt=0)
    settings: list[Setting] = Field(default_factory=list, description="empty: every visit")
    from_visit: int = Field(default=1, ge=1, description="e.g. 2: follow-up visits only")
    check: Literal["read_first"] | None = None
    examples: dict[Country, str] = Field(
        default_factory=dict, description="added to the description for a case in that country"
    )

    def text(self, country: Country) -> str:
        return " ".join(f"{self.description} {self.examples.get(country, '')}".split())


class ConsultationRubric(_Model):
    items: list[ConsultationItem] = Field(min_length=1)


def load_consultation_rubric(path: Path = DEFAULT_CONSULTATION) -> list[ConsultationItem]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ConsultationRubric.model_validate(data).items


# --- what the visit log shows, decided in code ----------------------------------------------


class LogFacts(_Model):
    turns_used: int
    turn_budget: int
    ended: str
    records_read: list[str]  # in the order first read
    records_before_talking: list[str]  # read before the clinician first spoke
    # read before its second spoken turn: one greeting or consent turn first is allowed
    records_after_greeting: list[str]
    records_not_read: list[str]
    spoke_to: dict[str, int]  # person -> times addressed
    examined: list[str]  # finding ids; a set's id also stands for each of its parts
    multi_question_turns: int  # times the clinician asked two or more questions at once
    invalid_actions: int


def log_facts(log: VisitLog, visit: Visit) -> LogFacts:
    parts = {f.id: f.parts for f in visit.examination}
    read: list[str] = []
    before: list[str] = []
    talked = False
    says = 0
    after_greeting: list[str] = []
    spoke: dict[str, int] = {}
    examined: list[str] = []
    multi = invalid = 0
    for event in log.events:
        if event.kind == "say":
            talked = True
            says += 1
            spoke[event.to or ""] = spoke.get(event.to or "", 0) + 1
            multi += (event.text or "").count("?") >= 2
        elif event.kind == "read_record" and event.request and event.request not in read:
            read.append(event.request)
            if says <= 1:
                after_greeting.append(event.request)
            if not talked:
                before.append(event.request)
        elif event.kind == "examine":
            for finding in event.finding_ids:
                examined += [finding, *parts.get(finding, [])]
        elif event.kind == "invalid":
            invalid += 1
    available = [r.value for r in visit.records_available]
    return LogFacts(
        turns_used=log.turns_used,
        turn_budget=log.turn_budget,
        ended=log.ended,
        records_read=read,
        records_before_talking=before,
        records_after_greeting=after_greeting,
        records_not_read=[r for r in available if r not in read],
        spoke_to=spoke,
        examined=list(dict.fromkeys(examined)),
        multi_question_turns=multi,
        invalid_actions=invalid,
    )


def unmet_requirements(item: RubricItem, facts: LogFacts) -> list[str]:
    """What an item requires that the log does not show (empty when all is there)."""
    if item.requires is None:
        return []
    missing = [f"did not examine {i}" for i in item.requires.examined if i not in facts.examined]
    missing += [
        f"did not read {r.value}" for r in item.requires.read if r not in facts.records_read
    ]
    missing += [
        f"did not speak to the {p.value}" for p in item.requires.spoke_to if p not in facts.spoke_to
    ]
    return missing


def _checked(check: str, facts: LogFacts) -> tuple[bool, str]:
    if check == "read_first":
        # The clinician arrives in the room: a greeting first is courteous, but the records
        # come before the first real question.
        if facts.records_after_greeting:
            return True, "read before its questions: " + ", ".join(facts.records_after_greeting)
        if not facts.records_read:
            return False, "read no records"
        return False, "asked questions before reading any record"
    raise ValueError(f"unknown consultation check {check!r}")


# --- verdicts and scores --------------------------------------------------------------------


class Verdict(_Model):
    id: str
    group: Group
    kind: str  # a rubric kind, or "consultation"
    weight: float
    critical: bool = False
    met: bool | None  # for a must-not-do, True means it happened; None means not graded
    applicable: bool = True
    reason: str = ""
    evidence: str = ""
    evidence_verified: bool = True
    overridden: str | None = None  # why code overruled the judge's "met"


class Penalty(_Model):
    type: PenaltyType
    quote: str
    reason: str
    weight: float
    evidence_verified: bool = True


class VisitScore(_Model):
    visit: int
    verdicts: list[Verdict]
    penalties: list[Penalty]
    log_facts: LogFacts
    errors: list[str] = []
    earned: float
    possible: float
    deductions: float
    score: float | None  # (earned - deductions) / possible, floored at 0
    criticals_met: bool | None  # None: no critical items here, or one could not be graded
    consultation_earned: float
    consultation_possible: float


class CaseScore(_Model):
    case_id: str
    judge: str
    visits: list[VisitScore]
    score: float | None
    criticals_met: bool | None
    critical_misses: list[str]
    ungraded: list[str]  # item ids a judge failed to grade
    consultation_score: float | None


def score_visit(
    number: int,
    verdicts: list[Verdict],
    penalties: list[Penalty],
    facts: LogFacts,
    errors: list[str],
) -> VisitScore:
    rubric = [v for v in verdicts if v.group in ("critical", "must_do")]
    possible = sum(v.weight for v in rubric)
    earned = sum(v.weight for v in rubric if v.met)
    deductions = sum(v.weight for v in verdicts if v.group == "must_not_do" and v.met)
    # A penalty whose quote is not in the transcript is listed but costs nothing.
    counted = [p for p in penalties if p.evidence_verified]
    over = sum(p.weight for p in counted if p.type == "over_provision")
    deductions += sum(p.weight for p in counted if p.type != "over_provision")
    deductions += min(over, OVER_PROVISION_CAP)
    # A judge failure must never read as a clinician failure: no score while any case item
    # is ungraded.
    partial = any(v.met is None for v in verdicts if v.group != "consultation")
    consult = [
        v for v in verdicts if v.group == "consultation" and v.applicable and v.met is not None
    ]
    return VisitScore(
        visit=number,
        verdicts=verdicts,
        penalties=penalties,
        log_facts=facts,
        errors=errors,
        earned=earned,
        possible=possible,
        deductions=deductions,
        score=None if partial or not possible else max(0.0, earned - deductions) / possible,
        criticals_met=criticals_verdict([v for v in verdicts if v.critical]),
        consultation_earned=sum(v.weight for v in consult if v.met),
        consultation_possible=sum(v.weight for v in consult),
    )


def critical_failed(v: Verdict) -> bool:
    """A critical must-do not done, or a critical must-not-do that happened."""
    return v.met is True if v.kind == RubricKind.MUST_NOT_DO.value else v.met is False


def criticals_verdict(criticals: Sequence[Verdict]) -> bool | None:
    """False if any critical failed (a failure decides even if another is ungraded), None if
    there are none or one is ungraded, else True."""
    if any(critical_failed(v) for v in criticals):
        return False
    if not criticals or any(v.met is None for v in criticals):
        return None
    return True


def score_case(case_id: str, judge: str, visits: list[VisitScore]) -> CaseScore:
    possible = sum(v.possible for v in visits)
    partial = any(x.met is None for v in visits for x in v.verdicts if x.group != "consultation")
    net = sum(v.earned for v in visits) - sum(v.deductions for v in visits)
    criticals = [x for v in visits for x in v.verdicts if x.critical]
    ungraded = [x.id for v in visits for x in v.verdicts if x.met is None]
    misses = [x.id for x in criticals if critical_failed(x)]
    consult_possible = sum(v.consultation_possible for v in visits)
    return CaseScore(
        case_id=case_id,
        judge=judge,
        visits=visits,
        score=None if partial or not possible else max(0.0, net) / possible,
        criticals_met=criticals_verdict(criticals),
        critical_misses=misses,
        ungraded=ungraded,
        consultation_score=(
            sum(v.consultation_earned for v in visits) / consult_possible
            if consult_possible
            else None
        ),
    )


# --- evidence -------------------------------------------------------------------------------

_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-"})


def _normal(text: str) -> str:
    return re.sub(r"\s+", " ", text.translate(_QUOTES).lower()).strip()


MIN_PIECE = 12  # characters: shorter pieces ("a", "GP to") would match almost anything


def quote_found(quote: str, source: str) -> bool:
    """True if every piece of `quote` (pieces joined by "...") is in `source`, ignoring case,
    spacing, curly quotes and the quote marks or full stop a judge wraps around it. Each piece
    must be at least MIN_PIECE characters."""
    haystack = _normal(source)
    pieces = [p.strip(" \"'.,;:") for p in re.split(r"\.\.\.|…", _normal(quote))]
    pieces = [p for p in pieces if p]
    return bool(pieces) and all(len(p) >= MIN_PIECE and p in haystack for p in pieces)


def evidence_sources(log: VisitLog) -> tuple[str, str]:
    """(everything quotable for an item, the clinician's own words for a penalty): the words
    said and found and the plan, never the grader's own labels."""
    said, everything = [], []
    for event in log.events:
        if event.kind == "say" and event.text:
            said.append(event.text)
        elif event.kind in ("reply", "interjection") and event.text:
            everything.append(event.text)
        elif event.kind == "examine":
            everything += [event.request or "", event.text or ""]
    plan = plan_text(log.plan) if log.plan else ""
    return "\n".join([*said, *everything, plan]), "\n".join([*said, plan])


# --- what the judge reads -------------------------------------------------------------------

NO_PLAN = "No plan was submitted: the visit reached its hard cap."


def judge_transcript(log: VisitLog, case: Case) -> str:
    names = display_names(case)
    loc = locale_of(case)
    gp = loc.clinician
    lines = []
    for event in log.events:
        turn = f"[turn {event.turn}]"
        match event.kind:
            case "say":
                lines.append(f"{turn} {gp} to {names.get(event.to or '', event.to)}: {event.text}")
            case "reply":
                lines.append(f"{turn} {names[event.actor]}: {event.text}")
            case "interjection" if event.text:
                lines.append(f"{turn} {names[event.actor]} (adds): {event.text}")
            case "read_record":
                title = next(
                    (t for r, t in loc.record_titles.items() if r.value == event.request),
                    event.request,
                )
                lines.append(f"{turn} {gp} read the {title}")
            case "examine":
                lines.append(f'{turn} {gp} examined "{event.request}": {event.text}')
            case "invalid":
                lines.append(f"{turn} invalid action: {event.error}")
            case "plan":
                lines.append(f"{turn} {gp} submitted the plan")
    return "\n".join(lines) or "(nothing happened)"


def _sources(case: Case, number: int) -> str:
    blocks = []
    for source in SOURCES:
        facts = facts_at(case, source, number)
        if not facts:
            continue
        rows = []
        for f in facts:
            how = ""
            if f.disclosure is not None:
                how = f", {f.disclosure.value}"
                if f.reveal_condition:
                    how += f" (only if {f.reveal_condition})"
            rows.append(f"- [{f.id}] ({f.accuracy.value}{how}) {f.statement}")
        blocks.append(f"{source}:\n" + "\n".join(rows))
    return "\n\n".join(blocks)


def _records_read(log: VisitLog) -> str:
    """Each record the clinician read, as it read it (with its own earlier GP entries)."""
    texts = {e.request: e.text for e in log.events if e.kind == "read_record" and e.text}
    return "\n\n".join(texts.values()) or "(it read no records)"


def visit_context(case: Case, log: VisitLog, earlier: Sequence[VisitLog], facts: LogFacts) -> str:
    visit = get_visit(case, log.visit)
    names = display_names(case)
    truth = "\n".join(
        f"- [{t.id}] ({t.category.value}) {t.statement}"
        for t in case.hidden_truth
        if t.applies_to(log.visit)
    )
    conflicts = "\n".join(
        f"- [{c.id}] facts {', '.join(c.facts)}: {c.expected_behaviour.strip()}"
        for c in case.conflicts
    )
    events = (
        "Since the last visit:\n" + "\n".join(f"- {e.strip()}" for e in visit.events_since_last)
        if visit.events_since_last
        else ""
    )
    earlier_text = ""
    if earlier:
        earlier_text = prompts.GRADER_EARLIER.format(
            plans="\n\n".join(
                f"Visit {e.visit}:\n" + (plan_text(e.plan) if e.plan else NO_PLAN) for e in earlier
            )
        )
    elif log.visit > min(v.number for v in case.visits):
        earlier_text = "\n(Earlier visits are not in this run log.)\n"
    return prompts.GRADER_VISIT.format(
        title=case.title,
        patient=f"{case.patient.name}, {case.patient.age}. {case.patient.summary.strip()}",
        truth=truth,
        sources=_sources(case, log.visit),
        conflicts=conflicts or "(none)",
        number=log.visit,
        setting=locale_of(case).setting_text[visit.setting],
        day=visit.day,
        present=", ".join(names[p.value] for p in visit.present),
        budget=visit.turn_budget,
        reason=visit.reason.strip(),
        events=events,
        earlier=earlier_text,
        log_facts=facts.model_dump_json(indent=1),
        records=_records_read(log),
        transcript=judge_transcript(log, case),
        plan=plan_text(log.plan) if log.plan else NO_PLAN,
    )


# --- judge calls ----------------------------------------------------------------------------


class _Item(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    reason: str = ""
    met: bool
    applicable: bool = True
    evidence: str = ""


class _Found(BaseModel):
    model_config = ConfigDict(extra="ignore")

    quote: str
    reason: str = ""


class _Reply(BaseModel):
    model_config = ConfigDict(extra="ignore")

    items: list[_Item]
    invented_facts: list[_Found] = []
    wrong_fact_actions: list[_Found] = []
    over_provision: list[_Found] = []


class _Ask(BaseModel):
    """One item as the judge is asked about it."""

    id: str
    text: str
    kind: str
    weight: float
    critical: bool = False


class _GroupResult(BaseModel):
    verdicts: list[Verdict]
    penalties: list[Penalty] = []
    errors: list[str] = []


def _problems(
    reply: _Reply, asks: list[_Ask], evidence_text: str, penalty_text: str, safety: bool
) -> list[str]:
    wanted = {a.id for a in asks}
    got = [i.id for i in reply.items]
    problems = []
    if set(got) != wanted or len(got) != len(wanted):
        problems.append(f"give exactly one entry for each of {sorted(wanted)}; you gave {got}")
    for item in reply.items:
        if item.met and not quote_found(item.evidence, evidence_text):
            problems.append(f"the evidence for {item.id} is not an exact quote: {item.evidence!r}")
    if safety:
        for key in _JUDGED_PENALTIES:
            for found in getattr(reply, key):
                if not quote_found(found.quote, penalty_text):
                    problems.append(f"the {key} quote is not exact: {found.quote!r}")
    return problems


async def judge_group(
    judge: Generate,
    context: str,
    group: Group,
    asks: list[_Ask],
    evidence_text: str,
    penalty_text: str,
    loc: Locale,
) -> _GroupResult:
    """One judge call (and at most one retry) for one rubric group at one visit."""
    safety = group == "must_not_do"
    guidance = {
        "critical": prompts.GRADER_RUBRIC_GUIDANCE,
        "must_do": prompts.GRADER_RUBRIC_GUIDANCE,
        "must_not_do": loc.text(prompts.GRADER_SAFETY_GUIDANCE),
        "consultation": prompts.GRADER_CONSULTATION_GUIDANCE,
    }[group]
    items = "\n".join(f"- {a.id}: {a.text}" for a in asks) or "(no items: list penalties only)"
    question = prompts.GRADER_ITEMS.format(
        guidance=guidance,
        items=items,
        applicable='"applicable": true | false, ' if group == "consultation" else "",
        extra=prompts.GRADER_SAFETY_EXTRA if safety else "",
    )
    system = loc.text(prompts.GRADER_SYSTEM)
    messages = [Message("system", system), Message("user", f"{context}\n{question}")]
    reply: _Reply | None = None
    fewest = 0
    problems: list[str] = []
    for attempt in range(2):
        raw = ""
        try:
            raw = await judge(messages)
            candidate = _Reply.model_validate(parse_json_object(raw))
        except (ValueError, ValidationError) as exc:
            problems = [f"unreadable reply: {str(exc)[:300]}"]
        except Exception as exc:  # a provider error must not lose the rest of the run
            problems = [f"judge call failed: {type(exc).__name__}: {str(exc)[:300]}"]
            break
        else:
            problems = _problems(candidate, asks, evidence_text, penalty_text, safety)
            ids_ok = sorted(i.id for i in candidate.items) == sorted(a.id for a in asks)
            # Keep the better of the two replies: a worse retry never replaces a good first.
            if ids_ok and (reply is None or len(problems) <= fewest):
                reply, fewest = candidate, len(problems)
            if not problems:
                break
        if attempt == 0:
            retry = prompts.GRADER_RETRY.format(problem="; ".join(problems))
            messages += [Message("assistant", raw), Message("user", retry)]

    if reply is None:
        error = f"{group}: judge failed after a retry: {'; '.join(problems)}"
        verdicts = [
            Verdict(
                id=a.id, group=group, kind=a.kind, weight=a.weight, critical=a.critical, met=None
            )
            for a in asks
        ]
        return _GroupResult(verdicts=verdicts, errors=[error])

    by_id = {i.id: i for i in reply.items}
    verdicts = []
    for ask in asks:
        item = by_id[ask.id]
        # A "met" whose quote is not in the transcript is neither credited nor a miss.
        found = not item.met or quote_found(item.evidence, evidence_text)
        verdicts.append(
            Verdict(
                id=ask.id,
                group=group,
                kind=ask.kind,
                weight=ask.weight,
                critical=ask.critical,
                met=item.met if found else None,
                applicable=item.applicable if group == "consultation" else True,
                reason=item.reason,
                evidence=item.evidence,
                evidence_verified=found,
            )
        )
    penalties = (
        [
            Penalty(
                type=kind,
                quote=found.quote,
                reason=found.reason,
                weight=PENALTY_WEIGHTS[kind],
                evidence_verified=quote_found(found.quote, penalty_text),
            )
            for key, kind in _JUDGED_PENALTIES.items()
            for found in getattr(reply, key)
        ]
        if safety
        else []
    )
    unverified = [v.id for v in verdicts if not v.evidence_verified]
    unverified += [p.type for p in penalties if not p.evidence_verified]
    errors = (
        [f"{group}: evidence not found in the transcript for {', '.join(unverified)}"]
        if unverified
        else []
    )
    return _GroupResult(verdicts=verdicts, penalties=penalties, errors=errors)


def _rubric_ask(item: RubricItem) -> _Ask:
    return _Ask(
        id=item.id,
        text=f"({item.kind.value}) {' '.join(item.description.split())}",
        kind=item.kind.value,
        weight=item.weight,
        critical=item.critical,
    )


async def grade_visit(
    case: Case,
    log: VisitLog,
    earlier: Sequence[VisitLog],
    judge: Generate,
    consultation: Sequence[ConsultationItem],
) -> VisitScore:
    visit = get_visit(case, log.visit)
    facts = log_facts(log, visit)
    context = visit_context(case, log, earlier, facts)
    evidence_text, penalty_text = evidence_sources(log)

    items = [r for r in case.rubric if r.visit == log.visit]
    groups: dict[Group, list[_Ask]] = {
        # A critical must-not-do is judged with the other must-not-dos, still marked critical.
        "critical": [
            _rubric_ask(r) for r in items if r.critical and r.kind != RubricKind.MUST_NOT_DO
        ],
        "must_do": [
            _rubric_ask(r) for r in items if not r.critical and r.kind != RubricKind.MUST_NOT_DO
        ],
        "must_not_do": [_rubric_ask(r) for r in items if r.kind == RubricKind.MUST_NOT_DO],
    }
    applies = [
        c
        for c in consultation
        if (not c.settings or visit.setting in c.settings) and visit.number >= c.from_visit
    ]
    groups["consultation"] = [
        _Ask(id=c.id, text=c.text(case.country), kind="consultation", weight=c.weight)
        for c in applies
        if c.check is None
    ]
    # The safety group always runs: it also looks for invented facts and over-provision.
    calls = {
        group: judge_group(
            judge, context, group, asks, evidence_text, penalty_text, locale_of(case)
        )
        for group, asks in groups.items()
        if asks or group == "must_not_do"
    }
    results = dict(zip(calls, await asyncio.gather(*calls.values()), strict=True))

    verdicts: list[Verdict] = []
    penalties: list[Penalty] = []
    errors: list[str] = []
    rubric = {r.id: r for r in items}
    for result in results.values():
        penalties += result.penalties
        errors += result.errors
        for verdict in result.verdicts:
            missing = unmet_requirements(rubric[verdict.id], facts) if verdict.id in rubric else []
            if verdict.met and missing:
                verdict = verdict.model_copy(
                    update={"met": False, "overridden": "; ".join(missing)}
                )
            verdicts.append(verdict)
    for item in applies:
        if item.check is not None:
            met, why = _checked(item.check, facts)
            verdicts.append(
                Verdict(
                    id=item.id,
                    group="consultation",
                    kind="consultation",
                    weight=item.weight,
                    met=met,
                    reason=f"from the log: {why}",
                )
            )
    if facts.turns_used > facts.turn_budget:
        penalties.append(
            Penalty(
                type="over_budget",
                quote=f"{facts.turns_used} turns used of a {facts.turn_budget}-turn budget",
                reason="from the log",
                weight=PENALTY_WEIGHTS["over_budget"],
            )
        )
    return score_visit(log.visit, verdicts, penalties, facts, errors)


async def grade_case(
    case: Case,
    log: CaseLog,
    judge: Generate,
    judge_name: str,
    consultation: Sequence[ConsultationItem],
    earlier: Sequence[VisitLog] = (),
) -> CaseScore:
    """Grade every visit in `log`. `earlier` supplies visits run before it (a `--visit N`
    run's `--from` log), used only as context."""
    if log.case_id != case.id:
        raise ValueError(f"the run is of {log.case_id}, not {case.id}")
    clash = {c.id for c in consultation} & {r.id for r in case.rubric}
    if clash:
        raise ValueError(f"consultation and case rubric share ids: {sorted(clash)}")
    ordered = sorted(log.visits, key=lambda v: v.visit)
    known = {v.visit: v for v in [*earlier, *ordered]}
    visits = await asyncio.gather(
        *(
            grade_visit(
                case,
                v,
                [known[n] for n in sorted(known) if n < v.visit],
                judge,
                consultation,
            )
            for v in ordered
        )
    )
    return score_case(case.id, judge_name, list(visits))


# --- several judges -------------------------------------------------------------------------


class Agreement(_Model):
    judges: tuple[str, str]
    items: int
    agreed: int
    critical_items: int
    critical_agreed: int


def agreement(scores: Sequence[CaseScore]) -> list[Agreement]:
    """Raw item-level agreement between each pair of judges on the same run."""
    out = []
    for a, b in combinations(scores, 2):
        left = {(v.visit, x.id): x for v in a.visits for x in v.verdicts}
        right = {(v.visit, x.id): x for v in b.visits for x in v.verdicts}
        pairs = [
            (left[k], right[k])
            for k in left.keys() & right.keys()
            if left[k].met is not None
            and right[k].met is not None
            and left[k].applicable
            and right[k].applicable
        ]
        critical = [(x, y) for x, y in pairs if x.critical]
        out.append(
            Agreement(
                judges=(a.judge, b.judge),
                items=len(pairs),
                agreed=sum(x.met == y.met for x, y in pairs),
                critical_items=len(critical),
                critical_agreed=sum(x.met == y.met for x, y in critical),
            )
        )
    return out


LabMatch = Literal["other_lab", "same_lab", "unknown"]


def primary_judge(judges: Sequence[str], clinician: str | None) -> tuple[str, LabMatch]:
    """The first judge from a lab (provider prefix) other than the clinician's. With only
    same-lab judges (development), the first judge, flagged; with a human or unrecorded
    clinician, the first judge. A routing provider (e.g. openrouter) is not mapped to a lab."""
    lab = clinician.split("/", 1)[0] if clinician and "/" in clinician else None
    if lab is None:
        return judges[0], "unknown"
    for judge in judges:
        if judge.split("/", 1)[0] != lab:
            return judge, "other_lab"
    return judges[0], "same_lab"


class GradeReport(_Model):
    case_id: str
    run: str
    clinician: str | None
    primary: str
    primary_lab: LabMatch
    scores: list[CaseScore]
    agreement: list[Agreement]
