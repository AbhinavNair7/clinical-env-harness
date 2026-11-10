# edith_marsh

- **Clinician:** openai/gpt-6.1-sol
- **Simulators:** patient openai/gpt-6-luna, carer openai/gpt-6-luna
- **Checker:** openai/gpt-6-luna
- **Inspect log:** logs/2026-11-04T15-53-36-00-00_case_27ZnpXQLmHL4aNyKLAfD5Z.eval
- **Tokens (all epochs):** clinician: 438367 in (433682 cached) / 14118 out; patient: 40044 in (39936 cached) / 2057 out; checker: 13339 in (0 cached) / 12962 out; carer: 87772 in (87598 cached) / 4864 out
- **Clinician memory:** notes

## Visit 1, home visit, Thursday 5 November 2026

- **Turns:** 33 used of a 40-turn budget (hard cap 80); ended by plan
- **Checker:** 3 flagged drafts, 2 regenerated; 10 interjection calls stayed silent

### What the GP was told

```text
Visit 1: home visit, Thursday 5 November 2026.
Patient: Edith Marsh, 84. Lives alone in a two-storey terraced house. Mild Alzheimer's disease, hypertension. Admitted in October after a fall with a postural drop in blood pressure. Care agency visits twice daily; her daughter visits on Sundays.
Present: Edith Marsh (patient), Janet Price (daughter).
Reason for this visit: The care agency phoned the practice: Edith was found on the floor last week and is missing evening medicines. Janet is there for the visit.
Records you can read: GP record (gp_record), Hospital discharge summary (discharge_summary), Care agency notes (care_agency_notes), Pharmacy record (pharmacy_record), Ambulance service patient report (ambulance_report).
```

### Consultation

` 1` **GP → Edith Marsh:** Hello Edith, I'm your GP. Is it all right if Janet stays while we talk, and could you tell me what has been troubling you recently?

` 1` **Edith Marsh:** Oh, yes, Janet can stay, love. I’m not sure there’s much troubling me, really. I’m getting on all right at home. My eyes aren’t what they were, though—I’ve got drops for them. I like my quiz shows in the afternoon; I’m not bad at them, you know.

` 2` _GP reads `gp_record`_
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

` 4` _GP reads `care_agency_notes`_
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

` 5` _GP reads `pharmacy_record`_
> Pharmacy record:
> PATIENT MEDICATION RECORD - Edith MARSH
> Monitored dosage system: weekly 7-day blister pack, delivered Mondays.
> Supplied separately: Adcal-D3 chewable tablets, latanoprost eye drops, paracetamol 500mg.
>   02 Nov 2026  Weekly blister pack dispensed. Morning: furosemide 40mg, amlodipine 10mg. Night: donepezil 10mg, atorvastatin 20mg.
>   26 Oct 2026  Weekly blister pack dispensed, contents unchanged.
>   22 Oct 2026  Repeat prescription received from GP: furosemide 40mg, amlodipine 10mg,
>              donepezil 10mg, atorvastatin 20mg, Adcal-D3, latanoprost, paracetamol.
>   05 Oct 2026  Weekly blister pack dispensed. Morning: furosemide 40mg, amlodipine 10mg. Night: donepezil 10mg, atorvastatin 20mg.

` 6` _GP reads `ambulance_report`_
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

` 7` **GP → Edith Marsh:** The carers found you on the floor last week. Can you tell me what you remember happening?

` 7` **Edith Marsh:** Oh, I don’t remember much about that, love. I haven’t had any falls—well, only the one before the hospital.

` 7` **Janet Price (adds):** Another fall? Nobody told me. Why didn’t the agency ring me? Is she all right—did she hurt herself?

` 8` **GP → Edith Marsh:** The ambulance crew checked you on 27 October and found no injury, but I will check you again today. Have you had any dizziness, blackouts, pain or other new symptoms since coming home?

` 8` **Edith Marsh:** I do get a bit giddy when I stand up, mostly in the mornings, but it passes if I sit down again. I haven’t blacked out, no.

` 9` _GP examines: General appearance, hydration, temperature, pulse/rhythm, oxygen saturation, lying and standing blood pressure at 1 and 3 minutes, with assistance and symptom monitoring_ → Please name one specific examination.

`10` _GP examines: Lying and standing blood pressure with symptoms_ → Lying 138/76, pulse 76 regular; standing 108/64, pulse 82 at 1 minute and 112/66, pulse 80 at 3 minutes; dizzy on standing. [x_postural_bp]

`11` **GP → Janet Price:** Edith's blood pressure drops on standing. The hospital stopped furosemide, but it appears to have been supplied again in her packs; I will correct that today. What changes have you noticed in her day-to-day abilities since discharge?

`11` **Janet Price:** Mum’s managing fine. She’s always tidy and cheerful when I come round. I haven’t noticed much change, really.

`11` **Edith Marsh (adds):** I still have my water tablet every morning, love. I’m up and down to the toilet after.

`12` _GP examines: Inspect current blister packs and separately supplied medicines in the home, including remaining doses and eye drops_ → Morning slots hold furosemide 40 mg and amlodipine 10 mg; night slots hold donepezil 10 mg and atorvastatin 20 mg. Five of last week's seven night slots are still full. The latanoprost bottle by her bed was opened nine weeks ago and is still nearly full. [x_dosette]

`13` **GP → Edith Marsh:** How do you manage your evening tablets and eye drops?

`13` **Edith Marsh:** The girls see to my tablets, love. I do my eye drops myself at bedtime, though. I’m usually in bed quite early.

`13` **Janet Price (adds):** I’d assumed the carers did her eye drops along with her tablets.

`14` **GP → Edith Marsh:** Would you show me how you normally put your eye drops in, without using this old bottle?

`14` **Edith Marsh:** Oh, I just tilt my head back and put a drop in each eye, love. I manage well enough.

`15` _GP examines: Observe Edith demonstrating ability to administer eye drops safely using a demonstration bottle_ → Unremarkable.

`16` **GP → Edith Marsh:** What time do you usually go to bed, compared with when the evening carers arrive?

`16` **Edith Marsh:** I’m usually in bed by half eight, love. I’m often asleep by the time the night girl comes.

`16` **Janet Price (adds):** She’s always been an early-to-bed sort—half eight, nine at the latest.

`17` **GP → Edith Marsh:** Could you talk me through how you manage getting washed and dressed, using the toilet and getting up and down the stairs?

`17` **Edith Marsh:** I see to my own washing and dressing, love. I go up and down the stairs slowly, holding the rail. My bedroom and the toilet are upstairs. I manage as best I can.

`18` _GP examines: Observe transfers and walking with her usual walking aid_ → Rises from the chair at the second attempt, pushing up with her arms. Walks slowly with a stick, reaching for furniture; unsteady on turning. Does not use the walking frame. [x_gait]

