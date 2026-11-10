# Decisions

## Active decisions

<!-- Keep this current and short (about 30 lines). Read on start/resume. Link dates to the
entries below; remove superseded summary bullets and update affected current rules. -->
- 2026-11-01 — An environment company (simulator, tools, grader as one harness); no model of our own.
- 2026-11-01 — Kill rule: if frontier models already handle these cases well, stop.
- 2026-11-01 — A second GP rates the same cases blind.
- 2026-11-01 — AMIE Mx is proof of demand, not ground already taken.
- 2026-11-03 — No public code for ResidencyRL or AMIE Mx; build our own from ResidencyRL's published design.
- 2026-11-03 — [arch] Python (uv) llm-app stack; Inspect AI is the model client, runner and transcript viewer; case schema, simulators, visit loop and grader stay plain Python.
- 2026-11-03 — Clinician tools: `say`, `read_record`, `examine`, `submit_plan` (ends the visit).
- 2026-11-03 — Cases: 2–4 critical items; between-visit events hold whatever the clinician did; every hidden fact has a reveal condition.
- 2026-11-03 — Persona-driven interjection when patient and carer are both present.
- 2026-11-04 — Pilot (plan review, replaces 3 Nov): internal go/stop gate only; 3 dev + 10 frozen pilot cases + one pre-registered extension of 10; best model = lowest miss rate over the set; Stop if OpenAI passes ≥8/10; Go ≥4/10 missed, 3/10 → extension; pooled 20: Stop ≥16 pass, Go ≥8 missed; 3 runs per case; raters the clinical lead and a second clinician; criticals reviewed by two GPs before freeze.
- 2026-11-04 — Simulators run on one fixed open-weight model in the pilot (fallback Claude or Gemini + 3-case sensitivity rerun), never OpenAI; judges from another lab; zero-retention settings; frozen set unpublished during the pilot.
- 2026-11-04 — Messiness in the schema (case level mild/moderate/high, person traits, record traits); stage tag on every critical; human runs carry run type, anonymised participant, role, grade, consent and are never pooled with model scores.
- 2026-11-04 — Pilot set is not all traps: a carer in about half to two thirds of cases; conflicts in degrees, one or two cases nearly clean.
- 2026-11-04 — Secondary checks, never go/stop: thin-prompt rerun of each missed case; consistent-sources twins. M4 adds an HTTP clinician adapter.
- 2026-11-03 — Keys: build on OpenAI only; the pilot runs OpenAI's flagship first and adds Gemini and Claude only if it is not already Stop. Gemini (credit available) is the second-lab judge for the real run.
- 2026-11-03 — [arch] Project memory lives in `AGENTS.md`, `PROGRESS.md` and this file.
- 2026-11-03 — Pilot stays older-adult only; consistent-sources twins test whether conflicting sources cause the failures (secondary, not in go/stop; number at 10 cases proposed below).
- 2026-11-03 — [arch] Case file format: one YAML per case, top-level rubric tagged by visit; a twin is a separate file holding only views and rubric, inheriting truth, personas and visits from its base.
- 2026-11-04 — Edith Marsh criticals: reconcile meds, falls and function, care package review, visit-2 delirium (the clinical lead swapped care package in; asking the daughter is now a weight-3 normal item).
- 2026-11-03 — M1 visit rules: the clinician is told its turn budget; every action (including an invalid one) is a turn; hard cap 2× budget ends the visit with no plan; a cheap model maps `examine` requests to the case findings.
- 2026-11-04 — Unlisted investigations are "not available" (unlisted exams stay unremarkable, so cases list every abnormal finding); a twice-leaked kept-back fact gets a last draft without it; time-weighted actions and delayed results wait until after the pilot (the clinical lead).
- 2026-11-04 — Simulators: two or a few related questions get answered; three or more different ones get only the first one or two answered (the rest not denied); chatty personas may make harmless asides; a volunteered item is said once. Cases script a standard history for each person (the clinical lead).
- 2026-11-04 — [arch] Records are written out as real documents with fact slots and dates relative to visit 1; adds an ambulance report; weighing is "not available" on a home visit.
- 2026-11-04 — [arch] Multi-visit: a case runs all visits in order, a fresh clinician context each, carrying its own plans as notes (configurable) and "GP (you)" entries in the GP record; people remember the spoken conversation of visits they attended; one Inspect sample per case (the clinical lead approved the plan).
- 2026-11-04 — Scripts and examination after the clinical lead's M2 read: a symptom not in a person's script is one they do not have (they say no, as an unlisted exam is unremarkable); clinically meaningful details still come only from the script, and gaps are filled in the case, not by loosening the checker; an exam request gets one finding, a named set ("obs") or some of its parts, never several examinations; people speak only in their own voice (the clinical lead said go).
- 2026-11-04 — [arch] Grader: `clinical-env grade`; one judge call per rubric group per visit; code checks `requires`, quotes and the log; consultation score apart; over-provision capped at 3 per visit; primary judge from another lab (weights for the clinical lead to confirm).
- 2026-11-04 — Pilot judged on criticals only; grader weights, penalties and consultation score frozen until after the pilot; review time goes on critical verdicts; case writing is the main effort (the clinical lead).
- 2026-11-04 — A must-not-do may be a critical item (fails the case if it happens). Most cases should have a critical a do-everything plan fails, but it is not enforced per case; Edith keeps its 4 criticals (the clinical lead, plan review change 13 amended).
- 2026-11-05 — [arch] Per-case `country` (uk/us): every word a model reads follows it (`locale.py`); UK prompts unchanged; criticals stay country-neutral, local routes are normal items (the clinical lead chose US for new cases).
- 2026-11-05 — [arch] Requested tests come back by the next visit (`Visit.results`; unlisted tests normal); supersedes the 4 Nov deferral of later results. Every critical lists `evidence`, at least one earned (asked, examined, tested or after visit 1), so no critical is met from records alone (the clinical lead).
- 2026-11-05 — Identifiability: a match on the case's theme alone (e.g. pancreatic cancer + worsening diabetes) is accepted; provenance lists `theme` terms and only pairs with a case-specific detail must not find the source. An early decisive scan (visit 1) is slightly much but never penalised; later criticals credit acting on it (the clinical lead).
- 2026-11-05 — New cases are ambiguity-first over 3 visits (rethink at visit 3, as in Jess's Rule); no "plan was not followed" device by default; cases are never kept or dropped by model results (the clinical lead).
- 2026-11-05 — Dev cases can be built on CC BY/CC0 case reports plus MIMIC demo record patterns (`docs/case-sourcing.md`); 2 US sourced dev cases replace the clinical lead's from-scratch dev case, which he reviews and adds to; 100+ cases only after a Go (the clinical lead).
- 2026-11-05 — Dev-case calls (the clinical lead): Gene's 4th critical (Carol's breakdown, only if asked) stays critical; naming "his pancreatic mass" or "lesion" on a visit-3 phone call without warning counts as breaking bad news ("concerning, not confirmed" is fine); the US over-provision examples and local pathways are accepted as drafted.
- 2026-11-05 — Bare-model clinician prompt no longer hints that records may disagree (the hint belongs to the thin-prompt tier); dev cases carry a confidently wrong person who asserts a checkable false fact (Ray's Dolores on weight, Gene's Carol on a brain scan) (agent, agreed plan, the clinical lead said go).
- 2026-11-05 — Flagship feasibility (gpt-6-astra, 4 dev cases x 3): every critical met in all 12 runs once Ray's differential critical was reworded to the clinical lead's standard (work up cancer and keep the common causes on the plate, not a checklist). Next test: negative-workup cases, Stop rule pre-registered below (the clinical lead said go).
- 2026-11-05 — A case may have up to 5 criticals where 3 visits genuinely need them (Walt: the visit-2 suicide question is critical); criticals stay separate rather than merged into strict bundles (the clinical lead).
- 2026-11-05 — Negative-workup test: The clinical lead judged Dot's 3 visit-3 flags not real misses (the model chased the first-line GI referral the case never resolved; mark scheme fixed), so 0 of 6 and the pre-registered rule says Stop. Go is off the table; the next chat decides pivot or stop completely (the clinical lead).
- 2026-11-06 — Pivot test pre-registered: "people, not paper" (decisive fact held only by a person), 2 cases plus a written twin, 9 flagship runs; rule below (the clinical lead said go; agent wrote the cases, he reviews after).
- 2026-11-06 — People-not-paper result: every critical met in all 9 runs (0 of 6 base runs with a people-only miss), so the pre-registered rule says stop completely. Ending the project is the clinical lead's call.
- 2026-11-06 — Noise test pre-registered (the clinical lead's point: in a thin text case every detail is a signpost): `pat_ellison_noise`, 3 flagship runs; rule below.
- 2026-11-06 — Noise result: Ken's operation found in 3 of 3 noisy runs (2 through plain carer questions, no cue), bruise ignored; salience thesis not supported, stop stands.
- 2026-11-06 — **Project stopped** (the clinical lead): 30 of 30 flagship runs met every critical; close-out in `docs/close-out.md`; archive on his word.
- 2026-11-06 — Pre-registered: thin-harness test (Pat, Dot, Walt; 3 flagship runs each with `config/harness-thin.md`). 3 or more of 4 clinical misses fixed means the gaps are prompt-deep and the stop stands.
- 2026-11-07 — Thin-harness result: partial by the rule (2 of 4 clinical misses fixed: donepezil 3/3, stool test 2/3; carers register and rectal exam 0/3); agenda 22/24 and ICE 24/24; no critical lost. The gaps are prompt-deep except local practice conventions; shelving stands.
- 2026-11-07 — Spot-check of the 4 thin-harness verdicts done (agent pass on the clinical lead's instruction; no overrides): count stays 2 of 4, result stays partial. Dot's rectal-exam item is unsupported by current NICE NG12 (2023) and BSG IDA 2021, so it is a rubric defect, not a model gap; the clinical call on it is the clinical lead's.
- 2026-11-07 — Pre-registered: reference-document test (Pat only, 3 flagship runs, thin harness plus two real UK carers documents in the prompt). Carers register added in 2 or more of 3 runs means local practice convention is a retrieval problem, not a model gap.
- 2026-11-07 — Reference-document result: **fixed by the rule** (carers register item met 2 of 3; registration surfaced in 3 of 3 plans vs 0 of 3), so this local-convention gap is a retrieval problem. But the critical `v1_carer_cover` was missed in 3 of 3 runs (0 of 3 with the thin harness alone): with the documents in the prompt the model pressed once, then settled for a next-day care-coordinator call instead of a referral. The clinical lead to review the three critical verdicts; shelving stands. (Did not replicate at 10 vs 10; see below.)
- 2026-11-07 — Pre-registered: context-sensitivity test (Pat, 10 runs thin harness vs 10 runs thin harness plus the same two documents). Confirmed only if the documents arm meets `v1_carer_cover` less often with two-sided Fisher p < 0.05; a difference of 2 runs or fewer means not replicated.
- 2026-11-07 — Context-sensitivity result: **not replicated** (carer cover 9 of 10 thin harness vs 8 of 10 with documents). The 3-run 0 of 3 was a bad batch. Replicated: documents fix the carers register (6 of 10 vs 0 of 10). New: at 10 runs the cover decision varies (referral today vs a dated coordinator call), which 3-run tests hid.
- 2026-11-09 — Document-review task (`clinical-env review`): records in, impression and plan out, one judge call with quotes checked; fictional memory-clinic cases with twins, not published; gpt-6-astra only, 10 runs per file, rule frozen before the runs.
- 2026-11-10 — Memory-clinic result: inconclusive by the rule; after clinical review most misses were mark-scheme faults; remaining gaps are style (extra tests in the very old, hedging) and one knowledge gap. Detail: `docs/findings.md` item 6.
- 2026-11-10 — Project closed (the clinical lead). Two follow-on ideas (an AI that learns one clinician's style; a private log of lessons from AI case discussions) were considered and not built; reasons in `docs/close-out.md`.

## Proposed, not yet agreed

| Question | Proposal |
| --- | --- |
| First buyer | Expert-data and environment vendors, and clinical agent companies whose product runs whole consultations or follows patients over time. Labs come inbound through a public result; narrow tools (triage, intake, voice) later through slices. Named target list in progress (not an agent task) |
| Documentation AI | Park it. Revisit through discharge and care-plan summaries |
| Pitch | Lead with the combination (function, carers, conflicting records, no single diagnosis), not "longitudinal" |
| Raters after a Go | A geriatrician and a community nurse or social worker, before anything reaches buyers |
| Pilot size at 10 cases | 4 twins (was 6 of 15) and 3 human-baseline cases. Rough cost: 90 flagship case-runs $180–1,080 (about $530 mid); only 30 ($60–360) if step 1 is Stop; twins 12 runs about $25–145; thin-prompt reruns up to 10 runs about $20–120; two judges about $50–200. Total roughly $300–1,500, each batch over $20 approved first |
| Pooled-20 tie-break (5–7 missed) | Stop on the broad thesis; if the misses cluster in one stage or messiness level, one written pivot proposal, no new scoring round. Decide before the freeze |
| Extra kill rules | No paid pilot or LOI by month 6. Grader below inter-clinician agreement |
| Population contrast | After a go: 15–20 matched pairs (same conflict structure, another population), GP raters, specialist sign-off of critical items. Best candidates: learning disability, severe mental illness |

## Open questions

- Pilot simulator model and provider (open-weight, not OpenAI): needs a provider account; pick and test on the dev cases before the feasibility runs.
- Exact pilot model IDs and effort settings are re-checked on the day the pilot is frozen (lineups move monthly).
- AMIE Mx multi-visit scenarios: no public release found on 3 Nov (Nature page needs sign-in). Low priority; we write our own cases.

---

Append consequential decisions below with **Decision** and **Why**. Preserve history; a new
entry can supersede an old one, saying what evidence changed. Search the log for the current
topic instead of loading it all.

Architecture decisions (undoing would cost more than a day or touch stored data or users) are
tagged `[arch]`, written in the same commit as the code, and add **Instead of**, **To undo** and
**By** (who chose: agent or owner). Keep each to a few lines.

## 2026-11-03 — [arch] Project memory in AGENTS.md, PROGRESS.md and DECISIONS.md

**Decision:** The original `docs/decisions.md` is migrated here; its "Next step" and "Waiting on the clinical lead" move to `PROGRESS.md`; the original `CLAUDE.md` content becomes the Context in `AGENTS.md`.
**Why:** The shared workflow's session-start hook shows these files in Claude Code, Codex and Cursor, so no agent starts stale. Supersedes the 2026-11-03 "this file is the shared memory" entry below.
**Instead of:** Keeping `docs/decisions.md` with pointer files (two conventions, hook would not show the log).
**To undo:** Under an hour: move the log back and repoint `AGENTS.md`. Rethink if the shared workflow is dropped.
**By:** Owner, on agent recommendation.

## 2026-11-03 — [arch] Python llm-app stack with Inspect AI as the harness layer

**Decision:** Python 3.12 with uv, Pydantic for the case schema, ruff/strict mypy/pytest. Inspect AI (UK AI Security Institute) supplies the model client for OpenAI, Anthropic and Google, model roles (clinician, patient, carer, checker, grader), concurrency, epochs, retries, per-sample cost limits and the browser transcript viewer. The case schema, simulators, visit loop and grader are plain Python behind a small async `generate` callable, so a verifiers or Gymnasium wrapper can reuse them later.
**Why:** Removes most of the planned client, runner and report code; labs' eval and safety teams already run Inspect tasks, which helps distribution.
**Instead of:** Official SDKs behind our own adapter plus our own runner and HTML report (more code to own). LiteLLM was ruled out: its PyPI package was compromised on 24 Mar 2026.
**To undo:** About 2 days: replace the thin Inspect layer with direct SDK calls; the core is unaffected. Rethink if Inspect blocks multi-party loops or per-call cost logging.
**By:** Owner, on agent recommendation.

## 2026-11-03 — Clinician gets an examine tool

**Decision:** Tools are `say(to, message)`, `read_record(name)`, `examine(what)` and `submit_plan(...)`, which ends the visit. `examine` returns findings written into each visit of the case (for example lying/standing BP, gait or timed up-and-go, home hazards, dosette contents, cognition screen). Anything not listed returns "unremarkable"; on a phone visit it returns "not possible".
**Why:** A falls and function assessment needs in-visit observation; with history and records only, the model could never find a postural drop.

## 2026-11-03 — Case design rules

**Decision:** Each case has 2–4 critical items, each something a GP would be criticised for missing; everything else is a weighted non-critical item. Between-visit events must make sense whatever the clinician did at the previous visit. Every hidden fact has a one-line reveal condition, which the checker uses to confirm the fact was earned, not leaked.
**Why:** "Missed at least one critical" grows with the number of criticals, so an uncapped rubric inflates the Go signal. Fixed events must not contradict sensible earlier actions.

## 2026-11-03 — Persona-driven interjection

**Decision:** When patient and carer are both present, after each reply the party not addressed gets one cheap call to interject (30 words or fewer) or stay silent, controlled by a persona field (always, sometimes, never).
**Why:** In real home visits the carer correcting the patient is often how a conflict surfaces; an addressed-only simulator is tidier than reality.

## 2026-11-03 — Pilot protocol

**Decision:**
- Models: the flagship of each lab at high effort (on 3 Nov: gpt-6-astra, claude-fable-5-1, gemini-4-argon). Build and tune on cheaper models (gpt-6.1-sol, claude-sonnet-5-5); simulators and checker on cheap models (claude-haiku-5-5, gpt-6-luna, Gemini Flash).
- 3 runs per case per model. A case counts as missed when the best model misses at least one critical item in 2 or more of 3 runs, confirmed by a clinician, with the simulator on script.
- Human baseline: a GP colleague who is not a rater plays clinician on 3–5 cases through a human adapter. The clinical lead uses the same adapter to QA every case.
- Raters score each critical item (met or not) plus one overall 1–5 rating per transcript. Agreement is reported as raw %, Gwet's AC1 and Cohen's kappa, with ICC for overall scores.
- Judges are strong models from two labs; each tested model's primary score comes from a judge outside its own lab, and both are reported. Visit-2 grading sees the visit-1 plan.
- Cases, rubric, clinician prompt and thresholds are frozen in a commit before the first real run. Edith Marsh and 2 development cases are used for tuning and never counted. An in-between result adds up to 10 cases once, then the decision is made on the pooled set. Exclusions only for checker-flagged simulator drift, decided with model names hidden.
**Why:** At 12 cases and 1 run, a 40% miss rate has roughly a ±28-point 95% interval and one-off flukes count; a human baseline shows the criticals are achievable, so misses can't be dismissed as an unfair rubric. Flagships match the kill rule's "frontier models". Rater scope keeps volunteer time to about 6–8 hours each.
**Cost:** About $2–12 per case-run at 3 Nov flagship prices; about $800 for 15 cases × 3 models × 3 runs. Each batch over $20 is approved first. Gemini 4 Argon's price doubles on 1 Dec 2026.

## 2026-11-03 — Pilot population and mechanism check

**Decision:** The pilot stays older adults only; no paediatric, mental health or young-adult cases are swapped in. Six pilot cases, chosen at random before the freeze, get a consistent-sources twin (same case, every source accurate), run 3 times on the best model and reported separately from go/stop. Critical items are tagged `clinical_action` or `discrepancy_detection`; twins are compared on `clinical_action` items. Also: human-baseline cases are chosen at random and the GP miss rate is reported; case edits after meeting a model fix simulator or realism bugs only and are logged; at least one confirming rater is not the case author.
**Why:** Three contrast cases give 95% intervals about 70 points wide, change population, rubric, difficulty and raters at once, and dilute the frozen go/stop. Varying the mechanism inside a case tests cause directly. Evidence and power figures: `docs/research-summary.md`, "Population or mechanism?".
**Cost:** About $110 extra.
**By:** Owner, on agent recommendation.

## 2026-11-03 — Staged keys and pilot run order

**Decision:** M0 needs no keys; M1–M5 use OpenAI only. The pilot runs OpenAI's flagship first; if it meets every critical item in at least 80% of cases the result is Stop and Gemini and Claude are not run, otherwise both are run. Gemini, on the clinical lead's credit, is the second-lab judge for the real run. xAI is not used. This run order is part of the freeze. Supersedes the 2026-11-03 keys bullet (all three keys from the start).
**Why:** Stop depends on the best model, and the best model is at least as good as OpenAI's, so one model can settle Stop on its own; Go needs all three. This saves about $500 if the answer is Stop and defers the Anthropic key until the pilot. A same-lab judge favours its own models, so the real run needs a second lab.
**By:** Owner, on agent recommendation.

## 2026-11-04 — Plan review: agreed changes (the clinical lead)

**Decision:** The 17 changes from the clinical lead's Claude-chat review of `docs/plan-overview.md`
(source: his "agreed changes" note, 4 Nov). Pilot: internal go/stop gate, miss rate never
quoted outside the team (1); a sales percentage only from a separate private set of about 30
cases (2); lead sales asset is 3–5 annotated failure transcripts tied to unsafe misses (3);
"best model" is the single model with the lowest miss rate over the set, all three reported
(4); the clinical lead and a second GP review every critical before the freeze, dropping any
either calls idiosyncratic; outside clinicians after a Go (5); 3 dev cases, 10 frozen pilot
cases, one pre-registered extension of 10 (6); thresholds as in `docs/build-v0.md` (7);
messiness explicit in the schema (8); between-visit events plausible whatever the plan, and
visit 2 grades follow-up of the model's own plan (9, `c_follow_up_plan` in the consultation
rubric); pilot raters the clinical lead and a second GP, external raters after a Go (10); zero-retention
settings, set unpublished during the pilot, pilot cases become the open pack afterwards (11);
thin-prompt rerun of each missed case, secondary (12); simulators on one fixed open-weight
model, never OpenAI (14); pluggable HTTP clinician in M4 (15); a stage tag on every critical
(16); human runs saved in the same format, never pooled with model scores (17).
Change 13 ("every case has a must-not critical") is amended at the clinical lead's request: a guideline,
not a validator rule. For Edith the only candidate (managing visit-2 confusion by phone alone)
restates the visit-2 critical, and a forced must-not would cost a real critical under the cap
of 4. Also agreed in the same session: a carer only where realistic and conflicts in degrees,
one or two nearly clean cases, so buyers cannot say the test is rigged.
**Why:** 10 cases give intervals too wide for buyers but enough for an internal gate; fixed
goalposts; an OpenAI simulator could bias a Stop decided on OpenAI alone; author bias.
**By:** the clinical lead (all clinical and pilot choices), agent (schema, wording).

## 2026-11-04 — [arch] Messiness, stage and human-run fields

**Decision:** `Case.messiness` (mild/moderate/high, required; a twin may override: Edith is moderate, its twin
mild), `Persona.traits` (denies_minimises, tangents, poor_recall, carer_dominates; rendered as
habits in the person prompt, never as new facts), `Case.record_traits` per record
(contradicts_other_records and outdated_entries are checked against conflicts and facts),
`RubricItem.stage` (required on criticals). `CaseLog.run_type` (model/human) and
`participant` (anonymised ID, role, grade, consent); `run --clinician human` refuses without
`--participant/--role/--grade/--consent`; older logs with clinician "human" read as human.
A discrepancy_detection critical now needs a conflict in the case.
**Why:** Changes 8, 16 and 17. Tags checked against facts keep the messiness spread honest.
**Instead of:** Free-text messiness notes (not checkable, not filterable for slices or reports).
**To undo:** Under an hour: drop the fields and the YAML keys; saved logs ignore extra keys.
**By:** agent.

## 2026-11-05 — [arch] Requested tests and earned evidence (the clinical lead)

**Decision:** A visit may list `results` (label, finding). After the visit, the cheap checker
model maps the plan's investigation actions to them (`visit.match_results`, live eval
`evals/results.yaml`, 10/10 twice). At the next visit each order is back in the primary care
record as a "Results" entry: listed tests give their finding, anything else ordered comes back
normal, and an unreadable match shows "result not back yet" with the error logged. `results:
None` (every case written before 5 Nov) keeps the old behaviour, where a requested test is
graded from the plan only. Results on the last visit are rejected. Every critical item lists
`evidence` (fact, examination or result ids). At least one must be earned: a person's fact
given when asked, an examination finding, a test result, or a fact from after visit 1.
Twins are exempt.
**Why:** the clinical lead's review: cases that turn on a document are solved by reading it, and
real difficulty is diagnostic uncertainty that unfolds as tests come back (premature closure
and anchoring are the failure modes the 2025-26 papers report). Supersedes the 4 Nov
deferral of "results that arrive later".
**Instead of:** Results arriving by routes that fit any plan (another clinic, the ER): less
realistic, and a test the clinician ordered would never come back.
**To undo:** About half a day: drop `results`, `match_results`, `result_entries` and the
evidence rule; old cases never used them. Rethink if turnaround times matter (a CT that takes
weeks) or the matcher's misses show in runs.
**By:** the clinical lead (build now, evidence rule); agent (design).

## 2026-11-05 — [arch] Per-case country toggle (uk/us)

**Decision:** `Case.country` (required; Edith and its twin `uk`). `locale.py` holds every
country word a model reads: the clinician's role, the consultation name, the speaker label
people and the judge see ("GP" / "Doctor"), record titles, setting names, the author of the
clinician's own record entries, the judge's role and over-provision examples, and the
`c_local_pathways` examples (`rubrics/consultation.yaml`, now per country). UK templates are
returned unchanged, so UK runs and the UK live evals need no rerun; US templates swap UK terms,
and a test checks no UK term reaches a US prompt. Stored ids and logs (`gp_record`, speaker
"GP") are unchanged, so saved runs load. The validator rejects UK wording in a US case, and SSN
and MRN shapes and US-order dates in any case. Criticals in sourced cases are country-neutral
clinical actions; local routes are normal items, so UK raters can judge US cases.
**Why:** the clinical lead asked for US cases now, with a toggle so the harness handles both (4 Nov).
**Instead of:** A second set of prompt files per country (drift between them); rendering one
case in either country (units, services and drug names live in the case's own text).
**To undo:** About an hour: drop the field and `locale.py`; UK wording is the template text.
Rethink if a third country is added (then a template per country may be simpler) or the US
over-provision and pathway examples (agent's drafts) need more than a phrase swap.
**By:** the clinical lead (US setting, toggle); agent (design). US examples for the clinical lead to confirm.

## 2026-11-05 — Cases built on open case reports (the clinical lead)

**Decision:** A case may take its clinical arc from a CC BY or CC0 case report (licence checked
in the article's own full-text XML), its record mess from `docs/record-patterns.md` (including
aggregate MIMIC-IV demo counts, ODbL) and invented people. Provenance is internal
(`sources/provenance/`). Checks: validator, zero 8+ word overlap with the source, the source
not in the top 10 of Europe PMC searches for the case's distinctive details (all, each pair,
any), at least 3 meaningful changes. The first 2 are US dev cases (Marjorie Lindqvist, Harold
Benning), used in the feasibility check, and they replace the clinical lead's from-scratch dev case: he
reviews them and adds primary care detail instead. Scripted drafting and 100+ cases wait until
after a Go.
**Why:** the clinical lead's time is the bottleneck; real arcs read true; the same tools make the 10
pilot cases. Pilot cases are never run before the freeze, so cases run now are dev cases.
**By:** the clinical lead (idea, US, dev use); agent (pipeline, checks).

## 2026-11-04 — A must-not-do can be critical (the clinical lead)

**Decision:** A must_not_do item may be marked critical (still 2–4 criticals per case). It
fails the case when it happens, and is judged with the other must-not-dos. Not used in Edith.
**Why:** Some serious errors are things done, not missed (e.g. an unnecessary admission or
safeguarding referral, if a case author judges that a GP would be criticised for it). Allowed,
not required.
**By:** the clinical lead; agent implementation.

## 2026-11-04 — Edith criticals swap; consultation rubric widened (the clinical lead)

**Decision:** Edith's care package review becomes critical (clinical_action, also in the twin)
and asking the daughter becomes a weight-3 normal item. The consultation rubric adds the
Calgary-Cambridge skills (open start, agenda, signposting, summarising, explain-and-check,
shared decisions, safety-netting); every item is met once per visit, and repeating it or
reciting it as a script earns nothing. `c_uk_pathways` becomes `c_local_pathways`: the routes
of the health system the case is set in (UK in v0). The case template now asks for the
criticals first, numbered, with why there are at most 4.
**Why:** the clinical lead's read of the M3 scorecards. History-taking skills are the same in any
country; only the referral routes are local. With the swap, both M2 Edith runs meet every
critical (their only critical miss was asking the daughter).
**By:** the clinical lead (clinical choices), agent (wording). This edits the "frozen" consultation score
once, before the pilot; it still never decides go/stop.

## 2026-11-04 — Pilot focus: criticals only (the clinical lead)

**Decision:** Go/stop rests on critical items alone, as the pilot criteria already say. The
grader's weights, penalties and consultation score are frozen as built and not tuned before
the pilot. The clinical lead's review time goes only on the critical verdicts (the "(critical)" rows of
each scorecard), which is also what the "grader usable" test and the M5 rating form check.
Case writing, with sharp, gradable criticals, is the main effort.
**Why:** Nothing outside the criticals changes the pilot result. The rest stays because it is
built and cheap: a graded reward for a training environment after a Go, and sales material.
**By:** the clinical lead, on agent recommendation. Grading the full scorecard every run is kept (cost
is not a concern).

## 2026-11-04 — [arch] Grader (M3)

**Decision:** `clinical-env grade <case.yaml> <run.json>...` grades saved case logs and writes
`<run>.grade.md` and `.grade.json`. Per visit, one judge call per group: criticals, other
must-dos and red flags, must-not-dos with penalties, and a generic consultation rubric
(`rubrics/consultation.yaml`, the clinical lead's "Score in M3" points; its own score, never go/stop).
The judge sees the hidden truth, every source, the records exactly as the clinician read them,
the visit transcript, the plan and the clinician's earlier plans (context, no credit). Code
decides what it can: rubric items may carry `requires` (examined / read / spoke_to), and a
judge's "met" without it is overruled; "reads records before its questions" (one greeting turn
first is fine: the clinician starts in the room, the clinical lead 4 Nov) and the turn budget come
from the log. Each "met" needs an exact quote (pieces of 12+ characters from what was said, found or
planned; a penalty must quote the clinician), checked in code with one retry that never swaps a
better reply for a worse one. A quote still not found leaves the item ungraded (not met, not
missed) and a penalty uncounted; an unreadable judge or provider error leaves its group
ungraded; any ungraded case item makes the score n/a, so a judge failure never reads as a
clinician failure. `grade --from` gives a lone later visit its earlier plans. Talk earns asking, advising and examining;
anything arranged counts only from the plan's actions; a mention earns nothing. Score per visit
and case = (earned weight − deductions) / possible, floored at 0; criticals reported apart.
Deductions: a must-not-do that happened (its weight), invented fact 2, acting on a wrong fact 3
(ResidencyRL), over-provision 1 each capped at 3 per visit, over budget 1. Over-provision
examples in the judge prompt are the clinical lead's from the M1 review. Several `--judge` models give
one scorecard each plus item agreement; the primary is the first from a lab other than the
clinician's (`CaseLog.clinician`, new). Prompt changes must pass `evals/grader.yaml`.
**Why:** The spec's grader, with code guarding what a judge gets wrong most (crediting
mentions, quoting what was never said, crediting an examination never done).
**Instead of:** An Inspect scorer inside `run` (grading would need a re-run to tune); one judge
call per visit (long outputs, worse per-item attention); uncapped over-provision (it outweighed
a missed critical on the real runs).
**To undo:** About a day: the grader reads only saved logs and the case. Rethink the weights,
the cap and the over-provision examples after the clinical lead's read and the rater agreement in M5.
**By:** Agent, on the clinical lead's go for M3; weights and cap for him to confirm.

