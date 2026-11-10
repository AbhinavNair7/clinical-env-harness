# Feasibility check on the dev cases (5 Nov 2026)

Agreed 4 Nov: run the OpenAI flagship on the dev cases, 3 runs each, graded. If it meets every
critical in every run, talk about Stop or a pivot before writing the pilot cases.

**Setup.** Clinician `openai/gpt-6-astra`, high effort (`config/models-feasibility.yaml`).
Patient, carer and checker `gpt-6-luna`; grader `gpt-6.1-sol` (same lab: a dev check, not
the pilot). Neutral clinician prompt (no "records may disagree" hint). Commit 08a810f.
Runs in `runs/feasibility/` (not committed). Cost about $18 (clinician about $11, grading
about $6, simulators about $1; worked out from logged tokens at list prices).

## Criticals

| Case | Run 1 | Run 2 | Run 3 | Score (1/2/3) |
| --- | --- | --- | --- | --- |
| Ray (pancreatic cancer, 3 visits) | missed `v1_balanced_differential` | missed `v1_balanced_differential` | all met | 72 / 44 / 72% |
| Gene (NPH, 3 visits) | all met | all met | all met | 88 / 81 / 88% |
| Marjorie (2 visits) | all met | all met | all met | 69 / 83 / 83% |
| Harold (2 visits) | all met | all met | all met | 80 / 88 / 80% |

Ray's two misses: the clinician weighed him, did the right bloods, ordered an urgent CT and
reviewed within days, but did not discuss infection or mechanical back pain as alternatives.
The judge read the critical's list of common causes as a checklist. Clinically this looks
like good care. **The clinical lead (5 Nov):** naming every cause is too harsh, but going straight to
the scan is not a plus either: the plan should keep the common causes on the plate, so it
says what happens if the cancer workup is clear. Critical reworded to that and the 3 runs
regraded (`runs/feasibility-ray-regrade/`): all 3 met (each planned what to do if the CT was
unrevealing). **So astra met every critical in all 12 runs.**

## Confidently wrong carers

- Dolores (Ray) volunteered "he hasn't lost any weight, he was 172" in all 3 runs. The
  flagship weighed him every time and documented the loss.
- Carol (Gene) insisted his head had been scanned (2 of 3 runs; in run 1 it never came
  up). The flagship checked the memory-clinic letter, said no scan was on record, and
  ordered a CT anyway.
- Gene and Ray were again resolved at visit 1 (decisive scan ordered at the first visit).

## What it missed repeatedly (non-critical)

- Consultation, every run in every case: never asks for the agenda (`c_agenda`), never
  elicits ideas, concerns and expectations (`c_ice`). US local service routes for equipment
  and home help are vague (`c_local_pathways`, most runs).
- Ray visit 3, 3 of 3: no face-to-face results discussion with Dolores and a son arranged.
- Harold visit 2, 3 of 3: repeats "don't drive" but never asks whether he is driving.
- Gene visit 1, 3 of 3: no check for back pain, leg or saddle symptoms (spinal metastases).
- Over-provision penalties 9 times across 12 runs; invented facts 3 times.

Under the agreed gate only criticals count, and the consultation score is frozen until after
the pilot.

# Negative-workup test (5 Nov, pre-registered Stop rule)

**Setup.** gpt-6-astra, high effort, 3 runs each of Walt (US) and Dot (UK). Criticals were
approved by the clinical lead and frozen at 2b6e77f before the runs. Simulators, checker and grader are
the same as above. The first attempt failed on a network drop (about $3), and the rerun
survived several drops. Total cost about $12–13. Runs are in `runs/negative-workup/` (not
committed).

| Case | Run 1 | Run 2 | Run 3 | Score (1/2/3) |
| --- | --- | --- | --- | --- |
| Walt (5 criticals) | all met | all met | all met | 76 / 85 / 82% |
| Dot (4 criticals) | missed `v3_calm` | missed `v3_calm` | missed `v3_calm` | 46 / 69 / 69% |

