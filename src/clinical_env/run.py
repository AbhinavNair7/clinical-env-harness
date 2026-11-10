"""Run a case: under Inspect for a model clinician (logs open in `inspect view`), or at the
terminal for a human clinician. Both write the same JSON case log and Markdown transcript.

One Inspect sample is one case run, all its visits in order; the log keeps each visit apart
so the grader can score per visit and per case.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.log import EvalLog, transcript
from inspect_ai.model import ChatMessage, Model, get_model
from inspect_ai.solver import Generate as InspectGenerate
from inspect_ai.solver import Solver, TaskState, solver

from clinical_env.case_run import CaseLog, Memory, clinician_notes, run_case
from clinical_env.case_schema import Case, Visit
from clinical_env.human import HumanClinician
from clinical_env.inspect_layer import inspect_generate, role_generators
from clinical_env.llm_clinician import LLMClinician, clinician_tools
from clinical_env.roles import ModelConfig, Role
from clinical_env.transcript import render_case_markdown
from clinical_env.validate import load_case
from clinical_env.views import clinician_briefing, display_names, visit_heading
from clinical_env.visit import Clinician, Simulators, VisitLog

STORE_KEY = "case_log"


def _role(name: Role) -> Model:
    return get_model(role=name.value, required=True)


def load_earlier(path: Path, case: Case, before: int) -> list[VisitLog]:
    """Visits before `before` from a saved case log, to run one later visit on its own."""
    log = CaseLog.model_validate_json(path.read_text(encoding="utf-8"))
    if log.case_id != case.id:
        raise ValueError(f"{path} is a run of {log.case_id}, not {case.id}")
    earlier = [v for v in log.visits if v.visit < before]
    missing = sorted(
        {v.number for v in case.visits if v.number < before} - {v.visit for v in earlier}
    )
    if missing:
        raise ValueError(f"{path} has no run of visit {', '.join(map(str, missing))}")
    return earlier


def headings(case: Case) -> dict[int, str]:
    return {v.number: visit_heading(case, v) for v in case.visits}


@solver
def case_solver(
    case_path: str, memory: str, visit: int | None, earlier_path: str | None, harness: str = ""
) -> Solver:
    async def solve(state: TaskState, generate: InspectGenerate) -> TaskState:
        case = load_case(Path(case_path))
        earlier = load_earlier(Path(earlier_path), case, visit) if earlier_path and visit else []
        clinicians: list[LLMClinician] = []

        def make(info: Visit) -> Clinician:
            clinician = LLMClinician(
                _role(Role.CLINICIAN), clinician_tools(info.present, info.records_available)
            )
            clinicians.append(clinician)
            return clinician

        simulators = Simulators(
            patient=inspect_generate(_role(Role.PATIENT)),
            carer=inspect_generate(_role(Role.CARER)),
            checker=inspect_generate(_role(Role.CHECKER)),
        )
        log = await run_case(
            case,
            make,
            simulators,
            memory=Memory(memory),
            visits=[visit] if visit else None,
            earlier=earlier,
            harness=harness,
        )
        # Each visit is a fresh clinician context; the viewer shows them one after another.
        messages: list[ChatMessage] = []
        for clinician in clinicians:
            clinician.close()
            messages += clinician.messages
        state.messages = messages
        state.store.set(STORE_KEY, log.model_dump(mode="json"))
        transcript().info(
            render_case_markdown(log, display_names(case), {}, headings(case)), source="case"
        )
        state.completed = True
        return state

    return solve


@task
def case_task(
    case_path: str,
    memory: str = Memory.NOTES.value,
    visit: int | None = None,
    earlier_path: str | None = None,
    harness: str = "",
) -> Task:
    case = load_case(Path(case_path))
    first = visit or min(v.number for v in case.visits)
    earlier = load_earlier(Path(earlier_path), case, first) if earlier_path else []
    sample = Sample(
        id=case.id if visit is None else f"{case.id}_v{visit}",
        input=clinician_briefing(
            case, first, clinician_notes(case, first, earlier, Memory(memory))
        ),
        metadata={"case_id": case.id, "visit": visit, "memory": memory, "harness": harness},
    )
    return Task(
        dataset=[sample],
        solver=case_solver(case_path, memory, visit, earlier_path, harness),
        name="case",
    )


def logs_from_eval(log: EvalLog) -> list[CaseLog]:
    if log.status != "success":
        raise RuntimeError(f"Inspect run {log.status}: {log.error.message if log.error else ''}")
    return [CaseLog.model_validate(s.store[STORE_KEY]) for s in log.samples or []]


def run_model_case(
    case_path: Path,
    models: dict[str, Model],
    *,
    epochs: int,
    log_dir: Path,
    memory: Memory = Memory.NOTES,
    visit: int | None = None,
    earlier_path: Path | None = None,
    harness: str = "",
) -> tuple[EvalLog, list[CaseLog]]:
    """`models` maps each role name to its model (see `inspect_layer.role_models`)."""
    [log] = inspect_eval(
        case_task(
            str(case_path),
            memory.value,
            visit,
            str(earlier_path) if earlier_path else None,
            harness,
        ),
        model=models[Role.CLINICIAN.value],
        model_roles=dict(models),
        epochs=epochs,
        log_dir=str(log_dir),
        display="plain",
    )
    return log, logs_from_eval(log)


def run_human_case(
    case_path: Path,
    config: ModelConfig,
    *,
    memory: Memory = Memory.NOTES,
    visit: int | None = None,
    earlier_path: Path | None = None,
    clinician: Clinician | None = None,
) -> CaseLog:
    case = load_case(case_path)
    earlier = load_earlier(earlier_path, case, visit) if earlier_path and visit else []
    generators = role_generators(config)
    simulators = Simulators(
        patient=generators[Role.PATIENT],
        carer=generators[Role.CARER],
        checker=generators[Role.CHECKER],
    )
    human = clinician or HumanClinician()
    return asyncio.run(
        run_case(
            case,
            lambda _: human,
            simulators,
            memory=memory,
            visits=[visit] if visit else None,
            earlier=earlier,
        )
    )


def save(log: CaseLog, case: Case, out_dir: Path, header: dict[str, str], stem: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{stem}.json").write_text(log.model_dump_json(indent=2), encoding="utf-8")
    path = out_dir / f"{stem}.md"
    text = render_case_markdown(log, display_names(case), header, headings(case))
    path.write_text(text, encoding="utf-8")
    return path


def timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
