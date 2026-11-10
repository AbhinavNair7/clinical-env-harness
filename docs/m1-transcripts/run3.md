# edith_marsh, visit 1

- **Clinician:** openai/gpt-6.1-sol
- **Simulators:** patient openai/gpt-6-luna, carer openai/gpt-6-luna
- **Checker:** openai/gpt-6-luna
- **Inspect log:** logs/ (local, not committed)
- **Tokens (all epochs):** clinician: 247281 in (242725 cached) / 7178 out; patient: 2111 in (0 cached) / 2036 out; checker: 11280 in (0 cached) / 5830 out; carer: 4844 in (0 cached) / 3133 out
- **Turns:** 33 used of a 40-turn budget (hard cap 80); ended by plan
- **Checker:** 2 flagged drafts, 2 regenerated; 14 interjection calls stayed silent

## What the GP was told

```text
Visit 1: home visit, Thursday 5 November 2026.
Patient: Edith Marsh, 84. Lives alone in a two-storey terraced house. Mild Alzheimer's disease, hypertension. Admitted 3 weeks ago after a fall with a postural drop in blood pressure. Care agency visits twice daily; her daughter visits on Sundays.
Present: Edith Marsh (patient), Janet Price (daughter).
Reason for this visit: The care agency phoned the practice: Edith was found on the floor last week and is missing evening medicines. Janet is there for the visit.
Records you can read: GP record (gp_record), Hospital discharge summary (discharge_summary), Care agency notes (care_agency_notes), Pharmacy record (pharmacy_record), Ambulance service patient report (ambulance_report).
```

## Consultation

` 1` **GP → Edith Marsh:** Hello Edith, I'm your GP. Is it all right if Janet stays while we talk about how things have been at home?

` 1` **Edith Marsh:** Oh yes, that's quite all right, love. Janet can stay.

` 2` **GP → Edith Marsh:** How have you been feeling since you came home from hospital?

` 2` **Edith Marsh:** Oh, not too bad, thank you, love. It’s nice to be home again. I’m getting on all right.

` 3` _GP reads `discharge_summary`_
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

` 5` **GP → Edith Marsh:** The carers said you were found on the floor last week. Can you tell me what happened?

` 5` **Edith Marsh:** I haven’t had any falls, love. Well, only the one before the hospital. I don’t remember much about it, really.

` 5` **Janet Price (adds):** She had that one fall before the hospital. Nothing since, as far as I know.

` 6` _GP reads `care_agency_notes`_
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
> Tue 27 Oct AM 07:48-09:55 On arrival client found on hallway floor, unable to say how long she had been there. Chatty, no obvious injury. 999 called, paramedics attended, client not taken to hospital. Carer stayed until paramedics left. Office and daughter informed.
> Tue 27 Oct PM 20:48-21:03 Medication given. Client tired but in good spirits.

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

` 8` _GP reads `pharmacy_record`_
> Pharmacy record:
> PATIENT MEDICATION RECORD - Edith MARSH
> Monitored dosage system: weekly 7-day blister pack, delivered Mondays.
> Supplied separately: Adcal-D3 chewable tablets, latanoprost eye drops, paracetamol 500mg.
>   02 Nov 2026  Weekly blister pack dispensed. Morning: furosemide 40mg, amlodipine 10mg. Night: donepezil 10mg, atorvastatin 20mg.
>   26 Oct 2026  Weekly blister pack dispensed, contents unchanged.
>   22 Oct 2026  Repeat prescription received from GP: furosemide 40mg, amlodipine 10mg,
>              donepezil 10mg, atorvastatin 20mg, Adcal-D3, latanoprost, paracetamol.
>   05 Oct 2026  Weekly blister pack dispensed. Morning: furosemide 40mg, amlodipine 10mg. Night: donepezil 10mg, atorvastatin 20mg.

` 9` **GP → Edith Marsh:** Have you had any dizziness when getting up, faint feelings, pain, or other new symptoms recently?

` 9` **Edith Marsh:** I do come over a bit giddy when I stand up, mostly in the mornings, love. Nothing else much.

`10` _GP examines: Full observations including pulse rhythm, temperature, oxygen saturation, respiratory rate, hydration and lying blood pressure followed by standing blood pressure at 1 and 3 minutes with symptoms_ → Please name one specific examination.

