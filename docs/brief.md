# Working brief

Nov 1, 2026 · @the clinical lead

Where we have got to on the clinical environments idea. Nothing here is final until we both say so.

## Thesis

The bet: AI is tested on single-visit diagnosis with cooperative patients, but real care is managing someone over time with unreliable information, under time pressure, often with no single diagnosis. We build the environment that tests and trains that.

**Scope (1 Nov).** The company builds environments for messy, longitudinal care, sold to labs that want their general models to handle it. A narrow environment still has a broad buyer: general models already know the medicine, and the headroom is in process and management. The first pack is complex older-adult needs, because that is where our edge is. It cuts across GP, geriatrics, community care, memory clinic and discharge planning:

- Function: mobility, walking aids, falls, frailty
- Activities of daily living and what the person can no longer do
- The current package of care, and whether it still fits
- Carers who give the history, sometimes inaccurately
- Conflicting information across forms, records and what the patient says
- Decline across visits, where management changes rather than a diagnosis being made

This is where your insider knowledge sits (memory clinic, home visits). It also travels: the US has the same problem in home health, assisted living and Medicare-funded care.

**What we sell.** A simulator, run through a harness. The simulator is the world the model practises in: the patient, the carer, the records and what happens after each decision, like a da Vinci console for surgical trainees or Minecraft for robots. The harness is the rig that plugs any model or agent into it, runs thousands of scenarios, records every transcript and scores it. Labs use it to train. Health AI companies use it to test their product: their AI plays the clinician, through an API or inside their own systems, and they get pass rates, failure examples and safety flags at each release. It does not care whether the model under test is one agent or several.

## Decisions

Six are agreed, six are leaning, and two are open: who buys first, and whether documentation AI companies are a first customer segment.

| Question | Current position | Status |
| --- | --- | --- |
| Build our own model? | No. Capital-heavy and the frontier keeps moving; Baichuan's gains came from the simulator and rubrics | Agreed |
| What are we? | An environment company: simulator, tools and grader as one harness | Agreed |
| First buyer | Health AI companies (testing their product) or labs (training their models) | Open |
| Clinical scope | Company: messy, longitudinal care. First pack: complex older-adult needs | Leaning |
| Target behaviour | Management over time, ahead of history-taking | Leaning |
| Experiment purpose | Both a hypothesis test and a sales sample, with failure criteria written down before running | Leaning |
| Rubric bias | A second GP rates the same cases blind | Agreed |
| Kill rule | If frontier models already handle these cases well, stop | Agreed |
| Google's multi-visit benchmark (AMIE Mx) | Proof of demand, not ground already taken | Agreed |
| UK pathways | A flavour inside cases, not the pitch | Leaning |
| Expert volume | Vendors win on volume; our edge is task and grader design | Leaning |
| Mercor as a first step | Dropped: not open to UK doctors | Agreed |
| Depth or breadth | Depth first: one deep pack, then breadth as more packs. Your contrarian view: older adults are a big enough population that labs may care about them directly | Leaning |
| Documentation AI as a first segment, global | Global from day one: scribe, summary and triage companies, mostly in the US. The UK (TORTUS, Anima, Accurx with Tandem, Heidi) is one market, with few buyers who are slow and sceptical. All face rising assurance demands; a simulator with known truth could test their notes for invented or missing facts | Open |

## Company shape (proposed 4 Nov, not agreed)

From the M1 discussion. Revisit after the pilot shows whether there is a gap.

- **One engine, sold two ways.** The same simulator, tools and grader.
  - **Training environment for labs:** many cases and variants; the grader's score is the reward.
  - **Test environment for labs and health AI companies:** a private test set the buyer never sees, refreshed regularly, giving a trusted independent score at each release.
- **Cases scale from clinician seeds.** Clinicians write seed cases from patterns they have seen, with every detail fictional. Later, AI makes variants of each seed (different medicines, personalities, records), and clinicians spot-check a sample. The v0 pilot uses 10–15 seeds written by the clinical lead, dictated or typed roughly and turned into case files by the agent.
- **Rater safeguards.** Several raters per case, blind to the model; agreement measured, so careless raters stand out; raters are not the case's author.
- **Gaming defences.** The test set stays private and is refreshed. Variants mean memorising one case does not help. The grader credits actions with reasons, not keywords. Training on the training set is intended; only the test set stays hidden.
- **Why buy ours rather than build their own.** A simulator is easy to build. What is hard to copy:
  - clinical validity: clinician-written cases, real-looking records, and a grader proven against clinician raters;
  - independence: a buyer or regulator trusts an outside test more than self-marking;
  - depth in longitudinal older-adult care;
  - a growing library of cases, transcripts and ratings.

  Risk: a big lab builds its own (as OpenAI did with HealthBench).
