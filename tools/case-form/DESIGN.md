# Case-writing form: design plan

Scope: one internal screen, used by one author. Not the product's design system.

## Brief

- **Audience and job.** The clinical lead, a clinician writing a fictional case in 15-minute gaps between
  shifts. The form must get a complete, gradable case out of their head without losing work.
- **Mechanism.** A blank one-page template becomes a guided case, section by section, with a
  finished example beside every answer and checks that catch what the validator would reject.
- **Proof.** Edith Marsh, the dev case, shown in every section in the form's own shape.
- **Metaphor.** A case notebook with the worked example written in the margin.

## Plan

1. **Point of view.** Quiet, paper-like and fast, for a tired clinician at the end of a shift;
   nothing to learn, nothing lost.
2. **The one bold move.** Edith sits in the margin of every section, typeset like a case note,
   so the example is read beside the field, not looked up elsewhere. On a phone the margin folds
   into a "See Edith's" toggle under the section's hint.
3. **Type.** Display and margin notes: the system's book serif (Iowan Old Style, Charter,
   Georgia), because the margin should read like a written note. Fields and labels: the system
   UI face, chosen for legibility in inputs. Three sizes: 24 / 15 / 13 px. No network fonts:
   the form works offline and sends nothing anywhere.
4. **Palette (light only; one mode designed).**
   `--paper #f6f5f0` canvas, `--ink #1c1f1e` text, `--muted #575d59` hints (6.2:1 on paper),
   `--line #d8d4c8` rules, `--surface #ffffff` fields, `--field-line #8c8a80` field borders (3.2:1 on paper), `--accent #1d5c58` focus, links and
   the primary button (under 10%), `--warn #8f3518` check failures.
5. **Imagery.** None. The example text is the imagery.
6. **Layout.** Left rail of section links with a status dot; main column of sections, each a
   two-column spread (fields 3fr, margin 2fr) with a rule between. Under 1000 px the rail
   becomes a top strip and the margin folds under the hint. Section order follows the case
   template, ending with checks and export.
7. **Motion.** None beyond instant state changes. A "Copied" / "Saved" text change confirms
   actions. Nothing animates.
8. **Also on the page.** Header actions (Open a draft, Load Edith, New case, Checks and export)
   and a privacy reminder with a warn-coloured rule above the export: cases must be fictional.
9. **References.** None taken; the technique (marginal worked example) comes from textbooks,
   not a site.
