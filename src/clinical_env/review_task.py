"""Document-review task: records in, impression and plan out, graded against a case rubric.

A second, smaller task beside the consultation harness (DECISIONS.md, 2026-11-09). The model
under test reads a patient's documents and writes what the case asks for (e.g. a pre-review
brief); it never sees the ground truth, rubric or notes. One judge call grades every item,
and a "met" counts only when its quote is really in the output. Plain Python behind
`Generate`, like the rest of the core.
"""

from __future__ import annotations

import asyncio
import hashlib
from collections import defaultdict
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from clinical_env import prompts
from clinical_env.grader import quote_found
from clinical_env.roles import Generate, Message
from clinical_env.simulators import parse_json_object


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ReviewDocument(_Strict):
    title: str = Field(min_length=1)
    text: str = Field(min_length=1)


class ReviewItem(_Strict):
    id: str = Field(pattern=r"^[a-z0-9_]+$")
    kind: Literal["must_do", "must_not_do"]
    description: str = Field(min_length=1)
    critical: bool = False


class ReviewCase(_Strict):
    """One case file. A pair is a base case (the default answer is wrong) and its twin (one or
    two facts changed so the default answer is right), so always deviating is not rewarded."""

    id: str = Field(pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=1)
    pair: str = Field(pattern=r"^[a-z0-9_]+$", description="shared by a base case and its twin")
    arm: Literal["base", "twin", "control"]
    task: str = Field(min_length=1, description="what the model under test is asked to write")
    documents: list[ReviewDocument] = Field(min_length=1)
    ground_truth: str = Field(min_length=1, description="judge only")
    rubric: list[ReviewItem] = Field(min_length=1)
    notes: str | None = Field(default=None, description="authoring notes; nobody sees these")

    @model_validator(mode="after")
    def _items(self) -> ReviewCase:
        ids = [item.id for item in self.rubric]
        if len(ids) != len(set(ids)):
            raise ValueError("rubric item ids must be unique")
        if not any(item.critical for item in self.rubric):
            raise ValueError("a case needs at least one critical item")
        return self


def load_review_case(path: Path) -> tuple[ReviewCase, str]:
    """The case and the sha256 of its file, so a run records exactly which version it used."""
    raw = path.read_bytes()
    try:
        case = ReviewCase.model_validate(yaml.safe_load(raw))
    except (yaml.YAMLError, ValidationError) as exc:
        raise ValueError(f"{path}: {exc}") from exc
    return case, hashlib.sha256(raw).hexdigest()


def review_messages(case: ReviewCase) -> list[Message]:
    """Everything the model under test sees: the task and the documents, nothing else."""
    documents = "\n\n".join(f"## {d.title}\n{d.text.strip()}" for d in case.documents)
    return [
        Message("system", prompts.REVIEW_SYSTEM),
        Message("user", prompts.REVIEW_TASK.format(task=case.task.strip(), documents=documents)),
    ]


class ReviewRun(BaseModel):
    case_id: str
    pair: str
    arm: str
    case_sha256: str
    model: str
    epoch: int
    started: str
    output: str
    error: str | None = None


async def run_review(
    case: ReviewCase,
    sha: str,
    generate: Generate,
    model: str,
    epochs: int,
    concurrency: int = 4,
) -> list[ReviewRun]:
    gate = asyncio.Semaphore(concurrency)

    async def one(epoch: int) -> ReviewRun:
        started = datetime.now(UTC).isoformat(timespec="seconds")
        async with gate:
            try:
                output, error = await generate(review_messages(case)), None
            except Exception as exc:  # a provider failure is recorded, not fatal to the batch
                output, error = "", f"{type(exc).__name__}: {exc}"
        if error is None and not output.strip():
            # e.g. reasoning used up the token limit, or a refusal: with nothing to quote, every
            # must-not-do would pass, so a blank reply is a failed run, never a graded one.
            error = "empty output"
        return ReviewRun(
            case_id=case.id,
            pair=case.pair,
            arm=case.arm,
            case_sha256=sha,
            model=model,
            epoch=epoch,
            started=started,
            output=output,
            error=error,
        )

    return list(await asyncio.gather(*(one(e) for e in range(1, epochs + 1))))


# --- grading ---------------------------------------------------------------------------------


Status = Literal["met", "not_met", "ungraded"]


class ItemVerdict(BaseModel):
    id: str
    status: Status
    reason: str = ""
    evidence: str = ""


class ReviewGrade(BaseModel):
    case_id: str
    pair: str
    arm: str
    model: str
    epoch: int
    judge: str
    verdicts: list[ItemVerdict]
    critical_pass: dict[str, bool | None]  # None: ungraded
    error: str | None = None  # the run or the judge failed; every item is ungraded


class _JudgeItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    reason: str = ""
    met: bool
    evidence: str = ""


class _JudgeReply(BaseModel):
    model_config = ConfigDict(extra="ignore")
    items: list[_JudgeItem]


def judge_messages(case: ReviewCase, output: str) -> list[Message]:
    documents = "\n\n".join(f"## {d.title}\n{d.text.strip()}" for d in case.documents)
    items = "\n".join(
        f"- {item.id} ({'MUST NOT' if item.kind == 'must_not_do' else 'must'}): {item.description}"
        for item in case.rubric
    )
    return [
        Message("system", prompts.REVIEW_GRADER_SYSTEM),
        Message(
            "user",
            prompts.REVIEW_GRADER_CASE.format(
                title=case.title,
                task=case.task.strip(),
                truth=case.ground_truth.strip(),
                documents=documents,
                output=output.strip() or "(no output)",
                items=items,
            ),
        ),
    ]


