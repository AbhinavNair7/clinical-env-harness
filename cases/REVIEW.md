# Case review: sourced dev cases

For the clinical lead (clinical reviewer): approve, edit or reject each case. One page per case below.
UK equivalents are in brackets. Both are **dev cases**: run in the feasibility check, never
scored in the pilot. Case files: `cases/dev/<id>.yaml`. Source and changes:
`sources/provenance/<id>.yaml` (internal).

| Case | Theme | Messiness | Carer | Criticals | Checks | Look at |
| --- | --- | --- | --- | --- | --- | --- |
| marjorie_lindqvist | Reversible decline: thiazide hyponatremia plus a lapsed levothyroxine refill; daughter wants an SSRI | moderate | daughter | 4 | validator, overlap 0, identifiability pass (6 pairs), visit-1 smoke run read | Is the no-antidepressant must-not fair as a critical? Is Na 128 outpatient management right? |
| harold_benning | Phenytoin toxicity from new amiodarone, called vertigo, meclizine added | mild | none | 3 | validator, overlap 0, identifiability pass after a rewrite, visit-1 smoke run read | Should stopping meclizine or driving advice be critical? Phenytoin dosing wording |

**Smoke runs (visit 1, dev config: gpt-6.1-sol clinician, gpt-6-luna people and checker, 5 Nov).**
Transcripts: `runs/smoke/` (not committed). Both read naturally: people stayed on script
(Marjorie 1 flagged draft, Harold 2, all regenerated), and Denise interjected where it fit.
**The cheaper dev clinician met every visit-1 critical in both cases.** It found the lapsed
levothyroxine and the filed sodium, declined sertraline with the sodium as the reason, named
amiodarone raising phenytoin, held phenytoin with a neurology restart plan, stopped meclizine
and advised no driving. In B it also sent him to the ER for a stroke workup (defensible on
apixaban; not penalised). This is one ungraded visit-1 run each, not the feasibility check,
but it points the same way as Edith: once the clinician reads the fill history, these cases
are solvable. If the flagship does the same at visit 2, these cases need to be harder (more
mess, or the key clue only in what people say) before the pilot cases are written. Fixed after
the runs: Harold's script said "one in the morning and one at night" (left over from
carbamazepine) and the model chased that false discrepancy; a "4AT" request matched the memory
test instead of attention.

**Your review (5 Nov) and what changed.** Both cases stay as the easy, nearly clean end of
the dev set: they turn on documents, so models solve them. The hard cases are being rebuilt
ambiguity-first (`cases/skeletons/`).

- Marjorie:
  - The visit-2 "organizer unchanged" device is gone. Visit 2 is new information instead: the
    ER says "continue home medications" (with the thiazide), starts levothyroxine 25 mcg and
    adds tramadol.
  - Criticals: the thyroid lapse; the sodium, now also "names the other likely causes and
    checks them in proportion"; no antidepressant; and, new at visit 2, stopping tramadol.
  - New normal items: reassess mood with a suicide question, and one clear thyroid dose
    (weight 3).
  - ER today is down to weight 1.
- Harold:
  - The cardiology letter is not in the chart at visit 1; it arrives before visit 2.
  - The fill history covers the last 30 days only, with no "NEW" labels and no interaction
    alert, so when the new pills started has to be asked.
  - Criticals: toxicity with an urgent level and same-day specialist advice (no unilateral
    change), stopping meclizine (now critical), and acting on the visit-2 level.
  - Stopping phenytoin outright and driving are weight-3 normal items.
- Both: every critical now lists its `evidence`, and the validator rejects a critical that
  rests on records alone.

US wording to confirm (my drafts, not yours yet): the US over-provision examples in the judge
prompt (`locale.py`) and the US referral routes for `c_local_pathways`
(`rubrics/consultation.yaml`).

---

## Marjorie Lindqvist, 84 (moderate, daughter present)

**Arc.** Over about 4 months she slows down: tired, naps, stops cooking, needs help in and out
of the tub, has one kitchen fall. Two causes, both found in the records:

- Losartan was switched to losartan-hydrochlorothiazide 5 months ago with no electrolyte check.
  An urgent care sodium of 128 (139 before the change) was filed with no action.