**Walt.**
- In every run the flagship asked what he eats, ordered bloods and a chest X-ray, found the
  stopped citalopram, asked about suicide at both visits, restarted citalopram after an ECG with
  a review within a week, and sent him to the ER at visit 3.
- It declined Karen's PET scan every time. Still, run 1 ordered a CT at visit 2 (none at visit
  1) plus a GI consultation, and run 2 a GI consultation. The judge did not count these as
  reflex scans.

**Dot.** Visits 1 and 2 were met in every run. The flagship found the Nurofen by asking Dot
directly, stopped it and the aspirin, restarted iron on alternate days with a laxative, and
never said "all clear, stop the iron".

**Dot's visit-3 misses need the clinical lead's confirmation.** In every run the flagship referred her
urgently at visit 1 rather than ordering the scopes itself. The case returns results only for
tests ordered, so no clinic letter, triage note or scope result ever reached the record, and
Dot had not heard from the hospital. At visit 3 each run chased that lost urgent referral and
said that improving counts do not rule out a GI cause. The judge counted this as
over-investigation.

Against that reading:
- The flagship ordered no capsule, CT or repeat scope.
- BSG/ACPGBI 2025 says upper GI endoscopy is "warranted in all, irrespective of FIT result",
  with secondary-care assessment for FIT-negative IDA.

