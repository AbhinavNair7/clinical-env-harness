# Research summary (3 Nov 2026)

The gap is real but narrow. No published benchmark tests function, carers, conflicting records and no-single-diagnosis together, and none of the closest systems has public code. Google's ResidencyRL paper names caregivers and multi-visit training as future directions, so the window is open but short.

## Is the code public?

| System | Code | What is public | Use for us |
| --- | --- | --- | --- |
| [ResidencyRL](https://arxiv.org/html/2608.07418) (DeepMind, Aug 2026) | Closed. Internal Google infrastructure; safety cited | Full method, reward weights and penalties. Rubric specs promised later | Design template for our simulator and grader |
| [AMIE Mx](https://www.nature.com/articles/s41586-026-10764-5) (Google, Nature, Jun 2026) | Closed | [RxQA](https://github.com/google-health/rxqa) medication benchmark. ResidencyRL lists the AMIE Mx scenarios as open data; not yet confirmed | Format reference for UK multi-visit cases, if downloadable |
| [MIRA](https://www.nature.com/articles/s41586-026-10675-5) (Kather lab, Nature, Jun 2026) | Reported on GitHub | Sandboxed FHIR record with 11 tools. Single emergency visit on MIMIC-IV | Reference for record tools only |
| [AgentClinic](https://arxiv.org/pdf/2405.07960) | Open | Patient and measurement agents | Reference simulator |
| [verifiers](https://github.com/PrimeIntellect-ai/verifiers) (Prime Intellect) | Open | Environment library and hub. v1 API still changing in 2026 | Packaging target after the pilot |

## Main papers

| Paper | Result | What it means for us |
| --- | --- | --- |
| ResidencyRL (DeepMind, Aug 2026) | RL on 57k simulated single-visit encounters. Adversarial diagnosis 81% to 88%, missed red flags down a third, AMIE Mx management 80% to 88% | Closest threat. Base model scored 1.3/5 on social history and missed a critical question in 65.5% of adversarial cases, so headroom exists |
| AMIE Mx (Google, Nature, Jun 2026) | 3 visits, 100 scenarios. Non-inferior to 21 PCPs, better guideline alignment | Multi-visit is published. No carers, no function |
| MIRA (Kather lab, Nature, Jun 2026) | Agent in a sandboxed record; 88.9% diagnostic accuracy on 574 ED cases | Record tools work. Single visit, no carers |
| HealthBench (OpenAI, May 2025) | 5,000 conversations, 48.5k rubric items, grader F1 0.71 | Bar for grader validation |
| Baichuan-M2 (Sep 2025) | 32B open model with simulator and rubrics: 34.7 vs GPT-5's 46.2 on HealthBench Hard | Simulators and rubrics drive the gains |
| ClinTraceBench (Sep 2026) | Agentic memory recovered 0 to 5% of facts planted across visits | Models lose information between visits |
| DemMA / T²-GRPO (Jun 2026) | RL environment for dementia caregiver agents | Nearest older-adult neighbour |
| GrandGuard (ACL 2026) | LLMs mishandle elderly-specific risks in over 50% of cases | Older-adult failures exist |
| Rubric hacking papers (2026) | Naming an item earned +7.3 points; dropping a critical recommendation cost only 0.9 | Long care plans are easy to game |

## What to copy from ResidencyRL
1. **Patient simulator.** One call per turn. Facts are volunteered or only given if asked; hidden facts come out only to a specific question. Answers only the first of several questions, under about 50 words. Each reply checked against failure modes: leaking reasoning, being too cooperative, knowing more than the patient would. Never sees the doctor's tool calls or the rubric.
2. **Grader.** One judge call per rubric group, structured output, ground truth attached. Management outweighs diagnosis (3/9 vs 2/9).
3. **Penalties.** Invented clinical facts cost 2. A contraindicated action, missed red flag or under-triage each cost 3.
4. **Turn budget.** A penalty starts at 30 turns. Without it the agent asks everything.
5. **Grader bias.** Their grader favoured the trained model. Ours must be checked against clinicians before we trust it.

Their stated gaps are our wedge: single visits only, US English text telehealth, no caregivers or other parties.

## Market
- RL tasks sell for $200 to $2,000 each; complex environments about $300k; exclusivity 4 to 5 times more.
- Big-lab contracts reach seven figures a quarter; smaller labs $300k to $500k.
- Halluminate: 9 people, $30M Series A, says 4 of the top 5 US closed labs pay it.
- Direct competitors: Archangel Health (YC F2026), Arcophos, BioStack ($9.5M), Mercor (bought Deeptune).
- Regulatory pull is weak: FDA's Aug 2026 paper is non-binding; MHRA took documentation-only scribes out of device rules in Jul 2026; HTI-5 dropped model cards.

## Population or mechanism? (3 Nov 2026)

Question: is "frontier models fail" a property of older adults or of conflicting sources over time? Answer: the parts of the mechanism fail in general adult data; nobody has tested them together or compared populations. Most items below are 2025–26 preprints read at abstract level.

| Paper | Result | What it means for us |
| --- | --- | --- |
| [MedDialBench](https://arxiv.org/html/2604.06846v1) (preprint, Apr 2026) | 5 frontier models. A patient who invents facts cuts diagnostic accuracy 19–31 points; withholding only 6–14. Invented facts combined with other behaviours are super-additive. Robustness does not track baseline skill | Strongest evidence that unreliable narrators break models. Single visit, diagnosis only |
| [SUP-MIMIC](https://arxiv.org/abs/2608.29582) (preprint, Aug 2026) | Accuracy drops on contradictory evidence; bias towards "healthy" (missed problems) | Conflicts cause misses, not over-calls |
| [MedDistractQA](https://arxiv.org/abs/2504.01201) (preprint, Apr 2025) | Irrelevant statements, including a family member's symptoms, cut accuracy up to 17.9% | Proxy-history confusion is plausible |
| [Chen et al., npj Digit Med](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12534679/) (Oct 2025) | Models comply with false drug premises up to 100% of the time | Models will act on a wrong record or carer claim |
| [LongMedBench](https://arxiv.org/html/2607.09322) (MICCAI 2026), [PsychiatryBench](https://www.nature.com/articles/s41746-026-02582-w) (2026) | Weak temporal reasoning across visits; largest gaps in multi-turn follow-up | Longitudinal weakness is general |
| AMIE Mx (Nature, Jun 2026; secondary sources) | Purpose-built system non-inferior to PCPs over 3 clean visits | Multi-visit alone may not cause failure; unreliable sources are our difference |
| [CARE-Bench](https://arxiv.org/html/2608.03731v1) (preprint, Aug 2026) | 85 caregiver and 53 paediatric cases of 500; authors say too few for subgroup claims | No usable evidence on proxy historians anywhere |
| [Med rec scoping review, JMIR](https://pmc.ncbi.nlm.nih.gov/articles/PMC13160534/) (2026) | 94 studies: 2 detect discrepancies, none resolve them | Discrepancy resolution is untested |
| [Deprescribing, JMIR Aging](https://aging.jmir.org/2025/1/e69504) (2025) | Finds criteria (PPV 0.83), applies them badly to the patient (PPV 0.47) | Individualising is the weak step |
| [PedMedQA](https://publications.aap.org/pediatricsopenscience/article/1/2/1/201957/PedMedQA-Comparing-Large-Language-Model-Accuracy), [PediatricsMQA](https://arxiv.org/html/2508.16439), [biomarker study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12559286/) (2025) | Age-group differences on knowledge QA are small and point both ways | No sign failures are population-specific |
| [McBain et al., Psychiatric Services](https://www.rand.org/pubs/external_publications/EP71040.html) (Aug 2025) | Chatbots inconsistent at intermediate suicide risk | Mental health cases mix safety-policy refusals into "failure" |
| [HealthBench disagreement](https://arxiv.org/pdf/2602.22758) (preprint, Feb 2026) | Physician specialty did not reduce disagreement; ambiguous wording did increase it | GP raters plus specialist rubric sign-off beat specialist raters |
| [Miller, Adding error bars to evals](https://arxiv.org/abs/2411.00640) (Nov 2024) | Clustered standard errors can be 3× naive ones | The case is the unit; runs and models are not extra cases |

Design conclusions (opinion, agreed 3 Nov; see `DECISIONS.md`):
- Swapping 3 non-older-adult cases into the pilot supports no inference: k/3 gives 95% intervals about 70 points wide, and only the single most extreme pattern reaches p < 0.05. It also dilutes the frozen go/stop.
- To test cause, vary the mechanism within a case (a consistent-sources twin), not the population.
- Population ranking for this mechanism: frail older adults, adults with a learning disability, severe mental illness, palliative care, homelessness or substance use, young-adult chronic disease, paediatrics (mostly surface resemblance; real conflicts are safeguarding thresholds).
- A population contrast needs about 15–20 matched pairs to detect a difference and about 100 cases per population to claim generality.
