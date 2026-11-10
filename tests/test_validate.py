"""Validator behaviour: the dev cases pass, and each authoring mistake is caught by name."""

from __future__ import annotations

import copy
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml

from clinical_env.validate import validate_paths

CASES = Path(__file__).resolve().parents[1] / "cases" / "dev"
BASE = CASES / "edith_marsh.yaml"
TWIN = CASES / "edith_marsh_twin.yaml"

Data = dict[str, Any]


def load(path: Path) -> Data:
    data = yaml.safe_load(path.read_text())
    assert isinstance(data, dict)
    return data


def write(directory: Path, data: Data) -> Path:
    path = directory / f"{data['id']}.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    return path


def errors_for(tmp_path: Path, mutate: Callable[[Data], object], source: Path = BASE) -> list[str]:
    data = copy.deepcopy(load(source))
    mutate(data)
    if source == TWIN:
        write(tmp_path, load(BASE))
    results = validate_paths([write(tmp_path, data)])
    return results[0].errors


def fact(data: Data, fact_id: str) -> Data:
    for facts in data["views"].values():
        for item in facts:
            if item["id"] == fact_id:
                assert isinstance(item, dict)
                return item
    raise KeyError(fact_id)


def rubric(data: Data, item_id: str) -> Data:
    item = next(r for r in data["rubric"] if r["id"] == item_id)
    assert isinstance(item, dict)
    return item


def exam(data: Data, finding_id: str) -> Data:
    found: Data = next(e for e in data["visits"][0]["examination"] if e["id"] == finding_id)
    return found


def test_dev_cases_are_valid() -> None:
    results = validate_paths([CASES])
    assert [(r.path.name, r.errors) for r in results] == [
        ("dot_fairbanks.yaml", []),
        ("edith_marsh.yaml", []),
        ("edith_marsh_twin.yaml", []),
        ("gene_ostrander.yaml", []),
        ("harold_benning.yaml", []),
        ("marjorie_lindqvist.yaml", []),
        ("pat_ellison.yaml", []),
        ("pat_ellison_noise.yaml", []),
        ("pat_ellison_twin.yaml", []),
        ("ray_kowalczyk.yaml", []),
        ("reg_holloway.yaml", []),
        ("walt_brenner.yaml", []),
    ]


def test_twin_alone_finds_its_base_beside_it() -> None:
    [result] = validate_paths([TWIN])
    assert result.ok, result.errors


def _drop_criticals(data: Data, keep: int) -> None:
    seen = 0
    for item in data["rubric"]:
        if item.get("critical"):
            seen += 1
            if seen > keep:
                item["critical"] = False
                item.pop("critical_type")


def _add_criticals(data: Data, extra: int) -> None:
    for item in [r for r in data["rubric"] if not r.get("critical") and r["kind"] == "must_do"][
        :extra
    ]:
        item["critical"] = True
        item["critical_type"] = "clinical_action"


