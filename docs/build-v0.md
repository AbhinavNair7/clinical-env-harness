# Build v0 spec

v0 answers one question: do frontier models fail at managing a complex older adult across visits when the patient, carer and records disagree? It is a small Python harness, 10 frozen pilot cases (plus one pre-registered extension of 10), and a grader checked against clinicians. This is a starting spec. Propose changes and log agreed ones in `DECISIONS.md`. Last updated 4 Nov 2026 with the agreed changes from the plan review (`DECISIONS.md`, "Plan review: agreed changes").

## Scope

| In v0 | Waits until after the pilot |
| --- | --- |
| Patient and carer simulators, each seeing only its own version of events, with persona-driven interjection | Consequences that branch on the model's decisions |
| Records that can disagree: GP record, care agency notes, discharge summary, pharmacy or dosette record | Automatic case generation |
| Examination findings the clinician can elicit during a visit | Packaging for Prime Intellect's verifiers library and hub |
| 2 to 3 visits per case, with fixed events between them | Narrow slices (e.g. referral triage) scored on one stage's criticals; v0 only tags the stage |
| A clinician harness any model plugs into through one adapter, plus a human adapter and (M4) an HTTP adapter for an outside agent | Any RL training |
| A grader with weighted critical items and penalties | A web product or dashboard |
| Readable transcripts and a blind rating export | Actions weighted by real time (a postural BP costs more than a question); v0 counts every action as one turn |
| | Turnaround times for investigations (a CT in weeks, bloods in hours); since 5 Nov a test ordered at one visit is back by the next (`Visit.results`) |

## Hard rules
- All case content is fictional. Never commit real patient data.
- Private GitHub repo. API keys in `.env`, never committed.
- Python. Keep the core (case schema, simulators, visit loop, grader) independent of any eval or RL framework so it can be wrapped for verifiers later.
- Every model call goes through Inspect AI's model API, so models are swapped by config and model role. Log tokens and cost per call.
- Every run saves a full transcript, including tool calls, examinations, interjections and simulator check flags.

## Components

1. **Case files.** One YAML per case, validated against a schema.
   - hidden_truth: the real state at each visit (mobility and aids, falls, ADLs, cognition, medicines actually taken, care actually delivered, carer strain, risks)
   - views: what each source believes. Sources: patient, carer, gp_record, care_agency_notes, discharge_summary, pharmacy_record, ambulance_report. Each fact has an id, links to a truth item, and is marked true, wrong or outdated. Each fact is also marked volunteered, if_asked, or hidden. A hidden fact carries a one-line reveal condition (the question that earns it), which the checker uses
   - documents (optional): each record written out as it would look, with `[[fact_id]]` slots and dates as day offsets from visit 1 (`{day:-21}`); visits carry a `day`
   - personas for patient and carer: cognition, health literacy, agenda, how they talk, whether they interject when the other is addressed (always, sometimes, never), and messiness `traits` (denies_minimises, tangents, poor_recall, carer_dominates). A carer only where realistic: about half to two thirds of pilot cases
   - country: `uk` or `us`; every word a model reads about the health system follows it (`locale.py`), and criticals stay country-neutral
   - messiness: each case is `mild`, `moderate` or `high` (Edith: moderate), and records carry `record_traits` (contradicts_other_records, contradicts_itself, miscoded, long_noisy, outdated_entries), checked against the facts. The pilot set aims for a spread: some cases with one stale medicine, some with a full contradiction, one or two nearly clean, so the test is not all traps
   - results (optional per visit): what each test would show if ordered at that visit; back by the next visit, unlisted tests normal. Every critical lists `evidence`, at least one earned (asked, examined, tested or after visit 1)
   - conflicts: the fact ids that disagree, what is true, and the expected clinician behaviour
   - visits: setting (home visit, phone, clinic), who is present, turn budget, events since the last visit, records available, record updates, examination findings available at that visit
   - events between visits must be plausible whatever plan was made at the previous visit (for example "the pharmacy never actioned the change"), so fixed events never punish good care
   - rubric per visit: must_do items with weights and a critical flag; must_not_do items (harm, over-provision, acting on a wrong fact); red flags. **2 to 4 critical items per case** (at most 5 in a 3-visit case that genuinely needs it: The clinical lead, 5 Nov), each something a GP would be criticised for missing (or, for a must-not-do, for doing). Each critical item is tagged `clinical_action` (needed whatever the sources say, e.g. stop furosemide and get the dosette changed) or `discrepancy_detection` (exists only because sources conflict), and with its consultation `stage` (intake, triage, history, records, examination, plan, follow_up) so a case can later run as a narrow slice. Most cases should have a critical that a do-everything plan fails (an unnecessary admission, an inappropriate new drug, over-investigation), as a must-not or in the wording of a must-do; not enforced per case (the clinical lead, 4 Nov)
   - optional twin: a consistent-sources version of the same case. Same personas, truth, visits and `clinical_action` criticals, but every source is accurate and the problem is in plain view. Stored as its own file with `twin_of`, holding only views and rubric; truth, personas and visits are inherited from the base. The validator rejects a twin with any wrong or outdated fact