def _problems(reply: _JudgeReply, case: ReviewCase, output: str) -> list[str]:
    wanted = {item.id for item in case.rubric}
    got = [item.id for item in reply.items]
    problems = []
    if sorted(got) != sorted(wanted):
        problems.append(f"give exactly one entry for each id: {', '.join(sorted(wanted))}")
    for item in reply.items:
        if item.met and not quote_found(item.evidence, output):
            problems.append(f"{item.id}: the evidence is not an exact quote from the output")
    return problems


def _grade(
    case: ReviewCase,
    run: ReviewRun,
    judge_name: str,
    verdicts: list[ItemVerdict],
    error: str | None = None,
) -> ReviewGrade:
    return ReviewGrade(
        case_id=case.id,
        pair=case.pair,
        arm=case.arm,
        model=run.model,
        epoch=run.epoch,
        judge=judge_name,
        verdicts=verdicts,
        critical_pass=critical_pass(case, verdicts),
        error=error,
    )


def ungraded(case: ReviewCase, run: ReviewRun, judge_name: str, error: str) -> ReviewGrade:
    """A failed run or judge call: kept in the counts as ungraded, never dropped."""
    verdicts = [ItemVerdict(id=item.id, status="ungraded") for item in case.rubric]
    return _grade(case, run, judge_name, verdicts, error)


async def grade_review(
    case: ReviewCase, run: ReviewRun, judge: Generate, judge_name: str, retries: int = 1
) -> ReviewGrade:
    """A met (or, for a must-not-do, a done) item needs a quote found in the output; after the
    retries, an item still without one is ungraded rather than guessed."""
    if run.error is not None:
        return ungraded(case, run, judge_name, f"run failed: {run.error}")
    messages = judge_messages(case, run.output)
    reply: _JudgeReply | None = None
    for attempt in range(retries + 1):
        try:
            text = await judge(messages)
        except Exception as exc:  # one judge failure must not abort the batch
            return ungraded(case, run, judge_name, f"judge failed: {type(exc).__name__}: {exc}")
        try:
            reply = _JudgeReply.model_validate(parse_json_object(text))
        except (ValueError, ValidationError) as exc:
            problem = f"not valid JSON in the asked shape ({exc.__class__.__name__})"
            problems = [problem]
            reply = None
        else:
            problems = _problems(reply, case, run.output)
        if not problems or attempt == retries:
            break
        messages = [
            *messages,
            Message("assistant", text),
            Message("user", prompts.GRADER_RETRY.format(problem="; ".join(problems))),
        ]
    entries = reply.items if reply else []
    once = {i.id for i in entries if sum(e.id == i.id for e in entries) == 1}
    by_id = {item.id: item for item in entries if item.id in once}  # duplicates: ungraded
    verdicts = []
    for item in case.rubric:
        got = by_id.get(item.id)
        if got is None or (got.met and not quote_found(got.evidence, run.output)):
            status: Status = "ungraded"
        else:
            status = "met" if got.met else "not_met"
        verdicts.append(
            ItemVerdict(
                id=item.id,
                status=status,
                reason=got.reason if got else "",
                evidence=got.evidence if got else "",
            )
        )
    return _grade(case, run, judge_name, verdicts)


def critical_pass(case: ReviewCase, verdicts: Sequence[ItemVerdict]) -> dict[str, bool | None]:
    """Pass means a must-do was met or a must-not-do was not done."""
    status = {v.id: v.status for v in verdicts}
    result: dict[str, bool | None] = {}
    for item in case.rubric:
        if not item.critical:
            continue
        got = status.get(item.id, "ungraded")
        if got == "ungraded":
            result[item.id] = None
        else:
            result[item.id] = (got == "met") == (item.kind == "must_do")
    return result


def run_result(grade: ReviewGrade) -> Literal["fails", "passes", "ungraded"]:
    """The rule's primary measure: a run fails the case if any critical fails, passes if every
    critical passes, and is otherwise ungraded."""
    results = grade.critical_pass.values()
    if any(r is False for r in results):
        return "fails"
    return "passes" if all(r is True for r in results) else "ungraded"


def summary_table(grades: Sequence[ReviewGrade]) -> str:
    """Per run, then per critical item: the numbers the pre-registered rule uses."""
    runs: dict[tuple[str, str], list[str]] = defaultdict(list)
    for grade in grades:
        runs[(grade.model, f"{grade.case_id} ({grade.arm})")].append(run_result(grade))
    lines = ["| Model | Case | Runs failing | Passing | Ungraded |", "|---|---|---|---|---|"]
    for (model, case), results in sorted(runs.items()):
        lines.append(
            f"| {model} | {case} | {results.count('fails')} | {results.count('passes')} | "
            f"{results.count('ungraded')} |"
        )
    lines.append("")
    counts: dict[tuple[str, str, str, str], list[bool | None]] = defaultdict(list)
    for grade in grades:
        for item, passed in grade.critical_pass.items():
            counts[(grade.model, grade.pair, f"{grade.case_id} ({grade.arm})", item)].append(passed)
    lines += ["| Model | Case | Critical item | Passed | Ungraded |", "|---|---|---|---|---|"]
    for (model, _pair, case, item), passes in sorted(counts.items()):
        graded = [r for r in passes if r is not None]
        lines.append(
            f"| {model} | {case} | {item} | {sum(graded)} of {len(graded)} | "
            f"{len(passes) - len(graded)} |"
        )
    return "\n".join(lines)