## 2026-11-04 — Simulator realism after run-1 review (agreed with the clinical lead)

**Decision:** Two questions, or a few closely related ones ("any pain or headache?"), get
answered. Three or more different questions at once get only the first one or two answered; the
rest are left, not denied, so the GP must ask again. (First version gave one blanket "no";
the clinical lead judged that read as lying, so it was softened the same day.) A chatty persona may make
short asides about everyday life or volunteered small talk, never a new clinical fact; the
checker allows them. A "volunteered" item is said once, repeated only if asked about again; no
phrase is reused. Every case scripts a standard history for each person (daily living, continence, stairs,
meals and shopping, help received, medicines, mood, alcohol, pain, wishes), so the simulator
rarely improvises. Full review notes: `docs/m1-transcripts/run1-review.md`.
**Why:** Run 1 had Edith repeat "I do all my own meals" six times, answer questions she was not
asked, and improvise daily-living answers the case did not cover. Real patients answer a list
of questions with a blanket "no", so stacking questions earns a realistic false negative.
**Instead of:** Always answering only the first question; a blanket "no" to every list.
**By:** the clinical lead (rules), agent (implementation).

## 2026-11-04 — Script fidelity, unlisted symptoms and exam sets (after the M2 read)

**Decision:** The simulated people may add harmless colour but no fact a GP could act on; that
keeps every model facing the same patient and lets the grader score against the script. When a
realistic question meets a gap ("who puts the eye drops in?"), the fix is a line in the case.
A symptom or problem missing from a person's script is one they do not have, or have not
noticed in the person they look after, so they answer routine negatives plainly; the checker
does not flag that. Exam findings can form a named set (`parts`): "obs" returns every part,
"pulse" only the pulse, and code turns ids from different examinations into "too broad".
**Why:** the clinical lead found "I couldn't say" to chest pain and "I couldn't tell you who puts them in"
unrealistic, and "pulse" returning the full observations wrong. 12 of 23 invented-fact flags
across the saved runs were routine negatives.
**Instead of:** A looser checker (models would meet different patients); scripting every
negative in each case (long, and still incomplete).
**By:** agent, from the clinical lead's review notes.

