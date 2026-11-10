"""Case file schema: the shape of one YAML case (see docs/build-v0.md, "Case files").

Pydantic checks shape and types only. Cross-references between parts of a case (fact ids,
critical counts, twins) are checked in `validate.py`, so an author sees every problem at once.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Strict(BaseModel):
    # Unknown keys are almost always typos in a hand-written case; reject them.
    model_config = ConfigDict(extra="forbid", frozen=True)


class Person(StrEnum):
    PATIENT = "patient"
    CARER = "carer"


class Record(StrEnum):
    GP_RECORD = "gp_record"
    CARE_AGENCY_NOTES = "care_agency_notes"
    DISCHARGE_SUMMARY = "discharge_summary"
    PHARMACY_RECORD = "pharmacy_record"
    AMBULANCE_REPORT = "ambulance_report"


SOURCES: tuple[str, ...] = tuple(p.value for p in Person) + tuple(r.value for r in Record)


class Accuracy(StrEnum):
    TRUE = "true"
    WRONG = "wrong"
    OUTDATED = "outdated"


class Disclosure(StrEnum):
    """How a person gives up a fact. Records have no disclosure: reading one shows all of it."""

    VOLUNTEERED = "volunteered"
    IF_ASKED = "if_asked"
    HIDDEN = "hidden"


class Interjection(StrEnum):
    ALWAYS = "always"
    SOMETIMES = "sometimes"
    NEVER = "never"


class Setting(StrEnum):
    HOME_VISIT = "home_visit"
    PHONE = "phone"
    CLINIC = "clinic"


class TruthCategory(StrEnum):
    MOBILITY = "mobility"
    FALLS = "falls"
    ADLS = "adls"
    COGNITION = "cognition"
    MEDICINES = "medicines"
    CARE_DELIVERED = "care_delivered"
    CARER_STRAIN = "carer_strain"
    RISKS = "risks"
    OTHER = "other"


class RubricKind(StrEnum):
    MUST_DO = "must_do"
    MUST_NOT_DO = "must_not_do"
    RED_FLAG = "red_flag"


class CriticalType(StrEnum):
    CLINICAL_ACTION = "clinical_action"  # needed whatever the sources say
    DISCREPANCY_DETECTION = "discrepancy_detection"  # exists only because sources conflict


class Stage(StrEnum):
    """The consultation stage a rubric item belongs to, so a case can later run as a narrow
    slice (e.g. referral triage) scored only on that stage's items."""

    INTAKE = "intake"
    TRIAGE = "triage"
    HISTORY = "history"
    RECORDS = "records"
    EXAMINATION = "examination"
    PLAN = "plan"
    FOLLOW_UP = "follow_up"


class Country(StrEnum):
    """The health system a case is set in. Every word a model reads about the setting (the
    clinician's role, record titles, referral routes) follows it; see locale.py."""

    UK = "uk"
    US = "us"


class Messiness(StrEnum):
    """How messy a case is overall; the pilot set aims for a spread, including near-clean."""

    MILD = "mild"
    MODERATE = "moderate"
    HIGH = "high"


class PersonTrait(StrEnum):
    """How a person makes the history harder to get. Simulators default to tidy, so a trait
    shapes how they talk; anything wrong they say must still be a scripted fact."""

    DENIES_MINIMISES = "denies_minimises"  # falls, alcohol, not coping
    TANGENTS = "tangents"
    POOR_RECALL = "poor_recall"  # vague about medicine names, times and dates
    CARER_DOMINATES = "carer_dominates"  # answers for or contradicts the patient (carer only)


class RecordTrait(StrEnum):
    """What makes a record messy. Authoring tags: the mess itself is written into the facts
    and the document."""

    CONTRADICTS_OTHER_RECORDS = "contradicts_other_records"
    CONTRADICTS_ITSELF = "contradicts_itself"
    MISCODED = "miscoded"  # or a wrong diagnosis carried forward
    LONG_NOISY = "long_noisy"
    OUTDATED_ENTRIES = "outdated_entries"  # e.g. a stopped medicine still listed


class Window(Strict):
    """Visits an item applies to, from_visit to until_visit inclusive (open-ended if None)."""

    from_visit: int = Field(default=1, ge=1)
    until_visit: int | None = Field(default=None, ge=1)

    def applies_to(self, visit: int) -> bool:
        return self.from_visit <= visit and (self.until_visit is None or visit <= self.until_visit)


class TruthItem(Window):
    id: str = Field(min_length=1)
    category: TruthCategory
    statement: str = Field(min_length=1)


class Fact(Window):
    id: str = Field(min_length=1)
    truth: str = Field(min_length=1, description="id of the truth item this fact is about")
    statement: str = Field(min_length=1)
    accuracy: Accuracy
    disclosure: Disclosure | None = None
    reveal_condition: str | None = Field(
        default=None, description="the question that earns a hidden fact (checker uses it)"
    )


