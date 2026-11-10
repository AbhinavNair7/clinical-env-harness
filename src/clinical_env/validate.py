"""Load case files and check the cross-references Pydantic cannot (docs/build-v0.md, DECISIONS.md).

Every check appends a readable message instead of raising, so an author sees all problems in a
case at once. A case is valid when its error list is empty.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from pydantic import ValidationError

from clinical_env.case_schema import (
    SOURCES,
    Accuracy,
    Case,
    Country,
    CriticalType,
    Disclosure,
    Fact,
    Person,
    PersonTrait,
    Record,
    RecordTrait,
    RubricItem,
    RubricKind,
    Setting,
    TruthItem,
    TwinSpec,
    Visit,
)
from clinical_env.locale import UK_TERMS
from clinical_env.views import DATE_TOKEN, ENTRIES_MARKER, PLACEHOLDER

MIN_VISITS, MAX_VISITS = 2, 3
MIN_CRITICALS, MAX_CRITICALS = (
    2,
    5,
)  # 5 only where 3 visits each need their own (the clinical lead, 5 Nov)
# A twin keeps only the base case's clinical_action criticals, so it may have fewer than two.
MIN_TWIN_CRITICALS = 1

# Case content must be fictional. These shapes suggest a real identifier was pasted in:
# an NHS number (3-3-4 digits, which also catches US phone numbers), a US social security or
# medical record number, or an absolute date in UK or US order (cases use relative times).
_MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
IDENTIFIER_PATTERNS = {
    "an NHS number": re.compile(r"\b\d{3}[ -]?\d{3}[ -]?\d{4}\b"),
    "a social security number": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "a medical record number": re.compile(r"\bMRN\b\W*\d{4,}", re.IGNORECASE),
    "an absolute date": re.compile(
        r"\b\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}\b"
        r"|\b(?:19|20)\d{2}-\d{2}-\d{2}\b"
        rf"|\b\d{{1,2}}(?:st|nd|rd|th)? (?:{_MONTHS}),? (?:19|20)\d{{2}}\b"
        rf"|\b(?:{_MONTHS}) \d{{1,2}}(?:st|nd|rd|th)?,? (?:19|20)\d{{2}}\b",
        re.IGNORECASE,
    ),
}

PERSON_SOURCES = {p.value for p in Person}
RECORD_SOURCES = {r.value for r in Record}


@dataclass
class FileResult:
    path: Path
    case_id: str | None = None
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass
class _Loaded:
    path: Path
    model: Case | TwinSpec


def check_case(case: Case, *, is_twin: bool = False) -> list[str]:
    """Return every cross-reference problem in a (resolved) case."""
    errors: list[str] = []
    errors += _duplicate_ids(case)
    visit_numbers = [v.number for v in case.visits]
    n_visits = len(visit_numbers)

    if visit_numbers != list(range(1, n_visits + 1)):
        errors.append(f"visits must be numbered 1..{n_visits} in order, got {visit_numbers}")
    if not MIN_VISITS <= n_visits <= MAX_VISITS:
        errors.append(f"a case needs {MIN_VISITS}-{MAX_VISITS} visits, got {n_visits}")

    truth = {t.id: t for t in case.hidden_truth}
    truth_ids = set(truth)
    for item in case.hidden_truth:
        errors += _window_errors(f"truth {item.id}", item.from_visit, item.until_visit, n_visits)

    errors += _view_errors(case, truth, n_visits, is_twin=is_twin)
    errors += _persona_errors(case)
    errors += _record_trait_errors(case)
    errors += _conflict_errors(case, truth_ids, is_twin=is_twin)
    errors += _visit_errors(case)
    errors += _document_errors(case)
    errors += _rubric_errors(case, n_visits, is_twin=is_twin)
    errors += _country_errors(case)
    return errors


def _strings(value: object) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list | tuple):
        for item in value:
            yield from _strings(item)


def _country_errors(case: Case) -> list[str]:
    """A US case must not read as British: every model reads its content (notes excepted)."""
    if case.country != Country.US:
        return []
    found = sorted(
        {
            m.group()
            for text in _strings(case.model_dump(exclude={"notes"}))
            for m in UK_TERMS.finditer(text)
        }
    )
    return [f"country us: UK wording {', '.join(repr(w) for w in found)}"] if found else []


def check_twin(twin: Case, base: Case) -> list[str]:
    """Twin-only rules: the twin's criticals are exactly the base's clinical_action criticals."""
    errors: list[str] = []
    twin_items = {r.id: r for r in twin.rubric}
    base_actions = [
        r for r in base.rubric if r.critical and r.critical_type == CriticalType.CLINICAL_ACTION
    ]
    for item in base_actions:
        mine = twin_items.get(item.id)
        # Evidence names the base's own fact ids; a twin's facts differ, so it is not compared.
        if mine is None or mine.model_copy(update={"evidence": []}) != item.model_copy(
            update={"evidence": []}
        ):
            errors.append(
                f"twin must keep clinical_action critical {item.id} from {base.id} unchanged"
            )
    allowed = {r.id for r in base_actions}
    for item in twin.rubric:
        if item.critical and item.id not in allowed:
            errors.append(
                f"rubric {item.id}: a twin's criticals must be the base's clinical_action "
                "criticals; it cannot add new ones"
            )
    if not base_actions:
        errors.append(f"base case {base.id} has no clinical_action critical, so a twin is useless")
    return errors


def validate_paths(paths: Sequence[Path]) -> list[FileResult]:
    """Validate case files (or every *.yaml in given directories), resolving twins."""
    files = _expand(paths)
    results: dict[Path, FileResult] = {}
    loaded: dict[str, _Loaded] = {}

    for path in files:
        result = FileResult(path)
        results[path] = result
        model = _load(path, result)
        if model is None:
            continue
        result.case_id = model.id
        if path.stem != model.id:
            result.errors.append(f"file name must match case id: rename to {model.id}.yaml")
        if model.id in loaded:
            result.errors.append(f"case id {model.id} also used by {loaded[model.id].path}")
            continue
        loaded[model.id] = _Loaded(path, model)

    for item in loaded.values():
        result = results[item.path]
        model = item.model
        if isinstance(model, Case):
            result.errors += check_case(model)
            continue
        base = _find_base(model, item.path, loaded, result)
        if base is None:
            continue
        twin = model.resolve(base)
        result.errors += check_case(twin, is_twin=True)
        result.errors += check_twin(twin, base)

    return [results[p] for p in files]


def _expand(paths: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        for file in sorted(path.glob("*.yaml")) if path.is_dir() else [path]:
            if file.resolve() not in seen:
                seen.add(file.resolve())
                files.append(file)
    return files


def _load(path: Path, result: FileResult) -> Case | TwinSpec | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        result.errors.append(f"cannot read file: {exc.strerror or exc}")
        return None
    for what, pattern in IDENTIFIER_PATTERNS.items():
        match = pattern.search(text)
        if match:
            result.errors.append(
                f"'{match.group()}' looks like {what}; case content must be fictional "
                "(use relative times such as '3 weeks ago')"
            )
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        result.errors.append(f"invalid YAML: {exc}")
        return None
    if not isinstance(data, dict):
        result.errors.append("a case file must be a YAML mapping")
        return None
    model_type: type[Case] | type[TwinSpec] = TwinSpec if "twin_of" in data else Case
    try:
        return model_type.model_validate(data)
    except ValidationError as exc:
        for error in exc.errors():
            location = ".".join(str(part) for part in error["loc"]) or "(top level)"
            result.errors.append(f"{location}: {error['msg']}")
        return None


def _find_base(
    twin: TwinSpec, path: Path, loaded: dict[str, _Loaded], result: FileResult
) -> Case | None:
    if twin.twin_of in loaded:
        candidate: Case | TwinSpec | None = loaded[twin.twin_of].model
    else:
        sibling = path.parent / f"{twin.twin_of}.yaml"
        if not sibling.is_file():
            result.errors.append(f"twin_of {twin.twin_of}: no {sibling.name} beside this file")
            return None
        candidate = _load(sibling, FileResult(sibling))
        if isinstance(candidate, Case) and check_case(candidate):
            candidate = None
        if candidate is None:
            result.errors.append(f"twin_of {twin.twin_of}: base case is invalid; fix it first")
            return None
    if not isinstance(candidate, Case):
        result.errors.append(f"twin_of {twin.twin_of} is itself a twin")
        return None
    return candidate


def _duplicate_ids(case: Case) -> list[str]:
    groups = {
        "truth": [t.id for t in case.hidden_truth],
        "fact": [f.id for facts in case.views.values() for f in facts],
        "conflict": [c.id for c in case.conflicts],
        "rubric": [r.id for r in case.rubric],
        "exam finding": [e.id for v in case.visits for e in v.examination],
        "test result": [r.id for v in case.visits for r in v.results or []],
    }
    return [
        f"duplicate {kind} id {item_id}"
        for kind, ids in groups.items()
        for item_id, count in Counter(ids).items()
        if count > 1
    ]


def _window_errors(label: str, start: int, end: int | None, n_visits: int) -> list[str]:
    errors = []
    if start > n_visits:
        errors.append(f"{label}: from_visit {start} is after the last visit ({n_visits})")
    if end is not None and (end < start or end > n_visits):
        errors.append(f"{label}: until_visit {end} must be between {start} and {n_visits}")
    return errors


def _view_errors(
    case: Case, truth: dict[str, TruthItem], n_visits: int, *, is_twin: bool
) -> list[str]:
    errors: list[str] = []
    for source, facts in case.views.items():
        if source not in SOURCES:
            errors.append(f"views: unknown source {source}; use one of {', '.join(SOURCES)}")
            continue
        for fact in facts:
            label = f"fact {fact.id} ({source})"
            errors += _window_errors(label, fact.from_visit, fact.until_visit, n_visits)
            about = truth.get(fact.truth)
            if about is None:
                errors.append(f"{label}: truth {fact.truth} is not a hidden_truth id")
            else:
                errors += _fact_truth_window(label, fact, about)
            if source in PERSON_SOURCES and not any(
                Person(source) in v.present and fact.applies_to(v.number) for v in case.visits
            ):
                errors.append(f"{label}: {source} is never present at a visit this fact applies to")
            if source in PERSON_SOURCES and fact.disclosure is None:
                errors.append(f"{label}: a person's fact needs disclosure")
            if source in RECORD_SOURCES and fact.disclosure is not None:
                errors.append(
                    f"{label}: records have no disclosure; reading shows the whole record"
                )
            if fact.disclosure == Disclosure.HIDDEN and not (fact.reveal_condition or "").strip():
                errors.append(f"{label}: a hidden fact needs a reveal_condition")
            if fact.disclosure != Disclosure.HIDDEN and fact.reveal_condition is not None:
                errors.append(f"{label}: reveal_condition is only for hidden facts")
            if is_twin and fact.accuracy != Accuracy.TRUE:
                errors.append(f"{label}: a twin's sources are all accurate, got {fact.accuracy}")

    if Person.CARER.value in case.views and case.personas.carer is None:
        errors.append("views: a carer view needs a carer persona")
    if Person.PATIENT.value not in case.views:
        errors.append("views: the patient needs a view")
    return errors


def _fact_truth_window(label: str, fact: Fact, about: TruthItem) -> list[str]:
    # A source cannot know about something before it happens; an accurate one cannot keep
    # describing it after it stops being true.
    if fact.from_visit < about.from_visit:
        return [
            f"{label}: applies from visit {fact.from_visit} but truth {about.id} "
            f"only starts at visit {about.from_visit}"
        ]
    if (
        fact.accuracy == Accuracy.TRUE
        and about.until_visit is not None
        and (fact.until_visit is None or fact.until_visit > about.until_visit)
    ):
        return [f"{label}: is true after truth {about.id} ends (visit {about.until_visit})"]
    return []


def _persona_errors(case: Case) -> list[str]:
    errors = []
    carer = case.personas.carer
    if carer is not None and Person.CARER.value not in case.views:
        errors.append("personas: a carer persona needs a carer view")
    if PersonTrait.CARER_DOMINATES in case.personas.patient.traits:
        errors.append("personas.patient: carer_dominates is a carer trait")
    return errors


def _record_trait_errors(case: Case) -> list[str]:
    """A tag must match what the facts show, so the messiness spread is real, not claimed."""
    errors = []
    in_conflict = {f for c in case.conflicts for f in c.facts}
    for record, traits in case.record_traits.items():
        label = f"record_traits.{record.value}"
        facts = case.views.get(record.value)
        if facts is None:
            errors.append(f"{label}: the case has no {record.value} view")
            continue
        if RecordTrait.CONTRADICTS_OTHER_RECORDS in traits and not any(
            f.id in in_conflict for f in facts
        ):
            errors.append(
                f"{label}: contradicts_other_records, but none of its facts is in a conflict"
            )
        if RecordTrait.OUTDATED_ENTRIES in traits and not any(
            f.accuracy == Accuracy.OUTDATED for f in facts
        ):
            errors.append(f"{label}: outdated_entries, but none of its facts is outdated")
    return errors


def _conflict_errors(case: Case, truth_ids: set[str], *, is_twin: bool) -> list[str]:
    errors: list[str] = []
    facts = {f.id: f for fs in case.views.values() for f in fs}
    in_conflict: set[str] = set()
    for conflict in case.conflicts:
        label = f"conflict {conflict.id}"
        if len(set(conflict.facts)) != len(conflict.facts):
            errors.append(f"{label}: a fact is listed twice")
        for fact_id in conflict.facts:
            if fact_id not in facts:
                errors.append(f"{label}: fact {fact_id} is not in any view")
            elif facts[fact_id].truth not in conflict.truth:
                errors.append(
                    f"{label}: fact {fact_id} is about {facts[fact_id].truth}, "
                    "which is not in this conflict's truth"
                )
        for truth_id in conflict.truth:
            if truth_id not in truth_ids:
                errors.append(f"{label}: truth {truth_id} is not a hidden_truth id")
        known = [facts[f] for f in conflict.facts if f in facts]
        if known and all(f.accuracy == Accuracy.TRUE for f in known):
            errors.append(f"{label}: every fact is true, so nothing disagrees")
        in_conflict.update(conflict.facts)

    if not is_twin:
        if not case.conflicts:
            errors.append("conflicts: a case needs at least one conflict between sources")
        for fact in facts.values():
            if fact.accuracy != Accuracy.TRUE and fact.id not in in_conflict:
                errors.append(f"fact {fact.id} is {fact.accuracy} but in no conflict")
    return errors


def _exam_set_errors(label: str, visit: Visit) -> list[str]:
    """A finding has its own text or is a set of other single findings, never both."""
    errors: list[str] = []
    findings = {f.id: f for f in visit.examination}
    for f in visit.examination:
        where = f"{label}: exam finding {f.id}"
        if (f.finding is None) == (not f.parts):
            errors.append(f"{where} needs either a finding or parts, not both or neither")
        if f.parts and len(set(f.parts)) < 2:
            errors.append(f"{where}: a set needs at least two different parts")
        for part in f.parts:
            if part not in findings or part == f.id:
                errors.append(f"{where}: part {part} is not another finding at this visit")
            elif findings[part].parts:
                errors.append(f"{where}: part {part} is itself a set")
    return errors


def _visit_errors(case: Case) -> list[str]:
    errors: list[str] = []
    for visit in case.visits:
        label = f"visit {visit.number}"
        if visit.number == 1 and visit.events_since_last:
            errors.append(f"{label}: the first visit has no events_since_last")
        if visit.setting == Setting.PHONE and visit.examination:
            errors.append(f"{label}: a phone visit has no examination findings")
        errors += _exam_set_errors(label, visit)
        if Person.CARER in visit.present and case.personas.carer is None:
            errors.append(f"{label}: carer present but the case has no carer persona")
        if len(set(visit.present)) != len(visit.present):
            errors.append(f"{label}: someone is listed twice in present")
        if visit.results and visit.number == len(case.visits):
            errors.append(
                f"{label}: results on the last visit are never seen (they come back later)"
            )
        following = next((v for v in case.visits if v.number == visit.number + 1), None)
        if visit.results and following and Record.GP_RECORD not in following.records_available:
            errors.append(
                f"{label}: results land in gp_record, which visit {following.number} cannot read"
            )
    days = [v.day for v in case.visits]
    if days and days[0] != 0:
        errors.append("visit 1 must be day 0 (days count from the first visit)")
    if any(later <= earlier for earlier, later in zip(days, days[1:], strict=False)):
        errors.append(f"visit days must increase, got {days}")

    for source in RECORD_SOURCES & case.views.keys():
        facts = case.views[source]
        reachable = any(
            Record(source) in v.records_available and any(f.applies_to(v.number) for f in facts)
            for v in case.visits
        )
        if facts and not reachable:
            errors.append(f"views: {source} has facts but is never available when they apply")
    return errors


def _document_errors(case: Case) -> list[str]:
    """Every fact in a written-out record appears once, on a line dated no later than the
    first visit it applies to; every slot names one of that record's facts."""
    errors: list[str] = []
    day_of = {v.number: v.day for v in case.visits}
    available = {r for v in case.visits for r in v.records_available}
    for record, text in case.documents.items():
        label = f"documents.{record.value}"
        if record not in available:
            errors.append(f"{label}: this record is never available at a visit")
        facts = {f.id: f for f in case.views.get(record.value, [])}
        seen: Counter[str] = Counter()
        markers = sum(line.strip() == ENTRIES_MARKER for line in text.splitlines())
        if markers > 1 or (markers and record != Record.GP_RECORD):
            errors.append(f"{label}: {ENTRIES_MARKER} goes on one line of the gp_record only")
        for line in text.splitlines():
            for bad in re.findall(r"\{(?:day|weekday)[^}]*\}", line):
                if not DATE_TOKEN.fullmatch(bad):
                    errors.append(f"{label}: bad date {bad}; use {{day:-21}} or {{weekday:-9}}")
            dated = [int(offset) for _, offset in DATE_TOKEN.findall(line)]
            for ref in PLACEHOLDER.findall(line):
                seen[ref] += 1
                fact = facts.get(ref)
                if fact is None:
                    errors.append(f"{label}: [[{ref}]] is not a fact in the {record.value} view")
                elif dated and max(dated) > day_of.get(fact.from_visit, 0):
                    errors.append(
                        f"{label}: [[{ref}]] sits on a line dated after visit "
                        f"{fact.from_visit}, so it would be hidden when it applies"
                    )
        for fact_id in facts:
            if seen[fact_id] != 1:
                errors.append(
                    f"{label}: fact {fact_id} must appear exactly once, found {seen[fact_id]}"
                )
    return errors