`11` _GP examines: Lying and standing blood pressure_ → Lying 138/76; standing 108/64 at 1 minute and 112/66 at 3 minutes; dizzy on standing. [x_postural_bp]

`12` **GP → Janet Price:** The dated care and ambulance records confirm another fall on 27 October, although Edith does not remember it. What have you noticed about her mobility and managing at home since discharge?

`12` **Janet Price:** She seems fine to me—always tidy and cheerful when I come round. Though last Sunday she grabbed the table getting up from her chair. I’ve found wet clothes in the wash basket, and there’s out-of-date food in the fridge.

`13` **GP → Edith Marsh:** Could you talk me through how you manage washing, dressing, meals and going to the toilet during the day?

`13` **Edith Marsh:** Oh, I manage all right, love. I do all my own meals, always have. I see to my washing and dressing too. I get on fine during the day.

`14` **GP → Janet Price:** What help does Edith actually need with washing, dressing, meals and toileting, including between care visits?

`14` **Janet Price:** The carers come morning and evening. They do her tablets and help her wash, I think. I couldn’t say about the rest between visits.

`14` **Edith Marsh (adds):** I do my own washing and dressing, love. The girls are there for company, really.

`15` _GP examines: Observed mobility and transfers, including chair rise and walking with her usual aid_ → Rises from the chair at the second attempt, pushing up with her arms. Walks slowly with a stick, reaching for furniture; unsteady on turning. Does not use the walking frame. [x_gait]

`16` **GP → Edith Marsh:** What makes it difficult to use the walking frame the hospital gave you?

`16` **Edith Marsh:** Oh, it’s not difficult, love. The frame’s for when I’m poorly. I manage with my stick.

`17` _GP examines: Home environment for falls hazards, including stairs, toilet access and location of walking frame_ → Loose rug in the hallway; dim landing light; walking frame folded by the front door. [x_home]

`18` _GP examines: Current medicines in the home including blister packs and separately supplied medicines_ → Morning slots hold furosemide 40 mg and amlodipine 10 mg; night slots hold donepezil 10 mg and atorvastatin 20 mg. Five of last week's seven night slots are still full. [x_dosette]

`19` **GP → Edith Marsh:** Your water tablet, furosemide, was stopped in hospital but is still in your packs. Your blood pressure drops when you stand, which can cause dizziness and falls. I recommend stopping that tablet and having the pharmacy replace the packs today. How does that sound?

`19` **Edith Marsh:** Oh, I see, love. I still have my water tablet every morning, and I’m up and down to the toilet after. If you think I ought to stop it, I suppose you’d better tell the girls what to do.

`19` **Janet Price (adds):** I thought the hospital had sorted her tablets out, and the chemist puts them in the pods.

`20` **GP → Edith Marsh:** The evening carers often come after you're asleep. What time would suit you better for help with supper and your medicines?

`20` **Edith Marsh:** Oh, I’m usually in bed by half eight, love, and often asleep by the time the night girl comes. I’m not sure what time would suit better.

`20` **Janet Price (adds):** She’s always been an early bird, in bed by half eight or nine at the latest.

`21` **GP → Edith Marsh:** How are you getting food and drinks at lunchtime when you are on your own?

`21` **Edith Marsh:** Oh, I do all my own meals, love. I’ve always managed that.

`22` _GP examines: Nutritional and hydration status_ → Thin; her cardigan and skirt hang loose. Food marks on her clothes, hair unwashed. Alert, chatty and pleasant. Lips a little dry. [x_general]

`23` **GP → Edith Marsh:** Is your toilet upstairs, and do you have any trouble getting there in time?

`23` **Edith Marsh:** Yes, love, it’s upstairs. I’m all right getting there, though I have the odd little accident if I can’t get there in time. I don’t like to make a fuss about it.

`24` **GP → Edith Marsh:** If you fell while alone and couldn't get up, how would you call for help?

`24` **Edith Marsh:** Oh, I’ve got one of those buttons somewhere, love. I can’t think where I’ve put it.

`25` _GP examines: Cardiovascular examination including pulse rate and rhythm and signs of heart failure_ → Heart sounds normal, chest clear, no ankle oedema, JVP not raised. [x_cardio]

