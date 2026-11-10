"""The case-writing form (tools/case-form/index.html) offers the schema's own values, so a draft
never carries a trait, setting or stage the case YAML would reject."""

from __future__ import annotations

import re
from enum import StrEnum
from pathlib import Path

import pytest

from clinical_env.case_schema import (
    SOURCES,
    Accuracy,
    Disclosure,
    Interjection,
    Messiness,
    PersonTrait,
    RecordTrait,
    RubricKind,
    Setting,
    Stage,
)

FORM = Path(__file__).resolve().parents[1] / "tools" / "case-form" / "index.html"


def form_values(const: str) -> set[str]:
    """First item of each ["value", ...] entry in `const NAME = [ ... ];`."""
    text = FORM.read_text(encoding="utf-8")
    match = re.search(rf"const {const} = \[(.*?)\];\n", text, re.DOTALL)
    assert match, f"{const} not found in the form"
    return set(re.findall(r'\[\s*"([a-z_]+)"', match.group(1)))


def values(enum: type[StrEnum]) -> set[str]:
    return {member.value for member in enum}


@pytest.mark.parametrize(
    ("const", "expected"),
    [
        ("PERSON_TRAITS", values(PersonTrait) - {PersonTrait.CARER_DOMINATES.value}),
        ("RECORD_TRAITS", values(RecordTrait)),
        ("SOURCES", set(SOURCES)),
        ("ACCURACY", values(Accuracy)),
        ("HOW", values(Disclosure) - {Disclosure.HIDDEN.value}),
        ("SETTINGS", values(Setting)),
        ("STAGES", values(Stage)),
        ("KINDS", values(RubricKind)),
        ("INTERJECT", values(Interjection)),
        ("MESSINESS", values(Messiness)),
    ],
)
def test_form_options_match_schema(const: str, expected: set[str]) -> None:
    assert form_values(const) == expected


def test_carer_traits_add_dominates() -> None:
    text = FORM.read_text(encoding="utf-8")
    assert 'PERSON_TRAITS.concat([["carer_dominates"' in text