## 2026-11-04 — [arch] Multi-visit runs (M2)

**Decision:** `run_case` (case_run.py) runs a case's visits in order. Each visit starts a fresh
clinician context. `Memory` sets what carries over: `notes` (default: its own earlier plans in
the briefing, plus a short dated "GP (you)" entry per earlier visit in the GP record),
`transcripts` (its earlier consultations: what it said, heard, read and found, and its plan) or
`none`. Each person gets the spoken conversation of the visits they were at, and so does the
checker; asked whether something arranged then has happened, a person who has no fact on it
has not heard. Between-visit events stay fixed, so plans never change the records. One Inspect
sample is one case run; the stored `CaseLog` keeps each `VisitLog` apart for per-visit grading.
`run CASE` runs all visits; `--visit N --from saved.json` runs one later visit for development.
**Why:** The spec's visit loop (build-v0.md item 4), approved by the clinical lead on 4 Nov. A real GP
finds its own earlier entry in the record; a daughter remembers what the GP told her.
**Instead of:** One Inspect sample per visit (loses the case as the unit of scoring and the
carry-over); simulators with no memory (Janet would not know what the GP had said).
**To undo:** About half a day: drop case_run.py and call `run_visit` per visit again. Rethink
if the grader needs visit-level samples, or plans need to change later records (v0 has none).
**By:** agent.

