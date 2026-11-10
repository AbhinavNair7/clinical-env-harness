"""Command line: `clinical-env validate ...`, `clinical-env run <case.yaml>` (all visits;
`--visit N` runs one, with earlier visits taken from `--from` a saved case log) and
`clinical-env grade <case.yaml> <run.json>...`; `clinical-env sources pull|check` for
case-report sources (docs/case-sourcing.md)."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from clinical_env.roles import DEFAULT_CONFIG, Role, load_model_config
from clinical_env.validate import CaseError, load_case, validate_paths

if TYPE_CHECKING:
    from inspect_ai.model import ModelUsage

    from clinical_env.case_run import Participant


def _validate(paths: list[Path]) -> int:
    results = validate_paths(paths)
    if not results:
        print("no case files found")
        return 1
    for result in results:
        if result.ok:
            print(f"OK   {result.path} ({result.case_id})")
        else:
            print(f"FAIL {result.path}")
            for error in result.errors:
                print(f"  - {error}")
    failed = sum(not r.ok for r in results)
    print(f"{len(results) - failed} valid, {failed} invalid")
    return 1 if failed else 0


def _run(args: argparse.Namespace) -> int:
    # Imported here so `validate` stays fast and needs no model provider.
    from dotenv import load_dotenv

    from clinical_env.case_run import Memory
    from clinical_env.inspect_layer import role_models
    from clinical_env.run import load_earlier, run_human_case, run_model_case, save, timestamp

    try:
        case = load_case(args.case)
    except CaseError as exc:
        print(exc)
        return 1
    numbers = sorted(v.number for v in case.visits)
    if args.visit is not None and args.visit not in numbers:
        print(f"{case.id} has no visit {args.visit}")
        return 1
    if args.epochs < 1:
        print("--epochs must be at least 1")
        return 1
    if args.earlier is not None:
        if args.visit is None:
            print("--from needs --visit: it supplies the visits before that one")
            return 1
        try:
            load_earlier(args.earlier, case, args.visit)
        except (OSError, ValueError) as exc:
            print(f"--from: {exc}")
            return 1
    elif args.visit is not None and args.visit != numbers[0]:
        print(f"note: visit {args.visit} without --from runs with no earlier visits to remember")
    harness = ""
    if args.harness is not None:
        if args.clinician == "human":
            print("--harness is for a model clinician only")
            return 1
        try:
            harness = args.harness.read_text(encoding="utf-8").strip()
        except OSError as exc:
            print(f"--harness: {exc}")
            return 1
        if not harness:
            print(f"--harness: {args.harness} is empty")
            return 1
    memory = Memory(args.memory)
    run = {"memory": memory, "visit": args.visit, "earlier_path": args.earlier}
    config = load_model_config(args.config)
    load_dotenv()  # API keys live in .env (never committed); the environment wins if both set
    sims = ", ".join(f"{r.value} {config.roles[r].model}" for r in (Role.PATIENT, Role.CARER))
    header = {"Simulators": sims, "Checker": config.roles[Role.CHECKER].model}
    if args.earlier is not None:
        header["Earlier visits from"] = str(args.earlier)
    if args.harness is not None:
        header["Harness"] = str(args.harness)
    visits = f"_v{args.visit}" if args.visit is not None else ""
    stem = f"{case.id}{visits}_{timestamp()}"

    if args.clinician == "human":
        try:
            participant = _participant(args)
        except ValueError as exc:
            print(exc)
            return 1
        log = run_human_case(args.case, config, **run)
        log.clinician = "human"
        log.run_type = "human"
        log.participant = participant
        who = f"human ({participant.id}, {participant.role}, {participant.grade})"
        path = save(log, case, args.out, {"Clinician": who, **header}, stem)
        print(f"\nTranscript: {path}")
        return 0

    eval_log, logs = run_model_case(
        args.case,
        role_models(config),
        epochs=args.epochs,
        log_dir=args.log_dir,
        harness=harness,
        **run,
    )
    usage = {
        role: f"{u.input_tokens + (u.input_tokens_cache_read or 0)} in "
        f"({u.input_tokens_cache_read or 0} cached) / {u.output_tokens} out"
        for role, u in (eval_log.stats.role_usage or {}).items()
    }
    header = {
        "Clinician": config.roles[Role.CLINICIAN].model,
        **header,
        "Inspect log": eval_log.location,
        "Tokens (all epochs)": "; ".join(f"{r}: {u}" for r, u in usage.items()) or "n/a",
    }
    for epoch, log in enumerate(logs, start=1):
        log.clinician = config.roles[Role.CLINICIAN].model
        path = save(log, case, args.out, header, f"{stem}_run{epoch}")
        print(f"Transcript: {path}")
    print(f"Inspect log: {eval_log.location} (open with: uv run inspect view)")
    return 0


def _participant(args: argparse.Namespace) -> Participant:
    """The human run's participant, or ValueError saying what is missing."""
    from pydantic import ValidationError

    from clinical_env.case_run import Participant

    missing = [f"--{n}" for n in ("participant", "role", "grade") if not getattr(args, n)]
    if missing:
        raise ValueError(f"a human run needs {', '.join(missing)} (an anonymised ID, never a name)")
    if not args.consent:
        raise ValueError("a human run is saved only with --consent (the participant agreed)")
    try:
        return Participant(id=args.participant, role=args.role, grade=args.grade, consent=True)
    except ValidationError as exc:
        raise ValueError(f"--participant: {exc.errors()[0]['msg']}") from exc


