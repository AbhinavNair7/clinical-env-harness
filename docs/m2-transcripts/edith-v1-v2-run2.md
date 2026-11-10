# edith_marsh

- **Clinician:** openai/gpt-6.1-sol
- **Simulators:** patient openai/gpt-6-luna, carer openai/gpt-6-luna
- **Checker:** openai/gpt-6-luna
- **Inspect log:** logs/2026-11-04T15-53-36-00-00_case_27ZnpXQLmHL4aNyKLAfD5Z.eval
- **Tokens (all epochs):** clinician: 438367 in (433682 cached) / 14118 out; patient: 40044 in (39936 cached) / 2057 out; checker: 13339 in (0 cached) / 12962 out; carer: 87772 in (87598 cached) / 4864 out
- **Clinician memory:** notes

## Visit 1, home visit, Thursday 5 November 2026

- **Turns:** 32 used of a 40-turn budget (hard cap 80); ended by plan
- **Checker:** 2 flagged drafts, 2 regenerated; 12 interjection calls stayed silent

### What the GP was told

```text
Visit 1: home visit, Thursday 5 November 2026.
Patient: Edith Marsh, 84. Lives alone in a two-storey terraced house. Mild Alzheimer's disease, hypertension. Admitted in October after a fall with a postural drop in blood pressure. Care agency visits twice daily; her daughter visits on Sundays.
Present: Edith Marsh (patient), Janet Price (daughter).
Reason for this visit: The care agency phoned the practice: Edith was found on the floor last week and is missing evening medicines. Janet is there for the visit.
Records you can read: GP record (gp_record), Hospital discharge summary (discharge_summary), Care agency notes (care_agency_notes), Pharmacy record (pharmacy_record), Ambulance service patient report (ambulance_report).
```

### Consultation

` 1` **GP → Edith Marsh:** Hello Edith, I'm your GP visiting to understand the fall and help you stay safe at home. Is it all right if Janet joins our conversation?

` 1` **Edith Marsh:** Oh yes, of course, love. Janet can stay.

` 2` **GP → Edith Marsh:** How have you been feeling, and what do you remember about being found on the floor last week?

` 2` **Edith Marsh:** Oh, I’m not too bad, thank you. I remember the one before I went to hospital, but I couldn’t tell you much about how I ended up on the floor, love.

` 3` _GP reads `gp_record`_
> GP record:
> Edith MARSH   Female   Age 84   Usual GP: Dr A Okafor
> 
> PROBLEMS - ACTIVE
>   Aug 2024   Alzheimer's disease (memory clinic: mild)
>   Mar 2021   Chronic kidney disease stage 3a
>   Jun 2015   Primary open angle glaucoma
>   Feb 2010   Osteoarthritis of knee
>   Apr 2003   Essential hypertension
> 
> PROBLEMS - PAST / MINOR
>   Nov 2025   Low back pain
>   Jan 2023   Herpes zoster (shingles), thoracic
>   Sep 2022   Seborrhoeic keratosis
>   2020       Benign paroxysmal positional vertigo - resolved after Epley manoeuvre
>   Jul 2019   Urinary tract infection
>   Oct 2017   Osteopenia (DEXA)
>   Mar 2014   Cataract extraction, left eye
>   Nov 2012   Cataract extraction, right eye
>   May 2008   Carpal tunnel syndrome, right
>   1996       Total abdominal hysterectomy (fibroids)
>   1971       Appendicectomy
> 
> REPEAT MEDICATION (last issued 22 Oct 2026)
>   Furosemide 40mg tablets - one each morning - 28 tablets
>   Amlodipine 10mg tablets - one each morning - 28 tablets
>   Donepezil 10mg tablets - one at night - 28 tablets
>   Atorvastatin 20mg tablets - one at night - 28 tablets
>   Adcal-D3 chewable tablets - one twice a day - 56 tablets
>   Latanoprost 50micrograms/ml eye drops - one drop both eyes at night - 2.5ml
>   Paracetamol 500mg tablets - two up to four times a day when required - 100 tablets
> 
> CONSULTATIONS (most recent first)
>   22 Oct 2026  Admin           Repeat prescription issued, all repeat items. Pharmacy to blister pack.
>   21 Oct 2026  Document        Hospital discharge summary received (Elderly Care). Filed, awaiting GP review.
>   12 Oct 2026  Document        ED attendance notification: fall at home, admitted.
>   04 Sep 2026  Practice nurse  Seasonal influenza vaccine given. COVID-19 booster given.
>   03 Jul 2026  Telephone       Daughter asking for eye drops on repeat. Already on repeat; advised.
>   18 Apr 2026  GP              Medication review. BP 146/82 sitting. No falls reported. Memory stable per daughter. Continue current medication.
>   10 Feb 2026  Letter          Eye clinic: glaucoma stable on latanoprost. Discharged to optometrist.
>   10 Nov 2025  GP              Low back pain after gardening. No red flags. Paracetamol, activity advice.
>   10 Aug 2025  Letter          Memory clinic review: mild Alzheimer's disease, stable. Continue donepezil. Discharged to GP.
>   14 May 2025  Letter          Letter from adult social care: package of care started, two 30-minute calls daily (morning and evening).
>   09 Apr 2025  Results         eGFR 52, potassium 4.6, HbA1c 39, cholesterol 4.1. Stable.
>   05 Mar 2025  GP              Annual hypertension review. BP 138/78. Continue.

` 4` _GP reads `discharge_summary`_
> Hospital discharge summary:
> DISCHARGE SUMMARY - Elderly Care, Ward 9
> Admitted 12 Oct 2026   Discharged 19 Oct 2026
> Presenting complaint: found on the floor at home by carer.
> Diagnosis: Fall at home secondary to postural hypotension.
> Other problems: hypertension; Alzheimer's disease (mild); CKD 3a; glaucoma.
> Investigations: bloods unremarkable apart from eGFR 49 (baseline 52). ECG sinus rhythm,
>   normal intervals. CXR clear. No head injury; CT head not indicated.
> Medication changes: Furosemide 40mg OM STOPPED - no evidence of heart failure, postural drop. GP please update repeats.
> Medication on discharge: amlodipine 10mg OM; donepezil 10mg ON; atorvastatin 20mg ON;
>   Adcal-D3 one BD; latanoprost both eyes ON; paracetamol 1g QDS PRN.
> Therapy: Assessed by physiotherapy. Discharged with a walking frame; advised to use it at all times.
> Social: lives alone; package of care twice daily, restarted on discharge; daughter visits weekly.
> GP actions: please review BP in 2 weeks.

` 5` _GP reads `care_agency_notes`_
> Care agency notes:
> CARE RECORD - Mrs Edith Marsh. Package: 2 calls daily (AM, PM). Medication: prompt from blister pack.
> MAR summary: Evening medicines, last 14 days: given 5, not given 9 (client asleep / declined).
> 
> Wed 04 Nov AM 08:06-08:20 Assisted with wash and dressing. Prompted medication, taken. Toast and tea. Client in good spirits.
> Wed 04 Nov PM 21:12-21:25 Client in bed, settled. Medication not given, client asleep.
> Tue 03 Nov AM 08:10-08:24 Personal care given. Medication taken. Breakfast made. Chatty this morning.
> Tue 03 Nov PM 21:26-21:38 Client in bed, settled. Medication offered, declined. Door locked.
> Mon 02 Nov AM 07:58-08:13 Personal care given. Medication taken. Cereal and tea. Sandwich made and left in fridge for lunch.
> Mon 02 Nov PM 21:14-21:29 Lunch sandwich still in fridge, client said she wasn't hungry. Supper of tea and biscuits. Client settled for bed.
> Sun 01 Nov AM 08:21-08:35 Personal care given. Medication taken. Daughter visiting today.
> Sun 01 Nov PM 20:52-21:06 Medication given. Client watching TV. All well.
> Sat 31 Oct AM 08:02-08:17 Personal care given. Medication taken. Home clean and tidy.
> Sat 31 Oct PM 21:31-21:44 Client in bed, asleep. Did not wake client. Medication not given.
> Fri 30 Oct AM 08:15-08:29 Personal care given. Medication taken. Client cheerful.
> Fri 30 Oct PM 21:05-21:18 Medication offered, client said she had already taken them. Settled.
> Thu 29 Oct AM 08:04-08:18 Personal care given. Medication taken. Porridge and tea.
> Thu 29 Oct PM 21:22-21:35 Client in bed, settled. Medication not given, client asleep.
> Wed 28 Oct AM 08:12-08:26 Personal care given. Medication taken. Client in good spirits.
> Wed 28 Oct PM 21:09-21:23 Medication offered, declined. Client tired.
> Tue 27 Oct AM 07:48-09:55 On arrival client found on hallway floor, unable to say how long she had been there. Chatty, no obvious injury. 999 called, paramedics attended, client not taken to hospital. Carer stayed until paramedics left. Office informed.
> Tue 27 Oct PM 20:48-21:03 Medication given. Client tired but in good spirits.