- Her levothyroxine refill lapsed about 2 months ago: no refills left and an unanswered
  pharmacy request. Denise (daughter) thought the doctor had stopped it, so it is not in the
  organizer. The chart still lists it.

Denise is sure it is grief-related depression and asks for sertraline. Visit 2 (day 11, office)
follows an ER visit for a night fall: sodium 127, TSH 38.2, tramadol added, "continue home
medications" copied from the chart. The organizer is unchanged whatever was planned at visit 1,
because Denise filled it as usual and the pharmacy auto-refilled the combination pill.

**Sources and conflicts.**

- Levothyroxine: chart list vs fill history and empty bottle vs "she takes everything" vs ER
  list.
- Sodium: old normal vs filed 128.
- Mood: Denise vs Marjorie.
- Function: "I manage fine" and a copied-forward note vs what Denise has seen.
- Fall: "I just sat down" vs Denise.

**Criticals.**

1. V1: finds the levothyroxine has not been taken for about 2 months and restarts it.
2. V1: acts on the sodium of 128. Stops the hydrochlorothiazide and arranges a repeat sodium
   and TSH within about a week.
3. V1, must-not: starts an antidepressant while the sodium and thyroid are untreated.
4. V2: finds out what is actually in the organizer, not the ER's list, and fixes how the
   changes reach it.

Normal items include tramadol (V2, weight 3), asking Denise what she has seen, the dementia
label and ER-today must-nots, and home health PT/OT (bath step).

**What changed from the source (6).** Hypothyroidism is known but the refill lapsed (found by
reconciliation, not a new diagnosis). A thiazide is added as a cause. Caught earlier in primary
care: no delirium, no hypertonic saline. The patient is a woman in the US with no COPD or
smoking. The daughter wants an antidepressant. Visit 2 adds an ER visit with tramadol.

**Checks.**

- Validator: OK.
- Overlap with the source: 0 shared runs of 8+ words.
- Identifiability: source not in the top 10 for all details, any of the 6 pairs (including
  hyponatremia + hypothyroidism, 1,363 hits) or any detail by relevance.
- Licence: CC BY 4.0, from its XML.

**For you to look at.**

- Is a must-not critical for starting an SSRI fair, or should it be weight 3? (A
  do-everything plan fails it, as the guideline wants.)
- Is Na 128, euvolemic and without severe symptoms, office-managed in your view? The rubric
  penalises sending her to the ER today.
- Levothyroxine restart dose at 84: the rubric accepts either restarting 75 mcg or a lower
  dose.
- The ER would likely have flagged TSH 38 more loudly. Realistic as written?
- US texture: Medicare annual wellness visit, auto-refill, the walk-in clinic and the
  fill-history format. Add what a US PCP would really see.

**Honest weak points.**

- Two critical misses could come from one root cause (not reading the fill history).
- The visit-2 "organizer unchanged" event relies on Denise not acting on visit-1 changes. It
  fits any plan, but it is the same device as Edith's.

---

## Harold Benning, 83 (mild, no carer)

**Arc.** Seizure-free for years on phenytoin 300 mg at night (level 14 last year). Cardiology
started amiodarone and apixaban 35 days ago for new atrial fibrillation. Amiodarone slowly
raises phenytoin. From about 2 weeks ago: unsteadiness ("walking on a boat"), double vision on
side gaze, drowsiness. Urgent care called it "vertigo, likely BPPV" without a positional test
and added meclizine 25 mg three times a day (a prescribing cascade: sedating, anticholinergic,
worse urine flow). He lives alone, drives daily to see his wife in memory care and plays things
down. Phenytoin also lowers apixaban levels.

Visit 2 (day 4, phone): neurology's annual level, drawn 5 days before visit 1, arrives at 31.5
(range 10 to 20). He is going by the old bottle labels and still takes meclizine.

**Sources and conflicts.**

- Medicines: the chart list predates cardiology, he says "same pills as always", and the fill
  history (with an overridden interaction alert) and his bottles show everything.
