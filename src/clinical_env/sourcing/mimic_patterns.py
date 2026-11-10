"""Record-messiness patterns counted in the MIMIC-IV and MIMIC-IV-ED demo data (ODbL v1.0).

Reads the demo CSVs from a local folder (never committed) and prints aggregate counts only:
no row, timeline or medicine list of any one patient leaves this module, and any count from
1 to 4 is shown as "<5". Cohort: patients aged 65 or over at two or more admissions.
`clinical-env sources mimic mimic/raw` prints the markdown used in docs/record-patterns.md.
"""

from __future__ import annotations

import csv
import gzip
import re
import statistics
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

HOSP = "mimic-iv-clinical-database-demo-2.2/hosp"
ED = "mimic-iv-ed-demo-2.2/ed"
MIN_AGE = 65
MIN_ADMISSIONS = 2
SUPPRESS_BELOW = 5

Row = dict[str, str]

# ICD-9 and ICD-10 code prefixes (no dots, as MIMIC stores them).
CHRONIC = {
    "hypertension": ("401", "I10"),
    "diabetes": ("250", "E10", "E11"),
    "chronic kidney disease": ("585", "N18"),
    "atrial fibrillation": ("42731", "I48"),
    "heart failure": ("428", "I50"),
    "dementia": ("290", "2941", "3310", "F01", "F02", "F03", "G30"),
    "COPD": ("491", "492", "496", "J44"),
    "hypothyroidism": ("244", "E03"),
}
HISTORY_OF = ("V10", "V11", "V12", "V13", "V14", "V15", "Z85", "Z86", "Z87")
LONG_TERM_DRUG = ("V586", "Z79")
UPPER_GI = ("530", "531", "532", "533", "534", "535", "5789", "K20", "K21", "K22", "K25", "K26",
            "K27", "K28", "K29", "K92")  # fmt: skip
PSYCH = ("290", "293", "295", "296", "297", "298", "F0", "F2", "F3", "R41")
DIABETES = CHRONIC["diabetes"]
PPI = ("pantoprazole", "omeprazole", "esomeprazole", "lansoprazole")
ANTIPSYCHOTIC = ("quetiapine", "haloperidol", "olanzapine", "risperidone")
SEDATIVE = ("lorazepam", "diazepam", "alprazolam", "clonazepam", "zolpidem", "temazepam")
CARDIO = ("metoprolol", "amlodipine", "lisinopril", "losartan", "furosemide", "carvedilol",
          "hydralazine", "torsemide")  # fmt: skip
HELD = ("Not Given", "Hold Dose")
_WORD = re.compile(r"[a-z]+")


def count(n: int) -> str:
    return f"<{SUPPRESS_BELOW}" if 0 < n < SUPPRESS_BELOW else str(n)


def share(n: int, of: int) -> str:
    """n of a total, hiding a small total, a small n, or a small remainder (18 of 20 shows 2)."""
    if of == 0:
        return "n/a"
    if of < SUPPRESS_BELOW:
        return f"n/a (fewer than {SUPPRESS_BELOW})"
    if 0 < n < SUPPRESS_BELOW or 0 < of - n < SUPPRESS_BELOW:
        return f"suppressed (of {of})"
    return f"{n} of {of} ({100 * n / of:.0f}%)"


def spread(values: Sequence[float]) -> str:
    """Median and interquartile range (never a single patient's minimum or maximum)."""
    if len(values) < SUPPRESS_BELOW:
        return "n/a (too few)"
    q1, med, q3 = statistics.quantiles(values, n=4)
    return f"median {med:g} (IQR {q1:g}-{q3:g})"


def drug_name(text: str) -> str:
    """The first word of a medicine name, lowercased: 'Metoprolol Tartrate' -> 'metoprolol'."""
    found = _WORD.findall(text.lower())
    return found[0] if found else ""


def full_name(text: str) -> str:
    return " ".join(_WORD.findall(text.lower()))