def _rubric_errors(case: Case, n_visits: int, *, is_twin: bool) -> list[str]:
    errors: list[str] = []
    criticals = 0
    for item in case.rubric:
        label = f"rubric {item.id}"
        if item.visit > n_visits:
            errors.append(f"{label}: visit {item.visit} does not exist")
        if item.critical:
            criticals += 1
            if item.critical_type is None:
                errors.append(f"{label}: a critical item needs critical_type")
            if item.stage is None:
                errors.append(f"{label}: a critical item needs a stage")
            if is_twin and item.critical_type == CriticalType.DISCREPANCY_DETECTION:
                errors.append(f"{label}: a twin has no conflicts, so no discrepancy_detection")
            elif item.critical_type == CriticalType.DISCREPANCY_DETECTION and not case.conflicts:
                errors.append(f"{label}: discrepancy_detection needs a conflict in the case")
        elif item.critical_type is not None:
            errors.append(f"{label}: critical_type is only for critical items")
        if item.requires is not None:
            errors += _requires_errors(case, item)
        if item.critical and not is_twin:
            errors += _evidence_errors(case, item)

    low = MIN_TWIN_CRITICALS if is_twin else MIN_CRITICALS
    if not low <= criticals <= MAX_CRITICALS:
        errors.append(f"a case needs {low}-{MAX_CRITICALS} critical items, got {criticals}")
    return errors