## 2026-11-04 — [arch] Records written out as documents

**Decision:** A case may give each record a `documents` entry: the record as it would look
(a cluttered coded GP record, a templated agency log, a discharge summary), with `[[fact_id]]`
where each graded fact sits and `{day:-21}` or `{weekday:-9}` for dates relative to visit 1.
Rendering drops lines naming a fact that does not apply yet and lines dated after the visit.
Visits gain `day` (visit 1 is day 0, rendered as Thursday 5 November 2026). New record type
`ambulance_report`. A twin reuses the base's documents with its own facts in the same slots and
may override a record's document. The validator checks every record fact appears exactly once,
every slot names a fact, dates parse, and a fact's line is not dated after the visit it applies
to. The examiner now sees the setting; weighing on a home visit is "not available".
**Why:** the clinical lead's review: real records are long and noisy, agencies write rosily from
templates, handwritten discharge summaries say "postural hypotension" without numbers, and
paramedics usually see a patient found on the floor. Facts stay atomic for grading; only
presentation changed. Case files stay free of absolute dates.
**Instead of:** Free-text records (the grader would lose fact ids); absolute dates in case files
(breaks the fictional-content check).
**To undo:** About half a day: drop `documents` and records fall back to bullet lists of facts.
Rethink if authors find slots too fiddly to write.
**By:** agent.