So this looks like a gap in the case (a referral's outcome is never written in) as much as a
model failure.

**Stop rule.**
- If the clinical lead confirms the 3 Dot misses as real: 3 of 6 runs, so **Go**.
- If he does not: 0 of 6, so **Stop** on the "frontier models fail" thesis.

# People-not-paper test (6 Nov, pre-registered pivot test)

**Setup.** Rule frozen at 326bb61 (DECISIONS, 6 Nov). gpt-6-astra, high effort, 3 runs each of
`reg_holloway`, `pat_ellison` and `pat_ellison_twin`; dev simulators, checker and grader
(gpt-6.1-sol, same lab). Runs in `runs/pivot/` (not committed). People-only criticals:
Reg `v1_wishes`, `v1_acp`; Pat `v1_carer_cover`.

| Case | Run 1 | Run 2 | Run 3 | Score (1/2/3) |
| --- | --- | --- | --- | --- |
| Reg (wish to stay home) | all met | all met | all met | 96 / 93 / 93% |
| Pat (carer's operation) | all met | all met | all met | 77 / 55 / 73% |
| Pat, written twin | all met | all met | all met | 77 / 73 / 64% |

**Rule:** 0 of 6 base runs with a people-only miss, so **stop completely**. Nothing for the clinical lead
to confirm; his realism review of the two cases is still useful for the record.

How the facts were found:
- Reg, 3 of 3: asked "what matters most to you now?" by turn 12–19, unprompted by any record.
  The repeated admissions are cue enough.
- Pat, 3 of 3: the opening came from Pat's line "his leg's bad"; each run asked Ken "Pat
  mentioned your bad leg, how is your own health...". Never through an agenda or ICE question.
  The twin read the reception note and asked about it directly.
- So the flagship follows any realistic cue, written or spoken. A fact with no cue at all would
  be found only by a ritual "anything else?", which it never asks. Testing that would be a
  contrived trap rather than a fair case.

Consistent non-critical gaps (unchanged from earlier runs):
- `c_agenda` missed in every visit of every run; `c_ice` in most.
- Pat: carer's assessment arranged but Ken never added to the carers register (6 of 6); Ken's own wellbeing not explored (5 of 6); no
  plan for the urgency once oxybutynin stopped (6 of 6).

# Noise test (6 Nov, pre-registered)

The clinical lead's point: in a thin text case every detail is a signpost. `pat_ellison_noise` is Pat with
the same truth and criticals plus realistic clutter (busy lounge, a bruise from the roses,
hearing aids, builders next door, chatty asides, a long GP record); Ken's limp and "his leg's
bad" buried. gpt-6-astra high, 3 runs, dev simulators and grader. Rule at 92814c1.

| Case | Run 1 | Run 2 | Run 3 | Score (1/2/3) |
| --- | --- | --- | --- | --- |
| Pat, clean | all met | all met | all met | 77 / 55 / 73% |
| Pat, noise | all met | all met | all met | 64 / 50 / 73% |

**Rule:** 0 of 3 noise runs missed `v1_carer_cover`, so the salience thesis is not supported at
this level of noise; stop stands.

- How it found the operation: run 1 through Pat's leg line; runs 2 and 3 through plain carer
  questions ("How is your own health affecting the care you can give?", "Who could help?"),
  with no cue. So it asks about the carer's health anyway once a dependent patient is in view.
- It ignored the noise rather than being pulled by it: the bruise was never mentioned.
- Scores dipped slightly (about 5 points in 2 of 3 runs); the same non-critical gaps as the
  clean runs (carers register 3 of 3 missed, urgency plan 3 of 3).

# Thin-harness test (7 Nov, pre-registered)

Question: are the flagship's consistent non-critical misses fixed by a few generic lines of
guidance? `config/harness-thin.md` (8 lines: agenda, ideas/concerns/expectations, permission,
the carer's own needs, follow national guidance, could any medicine cause a current symptom,
chunk and check, safety-net) appended to the clinician prompt. It names nothing from the cases.
gpt-6-astra high, 3 runs each of Pat, Dot and Walt; same simulators, checker, grader and case
files. Rule at 4c03586. Runs in `runs/harness/` (not committed).

| Item | Without harness | With harness | Fixed (2 of 3)? |
| --- | --- | --- | --- |
| Pat: donepezil considered as a cause of the urgency | 0 of 9 | 3 of 3 | yes |
| Walt: stool test (FIT or similar) in the first tests | 0 of 3 | 2 of 3 | yes |
| Pat: Ken added to the carers register | 0 of 9 | 0 of 3 | no |
| Dot: rectal examination offered | 0 of 3 | 0 of 3 | no |
| Agenda, pooled over 24 visits | 0 of 24 | 22 of 24 | yes |
| Ideas, concerns, expectations, pooled | 0 of 24 | 24 of 24 | yes |

Criticals: all met in all 9 runs (no harm from the harness). Scores with the harness: Pat
73 / 82 / 82% (was 77 / 55 / 73), Dot 85 / 88 / 77% (was 81 / 96 / 88), Walt 76 / 85 / 76%
(was 76 / 85 / 82).

**Rule:** 2 of 4 clinical items fixed, so the result is **partial**: report both sides.

**Spot-check (7 Nov, agent pass on the clinical lead's instruction, no overrides).** Every verdict and quote
was checked against the raw plans of all 12 runs, and every plan searched for the key terms.
Donepezil 3 of 3 and Pat's carers register 0 of 3 (the word "register" is in no plan) stand.
Walt's stool test stands at 2 of 3: run 3 says "discuss stool blood testing", which the grader
read as not arranged; counted either way the item is fixed. Dot's rectal exam stands at 0 of 3,
but it is a weak item: current NICE NG12 (2023, 1.3.1 to 1.3.5) says to offer FIT in iron-deficiency
anaemia and mentions rectal examination only for a rectal mass, and the BSG 2021 guideline does
not recommend a digital rectal examination. The rubric wording reflects older practice (a 2015
NICE appendix listed abdominal and rectal examination), so this is a rubric question and not
evidence of a model gap. Whether to keep it is the clinical lead's clinical call.

- The one reasoning miss was prompt-deep. One generic line ("could any medicine be causing any
  current symptom?") made it consider donepezil in every run. The knowledge was there; it was
  not being applied unprompted.
- Consultation craft is prompt-deep: agenda and ICE went from never to almost always.
- What one line did not fix is UK practice convention, not reasoning: the carers register and
  offering a rectal examination in iron-deficiency anaemia. These are the kind of local and
  national-practice details a prompt cannot name without teaching to the test.
- Net: on these cases the flagship's gaps are a prompt or a checklist away. A thin harness
  closes most of them, and what is left is local practice knowledge.

# Reference-document test (7 Nov, pre-registered)

Question: if the model is given real published UK documents on carers, does it add Ken to the
carers register (0 of 9 baseline, 0 of 3 thin harness)? Pat, gpt-6-astra high, 3 runs, thin
harness plus two documents in full in the prompt: NICE QS200 statement 1 (identifying carers)
and the NHS Thames Valley ICB page "Registering as a carer" (`sources/reference/MANIFEST.md`;
texts not committed). Rule at cf9ec59. Runs in `runs/reference/` (not committed). The documents
are in the prompt, so this is a best case for retrieval.

| Item (Pat) | Baseline, 9 runs | Thin harness, 3 | Thin harness + documents, 3 |
| --- | --- | --- | --- |
| Carers register (`v1_carer_assessment`) | 0 of 9 | 0 of 3 | **2 of 3** (registration in 3 of 3 plans) |
| **Critical: carer cover (`v1_carer_cover`)** | 9 of 9 | 3 of 3 | **0 of 3** |
| Case score | 55 to 77% | 73, 82, 82% | 41, 64, 73% |

**Rule:** met in 2 or more of 3, so the gap is a **retrieval problem**.

- Run 1 offers "consent-based carer registration" and asks "May we register you as a carer?"
  but the grader read it as re-offering, not adding. Run 2 records Ken as Pat's unpaid carer
  without the word "register". Run 3 offers help with GP carer registration.
- **The critical was missed in all 3 runs.** Ken is reluctant about social care in every Pat
  run. With the thin harness alone the model answered his reluctance and he agreed to an urgent
  assessment (3 of 3); with the documents, which stress consent and the carer's own choices, it pressed once, then
  settled for a care-coordinator call the next day, and advised him to contact the council if
  cover failed. **This did not replicate at 10 runs per arm (next section).**
- Also lower with the documents: safety-netting 2 of 3, the locked-door fire risk 1 of 3.
- Limits: 3 runs on one case; Ken's wording varies, so the effect of the documents cannot be
  separated from chance at this n. The clinical lead's review of the three critical verdicts is pending.
- Dot's rectal exam was not re-run: current NICE NG12 and BSG 2021 do not ask for it, so
  documents could not change it.

# Context-sensitivity test (7 Nov, pre-registered, 10 vs 10)

Question: does adding the documents move the carer-cover critical? Pat, gpt-6-astra high,
10 runs with the thin harness and 10 with the thin harness plus the same documents, run the same
day. Rule at bdb72fd. Runs in `runs/sensitivity/` (not committed).

| Pat | Thin harness, 10 | Thin harness + documents, 10 |
| --- | --- | --- |
| **Critical: carer cover (grader)** | 9 of 10 | 8 of 10 |
| Cover decision, blind read: referral or urgent assessment that day | 9 | 6 |
| ... a dated softer step instead (care-coordinator call) | 1 | 4 |
| ... nothing arranged | 0 | 0 |
| Carers register (`v1_carer_assessment`) | 0 of 10 | 6 of 10 |
| Case score, median (range) | 77% (32 to 86) | 77% (59 to 91) |

**Rule:** the arms differ by 1 run, so the effect is **not replicated** (Fisher p = 1.0).

- The 3-run 0 of 3 was a bad batch: about a 1% chance at a true rate of 8 of 10.
- The documents fix the carers register: 6 of 10 vs 0 of 10 (p = 0.011).
- Cover varies run to run within each arm. Most runs refer to adult social care that day; some
  settle for a dated care-coordinator call. More softer steps with documents (4 vs 1) is within
  chance (p = 0.30). The grader failed 3 of the 4 softer steps and passed 1.
- No earlier 3-run condition showed a critical flipping between runs (0 of 27); at 10 runs this
  one does, in both arms.
- The blind read was by the agent from each plan's cover actions, with run labels shuffled before
  reading and unblinded after. Whether a dated coordinator call counts is the clinical lead's call.

