# Close-out (6 Nov 2026)

**Decision: stop.** the clinical lead, 6 Nov, after both pre-registered rules said stop.

## The question and the answer

v0 asked: do frontier models fail at managing a complex older adult across 2–3 visits,
when the patient, a carer and the records disagree?

**No.** OpenAI's flagship (gpt-6-astra, high effort) met every critical item in 39 of 39 runs.

| Test | Cases | Runs | Critical misses |
| --- | --- | --- | --- |
| Core dev set | Ray, Gene, Marjorie, Harold | 12 | 0 (after Ray's critical was reworded) |
| Negative workup (do less) | Walt, Dot | 6 | 0 (after Dot's visit-3 mark scheme was fixed) |
| People, not paper | Reg, Pat, Pat's written twin | 9 | 0 |
| Noise | Pat with realistic clutter | 3 | 0 |
| Thin harness (7 Nov) | Pat, Dot, Walt with an 8-line generic prompt | 9 | 0 |
| Documents added (7 Nov, not part of the 39) | Pat, thin harness plus two UK carers documents | 3 | 3 (carer cover; did not replicate) |
| 10 vs 10 rerun (7 Nov, not part of the 39) | Pat, thin harness with and without the documents | 20 | 1 thin, 2 documents (carer cover) |

The rules were frozen in commits before each run. Detail: `docs/feasibility-dev.md`.

## What we learned

1. **The flagship is very good at the core job.**
   - It reconciles records against what people say: it weighed Ray, checked Gene's letter,
     and ordered a scan anyway.
   - It shows restraint after a negative workup.
   - It asks people what matters to them. Reg was asked what mattered most in 3 of 3 runs.
   - It finds a carer's hidden problem by asking, with or without a cue.
2. **Its gaps are real but cost points, not plans, and most are a prompt away.** An 8-line
   generic harness fixed agenda and ICE (0 of 24 visits to 22 and 24 of 24), the donepezil
   cascade (0 of 9 to 3 of 3) and a missing stool test; it did not fix UK practice conventions
   (carers register, offering a rectal exam). Without the harness:
   - It never asks for the agenda, or for ideas, concerns and expectations.
   - Its local service routes are vague.
   - It arranged a carer's assessment but never added Ken to the carers register (9 of 9).
   - It over-investigates mildly.
   - Case scores of 50–96% would look like failure on a dense rubric (HealthBench style). They
     are not failures of care.
3. **Published "failures" mostly come from levers we chose not to pull:**
   - weaker or base models;
   - dense partial-credit rubrics;
   - sources that lie with no paper trail;
   - scale;
   - very long horizons.

   We tested the flagship on fair, well-documented cases. That was the right test for the
   question, and it passed (`docs/pivot-options.md`).
4. **Case reports are the wrong raw material for finding failures.** A published case is
   coherent by design. It is good for realism and poor for finding blind spots. Failures, if
   they exist, would more likely come from real consultation recordings or real records at
   scale. Neither is available to us.
5. **Method lessons worth keeping:**
   - Check realism before paid runs, never after.
   - Write criticals to the GP standard, not as a checklist. Ray's "name every cause" wording
     produced false misses.
   - A referral's outcome must be written into the case (Dot's false misses).
   - Pre-register the rule in a commit before running. It made stopping easy and honest.

## What is reusable

| Asset | Where | Reuse |
| --- | --- | --- |
| Multi-visit harness | `src/clinical_env/` (run, visit, simulators, views, llm_clinician) | Any multi-party simulated consultation, any domain. Model choice is set in config through Inspect AI |
| Grader | `src/clinical_env/grader.py` | Rubric grading with `requires`, quote checks and over-provision caps |
| Case format and validator | `case_schema.py`, `validate.py`, `docs/case-template.md` | A case format with hidden facts, disclosure rules, conflicts and twins |
| 12 dev case files | `cases/dev/` | 9 cases plus 2 written twins and 1 noise copy. All fictional; UK and US |
| Sourcing pipeline | `src/clinical_env/sourcing/`, `docs/case-sourcing.md` | Europe PMC with a CC BY/CC0 licence check, overlap check and MIMIC demo record patterns |
| Evidence | `docs/feasibility-dev.md`, `docs/pivot-options.md`, `docs/research-summary.md` | Why frontier models pass on fair cases |

Code size: about 5,700 lines of Python; 393 tests pass (`./scripts/check` at 713c6fc).

**Not in Git:**
- Run transcripts and grades: `runs/`, `logs/`. These are the only copy and are kept on this
  Mac.
- Source full texts: `sources/pulls/**/fulltext`. These can be pulled again.
- `.env`.

## Spend

About $65–70 of OpenAI usage on flagship runs, all estimated, none billed separately:
- about $18 for the core set;
- about $12–13 for the negative workup;
- about $15–20 for the pivot and noise tests;
- about $15–20 for the thin-harness test.
- about $5–7 for the reference-document test (3 runs and grading);
- about $35–45 for the 10 vs 10 rerun (20 runs and grading).

Cheap dev and smoke runs add a little on top.

## What would have to change to reopen

Any one of these:
- a new model class that fails these cases;
- a buyer who wants this as a training environment rather than as a failure finder;
- access to real consultation data where failures are already visible.

The harness would carry over. The cases would not need rewriting.

## Addendum (10 Nov 2026): final close

**Decision: closed.** the clinical lead, 10 Nov.

- **Memory-clinic test (9–10 Nov).** A second, cheaper task (documents in, clinic letter out;
  `clinical-env review run|grade`, `src/clinical_env/review_task.py`) on fictional memory-clinic
  cases with twins. Inconclusive by its frozen rule. After the clinical lead's review most misses were
  mark-scheme faults; what remained was style within guidelines (extra tests in the very old,
  hedged commitment) and one knowledge gap (insulin driving rules). `docs/findings.md`, item 6.
- **Two follow-on ideas were considered and not built:**
  - *An AI that learns one clinician's style.* Parked: it would repeat the clinician's own
    errors, hospitals pay to reduce variation, not to preserve it, and advice about a specific
    patient is regulated as a medical device in the UK.
  - *A private log of lessons from case discussions with an AI.* Parked: few doctors discuss
    whole cases with an AI, a 10-minute appointment leaves no time, case content cannot leave
    approved tools, and the need fades as experience grows.
- **Lesson for a next project:** start from a problem other people report, that happens often
  and has someone who pays, and check that before building.
- **Numbers at close:** 416 tests pass (`./scripts/check` at dd0181d; later commits are docs
  only). Total spend about $110–130 of OpenAI usage, estimated.
- **Not in Git:** the memory-clinic case files. They are fictional, but stay on the clinical lead's Mac
  with `runs/`, `logs/` and `.env`.

## Archive

Done. The folder is at `~/Documents/archive/clinical-env` with `runs/`, `logs/` and `.env`
inside it. Archiving the GitHub repos is optional and the clinical lead's call.