## 2026-11-04 — Investigations, findings rule and kept-back slips (agreed with the clinical lead)

**Decision:** `examine` treats investigations (bloods, ECG, imaging) differently from bedside
examinations: unlisted ones return "not available during this visit, request it in your plan";
unlisted examinations still return "unremarkable", so a case must list every abnormal finding
its truth implies plus basic observations (`docs/case-template.md`). If a simulator reveals a
kept-back fact before its condition is met and its rewrite does too, it gets one last draft
with that fact removed from its script. The checker judges reveal conditions by meaning, with
a live test set (`evals/checker.yaml`) so earned facts are not hidden. Deferred to after the
pilot: weighting actions by real time, and results that arrive later.
**Why:** M1 runs showed the harness inventing a normal ECG that the model then relied on, a
kitchen check contradicting the truth, and kept-back facts reaching the clinician unearned.
**Instead of:** a fixed "I'm not sure" line after a slip (reads oddly as a reply).
**By:** the clinical lead (rules), agent (implementation).

## 2026-11-03 — Visit loop rules (M1)

**Decision:** The clinician's prompt states the visit's turn budget. Every action costs a turn,
including a reply with no tool call, bad arguments or speaking to someone absent; the error goes
back to the clinician. At the budget it is told to submit; at 2× the budget the visit ends with
no plan (logged, graded later). `examine` maps the request to the case's findings with the cheap
checker model (an exact label skips the call); an unlisted specific examination is
"Unremarkable", a broad one ("full examination" or a list of several) is told to name one.
Prompt changes to the matcher must pass `evals/examiner.yaml` (requests taken from M1
transcripts). The checker runs at medium effort: at low it mismatched findings. Simulators get the spoken
conversation as plain text, never records, examinations or tool calls.
**Why:** Bounds cost without making the budget a hard wall, stops a "full examination" from
revealing every finding in one turn, and keeps simulators blind to the clinician's tools.
**By:** agent, for the clinical lead to check in the M1 transcripts.

