"""Country wording: every word a model reads about the health system follows the case's country.

Prompts are written once, in UK wording (prompts.py). A US case reads them through
`Locale.text`, which swaps the UK terms for US ones; a UK case reads them unchanged, so UK
prompts stay exactly as they were tuned. Stored ids (`gp_record`, the "GP" speaker in logs)
never change, so saved runs load whatever the country. tests/test_locale.py checks that no UK
term reaches a US prompt template. Known exception: tool-schema values are stored ids and are
not localised (record ids such as `gp_record`, the `carer` party, the `safeguarding` action
type), so a US clinician still sees those words in its tools.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from functools import cache

from clinical_env.case_schema import Case, Country, Record, Setting

# Ordered: whole phrases first, then the generic "GP" -> "doctor" swap.
_US_PHRASES: tuple[tuple[str, str], ...] = (
    ("You are a UK general practitioner.", "You are a US primary care physician."),
    ("in a UK GP consultation", "in a US primary care visit"),
    ("a simulated GP consultation", "a simulated primary care visit"),
    (
        "You are an experienced UK GP examiner grading",
        "You are an experienced US primary care physician and examiner grading",
    ),
    # Over-provision examples: agent's US draft of the clinical lead's UK list, for him to confirm.
    (
        "A UK GP would count, for example: a safeguarding referral for care needs that a social "
        "care assessment is already addressing; same-day or emergency escalation (hospital, "
        "temporary placement, urgent community response) with no red flag;",
        "A US primary care physician would count, for example: an Adult Protective Services "
        "report for care needs that a home health or care needs assessment is already "
        "addressing; same-day or emergency escalation (emergency department, hospital "
        "admission, respite or nursing home placement) with no red flag;",
    ),
    (
        '"inspect the medicine packs" matches dosette contents',
        '"look at the pill bottles" matches pill organizer contents',
    ),
    ("a GP carries no scales", "a doctor on a home visit carries no scales"),
    ("telephone consultation", "telephone visit"),
    ("the telly", "the TV"),
    ("about Mum?", "about Mom?"),
)
_US_WORDS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bGPs\b"), "doctors"),
    (re.compile(r"\bThe GP\b"), "The doctor"),
    (re.compile(r"\bGP\b"), "doctor"),
)

# Words that must never reach a model in a US case (tests/test_locale.py).
UK_TERMS = re.compile(r"\b(UK|NHS|GPs?|dosette|telly|safeguarding|Mum)\b")


@cache
def _to_us(text: str) -> str:
    for old, new in _US_PHRASES:
        text = text.replace(old, new)
    for pattern, new in _US_WORDS:
        text = pattern.sub(new, text)
    return text


@dataclass(frozen=True)
class Locale:
    country: Country
    clinician: str  # how people and the judge see the clinician speak: "GP (to Edith): ..."
    author: str  # the author column of the clinician's own entries in the primary care record
    setting_text: Mapping[Setting, str]
    record_titles: Mapping[Record, str]

    def text(self, template: str) -> str:
        """A prompt template in this country's words (UK templates are returned unchanged)."""
        return template if self.country == Country.UK else _to_us(template)


UK = Locale(
    country=Country.UK,
    clinician="GP",
    author="GP (you)",
    setting_text={
        Setting.HOME_VISIT: "home visit",
        Setting.PHONE: "telephone consultation",
        Setting.CLINIC: "clinic appointment",
    },
    record_titles={
        Record.GP_RECORD: "GP record",
        Record.CARE_AGENCY_NOTES: "Care agency notes",
        Record.DISCHARGE_SUMMARY: "Hospital discharge summary",
        Record.PHARMACY_RECORD: "Pharmacy record",
        Record.AMBULANCE_REPORT: "Ambulance service patient report",
    },
)

US = Locale(
    country=Country.US,
    clinician="Doctor",
    author="Doctor (you)",
    setting_text={
        Setting.HOME_VISIT: "home visit",
        Setting.PHONE: "telephone visit",
        Setting.CLINIC: "office visit",
    },
    record_titles={
        Record.GP_RECORD: "Primary care chart",
        Record.CARE_AGENCY_NOTES: "Home care agency notes",
        Record.DISCHARGE_SUMMARY: "Hospital discharge summary",
        Record.PHARMACY_RECORD: "Pharmacy fill history",
        Record.AMBULANCE_REPORT: "EMS patient care report",
    },
)

LOCALES: Mapping[Country, Locale] = {Country.UK: UK, Country.US: US}


def locale_of(case: Case) -> Locale:
    return LOCALES[case.country]
