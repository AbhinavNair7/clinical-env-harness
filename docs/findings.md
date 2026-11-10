# Can a frontier model manage a frail older adult? Findings from clinical-env

November 2026. Clinical lead: a UK doctor. Engineering: AI coding agents.

## The question

AI clinicians are usually tested on one visit with a cooperative patient and a single right
diagnosis. Real general practice for older adults rarely looks like that:
- the person who knows the most is often a carer, who may be wrong or holding something back;
- the records disagree with each other and with what people say;
- there's often no single diagnosis, so the job is managing function, falls, medicines and care
  over several visits.

We set out to find out whether frontier models fail at this. If they did, a company could sell
the environment that exposes and trains it. If they didn't, we would stop.

## What we built

A simulator in which the model under test plays the GP across 2–3 home or clinic visits. It
can talk to a simulated patient and carer, read real-looking records, examine, and submit a
plan.
- Each person holds facts that are true, wrong or out of date. Some they volunteer, some they
  give only if asked, and some only if asked the right thing.
- A checker stops the simulated people leaking secrets or making things up.
- A grader scores each plan against a clinician-written rubric. Its quotes are checked against
  the transcript, so it can't credit something that never happened.

Every test had its pass/fail rule committed to Git before the first paid run.

## What we found

**1. On the things that change outcomes, the flagship didn't fail.** gpt-6-astra met every
critical item in 39 of 39 runs across 10 case variants (the pre-registered feasibility tests,
3 runs each; item 4 shows what 10 repeats of one case add). Some examples:
- A wife insisted her husband hadn't lost weight. It weighed him every time and found the loss.
- A carer insisted her husband's head had been scanned. It checked the letter, found no scan,
  and ordered one.
- After a clear workup for anaemia, it held back from more tests and reassured her properly.
- It asked a dying man what mattered most to him, unprompted, in 3 of 3 runs.
- It found a husband's undisclosed knee operation by asking about his own health, with or
  without a cue, and even with the cue buried in clutter.

**2. Its gaps were consistent but small.**

| Gap | How often, without help |
| --- | --- |
| Never asks "what would you like to cover today?" | 0 of 72 visits asked |
| Rarely asks the patient's own ideas, concerns and expectations | 5 of 72 |
| Vague local service routes ("refer to social care") | most US-case runs |
| Missed a prescribing cascade | 9 of 9 runs |

The cascade is the most interesting miss. Pat's urgency started after donepezil, and
oxybutynin was added to treat it. The model stopped the oxybutynin for good reasons in every
run, and it even noted that oxybutynin opposes donepezil. It never turned that round to ask
whether donepezil caused the urgency in the first place. It fixed the downstream drug and
stopped there.

**3. A thin harness fixed most of the gaps.** We added eight generic lines to the model's
instructions, written to apply to any older-adult visit and naming nothing from the cases. On
three cases rerun:

| Item | Without | With the 8 lines |
| --- | --- | --- |
| Asks the agenda | 0 of 24 visits | 22 of 24 |
| Asks ideas, concerns and expectations | 0 of 24 | 24 of 24 |
| Considers donepezil as the cause | 0 of 9 | 3 of 3 |
| Includes a stool test for occult blood | 0 of 3 | 2 of 3 |
| Adds the carer to the carers register | 0 of 9 | 0 of 3 |
| Offers a rectal examination† | 0 of 3 | 0 of 3 |

The knowledge was there; it just wasn't being applied unprompted. What a generic prompt can't
reach is local practice convention, such as a UK carers register.

† When we checked this item against the guidance, it did not hold up. Current NICE NG12 (2023)
says to offer a faecal immunochemical test in iron-deficiency anaemia and mentions rectal
examination only for a rectal mass, and the 2021 British Society of Gastroenterology guideline
does not recommend one. The model's FIT-led plans follow today's guidance; our rubric reflected
older practice. That makes it a rubric defect, not a model gap, and leaves 2 of the 3 genuine
misses fixed by the prompt.

**4. Real documents fixed the convention. A first alarm about side effects did not
replicate, but it showed how much one decision varies between runs.** The carers register was
the one gap a prompt could not reach, so we tested whether access to the knowledge would. We put
two real UK documents in the prompt (NICE quality statement QS200 on identifying carers, and an
NHS integrated care board page on registering as a carer). The first test was 3 runs per arm.
Its result looked alarming, so we pre-registered a rerun with 10 runs per arm.

| Item (Pat) | Thin harness | Thin harness + documents |
| --- | --- | --- |
| Carer added to or offered the carers register | 0 of 3, then 0 of 10 | 2 of 3, then 6 of 10 |
| **Critical: arranges care cover while the carer is in hospital** (grader) | 3 of 3, then 9 of 10 | 0 of 3, then 8 of 10 |
| Cover, blind read of the 10 + 10: refers to social care that day | 9 | 6 |
| ... settles for a dated care-coordinator call instead | 1 | 4 |
| ... arranges nothing | 0 | 0 |

Three things follow.
- **The documents fix the convention** (6 of 10 vs 0 of 10). Local practice knowledge is a
  retrieval problem, not a model failure.
- **The side effect did not replicate** (9 vs 8 of 10). The first 0 of 3 was a bad batch,
  about a 1% chance at the true rate. Three runs made us over-read it.