`19` **GP → Edith Marsh:** The hospital provided a walking frame. What makes it difficult to use at home?

`19` **Edith Marsh:** Oh, I only use the frame when I’m poorly, love. I manage with my stick most of the time.

`20` _GP examines: Home falls hazards and access to stairs, toilet, walking frame and emergency call system_ → Please name one specific examination.

`21` _GP examines: Home environmental falls hazards_ → Loose rug in the hallway; dim landing light; walking frame folded by the front door. [x_home]

`22` **GP → Edith Marsh:** What have you had to eat and drink so far today, and who helps with meals?

`22` **Edith Marsh:** I do all my own meals, I always have. Janet does a big shop for me on a Sunday, you see.
> ⚑ checker, draft 1: **invented_fact**: She says she has not had much to eat or drink today, which is not in the script.
> rejected draft 1: _I haven’t had much today, I don’t think. I do all my own meals, I always have. Janet does a big shop for me on a Sunday, you see._

`22` **Janet Price (adds):** I do a big shop on Sundays and fill her fridge.

`23` _GP examines: Food availability and signs of meals being eaten in the kitchen and fridge_ → Cooker cold with dust on the hob. Fridge holds out-of-date milk and ham. Two curled sandwiches from yesterday on the side. Little sign of meals being made. [x_kitchen]

`24` **GP → Janet Price:** The notes show carers help with washing and dressing, meals are sometimes uneaten, and evening visits usually come after Edith is asleep. The fridge also has expired food. Are you able to help more temporarily, or is that difficult for you?

`24` **Janet Price:** I work full time, so I can only come round on Sundays. I can’t take on much more during the week.

`24` **Edith Marsh (adds):** I don’t want to be a bother to Janet, doctor. I’d like to stay in my own home. The girls are very good, though they’re always rushing.

`25` _GP examines: Hydration and nutritional status including weight_ → Not available during this home visit. If you need it, request it in your plan.

`26` **GP → Edith Marsh:** I want to help you stay safely at home. Your water tablet is still being given even though hospital stopped it, your blood pressure drops, and you need more help with meals and medicines. Would you accept earlier, longer carer visits and an extra lunchtime visit?

`26` **Edith Marsh:** Oh, if that would help me manage at home, I suppose so, love. I don’t want to make a fuss, though. The girls do seem to be in a hurry.

`27` **GP → Edith Marsh:** So I can check I've explained it clearly, could you tell me what might happen if the current arrangements stayed the same, and how extra help would make things safer?

`27` **Edith Marsh:** Well, I might get giddy and end up on the floor again, I suppose. And I can’t always manage the meals. If the girls came for a bit longer and at lunchtime, they could see I’d eaten and help me with things. I do want to stay in my own home, love.

`28` _GP examines: Focused examination for injury following fall_ → Old bruising over the left hip; no bony tenderness; full range of hip movement. [x_bruising]

`29` **GP → Edith Marsh:** If you fell again and could not get up, how would you call for help?

`29` **Edith Marsh:** I’ve got one of those buttons somewhere, love, but I can’t think where I’ve put it. I’d have to hope someone came by.

`30` _GP examines: Cardiovascular examination_ → Heart sounds normal, chest clear, no ankle oedema, JVP not raised. [x_cardio]

`31` **GP → Janet Price:** I will arrange urgent care support today rather than assume you can cover weekdays. Can you stay until today's safe arrangements and corrected medicines are confirmed?

`31` **Janet Price:** Yes, I can stay until that’s sorted. There’s a key safe by the front door; the carers and I have the number.
> ⚑ checker, draft 1: **hidden_revealed**: She reveals her fear and guilt before the GP has asked how she is coping, what worries her, or mentioned a care home, respite, or a stay away from home.
> rejected draft 1: _Yes, I can stay until that’s sorted. I’m frightened you’ll say she needs a home. I feel guilty I’m not here more, but I want her to stay at home, with more help if that’s what it takes._
> ⚑ checker, draft 2: **hidden_revealed**: She reveals her fear that her mother will need a home and her guilt about not being there more, although the GP has not asked what worries her or mentioned a care home or respite.
> rejected draft 2: _Yes, I can stay until you’ve confirmed what’s happening today. I’m frightened you’ll say she needs a home, and I feel guilty I’m not here more. I want her to stay at home, with more help if that’s what it takes._

`32` **GP → Edith Marsh:** We will stop the water tablet today and have the pharmacy replace the packs safely. Please use your frame, stand up slowly and sit down if dizzy. I will arrange earlier, longer visits with lunchtime food and drink support, help with all medicines including fresh eye drops, and a falls and home-safety assessment. We will find or replace your alarm so you can wear it. Janet will stay while we arrange this, and I will check on you tomorrow. If we cannot arrange enough help today, we will discuss temporary supported care rather than leave you unsafe.

`32` **Edith Marsh:** Oh, thank you, love. I do want to stay here, so I’ll try to use the frame and sit down if I feel giddy. It’s kind of Janet to stay while you sort it all out.

`33` _GP submits plan_

### Plan

**Problems**
- Recurrent unwitnessed falls, including 27 October with unknown time on floor; no current evidence of significant injury, but cause not established by a normal ambulance sitting BP or ECG.
- Symptomatic postural hypotension: lying BP 138/76, standing 108/64 at one minute and 112/66 at three minutes.
- Medication reconciliation failure: furosemide restarted through unreconciled GP repeat and pharmacy packs despite explicit hospital discontinuation; no clinical evidence of heart failure.
- Unreliable evening medication administration and glaucoma-drop use; latanoprost bottle open nine weeks.
- Unmet personal-care and nutrition needs, with poorly timed and shortened care calls; possible service neglect requiring review.
- Mild Alzheimer's disease with impaired recall and overestimation of independence, but demonstrated understanding of proposed additional support and expressed wish to remain home.
- Unsafe mobility with stick, non-use of frame, stairs to bedroom/toilet, environmental hazards and inaccessible pendant alarm.
- CKD stage 3a, hypertension, glaucoma and osteopenia; daughter cannot provide additional regular weekday care.

**Function and ADLs:** Lives alone with two nominal 30-minute daily care calls, actually often about 12–15 minutes. Patient reports independence but care notes confirm help with washing, dressing, medicines and breakfast. Shopping supplied by daughter does not translate into meals eaten; expired food and uneaten sandwiches observed. Rises on second attempt, furniture-walks with stick and is unsteady turning. Frame remains folded by door. Bedroom and toilet upstairs; urgency after diuretic adds risk. Evening calls usually after her 20:30 bedtime, with nine of fourteen evening administrations missed. Daughter visits Sundays and works full time.