class Persona(Strict):
    name: str = Field(min_length=1)
    age: int | None = Field(default=None, ge=0)
    relationship: str | None = Field(default=None, description="carer only, e.g. daughter")
    cognition: str = Field(min_length=1)
    health_literacy: str = Field(min_length=1)
    agenda: str = Field(min_length=1)
    speech_style: str = Field(min_length=1)
    interjection: Interjection
    traits: list[PersonTrait] = Field(default_factory=list)


class Personas(Strict):
    patient: Persona
    carer: Persona | None = None


class Conflict(Strict):
    id: str = Field(min_length=1)
    facts: list[str] = Field(min_length=2)
    truth: list[str] = Field(min_length=1, description="truth item ids saying what is true")
    expected_behaviour: str = Field(min_length=1)


class ExamFinding(Strict):
    id: str = Field(min_length=1)
    label: str = Field(min_length=1, description="what is examined, e.g. lying and standing BP")
    finding: str | None = Field(default=None, min_length=1)
    parts: list[str] = Field(
        default_factory=list,
        description="a named set GPs ask for as one (e.g. observations): the ids of its findings",
    )


class OrderedTest(Strict):
    """What a test would show if the clinician orders it at this visit. It is back in the chart
    by the next visit; a test ordered but not listed comes back normal (so list every abnormal
    result the truth implies, as with examination findings)."""

    id: str = Field(min_length=1)
    label: str = Field(min_length=1, description="the test as ordered, e.g. CBC, CT abdomen")
    finding: str = Field(min_length=1)


class Visit(Strict):
    number: int = Field(ge=1)
    day: int = Field(default=0, ge=0, description="days after visit 1 (visit 1 is day 0)")
    setting: Setting
    present: list[Person] = Field(min_length=1)
    turn_budget: int = Field(gt=0)
    reason: str = Field(min_length=1)
    events_since_last: list[str] = Field(default_factory=list)
    records_available: list[Record] = Field(default_factory=list)
    examination: list[ExamFinding] = Field(default_factory=list)
    results: list[OrderedTest] | None = Field(
        default=None,
        description="tests ordered in this visit's plan come back by the next visit; "
        "None: off (a requested test is graded from the plan only); []: on, all normal",
    )


class Requires(Strict):
    """What the visit log must show before a judge's "met" counts (a must_do or red_flag item).

    Checked in code, so a plan that names an examination it never did earns no credit.
    """

    examined: list[str] = Field(default_factory=list, description="finding ids at this visit")
    read: list[Record] = Field(default_factory=list)
    spoke_to: list[Person] = Field(default_factory=list)


class RubricItem(Strict):
    id: str = Field(min_length=1)
    visit: int = Field(ge=1)
    kind: RubricKind
    description: str = Field(min_length=1)
    weight: float = Field(gt=0)
    critical: bool = False
    critical_type: CriticalType | None = None
    stage: Stage | None = Field(default=None, description="required on critical items")
    requires: Requires | None = None
    evidence: list[str] = Field(
        default_factory=list,
        description="critical items: the fact, examination finding or test result ids it "
        "depends on; at least one must be earned (validate.py), so no critical can be met "
        "from records alone",
    )


class PatientSummary(Strict):
    name: str = Field(min_length=1)
    age: int = Field(ge=0)
    summary: str = Field(min_length=1)


Views = dict[str, list[Fact]]
# A record written out as it would look, with [[fact_id]] where each of that record's facts
# goes and {day:-21} or {weekday:-9} for dates relative to visit 1 (see views.record_text).
Documents = dict[Record, str]


class Case(Strict):
    id: str = Field(pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=1)
    country: Country
    messiness: Messiness
    patient: PatientSummary
    hidden_truth: list[TruthItem] = Field(min_length=1)
    views: Views
    documents: Documents = Field(default_factory=dict)
    record_traits: dict[Record, list[RecordTrait]] = Field(default_factory=dict)
    personas: Personas
    conflicts: list[Conflict] = Field(default_factory=list)
    visits: list[Visit] = Field(min_length=1)
    rubric: list[RubricItem] = Field(min_length=1)
    notes: str | None = None


class TwinSpec(Strict):
    """A consistent-sources twin: the base case with every source accurate.

    Truth, personas and visits are inherited from the base case, so they cannot drift.
    Only the views and rubric are rewritten; conflicts are always empty.
    """

    id: str = Field(pattern=r"^[a-z0-9_]+$")
    twin_of: str = Field(pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=1)
    messiness: Messiness | None = Field(default=None, description="default: the base's")
    views: Views
    documents: Documents = Field(
        default_factory=dict,
        description="records written out differently from the base; the rest are reused "
        "with the twin's facts in the same slots",
    )
    record_traits: dict[Record, list[RecordTrait]] = Field(default_factory=dict)
    rubric: list[RubricItem] = Field(min_length=1)
    notes: str | None = None

    def resolve(self, base: Case) -> Case:
        return base.model_copy(
            update={
                "id": self.id,
                "title": self.title,
                "views": self.views,
                "documents": {**base.documents, **self.documents},
                "rubric": self.rubric,
                "messiness": self.messiness or base.messiness,
                "record_traits": self.record_traits,
                "conflicts": [],
                "notes": self.notes,
            }
        )
