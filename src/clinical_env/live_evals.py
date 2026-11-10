"""Live evals for the model judgement calls (paid; not in pytest).

`uv run python -m clinical_env.live_evals examiner|checker|checker_v2|results|grader|all`. Run
after changing the examiner, checker, results matcher or grader prompt or model. Prints each
miss; exits 1 on any miss.
`all` runs the cheap checker-role suites; name `grader` to run it (strong model, about 20
calls).
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from clinical_env import prompts
from clinical_env.case_run import CaseLog
from clinical_env.case_schema import Case, OrderedTest, Person
from clinical_env.grader import CaseScore, grade_case, load_consultation_rubric
from clinical_env.inspect_layer import role_generators
from clinical_env.plan import ActionType, Plan, PlanAction, Urgency
from clinical_env.roles import DEFAULT_CONFIG, Generate, Role, load_model_config
from clinical_env.simulators import GP, Checker, PersonSimulator, Utterance
from clinical_env.validate import load_case
from clinical_env.views import get_visit
from clinical_env.visit import match_exam, match_results

ROOT = DEFAULT_CONFIG.parents[1]


def exam_outcome(finding_ids: list[str], text: str) -> str:
    if finding_ids:
        return " ".join(sorted(finding_ids))
    if text == prompts.TOO_BROAD:
        return "too_broad"
    return "investigation" if text.startswith("Not available") else "none"


async def examiner_misses(case: Case, visit: int, items: list[Any], model: Generate) -> list[str]:
    info = get_visit(case, visit)
    results = await asyncio.gather(*(match_exam(info, i["request"], model) for i in items))
    return [
        f"{item['request']!r}: expected {item['expect']}, got {exam_outcome(ids, text)}"
        for item, (ids, text, _) in zip(items, results, strict=True)
        if exam_outcome(ids, text) != " ".join(sorted(str(item["expect"]).split()))
    ]


async def results_misses(
    case: Case,
    visit: int,
    items: list[Any],
    model: Generate,
    tests: list[Any] | None = None,
) -> list[str]:
    """Each item is one plan's investigation orders and the ids each order should match."""
    info = get_visit(case, visit).model_copy(
        update={"results": [OrderedTest.model_validate(t) for t in tests or []]}
    )

    async def one(item: dict[str, Any]) -> list[str]:
        actions = [
            PlanAction(
                type=ActionType.INVESTIGATION,
                detail=order,
                rationale="eval",
                urgency=Urgency.ROUTINE,
            )
            for order in item["orders"]
        ]
        plan = Plan(
            problems=["eval"],
            function_summary="eval",
            actions=actions,
            follow_up="eval",
            safety_netting="eval",
        )
        got = {m.order: m for m in await match_results(info, plan, model)}
        misses = []
        for order, want in zip(item["orders"], item["expect"], strict=True):
            match = got.get(order)  # absent: the matcher called it not a test (nothing back)
            ids = match.result_ids if match else []
            error = match.error if match else None
            if sorted(ids) != sorted(str(want).split()) or error:
                misses.append(f"{order!r}: expected {want or 'none'}, got {ids} {error or ''}")
        return misses

    results = await asyncio.gather(*(one(i) for i in items))
    return [m for r in results for m in r]


async def _never(messages: object) -> str:
    raise AssertionError("the checker eval never calls a simulator")


async def checker_misses(
    case: Case, visit: int, items: list[Any], model: Generate, earlier: str = ""
) -> list[str]:
    """`earlier` is what the speaker heard at earlier visits; an item may set `earlier: false`."""
    info = get_visit(case, visit)
    checker = Checker(model)
    people = {p: PersonSimulator(case, p, info, _never, checker) for p in info.present}

    async def one(item: dict[str, Any]) -> str | None:
        person = people[Person(item["speaker"])]
        said = [Utterance(GP, item["gp"], to=person.name)]
        memory = earlier if item.get("earlier", True) else ""
        flags = await checker.check(person.name, person.script, said, item["reply"], memory)
        hidden = {f.fact for f in flags if f.type == "hidden_revealed"}
        blocking = [f for f in flags if f.type != "checker_error"]
        if item["expect"] == "clean" and blocking:
            got = [f"{f.type} ({f.fact}): {f.detail}" for f in blocking]
            return f"{item['gp']!r}: expected clean, got {got}"
        if item["expect"] == "hidden_revealed" and item["fact"] not in hidden:
            return f"{item['gp']!r}: expected hidden_revealed {item['fact']}, got {flags}"
        if item["expect"] in ("over_cooperative", "invented_fact") and not any(
            f.type == item["expect"] for f in flags
        ):
            return f"{item['gp']!r}: expected {item['expect']}, got {flags}"
        return None

    results = await asyncio.gather(*(one(item) for item in items))
    return [r for r in results if r]