EARNED_DISCLOSURES = {Disclosure.IF_ASKED, Disclosure.HIDDEN}


def _evidence_errors(case: Case, item: RubricItem) -> list[str]:
    """A critical must rest on something the clinician has to earn: a fact a person gives only
    when asked, an examination finding, a test result, or a fact that appears after visit 1.
    Otherwise the answer is sitting in a document, which models read and pass."""
    label = f"rubric {item.id}: evidence"
    if not item.evidence:
        return [f"{label}: a critical item lists the ids it depends on"]
    persons = {p.value for p in Person}
    facts = {f.id: (source, f) for source, fs in case.views.items() for f in fs}
    found = {e.id: v.number for v in case.visits for e in v.examination}
    results = {r.id: v.number for v in case.visits for r in v.results or []}
    errors = []
    earned = False
    for ref in item.evidence:
        if ref in facts:
            source, fact = facts[ref]
            if fact.from_visit > item.visit:
                errors.append(f"{label} {ref} only applies from visit {fact.from_visit}")
            # A later visit's record line alone is still the answer sitting in a document.
            earned |= source in persons and (
                fact.disclosure in EARNED_DISCLOSURES or fact.from_visit > 1
            )
        elif ref in found or ref in results:
            at = found.get(ref, results.get(ref, 0))
            # A result ordered at visit n is seen at visit n + 1.
            seen = at if ref in found else at + 1
            if seen > item.visit:
                errors.append(f"{label} {ref} is not available by visit {item.visit}")
            earned = True
        else:
            errors.append(f"{label} {ref}: no such fact, examination finding or test result")
    if not earned:
        errors.append(
            f"{label}: everything listed is in a record or volunteered; a critical needs at "
            "least one fact a person gives when asked (or says at a later visit), an "
            "examination finding or a test result"
        )
    return errors