**Risks**
- Further postural falls, fracture, head injury and prolonged undiscovered lie.
- Dehydration, malnutrition, renal impairment and electrolyte disturbance from poor intake and inappropriate diuretic.
- Medication omissions, repeat prescribing error and glaucoma progression from unreliable drops.
- Falls on stairs, particularly during toileting; loose hall rug and dim landing light.
- Self-neglect/unmet care needs and possible organisational neglect; patient cannot reliably summon help.
- Unsafe assumption that daughter can compensate for inadequate commissioned care.

**Actions**

| Type | Detail | Rationale | Urgency |
|---|---|---|---|
| medication_change | Stop furosemide 40 mg immediately, remove it from active repeats and document hospital discontinuation. Contact community pharmacist today to collect/reconcile all old packs and supply corrected packs without furosemide; no further doses from erroneous packs. Do not ask Edith or Janet to identify/remove tablets themselves. Inform agency and update MAR and all medication lists, confirming receipt and implementation. | Directly documented prescribing/dispensing discrepancy with persistent symptomatic postural hypotension and no heart failure indication. | same_day |
| medication_change | Review amlodipine today and reduce from 10 mg to 5 mg daily initially, with pharmacy-managed replacement packs and BP review within 48–72 hours; titrate against standing BP, symptoms and individualised targets. Review all medicines for falls burden, including donepezil if dizziness persists. | Standing systolic BP 108 with symptoms and recurrent falls warrants de-intensification rather than pursuing low seated BP. | same_day |
| medication_change | Reconcile all medicines including separately supplied Adcal-D3, PRN paracetamol and drops. Agree a pharmacist-supported schedule moving donepezil and atorvastatin to the reliably attended morning round where appropriate, avoiding duplicate or catch-up doses. Arrange direct supported administration and MAR recording rather than unsupported prompts; assess ongoing statin benefit with Edith at subsequent review. | Full night compartments and agency MAR corroborate frequent omissions; simplifying timing should improve reliability. | same_day |
| medication_change | Discard the nine-week-open latanoprost bottle and supply a fresh bottle today, label opening/discard dates per product instructions, and assign administration and recording to trained carers at an agreed early-evening visit. Include all separately supplied medicines in the written care plan. | Old nearly full bottle and conflicting assumptions about responsibility indicate unreliable glaucoma treatment despite an unremarkable demonstration. | same_day |
| investigation | Arrange FBC, U&E, creatinine/eGFR, glucose and calcium within 24–48 hours, sooner if clinical deterioration; assess hydration, weight/BMI, weight trajectory and MUST score. Obtain repeat ECG if recurrent unexplained events or ongoing symptoms; assess pulse and other syncope causes rather than label all falls mechanical. | CKD, diuretic exposure, poor intake and recurrent falls warrant metabolic and nutritional assessment; previous normal ECG does not exclude intermittent causes. | within_days |
| care_package_change | Contact agency manager and adult social care urgently today for an interim increased package: full commissioned morning time for personal care/breakfast/fluids/medicines, an added lunchtime visit for an observed meal and fluids, and an earlier evening visit before 20:30 for supper, medicines and safe settling. Specify monitoring of intake, refusals and escalation; confirm exact start times and contingency before leaving. | Current visit timing and duration do not meet demonstrated needs; food left in the fridge is not evidence of eating. | same_day |
| other | Janet has agreed to stay until a safe handover is confirmed. Arrange food and drinks now and removal of spoiled food with consent. If enhanced care cannot start promptly, seek urgent social-care crisis/intermediate-care support or temporary supported placement, discussed with Edith; hospital assessment if acutely unwell or no safe clinical alternative. Do not rely on Janet for ongoing weekday coverage. | There must be a workable same-day bridge, not just a routine referral, given falls and unmet nutrition and medication needs. | same_day |
| referral | Urgent multidisciplinary falls/community frailty and physiotherapy assessment for strength, balance, transfers, frame use and multifactorial falls/syncope review; occupational therapy home assessment including stairs, toileting and personal-care needs. | Observed unsteady gait and recurrent falls despite recent discharge therapy suggest that current aids and arrangements are inadequate. | within_days |
| equipment | Unfold and place frame within reach, check fit and safe use with assistance. With consent remove loose rug and improve landing lighting today. Retrieve/test or urgently replace pendant alarm and ensure it is worn with a working response service and key-safe access. OT to consider rails, suitable toilet equipment/commode and safe downstairs arrangements rather than unsupported stair use. | Immediate modifiable hazards and inability to summon assistance increase risk of another prolonged lie. | same_day |
| safeguarding | With Edith's involvement raise an adult social-care safeguarding concern about unmet care needs/possible organisational neglect: repeated shortened calls, missed medication without effective escalation, nutrition concerns and communication after fall. Seek agency incident review and reliable notification to GP and agreed family contact. Record medication error as a patient-safety incident, explain and apologise for the error, and review discharge-reconciliation processes. | An adult with care and support needs is exposed to repeated avoidable harm; cheerful appearance does not establish safety. Investigate without assuming malicious intent. | same_day |
| carer_support | Record Janet's actual availability and offer a carer's assessment and support information. With Edith's consent agree who receives fall/medication alerts and share the updated written plan with Janet and the agency. | Daughter was unaware of the recurrent fall and cannot provide additional routine care. | within_days |
| referral | Arrange optometry/glaucoma review of vision and adherence; expedite ophthalmology advice for deterioration. Review fracture risk and suitability for osteoporosis treatment with renal function and prior DEXA information. | Visual impairment, glaucoma treatment uncertainty, osteopenia and recurrent falls compound injury risk. | within_days |
| advice | Explain postural precautions: sit before standing, rise slowly with support, sit or lie down promptly if dizzy, keep drinks accessible and encourage regular fluids unless a contraindication emerges. Avoid walking unsupported or rushing to the toilet; use frame and assistance. Discuss safe footwear and supervised activity rather than immobility. | Reduces immediate falls risk while medication and care arrangements are corrected. | same_day |
| follow_up | Document decision-specific capacity: Edith can explain fall/nutrition risks and how extra care helps, accepts changes and wishes to stay home. Respect this preference with supported decisions; reassess if cognition changes. Complete medication reconciliation and confirm actual care delivery rather than relying on referrals alone. | Alzheimer's diagnosis and limited recall do not automatically remove capacity or justify overriding her wishes. | same_day |

