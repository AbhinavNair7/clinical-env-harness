"""Requested tests: what the plan orders at one visit is back in the chart at the next."""

from __future__ import annotations

import asyncio
import copy
import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from conftest import CASES, FakeModel
from test_case_run import Models
from test_visit import PLAN, Scripted

from clinical_env import prompts
from clinical_env.case_run import CaseLog, run_case
from clinical_env.case_schema import Case, OrderedTest, Visit
from clinical_env.plan import Plan
from clinical_env.run import headings
from clinical_env.transcript import render_case_markdown
from clinical_env.validate import load_case, validate_paths
from clinical_env.views import display_names, get_visit
from clinical_env.visit import ReadRecord, SubmitPlan, match_results

BLOODS = OrderedTest(id="r_cbc", label="CBC", finding="Hemoglobin 10.9 g/dL (low).")
TSH = OrderedTest(id="r_tsh", label="TSH", finding="TSH 11.2 (high).")


def plan_with(*orders: tuple[str, str]) -> Plan:
    data = copy.deepcopy(PLAN)
    data["actions"] += [
        {"type": kind, "detail": detail, "rationale": "to find out", "urgency": "routine"}
        for kind, detail in orders
    ]
    return Plan.model_validate(data)


def matcher(reply: dict[str, Any] | str) -> FakeModel:
    text = reply if isinstance(reply, str) else json.dumps(reply)
    return FakeModel(lambda system, user: text)


def visit_with(edith: Case, results: list[OrderedTest] | None) -> Visit:
    return get_visit(edith, 1).model_copy(update={"results": results})


def test_listed_tests_return_their_finding_and_other_tests_come_back_normal(edith: Case) -> None:
    plan = plan_with(("investigation", "Full blood count and B12"), ("referral", "Falls clinic"))
    model = matcher({"orders": [{"order": 1, "ids": ["r_cbc"], "other": True}]})
    [match] = asyncio.run(match_results(visit_with(edith, [BLOODS, TSH]), plan, model))
    assert match.result_ids == ["r_cbc"]
    assert match.text == f"CBC: Hemoglobin 10.9 g/dL (low). {prompts.RESULT_OTHER_NORMAL}"
    assert match.error is None
    # The referral is not a test, so only the investigation reached the matcher.
    assert "Falls clinic" not in model.calls[0][-1].content


def test_an_unlisted_test_comes_back_normal(edith: Case) -> None:
    plan = plan_with(("investigation", "Vitamin D level"))
    model = matcher({"orders": [{"order": 1, "ids": [], "other": True}]})
    [match] = asyncio.run(match_results(visit_with(edith, [BLOODS]), plan, model))
    assert match.result_ids == [] and match.text == "Vitamin D level: no abnormality found."


def test_an_empty_results_list_means_everything_is_normal_without_a_model_call(
    edith: Case,
) -> None:
    model = matcher("never called")
    plan = plan_with(("investigation", "CBC"))
    [match] = asyncio.run(match_results(visit_with(edith, []), plan, model))
    assert match.text == "CBC: no abnormality found." and model.calls == []


def test_no_orders_no_call(edith: Case) -> None:
    model = matcher("never called")
    assert asyncio.run(match_results(visit_with(edith, [BLOODS]), plan_with(), model)) == []
    assert model.calls == []


def test_an_unreadable_reply_shows_not_back_yet_and_logs_the_error(edith: Case) -> None:
    plan = plan_with(("investigation", "CBC"))
    [match] = asyncio.run(match_results(visit_with(edith, [BLOODS]), plan, matcher("no json")))
    assert match.text == "CBC: result not back yet." and match.error


def test_an_unknown_id_is_not_back_yet_never_a_false_normal(edith: Case) -> None:
    plan = plan_with(("investigation", "CBC and a CT"))
    model = matcher({"orders": [{"order": 1, "ids": ["r_cbc", "r_ct"], "other": False}]})
    [match] = asyncio.run(match_results(visit_with(edith, [BLOODS]), plan, model))
    assert match.text == "CBC and a CT: result not back yet." and "r_ct" in (match.error or "")


@pytest.mark.parametrize(
    "reply",
    [
        {"orders": [{"order": 1, "ids": "r_cbc", "other": False}]},  # a string, not a list
        {"orders": []},  # the order left out
        {"orders": [{"order": 0, "ids": ["r_cbc"], "other": False}]},  # numbered from 0
    ],
    ids=["ids-not-a-list", "order-missing", "zero-based"],
)
def test_malformed_replies_are_not_back_yet(edith: Case, reply: dict[str, Any]) -> None:
    plan = plan_with(("investigation", "CBC"))
    [match] = asyncio.run(match_results(visit_with(edith, [BLOODS]), plan, matcher(reply)))
    assert match.text == "CBC: result not back yet." and match.error


def test_a_referral_typed_as_an_investigation_returns_nothing(edith: Case) -> None:
    plan = plan_with(("investigation", "Refer for colonoscopy"), ("investigation", "CBC"))
    reply = {
        "orders": [
            {"order": 1, "ids": [], "other": False, "kind": "not_a_test"},
            {"order": 2, "ids": ["r_cbc"], "other": False, "kind": "tests"},
        ]
    }
    matches = asyncio.run(match_results(visit_with(edith, [BLOODS]), plan, matcher(reply)))
    assert [m.order for m in matches] == ["CBC"]


