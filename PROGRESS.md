# Progress

<!-- Keep current state compact (about 60 lines). Re-read on start/resume; merge concurrent
updates. History belongs in Git and DECISIONS, not here. Never imply unchecked work passed. -->

## Current state (10 Nov): closed

- **Project closed (the clinical lead, 10 Nov).** `docs/close-out.md` has the addendum; `docs/findings.md`
  item 6 has the last test.
- **Memory-clinic test (9–10 Nov): inconclusive by the rule.** Documents in, clinic letter out
  (`clinical-env review run|grade`), fictional cases with twins, 10 runs per file. After clinical
  review most misses were mark-scheme faults; what remained was style within guidelines (extra
  tests in the very old, hedged commitment) and one knowledge gap (insulin driving rules). The
  case files are fictional and are not published.

- **Project stopped (the clinical lead, 6 Nov).** v0 asked whether frontier models fail at managing a
  complex older adult across visits when patient, carer and records disagree. They do not:
  gpt-6-astra (high effort) met every critical in 30 of 30 runs (core set, negative workup,
  people-not-paper, noise), each under a rule frozen before the runs.
- Close-out: `docs/close-out.md` (what was learned, what is reusable, spend, what would reopen
  it). Evidence: `docs/feasibility-dev.md`; reasoning: `docs/pivot-options.md`.
- Consistent non-critical gaps: no agenda or ICE, vague local routes, no carers-register entry,
  mild over-investigation.
- **Thin-harness test (7 Nov): partial by the rule.** An 8-line generic prompt fixed agenda
  (22/24), ICE (24/24), the donepezil cascade (3/3) and Walt's stool test (2/3); not the carers
  register or offering a rectal exam (0/3 each). No critical lost. Gaps are prompt-deep except
  local practice conventions. Shelving goes ahead.
- **Spot-check and reference test (7 Nov):** the 4 harness verdicts stand (2 of 4, partial); Dot's
  rectal-exam item is unsupported by current NICE/BSG guidance (rubric defect, the clinical lead's call).
  Giving Pat two real UK carers documents fixed the register item (2 of 3, retrieval problem by
  the rule). The 3-run carer-cover miss (0 of 3) did not replicate at 10 vs 10 (9 vs 8 of 10);
  the register fix did (6 vs 0 of 10). At 10 runs the cover decision varies between a same-day
  referral and a dated coordinator call. Detail: `docs/feasibility-dev.md`, DECISIONS 7 Nov.
- **Public release prep (7 Nov):** personal details and live business ideas stripped; missing
  source attributions added; README and `docs/findings.md` written for a public copy.

## Dev scores so far (case score; criticals)

| Case | Clinician | Runs | Scores | Criticals |
| --- | --- | --- | --- | --- |
| Edith (UK, M3) | gpt-6.1-sol | 2 | 71, 79% | all met |
| Ray | gpt-6.1-sol | 2 | 84, 60% | all met |
| Gene | gpt-6.1-sol | 2 | 62, 85% | 1 miss (bundled wording, since split) |
| Marjorie | gpt-6.1-sol | 2 | 74, 77% | 1 miss (bundled wording, since split) |
| Harold | gpt-6.1-sol | 1 full + 1 visit-1 | 68% (v1: 78%) | 1 real miss, v2_act_on_level |
| Ray | gpt-6-astra | 3 | 84, 56, 72% | all met (after rewording to the clinical lead's standard) |
| Gene | gpt-6-astra | 3 | 88, 81, 88% | all met |
| Marjorie | gpt-6-astra | 3 | 69, 83, 83% | all met |
| Harold | gpt-6-astra | 3 | 80, 88, 80% | all met |
| Walt (negative workup, US) | gpt-6-astra | 3 | 76, 85, 82% | all met |
| Dot (negative workup, UK) | gpt-6-astra | 3 | 81, 96, 88% | all met (after the visit-3 mark-scheme fix) |
| Reg (people-only, UK) | gpt-6-astra | 3 | 96, 93, 93% | all met |
| Pat (people-only, UK) | gpt-6-astra | 3 | 77, 55, 73% | all met |
| Pat written twin | gpt-6-astra | 3 | 77, 73, 64% | all met |
| Pat noise | gpt-6-astra | 3 | 64, 50, 73% | all met |
| Pat + thin harness | gpt-6-astra | 3 | 73, 82, 82% | all met |
| Dot + thin harness | gpt-6-astra | 3 | 85, 88, 77% | all met |
| Walt + thin harness | gpt-6-astra | 3 | 76, 85, 76% | all met |

## Gates

- Last check: `./scripts/check` PASS on the close-out files (10 Nov, 416 tests).
- If reopened: pre-register each test's rule in a commit before running; 10 runs per arm when a
  rate matters; a clinician reviews every rubric item before freezing.

## Next up

Nothing. Reopening needs one of the triggers in `docs/close-out.md`.

## Known gaps (only matter if reopened)

- A referral's outcome is never written into a case (Dot's visit-3 miss came from this).
- US clinicians see stored ids in tool options; US records print British-order dates; the
  validator misses "Nov 5, 2026" and "(555) 123-4567" shapes.
- `Checker`, `match_exam` and `render_conversation` default to UK. Human runs log no tokens.
- Second-lab judge waits for `GOOGLE_API_KEY`; zero-retention settings unchecked.

## Waiting on the clinical lead

- Spot-check of 4 verdicts; merge PR #12; publish the public copy; the word to archive.