def _requires_errors(case: Case, item: RubricItem) -> list[str]:
    label = f"rubric {item.id}: requires"
    requires = item.requires
    if requires is None:
        return []
    if item.kind == RubricKind.MUST_NOT_DO:
        return [f"{label} is only for must_do or red_flag items"]
    visit = next((v for v in case.visits if v.number == item.visit), None)
    if visit is None:
        return []  # reported above as a missing visit
    errors = []
    exams = {f.id for f in visit.examination}
    errors += [
        f"{label} examined {i}: no such finding at visit {visit.number}"
        for i in requires.examined
        if i not in exams
    ]
    errors += [
        f"{label} read {r.value}: not available at visit {visit.number}"
        for r in requires.read
        if r not in visit.records_available
    ]
    errors += [
        f"{label} spoke_to {p.value}: not present at visit {visit.number}"
        for p in requires.spoke_to
        if p not in visit.present
    ]
    return errors


class CaseError(Exception):
    """A case file failed validation; the message lists every problem."""


def load_case(path: Path) -> Case:
    """Load one valid case (a twin is resolved against its base), or raise CaseError."""
    results = validate_paths([path])
    if not results:
        raise CaseError(f"{path}: no case file found")
    result = results[0]
    if not result.ok:
        raise CaseError(f"{path} is invalid:\n" + "\n".join(f"  - {e}" for e in result.errors))
    model = _load(path, FileResult(path))
    if isinstance(model, TwinSpec):
        base = _find_base(model, path, {}, FileResult(path))
        if base is None:  # unreachable after a passing validation; kept for type narrowing
            raise CaseError(f"{path}: twin base not found")
        return model.resolve(base)
    if model is None:
        raise CaseError(f"{path}: could not load")
    return model