**Discrepancies**
- Hospital stopped furosemide, but GP repeats, pharmacy packs and Edith's account indicate continued use. → Discharge instruction plus actual pack inspection establish an unintentional restart. Stop and correct all prescribing, supply and administration records today.
- Edith denies a further fall and Janet had not been told, whereas agency and ambulance record a floor episode on 27 October. → Treat dated agency and ambulance observations as evidence of a recurrent unwitnessed fall; limited recall is not evidence it did not happen. Explain findings and improve notifications.
- Ambulance described a mechanical fall with normal sitting BP, while Edith reports morning giddiness and today's standing BP drops substantially. → Mechanical cause remains unproven. Current symptomatic orthostatic hypotension and medication error are major modifiable contributors; maintain multifactorial/syncope assessment.
- Edith reports independent washing, dressing and cooking; Janet sees a tidy, cheerful home and assumes adequate function. → Care notes document personal-care support; direct gait observation and kitchen findings show unmet needs. Assess function using observed performance and longitudinal evidence rather than Sunday appearance or recall alone.
- Care package is two 30-minute visits, yet recorded visits are usually about 12–15 minutes and evening doses are frequently omitted. → Actual timings and MAR establish an ineffective package. Escalate to manager/social care, lengthen visits and bring evening support before bedtime.
- Edith says she manages eye drops and Janet assumes carers administer them. → No reliable assigned responsibility; nine-week-old nearly full bottle strongly suggests inadequate use. Demonstration alone does not prove daily adherence; assign carer administration and MAR recording.
- Hospital advised frame use at all times, but ambulance saw stick use and frame is folded away. → Observed furniture-walking and unstable turns support consistent frame use and urgent therapy review.

**Follow-up:** Before leaving today confirm pharmacy correction, agency/social-care response, interim meals and supervision, and Janet-to-care-service handover. GP/team contact next day to verify new packs, actual visits, oral intake, dizziness and falls. Review blood results promptly and repeat lying/standing BP and renal function as indicated within 48–72 hours, with further review in one week of mobility, medication administration/MAR, nutrition and safeguarding response. Ensure named GP/team owns referrals and outstanding actions.

**Safety-netting:** Call 999 for collapse, chest pain, severe breathlessness, new focal neurological symptoms, serious injury, inability to rise after a fall, or head injury with concerning symptoms. Do not attempt an unsafe lift; use pendant/telephone and keep warm while waiting. Seek same-day GP assessment, or NHS 111 out of hours, for recurrent falls or worsening dizziness, new confusion, poor intake, markedly reduced urine, pain or inability to mobilise. Sudden painful red eye or sudden vision loss needs urgent same-day eye/emergency assessment. Carers should escalate missed medicines, missed visits, refusal of essential support or food and drink not being taken, rather than record and leave without a plan.

## Visit 2, telephone consultation, Thursday 19 November 2026