` 6` _GP reads `pharmacy_record`_
> Pharmacy record:
> PATIENT MEDICATION RECORD - Edith MARSH
> Monitored dosage system: weekly 7-day blister pack, delivered Mondays.
> Supplied separately: Adcal-D3 chewable tablets, latanoprost eye drops, paracetamol 500mg.
>   02 Nov 2026  Weekly blister pack dispensed. Morning: furosemide 40mg, amlodipine 10mg. Night: donepezil 10mg, atorvastatin 20mg.
>   26 Oct 2026  Weekly blister pack dispensed, contents unchanged.
>   22 Oct 2026  Repeat prescription received from GP: furosemide 40mg, amlodipine 10mg,
>              donepezil 10mg, atorvastatin 20mg, Adcal-D3, latanoprost, paracetamol.
>   05 Oct 2026  Weekly blister pack dispensed. Morning: furosemide 40mg, amlodipine 10mg. Night: donepezil 10mg, atorvastatin 20mg.

` 7` _GP reads `ambulance_report`_
> Ambulance service patient report:
> AMBULANCE SERVICE PATIENT REPORT (copy to GP)
> Incident 27 Oct 2026. Call 07:56, on scene 08:41, left scene 09:50. Caller: care worker.
> History: Unwitnessed fall. Found by care worker at the morning call lying on the hallway floor. Patient unable to say when she fell or how long she was on the floor; thinks she "must have slipped".
> Past history: hypertension, Alzheimer's disease, glaucoma. Recent admission after a fall.
> Medication: per blister pack. No anticoagulants.
> Obs: RR 16, SpO2 96% air, HR 78 regular, BP 134/76 sitting, temp 36.5, BM 6.4.
>   GCS 15; unsure of the date, which the carer says is usual for her.
> 12-lead ECG: sinus rhythm 76, no acute changes.
> Secondary survey: no head injury, no neck or hip pain, full range of movement all limbs.
>   Skin intact. Stood with help of one and walked to her chair with a stick.
> Impression: mechanical fall, no injury.
> Disposition: not conveyed. Patient declined hospital; has capacity for this decision.
>   Left in the care of the care worker. Worsening advice given. GP to consider falls referral.

` 8` **GP → Edith Marsh:** Have you had any dizziness, fainting, pain or other new symptoms since coming home from hospital?

` 8` **Edith Marsh:** No fainting, no, and nothing new really. Just my knees, the usual. I take a paracetamol if they’re bothering me.

` 8` **Janet Price (adds):** Mum’s managing fine. She’s always tidy and cheerful when I come round.

` 9` _GP examines: General condition, hydration, temperature, pulse and rhythm, respiratory rate, oxygen saturation; lying blood pressure after rest and standing blood pressure at 1 and 3 minutes with symptoms_ → Please name one specific examination.

`10` _GP examines: Lying and standing blood pressure with pulse and symptoms_ → Lying 138/76, pulse 76 regular; standing 108/64, pulse 82 at 1 minute and 112/66, pulse 80 at 3 minutes; dizzy on standing. [x_postural_bp]

`11` **GP → Edith Marsh:** Your blood pressure drops when you stand. The hospital stopped your water tablet, but it appears to have stayed in your packs. May I check your medicines and how you take them?

`11` **Edith Marsh:** Oh yes, you can have a look, love. I take all my tablets—the girls see to that. I still have my water tablet every morning, though; it does send me up and down to the toilet.

`11` **Janet Price (adds):** I thought the hospital had sorted her tablets out and the chemist puts them in the pods.

`12` _GP examines: Inspect all medicines, blister packs and separate eye drops and Adcal supplies in the home_ → Morning slots hold furosemide 40 mg and amlodipine 10 mg; night slots hold donepezil 10 mg and atorvastatin 20 mg. Five of last week's seven night slots are still full. The latanoprost bottle by her bed was opened nine weeks ago and is still nearly full. [x_dosette]

`13` **GP → Edith Marsh:** What happens with your evening medicines and eye drops when the carers come?

`13` **Edith Marsh:** The girls see to my tablets, though I’m often asleep by the time the night girl comes. I do my eye drops myself at bedtime.

`13` **Janet Price (adds):** I’d assumed the carers did her eye drops along with her tablets.

`14` **GP → Edith Marsh:** Could you talk me through getting around, washing, dressing, making meals and getting to the toilet on a usual day?

`14` **Edith Marsh:** I manage with my stick, love. The frame’s for when I’m poorly. I see to my own washing and dressing; the girls are just there for company.
> ⚑ checker, draft 1: **hidden_revealed**: She disclosed accidents before the GP asked about her bladder, leaking, or accidents.
> ⚑ checker, draft 1: **over_cooperative**: She answered more than two distinct areas of the GP’s multi-part question in one turn.
> rejected draft 1: _I manage with my stick, love. I see to my own washing and dressing, and I do all my meals myself. I go upstairs slowly, holding the rail—the bedroom and toilet are up there. I can’t always get to the toilet in time, but it’s only the odd accident._

`15` **GP → Janet Price:** What have you personally noticed about Edith's mobility and day-to-day care needs since discharge?

`15` **Janet Price:** Last Sunday she grabbed the table to get up from her chair. I’ve found wet clothes in the wash basket, and there’s out-of-date food in the fridge. The carers come morning and evening; they do her tablets and help her wash, I think.

`15` **Edith Marsh (adds):** I do my own washing and dressing, love, and I make my own meals. I’ve always managed that.

`16` _GP examines: Observe chair rise, transfers and walking with her usual aid and assess safe use of the prescribed walking frame_ → Rises from the chair at the second attempt, pushing up with her arms. Walks slowly with a stick, reaching for furniture; unsteady on turning. Does not use the walking frame. [x_gait]

`17` _GP examines: Inspect home for falls hazards, stairs, access to toilet and location of walking frame and emergency call equipment_ → Please name one specific examination.

`18` _GP examines: Home falls hazards assessment_ → Loose rug in the hallway; dim landing light; walking frame folded by the front door. [x_home]

`19` **GP → Edith Marsh:** What have you eaten and drunk since yesterday morning?

`19` **Edith Marsh:** Oh, I couldn’t tell you exactly, love. I make my own meals, I always have. I like my quiz shows in the afternoon; I’m not bad at them, you know.
> ⚑ checker, draft 1: **invented_fact**: She reports drinking a cup of tea, an unscripted fact about her fluid intake.
> rejected draft 1: _Oh, I couldn’t rightly say, love. I make my own meals, as I always have. I do like a nice cup of tea._

`20` _GP examines: Nutritional status including weight and recent weight trend_ → Not available during this home visit. If you need it, request it in your plan.

`21` **GP → Janet Price:** How much support can you realistically provide, and how is this affecting you?

`21` **Janet Price:** I work full time, so I can only come on Sundays. I’m frightened you’ll say she needs a home, and I feel guilty I’m not here more. I want her to stay at home, with more help if that’s what it takes.

`22` **GP → Edith Marsh:** What matters most to you about where you live and what help you receive?

`22` **Edith Marsh:** I want to stay in my own home, love. I don’t want to go into a home. My eyes aren’t what they were, but I’ve got drops for them.

`23` **GP → Edith Marsh:** I want to help you stay here safely. Your blood pressure falls when you stand, you are unsteady, and late visits mean medicines and meals are being missed. Would you accept earlier evening carers, extra help with lunch and medicines, and a therapist helping with your frame and home safety?

`23` **Edith Marsh:** Oh, I don’t want to be a bother, love. If it helps me stay here, I suppose we could try it. I manage with my stick, though—the frame’s for when I’m poorly.

`24` **GP → Edith Marsh:** So I can check I've explained it clearly, what do you understand could happen if you keep using only the stick, and how might the frame and extra help make staying home safer?

`24` **Edith Marsh:** Well, I might wobble and have another fall, I suppose. The frame could steady me, and the extra help might make things safer. I’ll try, if it means I can stay here.

`25` **GP → Edith Marsh:** Have your eyes changed suddenly, become painful or red, or has your eyesight gradually become less clear?

`25` **Edith Marsh:** It’s just not as clear as it used to be, love. It hasn’t suddenly changed, and it’s not painful or red.

`26` **GP → Edith Marsh:** Are you having trouble reaching the toilet in time, or any burning when you pass urine?

`26` **Edith Marsh:** Oh, I do have the odd accident if I can’t get there in time, love. It’s a bit embarrassing. No burning, though.

`27` _GP examines: Cardiovascular examination including signs of heart failure_ → Heart sounds normal, chest clear, no ankle oedema, JVP not raised. [x_cardio]

`28` _GP examines: Neurological examination for focal deficit or parkinsonism_ → Unremarkable.