2. **Simulators.** A patient agent and a carer agent, following ResidencyRL section 3.2.2.
   - one model call per turn; each sees only its own view, persona and the conversation so far
   - answers the question actually asked; two or a few related questions get answered, three or more different ones only the first one or two (the rest not denied); chatty personas may make harmless asides; a volunteered item is said once; replies under about 50 words
   - may be vague, minimise or contradict others, as its persona and traits say; anything wrong it says is a scripted fact, so every model meets the same person
   - when both are present, the party not addressed gets one cheap call after each reply to interject (30 words or fewer) or stay silent, as its persona's interjection setting says
   - never sees the clinician's tool calls, examinations, notes or the rubric
   - a checker call reviews each reply against the speaker's view and flags invented facts, hidden facts revealed without their reveal condition being met, or over-cooperation. Regenerate once on a flag; if a kept-back fact slips out again, one last draft with that fact taken out of the script; log every flag
3. **Clinician harness.** The model under test plays the clinician through four tools:
   - say(to: patient | carer, message)
   - read_record(name)
   - examine(what): returns the finding written into the case for this visit; a bedside examination or observation not listed returns "unremarkable" (so the case must list every abnormal finding its truth implies); an investigation not listed (bloods, ECG, imaging) returns "not available during this visit, request it in your plan"; on a phone visit returns "not possible"
   - submit_plan, which ends the visit: problem list (no forced single diagnosis), function and ADL summary, risks, actions (type, detail, rationale, urgency; types include medication change, referral, care package change, equipment, investigation, safeguarding, carer support), discrepancies found and how resolved, follow-up interval, safety-netting
   Each tool call counts as one turn against the visit's turn budget. Put the clinician behind an adapter interface. Build the LLM tool-calling adapter and a human adapter (a person plays clinician in the terminal or browser) for case QA and the human baseline. Human runs use the same transcript format with run type `human`, an anonymised participant ID, role, grade and a consent flag, and are never pooled with model scores. M4 adds an HTTP adapter so an outside agent (a company's own harness) can play clinician.
   Harness tiers in v0: the bare model, and the bare model plus a frozen, generic good-practice "thin prompt" (comprehensive geriatric assessment domains: read all records first, note and resolve source disagreements, ask about function, falls and the medicines actually taken, hear the patient as well as the carer, review the previous plan at follow-up, safety-net; no case content, checked by a second rater for hints). A stronger harness (forced reconciliation step, checklist) comes later.