- **The decision itself varies between runs.** Same model, prompt and case: most runs refer the
  carer to adult social care that day, and some settle for a care-coordinator call the next day.
  Both are defensible steps, but the grader passed one and failed the other. In every one of our
  earlier 3-run tests, no critical item ever changed between runs. At 10 runs this one does, in
  both arms. The documents may push towards the softer step (4 vs 1 of 10), but that is within
  chance at this size.

For anyone deploying a model in care: judge it on the worst of many runs, not on three, and
test whether retrieved context moves its safety decisions. The documents were placed in the
prompt, which is a best case for retrieval.

**5. Why published benchmarks report failures we didn't see.** Most papers that show frontier
models failing use at least one of these:
- **weaker or base models**: ResidencyRL's 65.5% missed-question rate is its base model;
- **dense partial-credit rubrics**: HealthBench Hard tops out near 46% because each prompt has
  many small items; our case scores of 50–96% would read as "failing" on that scale;
- **sources that lie with no paper trail**: MedDialBench's inventing patient cuts accuracy by
  19–31 points;
- **thousands of cases**: a 10% failure rate is invisible in a few dozen runs;
- **memory over very long horizons**.

We deliberately tested fair, well-documented cases, because that's what a buyer would ask
about first. On those, the flagship is good.

**6. A second test on judgement calls found differences of style, not errors (9–10 Nov).**
After the first close-out we tried a different angle. The clinical lead wrote memory-clinic
cases around one pattern: a model taking the defensible default over the call that fits this
patient. All the cases are fictional. They are inspired by clinical experience and contain no
real patient details. The case files are withheld as a private, held-out test set, so
future models cannot be tuned against them; the task, grader and every result are published.
The task was simpler than the simulator: read one patient's documents and
write the pre-review brief or clinic letter. Each scored case had a twin with one or two facts
changed so that the default answer was right, so a model could not pass by always deviating.
gpt-6-astra ran each file 10 times under a rule frozen beforehand.

| Pair (theme) | Base runs failed | Twin runs failed |
| --- | --- | --- |
| A fixed false belief alongside memory problems | 6 of 10 | 0 of 10 |
| Cognitive testing soon after seizures | 10 of 10 | 4 of 10 |
| Acute confusion: delirium or not | 0 of 10 | 0 of 10 |
| Family help: decline or lifelong habit | 0 of 10 | 0 of 10 |
| Dementia or mild impairment, judged on function (own rule) | 1 of 10 | 0 of 10 |
| Control | 0 of 10 | n/a |

By the rule the result was **inconclusive**: one pair met the bar where two were needed. The
clinical lead then read every failed item, and most turned out to be faults in the mark scheme:
- The 6 fails in the first pair were hedged answers to a case he judged genuinely ambiguous.
- The 10 fails in the second were a conditional mention ("consider if still unsure") of a test
  the mark scheme banned outright.
- Two knowledge items were wrong in the mark scheme, and the model's reading was sound.

What was left after review:
- **More tests by default in the very old.** It proposed repeat brain imaging in 10 of 10 runs
  where the clinical lead would not scan. Guidance allows either, so this is a difference of
  judgement, not an error.
- **Hedged commitment.** It names a "leading consideration" where a clinician would commit.
- **One real knowledge gap.** It missed the driving rules for insulin in 8 of 10 runs.

The clear threshold errors the cases were built around did not appear. A mark scheme written
from one clinician's notes failed sound answers more often than the model failed patients.
What separates the model from a given clinician here is style within the guidelines, and
clinicians differ from each other in the same way.

## What this means

- **For clinical AI evaluation:** on fair cases, the frontier is past "does it get the
  management right". The open problems are scale, adversarial sources, local knowledge, and
  whether plans hold up when the consequences play out.
- **For builders of AI clinicians:** a short consultation scaffold and a medicines check close
  most of the gap at almost no cost. Local pathway knowledge is a data problem, not a prompting
  problem.
- **For this project:** case reports are the wrong raw material for finding failures. They're
  coherent by design. Failures, if they exist at scale, are more likely in real consultation
  recordings and real records. Without those, we stopped. The second test (item 6) pointed the
  same way, and the project closed on 10 November 2026.

## Limits

- **One lab's flagship.** Gemini and Claude were not run, because the pre-registered rule
  said to stop first.
- **A same-lab grader.** The judge was also an OpenAI model. Flagged critical misses were
  reviewed by the clinical lead; non-critical verdicts mostly were not.
- **Small numbers.** 10 case variants and 3 runs each find consistent behaviour, not rare
  failures. Ten repeats of one case found a 10 to 20% miss rate on a critical that 3 runs hid.
- **Simulated people are language models.** They're tidier than real patients, even with the
  checker and the noise test.
- **The rubrics are our own.** Some misses, such as the carers register, are UK conventions
  rather than errors of care, and one (the rectal examination) did not match current guidance.
- **One clinician wrote and reviewed the memory-clinic mark scheme.** No second clinician rated
  those cases, and one item (conditional neuropsychology) was never ruled on.
- **Checks by an AI agent, not a second clinician.** The re-check of the thin-harness verdicts
  was an AI pass over the raw transcripts. The clinical lead has not yet reviewed the three
  critical misses in the documents test.

## Where to look

- Every run and verdict: [feasibility-dev.md](feasibility-dev.md).
- Every decision and pre-registered rule: [DECISIONS.md](../DECISIONS.md).
- The literature and market analysis: [research-summary.md](research-summary.md),
  [pivot-options.md](pivot-options.md).