`29` **GP → Edith Marsh:** If you fell when alone, how would you call for help?

`29` **Edith Marsh:** I’ve got one of those buttons somewhere, love, but I can’t think where I’ve put it.

`30` **GP → Edith Marsh:** Since the fall last week, have you had another fall, hit your head, or had any new pain, chest pain or racing heartbeat?

`30` **Edith Marsh:** No, love, I haven’t had another fall or hit my head. No new pain, chest pain or racing heart either.

`31` **GP → Janet Price:** There is a prescribing error: the stopped water tablet was reissued and is still being taken. I'll correct it with the pharmacy today, arrange safe replacement packs, and review Edith's pressure promptly. She also needs reliably earlier and longer care visits, meal and fluid support, observed medicines and drops, and urgent falls and home-safety support—not automatically a care home. Can you stay until today's medicine and care arrangements are confirmed?

`31` **Janet Price:** Yes, I can stay until we know what’s happening today. I can’t be here regularly, though—I work full time and only get round on Sundays.

`31` **Edith Marsh (adds):** Thank you, love. I do want to stay here, and I’ll try the extra help. I don’t want Janet worrying—she’s got her work.

`32` _GP submits plan_

### Plan

**Problems**
- Recurrent unwitnessed falls with persistent symptomatic orthostatic hypotension: 138/76 lying to 108/64 standing at 1 minute, with dizziness; multiple contributing factors rather than a securely established mechanical fall.
- Medication reconciliation failure: furosemide stopped in hospital but subsequently reissued, dispensed and taken; no current clinical evidence of heart failure.
- Unreliable evening medication administration, including donepezil and atorvastatin; uncertain administration of separately supplied Adcal-D3 and latanoprost.
- Unsafe mobility and functional needs exceeding current support: furniture-walking, difficulty rising, prescribed frame not used, dependence on carers for personal care despite self-reported independence.
- Risk of inadequate nutrition and hydration, functional urinary incontinence, environmental falls hazards and unavailable personal alarm.
- Alzheimer's disease with limited recall and insight, but demonstrated understanding of the proposed home-support decision and agreement to a trial.
- Gradual visual deterioration with glaucoma and unreliable eye-drop use; opened latanoprost bottle nine weeks old.
- Daughter's anxiety and limited capacity to provide regular care.

**Function and ADLs:** Lives alone in a two-storey house with twice-daily care and Sunday daughter visits. Requires assistance with washing/dressing and medication administration; meal preparation and intake are unreliable. Rises on second attempt using arms, walks slowly with stick and furniture support, unsteady turning; frame unused. Recurrent falls with uncertain time on floor and no accessible alarm. Wants to remain home and accepts enhanced support and frame trial after explaining the risks back.

**Risks**
- Further falls, syncope, fracture or prolonged time on floor from orthostatic hypotension, medication effects, impaired gait, poor vision and home hazards.
- Dehydration, acute kidney injury or electrolyte disturbance with CKD3a and continued diuretic exposure.
- Medication omissions, accidental duplicate doses and ineffective glaucoma treatment.
- Malnutrition, functional decline, incontinence-related harm and unmet care needs between visits.
- Breakdown of home support if daughter's availability is overestimated.

**Actions**

| Type | Detail | Rationale | Urgency |
|---|---|---|---|
| medication_change | Stop furosemide 40 mg immediately, remove from GP repeat prescribing and contact dispensing pharmacist today to remove it safely from all current and pending packs and provide corrected packs before the next dose. Do not ask Edith to identify tablets herself. Confirm changes in writing to agency, daughter and pharmacy and obtain acknowledgement. | Explicitly stopped during admission for postural hypotension; inadvertently restarted and still taken, without heart failure evidence. | same_day |
| medication_change | Reduce amlodipine from 10 mg to 5 mg daily with pharmacist-prepared corrected packs and updated MAR. Review standing BP and symptoms within 48–72 hours, with further reduction or withholding if symptomatic hypotension persists; individualise longer-term BP targets to standing pressure, frailty and falls. | Large symptomatic postural drop with recurrent falls despite acceptable lying BP; current antihypertensive burden is excessive. | same_day |
| investigation | Arrange FBC, U&E, creatinine/eGFR, sodium, potassium and calcium within 24–48 hours; assess hydration and oral intake today. Arrange ECG promptly, reviewing rate and conduction in relation to unexplained falls and donepezil; escalate if concerning symptoms or findings. | CKD, diuretic exposure and possible low intake increase renal/electrolyte risk; an unwitnessed fall cannot conclusively be labelled mechanical. | within_days |
| care_package_change | Contact agency and adult social care today for urgent reassessment: move evening call earlier while Edith is awake, provide sufficient time for personal care, observed medicines and eye drops, supper and fluids, and add a midday meal/hydration and welfare call. Reconcile commissioned 30-minute calls with documented 12–15-minute calls and establish an accountable interim schedule today. Confirm actual attendance and escalation for declined/missed doses or uneaten meals. | Nine of fourteen evening administrations missed; late and short visits do not meet demonstrated needs. Daughter cannot substitute for paid support. | same_day |
| medication_change | Pharmacist-led review of every medicine and MAR, including separate Adcal-D3 and PRN paracetamol. Consider moving suitable once-daily oral medicines to a reliably supervised morning time. Establish consecutive missed donepezil doses before restarting: if interrupted for a week or longer, obtain prescribing advice and re-titrate rather than automatically restarting 10 mg. Avoid double doses. Replace old latanoprost bottle today, use according to product storage/opening-expiry instructions and arrange trained carer administration with documented consent. | Inspection and records demonstrate missed oral doses and unreliable drop use; the current nine-week-open bottle should not remain in use. | same_day |
| referral | Urgent community falls/geriatric and physiotherapy referral for multifactorial falls assessment, gait, strength, transfers and supervised frame training. Review footwear, vision, continence, cognition and fracture risk; review osteopenia, vitamin D/calcium intake and need for osteoporosis assessment/treatment. | Repeated falls, impaired transfers and gait, prescribed frame not used and multiple modifiable risks. | within_days |
| equipment | Arrange urgent OT home assessment including stairs, lighting, toilet access, chair height and rails. With consent remove the loose hallway rug and improve landing lighting today; unfold and position the frame for accessible supervised use. Locate or replace and test the pendant alarm, arrange falls-detection/telecare and safe responder access; assess a commode if toilet access is unsafe. | Environmental hazards, functional incontinence and inability to summon help compound prolonged-lie risk. | same_day |
| investigation | Arrange measured weight, weight trend and MUST nutritional assessment through community staff; inspect food availability/expiry with consent and establish a meal/fluid record. Assess continence and toileting access rather than diagnosing UTI in the absence of suggestive symptoms; refer to continence service if ongoing after diuretic withdrawal and improved access. | Uneaten meals, expired food and uncertain intake suggest nutritional risk; urgency may relate to diuretic and mobility rather than infection. | within_days |
| referral | Arrange optometrist assessment of acuity and glaucoma control promptly, with ophthalmology input if indicated, ensuring reliable drops meanwhile. | Gradual visual decline and uncertain adherence may increase falls and threaten glaucoma control; no current acute ocular red flags. | within_days |
| safeguarding | Document consent and decision-specific capacity for home-support choices: Edith understands fall risk, benefit of assistance and expresses a consistent preference to remain home. Raise medication error as a patient-safety incident and urgently escalate unmet needs/short visits to agency manager and social care. Consider local adult safeguarding referral for neglect or self-neglect if essential care cannot be reliably delivered or investigation identifies neglect; do not assume daughter is responsible. If safe interim support cannot be secured today, arrange urgent intermediate care or hospital assessment, involving Edith and assessing capacity for that decision. | There is an actual systems-related medication error and significant unmet need, but dementia alone does not establish incapacity or mandate residential placement. | same_day |
| carer_support | Acknowledge Janet's concerns, explain that home support is being strengthened rather than presuming care-home placement, and offer a carer's assessment and dementia support services. Use her agreed presence today only until arrangements are confirmed; do not make her responsible for daily medication or care. | Janet works full-time, visits weekly and feels guilty and anxious. | within_days |
| advice | Explain the prescribing error openly with apology. Advise slow staged rising, sitting down immediately if dizzy, regular fluids unless a future clinical reason to restrict, regular meals, supported frame use and avoiding stairs or walking alone while dizzy. Provide a simple written medication/support plan to Edith, Janet and carers, including contact numbers. | Supports informed participation and reduces immediate postural and communication risks. | same_day |
| follow_up | Confirm corrected medication packs and safe care cover today; telephone agency/Janet tomorrow to verify implementation. Arrange home review in 48–72 hours for lying/standing BP, dizziness, pulse, blood results, intake and mobility; reassess again within 1–2 weeks after changes, including adherence, eye drops, nutritional measures, falls and adequacy of care. | High immediate risk requires confirmation of actions rather than referral alone. | within_days |