- Vertigo: the urgent care diagnosis and the problem list vs "the room doesn't spin" and a
  negative Dix-Hallpike.
- Level: last year's normal vs the interaction alert.

**Criticals.**

1. V1: recognises probable phenytoin toxicity from the amiodarone. Orders a level and a dose
   change with neurology, or a heart-medicine change with cardiology.
2. V1, must-not: stops phenytoin outright with no restart plan.
3. V2: acts on the level of 31.5. Finds out what he is actually taking, gives a clear dose
   instruction agreed with neurology and arranges a repeat level.

Normal items: stop meclizine (weight 3), driving advice (weight 3), reconcile the list, eye
movements and gait, stroke screen and 911 safety-net, the apixaban interaction, and must-nots
for accepting the BPPV label or adding sedatives.

**What changed from the source (8).** Carbamazepine became phenytoin (a rewrite after the
first identifiability check found the source). The mechanism is a slow amiodarone interaction,
not a dose escalation. The indication is long-standing epilepsy, not trigeminal neuralgia.
There is no atrial flutter or cardioversion. Urgent care adds meclizine. The presentation is
milder (no myoclonus or confusion). He is 83 and drives.

**Checks.**

- Validator: OK.
- Overlap: 0.
- Identifiability: the first draft (carbamazepine) failed on "carbamazepine toxicity +
  dizziness". After the rewrite, the source is not in the top 10 for all details, any of the 6
  pairs or any detail by relevance.
- Licence: CC BY 4.0.

**For you to look at.**

- Should stopping meclizine or driving advice be critical? Both are weight 3 now. With 3
  criticals this is the easier case.
- Phenytoin dose wording: the rubric accepts "hold a dose or two and restart lower, with
  neurology". Phenytoin's kinetics make small changes large; is the wording right?
- Would you send an 83-year-old on apixaban with new unsteadiness for a head CT? The rubric does
  not penalise imaging; it asks for a stroke screen and safety-net.
- Amiodarone for rate or rhythm control in a frail 83-year-old: realistic in US cardiology?

**Honest weak points.**

- The amiodarone-phenytoin interaction is a well-known teaching point, so strong models may
  spot it once they see the fill history. The test is then whether they look at the fill
  history and the bottles.
- Visit 2 is short and relies on him going by the old labels.

---

# Round 2: ambiguity-first cases (built 5 Nov from your skeleton lines)

| Case | Theme | Messiness | Carer | Criticals | Checks | Dev run (gpt-6.1-sol, 3 visits) |
| --- | --- | --- | --- | --- | --- | --- |
| ray_kowalczyk | Climbing sugars and weight loss: pancreatic cancer | moderate | wife | 3 | validator, overlap 0, identifiability: **fails on the core pair** (see below) | Imaging ordered at visit 1; visit 3 sent to ER but **said "pancreatic mass" on the phone** and missed dark urine and itching |
| gene_ostrander | Falls, bladder and memory labels: NPH | high | wife | 4 | validator, overlap 0, identifiability pass | **CT head ordered at visit 1** (no head injury); stopped oxybutynin, held donepezil, ECG, PT/OT, neurology; elicited Carol's strain |

## Ray Kowalczyk, 85 (moderate, wife Dolores)

- **From your lines:**
  - The old imaging is an ultrasound that "could not see the pancreas", not a normal CT.
  - No home sugars, just an office fingerstick of 291; the last weight is 9 months old, on
    another clinic's scale.
  - Past control has gone up and down.
  - Both Ray and Dolores wander off topic, and the turn budget is 30.
  - Back ache and post-meal pain come out only if asked.
- **Visits:**
  1. Office.
  2. Day 18, office: weight measurably down. The results are back only if they were ordered.
  3. Day 33, a phone slot booked by reception: Dolores reports breathlessness, a swollen calf
     (if asked), dark urine and itching (if asked).
- **Criticals:**
  1. V1: a balanced differential with a dated plan. A CT is also right if the back ache and
     post-meal pain are elicited.
  2. V2: urgent imaging (CT, MRI/MRCP or EUS), a PPI only alongside.
  3. V3: same-day in-person or ER assessment.
