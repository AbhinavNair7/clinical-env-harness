# Attribution

clinical-env cases are fictional. Some development cases are built on the clinical arc of
published case reports and on aggregate record patterns from open demo datasets. No sentence
of any source is reused (checked by `clinical-env sources check`), and no patient-level data
from any dataset appears in the repository.

## Case reports (CC BY 4.0)

- Bhutani P, Tanwar B, Choudhary N, Singh A, Dhar M. Functional and Cognitive Decline in an
  Older Adult With Severe Hyponatremia and Undiagnosed Hypothyroidism: A Geriatric Perspective.
  Cureus. 2026. doi:10.7759/cureus.100682. PMC12863219. Licence: CC BY 4.0
  (https://creativecommons.org/licenses/by/4.0/).
- Kobayashi K, Hamai A, Ando T. Overlooked Carbamazepine Toxicity: A Diagnostic Pitfall in an
  Elderly Patient With Dizziness. Cureus. 2025. doi:10.7759/cureus.78802. PMC11897834. Licence:
  CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).

- Alam F, Amin S, Omer E, Nasser N, Alam MA. Rapid Deterioration of Glycaemic Control Revealing
  Interval Metastatic Pancreatic Cancer Despite a Recent Normal CT Scan. Cureus. 2026.
  doi:10.7759/cureus.115088. PMC13600037. Licence: CC BY 4.0.
- Tanaka T, Fujiwara R, Sashida R, et al. Surgical Treatment of Vertebral Compression Fracture
  in a Patient with Idiopathic Normal Pressure Hydrocephalus. JMA Journal. 2023.
  doi:10.31662/jmaj.2023-0005. PMC10407305. Licence: CC BY 4.0.
- Baik J, McGuire S, Hughes N, Tariq T. Nonsteroidal Anti-inflammatory Drug (NSAID)-Induced
  Enteropathy Mimicking Crohn's Disease: A Reversible Cause of Ileitis. Cureus. 2026.
  doi:10.7759/cureus.108296. PMC13235628. Licence: CC BY 4.0.
- Sumya UM, Hamid T. Severe Malnutrition Revealing Psychotic Depression in an Elderly Patient
  Successfully Treated With Electroconvulsive Therapy: A Case Report. Cureus. 2026.
  doi:10.7759/cureus.116940. PMC13696058. Licence: CC BY 4.0.
- Ansari A, Sookai V, Gossen I, Matta S, Mahmudul H, Lazarescu R. Rethinking Care: Early
  Palliative Support for Advanced Heart Failure. Cureus. 2025. doi:10.7759/cureus.82106.
  PMC12066164. Licence: CC BY 4.0.
- Stefansdottir OA, Kaas MJ, Sudmann T. Second Partnership and Dementia Care in a Blended Family:
  Case Study of a Wicked Problem. Int J Environ Res Public Health. 2024.
  doi:10.3390/ijerph21091213. PMC11431802. Licence: CC BY 4.0.

## Papers (CC BY 4.0)

- `docs/papers/residencyrl-2608.07418.pdf`: ResidencyRL, arXiv:2608.07418 (2026), included
  unmodified under CC BY 4.0. Sections 3.1–3.3 informed the simulator and grader design.

Which case uses which source is recorded internally (`sources/provenance/`). Candidate metadata
and licence decisions: `sources/licence_log.csv`.

## Datasets (ODbL v1.0)

`docs/record-patterns.md` contains information from the MIMIC-IV Clinical Database Demo and
the MIMIC-IV-ED Demo, which are made available under the Open Database License (ODbL v1.0,
https://opendatacommons.org/licenses/odbl/1-0/). Only aggregate counts are used. The raw data
is downloaded locally into `mimic/` (gitignored) and never committed or shipped.

- Johnson A, Bulgarelli L, Pollard T, Horng S, Celi LA, Mark R. MIMIC-IV Clinical Database
  Demo (version 2.2). PhysioNet. 2023. doi:10.13026/dp1f-ex47.
- Johnson A, Bulgarelli L, Pollard T, Celi LA, Horng S, Mark R. MIMIC-IV-ED Demo (version 2.2).
  PhysioNet. 2023. doi:10.13026/jzz5-vs76.
- Goldberger A, Amaral L, Glass L, Hausdorff J, Ivanov PC, Mark R, et al. PhysioBank,
  PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic
  signals. Circulation. 2000;101(23):e215-e220.

To reproduce: download `https://physionet.org/content/mimic-iv-demo/get-zip/2.2/` and
`https://physionet.org/content/mimic-iv-ed-demo/get-zip/2.2/`, unzip both into `mimic/raw/`,
then run `uv run clinical-env sources mimic mimic/raw`.