**Discrepancies**
- Hospital stopped furosemide, while GP repeat, pharmacy packs and Edith's account show continued morning use. → Discharge instruction and absent heart failure findings support stopping; physical pack inspection establishes actual exposure. Correct every prescribing/dispensing/MAR source today.
- Edith says she takes all medicines and carers manage them; daughter assumed hospital/pharmacy arrangements guaranteed this. → MAR shows nine missed evenings in fourteen days and five of seven night slots remain full. Treat administration as unreliable, not simply patient non-compliance; revise timing and supervision.
- Edith says she administers her own drops, while daughter assumes carers do so. → Nearly full nine-week-open bottle strongly suggests unreliable use; allocate a named administration responsibility and fresh supply.
- Edith reports independence with washing, dressing, meals and stick mobility; daughter initially describes her as managing well. → Care notes document personal-care help and uneaten meals; daughter reports wet clothes and expired food; observed transfers and gait show impairment. Weekly cheerful appearance does not establish daily functional safety.
- Ambulance impression was mechanical fall with normal sitting BP, whereas hospital recorded postural hypotension. → Cause of unwitnessed fall remains uncertain. Today's reproducible symptomatic orthostatic drop and continued diuretic exposure identify an important ongoing contributor; normal sitting BP and an earlier reassuring ECG do not exclude it.
- Prescribed frame is viewed by Edith as only needed when ill; falls alarm is reportedly owned but cannot be located. → Current observed gait supports frame use now with training, and an inaccessible alarm is not effective protection.
- Commissioned care is two 30-minute calls, while routine records show approximately 12–15 minutes and late evening attendance. → Ask agency to explain and correct duration/timing against assessed need, with social-care review and escalation if necessary.

**Follow-up:** Same-day confirmation with pharmacy, agency and social care before Janet leaves; next-day implementation check. Home review in 48–72 hours with postural BP, symptoms, blood results and actual care delivery, followed by comprehensive review within 1–2 weeks. Named GP/practice team to track referrals and outstanding actions.

**Safety-netting:** Call 999 for collapse with incomplete recovery, chest pain, new severe breathlessness, stroke symptoms, serious injury, inability to get up safely after a fall, or head injury with concerning symptoms. Do not attempt to lift Edith unaided. Seek same-day GP/111 advice for further falls or near-faints, persistent dizziness, new confusion, markedly reduced intake/urine, inability to take essential medicines or failed care visits; use emergency assessment if she cannot be kept safe. Sudden visual loss or painful red eye needs urgent same-day eye/emergency assessment. Keep the functioning alarm worn and telephone/contact numbers within reach.

## Visit 2, telephone consultation, Thursday 19 November 2026

- **Turns:** 17 used of a 20-turn budget (hard cap 40); ended by plan
- **Checker:** 0 flagged drafts, 0 regenerated; 0 interjection calls stayed silent

### What the GP was told

```text
Visit 2: telephone consultation, Thursday 19 November 2026.
Patient: Edith Marsh, 84. Lives alone in a two-storey terraced house. Mild Alzheimer's disease, hypertension. Admitted in October after a fall with a postural drop in blood pressure. Care agency visits twice daily; her daughter visits on Sundays.
Present: Janet Price (daughter).
Reason for this visit: Janet asked for a call back after her mother's fall.
Records you can read: GP record (gp_record), Hospital discharge summary (discharge_summary), Care agency notes (care_agency_notes), Pharmacy record (pharmacy_record), Ambulance service patient report (ambulance_report).

Your notes from earlier visits:

Visit 1, home visit, Thursday 5 November 2026 (14 days ago)
Problems:
- Recurrent unwitnessed falls with persistent symptomatic orthostatic hypotension: 138/76 lying to 108/64 standing at 1 minute, with dizziness; multiple contributing factors rather than a securely established mechanical fall.
- Medication reconciliation failure: furosemide stopped in hospital but subsequently reissued, dispensed and taken; no current clinical evidence of heart failure.
- Unreliable evening medication administration, including donepezil and atorvastatin; uncertain administration of separately supplied Adcal-D3 and latanoprost.
- Unsafe mobility and functional needs exceeding current support: furniture-walking, difficulty rising, prescribed frame not used, dependence on carers for personal care despite self-reported independence.
- Risk of inadequate nutrition and hydration, functional urinary incontinence, environmental falls hazards and unavailable personal alarm.
- Alzheimer's disease with limited recall and insight, but demonstrated understanding of the proposed home-support decision and agreement to a trial.
- Gradual visual deterioration with glaucoma and unreliable eye-drop use; opened latanoprost bottle nine weeks old.
- Daughter's anxiety and limited capacity to provide regular care.
Function and ADLs: Lives alone in a two-storey house with twice-daily care and Sunday daughter visits. Requires assistance with washing/dressing and medication administration; meal preparation and intake are unreliable. Rises on second attempt using arms, walks slowly with stick and furniture support, unsteady turning; frame unused. Recurrent falls with uncertain time on floor and no accessible alarm. Wants to remain home and accepts enhanced support and frame trial after explaining the risks back.
Risks:
- Further falls, syncope, fracture or prolonged time on floor from orthostatic hypotension, medication effects, impaired gait, poor vision and home hazards.
- Dehydration, acute kidney injury or electrolyte disturbance with CKD3a and continued diuretic exposure.
- Medication omissions, accidental duplicate doses and ineffective glaucoma treatment.
- Malnutrition, functional decline, incontinence-related harm and unmet care needs between visits.
- Breakdown of home support if daughter's availability is overestimated.
Actions:
- medication_change (same_day): Stop furosemide 40 mg immediately, remove from GP repeat prescribing and contact dispensing pharmacist today to remove it safely from all current and pending packs and provide corrected packs before the next dose. Do not ask Edith to identify tablets herself. Confirm changes in writing to agency, daughter and pharmacy and obtain acknowledgement.. Why: Explicitly stopped during admission for postural hypotension; inadvertently restarted and still taken, without heart failure evidence.
- medication_change (same_day): Reduce amlodipine from 10 mg to 5 mg daily with pharmacist-prepared corrected packs and updated MAR. Review standing BP and symptoms within 48–72 hours, with further reduction or withholding if symptomatic hypotension persists; individualise longer-term BP targets to standing pressure, frailty and falls.. Why: Large symptomatic postural drop with recurrent falls despite acceptable lying BP; current antihypertensive burden is excessive.
- investigation (within_days): Arrange FBC, U&E, creatinine/eGFR, sodium, potassium and calcium within 24–48 hours; assess hydration and oral intake today. Arrange ECG promptly, reviewing rate and conduction in relation to unexplained falls and donepezil; escalate if concerning symptoms or findings.. Why: CKD, diuretic exposure and possible low intake increase renal/electrolyte risk; an unwitnessed fall cannot conclusively be labelled mechanical.
- care_package_change (same_day): Contact agency and adult social care today for urgent reassessment: move evening call earlier while Edith is awake, provide sufficient time for personal care, observed medicines and eye drops, supper and fluids, and add a midday meal/hydration and welfare call. Reconcile commissioned 30-minute calls with documented 12–15-minute calls and establish an accountable interim schedule today. Confirm actual attendance and escalation for declined/missed doses or uneaten meals.. Why: Nine of fourteen evening administrations missed; late and short visits do not meet demonstrated needs. Daughter cannot substitute for paid support.
- medication_change (same_day): Pharmacist-led review of every medicine and MAR, including separate Adcal-D3 and PRN paracetamol. Consider moving suitable once-daily oral medicines to a reliably supervised morning time. Establish consecutive missed donepezil doses before restarting: if interrupted for a week or longer, obtain prescribing advice and re-titrate rather than automatically restarting 10 mg. Avoid double doses. Replace old latanoprost bottle today, use according to product storage/opening-expiry instructions and arrange trained carer administration with documented consent.. Why: Inspection and records demonstrate missed oral doses and unreliable drop use; the current nine-week-open bottle should not remain in use.
- referral (within_days): Urgent community falls/geriatric and physiotherapy referral for multifactorial falls assessment, gait, strength, transfers and supervised frame training. Review footwear, vision, continence, cognition and fracture risk; review osteopenia, vitamin D/calcium intake and need for osteoporosis assessment/treatment.. Why: Repeated falls, impaired transfers and gait, prescribed frame not used and multiple modifiable risks.
- equipment (same_day): Arrange urgent OT home assessment including stairs, lighting, toilet access, chair height and rails. With consent remove the loose hallway rug and improve landing lighting today; unfold and position the frame for accessible supervised use. Locate or replace and test the pendant alarm, arrange falls-detection/telecare and safe responder access; assess a commode if toilet access is unsafe.. Why: Environmental hazards, functional incontinence and inability to summon help compound prolonged-lie risk.
- investigation (within_days): Arrange measured weight, weight trend and MUST nutritional assessment through community staff; inspect food availability/expiry with consent and establish a meal/fluid record. Assess continence and toileting access rather than diagnosing UTI in the absence of suggestive symptoms; refer to continence service if ongoing after diuretic withdrawal and improved access.. Why: Uneaten meals, expired food and uncertain intake suggest nutritional risk; urgency may relate to diuretic and mobility rather than infection.
- referral (within_days): Arrange optometrist assessment of acuity and glaucoma control promptly, with ophthalmology input if indicated, ensuring reliable drops meanwhile.. Why: Gradual visual decline and uncertain adherence may increase falls and threaten glaucoma control; no current acute ocular red flags.
- safeguarding (same_day): Document consent and decision-specific capacity for home-support choices: Edith understands fall risk, benefit of assistance and expresses a consistent preference to remain home. Raise medication error as a patient-safety incident and urgently escalate unmet needs/short visits to agency manager and social care. Consider local adult safeguarding referral for neglect or self-neglect if essential care cannot be reliably delivered or investigation identifies neglect; do not assume daughter is responsible. If safe interim support cannot be secured today, arrange urgent intermediate care or hospital assessment, involving Edith and assessing capacity for that decision.. Why: There is an actual systems-related medication error and significant unmet need, but dementia alone does not establish incapacity or mandate residential placement.
- carer_support (within_days): Acknowledge Janet's concerns, explain that home support is being strengthened rather than presuming care-home placement, and offer a carer's assessment and dementia support services. Use her agreed presence today only until arrangements are confirmed; do not make her responsible for daily medication or care.. Why: Janet works full-time, visits weekly and feels guilty and anxious.
- advice (same_day): Explain the prescribing error openly with apology. Advise slow staged rising, sitting down immediately if dizzy, regular fluids unless a future clinical reason to restrict, regular meals, supported frame use and avoiding stairs or walking alone while dizzy. Provide a simple written medication/support plan to Edith, Janet and carers, including contact numbers.. Why: Supports informed participation and reduces immediate postural and communication risks.
- follow_up (within_days): Confirm corrected medication packs and safe care cover today; telephone agency/Janet tomorrow to verify implementation. Arrange home review in 48–72 hours for lying/standing BP, dizziness, pulse, blood results, intake and mobility; reassess again within 1–2 weeks after changes, including adherence, eye drops, nutritional measures, falls and adequacy of care.. Why: High immediate risk requires confirmation of actions rather than referral alone.
Discrepancies:
- Hospital stopped furosemide, while GP repeat, pharmacy packs and Edith's account show continued morning use.: Discharge instruction and absent heart failure findings support stopping; physical pack inspection establishes actual exposure. Correct every prescribing/dispensing/MAR source today.
- Edith says she takes all medicines and carers manage them; daughter assumed hospital/pharmacy arrangements guaranteed this.: MAR shows nine missed evenings in fourteen days and five of seven night slots remain full. Treat administration as unreliable, not simply patient non-compliance; revise timing and supervision.
- Edith says she administers her own drops, while daughter assumes carers do so.: Nearly full nine-week-open bottle strongly suggests unreliable use; allocate a named administration responsibility and fresh supply.
- Edith reports independence with washing, dressing, meals and stick mobility; daughter initially describes her as managing well.: Care notes document personal-care help and uneaten meals; daughter reports wet clothes and expired food; observed transfers and gait show impairment. Weekly cheerful appearance does not establish daily functional safety.
- Ambulance impression was mechanical fall with normal sitting BP, whereas hospital recorded postural hypotension.: Cause of unwitnessed fall remains uncertain. Today's reproducible symptomatic orthostatic drop and continued diuretic exposure identify an important ongoing contributor; normal sitting BP and an earlier reassuring ECG do not exclude it.
- Prescribed frame is viewed by Edith as only needed when ill; falls alarm is reportedly owned but cannot be located.: Current observed gait supports frame use now with training, and an inaccessible alarm is not effective protection.
- Commissioned care is two 30-minute calls, while routine records show approximately 12–15 minutes and late evening attendance.: Ask agency to explain and correct duration/timing against assessed need, with social-care review and escalation if necessary.
Follow-up: Same-day confirmation with pharmacy, agency and social care before Janet leaves; next-day implementation check. Home review in 48–72 hours with postural BP, symptoms, blood results and actual care delivery, followed by comprehensive review within 1–2 weeks. Named GP/practice team to track referrals and outstanding actions.
Safety-netting: Call 999 for collapse with incomplete recovery, chest pain, new severe breathlessness, stroke symptoms, serious injury, inability to get up safely after a fall, or head injury with concerning symptoms. Do not attempt to lift Edith unaided. Seek same-day GP/111 advice for further falls or near-faints, persistent dizziness, new confusion, markedly reduced intake/urine, inability to take essential medicines or failed care visits; use emergency assessment if she cannot be kept safe. Sudden visual loss or painful red eye needs urgent same-day eye/emergency assessment. Keep the functioning alarm worn and telephone/contact numbers within reach.
```

