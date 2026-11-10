"""MIMIC pattern counts on tiny synthetic tables (no real MIMIC data in the repo)."""

from __future__ import annotations

import csv
import gzip
from pathlib import Path

from clinical_env.sourcing.mimic_patterns import (
    ED,
    HOSP,
    Data,
    count,
    drug_name,
    older_admissions,
    report,
    share,
    spread,
)


def write(root: Path, table: str, rows: list[dict[str, str]]) -> None:
    path = root / f"{table}.csv.gz"
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def adm(subject: str, hadm: str, admit: str, disch: str, where: str = "HOME") -> dict[str, str]:
    return {
        "subject_id": subject,
        "hadm_id": hadm,
        "admittime": admit,
        "dischtime": disch,
        "discharge_location": where,
    }


def synthetic(root: Path) -> Data:
    write(
        root,
        f"{HOSP}/patients",
        [
            {"subject_id": "1", "anchor_age": "80", "anchor_year": "2150"},
            {"subject_id": "2", "anchor_age": "50", "anchor_year": "2150"},
        ],
    )
    write(
        root,
        f"{HOSP}/admissions",
        [
            adm("1", "a1", "2150-01-01 10:00:00", "2150-01-05 10:00:00"),
            adm(
                "1", "a2", "2150-01-20 10:00:00", "2150-01-25 10:00:00", "SKILLED NURSING FACILITY"
            ),
            adm("2", "b1", "2150-01-01 10:00:00", "2150-01-02 10:00:00"),
            adm("2", "b2", "2150-03-01 10:00:00", "2150-03-02 10:00:00"),
        ],
    )
    write(
        root,
        f"{HOSP}/diagnoses_icd",
        [
            {"hadm_id": "a1", "icd_code": "I10"},  # hypertension, then gone at a2
            {"hadm_id": "a1", "icd_code": "Z7901"},
            {"hadm_id": "a2", "icd_code": "N179"},
        ],
    )
    write(
        root,
        f"{HOSP}/prescriptions",
        [
            {"hadm_id": "a1", "drug": "Pantoprazole", "drug_type": "MAIN"},
            {"hadm_id": "a1", "drug": "Metoprolol Tartrate", "drug_type": "MAIN"},
            {"hadm_id": "a2", "drug": "Sodium Chloride 0.9%", "drug_type": "BASE"},
        ],
    )
    write(
        root,
        f"{HOSP}/emar",
        [
            {"hadm_id": "a1", "medication": "Metoprolol Tartrate", "event_txt": "Administered"},
            {"hadm_id": "a1", "medication": "Metoprolol Tartrate", "event_txt": "Hold Dose"},
        ],
    )
    write(
        root,
        f"{ED}/edstays",
        [{"subject_id": "1", "hadm_id": "a1", "stay_id": "s1"}],
    )
    write(
        root,
        f"{ED}/medrecon",
        [
            {"stay_id": "s1", "name": "metoprolol succinate"},
            {"stay_id": "s1", "name": "*donepezil"},
        ],
    )
    return Data.load(root)


def test_cohort_is_65_plus_at_each_admission(tmp_path: Path) -> None:
    older = older_admissions(synthetic(tmp_path))
    assert list(older) == ["1"]
    assert [a["hadm_id"] for a in older["1"]] == ["a1", "a2"]


def test_report_counts_patterns_and_suppresses_small_numbers(tmp_path: Path) -> None:
    text = report(synthetic(tmp_path))
    assert "Cohort: <5 patients" in text
    assert "within 30 days <5" in text
    assert "absent at the next: n/a (fewer than 5) consecutive" in text  # hypertension dropped
    assert "proton pump inhibitor with no upper GI code n/a (fewer than 5)" in text
    assert "Home medicines never ordered during the admission: n/a (fewer than 5)" in text
    # No row-level detail: neither raw ids nor the synthetic drug list appear.
    assert "a1" not in text and "donepezil" not in text


def test_formatting_helpers() -> None:
    assert count(0) == "0" and count(3) == "<5" and count(12) == "12"
    assert share(3, 40) == "suppressed (of 40)"
    assert share(38, 40) == "suppressed (of 40)"  # the remainder of 2 would show
    assert share(1, 3) == "n/a (fewer than 5)"
    assert share(10, 40) == "10 of 40 (25%)"
    assert spread([1, 2]) == "n/a (too few)"
    assert spread([1, 2, 3, 4, 5]).startswith("median 3")
    assert drug_name("Metoprolol Tartrate") == "metoprolol"
    assert drug_name("*depakote DR") == "depakote"