def _grade(args: argparse.Namespace) -> int:
    import asyncio

    from dotenv import load_dotenv
    from inspect_ai.model import get_model

    from clinical_env.case_run import CaseLog
    from clinical_env.grader import (
        GradeReport,
        agreement,
        grade_case,
        load_consultation_rubric,
        primary_judge,
    )
    from clinical_env.inspect_layer import generate_config, inspect_generate
    from clinical_env.scorecard import render_scorecard

    try:
        case = load_case(args.case)
    except CaseError as exc:
        print(exc)
        return 1
    logs = {}
    for path in args.runs:
        try:
            log = CaseLog.model_validate_json(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"{path}: not a case log: {exc}")
            return 1
        if log.case_id != case.id:
            print(f"{path} is a run of {log.case_id}, not {case.id}")
            return 1
        logs[path] = log
    earlier = []
    if args.earlier is not None:
        try:
            earlier = CaseLog.model_validate_json(args.earlier.read_text(encoding="utf-8")).visits
        except (OSError, ValueError) as exc:
            print(f"--from: not a case log: {exc}")
            return 1
    config = load_model_config(args.config)
    spec = config.roles[Role.GRADER]
    names = list(dict.fromkeys(args.judge or [spec.model]))
    load_dotenv()
    usage: dict[str, list[ModelUsage]] = {name: [] for name in names}
    judges = {
        name: inspect_generate(
            get_model(name, config=generate_config(spec.model_copy(update={"model": name}))),
            usage[name],
        )
        for name in names
    }
    consultation = load_consultation_rubric()

    def write(report: GradeReport) -> None:
        stem = Path(report.run).with_suffix("")
        Path(f"{stem}.grade.json").write_text(report.model_dump_json(indent=2), encoding="utf-8")
        Path(f"{stem}.grade.md").write_text(render_scorecard(report), encoding="utf-8")
        main_score = next(s for s in report.scores if s.judge == report.primary)
        score = "n/a" if main_score.score is None else f"{main_score.score:.0%}"
        misses = ", ".join(main_score.critical_misses) or "none"
        print(f"{stem}.grade.md: score {score}; critical misses: {misses}")
        if main_score.ungraded:
            print(f"  not graded: {', '.join(main_score.ungraded)}")

    async def grade_all() -> None:
        for path, log in logs.items():  # each report is written as soon as it is graded
            scores = await asyncio.gather(
                *(grade_case(case, log, judges[n], n, consultation, earlier) for n in names)
            )
            primary, lab = primary_judge(names, log.clinician)
            write(
                GradeReport(
                    case_id=case.id,
                    run=str(path),
                    clinician=log.clinician,
                    primary=primary,
                    primary_lab=lab,
                    scores=list(scores),
                    agreement=agreement(scores),
                )
            )

    asyncio.run(grade_all())
    for name, used in usage.items():
        tokens_in = sum(
            u.input_tokens + (u.input_tokens_cache_read or 0) + (u.input_tokens_cache_write or 0)
            for u in used
        )
        cached = sum(u.input_tokens_cache_read or 0 for u in used)
        tokens_out = sum(u.output_tokens for u in used)
        print(f"{name}: {len(used)} calls, {tokens_in} in ({cached} cached) / {tokens_out} out")
    return 0