### Consultation

` 1` **GP → Janet Price:** Janet, before we discuss the fall, where is your mother now, and is she awake and safe with someone?

` 1` **Janet Price:** She’s at home. I’m ringing from work; the carers still come morning and evening. I couldn’t tell you if she’s awake just now.

` 2` **GP → Janet Price:** Please tell me what you know about this fall, including when it happened and whether she was injured or assessed.

` 2` **Janet Price:** She fell on Saturday night going to the loo and was on the bathroom floor until the carer came in the morning. The paramedics checked her over and left her at home; she had a bruise on her arm. I stayed the weekend and she was up in the night confused about where she was, and had wet the bed.

` 3` _GP reads `ambulance_report`_
> Ambulance service patient report:
> AMBULANCE SERVICE PATIENT REPORT (copy to GP)
> Incident 27 Oct 2026. Call 07:56, on scene 08:41, left scene 09:50. Caller: care worker.
> History: Unwitnessed fall. Found by care worker at the morning call lying on the hallway floor. Patient unable to say when she fell or how long she was on the floor; thinks she "must have slipped".
> Past history: hypertension, Alzheimer's disease, glaucoma. Recent admission after a fall.
> Medication: per blister pack. No anticoagulants.
> Obs: RR 16, SpO2 96% air, HR 78 regular, BP 134/76 sitting, temp 36.5, BM 6.4.
>   GCS 15; unsure of the date, which the carer says is usual for her.
> 12-lead ECG: sinus rhythm 76, no acute changes.
> Secondary survey: no head injury, no neck or hip pain, full range of movement all limbs.
>   Skin intact. Stood with help of one and walked to her chair with a stick.
> Impression: mechanical fall, no injury.
> Disposition: not conveyed. Patient declined hospital; has capacity for this decision.
>   Left in the care of the care worker. Worsening advice given. GP to consider falls referral.
> 14 Nov 2026  Further incident: Fall at night going to the toilet, found on the bathroom floor at the morning call; likely long lie. Obs within normal limits. Bruising right forearm, no head injury. Mechanical fall. Not conveyed; left with carer, GP to review.