`26` **GP → Janet Price:** Have you noticed any sudden change in Edith's confusion or health, rather than her usual memory difficulties?

`26` **Janet Price:** I couldn’t really say, doctor. I’m not with her every day.
> ⚑ checker, draft 1: **invented_fact**: Claims there has been no sudden change in Edith’s confusion or health, which is not established in the script.
> rejected draft 1: _No sudden change that I’ve noticed. Her memory’s worse than last year, but she’s still Mum—she covers it well._

`27` **GP → Janet Price:** How are you coping, and what help can you realistically provide while we arrange more support?

`27` **Janet Price:** I work full time, so I can only come on Sundays. I’m frightened you’ll say she needs a home, and I do feel guilty I’m not here more. I want Mum to stay at home, with more help if that’s what it takes.

`27` **Edith Marsh (stays silent after a rejected draft)**
> ⚑ checker, draft 1: **hidden_revealed**: Edith states her preference about staying at home, but the GP has not asked about her wishes or whether she wants to move into a home.
> rejected draft 1: _I want to stay in my own home, love. I don’t want to go into a home._

`28` **GP → Edith Marsh:** I'd like to help you stay safely at home with an earlier evening visit, a lunchtime visit for food and drinks, and help with washing and medicines. A therapist could also help with your frame and stairs. Would you like us to arrange that?

`28` **Edith Marsh:** Oh, yes, love, if that helps me stay here. I’d rather not go into a home. I do manage all right, but it’d be nice if the girls weren’t always rushing.

`29` **GP → Edith Marsh:** So I can check I've explained clearly, can you tell me why I'm suggesting more help and what might happen without it?

`29` **Edith Marsh:** Oh, I’m not quite sure, love. You think a bit more help would make things safer for me here, so I can stay in my own home.

`30` **GP → Edith Marsh:** Yes. I'm worried about another fall, lying alone without help, and missed meals and tablets. What do you think about those risks and accepting help to reduce them?

`30` **Edith Marsh:** Oh, I don’t want to fall again, love, or miss my meals. If a bit more help makes it safer for me to stay here, then I’m happy to accept it.

`31` _GP examines: Focused neurological examination_ → Unremarkable.

`32` **GP → Janet Price:** Staying at home is our aim too; this doesn't automatically mean a care home. I will urgently contact the agency and social care about longer visits, lunchtime support and earlier evening care, and arrange the pharmacy correction today. You aren't expected to replace paid care. If adequate support can't be provided today, we will need an urgent temporary care arrangement so Edith is not left unsafe.

`32` **Janet Price:** All right, doctor. I want Mum kept at home if you can make it safe, with more help. Please let me know what happens today—I'm not able to provide the extra care myself.

`32` **Edith Marsh (adds):** Oh, I do want to stay in my own home, love. Thank you for trying to arrange the help.

`33` _GP submits plan_

## Plan

**Problems**
- Recurrent falls: confirmed unwitnessed fall on 27 October after admission for a previous fall; possible prolonged time on floor, no injury identified then.
- Symptomatic postural hypotension: BP 138/76 lying to 108/64 standing, with dizziness; likely contributed to by inadvertent continued furosemide and possible inadequate intake.
- Medication reconciliation failure: hospital-stopped furosemide remains on GP repeat and in current blister packs.
- Evening medication omissions due to late visits, sleep and refusal; separately supplied medicines also need checking.
- Impaired mobility and transfers, furniture walking and non-use of prescribed frame; stairs to toilet and environmental hazards.
- Unmet personal care, nutrition, hydration and toileting needs despite reported independence; possible weight loss and functional incontinence.
- Alzheimer's disease with impaired recall and limited insight; assess decision-specific capacity where needed, not presume incapacity.
- Daughter available weekly only; current twice-daily care package insufficient.

**Function and ADLs:** Needs help with washing, dressing, medication and meals according to care records and observed presentation. Rises only at second attempt using arms; slow with stick, furniture walks and unsteady turning. Frame remains folded at front door. Upstairs toilet, urinary accidents, missed lunches and poor grooming indicate unmet needs between visits. Lives alone with daughter attending Sundays; wishes to remain at home and accepts increased support after explanation.