BASE_MISTAKES: list[tuple[str, Callable[[Data], object], str]] = [
    (
        "critical without evidence",
        lambda d: rubric(d, "v1_reconcile_meds").pop("evidence"),
        "rubric v1_reconcile_meds: evidence: a critical item lists the ids it depends on",
    ),
    (
        "critical resting on records alone",
        lambda d: rubric(d, "v1_reconcile_meds").update(evidence=["d_furosemide", "g_meds"]),
        "rubric v1_reconcile_meds: evidence: everything listed is in a record or volunteered; "
        "a critical needs at least one fact a person gives when asked (or says at a later "
        "visit), an examination finding or a test result",
    ),
    (
        "visit-2 critical resting on a visit-2 record line alone",
        lambda d: rubric(d, "v2_confusion").update(evidence=["a2_fall"]),
        "rubric v2_confusion: evidence: everything listed is in a record or volunteered; "
        "a critical needs at least one fact a person gives when asked (or says at a later "
        "visit), an examination finding or a test result",
    ),
    (
        "critical evidence that does not exist",
        lambda d: rubric(d, "v1_reconcile_meds").update(evidence=["x_dosette", "p_nope"]),
        "rubric v1_reconcile_meds: evidence p_nope: no such fact, examination finding or "
        "test result",
    ),
    (
        "visit-1 critical resting on a visit-2 fact",
        lambda d: rubric(d, "v1_reconcile_meds").update(evidence=["c2_dosette"]),
        "rubric v1_reconcile_meds: evidence c2_dosette only applies from visit 2",
    ),
    (
        "fact points at missing truth",
        lambda d: fact(d, "g_falls").update(truth="t_nope"),
        "fact g_falls (gp_record): truth t_nope is not a hidden_truth id",
    ),
    (
        "hidden fact without reveal condition",
        lambda d: fact(d, "p_dizzy").pop("reveal_condition"),
        "fact p_dizzy (patient): a hidden fact needs a reveal_condition",
    ),
    (
        "reveal condition on a non-hidden fact",
        lambda d: fact(d, "p_frame").update(reveal_condition="asked about the frame"),
        "fact p_frame (patient): reveal_condition is only for hidden facts",
    ),
    (
        "person fact without disclosure",
        lambda d: fact(d, "c_falls").pop("disclosure"),
        "fact c_falls (carer): a person's fact needs disclosure",
    ),
    (
        "record fact with disclosure",
        lambda d: fact(d, "g_meds").update(disclosure="if_asked"),
        "fact g_meds (gp_record): records have no disclosure; reading shows the whole record",
    ),
    (
        "only one critical item",
        lambda d: _drop_criticals(d, keep=1),
        "a case needs 2-5 critical items, got 1",
    ),
    (
        "six critical items",
        lambda d: _add_criticals(d, extra=2),
        "a case needs 2-5 critical items, got 6",
    ),
    (
        "critical without a stage",
        lambda d: rubric(d, "v1_falls_function").pop("stage"),
        "rubric v1_falls_function: a critical item needs a stage",
    ),
    (
        "no messiness level",
        lambda d: d.pop("messiness"),
        "messiness: Field required",
    ),
    (
        "carer trait on the patient",
        lambda d: d["personas"]["patient"]["traits"].append("carer_dominates"),
        "personas.patient: carer_dominates is a carer trait",
    ),
    (
        "record tagged as contradicting with no conflict",
        lambda d: (
            d["record_traits"].update(pharmacy_record=["contradicts_other_records"])
            or d.update(conflicts=[c for c in d["conflicts"] if c["id"] != "cf_furosemide"])
        ),
        "record_traits.pharmacy_record: contradicts_other_records, but none of its facts is in "
        "a conflict",
    ),
    (
        "record tagged outdated with no outdated fact",
        lambda d: d["record_traits"].update(care_agency_notes=["outdated_entries"]),
        "record_traits.care_agency_notes: outdated_entries, but none of its facts is outdated",
    ),
    (
        "discrepancy_detection critical with no conflicts",
        lambda d: (
            rubric(d, "v1_care_package").update(critical_type="discrepancy_detection")
            or d.update(conflicts=[])
        ),
        "rubric v1_care_package: discrepancy_detection needs a conflict in the case",
    ),
    (
        "critical without a type",
        lambda d: rubric(d, "v1_falls_function").pop("critical_type"),
        "rubric v1_falls_function: a critical item needs critical_type",
    ),
    (
        "rubric item for a visit that does not exist",
        lambda d: rubric(d, "v2_phone_only").update(visit=3),
        "rubric v2_phone_only: visit 3 does not exist",
    ),
    (
        "examination on a phone visit",
        lambda d: d["visits"][1].update(
            examination=[{"id": "x_bp", "label": "BP", "finding": "120/80"}]
        ),
        "visit 2: a phone visit has no examination findings",
    ),
    (
        "events before the first visit",
        lambda d: d["visits"][0].update(events_since_last=["something happened"]),
        "visit 1: the first visit has no events_since_last",
    ),
    (
        "visit numbering gap",
        lambda d: d["visits"][1].update(number=3),
        "visits must be numbered 1..2 in order, got [1, 3]",
    ),
    (
        "only one visit",
        lambda d: d.update(
            visits=d["visits"][:1], rubric=[r for r in d["rubric"] if r["visit"] == 1]
        ),
        "a case needs 2-3 visits, got 1",
    ),
    (
        "carer present without a carer persona",
        lambda d: (d["personas"].pop("carer"), d["views"].pop("carer")),
        "visit 1: carer present but the case has no carer persona",
    ),
    (
        "conflict where every fact is true",
        lambda d: d["conflicts"].append(
            {
                "id": "cf_all_true",
                "facts": ["d_fall", "a_floor"],
                "truth": ["t_falls"],
                "expected_behaviour": "x",
            }
        ),
        "conflict cf_all_true: every fact is true, so nothing disagrees",
    ),
    (
        "conflict names an unknown fact",
        lambda d: d["conflicts"][0]["facts"].append("zz_missing"),
        "conflict cf_furosemide: fact zz_missing is not in any view",
    ),
    (
        "wrong fact left out of every conflict",
        lambda d: d["conflicts"][1]["facts"].remove("c_falls"),
        "fact c_falls is wrong but in no conflict",
    ),
    (
        "no conflicts at all",
        lambda d: d.update(conflicts=[]),
        "conflicts: a case needs at least one conflict between sources",
    ),
    (
        "duplicate fact id",
        lambda d: fact(d, "a_meals").update(id="a_missed"),
        "duplicate fact id a_missed",
    ),
    (
        "unknown source",
        lambda d: d["views"].update(social_worker=[]),
        "views: unknown source social_worker; use one of patient, carer, gp_record, "
        "care_agency_notes, discharge_summary, pharmacy_record, ambulance_report",
    ),
    (
        "record never available",
        lambda d: [v.update(records_available=["gp_record"]) for v in d["visits"]],
        "views: pharmacy_record has facts but is never available when they apply",
    ),
    (
        "document slot names an unknown fact",
        lambda d: d["documents"].update(gp_record=d["documents"]["gp_record"] + "[[zz_nope]]\n"),
        "documents.gp_record: [[zz_nope]] is not a fact in the gp_record view",
    ),
    (
        "record fact missing from its document",
        lambda d: d["documents"].update(
            gp_record=d["documents"]["gp_record"].replace("[[g_bppv]]", "BPPV")
        ),
        "documents.gp_record: fact g_bppv must appear exactly once, found 0",
    ),
    (
        "record fact twice in its document",
        lambda d: d["documents"].update(gp_record=d["documents"]["gp_record"] + "[[g_bppv]]\n"),
        "documents.gp_record: fact g_bppv must appear exactly once, found 2",
    ),
    (
        "fact on a line dated after the visit it applies to",
        lambda d: d["documents"].update(
            gp_record=d["documents"]["gp_record"].replace("[[g_meds]]", "{day:3} [[g_meds]]")
        ),
        "documents.gp_record: [[g_meds]] sits on a line dated after visit 1, "
        "so it would be hidden when it applies",
    ),
    (
        "malformed date token",
        lambda d: d["documents"].update(gp_record=d["documents"]["gp_record"] + "{day:soon} x\n"),
        "documents.gp_record: bad date {day:soon}; use {day:-21} or {weekday:-9}",
    ),
    (
        "document for a record never available",
        lambda d: [v["records_available"].remove("ambulance_report") for v in d["visits"]],
        "documents.ambulance_report: this record is never available at a visit",
    ),
    (
        "visit days out of order",
        lambda d: d["visits"][1].update(day=0),
        "visit days must increase, got [0, 0]",
    ),
    (
        "first visit not on day 0",
        lambda d: d["visits"][0].update(day=2),
        "visit 1 must be day 0 (days count from the first visit)",
    ),
    (
        "fact window past the last visit",
        lambda d: fact(d, "c2_alarm").update(from_visit=3),
        "fact c2_alarm (carer): from_visit 3 is after the last visit (2)",
    ),
    (
        "misspelt key",
        lambda d: fact(d, "g_meds").update(acuracy="true"),
        "views.gp_record.0.acuracy: Extra inputs are not permitted",
    ),
    (
        "fact known before its truth happens",
        lambda d: fact(d, "c2_not_coping").pop("from_visit"),
        "fact c2_not_coping (carer): applies from visit 1 "
        "but truth t_fall_2 only starts at visit 2",
    ),
    (
        "true fact outlives its truth",
        lambda d: next(t for t in d["hidden_truth"] if t["id"] == "t_alarm").update(until_visit=1),
        "fact p_alarm (patient): is true after truth t_alarm ends (visit 1)",
    ),
    (
        "person fact never reachable",
        lambda d: fact(d, "p_frame").update(from_visit=2),
        "fact p_frame (patient): patient is never present at a visit this fact applies to",
    ),
    (
        "conflict truth does not match its facts",
        lambda d: d["conflicts"][4].update(truth=["t_alarm"]),
        "conflict cf_care: fact g_care is about t_care_delivered, which is not in this "
        "conflict's truth",
    ),
    (
        "conflict lists a fact twice",
        lambda d: d["conflicts"][4].update(facts=["g_care", "g_care"]),
        "conflict cf_care: a fact is listed twice",
    ),
    (
        "critical_type on a non-critical item",
        lambda d: rubric(d, "v1_amlodipine").update(critical_type="clinical_action"),
        "rubric v1_amlodipine: critical_type is only for critical items",
    ),
    (
        "until_visit before from_visit",
        lambda d: fact(d, "c2_alarm").update(until_visit=1),
        "fact c2_alarm (carer): until_visit 1 must be between 2 and 2",
    ),
    (
        "carer persona without a carer view",
        lambda d: d["views"].pop("carer"),
        "personas: a carer persona needs a carer view",
    ),
    (
        "no patient view",
        lambda d: d["views"].pop("patient"),
        "views: the patient needs a view",
    ),
    (
        "someone listed twice in present",
        lambda d: d["visits"][1].update(present=["carer", "carer"]),
        "visit 2: someone is listed twice in present",
    ),
    (
        "ISO date",
        lambda d: d["patient"].update(summary="Born 1941-03-12"),
        "'1941-03-12' looks like an absolute date; case content must be fictional "
        "(use relative times such as '3 weeks ago')",
    ),
    (
        "written date",
        lambda d: d["patient"].update(summary="Seen on 12 March 2026"),
        "'12 March 2026' looks like an absolute date; case content must be fictional "
        "(use relative times such as '3 weeks ago')",
    ),
    (
        "exam set with its own text too",
        lambda d: exam(d, "x_obs").update(finding="All normal."),
        "visit 1: exam finding x_obs needs either a finding or parts, not both or neither",
    ),
    (
        "exam finding with no text and no parts",
        lambda d: exam(d, "x_pulse").pop("finding"),
        "visit 1: exam finding x_pulse needs either a finding or parts, not both or neither",
    ),
    (
        "exam set with an unknown part",
        lambda d: exam(d, "x_obs").update(parts=["x_pulse", "x_nope"]),
        "visit 1: exam finding x_obs: part x_nope is not another finding at this visit",
    ),
    (
        "exam set with one part",
        lambda d: exam(d, "x_obs").update(parts=["x_pulse", "x_pulse"]),
        "visit 1: exam finding x_obs: a set needs at least two different parts",
    ),
    (
        "NHS-number-like string",
        lambda d: d["patient"].update(summary="NHS 943 476 5919"),
        "'943 476 5919' looks like an NHS number; case content must be fictional "
        "(use relative times such as '3 weeks ago')",
    ),
    (
        "absolute date",
        lambda d: d["patient"].update(summary="Born 12/03/1941"),
        "'12/03/1941' looks like an absolute date; case content must be fictional "
        "(use relative times such as '3 weeks ago')",
    ),
    (
        "US-order absolute date",
        lambda d: d["patient"].update(summary="Seen on March 12, 2026"),
        "'March 12, 2026' looks like an absolute date; case content must be fictional "
        "(use relative times such as '3 weeks ago')",
    ),
    (
        "social security number",
        lambda d: d["patient"].update(summary="SSN 219-09-9999"),
        "'219-09-9999' looks like a social security number; case content must be fictional "
        "(use relative times such as '3 weeks ago')",
    ),
    (
        "medical record number",
        lambda d: d["patient"].update(summary="MRN: 00482913"),
        "'MRN: 00482913' looks like a medical record number; case content must be fictional "
        "(use relative times such as '3 weeks ago')",
    ),
    (
        "no country",
        lambda d: d.pop("country"),
        "country: Field required",
    ),
]


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [pytest.param(m, e, id=name) for name, m, e in BASE_MISTAKES],
)
def test_base_case_mistakes_are_reported(
    tmp_path: Path, mutate: Callable[[Data], object], expected: str
) -> None:
    assert expected in errors_for(tmp_path, mutate)