` 4` _GP reads `gp_record`_
> GP record:
> Edith MARSH   Female   Age 84   Usual GP: Dr A Okafor
> 
> PROBLEMS - ACTIVE
>   Aug 2024   Alzheimer's disease (memory clinic: mild)
>   Mar 2021   Chronic kidney disease stage 3a
>   Jun 2015   Primary open angle glaucoma
>   Feb 2010   Osteoarthritis of knee
>   Apr 2003   Essential hypertension
> 
> PROBLEMS - PAST / MINOR
>   Nov 2025   Low back pain
>   Jan 2023   Herpes zoster (shingles), thoracic
>   Sep 2022   Seborrhoeic keratosis
>   2020       Benign paroxysmal positional vertigo - resolved after Epley manoeuvre
>   Jul 2019   Urinary tract infection
>   Oct 2017   Osteopenia (DEXA)
>   Mar 2014   Cataract extraction, left eye
>   Nov 2012   Cataract extraction, right eye
>   May 2008   Carpal tunnel syndrome, right
>   1996       Total abdominal hysterectomy (fibroids)
>   1971       Appendicectomy
> 
> REPEAT MEDICATION (last issued 22 Oct 2026)
>   Furosemide 40mg tablets - one each morning - 28 tablets
>   Amlodipine 10mg tablets - one each morning - 28 tablets
>   Donepezil 10mg tablets - one at night - 28 tablets
>   Atorvastatin 20mg tablets - one at night - 28 tablets
>   Adcal-D3 chewable tablets - one twice a day - 56 tablets
>   Latanoprost 50micrograms/ml eye drops - one drop both eyes at night - 2.5ml
>   Paracetamol 500mg tablets - two up to four times a day when required - 100 tablets
> 
> CONSULTATIONS (most recent first)
>   05 Nov 2026  GP (you)        Home visit. Problems: Recurrent unwitnessed falls with persistent
>                                symptomatic orthostatic hypotension: 138/76 lying to 108/64 standing
>                                at 1 minute, with dizziness; multiple contributing factors rather
>                                than a securely established mechanical fall; Medication
>                                reconciliation failure: furosemide stopped in hospital but
>                                subsequently reissued, dispensed and taken; no current clinical
>                                evidence of heart failure; Unreliable evening medication
>                                administration, including donepezil and atorvastatin; uncertain
>                                administration of separately supplied Adcal-D3 and latanoprost;
>                                Unsafe mobility and functional needs exceeding current support:
>                                furniture-walking, difficulty rising, prescribed frame not used,
>                                dependence on carers for personal care despite self-reported
>                                independence; Risk of inadequate nutrition and hydration, functional
>                                urinary incontinence, environmental falls hazards and unavailable
>                                personal alarm; Alzheimer's disease with limited recall and insight,
>                                but demonstrated understanding of the proposed home-support decision
>                                and agreement to a trial; Gradual visual deterioration with glaucoma
>                                and unreliable eye-drop use; opened latanoprost bottle nine weeks
>                                old; Daughter's anxiety and limited capacity to provide regular care.
>                                Plan: Stop furosemide 40 mg immediately, remove from GP repeat
>                                prescribing and contact dispensing pharmacist today to remove it
>                                safely from all current and pending packs and provide corrected packs
>                                before the next dose. Do not ask Edith to identify tablets herself.
>                                Confirm changes in writing to agency, daughter and pharmacy and
>                                obtain acknowledgement; Reduce amlodipine from 10 mg to 5 mg daily
>                                with pharmacist-prepared corrected packs and updated MAR. Review
>                                standing BP and symptoms within 48–72 hours, with further reduction
>                                or withholding if symptomatic hypotension persists; individualise
>                                longer-term BP targets to standing pressure, frailty and falls;
>                                Arrange FBC, U&E, creatinine/eGFR, sodium, potassium and calcium
>                                within 24–48 hours; assess hydration and oral intake today. Arrange
>                                ECG promptly, reviewing rate and conduction in relation to
>                                unexplained falls and donepezil; escalate if concerning symptoms or
>                                findings; Contact agency and adult social care today for urgent
>                                reassessment: move evening call earlier while Edith is awake, provide
>                                sufficient time for personal care, observed medicines and eye drops,
>                                supper and fluids, and add a midday meal/hydration and welfare call.
>                                Reconcile commissioned 30-minute calls with documented 12–15-minute
>                                calls and establish an accountable interim schedule today. Confirm
>                                actual attendance and escalation for declined/missed doses or uneaten
>                                meals; Pharmacist-led review of every medicine and MAR, including
>                                separate Adcal-D3 and PRN paracetamol. Consider moving suitable once-
>                                daily oral medicines to a reliably supervised morning time. Establish
>                                consecutive missed donepezil doses before restarting: if interrupted
>                                for a week or longer, obtain prescribing advice and re-titrate rather
>                                than automatically restarting 10 mg. Avoid double doses. Replace old
>                                latanoprost bottle today, use according to product storage/opening-
>                                expiry instructions and arrange trained carer administration with
>                                documented consent; Urgent community falls/geriatric and
>                                physiotherapy referral for multifactorial falls assessment, gait,
>                                strength, transfers and supervised frame training. Review footwear,
>                                vision, continence, cognition and fracture risk; review osteopenia,
>                                vitamin D/calcium intake and need for osteoporosis
>                                assessment/treatment; Arrange urgent OT home assessment including
>                                stairs, lighting, toilet access, chair height and rails. With consent
>                                remove the loose hallway rug and improve landing lighting today;
>                                unfold and position the frame for accessible supervised use. Locate
>                                or replace and test the pendant alarm, arrange falls-
>                                detection/telecare and safe responder access; assess a commode if
>                                toilet access is unsafe; Arrange measured weight, weight trend and
>                                MUST nutritional assessment through community staff; inspect food
>                                availability/expiry with consent and establish a meal/fluid record.
>                                Assess continence and toileting access rather than diagnosing UTI in
>                                the absence of suggestive symptoms; refer to continence service if
>                                ongoing after diuretic withdrawal and improved access; Arrange
>                                optometrist assessment of acuity and glaucoma control promptly, with
>                                ophthalmology input if indicated, ensuring reliable drops meanwhile;
>                                Document consent and decision-specific capacity for home-support
>                                choices: Edith understands fall risk, benefit of assistance and
>                                expresses a consistent preference to remain home. Raise medication
>                                error as a patient-safety incident and urgently escalate unmet
>                                needs/short visits to agency manager and social care. Consider local
>                                adult safeguarding referral for neglect or self-neglect if essential
>                                care cannot be reliably delivered or investigation identifies
>                                neglect; do not assume daughter is responsible. If safe interim
>                                support cannot be secured today, arrange urgent intermediate care or
>                                hospital assessment, involving Edith and assessing capacity for that
>                                decision; Acknowledge Janet's concerns, explain that home support is
>                                being strengthened rather than presuming care-home placement, and
>                                offer a carer's assessment and dementia support services. Use her
>                                agreed presence today only until arrangements are confirmed; do not
>                                make her responsible for daily medication or care; Explain the
>                                prescribing error openly with apology. Advise slow staged rising,
>                                sitting down immediately if dizzy, regular fluids unless a future
>                                clinical reason to restrict, regular meals, supported frame use and
>                                avoiding stairs or walking alone while dizzy. Provide a simple
>                                written medication/support plan to Edith, Janet and carers, including
>                                contact numbers; Confirm corrected medication packs and safe care
>                                cover today; telephone agency/Janet tomorrow to verify
>                                implementation. Arrange home review in 48–72 hours for lying/standing
>                                BP, dizziness, pulse, blood results, intake and mobility; reassess
>                                again within 1–2 weeks after changes, including adherence, eye drops,
>                                nutritional measures, falls and adequacy of care. Follow-up: Same-day
>                                confirmation with pharmacy, agency and social care before Janet
>                                leaves; next-day implementation check. Home review in 48–72 hours
>                                with postural BP, symptoms, blood results and actual care delivery,
>                                followed by comprehensive review within 1–2 weeks. Named GP/practice
>                                team to track referrals and outstanding actions.
>   22 Oct 2026  Admin           Repeat prescription issued, all repeat items. Pharmacy to blister pack.
>   21 Oct 2026  Document        Hospital discharge summary received (Elderly Care). Filed, awaiting GP review.
>   12 Oct 2026  Document        ED attendance notification: fall at home, admitted.
>   04 Sep 2026  Practice nurse  Seasonal influenza vaccine given. COVID-19 booster given.
>   03 Jul 2026  Telephone       Daughter asking for eye drops on repeat. Already on repeat; advised.
>   18 Apr 2026  GP              Medication review. BP 146/82 sitting. No falls reported. Memory stable per daughter. Continue current medication.
>   10 Feb 2026  Letter          Eye clinic: glaucoma stable on latanoprost. Discharged to optometrist.
>   10 Nov 2025  GP              Low back pain after gardening. No red flags. Paracetamol, activity advice.
>   10 Aug 2025  Letter          Memory clinic review: mild Alzheimer's disease, stable. Continue donepezil. Discharged to GP.
>   14 May 2025  Letter          Letter from adult social care: package of care started, two 30-minute calls daily (morning and evening).
>   09 Apr 2025  Results         eGFR 52, potassium 4.6, HbA1c 39, cholesterol 4.1. Stable.
>   05 Mar 2025  GP              Annual hypertension review. BP 138/78. Continue.