**Risks**
- Further falls, syncope, injury and prolonged unattended time on floor; alarm currently unlocated.
- Dehydration, acute kidney injury and electrolyte disturbance with CKD3a, diuretic use and poor intake.
- Medication harm and omitted donepezil, atorvastatin and potentially eye drops or calcium/vitamin D.
- Malnutrition, self-neglect and unmet care needs.
- Unsafe stairs and rushing to toilet after diuretic; loose rug and poor lighting.
- Carer strain and unsafe reliance on daughter's unavailable weekday support.

**Actions**

| Type | Detail | Rationale | Urgency |
|---|---|---|---|
| medication_change | Stop furosemide 40 mg immediately; remove from GP repeat list and document the reconciliation error. Contact pharmacy and care agency today for professionally corrected/replacement blister packs before the next morning dose, with explicit written medication instructions and confirmation received. Do not ask Edith to identify and remove tablets herself; recall obsolete packs safely. | Hospital explicitly stopped furosemide, no clinical evidence of heart failure, and symptomatic postural hypotension has recurred while it continued. | same_day |
| medication_change | Review amlodipine 10 mg in light of symptomatic standing BP; initially stop the erroneous diuretic and reassess within 48 hours, reducing amlodipine to 5 mg if low standing pressure or dizziness persists, sooner if worsening. Base ongoing BP treatment on standing readings and frailty rather than tight seated targets. | Avoid ongoing antihypertensive-related falls while monitoring response to correction of the clear prescribing error. | within_days |
| other | Complete reconciled medication list including separately supplied Adcal-D3, latanoprost and PRN paracetamol; establish actual administration with carers and pharmacy. Arrange supervised administration and MAR recording rather than prompts alone if needed. Discuss moving donepezil and atorvastatin to a reliably attended earlier time with pharmacist, preserving appropriate dosing intervals and separate Adcal doses; do not double missed doses. Review ongoing benefit and adverse effects of medicines, including donepezil-related bradycardia/syncope. | Night slots remain full and current visits occur after bedtime; blister packs alone do not ensure adherence or cover eye drops. | same_day |
| investigation | Arrange home bloods for U&E, creatinine/eGFR, FBC and calcium; check pulse/rhythm and obtain ECG in assessment of recurrent unexplained falls and donepezil use. Compare renal results with baseline and act promptly on abnormalities. | CKD, diuretic exposure, possible dehydration and unwitnessed falls require reversible causes to be assessed; previous normal ECG does not exclude current problems. | within_days |
| care_package_change | Contact agency manager and adult social care today for urgent needs reassessment: morning personal care, supervised medicines and breakfast; add lunchtime meal preparation and observed food/fluid intake; move evening call before usual 20:30 bedtime for supper, medicines and toileting. Ensure commissioned 30-minute calls provide sufficient time, noting routine recorded visits are approximately 12–15 minutes. Obtain named responsibility, implementation times and same-day confirmation. | Current visits miss meals and most evening medication, with evidence of poor hygiene and inability to meet needs independently. | same_day |
| other | Agree a same-day interim safety plan with Edith, agency and social care, including an additional welfare/meal visit and reliable medication supervision. Do not rely on Janet to cover weekdays. If adequate support cannot be secured or Edith cannot safely transfer, eat, drink or toilet, arrange urgent community crisis/intermediate care or temporary supported placement; hospital assessment if acute illness or immediate medical danger emerges. | Referrals alone do not protect her while awaiting services. | same_day |
| referral | Urgent community falls team/physiotherapy and occupational therapy home assessment for strength, balance, transfers, frame fitting and training, stairs, toileting and practical ADL needs. Assess vision, footwear, continence and bone health/fracture risk as part of comprehensive falls review. | Recurrent falls with observed unsafe gait and non-use of prescribed aid require multifactorial intervention. | within_days |
| equipment | With consent, remove/secure hallway rug, improve landing lighting, unfold and position frame for safe use with instruction. Locate, test and encourage wearing personal alarm; replace urgently if unavailable. OT to assess commode, rails and safe downstairs arrangements rather than unsupervised stair use or unsafe frame use on stairs. | Identified hazards, upstairs toilet and inaccessible alarm increase falls and long-lie risk. | same_day |
| investigation | Measure weight, BMI and nutritional screening score and seek previous weight; start food/fluid monitoring with carers and assess swallowing/dental difficulties if intake poor. Arrange dietitian input if malnutrition risk, and regular assisted meals, snacks and fluids unless a clinical contraindication emerges. | Loose clothing, thin appearance, uneaten lunches and dry lips suggest nutritional and hydration needs not met by meal preparation alone. | within_days |
| safeguarding | Raise same-day adult safeguarding concern/advice request regarding unmet care needs, possible neglect/self-neglect and medication-system failure, explaining this supportively to Edith and Janet. Seek agency incident review and practice medication-safety review of unprocessed discharge changes; establish whether commissioned support was delivered. Record findings without attributing blame prematurely. | A cognitively impaired adult with care needs has recurrent falls, missed medicines and evidence of inadequate care, and may be unable to protect herself. | same_day |
| carer_support | Offer Janet a carer's assessment and information on dementia/carer support; nominate a practice contact and update her today with Edith's permission about arrangements, without making her the default care provider. | Janet works full time, can attend only Sundays and expresses guilt and worry. | same_day |
| advice | Support Edith's expressed wish to remain at home. Use clear, repeated explanations and decision-specific capacity assessment if decisions become contested or riskier; document ability to understand, retain, use/weigh and communicate for the relevant decision. Her agreement after explanation supports increased care; dementia and poor recall alone do not establish incapacity. If capacity lacking, use least-restrictive best-interests processes with Janet and relevant professionals. | Respect autonomy while addressing reduced insight and risks. | same_day |
| follow_up | Named GP to confirm medication correction and safe care arrangements today, review symptoms, intake, pulse and lying/standing BP at home within 48 hours, and review blood results promptly. Reassess falls, weight, personal care, MAR adherence and success of the revised package within one week with agency and Janet. | High short-term risk and multiple service dependencies require active closed-loop follow-up. | same_day |

