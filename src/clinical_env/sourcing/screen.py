"""A transparent first-pass screen of candidates, before an author reads them.

Keeps reports that state a patient aged 70 or over and drops those whose title or abstract
says paediatric, surgical technique or image-led. It only narrows the reading list; choosing
a source stays a reading decision (sources/screening.md).
"""

from __future__ import annotations

import re

from clinical_env.sourcing.europepmc import Candidate

MIN_AGE = 70
_AGE = re.compile(
    r"\b(\d{2,3})[- ](?:year|yr)s?[- ]old\b|\baged? (\d{2,3})\b|\b(\d{2,3})-?y/?o\b",
    re.IGNORECASE,
)
_OLD_WORDS = re.compile(r"\b(?:octogenarian|nonagenarian|centenarian)\b", re.IGNORECASE)
EXCLUDE = {
    # Not "child": older adults' reports mention their children.
    "paediatric": re.compile(r"\b(?:pa?ediatric|infant|neonat\w*|adolescent)\b", re.IGNORECASE),
    "surgical technique": re.compile(
        r"\b(?:surgical technique|laparoscopic|arthroplasty|resection|flap|anastomosis)\b",
        re.IGNORECASE,
    ),
    "image-led": re.compile(
        r"\b(?:radiograph\w*|imaging findings|dermoscop\w*|histopatholog\w*|"
        r"fundoscop\w*|photograph\w*)\b",
        re.IGNORECASE,
    ),
}


def ages(text: str) -> list[int]:
    return [int(next(g for g in m.groups() if g)) for m in _AGE.finditer(text)]


def prefilter(candidate: Candidate) -> list[str]:
    """Reasons to drop a candidate; empty means it goes on the reading list."""
    text = f"{candidate.title}\n{candidate.abstract}"
    reasons = []
    if not any(a >= MIN_AGE for a in ages(text)) and not _OLD_WORDS.search(text):
        reasons.append(f"no stated age of {MIN_AGE}+")
    reasons += [name for name, pattern in EXCLUDE.items() if pattern.search(text)]
    return reasons