## 2026-11-03 — [arch] Case file format and validator rules (M0)

**Decision:** One YAML per case (`cases/<set>/<id>.yaml`, file name = id), validated by `clinical-env validate`. The rubric is a top-level list with a `visit` on each item. A twin is its own file with `twin_of`, `views` and `rubric` only; truth, personas and visits come from the base, and conflicts are empty. Validator rules beyond the spec: records carry no disclosure (reading shows the whole record); every wrong or outdated fact must sit in a conflict; each conflict has at least one wrong or outdated fact, and its truth list covers every fact in it; a fact cannot start before the truth it describes, and a true fact cannot outlive it; each person's fact must apply at a visit where that person is present; only must_do and red_flag items can be critical; a twin's criticals are exactly the base's clinical_action criticals, unchanged (so 1–4); strings shaped like NHS numbers or absolute dates are rejected (cases use relative times).
**Why:** Inheriting the twin's truth and visits means they cannot drift from the base, so the mechanism check compares like with like. The extra rules catch authoring mistakes that would silently weaken a case.
**Instead of:** A full duplicate twin file checked field by field (more to write, can drift); the rubric nested inside each visit (would force a twin to copy visits).
**To undo:** Under a day while there are few cases: change the schema and convert the YAML. Rethink if a twin genuinely needs different visits or events.
**By:** Agent, within the approved M0 plan.

## Earlier decisions (migrated from docs/decisions.md)

| Date | Decision | Why |
| --- | --- | --- |
| 2026-11-01 | Don't build our own model | Capital-heavy; the frontier keeps moving. Baichuan's gains came from the simulator and rubrics |
| 2026-11-01 | We are an environment company: simulator, tools and grader as one harness | Our edge is task and grader design |
| 2026-11-01 | Kill rule: if frontier models already handle these cases well, stop | The pilot exists to find out |
| 2026-11-01 | A second GP rates the same cases blind | Reduce rubric bias |
| 2026-11-01 | AMIE Mx is proof of demand, not ground already taken | It has no carers, no function focus, no conflicting records |
| 2026-11-03 | No public code for ResidencyRL or AMIE Mx. Build our own, copying ResidencyRL's published design | Both closed; methods are described in detail |
| 2026-11-03 | Use the clinical lead's own OpenAI and Gemini keys, not OpenRouter | He already has them and credit. Updated 3 Nov: an Anthropic key is added and Gemini needs billing for Pro/flagship models |
| 2026-11-03 | Claude Code is the home for this project; docs/decisions.md is the shared memory | Chat threads go stale. Superseded 3 Nov by the project-memory entry above |

## 2026-11-05 — Pre-registered: negative-workup test and Stop rule

**Decision:** Before the cases exist, two dev cases are written where the obvious workup
comes back negative: a classic cancer picture with a clear scan, and a bleeding picture with
negative scopes (the clinical lead gives 3-5 lines each from clinical experience, fictionalised; the agent
writes them as 3-visit cases). Criticals cover what to do after the negative result: no false
reassurance and discharge, no reflex next big test without a new feature, back to the common
causes, a dated re-review with safety-netting, and explaining the uncertainty. The clinical lead checks
the criticals before any run. Run: gpt-6-astra, high effort, 3 runs per case (6 runs), dev
simulators and grader, every critical verdict confirmed by the clinical lead.
- **Stop** the "frontier models fail" thesis if astra meets every critical in all 6 runs.
- **Go** (pilot cases written in this style) if the clinical lead confirms a critical miss in 2 or more
  of the 6 runs.
- Exactly 1 confirmed miss: 3 more runs per case; Go only with 3 or more misses in 12.
- Both cases stay in the set whatever the result; criticals are not changed after the runs.
**Why:** The 4 dev cases are black and white: the test the model orders confirms the
suspicion, and astra met every critical in all 12 runs. Real older-adult care often turns on
a negative result and base rates (most cancer-looking pictures have clear scans), where AI
tends to over-weight the rare serious diagnosis. The case type comes from clinical reality,
not from what models get wrong; fixing the rule first keeps it from being tuned to the result.
**By:** the clinical lead (go), agent (wording).

## 2026-11-05 — Negative-workup result: Stop on "frontier models fail"

**Decision:** Under the rule pre-registered earlier today, the negative-workup test is 0 of 6
runs with a confirmed critical miss, so Stop. The clinical lead reviewed Dot's three visit-3 flags. The
flagship chased the urgent GI referral it made at visit 1, and the case never recorded that
referral's outcome; the guidelines still advise the first-line GI assessment. He judged them
not real misses, and Dot's visit-3 mark scheme now allows chasing the first-line assessment
(regraded: all met). Together with the 4 dev cases x 3 runs, gpt-6-astra met every critical in
18 of 18 runs. Go is off the table. The next chat decides whether to pivot or stop completely.
**Why:** The kill rule (1 Nov) and the pre-registered Stop rule both point here. The
flagship's consistent weaknesses (agenda and ideas, concerns and expectations, local service
routes, some over-investigation) are real but not critical, and a prompt could likely fix
them.
**By:** the clinical lead (verdict and direction), agent (record).


## 2026-11-06 — Pre-registered: people-not-paper test and rule

**Decision:** One test of the last live thesis (`docs/pivot-options.md`): frontier models
reconcile documents well but miss a plan-changing fact held only by a person. Cases (agent's,
built on CC BY case reports, the clinical lead reviews after the runs): `cases/dev/reg_holloway.yaml`
(his wish to stay at home, never asked by the hospital) and `cases/dev/pat_ellison.yaml` (the
carer's knee replacement in under three weeks), plus `cases/dev/pat_ellison_twin.yaml` (the
same fact also written in the GP record). Run: gpt-6-astra, high effort
(`config/models-feasibility.yaml`), 3 runs of each (9 runs), dev simulators and grader.
- People-only criticals: `reg_holloway` `v1_wishes` and `v1_acp`; `pat_ellison`
  `v1_carer_cover`. The other criticals are reported but do not count.
- **Pivot** to "people, not paper" if the clinical lead confirms a people-only critical miss in 2 or more
  of the 6 base runs **and** the twin meets `v1_carer_cover` in 2 or more of its 3 runs.
- **Stop completely** otherwise. Misses with the twin also missed mean the gap is not
  elicitation, so they do not count as a pivot either.
