"""`clinical-env sources pull` and `clinical-env sources check <case.yaml>`.

`pull` writes sources/candidates.jsonl and sources/licence_log.csv (metadata and licence
evidence; abstracts only for accepted articles) and caches full texts in sources/fulltext/
(not committed). `check` runs a drafted case's source checks from its provenance file in
sources/provenance/<case_id>.yaml, which never sits beside the case.
"""

from __future__ import annotations

import csv
import json
from collections.abc import Sequence
from itertools import combinations
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field

from clinical_env.sourcing.europepmc import PMCID, Candidate, Client, FetchError
from clinical_env.sourcing.licence import LicenceDecision, decide
from clinical_env.sourcing.overlap import shared_runs, source_text, strings
from clinical_env.sourcing.screen import prefilter

LOG_FIELDS = [
    "pmcid",
    "accepted",
    "licence",
    "reason",
    "search_licence",
    "journal",
    "year",
    "title",
    "evidence",
]
TOP_HITS = 10


class Provenance(BaseModel):
    """Where a case came from and what was changed. Internal only: never shown to a model."""

    model_config = ConfigDict(extra="forbid")

    case_id: str
    pmcid: str = Field(pattern=PMCID)
    pmid: str | None = None
    title: str
    authors: str
    journal: str
    year: str
    doi: str | None = None
    licence: str
    url: str
    changes: list[str] = Field(min_length=3, description="clinically meaningful changes")
    record_patterns: list[str] = Field(default_factory=list)
    distinctive_details: list[str] = Field(
        min_length=3, max_length=4, description="for the identifiability search"
    )
    theme: list[str] = Field(
        default_factory=list,
        description="the clinical arc itself (e.g. pancreatic cancer, worsening diabetes): a "
        "match made only from theme terms is a theme-level match, accepted (5 Nov)",
    )


def pull(client: Client, query: str, limit: int, out: Path) -> int:
    candidates = client.search(query, limit)
    out.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    accepted = kept = 0
    for c in candidates:
        try:
            xml = client.full_text(c.pmcid)
        except FetchError as exc:
            decision = LicenceDecision(False, None, f"full text not fetched: {exc}", "")
            figures = 0
        else:
            decision = decide(xml, c.search_licence)
            figures = xml.count(b"<fig ") + xml.count(b"<fig>")
        drop = prefilter(c) if decision.accepted else []
        accepted += decision.accepted
        kept += decision.accepted and not drop
        rows.append(_row(c, decision, figures, drop))
    with (out / "candidates.jsonl").open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (out / "licence_log.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(
        f"{len(rows)} candidates: {accepted} CC BY/CC0 by their own XML, "
        f"{kept} through the prefilter. Wrote {out}/candidates.jsonl and licence_log.csv"
    )
    return 0


def _row(
    c: Candidate, decision: LicenceDecision, figures: int, drop: list[str]
) -> dict[str, object]:
    row: dict[str, object] = {
        "pmcid": c.pmcid,
        "accepted": decision.accepted,
        "licence": decision.licence,
        "reason": decision.reason,
        "search_licence": c.search_licence,
        "journal": c.journal,
        "year": c.year,
        "title": c.title,
        "evidence": decision.evidence,
        "pmid": c.pmid,
        "doi": c.doi,
        "authors": c.authors,
        "url": c.url,
        "figures": figures,
        "prefilter_drop": drop,
    }
    if decision.accepted:  # only openly licensed text is kept in the repo
        row["abstract"] = c.abstract
    return row


def check(client: Client, case_path: Path, provenance_dir: Path) -> int:
    data = yaml.safe_load(case_path.read_text(encoding="utf-8"))
    case_id = str(data.get("id", case_path.stem))
    prov_path = provenance_dir / f"{case_id}.yaml"
    prov = Provenance.model_validate(yaml.safe_load(prov_path.read_text(encoding="utf-8")))
    failures: list[str] = []
    if prov.case_id != case_id:
        failures.append(f"provenance case_id {prov.case_id} is not {case_id}")

    xml = client.full_text(prov.pmcid)
    licence = decide(xml, prov.licence)
    print(f"licence: {'ok' if licence.accepted else 'FAIL'} ({licence.reason})")
    if not licence.accepted:
        failures.append(f"licence: {licence.reason}")

    case_text = "\n".join(strings(data))
    runs = shared_runs(case_text, source_text(xml))
    print(f"overlap: {'ok' if not runs else 'FAIL'} ({len(runs)} shared runs of 8+ words)")
    for run in runs:
        print(f"  - {run}")
    if runs:
        failures.append(f"overlap: {len(runs)} shared runs")

    for label, query in identifiability_queries(prov.distinctive_details, prov.theme):
        total, top = client.hit_ids(query, TOP_HITS)
        mine = {x.lower() for x in (prov.pmcid, prov.pmid, prov.doi) if x}
        found = bool(mine & top)
        print(f"identifiability ({label}): {'FAIL' if found else 'ok'} ({total} hits) {query}")
        if found:
            failures.append(f"identifiability: source in the top {TOP_HITS} ({label})")

    print("PASS" if not failures else "FAIL: " + "; ".join(failures))
    return 1 if failures else 0


def identifiability_queries(details: list[str], theme: Sequence[str] = ()) -> list[tuple[str, str]]:
    """All details (and theme terms) together, every pair that includes at least one
    case-specific detail (an all-details search often finds nothing, which proves little), and
    any detail by relevance; all among case reports. Pairs of theme terms alone are not
    searched: any case on a common theme finds its best-known reports, which is accepted."""
    scope = ' AND PUB_TYPE:"case reports"'
    words = [*details, *theme]
    terms = {w: f"({w})" for w in words}
    pairs = [
        (f"pair: {a} + {b}", f"{terms[a]} AND {terms[b]}{scope}")
        for a, b in combinations(words, 2)
        if a in details or b in details
    ]
    return [
        ("all details", " AND ".join(terms.values()) + scope),
        *pairs,
        ("any detail, by relevance", "(" + " OR ".join(terms[d] for d in details) + ")" + scope),
    ]
