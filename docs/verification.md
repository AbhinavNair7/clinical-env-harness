# Verification

How to show a change works through the real interface. Add a section as each milestone adds an
interface. Record the command, result, revision and dirty state in `PROGRESS.md` and the PR.

## Every change

- `./scripts/check`: Ruff format and lint, strict mypy, pytest. Must pass on the final files.
- Pytest never makes paid model calls. Model behaviour in tests uses Inspect's `mockllm/model`.

## Case files (M0)

- `uv run clinical-env validate cases/dev` must print `OK` for every file and exit 0.
- A new or edited case: validate it, then check by eye that each critical item is something a
  GP would be criticised for missing (the clinical lead's call, not the validator's).
- A change to the validator: add the authoring mistake it catches to `tests/test_validate.py`
  (one mutation of the Edith Marsh case, asserting the exact message).
- Twins are validated against their base (`twin_of`), found beside them as `<twin_of>.yaml`.

## Model roles (M0)

- `config/models.yaml` must assign every role; `tests/test_roles.py` loads the real file.
- Before relying on a new model id, check it against the provider's model list (free) and
  Inspect's installed provider code.

## Case runs (M1 one visit, M2 all visits)

- Model clinician: `uv run clinical-env run cases/dev/<case>.yaml --epochs 2` runs every
  visit in order. Writes `runs/<case>_<time>_run<k>.md` (readable transcript) and `.json`
  (case log), and an Inspect log in `logs/` (`uv run inspect view`), one sample per case.
  Needs `OPENAI_API_KEY` in `.env`.
- One visit for development: `--visit N`; add `--from runs/<earlier>.json` to carry over that
  run's earlier visits (without it, visit N starts with nothing to remember).
  `--memory notes|transcripts|none` sets what the clinician carries between visits.
- Human clinician: add `--clinician human`; type `help` for commands. Same outputs, no
  Inspect log.
- From visit 2 on, also check: the briefing holds only the clinician's own earlier plan; the
  GP record shows its "GP (you)" entry in date order; people remember only visits they were
  at and make up nothing about what happened since.
- Read one transcript end to end and check: the GP's opening shows no hidden text; replies
  are in character and under about 50 words; interjections and examinations appear in order;
  checker flags and rejected drafts are shown; the plan is complete.
- Changed the examiner or checker prompt, a reveal condition, or the checker model:
  `uv run python -m clinical_env.live_evals all` must be all correct (live, about 40 cheap
  calls; the checker varies run to run, so run it 3 times). Add every new mismatch or wrong
  flag seen in a transcript to `evals/examiner.yaml`, `evals/checker.yaml` or (later visits) `evals/checker_v2.yaml`.
- `tests/test_views.py` asserts no hidden truth, rubric, conflict, note, event, exam finding or
  view text reaches the clinician's opening, and each person sees only their own facts.
  `tests/test_adapters.py` runs one full Inspect visit on mock models.

## Live model evaluations

Run separately from pytest. Report the model ids, cases, run count, cost and results. Any
batch over $20 needs the clinical lead's approval first.