- **Turns:** 17 used of a 20-turn budget (hard cap 40); ended by plan
- **Checker:** 1 flagged drafts, 1 regenerated; 0 interjection calls stayed silent

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
- Recurrent unwitnessed falls, including 27 October with unknown time on floor; no current evidence of significant injury, but cause not established by a normal ambulance sitting BP or ECG.
- Symptomatic postural hypotension: lying BP 138/76, standing 108/64 at one minute and 112/66 at three minutes.
- Medication reconciliation failure: furosemide restarted through unreconciled GP repeat and pharmacy packs despite explicit hospital discontinuation; no clinical evidence of heart failure.
- Unreliable evening medication administration and glaucoma-drop use; latanoprost bottle open nine weeks.
- Unmet personal-care and nutrition needs, with poorly timed and shortened care calls; possible service neglect requiring review.
- Mild Alzheimer's disease with impaired recall and overestimation of independence, but demonstrated understanding of proposed additional support and expressed wish to remain home.
- Unsafe mobility with stick, non-use of frame, stairs to bedroom/toilet, environmental hazards and inaccessible pendant alarm.
- CKD stage 3a, hypertension, glaucoma and osteopenia; daughter cannot provide additional regular weekday care.
Function and ADLs: Lives alone with two nominal 30-minute daily care calls, actually often about 12–15 minutes. Patient reports independence but care notes confirm help with washing, dressing, medicines and breakfast. Shopping supplied by daughter does not translate into meals eaten; expired food and uneaten sandwiches observed. Rises on second attempt, furniture-walks with stick and is unsteady turning. Frame remains folded by door. Bedroom and toilet upstairs; urgency after diuretic adds risk. Evening calls usually after her 20:30 bedtime, with nine of fourteen evening administrations missed. Daughter visits Sundays and works full time.
Risks:
- Further postural falls, fracture, head injury and prolonged undiscovered lie.
- Dehydration, malnutrition, renal impairment and electrolyte disturbance from poor intake and inappropriate diuretic.
- Medication omissions, repeat prescribing error and glaucoma progression from unreliable drops.
- Falls on stairs, particularly during toileting; loose hall rug and dim landing light.
- Self-neglect/unmet care needs and possible organisational neglect; patient cannot reliably summon help.
- Unsafe assumption that daughter can compensate for inadequate commissioned care.
Actions:
- medication_change (same_day): Stop furosemide 40 mg immediately, remove it from active repeats and document hospital discontinuation. Contact community pharmacist today to collect/reconcile all old packs and supply corrected packs without furosemide; no further doses from erroneous packs. Do not ask Edith or Janet to identify/remove tablets themselves. Inform agency and update MAR and all medication lists, confirming receipt and implementation.. Why: Directly documented prescribing/dispensing discrepancy with persistent symptomatic postural hypotension and no heart failure indication.
- medication_change (same_day): Review amlodipine today and reduce from 10 mg to 5 mg daily initially, with pharmacy-managed replacement packs and BP review within 48–72 hours; titrate against standing BP, symptoms and individualised targets. Review all medicines for falls burden, including donepezil if dizziness persists.. Why: Standing systolic BP 108 with symptoms and recurrent falls warrants de-intensification rather than pursuing low seated BP.
- medication_change (same_day): Reconcile all medicines including separately supplied Adcal-D3, PRN paracetamol and drops. Agree a pharmacist-supported schedule moving donepezil and atorvastatin to the reliably attended morning round where appropriate, avoiding duplicate or catch-up doses. Arrange direct supported administration and MAR recording rather than unsupported prompts; assess ongoing statin benefit with Edith at subsequent review.. Why: Full night compartments and agency MAR corroborate frequent omissions; simplifying timing should improve reliability.
- medication_change (same_day): Discard the nine-week-open latanoprost bottle and supply a fresh bottle today, label opening/discard dates per product instructions, and assign administration and recording to trained carers at an agreed early-evening visit. Include all separately supplied medicines in the written care plan.. Why: Old nearly full bottle and conflicting assumptions about responsibility indicate unreliable glaucoma treatment despite an unremarkable demonstration.
- investigation (within_days): Arrange FBC, U&E, creatinine/eGFR, glucose and calcium within 24–48 hours, sooner if clinical deterioration; assess hydration, weight/BMI, weight trajectory and MUST score. Obtain repeat ECG if recurrent unexplained events or ongoing symptoms; assess pulse and other syncope causes rather than label all falls mechanical.. Why: CKD, diuretic exposure, poor intake and recurrent falls warrant metabolic and nutritional assessment; previous normal ECG does not exclude intermittent causes.
- care_package_change (same_day): Contact agency manager and adult social care urgently today for an interim increased package: full commissioned morning time for personal care/breakfast/fluids/medicines, an added lunchtime visit for an observed meal and fluids, and an earlier evening visit before 20:30 for supper, medicines and safe settling. Specify monitoring of intake, refusals and escalation; confirm exact start times and contingency before leaving.. Why: Current visit timing and duration do not meet demonstrated needs; food left in the fridge is not evidence of eating.
- other (same_day): Janet has agreed to stay until a safe handover is confirmed. Arrange food and drinks now and removal of spoiled food with consent. If enhanced care cannot start promptly, seek urgent social-care crisis/intermediate-care support or temporary supported placement, discussed with Edith; hospital assessment if acutely unwell or no safe clinical alternative. Do not rely on Janet for ongoing weekday coverage.. Why: There must be a workable same-day bridge, not just a routine referral, given falls and unmet nutrition and medication needs.
- referral (within_days): Urgent multidisciplinary falls/community frailty and physiotherapy assessment for strength, balance, transfers, frame use and multifactorial falls/syncope review; occupational therapy home assessment including stairs, toileting and personal-care needs.. Why: Observed unsteady gait and recurrent falls despite recent discharge therapy suggest that current aids and arrangements are inadequate.
- equipment (same_day): Unfold and place frame within reach, check fit and safe use with assistance. With consent remove loose rug and improve landing lighting today. Retrieve/test or urgently replace pendant alarm and ensure it is worn with a working response service and key-safe access. OT to consider rails, suitable toilet equipment/commode and safe downstairs arrangements rather than unsupported stair use.. Why: Immediate modifiable hazards and inability to summon assistance increase risk of another prolonged lie.
- safeguarding (same_day): With Edith's involvement raise an adult social-care safeguarding concern about unmet care needs/possible organisational neglect: repeated shortened calls, missed medication without effective escalation, nutrition concerns and communication after fall. Seek agency incident review and reliable notification to GP and agreed family contact. Record medication error as a patient-safety incident, explain and apologise for the error, and review discharge-reconciliation processes.. Why: An adult with care and support needs is exposed to repeated avoidable harm; cheerful appearance does not establish safety. Investigate without assuming malicious intent.
- carer_support (within_days): Record Janet's actual availability and offer a carer's assessment and support information. With Edith's consent agree who receives fall/medication alerts and share the updated written plan with Janet and the agency.. Why: Daughter was unaware of the recurrent fall and cannot provide additional routine care.
- referral (within_days): Arrange optometry/glaucoma review of vision and adherence; expedite ophthalmology advice for deterioration. Review fracture risk and suitability for osteoporosis treatment with renal function and prior DEXA information.. Why: Visual impairment, glaucoma treatment uncertainty, osteopenia and recurrent falls compound injury risk.
- advice (same_day): Explain postural precautions: sit before standing, rise slowly with support, sit or lie down promptly if dizzy, keep drinks accessible and encourage regular fluids unless a contraindication emerges. Avoid walking unsupported or rushing to the toilet; use frame and assistance. Discuss safe footwear and supervised activity rather than immobility.. Why: Reduces immediate falls risk while medication and care arrangements are corrected.
- follow_up (same_day): Document decision-specific capacity: Edith can explain fall/nutrition risks and how extra care helps, accepts changes and wishes to stay home. Respect this preference with supported decisions; reassess if cognition changes. Complete medication reconciliation and confirm actual care delivery rather than relying on referrals alone.. Why: Alzheimer's diagnosis and limited recall do not automatically remove capacity or justify overriding her wishes.
Discrepancies:
- Hospital stopped furosemide, but GP repeats, pharmacy packs and Edith's account indicate continued use.: Discharge instruction plus actual pack inspection establish an unintentional restart. Stop and correct all prescribing, supply and administration records today.
- Edith denies a further fall and Janet had not been told, whereas agency and ambulance record a floor episode on 27 October.: Treat dated agency and ambulance observations as evidence of a recurrent unwitnessed fall; limited recall is not evidence it did not happen. Explain findings and improve notifications.
- Ambulance described a mechanical fall with normal sitting BP, while Edith reports morning giddiness and today's standing BP drops substantially.: Mechanical cause remains unproven. Current symptomatic orthostatic hypotension and medication error are major modifiable contributors; maintain multifactorial/syncope assessment.
- Edith reports independent washing, dressing and cooking; Janet sees a tidy, cheerful home and assumes adequate function.: Care notes document personal-care support; direct gait observation and kitchen findings show unmet needs. Assess function using observed performance and longitudinal evidence rather than Sunday appearance or recall alone.
- Care package is two 30-minute visits, yet recorded visits are usually about 12–15 minutes and evening doses are frequently omitted.: Actual timings and MAR establish an ineffective package. Escalate to manager/social care, lengthen visits and bring evening support before bedtime.
- Edith says she manages eye drops and Janet assumes carers administer them.: No reliable assigned responsibility; nine-week-old nearly full bottle strongly suggests inadequate use. Demonstration alone does not prove daily adherence; assign carer administration and MAR recording.
- Hospital advised frame use at all times, but ambulance saw stick use and frame is folded away.: Observed furniture-walking and unstable turns support consistent frame use and urgent therapy review.
Follow-up: Before leaving today confirm pharmacy correction, agency/social-care response, interim meals and supervision, and Janet-to-care-service handover. GP/team contact next day to verify new packs, actual visits, oral intake, dizziness and falls. Review blood results promptly and repeat lying/standing BP and renal function as indicated within 48–72 hours, with further review in one week of mobility, medication administration/MAR, nutrition and safeguarding response. Ensure named GP/team owns referrals and outstanding actions.
Safety-netting: Call 999 for collapse, chest pain, severe breathlessness, new focal neurological symptoms, serious injury, inability to rise after a fall, or head injury with concerning symptoms. Do not attempt an unsafe lift; use pendant/telephone and keep warm while waiting. Seek same-day GP assessment, or NHS 111 out of hours, for recurrent falls or worsening dizziness, new confusion, poor intake, markedly reduced urine, pain or inability to mobilise. Sudden painful red eye or sudden vision loss needs urgent same-day eye/emergency assessment. Carers should escalate missed medicines, missed visits, refusal of essential support or food and drink not being taken, rather than record and leave without a plan.
```

### Consultation

` 1` **GP → Janet Price:** Janet, please tell me what happened with this latest fall, including when it happened and how your mother is now.

` 1` **Janet Price:** She fell on Saturday night going to the loo and was on the bathroom floor until the carer came in the morning. The paramedics checked her over and left her at home. I stayed the weekend; she was up in the night not knowing where she was and had wet the bed. She’s better in the daytime, just a bit muddled.

` 2` _GP reads `ambulance_report`_
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

` 3` **GP → Janet Price:** Is someone with Edith now, and has she had any new difficulty staying awake, weakness, pain, trouble walking, fever, or reduced drinking or urine today?

` 3` **Janet Price:** She’s at home. I’m at work, and the carers still come morning and evening. She’s better in the daytime, just a bit muddled.

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
>   05 Nov 2026  GP (you)        Home visit. Problems: Recurrent unwitnessed falls, including 27
>                                October with unknown time on floor; no current evidence of
>                                significant injury, but cause not established by a normal ambulance
>                                sitting BP or ECG; Symptomatic postural hypotension: lying BP 138/76,
>                                standing 108/64 at one minute and 112/66 at three minutes; Medication
>                                reconciliation failure: furosemide restarted through unreconciled GP
>                                repeat and pharmacy packs despite explicit hospital discontinuation;
>                                no clinical evidence of heart failure; Unreliable evening medication
>                                administration and glaucoma-drop use; latanoprost bottle open nine
>                                weeks; Unmet personal-care and nutrition needs, with poorly timed and
>                                shortened care calls; possible service neglect requiring review; Mild
>                                Alzheimer's disease with impaired recall and overestimation of
>                                independence, but demonstrated understanding of proposed additional
>                                support and expressed wish to remain home; Unsafe mobility with
>                                stick, non-use of frame, stairs to bedroom/toilet, environmental
>                                hazards and inaccessible pendant alarm; CKD stage 3a, hypertension,
>                                glaucoma and osteopenia; daughter cannot provide additional regular
>                                weekday care. Plan: Stop furosemide 40 mg immediately, remove it from
>                                active repeats and document hospital discontinuation. Contact
>                                community pharmacist today to collect/reconcile all old packs and
>                                supply corrected packs without furosemide; no further doses from
>                                erroneous packs. Do not ask Edith or Janet to identify/remove tablets
>                                themselves. Inform agency and update MAR and all medication lists,
>                                confirming receipt and implementation; Review amlodipine today and
>                                reduce from 10 mg to 5 mg daily initially, with pharmacy-managed
>                                replacement packs and BP review within 48–72 hours; titrate against
>                                standing BP, symptoms and individualised targets. Review all
>                                medicines for falls burden, including donepezil if dizziness
>                                persists; Reconcile all medicines including separately supplied
>                                Adcal-D3, PRN paracetamol and drops. Agree a pharmacist-supported
>                                schedule moving donepezil and atorvastatin to the reliably attended
>                                morning round where appropriate, avoiding duplicate or catch-up
>                                doses. Arrange direct supported administration and MAR recording
>                                rather than unsupported prompts; assess ongoing statin benefit with
>                                Edith at subsequent review; Discard the nine-week-open latanoprost
>                                bottle and supply a fresh bottle today, label opening/discard dates
>                                per product instructions, and assign administration and recording to
>                                trained carers at an agreed early-evening visit. Include all
>                                separately supplied medicines in the written care plan; Arrange FBC,
>                                U&E, creatinine/eGFR, glucose and calcium within 24–48 hours, sooner
>                                if clinical deterioration; assess hydration, weight/BMI, weight
>                                trajectory and MUST score. Obtain repeat ECG if recurrent unexplained
>                                events or ongoing symptoms; assess pulse and other syncope causes
>                                rather than label all falls mechanical; Contact agency manager and
>                                adult social care urgently today for an interim increased package:
>                                full commissioned morning time for personal
>                                care/breakfast/fluids/medicines, an added lunchtime visit for an
>                                observed meal and fluids, and an earlier evening visit before 20:30
>                                for supper, medicines and safe settling. Specify monitoring of
>                                intake, refusals and escalation; confirm exact start times and
>                                contingency before leaving; Janet has agreed to stay until a safe
>                                handover is confirmed. Arrange food and drinks now and removal of
>                                spoiled food with consent. If enhanced care cannot start promptly,
>                                seek urgent social-care crisis/intermediate-care support or temporary
>                                supported placement, discussed with Edith; hospital assessment if
>                                acutely unwell or no safe clinical alternative. Do not rely on Janet
>                                for ongoing weekday coverage; Urgent multidisciplinary
>                                falls/community frailty and physiotherapy assessment for strength,
>                                balance, transfers, frame use and multifactorial falls/syncope
>                                review; occupational therapy home assessment including stairs,
>                                toileting and personal-care needs; Unfold and place frame within
>                                reach, check fit and safe use with assistance. With consent remove
>                                loose rug and improve landing lighting today. Retrieve/test or
>                                urgently replace pendant alarm and ensure it is worn with a working
>                                response service and key-safe access. OT to consider rails, suitable
>                                toilet equipment/commode and safe downstairs arrangements rather than
>                                unsupported stair use; With Edith's involvement raise an adult
>                                social-care safeguarding concern about unmet care needs/possible
>                                organisational neglect: repeated shortened calls, missed medication
>                                without effective escalation, nutrition concerns and communication
>                                after fall. Seek agency incident review and reliable notification to
>                                GP and agreed family contact. Record medication error as a patient-
>                                safety incident, explain and apologise for the error, and review
>                                discharge-reconciliation processes; Record Janet's actual
>                                availability and offer a carer's assessment and support information.
>                                With Edith's consent agree who receives fall/medication alerts and
>                                share the updated written plan with Janet and the agency; Arrange
>                                optometry/glaucoma review of vision and adherence; expedite
>                                ophthalmology advice for deterioration. Review fracture risk and
>                                suitability for osteoporosis treatment with renal function and prior
>                                DEXA information; Explain postural precautions: sit before standing,
>                                rise slowly with support, sit or lie down promptly if dizzy, keep
>                                drinks accessible and encourage regular fluids unless a
>                                contraindication emerges. Avoid walking unsupported or rushing to the
>                                toilet; use frame and assistance. Discuss safe footwear and
>                                supervised activity rather than immobility; Document decision-
>                                specific capacity: Edith can explain fall/nutrition risks and how
>                                extra care helps, accepts changes and wishes to stay home. Respect
>                                this preference with supported decisions; reassess if cognition
>                                changes. Complete medication reconciliation and confirm actual care
>                                delivery rather than relying on referrals alone. Follow-up: Before
>                                leaving today confirm pharmacy correction, agency/social-care
>                                response, interim meals and supervision, and Janet-to-care-service
>                                handover. GP/team contact next day to verify new packs, actual
>                                visits, oral intake, dizziness and falls. Review blood results
>                                promptly and repeat lying/standing BP and renal function as indicated
>                                within 48–72 hours, with further review in one week of mobility,
>                                medication administration/MAR, nutrition and safeguarding response.
>                                Ensure named GP/team owns referrals and outstanding actions.
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

` 7` **GP → Janet Price:** When did the night-time confusion and bedwetting first start compared with her usual memory difficulties?

` 7` **Janet Price:** It was that night after she fell on Saturday. Her memory’s been getting worse over the past year, but this getting up confused and wetting the bed was new.

` 8` **GP → Janet Price:** Has she mentioned burning or pain when passing urine, passing urine more often than usual, or lower tummy or back pain?

` 8` **Janet Price:** No, she hasn’t said it hurts or burns when she goes. I’m not sure if she’s going more often. Her wee has smelled strong, though.
> ⚑ checker, draft 1: **over_cooperative**: She answers all three separate symptom questions in the GP’s turn: pain or burning, frequency, and tummy or back pain.
> rejected draft 1: _She hasn’t said it burns or hurts, and I haven’t noticed her going more often or having tummy or back pain. Her wee did smell strong, though._

` 9` **GP → Janet Price:** A sudden fluctuating change like this could be delirium from illness, dehydration, pain or medicines, rather than simply worsening Alzheimer's. Strong-smelling urine alone does not prove a urine infection. I will arrange an urgent assessment at home today. Has she had any constipation or difficulty emptying her bladder?

` 9` **Janet Price:** I haven’t noticed constipation or trouble emptying her bladder. She did feel hot on Sunday night, and she’s barely eating. Her wee smells strong.

`10` **GP → Janet Price:** Can you contact the care agency now to have someone go to Edith and stay with her while we organise today's assessment, or is there another trusted person available?

`10` **Janet Price:** I can ring the agency now and ask them to send someone round and stay with her. I’m at work, so I can’t get there straight away.

`11` _GP reads `discharge_summary`_
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

`12` **GP → Janet Price:** Were any of the changes we arranged two weeks ago actually put in place, such as replacement medicine packs, extra or earlier care visits, blood tests or a blood pressure check?

`12` **Janet Price:** I’m not sure about the extra visits or checks. I thought the hospital had sorted her tablets out and the chemist was doing the pods.

`13` **GP → Janet Price:** Since the fall has she had any headache, vomiting, new severe pain or worsening difficulty walking, or is there any possibility she hit her head?

`13` **Janet Price:** I don’t think she hit her head, as far as I know. She’s got a bruise on her arm, but I haven’t noticed anything else.

`14` **GP → Janet Price:** Has anyone confirmed how much she is drinking and whether she is still passing a normal amount of urine today?

`14` **Janet Price:** I don’t know how much she’s had today. She’s been drinking her tea, but I can’t say if she’s passing her usual amount of urine.

`15` **GP → Janet Price:** The pharmacy record shows the old doses were still supplied on Monday: furosemide and amlodipine 10 mg. This conflicts with our plan and may be contributing to dehydration and falls. I'm sorry this has not been corrected. I will contact the pharmacy and agency urgently to stop the furosemide, replace the packs safely and check what she has actually received; please don't remove tablets yourselves. Is there anything else worrying you about keeping her safe at home?

`15` **Janet Price:** I want her to stay at home, with more help if that’s what it takes. I’m frightened you’ll say she needs a home, and I feel guilty I’m not there more.

`16` **GP → Janet Price:** This is not your fault, and you are not expected to replace a care service. We will involve Edith and aim to support her wishes to remain at home; temporary hospital or supported care may be needed if she is unwell or cannot be kept safe, not automatically a permanent move. Please ask the agency to confirm someone is with her now. If she is difficult to wake, suddenly much more confused, has weakness, severe breathlessness, collapses or cannot stand after injury, call 999. If nobody can attend promptly, contact us immediately so we can arrange an urgent welfare and clinical response rather than leave her alone.

`16` **Janet Price:** All right, I’ll ring the agency now and make sure someone’s with her. If they can’t get there promptly, I’ll ring you straight away.

`17` _GP submits plan_

### Plan

**Problems**
- Suspected delirium superimposed on Alzheimer's disease: abrupt new fluctuating night-time disorientation and incontinence since 14 November, possible fever and markedly reduced intake. Infection, dehydration, medication effects, pain and metabolic disturbance require urgent exclusion; cannot diagnose by telephone.
- Recurrent unwitnessed nocturnal fall on 14 November with likely prolonged lie and right forearm bruising; injury, postural hypotension and other syncope causes not excluded by ambulance observations.
- Persistent medication-reconciliation failure: pharmacy supplied furosemide 40 mg and amlodipine 10 mg on 9 and 16 November despite 5 November stop/reduction plan.
- Inadequate care delivery, nutrition and medication support; previous additional care, monitoring and safeguarding actions not confirmed implemented.
- CKD stage 3a with risk of acute kidney injury/electrolyte disturbance, recurrent falls, unsafe night-time toileting and inability to obtain help reliably.

**Function and ADLs:** Lives alone in two-storey home with only two daily care visits still reported. Previously required washing, dressing, meal and medication support and had unsafe stick/furniture walking despite a prescribed frame. Latest fall occurred en route to toilet overnight and she remained on bathroom floor until morning. New night-time disorientation and bedwetting further compromise independence. Current walking, hydration and immediate safety cannot be established by telephone. Daughter works and cannot provide routine weekday supervision.

**Risks**
- Unrecognised acute illness/delirium, sepsis, dehydration, AKI or electrolyte disturbance.
- Recurrent collapse, occult injury or complications of prolonged lie including muscle injury.
- Ongoing exposure to erroneous medicines and missed evening doses.
- Further overnight falls, prolonged undiscovered lie and unsafe periods alone.
- Malnutrition, unmet care needs and possible organisational neglect; unimplemented prior safety plan.
- Carer distress and unrealistic dependence on daughter.

**Actions**

| Type | Detail | Rationale | Urgency |
|---|---|---|---|
| referral | Arrange urgent same-day GP/urgent community response face-to-face home assessment, prioritised now given possible fever, poor intake and new confusion. Handover directly and confirm clinician and attendance time. If significant physiological disturbance, severe delirium, injury, inability to drink/mobilise, suspected AKI/rhabdomyolysis or no safe timely community assessment, arrange emergency hospital assessment/conveyance. | Telephone reassurance and previously normal ambulance observations cannot establish current safety or exclude acute illness. | same_day |
| other | Janet will contact agency immediately for a carer to attend and remain; practice team to contact agency directly and confirm attendance and interim supervision, current alertness, intake and urine output. Do not assume arrangement is in place. If unavailable activate urgent community/social-care crisis response; arrange hospital assessment if clinically unsafe without support. | Edith is currently alone with incompletely assessed acute confusion and poor intake; daughter cannot attend immediately. | same_day |
| investigation | At in-person assessment obtain full observations including temperature, pulse, respiratory rate, oxygen saturation, BP and glucose, hydration and delirium assessment (e.g. 4AT with collateral baseline). Examine heart/lungs, abdomen/bladder, neurological status, head, forearm and other injuries; assess pain, pressure areas, weight/intake, retention/constipation and supported mobility. Check lying/standing BP only when safe. Reassess possible head injury and imaging need from findings. | Identify reversible causes and acute severity, assess trauma and distinguish delirium from chronic cognitive decline. | same_day |
| investigation | Arrange urgent FBC, U&E/creatinine, electrolytes, glucose, calcium and inflammatory markers; consider CK and urinalysis for muscle injury given likely long lie and renal risk, and ECG for recurrent unexplained falls/pulse abnormalities. Ensure same-day review of results and hospital pathway if urgent testing/results cannot be safely delivered at home. | Diuretic exposure, CKD, poor intake and prolonged lie increase risk of renal and metabolic complications. | same_day |
| investigation | Assess for urinary and other infection sources. Obtain a properly collected urine sample for culture before antibiotics if clinically suspected UTI; do not use dipstick or odour alone to diagnose UTI in an older adult. New incontinence, possible fever and delirium warrant assessment, not automatic antibiotics. Treat promptly according to clinical findings/local guidance and renal function; do not delay emergency treatment for suspected sepsis. | No reported dysuria, frequency uncertain, strong smell nonspecific; avoid attributing delirium to asymptomatic bacteriuria while not missing infection. | same_day |
| medication_change | Contact pharmacist and agency today to verify actual administered doses and remove furosemide 40 mg from repeats and all packs immediately; no further doses. Arrange pharmacy-managed collection and replacement of erroneous packs, not family tablet removal. Implement previously planned amlodipine reduction to 5 mg pending today's clinical/BP assessment; withhold BP-lowering therapy if clinically indicated by hypotension/dehydration under assessing clinician. Reconcile every medicine and MAR, including donepezil, separate Adcal-D3 and latanoprost; confirm safe timing, supported administration and avoid duplicate doses. Confirm corrections with named pharmacy and agency staff. | Dated pharmacy dispensing demonstrates continued erroneous supply despite prior plan; symptomatic orthostasis and poor intake make continuation hazardous. | same_day |
| care_package_change | Urgently contact agency manager and adult social care to implement, not merely re-refer, full personal-care/meal/fluids/medication visits including lunchtime and earlier evening support. Assess and provide overnight supervision now while confused, with temporary supported placement/respite if home safety cannot be achieved. Provide a written handover, explicit escalation instructions and confirm start times and cover today. | Twice-daily visits do not address current night-time risk or nutrition; prior requested changes appear not delivered. | same_day |
| safeguarding | Escalate previous adult safeguarding concern today for recurrent harm with shortened/late visits and failed medication/care-plan implementation. Review why 5 November actions and follow-up failed, report medication safety incident and explain/apologise openly. Obtain actual visit logs, current MAR, referral status and previous blood/BP results, assigning a named GP to close each outstanding action. | Repeat falls and preventable ongoing medication exposure suggest system failures and unmet care needs requiring accountable action. | same_day |
| equipment | Urgent OT/community falls review of toileting, transfers, frame use, stairs and appropriate commode/downstairs arrangement. Verify working worn pendant, response service and key-safe access. Remove hazards, improve lighting and ensure drinks and telephone accessible; no unsupported night-time stair use while acutely confused. | Fall occurred going to the toilet and she could not summon help; an alarm alone may not suffice during delirium. | same_day |
| carer_support | Reassure Janet that this is not her fault and she is not expected to provide care she cannot sustain. Offer carer's assessment and practical support. Involve Edith directly during assessment, establish consent for information sharing, reassess decision-specific capacity in light of possible delirium and support decisions. If lacking capacity for urgent arrangements, make proportionate best-interests decisions with Janet and MDT, checking any relevant proxy authority. | Daughter is distressed and wishes home care; dementia does not itself establish incapacity or necessitate permanent placement. | same_day |
| advice | While awaiting assessment offer familiar reassurance, orientation, glasses/hearing aids, supported regular drinks/food if awake and swallowing safely, supervised frame use and toileting. Avoid sedatives for routine night-time confusion; address underlying causes and discomfort. | Non-drug delirium support and safe assistance reduce immediate harm. | same_day |
| follow_up | Named GP to verify same-day clinical attendance, carer cover, medication correction, investigation results and disposition, with telephone contact with Janet/agency today. Review next day and repeat renal function/BP as clinically indicated, then MDT review within days of cognition, falls, nutrition and actual care delivery; chase prior falls/OT, glaucoma and bone-health referrals once acute issues addressed. | Previous documented intentions did not translate into reliable implementation; closed-loop follow-up is essential. | same_day |

**Discrepancies**
- Daughter describes daytime improvement and longstanding memory decline, but new night disorientation and incontinence began abruptly after latest fall; agency documents wanting to go home on 17 November. → Treat as possible fluctuating delirium rather than assuming dementia progression or harmless sundowning; daytime improvement does not exclude delirium.
- 5 November plan stopped furosemide and reduced amlodipine, but GP repeat list remains old and pharmacy supplied unchanged packs on 9 and 16 November. → Actual dated dispensing establishes continued unsafe supply; verify MAR and correct prescribing, packing and administration directly today, acknowledging implementation failure.
- Ambulance calls fall mechanical with normal observations and no head injury; fall unwitnessed with likely long lie and subsequent new confusion. → Mechanism and duration remain uncertain. Normal observations at the time do not exclude postural hypotension, intermittent syncope, occult injury or subsequent illness; reassess face to face.
- Prior plan required increased/earlier care and monitoring, but daughter reports twice-daily visits, agency records late short call and no completion results are documented. → Do not assume referrals or changes occurred. Check actual logs/results and confirm an effective interim package and supervision today.
- Strong-smelling urine and bedwetting could be interpreted as UTI, but dysuria absent and frequency unknown. → These findings are not diagnostic; assess infection and alternative delirium causes, with culture if clinically indicated rather than empirical treatment based on smell alone.

**Follow-up:** Same-day named clinician ownership until home assessment, investigations, medicine correction and safe care/disposition confirmed. Contact Janet and agency today and next day; prompt results review and renal/BP reassessment according to findings. MDT review within days, with documented completion of each previously outstanding action.

**Safety-netting:** Janet advised to arrange agency attendance now and call practice immediately if this cannot be achieved; practice will independently confirm rather than rely solely on her. Call 999 for difficult arousal, collapse, severe or rapidly worsening confusion, new focal weakness, chest pain, severe breathlessness, major injury or inability to rise safely; do not attempt an unsafe lift. Urgent same-day GP/111 for increasing fever, reduced drinking/urine, vomiting, pain, further falls or increasing confusion; acute deterioration should not wait for planned home visit. Carers must escalate missed visits, medication errors or refusal/inability to eat or drink immediately and not leave without an agreed safe plan.