` 5` _GP reads `care_agency_notes`_
> Care agency notes:
> CARE RECORD - Mrs Edith Marsh. Package: 2 calls daily (AM, PM). Medication: prompt from blister pack.
> MAR summary: Evening medicines, last 14 days: given 5, not given 9 (client asleep / declined).
> 
> Tue 17 Nov PM 21:20-21:36 Client muddled, says she wants to go home. Reassured. Medication declined.
> Sat 14 Nov AM 07:55-08:40 Client found on bathroom floor, says she fell in the night. Bruise to right arm. Paramedics attended, client not taken to hospital. Daughter informed.
> Wed 04 Nov AM 08:06-08:20 Assisted with wash and dressing. Prompted medication, taken. Toast and tea. Client in good spirits.
> Wed 04 Nov PM 21:12-21:25 Client in bed, settled. Medication not given, client asleep.
> Tue 03 Nov AM 08:10-08:24 Personal care given. Medication taken. Breakfast made. Chatty this morning.
> Tue 03 Nov PM 21:26-21:38 Client in bed, settled. Medication offered, declined. Door locked.
> Mon 02 Nov AM 07:58-08:13 Personal care given. Medication taken. Cereal and tea. Sandwich made and left in fridge for lunch.
> Mon 02 Nov PM 21:14-21:29 Lunch sandwich still in fridge, client said she wasn't hungry. Supper of tea and biscuits. Client settled for bed.
> Sun 01 Nov AM 08:21-08:35 Personal care given. Medication taken. Daughter visiting today.
> Sun 01 Nov PM 20:52-21:06 Medication given. Client watching TV. All well.
> Sat 31 Oct AM 08:02-08:17 Personal care given. Medication taken. Home clean and tidy.
> Sat 31 Oct PM 21:31-21:44 Client in bed, asleep. Did not wake client. Medication not given.
> Fri 30 Oct AM 08:15-08:29 Personal care given. Medication taken. Client cheerful.
> Fri 30 Oct PM 21:05-21:18 Medication offered, client said she had already taken them. Settled.
> Thu 29 Oct AM 08:04-08:18 Personal care given. Medication taken. Porridge and tea.
> Thu 29 Oct PM 21:22-21:35 Client in bed, settled. Medication not given, client asleep.
> Wed 28 Oct AM 08:12-08:26 Personal care given. Medication taken. Client in good spirits.
> Wed 28 Oct PM 21:09-21:23 Medication offered, declined. Client tired.
> Tue 27 Oct AM 07:48-09:55 On arrival client found on hallway floor, unable to say how long she had been there. Chatty, no obvious injury. 999 called, paramedics attended, client not taken to hospital. Carer stayed until paramedics left. Office informed.
> Tue 27 Oct PM 20:48-21:03 Medication given. Client tired but in good spirits.

` 6` _GP reads `pharmacy_record`_
> Pharmacy record:
> PATIENT MEDICATION RECORD - Edith MARSH
> Monitored dosage system: weekly 7-day blister pack, delivered Mondays.
> Supplied separately: Adcal-D3 chewable tablets, latanoprost eye drops, paracetamol 500mg.
>   16 Nov 2026  Weekly blister pack dispensed, contents unchanged. Morning: furosemide 40mg, amlodipine 10mg. Night: donepezil 10mg, atorvastatin 20mg.
>   09 Nov 2026  Weekly blister pack dispensed, contents unchanged.
>   02 Nov 2026  Weekly blister pack dispensed. Morning: furosemide 40mg, amlodipine 10mg. Night: donepezil 10mg, atorvastatin 20mg.
>   26 Oct 2026  Weekly blister pack dispensed, contents unchanged.
>   22 Oct 2026  Repeat prescription received from GP: furosemide 40mg, amlodipine 10mg,
>              donepezil 10mg, atorvastatin 20mg, Adcal-D3, latanoprost, paracetamol.
>   05 Oct 2026  Weekly blister pack dispensed. Morning: furosemide 40mg, amlodipine 10mg. Night: donepezil 10mg, atorvastatin 20mg.

` 7` **GP → Janet Price:** The records suggest the medication and care changes planned on 5 November have not happened, which is concerning and I am sorry. Has her confusion started suddenly or become worse than her usual memory difficulties?

` 7` **Janet Price:** Yes, it was suddenly worse that night. She was confused about where she was, which isn’t like her. She’s better in the daytime, just a bit muddled.

` 8` **GP → Janet Price:** Has she had any fever, pain or burning when passing urine, new urinary frequency, cough, breathlessness, or other new illness symptoms?

` 8` **Janet Price:** She felt hot on Sunday night. She hasn’t said it hurts or burns when she wees.

` 9` **GP → Janet Price:** When did someone last speak to or see her, and what did they report about her alertness, drinking, passing urine and ability to walk?

` 9` **Janet Price:** I was with her over the weekend. She was more herself in the daytime, just a bit muddled, and she was drinking her tea.

`10` _GP reads `discharge_summary`_
> Hospital discharge summary:
> DISCHARGE SUMMARY - Elderly Care, Ward 9
> Admitted 12 Oct 2026   Discharged 19 Oct 2026
> Presenting complaint: found on the floor at home by carer.
> Diagnosis: Fall at home secondary to postural hypotension.
> Other problems: hypertension; Alzheimer's disease (mild); CKD 3a; glaucoma.
> Investigations: bloods unremarkable apart from eGFR 49 (baseline 52). ECG sinus rhythm,
>   normal intervals. CXR clear. No head injury; CT head not indicated.
> Medication changes: Furosemide 40mg OM STOPPED - no evidence of heart failure, postural drop. GP please update repeats.
> Medication on discharge: amlodipine 10mg OM; donepezil 10mg ON; atorvastatin 20mg ON;
>   Adcal-D3 one BD; latanoprost both eyes ON; paracetamol 1g QDS PRN.
> Therapy: Assessed by physiotherapy. Discharged with a walking frame; advised to use it at all times.
> Social: lives alone; package of care twice daily, restarted on discharge; daughter visits weekly.
> GP actions: please review BP in 2 weeks.

`11` **GP → Janet Price:** This sudden fluctuating confusion could be delirium from an acute illness, dehydration, medicines or injury, not simply worsening Alzheimer's. She needs an urgent face-to-face assessment today and a welfare check now. Can someone with access reach her immediately while we arrange urgent clinical support, without assuming you can leave work?

`11` **Janet Price:** There’s a key safe by the front door. The carers and I have the number, but I don’t know if one of them can get there right now. I’m at work, so I can’t go myself.

`12` **GP → Janet Price:** I will arrange an immediate welfare check through the agency and urgent community team using the key-safe access; if this cannot be achieved promptly, we will escalate to emergency services. Have you noticed any new severe headache, vomiting, one-sided weakness, trouble speaking, severe pain or difficulty bearing weight since the fall?

`12` **Janet Price:** No, I haven’t noticed any of those. She’s got the bruise on her arm, but nothing else that I know of.

`13` **GP → Janet Price:** What worries you most about her managing at home now?

`13` **Janet Price:** I’m worried she’ll fall again or be left confused on her own. I’m frightened you’ll say she needs a home. I want her to stay at home, with more help if that’s what it takes.

`14` **GP → Janet Price:** We will aim to support her at home if it can be made safe; a care home is not an automatic consequence of dementia or a fall. First we must assess and treat this new confusion and arrange reliable support, including overnight safety. Has your mother expressed what help she would accept now?

`14` **Janet Price:** She wants to stay in her own home. She’d accept more help if that’s what it takes to make it safe.

`15` **GP → Janet Price:** Do you know whether anyone changed her blister packs, checked her blood pressure or took blood tests after my visit two weeks ago?

`15` **Janet Price:** I haven’t heard anything about blood pressure checks or blood tests. I thought the hospital had sorted her tablets and the chemist does the pods, but I don’t know if the packs were changed.

`16` **GP → Janet Price:** I will take responsibility for chasing the assessment, medication corrections and care arrangements today, and update you today. Please do not change tablets yourself or feel you must provide overnight care. If you or a carer find her difficult to wake, collapsed, severely breathless, with stroke symptoms or unable to stand after injury, call 999. New confusion still needs assessment today even if she seems better in daylight; we should not assume a urine infection or start antibiotics without assessing her.

`16` **Janet Price:** All right. Please make sure someone checks her promptly and lets me know what they find. I’ll keep my phone with me at work.

`17` _GP submits plan_

### Plan

**Problems**
- Suspected acute delirium superimposed on Alzheimer's disease: abrupt new nocturnal disorientation, fluctuating daytime improvement and reported fever after recent fall; current condition unknown by telephone.
- Recurrent unwitnessed nocturnal falls, latest 14 November with probable prolonged lie and right forearm bruising; cause not established despite ambulance mechanical-fall label.
- Ongoing probable medication-related orthostatic hypotension: pharmacy still supplying furosemide 40 mg and amlodipine 10 mg despite 5 November stop/reduction plan.
- Unsafe gaps in care and persistent unreliable evening medication administration; previous care and monitoring plan has no documented implementation.
- Functional urinary incontinence and new bedwetting, with possible acute illness but insufficient evidence to diagnose UTI.
- CKD3a with risks of dehydration, AKI, electrolyte disturbance and complications of prolonged immobilisation.
- Daughter concerned about safety and institutional care, unable to provide immediate or daily supervision.

**Function and ADLs:** Lives alone in a two-storey home with only twice-daily care. Previously observed impaired transfers, furniture-walking and unsafe turning, requiring personal-care assistance and supervised medicines/meals. Latest fall occurred on a night-time toilet journey with an overnight lie. New fluctuating confusion increases dependence; present alertness, mobility, intake and safety cannot be established by telephone. Daughter works and cannot attend now; key-safe access exists. Edith reportedly wants to remain home and accepts additional help, requiring direct confirmation and decision-specific capacity assessment.

