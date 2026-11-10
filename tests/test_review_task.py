"""Document-review task: case shape, what the model sees, quote-checked grading, criticals."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from conftest import FakeModel

from clinical_env.cli import main
from clinical_env.review_task import (
    ItemVerdict,
    ReviewCase,
    ReviewGrade,
    ReviewRun,
    critical_pass,
    grade_review,
    load_review_case,
    review_messages,
    run_result,
    run_review,
    summary_table,
)

# Synthetic, fictional case.
CASE: dict[str, Any] = {
    "id": "syn_base",
    "title": "Synthetic memory review",
    "pair": "syn",
    "arm": "base",
    "task": "Write the pre-review brief.",
    "documents": [
        {"title": "Referral", "text": "Family manage her money. She never handled money."},
        {"title": "Cognitive test", "text": "RUDAS 19/30."},
    ],
    "ground_truth": "SECRET-TRUTH mild cognitive impairment; finances lifelong delegated.",
    "rubric": [
        {
            "id": "baseline",
            "kind": "must_not_do",
            "description": "SECRET-RUBRIC counts the family managing money as decline",
            "critical": True,
        },
        {
            "id": "mci",
            "kind": "must_do",
            "description": "Gives mild cognitive impairment as the working diagnosis",
            "critical": True,
        },
        {"id": "b12", "kind": "must_do", "description": "Checks B12"},
    ],
    "notes": "SECRET-NOTES authoring only",
}
OUTPUT = (
    "Impression: mild cognitive impairment, probably vascular. Family help with money is "
    "lifelong and not evidence of decline. Check B12 and folate."
)


def _case(**changes: Any) -> ReviewCase:
    return ReviewCase.model_validate({**CASE, **changes})


def _run(output: str = OUTPUT) -> ReviewRun:
    return ReviewRun(
        case_id="syn_base",
        pair="syn",
        arm="base",
        case_sha256="x",
        model="m",
        epoch=1,
        started="t",
        output=output,
    )


def _judge(*replies: dict[str, Any] | str) -> FakeModel:
    queue = [r if isinstance(r, str) else json.dumps(r) for r in replies]
    return FakeModel(lambda _system, _user: queue.pop(0) if len(queue) > 1 else queue[0])


def _items(**met: tuple[bool, str]) -> dict[str, Any]:
    return {
        "items": [
            {"id": key, "reason": "r", "met": value[0], "evidence": value[1]}
            for key, value in met.items()
        ]
    }


def test_load_records_hash_and_rejects_bad_cases(tmp_path: Path) -> None:
    path = tmp_path / "syn.yaml"
    path.write_text(yaml.safe_dump(CASE))
    case, sha = load_review_case(path)
    assert case.id == "syn_base" and len(sha) == 64
    duplicate = {**CASE, "rubric": [CASE["rubric"][0], CASE["rubric"][0]]}
    with pytest.raises(ValueError, match="unique"):
        ReviewCase.model_validate(duplicate)
    with pytest.raises(ValueError, match="critical"):
        ReviewCase.model_validate({**CASE, "rubric": [CASE["rubric"][2]]})
    (tmp_path / "typo.yaml").write_text(yaml.safe_dump({**CASE, "groundtruth": "x"}))
    with pytest.raises(ValueError, match="typo.yaml"):
        load_review_case(tmp_path / "typo.yaml")
    (tmp_path / "broken.yaml").write_text("id: [unclosed\n")
    with pytest.raises(ValueError, match="broken.yaml"):
        load_review_case(tmp_path / "broken.yaml")


def test_model_under_test_sees_task_and_documents_only() -> None:
    text = "\n".join(m.content for m in review_messages(_case()))
    assert "Write the pre-review brief." in text and "RUDAS 19/30." in text
    assert "## Referral" in text
    for secret in ("SECRET-TRUTH", "SECRET-RUBRIC", "SECRET-NOTES", "Checks B12"):
        assert secret not in text


def test_run_review_records_each_epoch_and_provider_failures() -> None:
    model = FakeModel(lambda _s, _u: OUTPUT)
    runs = asyncio.run(run_review(_case(), "sha", model, "m", epochs=3))
    assert [r.epoch for r in runs] == [1, 2, 3] and all(r.output == OUTPUT for r in runs)
    assert all(r.case_sha256 == "sha" and r.arm == "base" for r in runs)

    async def broken(_messages: object) -> str:
        raise RuntimeError("provider down")

    [failed] = asyncio.run(run_review(_case(), "sha", broken, "m", epochs=1))
    assert failed.output == "" and failed.error == "RuntimeError: provider down"


def test_blank_output_is_a_failed_run_not_a_pass() -> None:
    # A blank reply has nothing to quote, so every must-not-do would otherwise pass.
    [blank] = asyncio.run(run_review(_case(), "sha", FakeModel(lambda _s, _u: "  \n"), "m", 1))
    assert blank.error == "empty output"
    judge = _judge(_items(baseline=(False, ""), mci=(False, ""), b12=(False, "")))
    grade = asyncio.run(grade_review(_case(), blank, judge, "j"))
    assert not judge.calls and grade.error == "run failed: empty output"
    assert grade.critical_pass == {"baseline": None, "mci": None}
    assert run_result(grade) == "ungraded"


def test_judge_failure_is_ungraded_not_fatal() -> None:
    async def down(_messages: object) -> str:
        raise RuntimeError("judge down")

    grade = asyncio.run(grade_review(_case(), _run(), down, "j"))
    assert grade.error == "judge failed: RuntimeError: judge down"
    assert all(v.status == "ungraded" for v in grade.verdicts)


def test_duplicate_judge_entries_are_ungraded() -> None:
    reply = _items(baseline=(False, ""), mci=(False, ""), b12=(False, ""))
    reply["items"].append({"id": "mci", "reason": "r", "met": True, "evidence": ""})
    grade = asyncio.run(grade_review(_case(), _run(), _judge(reply, reply), "j"))
    assert {v.id: v.status for v in grade.verdicts} == {
        "baseline": "not_met",
        "mci": "ungraded",
        "b12": "not_met",
    }


def test_grade_counts_quoted_verdicts_and_criticals() -> None:
    judge = _judge(
        _items(
            baseline=(False, ""),
            mci=(True, "Impression: mild cognitive impairment, probably vascular"),
            b12=(True, "check b12 and folate."),  # case and the judge's full stop are ignored
        )
    )
    grade = asyncio.run(grade_review(_case(), _run(), judge, "j"))
    assert [v.status for v in grade.verdicts] == ["not_met", "met", "met"]
    assert grade.critical_pass == {"baseline": True, "mci": True}
    assert len(judge.calls) == 1
    assert "SECRET-TRUTH" in judge.calls[0][1].content  # the judge does see the ground truth


def test_must_not_done_fails_the_critical() -> None:
    judge = _judge(
        _items(
            baseline=(True, "Family help with money is lifelong"),
            mci=(False, ""),
            b12=(False, ""),
        )
    )
    grade = asyncio.run(grade_review(_case(), _run(), judge, "j"))
    assert grade.critical_pass == {"baseline": False, "mci": False}


def test_invented_quote_is_retried_then_ungraded() -> None:
    bad = _items(
        baseline=(False, ""), mci=(True, "a diagnosis of dementia is made"), b12=(False, "")
    )
    judge = _judge(bad, bad)
    grade = asyncio.run(grade_review(_case(), _run(), judge, "j"))
    assert len(judge.calls) == 2
    assert "mci: the evidence is not an exact quote" in judge.calls[1][-1].content
    assert {v.id: v.status for v in grade.verdicts}["mci"] == "ungraded"
    assert grade.critical_pass["mci"] is None


def test_retry_fixes_missing_items_and_bad_json() -> None:
    good = _items(baseline=(False, ""), mci=(False, ""), b12=(False, ""))
    judge = _judge("not json at all", good)
    grade = asyncio.run(grade_review(_case(), _run(), judge, "j"))
    assert len(judge.calls) == 2 and "not valid JSON" in judge.calls[1][-1].content
    assert all(v.status == "not_met" for v in grade.verdicts)

    judge = _judge(_items(baseline=(False, "")), good)
    asyncio.run(grade_review(_case(), _run(), judge, "j"))
    assert "one entry for each id: b12, baseline, mci" in judge.calls[1][-1].content


def test_critical_pass_skips_non_critical_and_marks_ungraded() -> None:
    verdicts = [ItemVerdict(id="baseline", status="ungraded"), ItemVerdict(id="b12", status="met")]
    assert critical_pass(_case(), verdicts) == {"baseline": None, "mci": None}


def _grade_with(**passes: bool | None) -> ReviewGrade:
    return ReviewGrade(
        case_id="syn_base",
        pair="syn",
        arm="base",
        model="m",
        epoch=1,
        judge="j",
        verdicts=[],
        critical_pass=passes,
    )


def test_run_result_fails_on_any_failed_critical() -> None:
    assert run_result(_grade_with(baseline=True, mci=True)) == "passes"
    assert run_result(_grade_with(baseline=None, mci=False)) == "fails"
    assert run_result(_grade_with(baseline=True, mci=None)) == "ungraded"


def test_summary_table_counts_runs_and_criticals() -> None:
    grades = [
        _grade_with(baseline=True, mci=True),
        _grade_with(baseline=True, mci=False),
        _grade_with(baseline=None, mci=True),
        _grade_with(baseline=False, mci=None),
    ]
    table = summary_table(grades)
    assert "| m | syn_base (base) | 2 | 1 | 1 |" in table  # per run: fails, passes, ungraded
    assert "| m | syn_base (base) | mci | 2 of 3 | 1 |" in table
    assert "| m | syn_base (base) | baseline | 2 of 3 | 1 |" in table


def test_cli_runs_and_grades_end_to_end(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config = tmp_path / "models.yaml"
    roles = ["clinician", "patient", "carer", "checker", "grader"]
    config.write_text(yaml.safe_dump({"roles": {r: {"model": "mockllm/model"} for r in roles}}))
    case_path = tmp_path / "syn.yaml"
    case_path.write_text(yaml.safe_dump(CASE))
    out = tmp_path / "runs"
    args = ["review", "run", str(case_path), "--epochs", "2"]
    assert main([*args, "--config", str(config), "--out", str(out)]) == 0
    runs = sorted(out.glob("*/*.json"))
    assert [p.name for p in runs] == ["syn_base.e01.json", "syn_base.e02.json"]
    assert "2 calls to mockllm/model (1 cases)" in capsys.readouterr().out

    grade_args = ["review", "grade", "--case", str(case_path), *map(str, runs)]
    assert main([*grade_args, "--config", str(config)]) == 0
    printed = capsys.readouterr().out
    # The mock judge never replies with JSON, so every critical is ungraded, not guessed.
    assert "| mockllm/model | syn_base (base) | mci | 0 of 0 | 2 |" in printed
    assert "| mockllm/model | syn_base (base) | 0 | 0 | 2 |" in printed
    assert runs[0].with_suffix(".grade.json").is_file()

    # A failed run stays in the counts as ungraded and makes the command fail.
    failed = ReviewRun.model_validate_json(runs[1].read_text())
    runs[1].write_text(failed.model_copy(update={"output": "", "error": "x"}).model_dump_json())
    assert main([*grade_args, "--config", str(config)]) == 1
    printed = capsys.readouterr().out
    assert "ungraded, run failed: x" in printed
    assert "| mockllm/model | syn_base (base) | 0 | 0 | 2 |" in printed

    other = tmp_path / "copy.yaml"
    other.write_text(case_path.read_text())
    assert main(["review", "run", str(case_path), str(other), "--config", str(config)]) == 1
    assert "two case files share an id" in capsys.readouterr().out

    case_path.write_text(yaml.safe_dump({**CASE, "title": "edited after the run"}))
    assert main([*grade_args, "--config", str(config)]) == 1
    assert "has changed since this run" in capsys.readouterr().out
