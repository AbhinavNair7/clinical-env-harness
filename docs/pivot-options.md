# Stop or pivot (6 Nov 2026, draft for discussion)

## What we saw

gpt-6-astra (high effort) met every critical in 18 of 18 dev runs: 4 dev cases plus 2
negative-workup cases (Walt, Dot), 3 runs each (`docs/feasibility-dev.md`). It caught every
confidently wrong carer (it weighed Ray, checked Gene's memory-clinic letter). It declined
Karen's PET scan and did not falsely reassure after negative scopes.

Weak in every case and run (non-critical): never asks the agenda or ideas, concerns and
expectations (ICE); vague local service routes; some over-investigation (Walt's CT and GI
consult, 9 over-provision penalties in 12 runs); repeats "don't drive" without asking whether
Harold drives.

## How the papers found failures when we didn't

Almost none show a frontier model failing at careful management of a well-documented case.

| Lever | Example | Did our cases use it? |
| --- | --- | --- |
| Weaker or base models | ResidencyRL's 65.5% missed critical question is its *base* model; Baichuan-M2 vs GPT-5 | No: we tested the flagship |
| Dense partial-credit rubrics | HealthBench Hard: best model ~46% because each prompt has many soft items | Partly: our 44–96% case scores would read as "fails" there; go/stop counts criticals only |
| A source that lies with no paper trail | MedDialBench: an inventing patient cuts accuracy 19–31 points; false drug premises accepted up to 100% | No: every wrong carer could be checked against a record or an examination, and was |
| Truth reachable only by asking | ResidencyRL hidden facts; base model 1.3/5 on social history | Rarely. Where it was (ask Janet; is Harold driving?) the model missed it |
| Scale and the hard slice | ResidencyRL's adversarial set, SUP-MIMIC; thousands of cases | No: a 10% failure rate is invisible in 18 runs |
| Memory over long horizons | ClinTraceBench: agentic memory recovered 0–5% of planted facts | No: our visits fit in context |

Reading: our result fits the literature. The flagship is excellent at **reconciling documents
and examinations** and at **restraint after a negative test**. Its consistent gaps are in
**people** (what they want, what they didn't say, what a carer saw) and **local knowledge**.

## What the annotation vendors actually do

Mercor, Surge, Scale/Outlier, Invisible, Turing, Handshake, micro1, Alignerr, DataAnnotation
and similar mostly sell **expert hours** (Mercor bills about 35% on top of pay): rank A vs B,
write ideal answers and per-prompt rubrics, red-team, "stump the model", lately RL
environments (Mercor bought Deeptune, Jul 2026). Appen, Telus, Welocalize, RWS, Lionbridge,
OneForma are mostly volume labelling and localisation.

Structural gaps in that model:
1. **Answer-only grading.** Rubrics mark the reply, not what the model should have asked.
2. **US-centric supply.** US board certification; Europe hard to get into. NHS and social-care
   routes are thin.
3. **No consequences.** Nobody sees what happened next.
4. **Disagreement averaged away** (HealthBench: doctors disagree a lot).
5. **Throughput incentives** reward fast, gradable items over slow cases with hidden state.

## Contrarian bets

| # | Bet | Status |
| --- | --- | --- |
| A | **People, not paper.** The fact that changes the plan lives only in a person's head and comes out only when asked (agenda, ICE, a specific question). Nothing written contradicts it | Untested. Our cases always left a paper trail |
| B | **Do less.** Reward restraint | **Tested, passed** (Walt, Dot). Mild over-investigation only, non-critical |
| C | **UK local routes as the moat** | Untested as a critical; weak as a lab sell, maybe a UK-buyer sell |
| D | **Consequences.** Plans change later visits; score outcomes | Large build; v0 events are fixed |

## Result (6 Nov)

Bet A was run under a frozen rule (DECISIONS, 6 Nov): 2 cases where the decisive fact is held
only by a person, plus a written twin, 9 flagship runs. **Every critical met in all 9 runs**
(`docs/feasibility-dev.md`), so the rule says **stop completely**. The flagship asked "what
matters most to you now?" unprompted, and picked up a wife's "his leg's bad" to find the
husband's operation. Its gaps (agenda, ICE, carers register) are real but cost points, not
plans.

The clinical lead's follow-up idea, that thin text gives cues away, was tested too: Pat with realistic
clutter, 3 runs, every critical met; the flagship asked about the carer's health without any cue
and ignored the clutter. Stop stands.

## Sources

- [HeroHunt: top 10 human data providers 2026](https://www.herohunt.ai/blog/top-10-human-data-providers-full-in-depth-review/)
  (promotional; Mercor coverage not neutral)
- [HeroHunt: Mercor vs Surge vs Scale buyer guide](https://www.herohunt.ai/blog/mercor-vs-surge-vs-scale-ai-2026-buyer-guide/)
- [Surge AI (Wikipedia)](https://en.wikipedia.org/wiki/Surge_AI), [Mercor (Wikipedia)](https://en.wikipedia.org/wiki/Mercor)
- Papers: `docs/research-summary.md`; dev results: `docs/feasibility-dev.md`
