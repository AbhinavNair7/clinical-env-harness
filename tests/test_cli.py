from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from clinical_env.cli import main

CASES = Path(__file__).resolve().parents[1] / "cases" / "dev"


def test_validate_passes_on_dev_cases(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate", str(CASES)]) == 0
    out = capsys.readouterr().out
    assert "OK   " in out and "(edith_marsh_twin)" in out
    assert out.strip().endswith(f"{len(list(CASES.glob('*.yaml')))} valid, 0 invalid")


def test_validate_fails_and_lists_errors(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    bad = tmp_path / "bad_case.yaml"
    bad.write_text("id: bad_case\ntitle: x\n")
    assert main(["validate", str(bad)]) == 1
    out = capsys.readouterr().out
    assert f"FAIL {bad}" in out
    assert "  - patient: Field required" in out
    assert out.strip().endswith("0 valid, 1 invalid")


def test_same_file_twice_is_checked_once(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate", str(CASES), str(CASES / "edith_marsh.yaml")]) == 0
    n = len(list(CASES.glob("*.yaml")))
    assert capsys.readouterr().out.strip().endswith(f"{n} valid, 0 invalid")


def test_validate_empty_directory_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate", str(tmp_path)]) == 1
    assert "no case files found" in capsys.readouterr().out


def test_installed_entry_point_runs() -> None:
    result = subprocess.run(
        [
            str(Path(sys.executable).parent / "clinical-env"),
            "validate",
            str(CASES / "edith_marsh.yaml"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 valid, 0 invalid" in result.stdout


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        ([], "a human run needs --participant, --role, --grade"),
        (["--participant", "P01", "--role", "GP", "--grade", "GPST1"], "only with --consent"),
        (
            ["--participant", "Jane Doe", "--role", "GP", "--grade", "GPST1", "--consent"],
            "--participant: String should match pattern",
        ),
    ],
)
def test_human_run_needs_an_anonymised_consenting_participant(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], extra: list[str], message: str
) -> None:
    case = str(CASES / "edith_marsh.yaml")
    argv = ["run", case, "--clinician", "human", "--out", str(tmp_path), *extra]
    assert main(argv) == 1
    assert message in capsys.readouterr().out
    assert not list(tmp_path.iterdir())  # nothing run or saved


@pytest.mark.parametrize(
    ("content", "extra", "message"),
    [
        (None, [], "--harness: "),
        ("  \n", [], "is empty"),
        ("Ask the agenda first.", ["--clinician", "human"], "model clinician only"),
    ],
)
def test_bad_harness_is_refused_before_anything_runs(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    content: str | None,
    extra: list[str],
    message: str,
) -> None:
    harness = tmp_path / "harness.md"
    if content is not None:
        harness.write_text(content, encoding="utf-8")
    out = tmp_path / "out"
    case = str(CASES / "edith_marsh.yaml")
    argv = ["run", case, "--harness", str(harness), "--out", str(out), *extra]
    assert main(argv) == 1
    assert message in capsys.readouterr().out
    assert not out.exists()