def read(root: Path, table: str) -> list[Row]:
    with gzip.open(root / f"{table}.csv.gz", "rt", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


@dataclass
class Data:
    patients: list[Row]
    admissions: list[Row]
    diagnoses: list[Row]
    prescriptions: list[Row]
    emar: list[Row]
    edstays: list[Row]
    medrecon: list[Row]

    @classmethod
    def load(cls, root: Path) -> Data:
        return cls(
            patients=read(root, f"{HOSP}/patients"),
            admissions=read(root, f"{HOSP}/admissions"),
            diagnoses=read(root, f"{HOSP}/diagnoses_icd"),
            prescriptions=read(root, f"{HOSP}/prescriptions"),
            emar=read(root, f"{HOSP}/emar"),
            edstays=read(root, f"{ED}/edstays"),
            medrecon=read(root, f"{ED}/medrecon"),
        )


def _time(text: str) -> datetime:
    return datetime.fromisoformat(text)


def older_admissions(data: Data) -> dict[str, list[Row]]:
    """Each patient's admissions at age 65+, oldest first (MIMIC age = anchor_age + years)."""
    patients = {p["subject_id"]: p for p in data.patients}
    by_patient: dict[str, list[Row]] = defaultdict(list)
    for a in data.admissions:
        p = patients[a["subject_id"]]
        age = int(p["anchor_age"]) + _time(a["admittime"]).year - int(p["anchor_year"])
        if age >= MIN_AGE:
            by_patient[a["subject_id"]].append(a)
    return {s: sorted(v, key=lambda a: a["admittime"]) for s, v in by_patient.items()}


def _codes(data: Data) -> dict[str, set[str]]:
    codes: dict[str, set[str]] = defaultdict(set)
    for d in data.diagnoses:
        codes[d["hadm_id"]].add(d["icd_code"].strip().upper())
    return codes


def _has(codes: Iterable[str], prefixes: Sequence[str]) -> bool:
    return any(c.startswith(tuple(prefixes)) for c in codes)


def _orders(data: Data) -> dict[str, list[Row]]:
    orders: dict[str, list[Row]] = defaultdict(list)
    for rx in data.prescriptions:
        if rx["drug_type"] == "MAIN":
            orders[rx["hadm_id"]].append(rx)
    return orders


def report(data: Data) -> str:
    older = older_admissions(data)
    cohort = {s: v for s, v in older.items() if len(v) >= MIN_ADMISSIONS}
    hadms = [a["hadm_id"] for v in cohort.values() for a in v]
    codes = _codes(data)
    orders = _orders(data)
    out = [
        "## Counts from the MIMIC-IV demo (generated)",
        "",
        f"Cohort: {count(len(cohort))} patients aged {MIN_AGE}+ at {MIN_ADMISSIONS}+ "
        f"admissions, {count(len(hadms))} admissions. Counts of 1-4 show as <5.",
        "",
        *_timeline(cohort),
        *_problem_list(cohort, codes),
        *_prescribing(hadms, codes, orders),
        *_given(data, set(hadms)),
        *_home_list(data, older, orders),
    ]
    return "\n".join(out) + "\n"


def _timeline(cohort: dict[str, list[Row]]) -> list[str]:
    gaps = [
        (_time(b["admittime"]) - _time(a["dischtime"])).days
        for v in cohort.values()
        for a, b in zip(v, v[1:], strict=False)
    ]
    bands = Counter(
        "within 30 days" if g <= 30 else "31-90 days" if g <= 90 else "91-365 days"
        if g <= 365 else "over a year"
        for g in gaps
    )  # fmt: skip
    places = Counter(a["discharge_location"] or "not recorded" for v in cohort.values() for a in v)
    lines = ["### Admissions timeline", ""]
    lines.append(
        f"- Gap from discharge to the next admission ({count(len(gaps))} gaps): "
        + ", ".join(
            f"{b} {count(bands[b])}"
            for b in ("within 30 days", "31-90 days", "91-365 days", "over a year")
        )
    )
    lines.append(
        "- Discharged to: "
        + ", ".join(f"{place.lower()} {count(n)}" for place, n in places.most_common())
    )
    return [*lines, ""]


def _problem_list(cohort: dict[str, list[Row]], codes: dict[str, set[str]]) -> list[str]:
    per_admission = [len(codes[a["hadm_id"]]) for v in cohort.values() for a in v]
    pairs = vanished = 0
    vanished_by: Counter[str] = Counter()
    for v in cohort.values():
        for a, b in zip(v, v[1:], strict=False):
            pairs += 1
            gone = [
                name
                for name, prefixes in CHRONIC.items()
                if _has(codes[a["hadm_id"]], prefixes) and not _has(codes[b["hadm_id"]], prefixes)
            ]
            vanished += bool(gone)
            vanished_by.update(gone)
    hadms = [a["hadm_id"] for v in cohort.values() for a in v]
    history = sum(_has(codes[h], HISTORY_OF) for h in hadms)
    long_term = sum(_has(codes[h], LONG_TERM_DRUG) for h in hadms)
    return [
        "### Coded problem list",
        "",
        f"- Diagnosis codes per admission: {spread(per_admission)}.",
        f"- A chronic condition coded at one admission and absent at the next: "
        f"{share(vanished, pairs)} consecutive admission pairs. Most often: "
        + (", ".join(f"{n} {count(k)}" for n, k in vanished_by.most_common(4)) or "none")
        + ".",
        f"- Admissions with a 'personal history of' code: {share(history, len(hadms))}; with a "
        f"'long-term (current) use of' drug code: {share(long_term, len(hadms))}.",
        "",
    ]


def _prescribing(
    hadms: list[str], codes: dict[str, set[str]], orders: dict[str, list[Row]]
) -> list[str]:
    per_admission = [len({drug_name(o["drug"]) for o in orders[h]}) for h in hadms]

    def ordered(h: str, names: Sequence[str]) -> bool:
        return any(drug_name(o["drug"]) in names for o in orders[h])

    ppi = [h for h in hadms if ordered(h, PPI)]
    psych = [h for h in hadms if ordered(h, ANTIPSYCHOTIC)]
    insulin = [h for h in hadms if ordered(h, ("insulin",))]
    sedative = sum(ordered(h, SEDATIVE) for h in hadms)
    return [
        "### Hospital prescribing",
        "",
        f"- Different medicines ordered per admission: {spread(per_admission)}.",
        "- Started with no matching coded indication: proton pump inhibitor with no upper GI "
        f"code {share(sum(not _has(codes[h], UPPER_GI) for h in ppi), len(ppi))} admissions "
        "where one was ordered; antipsychotic with no psychiatric, delirium or dementia code "
        f"{share(sum(not _has(codes[h], PSYCH) for h in psych), len(psych))}; insulin with no "
        f"diabetes code {share(sum(not _has(codes[h], DIABETES) for h in insulin), len(insulin))}.",
        f"- A benzodiazepine or Z-drug ordered: {share(sedative, len(hadms))} admissions.",
        "",
    ]


def _given(data: Data, hadms: set[str]) -> list[str]:
    events = [e for e in data.emar if e["hadm_id"] in hadms]
    doses = [e for e in events if e["event_txt"] in ("Administered", *HELD)]
    held = [e for e in doses if e["event_txt"] in HELD]
    by_drug = Counter(
        drug_name(e["medication"]) for e in held if drug_name(e["medication"]) in CARDIO
    )
    given = Counter(
        drug_name(e["medication"]) for e in doses if drug_name(e["medication"]) in CARDIO
    )
    return [
        "### Prescribed vs given (eMAR)",
        "",
        f"- Doses charted as not given or held: {share(len(held), len(doses))} charted doses.",
        "- Blood pressure and heart medicines not given or held, of doses charted: "
        + (", ".join(f"{d} {share(n, given[d])}" for d, n in by_drug.most_common()) or "none")
        + ".",
        "",
    ]


def _home_list(data: Data, older: dict[str, list[Row]], orders: dict[str, list[Row]]) -> list[str]:
    older_hadms = {a["hadm_id"] for v in older.values() for a in v}
    stays = [s for s in data.edstays if s["hadm_id"] in older_hadms]
    home: dict[str, set[str]] = defaultdict(set)
    home_full: dict[str, set[str]] = defaultdict(set)
    for m in data.medrecon:
        name = drug_name(m["name"].lstrip("*"))
        if name:
            home[m["stay_id"]].add(name)
            home_full[m["stay_id"]].add(full_name(m["name"]))
    listed = [s for s in stays if home[s["stay_id"]]]
    meds = missing = stays_missing = formulation = 0
    new_starts: list[float] = []
    for s in listed:
        ordered = {drug_name(o["drug"]) for o in orders[s["hadm_id"]]}
        ordered_full = {full_name(o["drug"]) for o in orders[s["hadm_id"]]}
        gone = home[s["stay_id"]] - ordered
        meds += len(home[s["stay_id"]])
        missing += len(gone)
        stays_missing += bool(gone)
        formulation += sum(
            1
            for full in home_full[s["stay_id"]]
            if drug_name(full) in ordered and full not in ordered_full and " " in full
        )
        new_starts.append(len(ordered - home[s["stay_id"]]))
    ed_patients = {s["subject_id"] for s in data.edstays}
    hosp_patients = {p["subject_id"] for p in data.patients}
    return [
        "### ED home-medicine list vs the admission's orders",
        "",
        f"- ED demo patients who are also in the hospital demo: "
        f"{share(len(ed_patients & hosp_patients), len(ed_patients))}.",
        f"- Admitted ED stays of patients aged {MIN_AGE}+ with a home-medicine list: "
        f"{count(len(listed))}.",
        f"- Home medicines never ordered during the admission: {share(missing, meds)} listed "
        f"medicines; stays with at least one: {share(stays_missing, len(listed))}.",
        f"- Home medicine ordered under another formulation or salt (same first word, different "
        f"name): {count(formulation)} medicines.",
        f"- Medicines ordered in hospital that were not on the home list, per stay: "
        f"{spread(new_starts)}.",
        "",
    ]


def main(root: Path) -> int:
    print(report(Data.load(root)), end="")
    return 0
