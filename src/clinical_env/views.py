"""What each party may see at a visit. Every prompt is built from these functions only.

The clinician sees the briefing, records it reads and findings it examines. Each person sees
only their own facts. Hidden truth, the rubric, conflicts, case notes and the between-visit
events never leave the case file through here (tests/test_views.py checks this).
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass
from datetime import date, timedelta

from clinical_env.case_schema import Case, Fact, Person, Persona, Record, Visit
from clinical_env.locale import locale_of

# Visit 1 of every case falls on this fictional date. Case files hold only day offsets
# (validate.py rejects absolute dates there), so dates appear only when a record is rendered.
DAY_ZERO = date(2026, 11, 5)
PLACEHOLDER = re.compile(r"\[\[([A-Za-z0-9_]+)\]\]")
DATE_TOKEN = re.compile(r"\{(day|weekday):(-?\d+)\}")
DATE_FORMATS = {"day": "%d %b %Y", "weekday": "%a %d %b"}


def get_visit(case: Case, number: int) -> Visit:
    for visit in case.visits:
        if visit.number == number:
            return visit
    raise ValueError(f"case {case.id} has no visit {number}")


def facts_at(case: Case, source: str, visit: int) -> list[Fact]:
    return [fact for fact in case.views.get(source, []) if fact.applies_to(visit)]


def persona(case: Case, person: Person) -> Persona:
    found = case.personas.patient if person == Person.PATIENT else case.personas.carer
    if found is None:
        raise ValueError(f"case {case.id} has no {person.value} persona")
    return found


def describe(case: Case, person: Person) -> str:
    """How the clinician knows a person, e.g. 'Janet Price (daughter)'."""
    who = persona(case, person)
    if person == Person.PATIENT:
        return f"{who.name} (patient)"
    return f"{who.name} ({who.relationship or 'carer'})"


def visit_date(visit: Visit) -> date:
    return DAY_ZERO + timedelta(days=visit.day)


def display_names(case: Case) -> dict[str, str]:
    """'patient'/'carer' to each person's name, for transcripts."""
    names = {Person.PATIENT.value: case.personas.patient.name}
    if case.personas.carer is not None:
        names[Person.CARER.value] = persona(case, Person.CARER).name
    return names


def visit_heading(case: Case, visit: Visit, today: int | None = None) -> str:
    """E.g. 'Visit 1, home visit, Thursday 5 November 2026 (14 days ago)'."""
    day = visit_date(visit)
    setting = locale_of(case).setting_text[visit.setting]
    text = f"Visit {visit.number}, {setting}, {day:%A} {day.day} {day:%B %Y}"
    if today is not None and today > visit.day:
        text += f" ({today - visit.day} days ago)"
    return text


def clinician_briefing(case: Case, number: int, notes: str = "") -> str:
    """The clinician's opening view of a visit: no truth, rubric, events or other views.

    `notes` is what the clinician carries from earlier visits (case_run.py builds it from
    its own earlier plans, never from the case file)."""
    visit = get_visit(case, number)
    loc = locale_of(case)
    present = ", ".join(describe(case, p) for p in visit.present)
    records = ", ".join(f"{loc.record_titles[r]} ({r.value})" for r in visit.records_available)
    day = visit_date(visit)
    when = f"{day:%A} {day.day} {day:%B %Y}"
    lines = [
        f"Visit {visit.number}: {loc.setting_text[visit.setting]}, {when}.",
        f"Patient: {case.patient.name}, {case.patient.age}. {case.patient.summary.strip()}",
        f"Present: {present}.",
        f"Reason for this visit: {visit.reason.strip()}",
        f"Records you can read: {records or 'none'}.",
    ]
    if notes:
        lines += ["", notes]
    return "\n".join(lines)


@dataclass(frozen=True)
class RecordEntry:
    """A dated entry added to a record by the run (the clinician's own earlier consultation),
    not by the case file."""

    day: int
    author: str
    text: str


# A line holding only this marks where run entries go (the GP record's consultations).
ENTRIES_MARKER = "{entries}"
ENTRY_AUTHOR_WIDTH = 16  # matches the case files' consultation columns
ENTRY_WIDTH = 100


def _entry_lines(entry: RecordEntry, indent: str) -> list[str]:
    lead = f"{indent}{_date_text('day', entry.day)}  {entry.author:<{ENTRY_AUTHOR_WIDTH}}"
    return textwrap.wrap(
        " ".join(entry.text.split()),
        width=ENTRY_WIDTH,
        initial_indent=lead,
        subsequent_indent=" " * len(lead),
    )


def record_text(
    case: Case, record: Record, number: int, entries: tuple[RecordEntry, ...] = ()
) -> str:
    """A record as the clinician reads it at this visit.

    With a document, each [[fact_id]] becomes that fact's statement and each date token a
    date. A line is dropped when it names a fact that does not apply at this visit or carries
    a date after the visit (it has not happened yet). Without one, facts are listed.
    `entries` (dated before this visit) go in the section that starts at the document's
    {entries} line (it ends at a blank line), in date order, most recent first. A document
    without that line shows them at its end.
    """
    facts = facts_at(case, record.value, number)
    today = get_visit(case, number).day
    entries = tuple(sorted((e for e in entries if e.day < today), key=lambda e: -e.day))
    title = locale_of(case).record_titles[record]
    template = case.documents.get(record)
    if template is None:
        body = [f"- {fact.statement.strip()}" for fact in facts]
        body += [f"- {_date_text('day', e.day)} {e.author}: {e.text}" for e in entries]
        return f"{title}:\n" + ("\n".join(body) or "- (no entries)")
    shown = {fact.id: " ".join(fact.statement.split()) for fact in facts}
    lines: list[tuple[int | None, str]] = []  # (leading date offset, rendered line)
    marker: tuple[int, str] | None = None  # (index, indent) of the {entries} line
    for line in template.strip("\n").splitlines():
        indent = line[: len(line) - len(line.lstrip())]
        if line.strip() == ENTRIES_MARKER:
            marker = (len(lines), indent)
            continue
        if any(ref not in shown for ref in PLACEHOLDER.findall(line)):
            continue
        if any(int(offset) > today for _, offset in DATE_TOKEN.findall(line)):
            continue
        lead = DATE_TOKEN.match(line.lstrip())
        line = PLACEHOLDER.sub(lambda m: shown[m.group(1)], line)
        lines.append((int(lead.group(2)) if lead else None, DATE_TOKEN.sub(_date, line).rstrip()))
    start, indent = marker if marker else (len(lines), "")
    end = next((i for i in range(start, len(lines)) if not lines[i][1].strip()), len(lines))
    for entry in entries:  # newest first: each goes above the first older dated line
        at = next(
            (i for i in range(start, end) if (off := lines[i][0]) is not None and off < entry.day),
            end,
        )
        new = [(entry.day, text) for text in _entry_lines(entry, indent)]
        lines[at:at] = new
        end += len(new)
    return f"{title}:\n" + ("\n".join(t for _, t in lines) or "(no entries)")


def _date_text(kind: str, offset: int) -> str:
    return (DAY_ZERO + timedelta(days=offset)).strftime(DATE_FORMATS[kind])


def _date(match: re.Match[str]) -> str:
    kind, offset = match.groups()
    return _date_text(kind, int(offset))
