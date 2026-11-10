# Screening: first pull (4 Nov 2026)

`clinical-env sources pull --limit 150` (default query): 150 candidates, all CC BY by their own
XML (the search already filters on licence), 80 through the prefilter. Full log:
`licence_log.csv`; candidates and abstracts: `candidates.jsonl`.

Shortlist from reading the 80 titles and abstracts, then the full text of the two picked.
Each row is judged for primary care fit (could a primary care doctor have caught it over
weeks?) and how common or unglamorous the problem is.

| # | PMCID | Theme | Primary care fit | Notes |
| --- | --- | --- | --- | --- |
| 1 | PMC12863219 | Hyponatremia and hypothyroidism behind months of decline | High: slow decline put down to age, carer-reported | **Picked (case A).** Reversible; fits medicine reconciliation and a carer |
| 2 | PMC11897834 | Antiepileptic toxicity mistaken for vertigo | High: dizziness, falls risk, medicine review | **Picked (case B).** Rewritten to phenytoin after the identifiability check |
| 3 | PMC12755957 | Delirium from an over-the-counter cold remedy | High: unlisted medicine, carer notices | Good for an "unlisted OTC medicine" case; product is not a US one, swap to diphenhydramine |
| 4 | PMC12484005 | Electrolyte loss from years of a PPI | High: PPI with no indication (a MIMIC pattern) | Deprescribing case; needs results that arrive by a route independent of the plan |
| 5 | PMC13158927 | AKI from overtreated hypertension | Medium: similar to Edith (blood pressure, falls) | Avoid until the set needs another blood pressure case |
| 6 | PMC13438251 | Fludrocortisone for low blood pressure causing low potassium | Medium: prescribing cascade | Overlaps Edith's postural theme |
| 7 | PMC12522493 | Hydralazine-induced diarrhea; deprescribing | High: prescribing cascade, unglamorous | Good mild case |
| 8 | PMC13418649 | Serotonin and anticholinergic toxicity in a 95-year-old | Medium: delirium, polypharmacy | Acute; would need softening for primary care |
| 9 | PMC12954340 | Minor falls overlooked: vertebral fractures | High: falls taken lightly | Image-led diagnosis; keep the arc, drop the imaging |
| 10 | PMC12101221 | Multifactorial intervention for ageing in place | High | A possible nearly clean case |

Not picked: surgery and anaesthesia reports, rare diagnoses (autoimmune encephalitis, late
cystic fibrosis, neurosyphilis), oncology and skin reactions.
