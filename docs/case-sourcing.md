# Building cases on open case reports

How a case is built on a published case report so it feels true without being recognisable.
Agreed with the clinical lead on 4 Nov 2026 (DECISIONS.md). First use: 2 US dev cases
(`cases/dev/marjorie_lindqvist.yaml`, `cases/dev/harold_benning.yaml`).

## Layers

Each case blends three layers:

1. **Clinical arc** from one CC BY or CC0 case report: what went wrong, over what timeframe, how
   it was or should have been caught. It is moved into 2–3 primary care visits; a hospital stay
   becomes a discharge summary between visits.
2. **Record layer**: 2–4 patterns from `docs/record-patterns.md`, planted in the records.
3. **People layer**, invented: the patient and (only where realistic) a carer, what each
   believes, remembers wrongly or keeps back, and how they talk.

The case is written in the normal case YAML (`clinical-env validate`). Its source and what was
changed go in `sources/provenance/<case_id>.yaml`. That file is internal: it is never shown to a
model, never sits beside the case (the validator reads every YAML in a case folder) and is never
published with the case.

## Steps and commands

1. **Pull** candidates: `uv run clinical-env sources pull --limit 150`. This searches Europe PMC
   (fielded query in `sourcing/europepmc.py`, about 1 request a second with backoff), fetches
   each full-text XML into `sources/fulltext/` (not committed), decides the licence and writes
   `sources/candidates.jsonl` and `sources/licence_log.csv`. Abstracts are kept only for
   accepted articles.
2. **Screen**: the code prefilter keeps reports with a stated age of 70+ and drops paediatric,
   surgical-technique and image-led ones. An author then reads the survivors and writes
   `sources/screening.md`. Prefer common, unglamorous problems a primary care doctor could
   have caught over rare diagnoses.
3. **Draft** the case (YAML plus provenance). Use new names, places and institutions, move the
   age 2–5 years, use relative dates only, make at least 3 clinically meaningful changes
   (logged), copy no sentences, and drop any rare detail that could identify the real patient.
   Keep the criticals country-neutral (clinical actions); country-specific routes are normal
   items.
   One action per critical: the core thing a GP would be criticised for missing. Extras
   ("scheduled acetaminophen", "says it may be treatable") go in normal items. Bundling them
   made the first graded dev runs fail criticals on a detail (5 Nov).
4. **Check**:
   - `uv run clinical-env validate <case>`
   - `uv run clinical-env sources check <case>`: the licence again, zero shared runs of 8+
     words with the source, and identifiability. The source must not be in the top 10 of a
     Europe PMC search for all the distinctive details together, for every pair of them, or
     for any of them by relevance. An all-details search often finds nothing, so the pairs are
     the real test.
     A match on the theme alone is accepted (the clinical lead, 5 Nov): any case on a common theme finds
     its best-known reports. So list the clinical arc as `theme` in the provenance (for
     example "pancreatic cancer", "worsening diabetes"); pairs made only of theme terms are
     not searched, and every pair with a case-specific detail must still miss the source.
   - a self-review checklist: clinical plausibility, consistency across visits, conflicts
     resolvable inside the simulation, a fair rubric, the licence logged.
   - one visit-1 smoke run on the dev config.
5. **Review**: `cases/REVIEW.md` has one sheet per case for the clinical lead (the clinical reviewer), who
   approves, edits or rejects each one.

## Licence rule (strict)

Keep an article only if its own full-text XML (`<permissions><license>` in `<front>`) says CC BY
or CC0, read from the licence link (`xlink:href`, `ali:license_ref`) and the wording. Reject
NC, SA, ND, a missing or ambiguous licence, or one that disagrees with the search metadata.
Every decision is logged with its evidence string. Two traps were found in real data:

- Cureus gives only wording ("CC-BY 4.0"), with no link.
- BMC journals add a CC0 waiver for the data to a CC BY article. That sentence is about the
  data, not the article (`licence._without_data_waiver`).

Checked on 4 Nov against real CC BY-NC articles (rejected) and BMC case reports (accepted).

## MIMIC

`uv run clinical-env sources mimic mimic/raw` prints aggregate pattern counts from the MIMIC-IV
and MIMIC-IV-ED demo data (ODbL v1.0; download notes in `ATTRIBUTION.md`). The raw data lives in
`mimic/` (gitignored) and nothing at patient level leaves the script. Counts of 1–4 show as <5.

## Scale-up (after a Go; not built)

- Batch pulls with the same code and query variants per theme. The licence check and prefilter
  are already automatic.
- Cheap-model structured screening (age, problem, primary care fit, timeline) replaces the
  reading step for the first pass; an author reads the shortlist.
- Drafting through the Claude API from a template prompt plus the source text, the pattern
  library and a target cell. Every draft goes through the same validator, overlap and
  identifiability checks, with a retry on failure.
- A coverage matrix (theme × messiness × carer × setting) to stop themes repeating. It is
  filled before drafting and checked when a draft is accepted.
- The review queue is the limit. At about 10 cases a week, 100 cases are about 10 weeks of
  The clinical lead's time unless more reviewers join, so batch size follows reviewer time.
- The v0 spec defers automatic case generation until after the pilot. Its 10 frozen cases and
  the 10-case extension come from this same process, one case at a time.

## Known limits

- The identifiability search tests a search engine, not a model's memory. A model may still
  recognise a common teaching arc (for example amiodarone raising phenytoin). The test is about
  eliciting and reconciling, so knowing the arc does not answer what is in the pill organizer.
- Case reports are hospital-written and skew to the dramatic. The primary care texture comes
  from the record and people layers and from the clinical lead's review.
- Claude drafts the cases and Claude is one of the tested labs. The clinical lead sets the criticals, and
  OpenAI runs first in the pilot.
- CC BY attribution vs hiding the source: fine while the repo is private. Before any open pack,
  decide (a legal call) on a general attribution list with no per-case mapping.