4. **Visit loop.** A case runs all its visits in order, each with a fresh clinician context. Between visits the clinician gets its own earlier plans as notes plus the updated records, not the old transcripts (`--memory notes`, the default; `transcripts` and `none` are the alternatives). Its earlier consultations also appear as short dated entries in the GP record. Each patient or carer remembers the spoken conversation of the visits they were at; if asked whether something arranged then has happened and the case does not say, they have not heard. Events between visits are fixed in the case for v0, so no plan changes the records. One Inspect sample is one case run; the log keeps each visit apart for grading.
5. **Grader.** Clinical points from the clinical lead's transcript reviews that the grader must judge (proportion, UK pathways, one question at a time, ideas/concerns/expectations, reading records first) are listed under "Score in M3" in `docs/m1-transcripts/run1-review.md`.
   - one judge call per rubric group, structured JSON output; each item met or not met, with an evidence quote
   - deterministic checks from the logs where possible (did it read the agency notes, did it speak to the carer, did it examine postural BP)
   - penalties for invented facts in the plan, acting on a wrong fact, must_not_do items, over-provision, and exceeding the turn budget
   - a mention earns no credit unless it is an action with a rationale (rubric padding is a known failure)
   - judges are strong models (not the cheap simulator models) from two labs; each tested model's primary score comes from a judge outside its own lab; report both judges and their agreement
   - grading of visit 2 onwards sees the clinician's earlier plans, and scores whether it followed up its own plan (`c_follow_up_plan`)
   - scorecard per visit and per case
   - built in M3 as `clinical-env grade <case.yaml> <run.json>...` (see `DECISIONS.md`, "Grader (M3)"): rubric items may say what the log must show (`requires`: examined, read, spoke_to); consultation-quality points live in `rubrics/consultation.yaml` and score apart from the case; over-provision costs 1 per action, at most 3 per visit
6. **Runner and report.** Inspect AI runs cases × models × runs (epochs) with concurrency, retries, caching and a cost cap, and its viewer shows every transcript in a browser. A small static case view on top of the Inspect logs shows each transcript beside its sources, highlights the conflicts, and puts grader verdicts beside their evidence.
7. **Blind rating.** Export runs with model names hidden and order shuffled to a self-contained HTML rating form (opens in a browser, no install, saves a CSV). Raters score each critical item met or not met, plus one overall 1 to 5 rating per transcript (about 8 to 10 minutes each). Agreement statistics: raw agreement, Gwet's AC1 and Cohen's kappa per critical item; ICC for overall ratings; grader against raters.

## Milestones
Before each milestone, a plan of 10 lines or fewer; build after the clinical lead says go. Commit at each one and tell the clinical lead what changed.
- **M0** Package, case schema, validator, Edith Marsh test case, thin Inspect layer with model roles
- **M1** One visit end to end with both simulators, interjection, examine and the human adapter. **Stop** and show the clinical lead two full transcripts
- **M2** Multi-visit
- **M3** Grader
- **M4** Batch runs, cost tracking, case view report, HTTP clinician adapter, thin-prompt tier, frozen pilot config (simulators never OpenAI; judge from another lab)
- **M5** Blind rating export and agreement stats