**Why:** In 18 dev runs the flagship always found hidden facts the clinical picture pointed to
(Dot's Nurofen, Ray's weight), but never asked the agenda or ICE. This asks whether that gap
ever changes the plan. Fixing the rule before the flagship runs keeps it from being tuned.
**Known weakness:** visit-1 smoke runs on the cheaper dev clinician (gpt-6.1-sol) came first.
It met all three people-only criticals: it asked Reg "what matters most to you now" and asked
Ken about his own health after Pat said his leg was bad. The criticals were not changed after
that; only Ken's missing standard-history lines were scripted (realism fix, logged in the case
notes). So Stop is the expected result.
**By:** the clinical lead (go), agent (cases and wording).

## 2026-11-06 — People-not-paper result: stop completely (rule)

**Decision:** Under the rule fixed at 326bb61, gpt-6-astra met every critical in all 9 runs
(Reg 3, Pat 3, Pat's twin 3), so 0 of 6 base runs with a people-only miss: **stop completely**.
It found Reg's wish by asking what mattered most (3 of 3) and Ken's operation through Pat's
"his leg's bad" (3 of 3). Details: `docs/feasibility-dev.md`.
**Why:** The thesis needed the flagship to miss a plan-changing fact held only by a person; it
follows any realistic cue. Its remaining gaps (agenda, ICE, carer's assessment) lower scores but
did not change a plan in 27 dev runs.
**By:** rule pre-registered (the clinical lead go, agent wording); ending the project is the clinical lead's call.

## 2026-11-06 — Pre-registered: noise test

**Decision:** the clinical lead's point after the people-not-paper result: thin text cases give the
answer away, because every detail is a signpost (a lone limp gets noticed). Test it on one case:
`cases/dev/pat_ellison_noise.yaml` is `pat_ellison` with the same truth, criticals and reveal
conditions, plus realistic clutter: a busy lounge, a bruise from the roses, hearing aids,
builders next door, chatty asides from both, and a long GP record. Ken's limp and Pat's "his
leg's bad" keep their wording, buried among the rest. Run: gpt-6-astra, high effort, 3 runs, dev
simulators and grader; compare with `pat_ellison` (3 of 3 met).
- **Noise matters** if the clinical lead confirms a `v1_carer_cover` miss in 2 or more of the 3 runs. Then
  a bigger noise test (more cases, matched clean and noisy pairs) is worth proposing.
- **Otherwise** the salience thesis is not supported at this level of noise, and stop stands.
**Known weakness:** one visit-1 smoke run on the dev clinician came first. It noticed the stick
in the long home description ("I notice you use a stick") and met the critical. Nothing was
changed after it.
**By:** the clinical lead (idea and go), agent (case and wording).


## 2026-11-06 — Noise result: stop stands (rule)

**Decision:** gpt-6-astra met every critical in all 3 runs of `pat_ellison_noise`, so 0 of 3
`v1_carer_cover` misses: the salience thesis is not supported at this level of noise and stop
stands. In 2 of 3 runs it asked about Ken's own health or who could help without using any cue,
and it never mentioned the bruise. Details: `docs/feasibility-dev.md`.
**By:** rule pre-registered (the clinical lead go, agent wording).


## 2026-11-06 — Stop the project

**Decision:** Stop clinical-env. Both pre-registered rules (people-not-paper, noise) said stop,
on top of the earlier Stop; 30 of 30 flagship runs met every critical.
**Why:** Frontier models do not fail this task on fair cases; the gaps found cost points, not
plans. Case reports cannot supply the failures.
**Instead of:** Pivoting to UK local routes (C) or consequences (D).
**To reopen:** a model class that fails these cases, a buyer for the harness as a training
environment, or real consultation data. Close-out: `docs/close-out.md`.
**By:** the clinical lead (decision), agent (write-up).


## 2026-11-06 — Pre-registered: thin-harness test

**Question:** are the flagship's consistent non-critical misses fixed by a thin, generic
harness (a few lines of consultation and review guidance), or are they deeper?
**Setup:** `config/harness-thin.md` appended to the clinician prompt (`run --harness`). Every
line applies to any older-adult visit; it names nothing from these cases. gpt-6-astra, high
effort, 3 runs each of Pat (UK), Dot (UK), Walt (US); same simulators, checker, grader and case
files as the baseline runs. Local routes are out of scope (they need data, not a prompt).
**Measured against the baseline (all 0 of 3 without the harness):**
- Pat `v1_urgency_plan` (donepezil considered as a cause of the urgency).
- Pat `v1_carer_assessment` (assessment and carers register).
- Walt `v1_stool_test` (FIT or similar in the first tests).
- Dot `v1_examine` (rectal examination offered).
An item is fixed if met in 2 or more of its 3 runs, after the clinical lead's spot-check of these 4
verdicts (his overrides count).
**Rule:**
- 3 or 4 fixed: the gaps are prompt-deep; no business in them; the stop stands.
- 0 or 1 fixed: a real gap; write up the unfixed misses as the candidate and discuss.
- 2 fixed: partial; report both sides and discuss.
**Reported, not in the rule:** agenda (`c_agenda`) and ideas, concerns, expectations
(`c_ice`), pooled over the 24 visits (baseline 0 of 24 each), fixed at 16 or more; any
critical missed with the harness (a harm the harness caused); scores against baseline.
**Not changed after seeing results.**
**By:** the clinical lead (go), agent (harness text and wording).


## 2026-11-07 — Thin-harness result: partial (rule)

**Decision:** 2 of 4 clinical items fixed (Pat donepezil 3 of 3, Walt stool test 2 of 3; Pat
carers register and Dot rectal examination 0 of 3), so the rule says partial. Agenda 22 of 24 and
ICE 24 of 24 visits with the harness (0 of 24 each without). Every critical met in all 9 runs.
**Reading:** the one reasoning miss and the consultation gaps are prompt-deep; what is left is
UK practice convention. This does not reopen the project; the shelving and public write-up go
ahead. The clinical lead's spot-check of the 4 verdicts is pending and could move the count.
Details: `docs/feasibility-dev.md`.
**By:** rule (the clinical lead go, agent wording).


## 2026-11-07 — Spot-check of the four thin-harness verdicts

**Decision:** The four clinical verdicts stand; the result stays **partial** (2 of 4 fixed).
**What was checked:** each grader verdict and its quote against the raw plan text of all 12
runs (`runs/harness/`, not committed), plus a text search of every plan for the key terms.
- Pat donepezil as cause of urgency: met 3 of 3, quoted in each plan.
- Walt stool test: met in runs 1 and 2 ("arrange ... FIT"). Run 3 says "discuss stool blood
  testing" among the first tests; the grader marked it not met. Borderline, and the item is
  fixed either way (2 of 3 or 3 of 3).
- Pat carers register: 0 of 3. The word "register" appears in none of the three plans.
- Dot rectal exam: 0 of 3. Rectal bleeding appears only in safety-netting; the plans are
  FIT-led referrals.
**Finding:** current NICE NG12 (2023, 1.3.1 to 1.3.5) says to offer FIT in iron-deficiency
anaemia and mentions rectal examination only for a rectal mass; the BSG 2021 guideline (Gut
70:2030, full text searched) does not recommend a digital rectal examination. A 2015 NICE
appendix did list abdominal and rectal examination. Dot's item `v1_examine` therefore reflects
older practice. It is a rubric question, not evidence of a gap.
**Open for the clinical lead:** keep or drop the rectal-exam wording of `v1_examine`. Not changed here.
**By:** agent (pass), the clinical lead (clinical call on `v1_examine`, pending).


## 2026-11-07 — Pre-registered: reference-document test (carers register)

**Question:** the thin-harness test left one gap that looked like missing local knowledge:
Pat's carer, Ken, is never added to the carers register (0 of 9 baseline, 0 of 3 thin
harness). If the model is given real published UK documents on carers, does it add him? If
yes, the gap is a retrieval problem and not a model failure.
**Setup:** Pat (UK), gpt-6-astra high effort, 3 runs, same simulators, checker, grader and case
file as before. Clinician prompt = `config/harness-thin.md` plus two real documents in full:
NICE QS200 quality statement 1 (identifying carers) and the NHS Thames Valley ICB page
"Registering as a carer". The documents are in the prompt, so this is a best case for
retrieval (an upper bound), not a test of finding the right document. Source texts are not
committed (publisher copyright); `sources/reference/MANIFEST.md` has URLs, dates and hashes.
**Measured:** `v1_carer_assessment` (offers a carer's assessment and adds Ken to the carers
register), against 0 of 3 with the thin harness alone.
**Rule:**
- Met in 2 or more of 3 runs: the gap is a retrieval problem; local practice convention
  needs data, not a better model.
- Met in 0 or 1 of 3: documents in the prompt do not close it; the gap is about applying
  knowledge, a stronger lead; discuss.
**Reported, not in the rule:** whether the plan cites or paraphrases the documents; any
critical missed (a harm from the extra text); scores against the thin-harness runs.
**Dot's rectal-exam item is not re-run:** the documents that matter (NG12, BSG 2021) do not
ask for it, so a retrieval test would only confirm that the model follows them.
**Not changed after seeing results.**
**By:** the clinical lead (go, 7 Nov), agent (wording).


## 2026-11-07 — Reference-document test result: fixed by the rule, with a critical lost

**Decision:** By the pre-registered rule (carers register in 2 or more of 3 runs) the gap is a
**retrieval problem**: given two real UK documents on carers, the model acted on the convention
it had never applied (0 of 9 baseline, 0 of 3 thin harness). It does not reopen the project.
**Numbers (Pat, gpt-6-astra high, 3 runs, rule at cf9ec59):**
- `v1_carer_assessment` (carer's assessment and carers register): met 2 of 3 by the grader.
  Registration appears in all 3 plans (run 1 "re-offer consent-based carer registration", run 3
  "offer help with GP carer registration", run 2 "record Ken as Pat's unpaid carer"); 0 of 3
  plans mentioned it with the thin harness alone.
- **Critical `v1_carer_cover` missed in 3 of 3 runs** (met 3 of 3 with the thin harness; 12 of
  12 across all earlier Pat runs). Case score 41, 64, 73% (thin harness: 73, 82, 82%).
  Also lower: `c_safety_net` 2 of 3, `v1_door` 1 of 3, `c_summarise` 2 of 3 (each 3, 2, 3 of 3
  before).
**What happened:** Ken is reluctant about social care in every Pat run. With the thin harness alone the model
answered his reluctance and got his agreement to an urgent assessment (3 of 3).
With the documents, which stress consent and the carer's own choices, it pressed once,
then settled for a care-coordinator call the next day, and told him to contact the council if
cover failed. (Wording corrected 7 Nov: an earlier draft said it accepted the refusal.) The grader counted that as no cover arranged.
**Caution:** 3 runs on one case; Ken's wording varies by run, so the document effect is not
separable from chance with this n. The documents are in the prompt, an upper bound for
retrieval. The three critical verdicts need the clinical lead's review, as every flagged critical does:
whether deferring to a competent carer's refusal with a safety net is a failure is his
clinical call. Dot's rectal-exam item was not re-run (see the spot-check entry).
**Reading:** local practice knowledge is data, not capability, and adding data is not free:
the same text that fixed the convention coincided with a worse call on the case's main
safety issue.
**By:** rule (the clinical lead go, agent wording).


## 2026-11-07 — Pre-registered: context-sensitivity test (10 vs 10)

**Question:** does adding relevant documents to the prompt move a safety-critical decision?
The 3-run reference test went from carer cover met 3 of 3 (thin harness) to 0 of 3 (thin harness
plus documents). Within every earlier condition, no critical flipped between runs (0 of 27
item groups), so a shift between conditions would be sensitivity to context, not randomness.
**Setup:** Pat (UK), gpt-6-astra high effort, same simulators, checker, grader and case file.
Arm A: `config/harness-thin.md`, 10 new runs. Arm B: `sources/reference/harness-thin-carers.txt`
(sha256 0f225fcd833f, the same file as the 3-run test), 10 new runs. Both arms run the same
day; the earlier 3 + 3 runs are reported separately, not pooled.
**Primary measure:** the grader's `v1_carer_cover` verdict, rubric unchanged.
**Rule:**
- Confirmed: arm B meets it less often than arm A, two-sided Fisher exact p < 0.05 (for
  example 10 vs 5 or fewer, 9 vs 3 or fewer).
- Not replicated: the arms differ by 2 runs or fewer.
- Anything between: inconclusive; report the numbers, claim nothing.
**Secondary, reported, not in the rule:** each run's visit-1 cover decision, classified by the
agent from the plan and closing turns with arm labels hidden: (A) referral to adult social care
or an urgent social-care or carer's assessment arranged or agreed; (B) a dated next step towards
cover (care-coordinator call, GP call or visit to plan it) without a referral; (C) safety-net
only. This tests the lenient reading the clinical lead raised (a coordinator call as "starting to arrange
care"). Also reported: carers-register item, case scores, other critical misses.
**Spend:** about $35–45 estimated (20 runs and grading); approved by the clinical lead in chat, 7 Nov.
**Not changed after seeing results.**
**By:** the clinical lead (go), agent (design and wording).


## 2026-11-07 — Context-sensitivity result (10 vs 10): not replicated

**Decision:** By the rule (rule at bdb72fd), the documents do **not** move the critical: Pat's
`v1_carer_cover` met 9 of 10 with the thin harness and 8 of 10 with the documents (Fisher
p = 1.0). The 0 of 3 in the first reference test was a bad batch: at a true rate of 8 of 10,
three misses in a row has about a 1% chance, so it was either unlucky or something correlated
within that batch; this test cannot say which.
**Secondary (blind agent read, arm labels hidden):** every run took a dated step towards cover
(none C). Referral or urgent assessment that day (A): 9 of 10 thin, 6 of 10 documents. A dated
softer step, usually a care-coordinator call, instead (B): 1 of 10 thin, 4 of 10 documents
(p = 0.30, within chance). The grader failed 3 of the 4 B runs and passed 1, so it is not
fully consistent on the softer step either.
**Carers register (`v1_carer_assessment`):** 0 of 10 thin vs 6 of 10 documents (p = 0.011).
The documents fix the convention, confirming the 3-run result.
**Scores:** thin 32 to 86% (median 77), documents 59 to 91% (median 77). No other critical missed.
**Reading:**
- Local practice knowledge is a retrieval problem; the side-effect scare did not hold up.
- The cover decision is not deterministic: the same model, prompt and case refers that day in
  most runs and settles for a coordinator call in others. Across every earlier 3-run condition no
  critical flipped (0 of 27 item groups); with 10 runs, this one flips in both arms. Three runs
  per case is too few to see a 10 to 20% miss rate.
- Whether a dated coordinator call meets "starts arranging care" is the clinical lead's call. In chat he
  said it could count; the verdicts are not overridden until he reviews them.
**Spend:** about $35–45 estimated for 20 runs and grading, as approved; not billed separately.
**By:** rule (the clinical lead go, agent wording); classification by agent.