- **Must-nots:**
  - Insulin with no plan.
  - A scattergun cancer workup.
  - More mirtazapine.
  - Trusting the old ultrasound.
  - Reassuring and waiting again at visit 2.
  - Breaking the cancer news on the phone (weight 3).
- **Identifiability, your call:** "pancreatic cancer + worsening diabetes" puts the source in
  the top 10. So does "+ new-onset diabetes". I tested both; any case on this theme finds it,
  because the source is the top recent report of a guideline-level link (new-onset diabetes is
  a NICE NG12 trigger). Ray shares no sentence or specific detail with it (overlap 0;
  glipizide, mirtazapine and prednisone pairs pass). Options:
  1. Accept, logged as "theme, not case".
  2. Change the theme.
  3. Use a different seed (the result is the same).
- **What the dev run did:**
  - Visit 1: drew out the back ache and post-meal pain and ordered imaging, so the mass was in
    the chart by visit 2. Your rubric counts that as right.
  - Visit 3: sent him to the ER by ambulance for a suspected clot, which is good. But it
    named "his pancreatic mass" on the phone before anyone had told them. It never asked
    about the urine, itching or eyes.
  - Simulator: Dolores dropped a tomato aside into a tense call. Ray's age and some daily
    detail were improvised; those are now scripted.

## Gene Ostrander, 80 (high, wife Carol)

- **From your lines and your memory-clinic patient (fictionalised):**
  - Prostatectomy 15 years ago, with leakage afterwards that settled and is worse for a year.
  - A summer fall blamed on the heat, after which his gait never recovered.
  - No head injury now: the paramedics found a normal ECG and called it a mechanical fall.
  - Three labels: mechanical falls, overactive bladder (oxybutynin on top of donepezil), and
    Alzheimer's that was never imaged.
  - Carol plays down the wetting and her own state.
- **Visits:** 1, office; 2, day 21, office; 3, day 46, home visit after a bathroom fall.
- **Criticals:**
  1. V1: medicines and the slow pulse.
  2. V2: brain imaging once the basic workup is negative.
  3. V3: a rethink and an NPH referral, or imaging now.
  4. V3: Carol's breakdown, which counts only if she is asked how she is coping.
- **What the dev run did:** urgent CT head at visit 1, given recurrent falls on aspirin, plus
  an ECG, bloods, stopping oxybutynin, holding donepezil, PT/OT and neurology. The CT was back
  at visit 2 (big ventricles) and it pushed the hydrocephalus referral. At visit 3 it sent
  him to the ER for an "uncertain head injury" (the script now says he didn't hit his head).
  Carol's strain was drawn out and acted on.

## For you to decide

1. **Is imaging at visit 1 fair in these two cases?**
   - In both, the cheap dev model ordered the decisive scan at visit 1. The case then stops
     being ambiguous.
   - If you'd call visit-1 imaging over-investigation here (you said you wouldn't CT Gene
     without a head injury), it becomes a must-not or over-provision item. The cases then test
     restraint plus timely escalation.
   - If it's reasonable, these cases mostly test the visit-3 handling, which is where the
     model slipped.
2. **Ray's identifiability:** accept as theme-level, or change.
3. **Gene has 4 criticals.** Keep Carol's breakdown as critical?

---

# Negative-workup cases (5 Nov): criticals for the clinical lead to approve before the flagship runs

Pre-registered Stop rule in `DECISIONS.md` (5 Nov). Both cases stay in the set whatever the
result, and criticals are not changed after the runs. Skeletons and guideline notes:
`cases/skeletons/`. Checks: validator, overlap 0, identifiability pass (Walt after switching
sertraline to citalopram, which the source names), full test suite.

**Smoke runs (visit 1 only, dev config: gpt-6.1-sol clinician, 5 Nov).** Transcripts:
`runs/smoke-neg/` (not committed). Both read naturally.
- Walt: the dev model asked what he eats, screened red flags, asked about suicide, found the
  stopped citalopram, ordered bloods and a chest X-ray, and kept CT for later "if unexplained".
  It also arranged a same-day crisis assessment at visit 1 for a passive death wish (not
  penalised).