TWIN_MISTAKES: list[tuple[str, Callable[[Data], object], str]] = [
    (
        "twin with a wrong fact",
        lambda d: fact(d, "c_falls").update(accuracy="wrong"),
        "fact c_falls (carer): a twin's sources are all accurate, got wrong",
    ),
    (
        "twin with an outdated record",
        lambda d: fact(d, "g_care").update(accuracy="outdated"),
        "fact g_care (gp_record): a twin's sources are all accurate, got outdated",
    ),
    (
        "twin drops a clinical_action critical",
        lambda d: d.update(rubric=[r for r in d["rubric"] if r["id"] != "v2_confusion"]),
        "twin must keep clinical_action critical v2_confusion from edith_marsh unchanged",
    ),
    (
        "twin rewords a clinical_action critical",
        lambda d: rubric(d, "v1_reconcile_meds").update(description="Stops furosemide."),
        "twin must keep clinical_action critical v1_reconcile_meds from edith_marsh unchanged",
    ),
    (
        "twin keeps a discrepancy_detection critical",
        lambda d: rubric(d, "v1_amlodipine").update(
            critical=True, critical_type="discrepancy_detection"
        ),
        "rubric v1_amlodipine: a twin has no conflicts, so no discrepancy_detection",
    ),
    (
        "twin adds a critical the base does not have",
        lambda d: rubric(d, "v1_amlodipine").update(critical=True, critical_type="clinical_action"),
        "rubric v1_amlodipine: a twin's criticals must be the base's clinical_action criticals; "
        "it cannot add new ones",
    ),
    (
        "twin of a case that does not exist",
        lambda d: d.update(twin_of="nobody"),
        "twin_of nobody: no nobody.yaml beside this file",
    ),
    (
        "twin lacks a fact the reused base document needs",
        lambda d: d["views"].update(
            ambulance_report=[f for f in d["views"]["ambulance_report"] if f["id"] != "m_fall"]
        ),
        "documents.ambulance_report: [[m_fall]] is not a fact in the ambulance_report view",
    ),
    (
        "twin tries to override truth",
        lambda d: d.update(hidden_truth=[]),
        "hidden_truth: Extra inputs are not permitted",
    ),
]


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [pytest.param(m, e, id=name) for name, m, e in TWIN_MISTAKES],
)
def test_twin_mistakes_are_reported(
    tmp_path: Path, mutate: Callable[[Data], object], expected: str
) -> None:
    assert expected in errors_for(tmp_path, mutate, source=TWIN)