def _variant(log: CaseLog, item: dict[str, Any]) -> CaseLog:
    """The fixture run with its first visit's plan changed as the eval item says."""
    visit = log.visits[0]
    assert visit.plan is not None
    plan = visit.plan.model_dump(mode="json")
    if "plan" in item:
        plan = item["plan"]
    word = str(item.get("drop_actions", "")).lower()
    if word:
        plan["actions"] = [a for a in plan["actions"] if word not in a["detail"].lower()]
    word = str(item.get("drop_discrepancies", "")).lower()
    if word:
        plan["discrepancies"] = [
            d
            for d in plan["discrepancies"]
            if word not in (d["description"] + d["resolution"]).lower()
        ]
    plan["actions"] = [*plan["actions"], *item.get("add_actions", [])]
    changed = visit.model_copy(update={"plan": Plan.model_validate(plan)})
    return log.model_copy(update={"visits": [changed]})


def grade_misses(score: CaseScore, expect: dict[str, Any]) -> list[str]:
    verdicts = {v.id: v for visit in score.visits for v in visit.verdicts}
    penalties = [p.type for visit in score.visits for p in visit.penalties]
    misses = []
    for item_id, met in (expect.get("met") or {}).items():
        got = verdicts[item_id].met
        if got is not met:
            misses.append(f"{item_id}: expected {met}, got {got} ({verdicts[item_id].reason})")
    for kind, least in (expect.get("penalties") or {}).items():
        if penalties.count(kind) < least:
            misses.append(f"expected at least {least} {kind}, got {penalties}")
    for kind in expect.get("no_penalties") or []:
        if kind in penalties:
            misses.append(f"expected no {kind}, got {penalties}")
    errors = [e for visit in score.visits for e in visit.errors]
    return misses + [f"grader error: {e}" for e in errors]


async def grader_misses(case: Case, spec: dict[str, Any], model: Generate) -> list[str]:
    log = CaseLog.model_validate_json((ROOT / spec["fixture"]).read_text(encoding="utf-8"))
    consultation = load_consultation_rubric()

    async def one(item: dict[str, Any]) -> list[str]:
        score = await grade_case(case, _variant(log, item), model, "grader", consultation)
        return [f"{item['name']}: {m}" for m in grade_misses(score, item["expect"])]

    results = await asyncio.gather(*(one(i) for i in spec["items"]))
    return [m for r in results for m in r]


SUITES: dict[str, Any] = {
    "examiner": examiner_misses,
    "checker": checker_misses,
    "checker_v2": checker_misses,
    "results": results_misses,
}
CHEAP = list(SUITES)


async def run(names: list[str]) -> int:
    generators = role_generators(load_model_config())
    failed = 0
    for name in names:
        spec = yaml.safe_load((ROOT / "evals" / f"{name}.yaml").read_text(encoding="utf-8"))
        case = load_case(ROOT / Path(spec["case"]))
        if name == "grader":
            misses = await grader_misses(case, spec, generators[Role.GRADER])
            items = {i["name"] for i in spec["items"]}
            wrong = {m.split(":", 1)[0] for m in misses}
            for miss in misses:
                print(f"MISS [{name}] {miss}")
            print(f"{name}: {len(items - wrong)}/{len(items)} items fully correct")
            failed += bool(misses)
            continue
        model = generators[Role.CHECKER]
        extra = {k: spec[k] for k in ("earlier", "tests") if k in spec}
        misses = await SUITES[name](case, spec["visit"], spec["items"], model, **extra)
        for miss in misses:
            print(f"MISS [{name}] {miss}")
        total = len(spec["items"])
        print(f"{name}: {total - len(misses)}/{total} correct")
        failed += bool(misses)
    return 1 if failed else 0


if __name__ == "__main__":
    load_dotenv()
    chosen = sys.argv[1:] or ["all"]
    sys.exit(asyncio.run(run(CHEAP if chosen == ["all"] else chosen)))