- Dot: it asked about bowel symptoms, the iron and shop-bought painkillers, found the Nurofen,
  stopped it and the aspirin, ordered FIT and coeliac serology, and referred urgently. It also
  started omeprazole and alternate-day iron.
- Both visit-1 critical sets look met. As planned, the test is at visit 2 (the negative results
  under pressure) and visit 3.
- Fixed after the runs: Karen said "no guns" because her script had the rifle only from visit
  3, so it is now in her and Walt's scripts from visit 1. A mental state examination no longer
  comes back "unremarkable".

## Walt Brenner, 79 (US, moderate, daughter Karen)

**Arc.** He's lost 17 lb since his wife died 8 months ago, and his daughter is sure it's cancer.
- Visit 1: he has no appetite at all, with no early fullness and no swallowing trouble, and no
  red flags. He stopped his citalopram, but it is still auto-refilled. The last wellness note,
  copied forward from before the death, says "mood good".
- Visit 2: every test is clear. Karen says "the tests missed it" and wants a PET and scopes. He
  wakes at 4 and says "what's the point".
- Visit 3, a phone call with Karen: he has barely eaten or drunk for 3 days, stays in bed, and
  said "I'd rather not wake up". There is a rifle in the closet.

| # | Critical | Approve? |
| --- | --- | --- |
| 1 | **V1** Finds out whether he is actually eating and why not (no appetite, versus full early, versus can't swallow or pain). | yes (the clinical lead, 5 Nov) |
| 2 | **V1** Proportionate first tests: bloods plus chest imaging (chest X-ray or CT). A CT is acceptable but not required, and no "if clear" plan is required. | yes (the clinical lead, 5 Nov) |
| 3 | **V2** After the clear tests, recognises depression and starts treating it (an antidepressant or an urgent mental health referral), with a review within about 2 weeks. Not met by "come back in months" or by more scans instead. | yes (the clinical lead, 5 Nov) |
| 4 | **V2** Asks Walt directly about thoughts of death, suicide or self-harm (the clinical lead: critical, 5 Nov). | yes (the clinical lead, 5 Nov) |
| 5 | **V3** Same-day risk assessment by an appropriate route: a home visit, the crisis team, the ER, or bringing him in today. Not phone advice alone, a dose increase, or a routine appointment. | yes (the clinical lead, 5 Nov) |

Weight-3 normal items: the must-nots against a reflex scan and false reassurance at visit 2.
The case has 5 criticals; the validator now allows up to 5 (the clinical lead, 5 Nov).

## Dot Fairbanks, 82 (UK, moderate, husband Frank)

**Arc.** Hb 94, ferritin 9. Three common causes: a tea-and-toast diet since her knees stopped
her cooking, Nurofen that Frank buys (he says "she only takes what's in the pack"), and aspirin
still in the blister pack on top of apixaban. She also stopped her iron.
- Visit 2: FIT 6, coeliac negative (scopes clear if requested), and Hb barely moved. Frank asks
  "can she stop the iron?"
- Visit 3, a phone call: Hb 109 and rising. Frank says the Nurofen is fine.

| # | Critical | Approve? |
| --- | --- | --- |
| 1 | **V1** Screens for symptoms that would make it bowel or upper-GI cancer (bowel habit, bleeding or black stools, weight loss, abdominal pain, swallowing, reflux or vomiting). Most of them asked is enough. | yes (the clinical lead, 5 Nov) |
| 2 | **V1** UK route: FIT and coeliac serology in primary care, with referral by the result. Direct referral for scopes is also acceptable. | yes (the clinical lead, 5 Nov) |
| 3 | **V2** After the negative tests, acts on at least one common cause (diet alone is acceptable), keeps the iron going, and rechecks in about 4 weeks. Not met by "all clear, stop the iron". | yes (the clinical lead, 5 Nov) |
| 4 | **V3** With Hb rising, reassures, continues iron with a recheck, and orders no further tests while she is responding. | yes (the clinical lead, 5 Nov) |

Weight-3 normal items: finds the Nurofen by asking Dot directly, and the must-nots against
reflex capsule or CT, stopping the iron, and over-investigating at visit 3.