def test_file_name_must_match_case_id(tmp_path: Path) -> None:
    path = tmp_path / "edith.yaml"
    path.write_text(BASE.read_text())
    [result] = validate_paths([path])
    assert result.errors == ["file name must match case id: rename to edith_marsh.yaml"]


def test_invalid_yaml_and_non_mapping_are_reported(tmp_path: Path) -> None:
    broken = tmp_path / "broken.yaml"
    broken.write_text("id: [unclosed\n")
    listing = tmp_path / "listing.yaml"
    listing.write_text("- just\n- a list\n")
    results = {r.path.name: r.errors for r in validate_paths([broken, listing])}
    assert results["broken.yaml"][0].startswith("invalid YAML:")
    assert results["listing.yaml"] == ["a case file must be a YAML mapping"]


def test_missing_file_is_reported(tmp_path: Path) -> None:
    [result] = validate_paths([tmp_path / "absent.yaml"])
    assert result.errors[0].startswith("cannot read file:")


def test_twin_of_invalid_base_is_reported(tmp_path: Path) -> None:
    base = load(BASE)
    base["visits"][0]["setting"] = "telepathy"
    write(tmp_path, base)
    twin_path = write(tmp_path, load(TWIN))
    results = {r.path.name: r.errors for r in validate_paths([twin_path])}
    assert results["edith_marsh_twin.yaml"] == [
        "twin_of edith_marsh: base case is invalid; fix it first"
    ]