## Pilot and failure criteria (agreed 3 Nov, revised 4 Nov; freeze in a commit before the first real run)
- Purpose: an internal go/stop gate. Its miss rate is never quoted outside the team. A percentage becomes a sales metric only on a separate private set of about 30 cases, written after the pilot. The lead sales asset is 3–5 annotated failure transcripts, each tied to a critical a GP would call unsafe.
- Cases: 3 dev cases (Edith plus two) for tuning, never scored. 10 pilot cases, frozen and never seen during tuning. One pre-registered extension of 10 more. Aim for a spread of messiness (mild, moderate, high, one or two nearly clean) and a carer in about half to two thirds.
- Critical review: before the freeze the clinical lead and a second GP review every critical and drop any that either calls idiosyncratic. Outside clinicians review after a Go.
- Models: the flagship of each of three labs at high effort (on 3 Nov: gpt-6-astra, claude-fable-5-1, gemini-4-argon). Re-check IDs on the day of freezing. Build and tune on cheaper models.
- Simulators: patient and carer run on one fixed open-weight model for the whole pilot, recorded in the freeze. If it does not read realistically on the dev cases, fall back to a fixed Claude or Gemini model plus a 3-case sensitivity rerun with a different simulator model. Never OpenAI (OpenAI alone can trigger Stop at step 1).
- Judges: from a different lab to the model being scored.
- Data: zero-retention API settings wherever available (Inspect sends OpenAI `store: false` by default). The frozen set is not published during the pilot; afterwards the pilot cases become the open pack and the private sales set is written fresh.
- Runs: 3 per case per model. A missed case: the model misses at least one critical item in 2 or more of its 3 runs, confirmed by a clinician, in transcripts where the simulator stayed on script.
- "Best model": the single model with the lowest miss rate across the whole set, not the best model per case. All three are reported side by side.
- Step 1, OpenAI flagship only: Stop if it passes 8/10 or more cases. Otherwise run Gemini and Claude.
- After all three labs, at 10 cases: Go if the best model has 4/10 or more confirmed missed cases; Stop if it passes 8/10 or more; in between (3/10 missed) triggers the one extension.
- At the pooled 20: Stop at 16/20 or more passing; Go at 8/20 or more missed. Tie-break for 5–7 missed: open, decide before the freeze.
- No editing frozen cases, criticals or prompts after seeing results. Case edits before the freeze fix simulator or realism bugs only, never difficulty, and are logged in the case file.
- Exclusions: only for simulator drift flagged by the checker, decided with model names hidden.
- Raters: The clinical lead and a second GP for the pilot; at least one confirming rater is not the case author. External raters are added after a Go, before anything reaches buyers.
- Human baseline: a GP colleague who is not a rater plays clinician on a few cases (number at the 10-case size: proposed in `DECISIONS.md`), chosen at random before the freeze, through the human adapter. Report the GP's miss rate beside the models'.
- Thin-prompt check (secondary, never in go/stop): rerun each missed case once with the frozen thin prompt and report how many misses survive. Separates shallow, prompt-fixable failures from real ones.
- Mechanism check (secondary, never in go/stop): a few pilot cases, chosen at random before the freeze, get a consistent-sources twin (number at the 10-case size: proposed in `DECISIONS.md`). Run each twin 3 times on the best model. A failure is attributed to the mechanism when a `clinical_action` critical is missed in at least 2 of 3 runs of the case and met in at least 2 of 3 runs of its twin.
- Population: older adults only. A population contrast waits until after a go (see `DECISIONS.md`, proposed).
- Reporting: the thresholds are a decision rule, not an estimate (4/10 has a 95% interval of about 12–74%). "Best model" is the lowest of three noisy miss rates, which biases towards stop.
- Grader usable: its agreement with raters is at least as high as the raters' agreement with each other.
- Freeze: cases, rubric, clinician and thin prompts, simulator model and these thresholds are committed before the first real run; record the commit hash in `DECISIONS.md`.
- Cost: about $2 to $12 per case-run at 3 Nov flagship prices; re-estimate for 10 cases in `DECISIONS.md` (proposed). Each batch over $20 is approved first.

## Test case (pipeline only)

Dev cases since 5 Nov: Edith Marsh (UK), and two US cases built on open case reports
(`docs/case-sourcing.md`): Marjorie Lindqvist and Harold Benning. The clinical lead reviews and edits
them instead of writing a dev case from scratch.

Edith, the first test case:
Edith Marsh, 84, lives alone with mild Alzheimer's disease. Her daughter visits weekly and says she is "managing fine". A care agency visits twice daily; its notes record missed medicines and one morning she was found on the floor. The GP record lists furosemide 40 mg, amlodipine 10 mg and donepezil 10 mg. A discharge summary from 3 weeks ago stopped furosemide after a fall with low blood pressure, but the pharmacy dosette still contains it. Edith says she has not fallen.
- Visit 1: home visit after the agency raises a concern.
- Visit 2: 14 days later, phone call with the daughter after a second fall.
- Critical items: reconciling medicines across all sources, a falls and function assessment, a care package review, and recognising probable delirium at visit 2 (asking the daughter what she has actually seen is a high-weight normal item since 4 Nov).

## Done for v0
the clinical lead can run 10 cases against 3 models × 3 runs with one command, read every transcript in a browser, see scores with evidence, and export blind ratings.
