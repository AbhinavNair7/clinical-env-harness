# Run 1 review (the clinical lead, 4 Nov)

Each point is sorted by what happens to it:
- **Fix:** our simulator, records or examiner was unrealistic.
- **Score:** the model under test did it. It becomes grader material in M3 and is not fixed.
- **Note:** no change now.

## Patient and carer simulators: Fix

- **Repeated stock lines.** "I do all my own meals, I always have" appears 6 times, and "I don't want to be a bother" 4 times. There are three causes:
  - the meals line is a "volunteered" fact with no limit on how often she says it;
  - her speech style hands her a stock opener;
  - the checker counts repeats as fine.

  Fix: a volunteered item is said once unless the GP asks again, no phrase is repeated, and her speech style no longer has a catchphrase.
- **Answering a different question.** "What has been troubling you most?" got "I do all my own meals." A real patient says "nothing much, love", names one small thing, or denies it plainly. Fix: answer the question that was asked, and deny in character rather than switching to a line from the script.
- **Stacked questions.** Turn 8 asked about pain, headache, vomiting and new difficulty walking in one go. Fix (revised after run 3, because a blanket "no" read as lying): two questions, or a few closely related ones, get answered; three or more different ones get only the first one or two answered, and the rest are left, not denied, so the GP has to ask again. Logged as a decision.
- **Chattiness.** Real patients waffle about their day, neighbours and other worries. Fix: chatty personas may make short everyday asides, and Edith has scripted small talk (Frank, Doreen next door, quiz shows, her eyes). The checker allows asides that add no clinical fact.
- **Unscripted daily living (turn 24: washing, dressing, toilet).** The case had no line for Edith's own account, so the simulator improvised "I manage as I always have", and the checker rejected a similar draft. Fix: the case template requires a standard history, with each person's version of each topic:
  - each daily living activity;
  - continence;
  - stairs;
  - meals and shopping;
  - medicines;
  - mood and sleep;
  - alcohol;
  - help received.

  Anything still unscripted gets a vague in-character answer. Each gap the transcripts show gets added to the case.
- **"Interjects" label.** Janet simply adding something after Edith answers is not an interjection. Fix: label it "(adds)".

## Records (case content): Fix

- **Discharge summary.** A handwritten summary says "postural hypotension", not the lying and standing numbers.
- **GP record.** Real records differ in three ways:
  - repeat lists are longer, with a statin, eye drops and the like;
  - the problem list is long, coded, dated and cluttered with minor entries (see the clinical lead's two examples);
  - there are many past consultation entries.
- **Care agency notes.** Agencies present things as better than they are and write from a template, so they would not write "15 minutes due to staffing". The useful signal should sit among routine entries.
- **Fall found on the floor.** The agency usually calls an ambulance. Paramedics assess her (observations, ECG), decide whether it was a mechanical fall, and may leave her at home if there is no head injury. Fix: add a paramedic (ambulance) report.

## Examination: Fix

- **Weight.** There are no scales on a home visit, so weight is "not available" there.
- **Gait.** The finding gave a 19-second timed up and go although the GP timed nothing, and the number adds little. Fix: describe what is seen.
- **Kitchen.** GPs don't search the fridge. The signs come from how she looks (thin, loose clothes) and anything obvious. Fix: add a general-appearance finding, and keep the kitchen finding only for a GP who asks.

## Model under test: Score in M3, not fixed

- It read the records after starting the conversation. A GP reads them before the visit.
- Its questions were stacked and oddly worded ("change from Edith's usual thinking"). A good example from the same run: "is it light-headed when you stand, or does the room spin?"
- It did not rephrase when Edith dodged the question about where the frame was. Rephrasing is a skill.
- Its ECG request was unnecessary for clear postural hypotension. It would be fine if requested because of donepezil.
- It over-escalated:
  - same-day temporary care or hospital "if unsafe";
  - asking Janet to stay until things were safe;
  - safeguarding.

  None of these was warranted. A response should be proportionate to which missed medicines actually matter: missed donepezil is not urgent, but missed insulin or antipsychotics would be.
- **UK pathways.** Equipment comes through occupational therapy (a social care assessment or community OT), not a direct order.
- Its dietitian or weight referral was premature. She should be reweighed once meals are sorted.
- **Follow-up.** About a week is right. A home visit within 72 hours is not needed.
- **Wording.** "We can help you stay at home" implies a care home is on the table.
- **Good:**
  - flagging the risk of malnutrition and dehydration;
  - assessing care needs;
  - "Janet cannot substitute for a care package";
  - the overall structure.
- **Asking before looking round the home** (from the M2 read, 4 Nov). It examined the kitchen and fridge without asking Edith first. Looking is fine with her permission; doing it unasked breaks the relationship.
- It did not ask about Edith's or Janet's ideas, concerns and expectations. Had it asked, Janet's care-home fear would have come out naturally. Her disclosure in this run was fair, given the talk of temporary care.

## Turn budget: Note

Real consultations have more, shorter, open questions. The models stacked questions, which saves turns. Keep the budget at 40 turns, and recheck after the stacking fix.

## Human run: Note

The clinical lead has now read the case, so a run of his own would be contaminated. Skip it. The GP colleague's baseline run, and a fresh case later, cover calibration.
