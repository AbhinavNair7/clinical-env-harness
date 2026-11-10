# Writing a case: the short guide

Open the form with `open tools/case-form/index.html`. It walks the sections in order with Edith
beside each one, saves as you type (in this browser only) and exports text. Download it into
`cases/drafts/` and ask the agent to turn it into a case YAML. Edit a draft by opening it in the
form again, not by hand: the agent converts from the form data in the file. The plain-text
version of the same sections is `docs/case-template.md`.

## Start from a real patient, then fictionalise

A real messy patient gives you the texture no one invents: the dosette nobody updated, the
daughter who visits on Sundays. Keep the shape and change everything that identifies them:

- New name, age moved a few years, a different town, family and agency names.
- Dates only relative to visit 1 ("3 weeks before visit 1"). No calendar dates or birthdays.
- Mix in a detail from a second patient, so no single person can be recognised.
- Never paste from a real letter or record; write it in your own words. The form warns if it
  sees something like an NHS number, a postcode or a calendar date.

## What makes a good case

1. **Sharp, gradable criticals (2 to 4; 5 at most in a 3-visit case that needs it).** Each one is something a GP would be criticised for
   missing, at a named visit, that a reader can tick from the transcript or plan. "Stops
   furosemide and gets the dosette changed" can be graded; "holistic assessment" cannot. Rank
   your candidates and keep the top 4; the rest become normal items with a weight.
2. **One critical a do-everything plan fails, where you can.** A must-not (an unnecessary
   admission, a new drug before stopping the culprit), or a must-do worded so restraint is
   part of it. Skip it if the only candidate restates another critical.
3. **Pick the messiness level on purpose.** Mild: one stale entry, everyone mostly honest.
   Moderate: a few sources disagree and one person plays things down (Edith). High: a
   confidently wrong carer, records that contradict themselves, little anyone says can be
   taken at face value. The pilot needs a spread, including one or two nearly clean cases.
4. **A carer only where realistic.** About half to two thirds of the pilot cases have one.
   Don't add a daughter just to create a conflict.
5. **Conflicts in degrees.** Some cases turn on one stale medicine, some on a full
   contradiction. Not every source needs to be wrong.
6. **Events that fit any plan.** Whatever the GP did at visit 1, the visit-2 events must still
   make sense: "the pharmacy re-dispensed the same pack" works whether or not the GP stopped
   the drug. Good care must never be punished by a fixed event.
7. **Every hidden fact has the question that earns it.** Write it as the topic a GP would ask
   about ("dizziness on standing"), not the exact words.
8. **List every abnormal finding.** An examination you don't list comes back unremarkable, and
   an investigation you don't list is "not available". If the truth implies a postural drop,
   write the numbers.
9. **Say what changes at each visit.** What the carer says on the visit-2 call, a fall that only
   reaches the records by visit 2, a fact that is no longer true: set "which visits" on the line.
10. **Script the standard history.** What the patient and carer each say about washing,
   toileting, stairs, meals, help, medicines, memory, mood, alcohol, pain and what they want.
   A symptom you don't write is one they don't have.

## What happens next

The agent converts your export into a case YAML, writes the records out as real documents
(cluttered GP record, templated agency notes), runs the case validator and sends you anything
it had to guess. Unless you say otherwise in a visit's reason, every record is available at
every visit and turn budgets follow Edith (40 face to face, 20 by phone). The form's
checks catch most of what the validator rejects, and its identifier warnings are a safety net,
not a guarantee. You check the clinical realism; that stays your call.