**Risks**
- Unrecognised infection/sepsis, dehydration, metabolic disturbance, injury or other acute illness causing delirium.
- Further fall, syncope, fracture or prolonged lie while alone, especially overnight.
- AKI/electrolyte disturbance and possible rhabdomyolysis after prolonged lie with CKD and ongoing diuretic exposure.
- Medication harm from continued incorrect packs, missed doses or inappropriate donepezil restart.
- Neglect or unmet essential needs from failed implementation of agreed care and clinical follow-up.
- Carer distress and unsustainable reliance on daughter.

**Actions**

| Type | Detail | Rationale | Urgency |
|---|---|---|---|
| other | Practice to contact agency manager immediately for an urgent in-person welfare check using authorised key-safe access and obtain direct report of alertness, breathing, mobility, intake and urine output. Arrange urgent same-day GP home visit/urgent community response assessment in parallel, not a routine telephone review. If immediate safety cannot be established promptly or concerning findings arise, contact ambulance services and communicate access arrangements; do not leave her unassessed awaiting the next routine care call. | Current condition is unknown, she lives alone and has new fluctuating confusion with possible fever following a long-lie fall. | same_day |
| investigation | At urgent face-to-face assessment obtain full observations including temperature, pulse, BP, respiratory rate, oxygen saturation, glucose, hydration and consciousness; assess delirium with 4AT and collateral baseline/history. Examine neurological status, head/injury signs, forearm, hips, gait/weight-bearing if safe, chest, abdomen, skin/pressure areas, pain, constipation and urinary retention. Check lying/standing BP only when safe. Determine head strike/LOC and investigate or transfer for head injury/fracture if indicated. Transfer urgently if unstable, sepsis suspected, major injury, marked dehydration or assessment/treatment cannot safely be delivered at home. | Telephone information and normal ambulance observations five days ago cannot exclude current acute illness, occult injury or delirium. | same_day |
| investigation | Arrange same-day FBC, U&E/creatinine/eGFR, sodium, potassium, calcium, glucose and inflammatory markers as clinically indicated; add CK given probable long lie, especially with muscle pain, weakness or dark/reduced urine. Obtain ECG for unexplained falls/rate/conduction and donepezil exposure. Investigate infection according to clinical findings; obtain urine culture if clinical suspicion of urinary infection, not dipstick-based diagnosis in this older adult. Do not prescribe antibiotics solely for confusion, bedwetting or asymptomatic bacteriuria. | Possible fever and delirium require a cause search; CKD, continued diuretic and long lie increase renal and metabolic risks. | same_day |
| medication_change | Immediately contact pharmacist and agency to verify actual administration and remove furosemide 40 mg from all current/pending packs and GP repeats, confirming hospital stop instruction. Implement amlodipine reduction to 5 mg with corrected pharmacy packs/MAR; same-day clinician may withhold further antihypertensive doses if acute hypotension/dehydration warrants. Confirm whether today's doses were taken and prevent any further incorrect dose. Do not ask Edith or Janet to identify or remove tablets. Send written changes and obtain acknowledgement from pharmacy and agency. | 9 and 16 November dispensing documents unchanged harmful regimen despite explicit prior instructions, with persistent high falls risk and no heart failure indication. | same_day |
| medication_change | Reconcile every medicine against physical packs and current MAR at the home assessment, including consecutive missed donepezil doses, pulse/ECG, Adcal-D3, PRN analgesia and latanoprost. Avoid doubling or automatically restarting donepezil 10 mg after a week or more off; obtain prescriber/pharmacist advice on re-titration. Review suitability of supervised morning dosing for once-daily medicines. Confirm fresh in-date eye drops and named trained administration responsibility. | Late evening visits and documented refusals/omissions continue; prescribing lists alone do not establish exposure. | same_day |
| care_package_change | Urgently convene agency manager, adult social care and urgent community response to secure sufficient supervised care today, including overnight cover while delirium is assessed, earlier adequate-length evening visits, midday meals/fluids, personal care and observed medication/drop administration. Confirm actual attendance and escalation procedures. If adequate supervision and clinical treatment cannot be secured, arrange urgent intermediate care or hospital assessment rather than leaving Edith alone. Do not rely on Janet to fill gaps. | Two brief daily calls have failed to prevent an overnight long lie, missed medicines and unmet nutrition and toileting needs. | same_day |
| safeguarding | Raise an urgent adult safeguarding concern regarding persistent unmet essential care and repeated medication-system failures with actual further harm. Escalate to agency commissioner/manager and practice clinical governance, trace why 5 November actions and planned reviews were not completed, and report medication/patient-safety incidents. Explain known facts openly with apology, avoid assigning unverified blame, and name a practice clinician accountable for closing each action. | Documented unchanged dispensing and ongoing late short calls after a prior comprehensive safety plan suggest unresolved systems failures and possible neglect. | same_day |
| other | Speak directly with Edith at the urgent assessment, explain options in accessible terms, establish consent and decision-specific capacity for assessment, treatment and immediate support/accommodation. Optimise communication and consider fluctuating delirium. If she lacks capacity, use least-restrictive best-interests decisions with Janet and relevant professionals; confirm any health/welfare LPA rather than assuming daughter can consent. Do not assume dementia means incapacity or mandate permanent placement. | Prior capacity assessment cannot establish capacity during a new acute confusional episode; her preference is to remain home if safe. | same_day |
| equipment | Urgent OT/falls team review of night-time toilet route, bedside commode, lighting, rails, appropriate frame and supervised transfers. Locate/replace and test wearable alarm and consider automatic falls detection with responder access, recognising it cannot replace supervision during delirium. Avoid unsupported stairs/toileting while unsafe. | Recent bathroom fall and prolonged lie demonstrate an unmet night-time mobility and rescue need. | same_day |
| referral | Confirm and expedite outstanding falls/geriatric, physiotherapy and OT referrals, nutritional assessment and optometry follow-up; address continence after acute causes and toileting access are assessed. Review weight, meals/fluids, fracture risk and longer-term support after acute recovery. | Multiple established modifiable contributors persist and referral completion is unverified. | within_days |
| carer_support | Acknowledge Janet's anxiety, explain that temporary hospital/intermediate care if necessary is not a decision for permanent residential care, and aim for Edith's preferred home setting when safe. Offer carer's assessment and dementia support; record Janet's limited availability and agreed role as contact, not substitute carer. | Daughter wants safe home support but cannot provide immediate, daily or overnight care. | same_day |
| follow_up | Named GP/practice coordinator to confirm welfare-check outcome, clinician attendance, disposition, corrected packs and supervision today and telephone Janet with an update. Review results the same day and reassess within 24 hours if at home; arrange further home review within 48–72 hours with postural BP, pulse, cognition, renal function, intake and mobility, then comprehensive review in 1–2 weeks. | Previous intended actions were not verified; closed-loop follow-up is essential. | same_day |

**Discrepancies**
- Ambulance describes the 14 November fall as mechanical with normal observations, whereas she had a probable long lie, known orthostatic hypotension and subsequent fluctuating confusion. → Treat mechanism as uncertain and ambulance findings as time-limited reassurance only; urgent reassessment for acute illness, injury and medication effects.
- 5 November plan stopped furosemide and reduced amlodipine, but GP repeats remain old and pharmacy dispensed unchanged packs on 9 and 16 November. → Assume continued exposure is possible until actual packs/MAR verified; urgently correct all prescribing, dispensing and administration sources with acknowledgement.
- Previous plan requested enhanced earlier care and monitoring; current notes still show twice-daily visits including 21:20 attendance and no documented blood tests or BP review. → Do not infer implementation from a written plan. Verify directly and escalate failures with agency, social care and practice team.
- Alzheimer's is labelled mild and daytime functioning appears better, but daughter describes abrupt unfamiliar disorientation and agency notes new desire to go home while at home. → Acute fluctuating change suggests possible delirium superimposed on dementia, not established progression or benign sundowning.
- Bedwetting and feeling hot could suggest infection, but no dysuria is reported and current clinical status is unknown. → Assess for urinary and non-urinary causes, including functional incontinence, medicines and retention; do not label or treat UTI from confusion alone.

**Follow-up:** Immediate closed-loop welfare check and same-day face-to-face medical assessment. Named practice clinician confirms safe disposition, actual support and medication correction today and updates Janet on her mobile. Review investigations today; reassess within 24 hours if remaining home and again within 48–72 hours, with longer-term multidisciplinary review after acute recovery.

**Safety-netting:** Agency/relative to call 999 if Edith is difficult to wake, collapses, has severe breathing difficulty, chest pain, stroke symptoms, serious/head injury symptoms, cannot bear weight after injury or is found fallen and cannot get up safely; do not lift unaided. Acute confusion with fever, reduced intake/urine, worsening weakness or failed essential care requires same-day urgent assessment, not waiting for routine review. If she cannot be contacted or immediate safety cannot be established, escalate urgently through emergency services. No unattended home management unless reliable interim supervision and clinical follow-up are confirmed.