def _sources(args: argparse.Namespace) -> int:
    from clinical_env.sourcing import commands
    from clinical_env.sourcing.europepmc import DEFAULT_QUERY, Client, FetchError

    if args.sources_command == "mimic":
        from clinical_env.sourcing import mimic_patterns

        return mimic_patterns.main(args.root)
    if args.sources_command == "pull":
        client = Client(cache_dir=args.out / "fulltext")
        return commands.pull(client, args.query or DEFAULT_QUERY, args.limit, args.out)
    client = Client(cache_dir=args.sources / "fulltext")
    try:
        return commands.check(client, args.case, args.sources / "provenance")
    except FetchError as exc:  # no network or Europe PMC down: say so, not a traceback
        print(f"FAIL: could not reach Europe PMC ({exc})")
        return 2


def _usage_line(name: str, used: Sequence[ModelUsage]) -> str:
    tokens_in = sum(
        u.input_tokens + (u.input_tokens_cache_read or 0) + (u.input_tokens_cache_write or 0)
        for u in used
    )
    tokens_out = sum(u.output_tokens for u in used)
    return f"{name}: {len(used)} calls, {tokens_in} in / {tokens_out} out"


def _review_run(args: argparse.Namespace) -> int:
    import asyncio

    from dotenv import load_dotenv
    from inspect_ai.model import get_model

    from clinical_env.inspect_layer import generate_config, inspect_generate
    from clinical_env.review_task import load_review_case, run_review
    from clinical_env.run import timestamp

    if args.epochs < 1:
        print("--epochs must be at least 1")
        return 1
    try:
        cases = [load_review_case(path) for path in args.cases]
    except (OSError, ValueError) as exc:
        print(exc)
        return 1
    ids = [case.id for case, _ in cases]
    if len(ids) != len(set(ids)):
        print(f"two case files share an id: {', '.join(sorted(ids))}")
        return 1
    spec = load_model_config(args.config).roles[Role.CLINICIAN]
    print(f"{len(cases) * args.epochs} calls to {spec.model} ({len(cases)} cases)")
    load_dotenv()
    usage: list[ModelUsage] = []
    generate = inspect_generate(get_model(spec.model, config=generate_config(spec)), usage)
    out = args.out / timestamp()
    out.mkdir(parents=True, exist_ok=True)

    async def run_all() -> int:
        failed = 0
        for case, sha in cases:  # cases in turn, epochs in parallel; each written when done
            for run in await run_review(case, sha, generate, spec.model, args.epochs):
                path = out / f"{run.case_id}.e{run.epoch:02d}.json"
                path.write_text(run.model_dump_json(indent=2), encoding="utf-8")
                failed += run.error is not None
                print(f"{path}{'  ERROR ' + run.error if run.error else ''}")
        return failed

    failed = asyncio.run(run_all())
    print(_usage_line(spec.model, usage))
    return 1 if failed else 0


