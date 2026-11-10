# Case template

Easiest route: the form at `tools/case-form/index.html` (open it in a browser) walks these sections with Edith as the worked example and exports a draft; `docs/case-writing-guide.md` says what makes a good case. This file is the same template as plain text.

Write each case in plain English, about one page. Fictional composites only: no real names, dates of birth, NHS numbers, addresses or copied letters. Save drafts in `cases/drafts/` and ask Claude Code to convert them into case files.

Rules:
- Events between visits must be plausible whatever plan was made at the previous visit (for example, "the pharmacy never actioned the change"). Good care must never be punished by a fixed event.
- 2 to 4 critical items per case (5 at most, in a 3-visit case that genuinely needs it), each something a GP would be criticised for missing (or doing).
- Not every case is a trap. Across the 10 pilot cases: a carer only where realistic (about half
  to two thirds), and conflicts in degrees: some cases have one stale medicine, some a full
  contradiction, one or two are nearly clean. The messiness level below records which.

**Critical items decide the whole pilot.** A model fails a case if it misses any one of them,
so every extra critical makes failing easier; that is why there are at most 4 (5 in a 3-visit case that genuinely needs it). Everything else
(the other must-dos, must-not-dos, red flags) is scored but never decides go or stop. When you
have more than 4 candidates, rank them and keep the 4 you would most criticise a GP for
missing; the rest stay as normal items with a weight (3 = important, 2 = should, 1 = nice).

```
Title:

Messiness: mild / moderate / high (how hard the sources make it, not how ill the patient is)

Patient: age, living situation, main conditions, cognition, how they talk
Does the patient chip in when the carer is being asked? (always / sometimes / never)
Patient habits (tick any): denies or minimises (falls, alcohol, not coping) / goes off on
tangents / poor recall, vague or wrong medicine names. Anything wrong they say goes in "What
each source says" below as a wrong fact; the habit only shapes how they say it.

Carer (only if realistic for this case): who, how often they see the patient, what they believe, their agenda
Does the carer chip in when the patient is being asked? (always / sometimes / never)
Carer habits (tick any): denies or minimises / tangents / poor recall / dominates (answers
for the patient or contradicts them)

What's really true: function, mobility and aids, falls, ADLs, medicines actually taken, care actually delivered, risks

What each source says (mark anything wrong or out of date; for each record, tick what makes it
messy: contradicts another record / contradicts itself / miscoded or a wrong diagnosis carried
forward / long or noisy / outdated entries such as a stopped medicine still listed):
- Patient:
- Carer:
- GP record:
- Care agency notes:
- Discharge summary:
- Pharmacy or dosette:
- Ambulance report (if paramedics attended a fall):

Standard history: what the patient and the carer each say about every topic a GP routinely
asks, so the simulator never has to make it up: washing and dressing, toileting and
continence, stairs and mobility, meals and shopping, help they get, medicines, memory, mood
and sleep, alcohol and smoking, pain, and what they want from the visit. Also who gives
each medicine that is outside the blister pack (drops, inhalers, creams). Only symptoms they
have need writing: anything not listed is one they don't have, and they'll say no if asked.

Records should read like the real thing (Claude writes them out from your notes): a long,
cluttered GP problem list and repeat list with old consultations; agency notes written from a
template that make things sound fine; a handwritten-style discharge summary (diagnosis, not
the BP numbers). Give dates as "3 weeks before visit 1", not calendar dates.

Long-standing conditions or red herrings (optional; e.g. an old BPPV diagnosis when today's
dizziness is postural, or more than one cause for a symptom):

Hidden facts (only come out if asked the right question). For each, the question that earns it:
- Fact:                     Revealed if asked about:

Visits (2 or 3), for each:
- Setting and who's there, and how many days after visit 1:
- What changed since last time:
- Examination findings (anything you'd find if you looked: lying/standing BP, gait or TUG, home hazards, dosette contents, cognition screen; anything not listed counts as unremarkable, so list **every** abnormal finding the truth implies, and the basic observations; an investigation such as bloods or an ECG is "not available" unless you list its result):
  Write the basic observations one per line (pulse, BP, temperature, respiratory rate, oxygen saturation); asking for "obs" returns them all, asking for "pulse" returns only the pulse.

CRITICAL ITEMS (2 to 4, at most 5; the only ones that decide go/stop). For each: what the GP must do
(or must not do, if doing it would be a serious error), at which visit, "action" (needed
whatever the sources say) or "detect" (only exists because sources disagree), and the stage
it belongs to (intake / triage / history / records / examination / plan / follow-up).
Where you can, make one critical something a do-everything plan fails: a must-not (an
unnecessary admission, an inappropriate new drug, over-investigation) or a must-do worded so
restraint is part of it. Not required when the only candidate just restates another critical.
1.
2.
3.
4.

Other must do (one line each, with weight 3 / 2 / 1). At visit 2 or 3, the grader already checks
that the GP follows up its own earlier plan; add a case item only for a case-specific check:

Must not do:

Red flags:

Twin (only if asked; Claude can draft it): what each source says when everyone tells the truth
and the problem is in plain view. Same patient, visits and "action" criticals.
```