- **Internal tool (timed to need).** A small web app for clinicians to dictate cases, review them and rate transcripts. It doubles as the reviewer network's workspace.
  - **Cases now:** the clinical lead sends voice notes, typed notes or a Word document; the agent writes the case file and a readable case view for him to check. No tool needed.
  - **Rating in the pilot:** everything runs on the clinical lead's laptop. The second rater uses the blind rating form planned in M5: a single HTML file that opens in a browser, hides model names and saves a CSV. No hosting.
  - **A hosted web app:** only once outside reviewers join.
  - **Agent office:** a view of the patient, carer, GP and grader agents talking. A demo and pitch piece, best after the pilot has results worth showing.
- **Case types to draw on:**
  - carer burnout or a failing care package
  - self-neglect
  - delirium on dementia
  - polypharmacy or anticholinergic burden
  - Parkinson's medicine timing
  - hypos on insulin or a sulfonylurea given by carers
  - falls on anticoagulants
  - a "UTI" that is something else
  - financial or safeguarding concern
  - heart failure where the fluids and weight do not add up
  - end-of-life wishes or a ReSPECT form not followed

## Why it might be wrong

The strongest case against is that Google and the vendors are already close to this, and our case set may be too small to prove anything to a buyer.

- **Already covered.** Google has a multi-visit benchmark; labs may already train on longitudinal and functional cases in-house, where we cannot see it.
- **Models may cope.** Frontier models might already handle function, care packages and carers well. The experiment exists to find out.
- **Simulator bias.** An LLM playing a frail patient or a carer may be far tidier than reality, so failures we find could be artefacts, or real failures could be hidden. Mitigation: every run is a readable transcript, so we can audit exactly where the simulator drifts from the script, add a script checker (Baichuan's simulator has one) and fix it.
- **Rater bias.** Two clinicians from similar training may share blind spots.
- **Buyer fit.** Labs may want breadth and volume, not a deep slice of older-adult care; health AI companies may only pay for evals tied to their exact product.
- **Market size.** Older-adult care AI may have fewer funded buyers than the size of the problem suggests.
- **Vendors can copy.** If it works, Mercor-scale vendors can staff the same task type quickly.

## What we already know

The evidence so far, so this tab stands on its own.

- Labs reportedly discussed spending over $1B a year on RL environments; tasks usually sell for $200 to $2,000 each and contracts often run six to seven figures a quarter ([Epoch AI](https://epoch.ai/gradient-updates/state-of-rl-envs)).
- The field's stated bottlenecks are reward hacking, difficulty calibration and quality at scale, not writing cases ([Epoch AI](https://epoch.ai/gradient-updates/state-of-rl-envs)).
- ResidencyRL (August 2026, built on Google's Gemini) trained on 57,453 simulated encounters: adversarial diagnostic accuracy rose from 81% to 88%, missed red flags fell by about a third, and clinicians preferred it in 87.6% of blinded comparisons. Its grader stayed biased toward the trained model, and it covered only US, English, text telehealth ([summary](https://www.emergentmind.com/papers/2608.07418)).
- Baichuan-M2, a 32B open model trained with a patient simulator and rubric generator, scored 34.7 on HealthBench Hard against GPT-5's 46.2 in September 2025 ([paper](https://arxiv.org/abs/2509.02208v1)).
- BioStack Platforms (YC Spring 2026, $9.5M seed led by Peak XV) builds healthcare training environments for labs: the nearest analogue and a possible buyer ([Inc42](https://inc42.com/buzz/biostack-nets-9-5-mn-to-build-training-datasets-for-medical-ai/)).
- Mercor pays medical experts $115–150/hr but does not accept UK doctors.
- One example market, the UK, where documentation AI is scaling under assurance pressure but buyers are few and sceptical. NHS England's ambient voice technology registry is self-certified, and assurance sits with each local NHS organisation ([NHS England](https://transform.england.nhs.uk/digitise-connect-transform/digitising-the-frontline/ambient-voice-technology-self-certified-supplier-registry)). TORTUS reached UKCA Class IIa in June 2026 ([iatroX](https://www.iatrox.com/blog/heidi-tandem-tortus-nhs-avt-strategies)). Anima serves over 1,000 GP practices ([Bridgehead](https://www.bridgeheadcommunications.com/medtech-index/anima-health)), and its AI produced fabricated diagnoses for one patient in 2025 ([Fortune](https://fortune.com/2025/07/20/uk-health-service-ai-tool-false-diagnoses-patient-screening-nhs-anima-health-annie)). HSSIB has opened an investigation into ambient voice technology in hospitals ([HTN](https://htn.co.uk/?p=88031)).
- Possible move: a simulator with hidden ground truth can test whether a scribe's note or a summary invents or omits facts, so documentation AI companies anywhere are possible buyers. The US market is far larger; the UK is one reachable but sceptical example.

## Research prompt

Copy everything in the block below into a deep research run.

```
I am a UK doctor deciding whether to start a company that builds clinical AI environments: a patient simulator, clinical tools and a grader, packaged as a harness any model or agent can plug into. Labs would use it to train models with reinforcement learning; health AI companies would use it to test their products.

My thesis: clinical AI is mostly tested on single-visit diagnosis with cooperative patients. Real care, especially for older adults with complex needs, is managing someone over time with unreliable information (carers, conflicting records), under time pressure, often with no single diagnosis. Function, mobility, frailty, activities of daily living and packages of care matter more than the diagnosis. I believe this is under-tested and under-trained. The company would build environments for messy, longitudinal care in general, with older-adult complex needs as the first pack.

Research the following, as of November 2026, in the US and UK. Cite every factual claim with a link, date each source, and label your own opinion or estimates clearly.

1. Existing benchmarks and environments. Which clinical AI benchmarks or RL environments (for example AMIE and AMIE Mx, HealthBench, MedHELM, AgentClinic, CRAFT-MD, ResidencyRL, ClinEnv, DiagGym, MedAgentBench, and any newer ones) test: functional assessment and ADLs, frailty, falls, care packages and social care, carers or other third parties in the conversation, conflicting information, multi-visit or longitudinal management, and cases with no single diagnosis? For each: what it covers, how it grades, how big it is, and what gaps its authors admit. Present as a table.

2. How buyers evaluate today. How do frontier labs and health AI companies currently evaluate and post-train clinical models? Who supplies them (for example BioStack Platforms, Mercor, Surge, Turing, Handshake, micro1, Medcase, AfterQuery, others)? What do they buy (tasks, rubrics, environments, evals), at what prices, under what contract terms and security requirements, and how fast do they decide?

3. Health AI companies in older-adult care. List companies in the US and UK building AI for home care, care homes, assisted living, care coordination, dementia, falls or discharge planning. Note funding, stage and whether they publish or need clinical evaluations.

4. Regulatory and policy drivers that create demand for clinical AI evaluation: FDA, MHRA, EU AI Act, CMS, CQC, NHS England and anything relevant to older-adult or social care AI.

5. State of the art, papers first. Identify the 15 to 20 most important papers from 2024 to 2026 on clinical patient simulators, RL and post-training for clinical models, interactive and multi-visit clinical benchmarks, LLM-judge and rubric validation, and reward hacking. For each give the contribution, method, headline result, admitted limitations and whether code or data is released, ranked by relevance to my thesis. Also cover: patient simulators with third parties and memory across visits; known reward hacking in clinical RL; how graders are validated against clinicians (inter-rater agreement, calibration); open-source tooling for building environments.

6. Clinical documentation and triage AI, US first and UK second: ambient scribes, clinic and discharge summaries, document processing and triage (the leading US ambient scribe and documentation companies, plus UK players such as TORTUS, Anima, Accurx with Tandem, Heidi and others on the NHS England ambient voice technology registry). How are these products evaluated today? What do US regulators and assurance schemes require, and what do NHS England, the MHRA, HSSIB and the Welsh ambient voice framework require? Does any shared, simulation-based test harness exist for US or UK settings? Would these companies pay for one, who decides, and how fast?

7. Demand signals from 2025 to 2026: funding rounds, acquisitions, job posts and lab announcements about healthcare RL environments or clinical evals.

8. The strongest arguments that this thesis is wrong or the business would fail.

9. Ten specific companies or people worth contacting first, with why each.

Format: a structured report with tables, an executive summary of no more than 200 words at the top, and a final section listing what remains unknown.
```

## Next

1. Run the research prompt and bring the report back.
2. Discuss together: settle the first buyer, confirm scope and target behaviour, and agree the experiment design and kill criteria.
3. Write the final plan in this tab, marked agreed.
4. Hand the plan to Claude to execute.