def _review_grade(args: argparse.Namespace) -> int:
    import asyncio

    from dotenv import load_dotenv
    from inspect_ai.model import get_model

    from clinical_env.inspect_layer import generate_config, inspect_generate
    from clinical_env.review_task import (
        ReviewGrade,
        ReviewRun,
        grade_review,
        load_review_case,
        summary_table,
    )

    try:
        loaded = [load_review_case(path) for path in args.cases]
        runs = {p: ReviewRun.model_validate_json(p.read_text(encoding="utf-8")) for p in args.runs}
    except (OSError, ValueError) as exc:
        print(exc)
        return 1
    cases = {case.id: (case, sha) for case, sha in loaded}
    if len(cases) != len(loaded):
        print("two case files share an id")
        return 1
    for path, run in runs.items():
        if run.case_id not in cases:
            print(f"{path}: no case file given for {run.case_id}")
            return 1
        if cases[run.case_id][1] != run.case_sha256:
            print(f"{path}: case file {run.case_id} has changed since this run")
            return 1
    spec = load_model_config(args.config).roles[Role.GRADER]
    load_dotenv()
    usage: list[ModelUsage] = []
    judge = inspect_generate(get_model(spec.model, config=generate_config(spec)), usage)
    gate = asyncio.Semaphore(4)

    async def one(path: Path, run: ReviewRun) -> ReviewGrade:
        async with gate:  # a failed run or judge call comes back ungraded, never dropped
            grade = await grade_review(cases[run.case_id][0], run, judge, spec.model)
        path.with_suffix(".grade.json").write_text(grade.model_dump_json(indent=2), "utf-8")
        if grade.error:
            print(f"{path}: ungraded, {grade.error}")
        return grade

    async def grade_all() -> list[ReviewGrade]:
        return list(await asyncio.gather(*(one(p, r) for p, r in runs.items())))

    grades = asyncio.run(grade_all())
    print(summary_table(grades))
    print(_usage_line(spec.model, usage))
    return 1 if any(g.error for g in grades) else 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="clinical-env")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="check case files against the schema")
    validate.add_argument("paths", nargs="+", type=Path, help="case YAML files or directories")

    run = commands.add_parser("run", help="run a case, every visit in order")
    run.add_argument("case", type=Path, help="case YAML file")
    run.add_argument("--visit", type=int, default=None, help="run only this visit (development)")
    run.add_argument(
        "--from",
        dest="earlier",
        type=Path,
        default=None,
        help="saved case log (.json) whose earlier visits --visit carries over",
    )
    run.add_argument(
        "--memory",
        choices=["notes", "transcripts", "none"],
        default="notes",
        help="what the clinician carries between visits (default: its own plans as notes)",
    )
    run.add_argument("--clinician", choices=["model", "human"], default="model")
    human = run.add_argument_group("human runs (--clinician human)")
    human.add_argument("--participant", help="anonymised participant ID, e.g. P01; never a name")
    human.add_argument("--role", help="e.g. GP, GP trainee")
    human.add_argument("--grade", help="e.g. GPST1, consultant")
    human.add_argument("--consent", action="store_true", help="the participant agreed")
    run.add_argument("--epochs", type=int, default=1, help="runs of the case (model only)")
    run.add_argument(
        "--harness",
        type=Path,
        default=None,
        help="text file appended to the clinician's system prompt (model only; harness tests)",
    )
    run.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    run.add_argument("--out", type=Path, default=Path("runs"), help="transcript folder")
    run.add_argument("--log-dir", type=Path, default=Path("logs"), help="Inspect log folder")

    grade = commands.add_parser("grade", help="grade saved case runs (writes .grade.md/.json)")
    grade.add_argument("case", type=Path, help="case YAML file the runs are of")
    grade.add_argument("runs", nargs="+", type=Path, help="case logs (.json) from `run`")
    grade.add_argument(
        "--judge",
        action="append",
        default=None,
        help="judge model id (repeat for a second lab); default: the config's grader",
    )
    grade.add_argument(
        "--from",
        dest="earlier",
        type=Path,
        default=None,
        help="case log holding the earlier visits of a `run --visit N` log (context for the judge)",
    )
    grade.add_argument("--config", type=Path, default=DEFAULT_CONFIG)

    sources = commands.add_parser("sources", help="case-report sources (docs/case-sourcing.md)")
    source_commands = sources.add_subparsers(dest="sources_command", required=True)
    pull = source_commands.add_parser("pull", help="search Europe PMC and log licence decisions")
    pull.add_argument("--query", default=None, help="Europe PMC query (default: built in)")
    pull.add_argument("--limit", type=int, default=150)
    pull.add_argument("--out", type=Path, default=Path("sources"))
    check = source_commands.add_parser(
        "check", help="licence, overlap and identifiability checks for a drafted case"
    )
    check.add_argument("case", type=Path, help="case YAML file")
    check.add_argument("--sources", type=Path, default=Path("sources"))
    mimic = source_commands.add_parser(
        "mimic", help="print aggregate record patterns from the MIMIC demo data (ODbL)"
    )
    mimic.add_argument("root", type=Path, help="folder holding the unzipped demo datasets")

    review = commands.add_parser("review", help="document-review task (records in, plan out)")
    review_commands = review.add_subparsers(dest="review_command", required=True)
    review_run = review_commands.add_parser("run", help="run review cases with the clinician")
    review_run.add_argument("cases", nargs="+", type=Path, help="review case YAML files")
    review_run.add_argument("--epochs", type=int, default=1, help="runs per case")
    review_run.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    review_run.add_argument("--out", type=Path, default=Path("runs") / "review")
    review_grade = review_commands.add_parser("grade", help="grade review runs, print criticals")
    review_grade.add_argument("--case", dest="cases", action="append", type=Path, required=True)
    review_grade.add_argument("runs", nargs="+", type=Path, help="run files from `review run`")
    review_grade.add_argument("--config", type=Path, default=DEFAULT_CONFIG)

    args = parser.parse_args(argv)
    if args.command == "review":
        return _review_run(args) if args.review_command == "run" else _review_grade(args)
    if args.command == "validate":
        return _validate(args.paths)
    if args.command == "sources":
        return _sources(args)
    if args.command == "grade":
        return _grade(args)
    return _run(args)