def test_a_vague_order_is_not_processed(edith: Case) -> None:
    plan = plan_with(("investigation", "Routine bloods"))
    reply = {"orders": [{"order": 1, "ids": [], "other": False, "kind": "vague"}]}
    [match] = asyncio.run(match_results(visit_with(edith, [BLOODS]), plan, matcher(reply)))
    assert match.text == "Routine bloods: not processed by the lab (no tests named)."


class ResultModels(Models):
    """Edith's fake people, with a checker that also answers the results matcher."""

    def __init__(self, reply: dict[str, Any]) -> None:
        super().__init__()
        default = self.checker._reply

        def answer(system: str, user: str) -> str:
            if system == prompts.RESULTS_SYSTEM:
                return json.dumps(reply)
            return default(system, user)

        self.checker = FakeModel(answer)


def _run(case: Case, reply: dict[str, Any]) -> tuple[CaseLog, Scripted, ResultModels]:
    models = ResultModels(reply)
    plan = copy.deepcopy(PLAN)
    plan["actions"].append(
        {
            "type": "investigation",
            "detail": "Full blood count",
            "rationale": "x",
            "urgency": "routine",
        }
    )
    first = Scripted([SubmitPlan(plan)])
    second = Scripted([ReadRecord("gp_record"), SubmitPlan(PLAN)])
    clinicians = {1: first, 2: second}
    log = asyncio.run(run_case(case, lambda v: clinicians[v.number], models.simulators()))
    return log, second, models


def _with_results(edith: Case, results: list[OrderedTest] | None) -> Case:
    visits = [edith.visits[0].model_copy(update={"results": results}), *edith.visits[1:]]
    return edith.model_copy(update={"visits": visits})


def test_a_requested_test_is_in_the_chart_at_the_next_visit(edith: Case) -> None:
    case = _with_results(edith, [BLOODS])
    log, second, _ = _run(case, {"orders": [{"order": 1, "ids": ["r_cbc"], "other": False}]})
    assert [m.result_ids for m in log.visits[0].results] == [["r_cbc"]]
    chart = next(e.text for e in log.visits[1].events if e.kind == "read_record")
    assert "Results" in (chart or "") and "Hemoglobin 10.9 g/dL (low)." in (chart or "")
    markdown = render_case_markdown(log, display_names(case), {}, headings(case))
    assert "Tests ordered (in the chart by the next visit)" in markdown


def test_unrequested_results_never_appear(edith: Case) -> None:
    case = _with_results(edith, [BLOODS, TSH])
    log, _, _ = _run(case, {"orders": [{"order": 1, "ids": ["r_cbc"], "other": False}]})
    chart = next(e.text for e in log.visits[1].events if e.kind == "read_record") or ""
    assert "TSH 11.2" not in chart


def test_cases_without_results_are_unchanged(edith: Case) -> None:
    log, _, models = _run(edith, {"orders": []})
    assert log.visits[0].results == []
    assert not any(c[0].content == prompts.RESULTS_SYSTEM for c in models.checker.calls)
    chart = next(e.text for e in log.visits[1].events if e.kind == "read_record") or ""
    assert "Full blood count" not in chart


def test_the_last_visit_is_never_matched(edith: Case) -> None:
    visits = [*edith.visits[:-1], edith.visits[-1].model_copy(update={"results": [BLOODS]})]
    case = edith.model_copy(update={"visits": visits})
    models = ResultModels({"orders": [{"order": 1, "ids": ["r_cbc"], "other": False}]})
    plan = copy.deepcopy(PLAN)
    plan["actions"].append(
        {"type": "investigation", "detail": "CBC", "rationale": "x", "urgency": "routine"}
    )
    clinicians = {1: Scripted([SubmitPlan(PLAN)]), 2: Scripted([SubmitPlan(plan)])}
    log = asyncio.run(run_case(case, lambda v: clinicians[v.number], models.simulators()))
    assert log.visits[-1].results == []
    assert not any(c[0].content == prompts.RESULTS_SYSTEM for c in models.checker.calls)


def _written(tmp_path: Path, mutate: Any) -> list[str]:
    data = yaml.safe_load((CASES / "edith_marsh.yaml").read_text(encoding="utf-8"))
    mutate(data)
    path = tmp_path / "edith_marsh.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    [result] = validate_paths([path])
    return result.errors


def test_validator_rejects_results_on_the_last_visit(tmp_path: Path) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["visits"][-1]["results"] = [{"id": "r_x", "label": "CBC", "finding": "Normal."}]

    assert any("results on the last visit" in e for e in _written(tmp_path, mutate))


def test_validator_rejects_results_the_next_visit_cannot_read(tmp_path: Path) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["visits"][0]["results"] = [{"id": "r_x", "label": "CBC", "finding": "Normal."}]
        d["visits"][1]["records_available"] = ["care_agency_notes"]

    errors = _written(tmp_path, mutate)
    assert any("results land in gp_record, which visit 2 cannot read" in e for e in errors)


def test_validator_rejects_duplicate_result_ids(tmp_path: Path) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["visits"][0]["results"] = [
            {"id": "r_x", "label": "CBC", "finding": "Normal."},
            {"id": "r_x", "label": "TSH", "finding": "Normal."},
        ]

    assert "duplicate test result id r_x" in _written(tmp_path, mutate)


@pytest.mark.parametrize("name", ["edith_marsh.yaml", "harold_benning.yaml"])
def test_dev_cases_still_load(name: str) -> None:
    assert load_case(CASES / name).id