def test_twin_of_a_base_failing_cross_checks_is_reported(tmp_path: Path) -> None:
    base = load(BASE)
    base["conflicts"] = []  # parses, but fails check_case
    write(tmp_path, base)
    twin_path = write(tmp_path, load(TWIN))
    [result] = validate_paths([twin_path])
    assert result.errors == ["twin_of edith_marsh: base case is invalid; fix it first"]


def test_twin_of_a_twin_is_reported(tmp_path: Path) -> None:
    write(tmp_path, load(BASE))
    write(tmp_path, load(TWIN))
    second = load(TWIN)
    second.update(id="edith_marsh_twin2", twin_of="edith_marsh_twin")
    write(tmp_path, second)
    results = {r.path.name: r.errors for r in validate_paths([tmp_path])}
    assert results["edith_marsh_twin2.yaml"] == ["twin_of edith_marsh_twin is itself a twin"]
    assert results["edith_marsh.yaml"] == results["edith_marsh_twin.yaml"] == []


def test_base_without_clinical_action_critical_cannot_have_twin() -> None:
    from clinical_env.case_schema import Case, CriticalType, TwinSpec
    from clinical_env.validate import check_twin

    base = Case.model_validate(load(BASE))
    detection_only = base.model_copy(
        update={
            "rubric": [
                r.model_copy(update={"critical_type": CriticalType.DISCREPANCY_DETECTION})
                if r.critical
                else r
                for r in base.rubric
            ]
        }
    )
    twin = TwinSpec.model_validate(load(TWIN)).resolve(detection_only)
    assert (
        "base case edith_marsh has no clinical_action critical, so a twin is useless"
        in check_twin(twin, detection_only)
    )


def test_duplicate_case_id_across_files_is_reported(tmp_path: Path) -> None:
    first = tmp_path / "a"
    second = tmp_path / "b"
    first.mkdir()
    second.mkdir()
    write(first, load(BASE))
    write(second, load(BASE))
    results = validate_paths([first, second])
    assert results[0].ok
    assert results[1].errors == [f"case id edith_marsh also used by {first / 'edith_marsh.yaml'}"]


def test_a_must_not_do_can_be_critical(tmp_path: Path) -> None:
    def swap(data: Data) -> None:
        rubric(data, "v1_care_package").update(critical=False)
        rubric(data, "v1_care_package").pop("critical_type")
        rubric(data, "v1_care_home").update(
            critical=True, critical_type="clinical_action", evidence=["c_strain"]
        )

    assert errors_for(tmp_path, swap) == []
