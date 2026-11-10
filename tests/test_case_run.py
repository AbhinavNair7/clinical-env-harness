"""Multi-visit runs: what carries from one visit to the next, and what never does."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import pytest
from conftest import CASES, FakeModel, checker_reply
from test_views import _leaks, _secrets
from test_visit import PLAN, Scripted

from clinical_env.case_run import CaseLog, Memory, run_case
from clinical_env.case_schema import Case, Record, Visit
from clinical_env.cli import main
from clinical_env.human import HumanClinician
from clinical_env.run import headings, load_earlier
from clinical_env.transcript import render_case_markdown
from clinical_env.validate import load_case, validate_paths
from clinical_env.views import RecordEntry, display_names, record_text
from clinical_env.visit import Action, ReadRecord, Say, Simulators, SubmitPlan

VISIT_1: list[Action] = [
    Say("carer", "What have you noticed at home?"),
    Say("patient", "How are you, Edith?"),
    SubmitPlan(PLAN),
]
VISIT_2: list[Action] = [ReadRecord("gp_record"), Say("carer", "How is Mum now?"), SubmitPlan(PLAN)]


class Models:
    def __init__(self) -> None:
        self.patient = FakeModel(lambda s, u: "Oh I'm fine, love.")
        self.carer = FakeModel(lambda s, u: "SILENT" if "SILENT" in u else "She's not, doctor.")
        self.checker = FakeModel(checker_reply())

    def simulators(self) -> Simulators:
        return Simulators(self.patient, self.carer, self.checker)


def _run(
    case: Case, memory: Memory = Memory.NOTES, scripts: list[list[Action]] | None = None
) -> tuple[CaseLog, list[Scripted], Models]:
    models = Models()
    clinicians = [Scripted(list(s)) for s in (scripts or [VISIT_1, VISIT_2])]
    started: list[Scripted] = []

    def make(visit: Visit) -> Scripted:
        started.append(clinicians[visit.number - 1])
        return started[-1]

    log = asyncio.run(run_case(case, make, models.simulators(), memory=memory))
    return log, started, models


def _systems(model: FakeModel) -> list[str]:
    return [call[0].content for call in model.calls]


def test_runs_every_visit_in_order_with_a_fresh_clinician_each(edith: Case) -> None:
    log, clinicians, _ = _run(edith)
    assert [v.visit for v in log.visits] == [1, 2] and log.memory == Memory.NOTES
    first, second = clinicians
    assert first is not second
    assert first.briefing.startswith("Visit 1:") and second.briefing.startswith("Visit 2:")
    assert "notes from earlier visits" not in first.briefing


def test_notes_carry_the_earlier_plan_but_not_the_transcript(edith: Case) -> None:
    _, (_, second), _ = _run(edith)
    assert "Your notes from earlier visits:" in second.briefing
    assert "Visit 1, home visit, Thursday 5 November 2026 (14 days ago)" in second.briefing
    assert "Stop furosemide; ask pharmacy to remove it from the dosette" in second.briefing
    assert "Why: Postural drop, no heart failure" in second.briefing
    assert "What have you noticed at home?" not in second.briefing
    assert "She's not, doctor." not in second.briefing


def test_transcripts_memory_carries_the_earlier_consultation(edith: Case) -> None:
    _, (_, second), _ = _run(edith, Memory.TRANSCRIPTS)
    assert "Your earlier consultations with this patient:" in second.briefing
    assert "You (to Janet Price): What have you noticed at home?" in second.briefing
    assert "Janet Price: She's not, doctor." in second.briefing
    assert "Your plan:" in second.briefing


def test_no_memory_sees_each_visit_cold(edith: Case) -> None:
    _, (_, second), _ = _run(edith, Memory.NONE)
    assert second.briefing.splitlines()[-1].startswith("Records you can read:")
    assert "earlier" not in second.briefing.lower()
    assert "GP (you)" not in second.results[0]  # no GP record entry either


def test_visit_two_gp_record_holds_the_visit_one_entry_in_date_order(edith: Case) -> None:
    _, (first, second), _ = _run(edith, scripts=[[ReadRecord("gp_record"), *VISIT_1], VISIT_2])
    assert "GP (you)" not in first.results[0]
    record = second.results[0]
    lines = record.splitlines()
    entry = next(i for i, line in enumerate(lines) if "GP (you)" in line)
    assert lines[entry].lstrip().startswith("05 Nov 2026  GP (you)")
    flat = " ".join(record.split())
    assert "Home visit. Problems: Falls with postural hypotension." in flat
    assert "Plan: Stop furosemide; ask pharmacy to remove it from the dosette." in flat
    assert "Follow-up: Phone in one week." in flat
    assert "22 Oct 2026  Admin" in lines[entry + 1 + _wrapped(lines, entry)]


def _wrapped(lines: list[str], entry: int) -> int:
    """Continuation lines of a wrapped entry start with spaces only, no date."""
    count = 0
    while not lines[entry + 1 + count].lstrip()[:2].isdigit():
        count += 1
    return count


def test_an_entry_goes_at_the_end_of_a_record_without_a_document(edith: Case) -> None:
    plain = edith.model_copy(update={"documents": {}})
    entry = RecordEntry(day=0, author="GP (you)", text="Home visit. Plan: stop furosemide.")
    text = record_text(plain, Record.GP_RECORD, 2, (entry,))
    assert text.splitlines()[-1] == "- 05 Nov 2026 GP (you): Home visit. Plan: stop furosemide."
    assert "GP (you)" not in record_text(plain, Record.GP_RECORD, 1, (entry,))  # not yet written


def test_people_remember_only_the_visits_they_were_at(edith: Case) -> None:
    _, _, models = _run(edith)
    visit_two = [s for s in _systems(models.carer) if "telephone consultation" in s]
    assert visit_two, "Janet was called at visit 2"
    memory = visit_two[0]
    assert "Earlier consultations you were at." in memory
    assert "Visit 1, home visit, Thursday 5 November 2026 (14 days ago):" in memory
    assert "GP (to Janet Price): What have you noticed at home?" in memory
    assert "Edith Marsh: Oh I'm fine, love." in memory  # she heard her mother's answer too
    # Visit-1 prompts are unchanged from M1: nothing to remember yet.
    assert not any("Earlier consultations" in s for s in _systems(models.patient))
    visit_one = [s for s in _systems(models.carer) if "home visit" in s.split("\n")[0]]
    assert visit_one and not any("Earlier consultations" in s for s in visit_one)


def test_checker_knows_what_was_said_at_earlier_visits(edith: Case) -> None:
    _, _, models = _run(edith)
    turns = [call[-1].content for call in models.checker.calls]
    later = [t for t in turns if "How is Mum now?" in t]
    assert later and "Earlier consultations the speaker was at" in later[0]
    assert "What have you noticed at home?" in later[0]
    assert not any("Earlier consultations" in t for t in turns if "How is Mum now?" not in t)


@pytest.mark.parametrize("memory", list(Memory))
def test_visit_two_clinician_never_sees_hidden_text(edith: Case, memory: Memory) -> None:
    _, (_, second), _ = _run(edith, memory)
    seen = "\n".join([second.briefing, *second.results])
    allowed = {f"gp_record {f.id}" for f in edith.views["gp_record"] if f.applies_to(2)}
    allowed |= {f"carer {f.id}" for f in edith.views["carer"]}  # Janet may say her own lines
    assert set(_leaks(seen, _secrets(edith))) <= allowed
    for event in edith.visits[1].events_since_last:
        assert " ".join(event.split()).lower() not in " ".join(seen.split()).lower()


def test_a_later_visit_runs_alone_from_saved_earlier_visits(edith: Case) -> None:
    saved, _, _ = _run(edith)
    models = Models()
    clinician = Scripted(list(VISIT_2))
    log = asyncio.run(
        run_case(
            edith, lambda _: clinician, models.simulators(), visits=[2], earlier=saved.visits[:1]
        )
    )
    assert [v.visit for v in log.visits] == [2]
    assert "Your notes from earlier visits:" in clinician.briefing


def test_case_transcript_shows_both_visits_in_order(edith: Case) -> None:
    log, _, _ = _run(edith)
    text = render_case_markdown(log, display_names(edith), {"Run": "t"}, headings(edith))
    order = [
        "# edith_marsh",
        "- **Clinician memory:** notes",
        "## Visit 1, home visit, Thursday 5 November 2026",
        "### What the GP was told",
        "### Plan",
        "## Visit 2, telephone consultation, Thursday 19 November 2026",
        "Your notes from earlier visits:",
        "**GP → Janet Price:** How is Mum now?",
    ]
    positions = [text.index(item) for item in order]
    assert positions == sorted(positions)


def test_human_clinician_plays_every_visit(edith: Case) -> None:
    plan_lines = [
        *["Falls", ""],
        "Stick indoors",
        "",
        "medication_change | Stop furosemide | Postural drop | same_day",
        "",
        "",
        "One week",
        "999 if hurt",
    ]
    lines = iter(
        ["c What have you seen?", "plan", *plan_lines, "c How is she now?", "plan", *plan_lines]
    )
    shown: list[str] = []
    human = HumanClinician(read=lambda prompt: next(lines), write=shown.append)
    log = asyncio.run(run_case(edith, lambda _: human, Models().simulators()))
    assert [v.ended for v in log.visits] == ["plan", "plan"]
    starts = [s for s in shown if s.startswith("=" * 72)]
    assert len(starts) == 2
    assert "Visit 2:" in starts[1] and "Your notes from earlier visits:" in starts[1]
    assert "- medication_change (same_day): Stop furosemide. Why: Postural drop" in starts[1]


def _saved(tmp_path: Path, case_id: str = "edith_marsh") -> Path:
    path = tmp_path / f"{case_id}.json"
    path.write_text(CaseLog(case_id=case_id, memory=Memory.NOTES).model_dump_json())
    return path


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (["--from", "RUN"], "--from needs --visit"),
        (["--visit", "3"], "has no visit 3"),
        (["--visit", "2", "--from", "OTHER"], "is a run of someone_else"),
        (["--visit", "2", "--from", "MISSING"], "--from:"),
    ],
)
def test_cli_run_checks_visit_and_from(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], args: list[str], message: str
) -> None:
    paths: dict[str, Any] = {
        "RUN": _saved(tmp_path),
        "OTHER": _saved(tmp_path, "someone_else"),
        "MISSING": tmp_path / "nope.json",
    }
    argv = ["run", str(CASES / "edith_marsh.yaml"), *[str(paths.get(a, a)) for a in args]]
    assert main(argv) == 1
    assert message in capsys.readouterr().out


ENTRY = RecordEntry(day=0, author="GP (you)", text="Home visit. Plan: stop furosemide.")


@pytest.mark.parametrize("name", ["edith_marsh.yaml", "edith_marsh_twin.yaml"])
def test_entry_goes_under_consultations_in_base_and_twin(name: str) -> None:
    case = load_case(CASES / name)
    lines = record_text(case, Record.GP_RECORD, 2, (ENTRY,)).splitlines()
    heading = lines.index("CONSULTATIONS (most recent first)")
    entry = next(i for i, line in enumerate(lines) if "GP (you)" in line)
    assert entry == heading + 1  # visit 1 is newer than every earlier consultation
    assert "{entries}" not in "\n".join(lines)
    assert "{entries}" not in record_text(case, Record.GP_RECORD, 1)


def test_older_entries_go_below_newer_lines_and_end_the_section(edith: Case) -> None:
    late = RecordEntry(day=-700, author="GP (you)", text="Oldest consultation of all.")
    lines = record_text(edith, Record.GP_RECORD, 2, (ENTRY, late)).splitlines()
    oldest = next(i for i, line in enumerate(lines) if "Oldest consultation" in line)
    assert "Annual hypertension review" in lines[oldest - 1]  # day -610, the last line
    assert oldest == len(lines) - 1


def test_validator_allows_one_entries_marker_in_the_gp_record_only(tmp_path: Path) -> None:
    text = (CASES / "edith_marsh.yaml").read_text()
    bad = text.replace("  pharmacy_record: |\n", "  pharmacy_record: |\n    {entries}\n")
    path = tmp_path / "edith_marsh.yaml"
    path.write_text(bad)
    [result] = validate_paths([path])
    assert any("{entries} goes on one line of the gp_record only" in e for e in result.errors)


def test_from_must_hold_every_earlier_visit(edith: Case, tmp_path: Path) -> None:
    path = _saved(tmp_path)  # a saved run with no visits
    with pytest.raises(ValueError, match="has no run of visit 1"):
        load_earlier(path, edith, 2)
    assert load_earlier(path, edith, 1) == []


def test_old_human_logs_are_marked_human_and_model_runs_default_to_model() -> None:
    from clinical_env.case_run import CaseLog, Memory

    assert CaseLog(case_id="x", memory=Memory.NOTES, clinician="human").run_type == "human"
    model = CaseLog(case_id="x", memory=Memory.NOTES, clinician="openai/gpt-6-astra")
    assert model.run_type == "model" and model.participant is None
