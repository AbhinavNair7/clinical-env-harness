"""Country wording: UK prompts are untouched, and no UK term reaches a model in a US case."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from conftest import FakeModel

from clinical_env import prompts
from clinical_env.case_schema import Case, Country, Person, Record, Setting
from clinical_env.grader import load_consultation_rubric
from clinical_env.locale import UK, UK_TERMS, US, locale_of
from clinical_env.simulators import GP, Checker, PersonSimulator, Utterance, render_conversation
from clinical_env.validate import check_case
from clinical_env.views import clinician_briefing, get_visit, record_text, visit_heading


def _templates() -> Iterator[tuple[str, str]]:
    for name, value in vars(prompts).items():
        if name.isupper() and isinstance(value, str):
            yield name, value
        elif name.isupper() and isinstance(value, dict):
            for key, text in value.items():
                yield f"{name}[{key}]", text


TEMPLATES = list(_templates())
# The document-review prompts are UK-only by design (UK memory-service cases); they never pass
# through a locale, so only the consultation prompts must localise cleanly.
LOCALISED = [(n, t) for n, t in TEMPLATES if not n.startswith("REVIEW_")]


@pytest.mark.parametrize(("name", "template"), TEMPLATES, ids=[n for n, _ in TEMPLATES])
def test_uk_templates_are_unchanged(name: str, template: str) -> None:
    assert UK.text(template) is template


@pytest.mark.parametrize(("name", "template"), LOCALISED, ids=[n for n, _ in LOCALISED])
def test_us_templates_carry_no_uk_terms(name: str, template: str) -> None:
    assert not UK_TERMS.findall(US.text(template)), US.text(template)


def test_us_wording_reads_as_us_primary_care() -> None:
    assert US.text(prompts.CLINICIAN_SYSTEM).startswith("You are a US primary care physician.")
    assert "in a US primary care visit" in US.text(prompts.PERSON_SYSTEM)
    assert "Adult Protective Services" in US.text(prompts.GRADER_SAFETY_GUIDANCE)
    assert "pill organizer" in US.text(prompts.EXAMINER_SYSTEM)


def test_uk_wording_is_what_saved_runs_used() -> None:
    assert UK.setting_text[Setting.PHONE] == "telephone consultation"
    assert UK.record_titles[Record.GP_RECORD] == "GP record"
    assert UK.author == "GP (you)"
    line = [Utterance(GP, "Hello", to="Edith")]
    assert render_conversation(line) == "GP (to Edith): Hello"
    assert render_conversation(line, US.clinician) == "Doctor (to Edith): Hello"


def test_every_record_and_setting_has_wording() -> None:
    for loc in (UK, US):
        assert set(loc.record_titles) == set(Record)
        assert set(loc.setting_text) == set(Setting)


def test_local_pathways_examples_follow_the_country() -> None:
    item = next(c for c in load_consultation_rubric() if c.id == "c_local_pathways")
    uk = item.text(Country.UK)
    # Byte-identical to the description before examples were split out (4 Nov).
    assert uk == (
        "Uses the referral and care routes of the health system the case is set in, not those "
        "of another country. In a UK case: equipment and home adaptations through occupational "
        "therapy (social care or community OT), care changes through a social care assessment, "
        "falls through the falls service or community physiotherapy, dosette changes through "
        "the pharmacy. Ordering equipment or care directly counts against it."
    )
    us = item.text(Country.US)
    assert "In a US case" in us
    assert "In a UK case" not in us


def _as_us(edith: Case) -> Case:
    return edith.model_copy(update={"country": Country.US})


def test_a_us_case_shows_us_titles_and_settings(edith: Case) -> None:
    us = _as_us(edith)
    assert locale_of(us) is US
    briefing = clinician_briefing(us, 1)
    assert "Primary care chart (gp_record)" in briefing
    assert "GP record" not in briefing
    assert record_text(us, Record.GP_RECORD, 1).startswith("Primary care chart:")
    assert visit_heading(us, get_visit(us, 2)).startswith("Visit 2, telephone visit")


def test_us_person_prompt_wording(edith: Case) -> None:
    model = FakeModel(lambda system, user: "")
    us = _as_us(edith)
    person = PersonSimulator(us, Person.PATIENT, get_visit(us, 1), model, Checker(model, US))
    # The template words are US; Edith's own UK facts are case content, checked by the validator.
    assert "in a US primary care visit" in person.system
    assert "UK GP" not in person.system


def test_validator_rejects_uk_wording_in_a_us_case(edith: Case) -> None:
    errors = check_case(_as_us(edith))
    assert any(e.startswith("country us: UK wording") and "'dosette'" in e for e in errors)
    assert not any(e.startswith("country us") for e in check_case(edith))


def test_clinician_prompt_does_not_hint_at_conflicting_sources() -> None:
    # The bare-model tier must not cue discrepancy hunting; the hint belongs to the thin prompt.
    text = prompts.CLINICIAN_SYSTEM.lower()
    assert "may not agree" not in text
    assert "conflict" not in text
