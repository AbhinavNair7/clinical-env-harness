"""What each party sees: nothing hidden may reach the clinician or the wrong person."""

from __future__ import annotations

import pytest
from conftest import CASES, FakeModel, checker_reply

from clinical_env import prompts
from clinical_env.case_schema import Case, Person, Record
from clinical_env.llm_clinician import clinician_tools
from clinical_env.simulators import Checker, PersonSimulator
from clinical_env.validate import load_case
from clinical_env.views import clinician_briefing, get_visit, record_text


def _norm(text: str) -> str:
    return " ".join(text.split()).lower()


def _secrets(case: Case) -> dict[str, str]:
    """Text the clinician must never be handed up front, by where it comes from."""
    secrets = {f"truth {t.id}": t.statement for t in case.hidden_truth}
    secrets |= {f"rubric {r.id}": r.description for r in case.rubric}
    secrets |= {f"conflict {c.id}": c.expected_behaviour for c in case.conflicts}
    for visit in case.visits:
        secrets |= {f"event v{visit.number}.{i}": e for i, e in enumerate(visit.events_since_last)}
        secrets |= {f"exam {x.id}": x.finding for x in visit.examination if x.finding}
    for source, facts in case.views.items():
        secrets |= {f"{source} {f.id}": f.statement for f in facts}
    if case.notes:
        secrets["notes"] = case.notes
    return secrets


def _leaks(text: str, secrets: dict[str, str]) -> list[str]:
    seen = _norm(text)
    return [label for label, secret in secrets.items() if _norm(secret) in seen]


@pytest.mark.parametrize("visit", [1, 2])
def test_clinician_start_holds_no_hidden_text(edith: Case, visit: int) -> None:
    info = get_visit(edith, visit)
    tools = clinician_tools(info.present, info.records_available)
    opening = "\n".join(
        [
            prompts.CLINICIAN_SYSTEM.format(turn_budget=info.turn_budget),
            clinician_briefing(edith, visit),
            *(t.model_dump_json() for t in tools),
        ]
    )
    assert _leaks(opening, _secrets(edith)) == []


def test_briefing_names_who_is_present_and_the_records(edith: Case) -> None:
    briefing = clinician_briefing(edith, 1)
    assert "Visit 1: home visit, Thursday 5 November 2026." in briefing
    assert "Edith Marsh (patient), Janet Price (daughter)" in briefing
    assert "care_agency_notes" in briefing and "ambulance_report" in briefing
    assert "Thursday 19 November 2026" in clinician_briefing(edith, 2)  # visit 2 is day 14


def test_record_shows_only_entries_for_that_visit(edith: Case) -> None:
    visit_1 = record_text(edith, Record.PHARMACY_RECORD, 1)
    visit_2 = record_text(edith, Record.PHARMACY_RECORD, 2)
    assert "02 Nov 2026  Weekly blister pack dispensed. Morning: furosemide" in visit_1
    assert "16 Nov 2026" not in visit_1  # dated after visit 1: has not happened yet
    assert "16 Nov 2026  Weekly blister pack dispensed, contents unchanged." in visit_2


@pytest.mark.parametrize("record", list(Record))
@pytest.mark.parametrize("visit", [1, 2])
def test_written_records_resolve_every_slot_and_date(
    edith: Case, record: Record, visit: int
) -> None:
    text = record_text(edith, record, visit)
    assert "[[" not in text and "{day:" not in text and "{weekday:" not in text


def test_written_record_drops_lines_for_facts_not_yet_true(edith: Case) -> None:
    visit_1 = record_text(edith, Record.CARE_AGENCY_NOTES, 1)
    visit_2 = record_text(edith, Record.CARE_AGENCY_NOTES, 2)
    assert "Tue 27 Oct AM 07:48-09:55 On arrival client found on hallway floor" in visit_1
    assert "bathroom floor" not in visit_1  # a2_fall applies from visit 2
    assert "Sat 14 Nov AM 07:55-08:40 Client found on bathroom floor" in visit_2


def test_record_without_a_document_lists_its_facts(edith: Case) -> None:
    plain = edith.model_copy(update={"documents": {}})
    text = record_text(plain, Record.DISCHARGE_SUMMARY, 1)
    assert text.splitlines()[1] == "- Fall at home secondary to postural hypotension."


def test_twin_reuses_base_documents_with_its_own_facts() -> None:
    twin = load_case(CASES / "edith_marsh_twin.yaml")
    agency = record_text(twin, Record.CARE_AGENCY_NOTES, 1)
    assert "Calls running at about 15 minutes because of staffing" in agency  # twin fact
    assert "Tue 27 Oct AM 07:48-09:55" in agency  # base layout
    assert "Falls: two this month" in record_text(twin, Record.GP_RECORD, 1)  # twin's own layout


@pytest.mark.parametrize("person", [Person.PATIENT, Person.CARER])
def test_person_sees_only_their_own_view(edith: Case, person: Person) -> None:
    visit = get_visit(edith, 1)
    model = FakeModel(checker_reply())
    simulator = PersonSimulator(edith, person, visit, model, Checker(model))
    own = {f"{person.value} {f.id}" for f in edith.views[person.value] if f.applies_to(1)}
    leaks = _leaks(simulator.system, _secrets(edith))
    assert sorted(leaks) == sorted(own)
    # Hidden facts come with their reveal condition, so the simulator knows when to give them.
    assert "(keep back; only say this if the GP has asked" in simulator.system


def test_visit_two_facts_stay_out_of_visit_one(edith: Case) -> None:
    visit = get_visit(edith, 1)
    model = FakeModel(checker_reply())
    carer = PersonSimulator(edith, Person.CARER, visit, model, Checker(model))
    assert "furosemide 40" not in carer.system  # c2_dosette is a visit-2 fact


def test_janet_knows_about_the_second_fall_at_visit_two(edith: Case) -> None:
    model = FakeModel(checker_reply())
    carer = PersonSimulator(edith, Person.CARER, get_visit(edith, 2), model, Checker(model))
    assert "bathroom floor till the carer came" in carer.system
    assert "Nothing since, as far as I know" not in carer.system  # c_falls ends at visit 1
    assert "Mum's managing fine" not in carer.system
