"""The licence rule: keep an article only if its own full-text XML says CC BY or CC0.

Strict on purpose. Anything non-commercial, share-alike or no-derivatives is rejected, and so
is a missing, ambiguous or self-contradicting licence, or one that disagrees with the search
metadata. Both the licence link and its wording are read: some journals (Cureus, for one)
give only wording ("Creative Commons Attribution License CC-BY 4.0"), with no link.
"""

from __future__ import annotations

import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Literal

Kind = Literal["cc-by", "cc0", "restricted"]

XLINK = "{http://www.w3.org/1999/xlink}href"
ALI_REF = "{http://www.niso.org/schemas/ali/1.0/}license_ref"

_URL = re.compile(
    r"creativecommons\.org/(?:licenses/(?P<terms>[a-z-]+)|publicdomain/(?P<pd>zero|mark))",
    re.IGNORECASE,
)
# Text is normalised first (_normalise): any dash becomes "-" and whitespace collapses, so
# "Non Commercial", "CC BY–NC" and "CCBY-NC" all match.
_RESTRICTED_WORDS = re.compile(
    r"non[\s-]?commercial|share[\s-]?alike|no[\s-]?deriv"
    r"|\bcc[\s-]?by[\s-]?(?:nc|sa|nd)\b|\bby[\s-](?:nc|sa|nd)\b",
    re.IGNORECASE,
)
_DASHES = dict.fromkeys(map(ord, "\u2010\u2011\u2012\u2013\u2014\u2015\u2212"), "-")
_CC0_WORDS = re.compile(r"\bcc0\b|\bcc zero\b|public domain dedication", re.IGNORECASE)
_BY_WORDS = re.compile(r"creative commons attribution\b|\bcc[ -]?by\b", re.IGNORECASE)
_DATA_WAIVER = re.compile(r"appl(?:y|ies) to the data|data made available", re.IGNORECASE)
EVIDENCE_CHARS = 300


@dataclass(frozen=True)
class LicenceDecision:
    accepted: bool
    licence: str | None  # "cc by" or "cc0" when accepted
    reason: str
    evidence: str  # the licence link(s) and wording the decision was made on


def _normalise(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).translate(_DASHES).split())


def _url_kind(url: str) -> Kind | None:
    """None for a link that is not a Creative Commons licence (rejected as unknown)."""
    match = _URL.search(url)
    if match is None:
        return None
    if match.group("pd"):
        return "cc0" if match.group("pd").lower() == "zero" else "restricted"
    return "cc-by" if match.group("terms").lower() == "by" else "restricted"


def _text_kind(text: str) -> Kind | None:
    text = _normalise(text)
    if _RESTRICTED_WORDS.search(text):
        return "restricted"
    if _CC0_WORDS.search(text):
        return "cc0"
    if _BY_WORDS.search(text):
        return "cc-by"
    return None


def _without_data_waiver(text: str) -> tuple[str, bool]:
    """BMC journals add a CC0 waiver for the data to a CC BY article ("... applies to the data
    made available in this article"). That sentence is about data, not the article."""
    sentences = re.split(r"(?<=[.;])\s+", text)
    kept = [x for x in sentences if not _DATA_WAIVER.search(x)]
    return " ".join(kept), len(kept) < len(sentences)


def decide(xml: bytes, search_licence: str | None) -> LicenceDecision:
    """Decide from the <permissions><license> elements of a JATS full-text XML."""
    try:
        root = ET.fromstring(xml)  # Python's expat refuses entity-expansion bombs
    except ET.ParseError as exc:
        return LicenceDecision(False, None, f"unreadable XML: {exc}", "")
    # The article's own licence sits in <front>; figures in the body can carry their own.
    front = root.find(".//front")
    if front is None:  # without front matter a figure's licence could pass for the article's
        return LicenceDecision(False, None, "no <front> in the full text", "")
    permissions = list(front.iter("permissions"))
    licences = [el for perm in permissions for el in perm.iter("license")]
    refs = [el for perm in permissions for el in perm.iter(ALI_REF)]
    if not licences and not refs:
        return LicenceDecision(False, None, "no licence element in the full text", "")
    urls = [(el.text or "").strip() for el in refs]
    texts: list[str] = []
    for el in licences:
        text, waiver = _without_data_waiver(" ".join("".join(el.itertext()).split()))
        links = [child.get(XLINK) or "" for child in el.iter() if child.get(XLINK)]
        urls += [u for u in links if not (waiver and _url_kind(u) == "cc0")]
        texts.append(text)
    urls = [u for u in urls if u]
    evidence = " | ".join([*dict.fromkeys(urls), *texts])[:EVIDENCE_CHARS]
    unknown = [u for u in urls if _url_kind(u) is None]
    if unknown:
        return LicenceDecision(False, None, f"licence link is not CC: {unknown[0]}", evidence)
    kinds = {k for k in (*map(_url_kind, urls), *map(_text_kind, texts)) if k is not None}
    if "restricted" in kinds:
        return LicenceDecision(False, None, "restricted licence (NC, SA, ND or PD mark)", evidence)
    if not kinds:
        return LicenceDecision(False, None, "licence does not name CC BY or CC0", evidence)
    if len(kinds) > 1:
        return LicenceDecision(False, None, "licence names both CC BY and CC0", evidence)
    licence = "cc by" if kinds == {"cc-by"} else "cc0"
    if (search_licence or "").strip().lower() != licence:
        return LicenceDecision(
            False, None, f"search metadata says {search_licence!r}, full text {licence}", evidence
        )
    return LicenceDecision(True, licence, f"full text says {licence}", evidence)