**Discrepancies**
- Edith and Janet recall only the pre-admission fall; agency and ambulance records document a second fall on 27 October. → Accept contemporaneous agency and ambulance documentation as confirmation of recurrent falls; explain sensitively that memory may be incomplete and that mechanism remains uncertain, despite ambulance label of mechanical fall.
- Hospital stopped furosemide, but GP repeat, pharmacy record and actual blister packs continue it. → Discharge instruction plus current symptomatic postural drop and absence of heart failure support immediate cessation and correction of all prescribing/dispensing records.
- Edith reports independent meals and personal care; daughter initially describes her as fine. → Care notes document assistance, untouched lunch and short visits; examination shows poor grooming, loose clothing and unsafe mobility. Use observed function and triangulated records to establish support needs, while respecting Edith's preferences.
- Twice-daily visits and blister packing imply medication support, but evening MAR records 9 of 14 doses not given and most recent night slots remain full. → Support is not effective at the current late visit times. Earlier adequately long visits, administration review and MAR monitoring required; separately supplied medicines need explicit oversight.
- Hospital advised frame use at all times; Edith regards it as only for illness and walks with a stick. → Observed instability supports frame reassessment, education and supervised practice rather than accepting reported safe mobility.

**Follow-up:** Practice retains responsibility for same-day confirmation that agency, pharmacy and social care have received and acted on the plan; contact Janet with Edith's agreement. Home clinical review within 48 hours with postural BP, pulse, hydration and laboratory results; multidisciplinary/function and medication-adherence review within one week. Escalate today if interim care cannot keep her safe.

**Safety-netting:** Explain directly to Edith, Janet and carers: call 999 for collapse, serious injury, head injury with concerning symptoms, new weakness/speech disturbance, chest pain, severe breathlessness, or a fall with inability to get up or suspected prolonged time on the floor; do not attempt an unsafe lift. Seek same-day GP/111 assessment for increasing dizziness, further falls, new confusion, poor fluid intake, reduced urine, fever or inability to take medicines. Rise slowly, sit immediately if dizzy, use the assessed walking aid and seek help with transfers/stairs. Ensure accessible working alarm/phone and an agreed carer response and access plan. Do not double omitted doses.
