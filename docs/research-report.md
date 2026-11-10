# Clinical AI Environments for Messy, Longitudinal, Older-Adult Care: Market, Evidence and Viability (US/UK, November 2026)

**Bottom line:** The gap you describe is real. No published benchmark or RL environment found in this research jointly tests functional status/ADLs, frailty and falls, care packages, carers as third parties, conflicting records, multiple visits and cases with no single diagnosis. But the business is only viable as a narrow, evidence-led wedge. Frontier labs, Google above all, are already building longitudinal clinical simulators in-house. Data vendors are bundling "healthcare environments" into expert-hour contracts. And no regulator yet requires simulation-based testing. [Opinion]

## TL;DR
- **The gap is real but narrowing fast.** Google's AMIE Mx (Nature, June 2026) and ResidencyRL (arXiv, Aug 2026) already cover multi-visit management and adversarial simulated patients. Even so, no benchmark found tests ADLs, frailty, care packages, carers and conflicting records together. Older-adult complex care is still an open niche. [Opinion]
- **Buyers exist and pay well, but procurement favours incumbents.** Labs pay roughly $200–$2,000 per RL task and up to about $300,000 for complex environments (Epoch AI's Jan 12, 2026 FAQ, based on 18 interviews, plus SemiAnalysis-reported figures). Mercor's specialty physician listings pay about $130–$400/hour; Built In reports primary care at $130–$170/hour. Bloomberg (Oct 16, 2026) puts Mercor's average at $110/hour; its $400 figure was for civil rights attorneys. Epoch AI quotes an RL environment founder saying contracts "are often seven figures per quarter or more." Environment talent is being absorbed: in Sept 2026 Google DeepMind completed a license-and-hire talent deal with Mechanize. Talks had been reported at more than $1.5B, final terms were undisclosed, and Mechanize was not bought outright. The best route in is a credible open benchmark followed by paid custom packs, not a cold sale of a platform. [Opinion]
- **Regulatory pull is emerging, not mandatory.** FDA's Aug 18, 2026 discussion paper names "standardized patient interactions" and benchmarking as evidence approaches. MHRA (July 29, 2026) moved documentation-only scribes out of medical-device regulation, and ONC's HTI-5 (Oct 26, 2026) removed model-card requirements.\[1\]\[2\] Scribe vendors therefore face less compulsion, not more, to buy third-party simulation testing. Start part-time with a validated open pack and clear kill criteria, and only then go full-time. [Opinion]

## Executive summary (≤200 words)
Clinical AI evaluation has moved quickly from single-visit diagnosis toward multi-visit, interactive and RL-based testing:
- AMIE Mx: 100 multi-visit scenarios, 21 primary care physicians, Nature 2026.\[3\]\[4\]
- ResidencyRL: about 57,000 simulated scenarios, up to 60 turns, Aug 2026.\[5\]
- Longitudinal memory benchmarks such as ClinTraceBench and MedLoCoMo (2026).\[6\]\[7\]

None of these, as described, centres function, frailty, social care packages, carers or unreliable records. Older-adult work is fragmented: GrandGuard covers safety prompts and DemMA covers a dementia-caregiver environment.\[8\]\[9\]

Demand signals are strong:
- OpenAI and Anthropic both launched healthcare products in January 2026.\[10\]\[11\]\[12\]
- Mercor is recruiting board-certified specialists "in partnership with a leading AI lab" (Oct 2026).\[13\]
- RL-environment startups are raising money (Halluminate, $30M, Oct 2026) or losing staff to labs (Mechanize's talent deal with Google DeepMind).

The risks are severe. Labs build in-house. Vendors like Mercor already pitch healthcare environments. Health-specialist entrants already exist (Archangel Health, Arcophos).\[14\]\[15\] UK and US scribe deregulation weakens compliance-driven demand.

[Opinion] Viable as a part-time wedge: an open, clinician-validated "complex older adult" pack with a validated grader, sold first to frontier lab health teams and health AI evaluation leads. Founder time and grader validity are the binding constraints.

---

## 1. Existing benchmarks and environments

### 1a. Coverage matrix
Coverage ratings are the researcher's assessment from published descriptions [Opinion]. Y = explicitly covered; P = partial or incidental; N = not described; ? = not verifiable here.

| Benchmark / environment | ADLs / function | Frailty / falls | Care packages / social care | Carers / third parties | Conflicting info | Multi-visit / longitudinal | No single diagnosis | Grading method | Size | Admitted gaps | Source & date |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AMIE (diagnostic) | N | N | N | N | N | N | N | Specialist and patient-actor ratings in a virtual OSCE | Text consultations vs primary care physicians [background knowledge, not re-verified] | Simulated text chat, not real-world | Nature, 2025 |
| AMIE Mx (disease management) | P | N | N | N | P (information revealed incrementally) | Y (3 visits) | P | Blinded specialist rating of appropriateness, completeness, precision, guideline alignment; RxQA medication benchmark | 100 multi-visit scenarios, 5 specialties, 21 primary care physicians, NICE/BMJ Best Practice | "Art-of-the-possible demonstration… simulated settings with patient actors" | Nature, June 17, 2026\[4\]\[16\]\[17\] |
| HealthBench | P (incidental) | P | N | P (some conversations with lay users/carers) | N | N (static multi-turn) | P | Physician-written rubric per conversation, graded by GPT-4.1 | 5,000 conversations, 262 physicians, 48,562 criteria | Static offline conversations; grader inherits model biases (PMC commentary, 2025) | OpenAI, May 2025\[18\]\[19\] |
| MedHELM | ? | ? | N | N | N | N | ? | LLM-jury; ICC 0.47 vs clinicians (clinician–clinician 0.43) | 121 tasks, 5 categories, 22 subcategories | Not extracted | Stanford, 2025 (as summarised in arXiv 2607.02175, 2026)\[20\] |
| AgentClinic | N | N | N | N | P (biased patient/doctor agents) | N | N | Diagnostic accuracy | Cases from 9 specialties; 749 cases in 7 multilingual environments | Simulated agents | arXiv v5, May 27, 2025\[21\] |
| CRAFT-MD | N | N | N | N | N | N | N | Diagnostic accuracy in simulated conversation | Large vignette set [background knowledge, not re-verified] | Models degrade in conversation vs vignettes | Nature Medicine, 2025 [not re-verified] |
| ResidencyRL | P | ? | N | ? | Y (hidden information, adversarial patients) | P (evaluated on AMIE Mx) | P | Hierarchical rubric autorater (6 dimensions plus safety flags); 97-case clinician side-by-side | 57K generated scenarios (arXiv:2608.07418, Liévin, Schmidgall, Strother, Bijamov et al.); up to 60 turns and 8 tool calls | "Prospective validation… remains necessary" | Google DeepMind, arXiv Aug 7, 2026 |
| DiagGym / DiagBench | N | N | N | N | N | N | N (diagnosis-terminal) | Diagnostic accuracy and exam-recommendation match | 750 cases; 99 with 973 physician rubrics | Diagnosis-focused | arXiv, Oct 2025\[22\] |
| MedAgentBench | N | N | N | N | N | N | P | Task success in a FHIR EHR environment | Hundreds of tasks [background knowledge, not re-verified] | ? | Stanford, 2025 [not re-verified] |
| ClinEnv | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | Not located in this research |
| ClinTraceBench | N | N | N | N | P | Y | P | Source-verifiable QA | 6,271 questions; 8 memory strategies × 4 backbones | Compression loses relations; Mem0/A-Mem recover 0–5.3% of injected positives | arXiv, Sept 2026\[6\] |
| MedLoCoMo | N | N | N | N | P | Y (multi-admission) | P | Open-answer QA including abstention | 100 timelines, about 74,512 tokens each | EHR-derived QA, not interactive care | arXiv, July 2026\[7\] |
| ClinicalMC | N | N | N | N | N | Y (admission to discharge) | P | Multi-agent (patient/examiner/doctor) | Chinese and English datasets | ? | arXiv, June 2026\[23\] |
| MedDialBench | N | N | N | N | Y (adversarial patient behaviours) | N | N | Diagnostic robustness | ? | ? | arXiv, Apr 2026 |
| GrandGuard | P | P ("mocking frailty") | N | N | N | N | N | Safety labels | 10,404 prompts/responses | Single-turn safety | ACL Findings, 2026\[8\] |
| Late-life depression benchmark | P | P (frailty, functional decline, self-neglect domain) | P (caregiver support) | Y (30 of 90 questions from carers) | N | N | P | Blinded clinician rating | 90 questions, 3 LLMs | Small; Q&A only | Frontiers in Psychiatry, 2026\[24\] |
| DemMA / T²-GRPO (caregiver agents) | P | ? | ? | Y (agent is the caregiver) | ? | ? | Y (care, not diagnosis) | Environment-emitted turn rewards from behavioural annotations | ? | ? | arXiv, June 2026\[9\] |
| Arcophos Clinical Benchmarks Index | ? | ? | ? | ? | ? | P ("patient follow-up") | ? | Aggregates public benchmarks | 150 models, 25 labs, 10 boards | Self-described | arcophos.com, Oct 23, 2026\[15\] |

**What this means [Opinion]:**
- Longitudinality is no longer a differentiator. Google has published it in Nature and trained on it with RL.
- Your defensible wedge is the combination that nobody publishes together:
  - function and ADLs, frailty and falls, and care packages as primary outcome targets;
  - carers and conflicting records as structured sources of noise;
  - "no single diagnosis" as the default case.
- Strongest adjacency: the DemMA caregiver environment.
- Biggest threat: ResidencyRL. Its curriculum (hidden information, adversarial patients) could absorb an older-adult scenario family cheaply.

## 2. How buyers evaluate and post-train today

**What labs do in-house:**
- **Google/DeepMind** runs the most visible clinical simulation programme: AMIE, AMIE Mx and ResidencyRL. ResidencyRL trained Gemini 3.5 Flash with GRPO against LLM patient simulators and an LLM autorater, then validated with board-certified clinicians (arXiv, Aug 2026).\[25\]
- **OpenAI** built HealthBench with 262 physicians (May 2025).\[18\] It says it works with "hundreds of physician advisors across 60 countries" to train and evaluate health features (Fierce Healthcare, July 24, 2026).\[26\] ChatGPT for Healthcare was evaluated "through physician-led testing across benchmarks, including HealthBench and GDPval" (Axios, Jan 8, 2026).\[27\]
- **Anthropic** launched Claude for Healthcare on Jan 11, 2026, on Opus 4.5, "trained specifically for healthcare and life sciences tasks" (Fierce Healthcare, Jan 11, 2026).\[10\]\[12\]\[28\]\[29\] Its health evaluation stack is not public.
- **Meta, xAI, Microsoft, Amazon:** no clinical evaluation methodology was verified in this research (see Unknowns).

**Who supplies them, and at what price:**

| Item | Figure | Source & date |
|---|---|---|
| Expert RL tasks | $200–$2,000 per task | Epoch AI, "An FAQ on reinforcement learning environments" (Jean-Stanislas Denain & Chris Barber, Jan 12, 2026; 18 interviews), via Taskade, 2026 |
| Website/UI replica environment | About $20,000 each | SemiAnalysis via HeroHunt, 2026\[30\] |
| Complex product clone | About $300,000 | Same\[30\] |
| Exclusivity premium | 4–5× the non-exclusive price | Same\[30\] |
| Contract size | An RL environment founder told Epoch AI contracts "are often seven figures per quarter or more"; $300k–$500k per quarter for smaller labs (Troveo). Epoch also reports RL use outnumbers benchmarking requests "perhaps 10-20x" | Epoch AI, Jan 12, 2026; Troveo, 2026 |
| Lab budget signal | Anthropic leaders discussed spending more than $1B on RL environments over "the next year," including "simulated apps like Zendesk and Salesforce" | The Information via TechCrunch, Sept 21, 2025 |
| Compute logic for spending more per task | About $2,400 lifetime compute per task, so labs should spend "a few thousand dollars per task" | Mechanize blog, Aug 2025\[31\] |
| Mercor physician pay | Primary care $130–$170/hr (Built In); specialty listings $130–$400/hr (Mozibox); platform average $110/hr (Bloomberg, whose $400/hr figure was for civil rights attorneys, not doctors) | Built In via HeroHunt 2026; Mozibox 2026; Bloomberg Oct 16, 2026 |
| Mercor margin | About 35% estimated take rate | HeroHunt, 2026 (estimate by that source)\[32\] |
| Prime Intellect bounties | $1,000–$5,000+ per environment | aitraining.jobs, July 2026\[33\] |

**Vendors:**
- **Data and expert-hour incumbents:**
  - Mercor pitched investors on healthcare RL environments (TechCrunch, Sept 2025).\[34\]
  - Mercor posted Oct 24, 2026 listings for board-certified radiologists, cardiologists, neurologists and others "to evaluate health AI models in partnership with a leading AI lab" (Skillora, Oct 2026).\[13\]
  - Mercor acquired the environment company Deeptune in July 2026 (rl-list, 2026).\[35\]
  - Handshake runs a year-round physician AI fellowship. Scale AI (Outlier) and Snorkel recruit doctors (SF Standard, Apr 17, 2026).\[36\]
- **Environment-native startups:** about 20 seed-to-Series-A companies (CleverX, 2026).\[37\] One 2026 directory lists 38 environment vendors (HeroHunt citing rl-list).\[37\]\[38\] Examples:
  - Halluminate: $30M Series A led by Oak HC/FT, Oct 1, 2026, for $38.5M total. CEO Jerry Wu told Fortune "four of the top five closed-source U.S. AI labs are paying customers" and that the company is profitable; it has nine employees. Its focus is finance (investment banking and private equity), not health.
  - HUD, Fleet, Bespoke Labs, AfterQuery, Datacurve.\[35\]\[37\]
- **Health-specific environment entrants (direct competitors):**
  - **Archangel Health** (YC F2026, 2 employees) offers "RL environments inside real de-identified EHRs, physician-verified training data, and benchmarks" and says "frontier labs and medical AI companies use it today" (YC directory, 2026).\[14\]
  - **Arcophos** calls itself "the frontier research lab for AI-native healthcare systems." It runs Clinical Deployment Environments in clinics it operates and publishes a Clinical Benchmarks Index (arcophos.com, Oct 2026).\[15\]
- **BioStack Platforms, Surge, Turing, micro1, Medcase, Invisible:** health-specific pricing and terms were not verified (see Unknowns).

**Contract terms, security and speed:**
- Exclusivity is the biggest price lever (SemiAnalysis via HeroHunt, 2026).\[39\]
- Labs "guard their best environments as competitive secrets" (HeroHunt, 2026).\[30\]
- [Opinion] Expect exclusivity or a right of first refusal, IP assignment of tasks, no PHI (synthetic data only), SOC 2-style controls and vetted annotator identities. The per-lab procurement cycle was not verifiable. [Estimate] Pilot purchases by lab post-training teams appear to close in weeks to a few months when a vendor is already onboarded, and longer for a new vendor.

## 3. Health AI companies in older-adult care (lighter)

| Company | Country | Focus | Funding / stage | Publishes or needs clinical evals? | Source & date |
|---|---|---|---|---|---|
| Sensi.AI | US/Israel | Audio-based in-home care monitoring; "AI Operating System for Senior Care" | $45M Series C (Oct 9, 2025); >$98M total | Claims ~80% of the largest US home care networks; no peer-reviewed eval found [Opinion: needs one] | AccessNewswire, Oct 9, 2025; McKnight's, 2025\[40\]\[41\]\[42\] |
| Cera | UK | Digital-first home healthcare with predictive AI for hospital avoidance | $556.7M total (incl. debt) | Not verified here | Failory, 2026\[43\] |
| Birdie | UK | Home care digital platform | $52.6M | Not verified | MedicalStartups, 2026\[44\] |
| CarePredict | US | AI elder-care monitoring | $48.7M | Not verified | MedicalStartups, 2026\[44\] |
| Sage | US | Caregiver tools for senior living | $124M | Not verified | MedicalStartups, 2026\[44\] |
| Intuition Robotics | Israel/US | Care companion (ElliQ) | $83M | Not verified | MedicalStartups, 2026\[44\] |

Dementia, falls and discharge-planning AI companies beyond these were not verified in this research. [Opinion] These companies are better seen as future users of an older-adult evaluation pack (to show safety to agencies and payers) than as early revenue. Their budgets are small and none faces a mandate to run simulation tests.

## 4. Regulatory and policy drivers (lighter)

- **FDA:**
  - The Digital Health Advisory Committee met Nov 20–21, 2024 on generative-AI device lifecycle, and Nov 6, 2025 on generative-AI mental health devices (Psychiatric Times, 2025).\[45\]\[46\]
  - Jan 6, 2026 clinical decision support guidance extended enforcement discretion to some AI that gives a single recommendation clinicians can verify (Textbook of Digital Health, May 2026).\[47\]
  - **Key signal:** the Aug 18, 2026 discussion paper (docket FDA-2026-N-7874; comments closed Oct 19, 2026) proposes a competency-based approach. That means device benchmarking across ten elements (safety, clinical proficiency, generalizability, agentic conduct), followed by clinical confirmation through retrospective evaluation, shadow deployment, **standardized patient interactions**, clinician adjudication or prospective studies. It also names contamination, saturation and lack of representativeness as problems with public benchmarks (Innolitics, Aug 18, 2026).\[48\]
  - It is a discussion paper, not guidance.\[48\]
  - No generative-AI device had been authorized as of June 2026 (CRS, June 10, 2026).\[49\]
- **EU AI Act:** the Digital Omnibus (Regulation 2026/1744, in force July 27, 2026) moves Annex III high-risk obligations to Dec 2, 2027 and Annex I (medical devices) to Aug 2, 2028. Article 50 transparency has applied since Aug 2, 2026 (Freshfields; aiacto, 2026).\[50\]\[51\]
- **ONC/ASTP:** the HTI-5 final rule (Oct 26, 2026) removed HTI-1 model-card and risk-management requirements for predictive decision support interventions (healthsystemcio, Oct 26, 2026).\[2\]\[52\]
- **Joint Commission/CHAI:**
  - Responsible Use of AI in Healthcare guidance, Sept 17, 2025 (CHAI).\[53\]
  - A voluntary Responsible Use of AI in Healthcare (RUAIH) certification launched later, alongside CHAI governance playbooks. It "does not validate or certify individual AI products" (HC Innovation Group, 2026).\[54\]
- **MHRA/NHS England:** see Section 6. MHRA AI Airlock, CQC, NICE, CMS specifics and the Oxford statement on generative AI in social care were not verified in this research (see Unknowns).

[Opinion] The only regulator-originated text pointing directly at simulated patient testing is FDA's non-binding discussion paper. That favours selling "FDA-style competency benchmarking" to device-pathway companies over scribes.

## 5. State of the art: papers (ranked by relevance to the thesis)

| Rank | Paper (date) | Contribution | Method | Headline result | Admitted limitations | Code/data |
|---|---|---|---|---|---|---|
| 1 | AMIE Mx, "Towards conversational AI for disease management" (Nature, June 17, 2026) | Multi-visit management agent | Dialogue agent plus Management Reasoning agent (Gemini), randomized blinded virtual OSCE | Non-inferior to 21 primary care physicians overall; better guideline alignment across all 3 visits | Simulated settings with patient actors | Not verified\[16\]\[55\]\[56\] |
| 2 | ResidencyRL (arXiv, Aug 7, 2026) | Long-horizon multi-turn clinical RL | GRPO; LLM patient simulators (routine/hidden/adversarial); rubric autorater | Adversarial diagnostic accuracy 81%→88%; missed red flags −31%; clinicians preferred it in 87.6% of cases; AMIE Mx management 80.1%→88.4% | Needs prospective validation | Not verified\[25\] |
| 3 | T²-GRPO caregiver agents on DemMA (arXiv, June 2026) | RL for dementia-care interaction | Turn-trajectory GRPO with environment-emitted rewards | Caregiver-contingent response mean 4.24 | Not extracted | Not verified\[9\] |
| 4 | ClinTraceBench (arXiv, Sept 2026) | Longitudinal memory audit | 8 history strategies × 4 backbones; 6,271 questions | Agentic memory (Mem0, A-Mem) recovers only 0–5.3% of injected relations | Derived from EHR records | Not verified\[6\] |
| 5 | MedLoCoMo (arXiv, July 2026) | Multi-session patient memory | 100 timelines, about 74.5k tokens each | Not extracted | QA, not care actions | Not verified\[7\] |
| 6 | ClinicalMC (arXiv, June 2026) | Multi-course decision-making | Patient/examiner/doctor agents | Not extracted | Not extracted | Not verified\[23\] |
| 7 | HealthBench (May 2025) | Rubric evaluation at scale | 48,562 physician criteria; GPT-4.1 grader | Grader macro-F1 0.709; above average physician in 5 of 7 themes | Grader tuned with GPT-4.1; static conversations | Open-source\[57\] |
| 8 | Reward Hacking in Rubric-Based RL (arXiv 2605.12474, 2026) | Characterises rubric hacking | Systematic analysis | Policies produce artefacts and verbose self-evaluation to fool verifiers | — | Not verified\[58\] |
| 9 | Rubric Dropout (arXiv, Aug 2026) | Mitigation | Randomly drops rubric items in GRPO on medical rubrics; gold-judge check | Improves out-of-distribution performance late in training; largest gains on clinical axes | Medical used only as testbed | Not verified\[59\] |
| 10 | Rubric-guided RL survey (arXiv, Aug 2026) | Case studies of hacking | Review | Rubric verifier preferred the RL checkpoint on 85.8% of prompts, but rubric-free judges preferred the base model on 78.4%; 90.2% of rubric weight was presence-based | — | —\[60\] |
| 11 | Doctor-R1 (arXiv, Oct 2025) | Agentic RL for clinical inquiry | 8-dimension reward plus veto penalties | Saw "repetitive empathetic statements" hacking early; manually reviewed about 50 high-reward trajectories/day | — | Not verified\[61\] |
| 12 | Evidence-seeking diagnostic RL (arXiv, July 2026) | Medical RL with verifiable rewards and anti-hacking penalties | Conflict detection, "differential-as-mirror" | Models appended rare diseases and gave vague diagnoses to inflate reward | — | Not verified\[62\] |
| 13 | DiagGym/DiagAgent (arXiv, Oct 2025) | EHR world model as RL environment | Generative exam-result simulator; multi-turn RL | DiagBench 750 cases | Diagnosis-focused | Models on Hugging Face\[22\] |
| 14 | MedDialBench / "Beyond idealized patients" (arXiv, Mar–Apr 2026) | Adversarial patient behaviours | Parametric behaviour injection | Not extracted | — | Not verified |
| 15 | GrandGuard (ACL Findings, 2026) | Older-adult safety taxonomy | 10,404 labelled prompts | Leading LLMs mishandle elderly-specific risks in >50% of cases; response safety 22.6%–89.8% | Single-turn | Not verified\[8\] |
| 16 | MedHELM (2025) | Broad clinical task taxonomy | LLM-jury | ICC 0.47 vs clinicians (clinician–clinician 0.43) | — | Not verified\[20\] |
| 17 | AgentClinic (2024/2025) | Multimodal clinical agent benchmark | 4 language agents incl. patient and measurement | Shows premature closure | Simulated | Open-source |
| 18 | PatientSim (NeurIPS, 2025) | Persona-grounded patient simulator | Multi-dimensional personas from real clinical data | Not extracted | — | Not verified |
| 19 | CHERRL (arXiv, 2026, ICLR 2027 submission) | Controllable hacking environment | Injects known judge biases | Makes hacking observable before training derails | — | Not verified\[63\] |
| 20 | MTBBench (arXiv, Nov 2025) | Longitudinal oncology tumour-board benchmark | Multimodal, temporally distributed events | Not extracted | Oncology only | Not verified\[64\] |

**Simulators with third parties and memory:**
- Carers mostly appear as question authors (the late-life depression benchmark: 30 of 90 questions) or as the agent being trained (DemMA/T²-GRPO).\[9\]\[24\] They do not appear as an independent simulated party that a clinician agent must reconcile with the patient and the record.
- Memory across visits is handled by structured state in AMIE Mx (patient summary, differential, plan). It is audited by ClinTraceBench, which found compressed and agentic memory loses relations.\[6\]\[65\]
- [Opinion] A simulator with a patient, a carer, a care agency record and a GP record that disagree with each other, persisting across visits, appears unpublished. That is your most defensible technical asset.

**Reward hacking in clinical RL:** documented failure modes include:
- verbosity and presence-criterion stuffing;\[60\]
- boilerplate "consult your doctor" disclaimers that satisfy safety items;\[60\]
- empathy-phrase repetition (Doctor-R1);\[61\]
- appending rare diseases or giving vague diagnoses (evidence-seeking RL).\[62\]

An additive-rubric analysis found that naming an item earned +7.3 points while dropping a critical recommendation cost only −0.9 (Shadow-LLM failure-cases, citing a 2026 paper).\[66\] [Opinion] Older-adult care is especially exposed: "comprehensive" plans that list every care service will out-score parsimonious, correct plans unless the grader penalises over-provision and missed priorities.

**Grader validation against clinicians:**
- HealthBench: macro-F1 0.709 on 34 consensus criteria, placing it at the 70th–88th percentile of physicians by theme (OpenAI, May 2025; Emergent Mind).\[57\]\[67\]
- MedHELM: jury ICC 0.47 vs clinician–clinician 0.43.\[20\]
- ClinConsensus (2026): 82,500 aligned decisions per expert group, with "substantial but non-uniform" physician agreement.\[68\]
- ER-Reason: 52.6% exact inter-physician agreement on final-diagnosis scores (cited in arXiv 2607.02175).\[20\]
- [Opinion] The bar for a credible grader is therefore "matches inter-clinician agreement on a held-out, multiply-rated set". For older-adult care, the raters must include GPs, geriatricians, nurses and social care professionals.

**Open-source tooling:**
- Prime Intellect's Environments Hub (launched Aug 27, 2025) hosts more than 2,500 environments. It ships the verifiers library and the prime-rl trainer (aitraining.jobs, July 2026; CleverX, 2026).\[33\]\[37\]\[69\]
- Gymnasium (formerly OpenAI Gym) is the standard RL interface (HistoGym, arXiv 2024).\[70\]
- HUD offers an open SDK for agent environments (rl-list, 2026).\[35\]
- inspect_ai and OpenEnv were not verified in this research. [Opinion] Ship your harness as a verifiers/Gymnasium-compatible package so any lab can plug it in.

## 6. Clinical documentation and triage AI (US first, UK second)

**US market (dated):**

| Company | Latest funding / status | Date |
|---|---|---|
| Abridge | $300M Series E at about $5.3B (June 2025); reported $316M extension at an unchanged $5.3B (Apr 2026, secondary sources only); Best in KLAS Ambient Speech 2026 (94.7, per a competitor's blog) | June 2025 / Apr 29, 2026\[71\]\[72\]\[73\] |
| Ambience Healthcare | $243M Series C at about $1.25B; no 2026 priced round found | July 2025\[74\]\[75\] |
| Suki | $90M Series E, valuation undisclosed, 450+ organizations | Oct 13–14, 2026\[76\]\[77\] |
| Nabla | $70M Series C, $120M total | June 17, 2025\[78\] |
| Commure (owns Augmedix, acquired for about $139M in 2024) | $70M at $7B post-money | May 19, 2026\[79\]\[80\] |
| Microsoft Dragon Copilot | Repositioned at HIMSS as an agentic assistant for nurses and radiologists, with a partner marketplace | Mar 5, 2026\[81\]\[82\] |
| Epic AI Charting (native) | Released; drafts notes and queues orders | Feb 4, 2026\[83\]\[84\] |

[Opinion] Epic shipping native ambient charting makes accuracy differentiation existential for third-party scribes. That raises their motive to prove quality with external evidence.

**How scribes are evaluated today:**
- **UCLA randomized trial (NEJM AI, Dec 2025):** 238 physicians randomized to DAX, Nabla or usual care, about 48k visits. Only Nabla significantly reduced time-in-note. Both improved burnout scores, and physicians reported occasional clinically significant inaccuracies.\[85\]\[86\]\[87\]
- **JAMA Network Open (Oct 2025, secondary source):** burnout fell from 51.9% to 38.8% after 30 days.\[88\]
- **PDQI-9 is the de facto quality instrument,** often modified to add a hallucination item:
  - a 2026 JMIR Medical Informatics study found omissions in 18% of 356 notes and hallucinations in 2.5%;\[89\]
  - a simulated-encounter study scored notes from 32.0 (cardiology) to 42.2 (neurology);\[90\]
  - an Australian pilot found 47% of staff reported hallucinations (Jan 2026).\[91\]\[92\]
- A vendor-involved (Heidi) multi-country simulation preprint appeared in Aug 2026.\[93\]
- A 2026 Journal of Medical Systems scoping review reportedly found no standard accuracy method (secondary source).\[73\]
- KLAS satisfaction scores are the main cross-vendor signal.\[94\]

**US requirements:**
- **FDA:** scribes are generally outside device regulation. The Aug 2026 discussion paper suggests a documentation tool is "possibly not" a device (Innolitics, Aug 2026).\[48\]
- **CHAI:** Applied Model Card and an assurance-lab framework (draft Oct 2024; labs still described as in pilot).\[95\] It also runs a central model-card registry with a checkbox for third-party validation,\[96\]\[97\]\[98\] plus an ambient AI evaluation framework that is unverified here.
- **Joint Commission:** RUAIH certification for organisations, not products.\[54\]
- **ONC HTI-5 (Oct 26, 2026):** removed model-card requirements.
- **State laws:**
  - California AB 3030 (AI patient communications need a disclaimer unless a clinician reviews them; effective Jan 1, 2025) and AB 489 (effective Jan 1, 2026).\[99\]\[100\]
  - Texas SB 1188 (clinician review of AI records and disclosure; effective Sept 1, 2025) and TRAIGA (written AI disclosure; $10k–$200k penalties; effective Jan 1, 2026).\[101\]
  - Illinois HB 1806 restricts AI in therapy (secondary source).\[102\]\[103\]
  - Others (Nevada, Louisiana, Arizona, Colorado) are reported by a vendor blog only.\[99\]

**UK requirements:**
- **NHS England guidance:**
  - Guidance on AI-enabled ambient scribing was first published Apr 27, 2025; Version 3 was updated July 29, 2026 (Bird & Bird, 2026).\[104\]\[105\]\[106\]
  - The self-certified AVT Supplier Registry opened Jan 16, 2026 and lists 30 suppliers, including Accurx, Anima, Heidi Health, Tandem, Tortus, Microsoft Dragon, Corti, Lyrebird and X-On Health (NHS England Digital, 2026).\[105\]\[107\]
  - Original criteria included Class I medical device status, a current DTAC assessment and "evidence of benefit" in NHS settings (HTN, Jan 19, 2026).\[108\]
  - Listing "does not guarantee a contract and the Registry is not a commercial framework" (Bird & Bird, 2026).\[106\]
- **MHRA (July 29, 2026):** AVT "intended solely for transcription, summarising… drafting letters, or suggesting clinical codes for a clinician to review" is **not** a medical device. Products that support diagnosis or treatment, or take automated action without review, remain regulated (HTN; techUK, 2026).\[109\]\[110\]
- **Demand signals:**
  - NHS England Midlands procured AVT at scale for all 1,239 GP practices and more than 70,000 clinicians across 15 trusts (NHS England, July 15, 2026).\[111\]
  - The GP contract asks ICBs to support AVT deployment.\[111\]
- HSSIB and the Welsh ambient voice framework were not verified in this research (see Unknowns).

**Does a shared simulation-based harness exist?** No shared US or UK harness was found. Researchers use ACI-Bench and PriMock57. One hobby repository, scribe-bench (Sept 2026), runs speech-recognition and hallucination checks on them.\[112\] Simulation appears only within single studies.

**Would scribe companies pay, who decides and how fast?** [Opinion/Estimate]
- **US:** yes, modestly. The best-funded vendors (Abridge, Ambience, Commure, Suki) need external proof against Epic and for health-system AI governance committees.
- **Decision-makers:** the Chief Medical Officer or Chief Medical Information Officer plus the head of ML/evaluation. Clinical safety and regulatory leads matter more in the UK.
- **Price:** [Estimate] a $25k–$150k annual evaluation contract.
- **Speed:** [Estimate] 1–3 months for a pilot at a startup; 3–9 months where security review is involved.
- **UK:** after MHRA's July 2026 change and registry self-certification, compliance pull is weak. Vendors will pay mainly if NHS buyers or a regional procurement (like the Midlands) start asking for comparative simulated-safety evidence. [Opinion] Scribes are a secondary market for you. Their core problem (transcript-to-note fidelity) differs from your thesis (longitudinal decision-making), except for discharge and care-plan summaries for older adults, which are a natural bridge.

## 7. Demand signals 2025–2026 (lighter)
- **OpenAI:**
  - ChatGPT Health launched Jan 7, 2026, citing 230M weekly health askers (TechCrunch, Jan 7, 2026).\[113\]
  - It became available to all US adults July 23, 2026, with more than 300M weekly (Fierce Healthcare, July 24, 2026).\[26\]\[114\]
  - ChatGPT for Healthcare launched Jan 8, 2026 with AdventHealth, HCA, Cedars-Sinai and others (Axios).\[27\]
- **Anthropic:** Claude for Healthcare launched Jan 11, 2026.\[12\] Banner Health reports more than 22,000 clinical providers on the platform (R&D World, Jan 11, 2026).\[10\]
- **Google:** AMIE Mx (June 2026)\[55\] and ResidencyRL (Aug 2026). In Sept 2026 it also completed a talent deal with Mechanize: a non-exclusive licence plus hires, after Business Insider had reported talks worth more than $1.5B (Business Insider via Kingy AI, Sept 12, 2026). Final terms were undisclosed, and one outlet reports the figure as more than $2B, unverified. Co-founder Tamay Besiroglu and more than a dozen staff joined DeepMind, while Mechanize keeps operating independently under CEO Guive Assadi.
- **Environment funding and M&A:**
  - Halluminate: $30M Series A, Oct 1, 2026.\[115\]
  - Mercor acquired Deeptune, July 2026.\[35\]
  - Prime Intellect: reported $130M Series A and ARR above $100M (CleverX, 2026; not independently verified).\[37\]
  - Archangel Health: YC F2026.\[14\]
- **Health AI labs:** Ortet launched with a $500M commitment from Thoreau (Fierce Healthcare, Sept 30, 2026).\[116\]
- **Jobs:** Mercor's Oct 2026 board-certified specialist listings for "a leading AI lab". Bloomberg (Oct 16, 2026) reports Mercor's average pay at $110/hour. Its $400/hour figure was for civil rights attorneys, while Mercor's own specialty physician listings reach $400/hour (Mozibox, 2026).

## 8. The strongest case that this fails (adversarial)
1. **Labs build it themselves, and the leader already has.** Google published both a multi-visit benchmark and a 57k-scenario RL simulator. It also hired environment talent through its Mechanize license-and-hire deal rather than buying environments. [Opinion] If Google wants an older-adult curriculum, a team with Gemini, clinician panels and patient-actor infrastructure can do it in a quarter.
2. **Vendors commoditise the labour.** Mercor already sells physician hours at $130–$400 and pitches healthcare environments.\[34\]\[117\] Its roughly 35% take rate and recruiting machine beat a solo founder on supply. Archangel Health and Arcophos are already health-specific.\[14\]\[15\]
3. **The niche may be too small for frontier labs.** Labs optimise for broad benchmarks (HealthBench, GDPval). Older-adult complex care may not move headline metrics, so budgets may treat it as a long-tail curriculum worth a few hundred tasks, not a company. [Estimate] One non-exclusive 300-task pack at about $1,000 per task is about $300k: a good contract, not a venture-scale business on its own.
4. **Regulators don't require simulation.** FDA's paper is non-binding. MHRA deregulated documentation-only scribes. HTI-5 removed model cards. The Joint Commission certifies organisations, not products.\[48\]\[54\]\[118\] NHS AVT is self-certified.
5. **Simulator validity is contestable.** Every major paper admits simulated settings need prospective validation (AMIE Mx, ResidencyRL).\[25\] LLM simulators of confused older patients and stressed carers are hard to validate, and a lab can dismiss your environment as unrealistic.
6. **Graders get hacked.** Rubric RL in medicine shows documented verbosity and disclaimer hacking (85.8% vs 78.4% judge disagreement).\[60\] Older-adult care plans are long and open-ended, which makes them more hackable. If your grader is exploited in a customer's run, your reputation goes with it.
7. **Benchmarks saturate and leak.** FDA itself flags contamination and saturation of public benchmarks (Aug 2026).\[48\] An open benchmark loses commercial value once it is trained on.
8. **Founder constraints.** A part-time clinical founder competes against teams paying engineers $350k–$500k (Mechanize)\[38\] and nine-person firms like Halluminate, whose CEO says four of the top five closed-source US labs are paying customers and the company is profitable. Labs expect fast iteration, security compliance and 24/7 responsiveness. [Opinion] This is the single biggest risk. NHS trainee contracts, working-time rules and any conflict-of-interest declarations also need checking (not verified here).
9. **The UK lens may not transfer.** Care packages, ICBs and CQC are UK-specific, while the money is in US labs. US long-term services and supports (Medicaid HCBS, home health, SNFs) need different scenario content.

**Counter-arguments that keep it alive [Opinion]:**
- No one has published the function/carer/conflicting-records combination.
- Labs buy many niche curricula to avoid blind spots.
- A practising UK GP's clinical judgement is the scarce input for grader validity.
- FDA's direction (competency benchmarking plus standardized patients) could make your harness a reusable evidence tool for device-pathway companies.

## 9. Ten people or organisations to contact first

| # | Person / org | Public role | Why |
|---|---|---|---|
| 1 | Tao Tu and Mike Schaekermann (Google DeepMind / Google Research) | Authors on AMIE and ResidencyRL (arXiv, Aug 2026) | Owners of the closest system; test whether an older-adult/carer curriculum is a gap they would source externally\[25\] |
| 2 | Valentin Liévin and Samuel Schmidgall (Google DeepMind) | ResidencyRL co-first authors; Schmidgall led AgentClinic | Simulator design, adversarial patients, external benchmark interest\[25\] |
| 3 | Rahul K. Arora (OpenAI) | Lead author of HealthBench (May 2025) | Rubric/grader methods; whether OpenAI would adopt a longitudinal older-adult extension |
| 4 | Eric Kauderer-Abrams (Anthropic) | Head of biology and life sciences (Fierce Healthcare, Jan 2026) | Anthropic's health push; route to post-training teams\[12\] |
| 5 | Archangel Health founders (YC F2026) | Health RL environments in de-identified EHRs | Possible partner, acquirer or competitor; tests market pricing\[14\] |
| 6 | Arcophos | Runs Clinical Deployment Environments and a Clinical Benchmarks Index | Possible partner for older-adult scenarios grounded in real clinics\[15\] |
| 7 | Jerry Wu, Halluminate | Wrote Halluminate's Series A post (Oct 2026); backed by healthcare investor Oak HC/FT | Playbook for a small team selling expert environments to four of five labs\[115\] |
| 8 | Prime Intellect (Environments Hub team) | Runs the open hub and bounties | Distribution and credibility for an open older-adult pack |
| 9 | Rob Thompson (NHS England) and Lawrence Tallon (MHRA) | NHS England Chief Digital, Data and Technology Officer; MHRA Chief Executive, co-signatories of the July 29, 2026 AVT letter | UK appetite for simulation-based assurance of AVT and agentic tools\[119\] |
| 10 | Romi Gubes (Sensi.AI) or Mahiben Maruthappu (Cera) | CEO/co-founder of Sensi.AI; co-founder of Cera | Older-adult AI buyers who could validate scenarios and pay for safety evidence\[42\]\[43\] |

## Recommendations [Opinion]
1. **Stay in training. Build a 90-day proof:**
   - 50–100 older-adult complex-care scenarios, each with a patient simulator, a carer simulator, conflicting GP and agency records, and 2–4 visits;
   - outcome rubrics centred on function, falls, ADLs, care packages and safety-netting, with penalties for over-provision and disclaimer padding.
2. **Validate the grader before selling.** Use at least 3 independent raters (GP, geriatrician, community nurse or social worker). Report macro-F1 against inter-rater agreement, HealthBench-style.
3. **Publish openly** on Prime Intellect / verifiers with a preprint. Use it as a calling card to labs, and keep a larger private set for paid, ideally exclusive, packs. [Estimate] Price at $1,000–$3,000 per task, or $150k–$500k per custom pack.
4. **Sell in this order:** frontier lab health post-training teams, then health AI evaluation leads (older-adult and discharge tools), then scribe vendors (via discharge and care-plan summary evaluation), then FDA-pathway device companies.
5. **Kill criteria:** stop if, by month 6, you have no paid pilot or LOI from at least one lab or vendor, or if your validated grader cannot reach inter-clinician agreement.

## What remains unknown
- ClinEnv: not located. The exact sizes and grading of CRAFT-MD, MedAgentBench and the original AMIE study were not re-verified in this pass.
- Lab-by-lab evaluation practices at Meta, xAI, Microsoft (beyond Dragon Copilot) and Amazon.
- Health-specific pricing, contract terms and security requirements for BioStack Platforms, Surge, Turing, Handshake, micro1, Medcase, AfterQuery, Scale AI and Invisible.
- Actual procurement cycle lengths at labs and scribe vendors.
- Whether AMIE Mx, ResidencyRL, ClinTraceBench, MedLoCoMo and the DemMA environment have released code or data.
- MHRA AI Airlock outputs, MHRA software-as-a-medical-device reform details, CQC, NICE, DTAC revisions, CMS policy, HSSIB reports and the Welsh ambient voice framework.
- The Oxford statement on responsible generative AI in social care, and any UK adult social care AI guidance.
- Funding and evaluation practices of dementia, falls and discharge-planning AI companies beyond those listed.
- Final terms of the Google–Mechanize deal;\[120\] whether Abridge's 2026 extension closed; Prime Intellect's revenue.
- Employment-contract constraints on outside business activity.

## Sources

1. [ONC Finalizes HTI-5, De-regulating Less than Anticipated and Punting on Information Blocking Changes](https://www.reedsmith.com/our-insights/blogs/health-industry-washington-watch/102o6vt/onc-finalizes-hti-5-de-regulating-less-than-anticipated-and-punting-on-informati/)
2. [HHS Finalizes HTI-5 Deregulatory Rule - Hooper Lundy & Bookman](https://hooperlundy.com/hhs-finalizes-hti-5-deregulatory-rule/)
3. [AMIE: How Conversational AI Is Moving Beyond Diagnosis to Disease Management — Computing for All](https://computing4all.com/amie-moving-beyond-diagnosis/)
4. [Google AMIE moves medical AI into long-term care](https://www.yaitec.com/en/blog/google-amie-ai-medica-cuidado-continuo)
5. [August 2026 Newsletter 🤖 🧬 🩺 - Clinical AI Academy](https://clinicalaiacademy.substack.com/p/august-2026-newsletter)
6. [ClinTraceBench: Source-Verifiable Longitudinal ClinicalReasoning over EHR-Derived Dialogues](https://arxiv.org/html/2609.01111v1)
7. [MedLoCoMo: A Long-Context Multi-Session Medical Dialogue Benchmark for Large Language Models](https://arxiv.org/html/2607.22566v1)
8. [GRANDGUARD: Taxonomy, Benchmark, and Safeguards ...](https://aclanthology.org/2026.findings-acl.1116.pdf)
9. [Can the Environment Speak for Itself? \$T^{2}\$-GRPO: A Turn-Trajectory Group Relative Policy Optimization for Caregiver Agents](https://arxiv.org/pdf/2606.08875)
10. [Anthropic’s Claude heads deeper into healthcare with HIPAA-ready tools](https://www.rdworldonline.com/anthropics-claude-heads-deeper-into-healthcare-with-hipaa-ready-tools/)
11. [OpenAI launches ChatGPT Health to connect user medical records, wellness apps](https://www.cnbc.com/2026/01/07/openai-chatgpt-health-medical-records.html)
12. [JPM26: Anthropic launches Claude for Healthcare to turbocharge AI efficiency at health systems, payers](https://www.fiercehealthcare.com/ai-and-machine-learning/jpm26-anthropic-launches-claude-healthcare-targeting-health-systems-payers)
13. [Mercor Jobs: Live AI Training Roles, Pay & the Interview](https://skillora.ai/ai-training-jobs/mercor)
14. [Health Tech Startups funded by Y Combinator (YC) 2026](https://www.ycombinator.com/companies/industry/health-tech)
15. [Arcophos](https://arcophos.com/)
16. [Towards conversational artificial intelligence for disease management](https://www.nature.com/articles/s41586-026-10764-5)
17. [Google AMIE advances disease management AI in Nature study](https://www.edtechinnovationhub.com/news/google-extends-amie-beyond-diagnosis-in-nature-disease-management-study)
18. [Introducing HealthBench](https://openai.com/index/healthbench/)
19. [HealthBench: Advancing AI evaluation in healthcare, but not yet clinically ready - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12547120/)
20. [A rubric-based controlled comparison of frontier language models on expert-authored clinical reasoning tasks](https://arxiv.org/pdf/2607.02175)
21. [2025-5-27 AgentClinic: a multimodal agent benchmark to](https://arxiv.org/pdf/2405.07960)
22. [Paper page - Evolving Diagnostic Agents in a Virtual Clinical Environment](https://huggingface.co/papers/2510.24654)
23. [ClinicalMC: A Benchmark for Multi-Course Clinical Decision-Making with Large Language Models](https://arxiv.org/html/2606.03157)
24. [Frontiers](https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2026.1956736/full)
25. [ResidencyRL: Reinforcement Learning in Simulated Clinical Environments](https://arxiv.org/html/2608.07418)
26. [OpenAI makes Health in ChatGPT widely available, moving deeper into consumer health](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-makes-health-chatgpt-widely-available-moving-deeper-consumer-health)
27. [ChatGPT unveils new health tool for doctors](https://www.axios.com/2026/01/08/openai-chatgpt-doctors-patients-health-tab)
28. [Claude for Healthcare & Life Sciences: 2026 Technical Guide](https://intuitionlabs.ai/articles/claude-healthcare-life-sciences-ai-capabilities-2026)
29. [JPM: Anthropic launches Claude for Healthcare](https://www.mobihealthnews.com/news/jpm-anthropic-launches-claude-healthcare)
30. [Top 10 Data Annotators for AI Labs (2026 Benchmark)](https://www.herohunt.ai/blog/top-10-data-annotators-for-ai-labs-2026-benchmark/)
31. [Cheap RL tasks will waste compute](https://www.mechanize.work/blog/cheap-rl-tasks-will-waste-compute/)
32. [Mercor 2026: How It Works, Pay, Alternatives](https://www.herohunt.ai/blog/mercor-2026-how-it-works-pay-alternatives/)
33. [Agentic Tasks & RL Environments Jobs: 2026 Pay, Platforms & How to Start](https://aitraining.jobs/roles/agentic-eval)
34. [Silicon Valley bets big on 'environments' to train AI agents](https://techcrunch.com/2025/09/21/silicon-valley-bets-big-on-environments-to-train-ai-agents/)
35. [RL Environments for Enterprise Workflows (2026)](https://www.rl-list.com/rl-environments-for-enterprise)
36. [SF is so expensive, even doctors are working AI side hustles](https://sfstandard.com/2026/04/17/sf-doctors-taking-side-hustles-tutoring-ai/)
37. [Companies Building RL Environments in 2026](https://cleverx.com/blog/companies-building-rl-environments-2026/)
38. [Hiring RL Environment Engineers: 2026 Labs Guide](https://www.herohunt.ai/blog/hiring-rl-environment-engineers-2026-labs-guide/)
39. [How to Sell RL Environments to AI Labs](https://www.troveo.ai/resources/sell-rl-environments)
40. [Sensi.AI raises \$45M Series C funding to advance product innovation, go-to-market efforts](https://www.mcknightsseniorliving.com/news/sensi-ai-raises-45m-series-c-funding-to-advance-product-innovation-go-to-market-efforts/)
41. [Sensi.AI Raises \$45M Series C, Extending Its Dominance of Care Intelligence in Vertical AI](https://www.accessnewswire.com/newsroom/en/healthcare-and-pharmaceutical/sensi.ai-raises-45m-series-c-extending-its-dominance-of-care-intellig-1081170)
42. [Female-led Sensi.AI gets \$45M to accelerate AI-driven care intelligence for ageing populations — TFN](https://techfundingnews.com/sensiai-raises-45m-series-c-to-accelerate-ai-care-intelligence-for-seniors/)
43. [Top 19 Elder Care Startups to Watch in 2026](https://www.failory.com/startups/elder-care)
44. [Top 57 Caregiver startups 2026](https://www.medicalstartups.org/top/caregiver/)
45. [FDA Committee Meets on Generative AI Digital Mental Health Devices](https://www.psychiatrictimes.com/view/fda-committee-meets-on-generative-ai-digital-mental-health-devices)
46. [U.S. FDA and CMS Actions on Generative AI-Enabled Mental Health Devices Yield Insights Across AI Product Development](https://www.sidley.com/en/insights/newsupdates/2025/11/us-fda-and-cms-actions-on-generative-ai-enabled-mental-health-devices-yield-insights-across-ai)
47. [Digital health round-up: 17 May 2026 · Textbook of Digital Health](https://www.textbookofdigitalhealth.com/news/2026-05-17-roundup.html)
48. [FDA Releases Generative AI Medical Device Discussion Paper: What's Inside | Innolitics](https://innolitics.com/articles/fda-generative-ai-medical-devices-discussion-paper/)
49. [FDA Regulation of AI-Enabled Devices](https://www.congress.gov/crs-product/IF13245)
50. [EU AI Act unpacked #34: The final Digital Omnibus on AI - Key amendments to the AI Act and their impact on businesses active in the EU](https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-34-the-final-digital-omnibus-on-ai-key-amendments-to-the-a-102nber)
51. [Digital Omnibus Adopted: AI Act High-Risk Delayed to 2027](https://www.aiacto.eu/en/blog/digital-omnibus-ai-act-report-2027)
52. [HTI-5 Final Rule Drops Source-Attribute Requirements for AI and Other Decision Support Tools From EHR Certification](https://healthsystemcio.com/2026/10/26/hti-5-final-rule-ai-source-attributes/)
53. [Joint Commission and Coalition for Health AI (CHAI) Release Initial Guidance to Support Responsible AI Adoption Across U.S. Health Systems](https://www.chai.org/news/joint-commission-and-coalition-for-health-ai-chai-release-initial-guidance)
54. [In Tandem, CHAI Releases AI Governance Playbooks, Joint Commission Launches Certification](https://www.hcinnovationgroup.com/analytics-ai/ai-governance/news/55381111/in-tandem-chai-releases-ai-governance-playbooks-joint-commission-launches-certification)
55. [Google advances AMIE toward longitudinal disease management](https://letsdatascience.com/news/google-advances-amie-toward-longitudinal-disease-management-ed2cd0cf)
56. [Two-Agent AMIE Architecture Matches Physicians on 3-Visit Plans](https://getaibook.com/news/two-agent-amie-architecture-matches-physicians-on-3-visit-pl)
57. [HealthBench: Evaluating Large Language Models Towards Improved Human Health](https://www.alphaxiv.org/abs/2505.08775)
58. [Reward Hacking in Rubric-Based Reinforcement Learning](https://arxiv.org/pdf/2605.12474)
59. [Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-Based RL](https://arxiv.org/html/2608.11669)
60. [A Survey on Rubric-Guided Reinforcement Learning for Language Models](https://arxiv.org/pdf/2608.27505)
61. [Doctor-R1: Mastering Clinical Inquiry with Experiential Agentic Reinforcement Learning](https://arxiv.org/pdf/2510.04284)
62. [Reinforcement Learning for Evidence-Seeking Diagnostic Reasoning with Large Language Models](https://arxiv.org/pdf/2607.02983)
63. [Under review as a conference paper at ICLR 2027](https://arxiv.org/pdf/2606.04923)
64. [MTBBench: A Multimodal Sequential Clinical Decision-Making Benchmark in Oncology](https://arxiv.org/html/2511.20490v1)
65. [Leveraging Gemini 1.5's Long Contextual Capabilities, Google's Conversational Healthcare System AMIE Achieved the Reasoning Level of a General Practitioner in 100 Scenarios Involving Multiple Patient visits.](https://hyper.ai/en/news/52043)
66. [Additive rubric-RL creates 8:1 marginal reward for padding answers over preserving critical clinical decisions · Issue #240 · Shadow-LLM/failure-cases · GitHub](https://github.com/Shadow-LLM/failure-cases/issues/240)
67. [HealthBench Consensus: Medical LLM Benchmark](https://www.emergentmind.com/topics/healthbench-consensus)
68. [ClinConsensus: A Physician-Calibrated Benchmark for Evaluating Clinical Rubric Coverage in Chinese Medical LLMs](https://arxiv.org/pdf/2603.02097)
69. [Why RL Environments Became AI’s Hottest Bottleneck in 2026](https://pub.towardsai.net/why-rl-environments-became-ais-hottest-bottleneck-in-2026-0eec9c15e1bf?gi=cdf80ca0fe28)
70. [HistoGym: A Reinforcement Learning Environment for Histopathological Image Analysis](https://arxiv.org/pdf/2408.08847)
71. [Abridge lands \$300M funding round led by Andreessen Horowitz](https://technical.ly/entrepreneurship/abridge-300m-healthtech-ai-funding/)
72. [Abridge Closes Reported \$316M Series E Extension at \$5.3B Valuation, Medical AI Reaches Frontier Funding Tier](https://techjacksolutions.com/ai-brief/abridge-closes-reported-316m-series-e-extension-at-53b-valua/)
73. [How AI Ambient Scribes Work: A 2026 Evaluation Guide](https://interexy.com/how-ai-ambient-scribe-work-guide)
74. [Ambience unveils multi-year roadmap to ‘rebuild’ healthcare with AI](https://www.beckershospitalreview.com/healthcare-information-technology/innovation/ambience-unveils-multi-year-roadmap-to-rebuild-healthcare-with-ai/)
75. [Yes, the EHR Is Going to Kill Your AI Startup](https://techysurgeon.substack.com/p/yes-the-ehr-is-going-to-kill-your)
76. [Suki Raises \$90M in Series E Funding](https://www.finsmes.com/2026/10/suki-raises-90m-in-series-e-funding.html)
77. [Suki secures \$90M in series E funding to accelerate growth, expand AI capabilities](https://ramaonhealthcare.com/suki-secures-90m-in-series-e-funding-to-accelerate-growth-expand-ai-capabilities/)
78. [Nabla Raises \$70M Series C to Deliver Agentic AI to the Heart of Clinical Workflows, Bringing Total Funding to \$120M](https://www.prnewswire.com/news-releases/nabla-raises-70m-series-c-to-deliver-agentic-ai-to-the-heart-of-clinical-workflows-bringing-total-funding-to-120m-302483646.html)
79. [Commure raises \$70M, boosting post-money valuation to \$7B](https://www.mobihealthnews.com/news/commure-raises-70m-boosting-post-money-valuation-7b)
80. [Health tech company Commure to acquire Augmedix in \$139M deal as AI scribe competition heats up](https://www.fiercehealthcare.com/ai-and-machine-learning/augmedix-acquired-commure-valuation-139-mil)
81. [Microsoft Upgrades Dragon Copilot to an Agentic Clinical Assistant at HIMSS 2026](https://hitconsultant.net/2026/03/05/microsoft-dragon-copilot-himss-2026-agentic-clinical-ai-nurses-radiologists/)
82. [Dragon Copilot review: Microsoft's clinical AI, pricing, and where it fits](https://www.plaud.ai/blogs/articles/dragon-copilot-review)
83. [Epic's AI scribe goes live as EHR giant touts strong adoption of built-in AI features](https://www.fiercehealthcare.com/ai-and-machine-learning/epic-rolls-out-ai-charting-and-more-built-automation-clinicians-and)
84. [Epic AI Scribe 2026: Chart with Art vs Abridge and Dragon](https://nirmitee.io/blog/epic-ai-scribe/)
85. [Ambient AI Scribes in Clinical Practice: A Randomized Trial](https://ai.nejm.org/doi/full/10.1056/AIoa2501000)
86. [Ambient AI Scribes in Clinical Practice : NEJM AI](https://www.ovid.com/journals/neai/fulltext/10.1056/aioa2501000~ambient-ai-scribes-in-clinical-practice-a-randomized-trial)
87. [Ambient AI Scribes in Clinical Practice: A Randomized Trial - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12768499/)
88. [Ambient AI Scribes in 2026: Clinical Evidence, ROI Data, and Vendor Comparison](https://www.ehrsource.com/articles/ambient-ai-scribes-comparison/)
89. [Original Paper Quality of Clinical Notes Created by Ambient Listening](https://medinform.jmir.org/2026/1/e86474/PDF)
90. [Ambient Scribe Technology in Simulated Patient Encounters Across Specialties - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12780926/)
91. [Performance, acceptability, and impact of ambient listening scribe technology in an outpatient context: a mixed methods trial evaluation](https://www.researchsquare.com/article/rs-7033639/v1)
92. [Performance, acceptability, and impact of ambient listening scribe technology in an outpatient context: a mixed methods trial evaluation](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12882620/)
93. [Quality, consistency, and clinical safety of AI-generated versus clinician-written clinical notes: a multi-country paired simulation study](https://www.medrxiv.org/content/10.64898/2026.08.18.26360701v1.full)
94. [Best AI Medical Scribes 2026: Top 10 Tools Ranked & Compared](https://www.commure.com/blog-scribe/best-ai-medical-scribes)
95. [CHAI, Joint Commission release guidance for providers using AI](https://www.fiercehealthcare.com/ai-and-machine-learning/chai-and-joint-commission-release-guiding-document-health-systems-using-ai)
96. [CHAI creates central repository for AI model cards](https://www.fiercehealthcare.com/ai-and-machine-learning/chai-creates-central-repository-ai-model-cards)
97. [CHAI Advances Assurance Lab Certification and 'Nutrition Label' for Health AI](https://www.prnewswire.com/news-releases/chai-advances-assurance-lab-certification-and-nutrition-label-for-health-ai-302280530.html)
98. [CHAI Certification: Health AI Assurance Framework Guide](https://trussed.ai/resources/chai-certification-health-ai-assurance-framework-guide)
99. [State Laws on Healthcare AI - BastionGPT](https://bastiongpt.com/post/state-laws-on-healthcare-ai)
100. [What AI Disclosure and Consent Requirements Do We Need to Comply With Under New State Laws?](https://mosaiclifetech.com/governance/what-ai-disclosure-and-consent-requirements-do-we-need-to-comply-with)
101. [HRx: New Year, New AI Rules: Healthcare AI Laws Now in Effect - Akerman LLP](https://www.akerman.com/en/perspectives/hrx-new-year-new-ai-rules-healthcare-ai-laws-now-in-effect.html)
102. [Shaping the Future: Navigating State-Level AI Legislation in Healthcare](https://www.healthcarelawinsights.com/2026/02/shaping-the-future-navigating-state-level-ai-legislation-in-healthcare/)
103. [AI Laws by State (2026): What Small Businesses Must Follow](https://startbusinessbystate.com/ai-laws-by-state/)
104. [One note in three: a verified census of three deployed AI scribes, and the instrument that counted it](https://arxiv.org/pdf/2608.31017)
105. [Latest news - AI and Digital Regulations Service for health and social care](https://www.digitalregulations.innovation.nhs.uk/latest-news/)
106. [Ambient Scribing in the NHS: A Compliance Framework Suppliers Cannot Ignore, Moona Malik, Pieter Erasmus](https://biotalk.twobirds.com/post/102nfao/ambient-scribing-in-the-nhs-a-compliance-framework-suppliers-cannot-ignore)
107. [Ambient Voice Technology Self-Certified Supplier Registry - NHS England Digital](https://digital.nhs.uk/services/ambient-scribing/ambient-voice-technology-self-certified-supplier-registry)
108. [NHS England lists 19 suppliers meeting criteria for ambient voice registry](https://htn.co.uk/2026/01/19/nhs-england-lists-19-suppliers-meeting-criteria-for-ambient-voice-registry/)
109. [Ambient voice technology regulation: techUK position statement](https://www.techuk.org/insights/policy-views/ambient-voice-technology-regulation-techuk-position-statement)
110. [MHRA clarifies regulatory medical devices status of ambient voice technologies](https://htn.co.uk/2026/07/29/mhra-clarifies-regulatory-medical-devices-status-of-ambient-voice-technologies/)
111. [NHS England — Midlands » Midlands leads the way on ambient voice technology](https://www.england.nhs.uk/midlands/2026/07/15/midlands-leads-the-way-on-ambient-voice-technology/)
112. [GitHub - sipratt-p/scribe-bench: Open-data evaluation harness for ambient clinical documentation: 7 ASR systems, note generation, LoRA fine-tuning, a claim-level verifier and clinician-defined scorers on PriMock57 and ACI-Bench · GitHub](https://github.com/sipratt-p/scribe-bench)
113. [OpenAI unveils ChatGPT Health, says 230 million users ask about health each week](https://techcrunch.com/2026/01/07/openai-unveils-chatgpt-health-says-230-million-users-ask-about-health-each-week/)
114. [OpenAI makes ChatGPT Health available to all US users](https://techcrunch.com/2026/07/23/openai-makes-chatgpt-health-available-to-all-u-s-users/)
115. [Halluminate: RL environment vendor profile](https://www.rl-list.com/vendors/halluminate)
116. [Thoreau commits \$500M to new frontier AI lab for healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/ex-genentech-meta-aws-ai-leaders-launch-health-ai-lab-500m-backing)
117. [AI Tutoring/Training for Physicians: Best Platforms, Pay Rates, and Real Doctor Experiences](https://mozibox.com/articles/1769)
118. [MHRA Ambient Voice Technology Guidance 2026:](https://8foldgovernance.com/mhra-ambient-voice-technology-guidance-ai-scribes-nhs/)
119. [MHRA Ambient Voice Technology 2026: When an AI Scribe Is a Medical Device in Great Britain](https://meddeviceguide.com/blog/mhra-ambient-voice-technology-avt-ai-scribe-medical-device-qualification-guide)
120. [Google Brings Mechanize’s AI Coding Talent to DeepMind. What Happened to the Reported \$1.5 Billion Deal? - Kingy AI](https://kingy.ai/news/google-mechanize-ai-coding-talent-deal/)
