# Title

Adapted in structure from nature-skills (nature-writing/static/fragments/section/title.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

## Cell rules (source: cell.md §3)

| Rule | Value |
|---|---|
| Length | about 10–12 words |
| Hard limit | ≤ 145 characters with spaces |
| Vocabulary | no jargon or uncommon abbreviations; abbreviations avoided in the title |
| Content | conveys the broad conceptual significance |
| Novelty words | "novel" and "first" discouraged |
| Spelling | US |

Not specified by Cell (see cell.md): declarative versus descriptive form, use of a colon or a
question, naming the model organism, a short or running title.

## Counting method

- Characters: every character including spaces, after removing markup (italics markers).
- Words: whitespace-separated tokens; a hyphenated compound counts as one.
- `cell_text_check.py` reports both. More than 145 characters is a FAIL; the word count is
  reported against "about 10–12" and warned only when clearly above it.

## How to build it (craft guidance, not a journal rule)

1. Start from the one-sentence argument (`../static/core/workflow.md` step 1).
2. Keep the actor, the action and the biological consequence. Drop the method.
3. Use a verb. A title that states a finding needs one.
4. Replace lab names and abbreviations with what the thing is ("a secreted damage signal").
5. Name the biological question a non-specialist cares about, not the assay.
6. Count. If over 12 words, cut modifiers first, then the system, then the mechanism detail.

Three workable forms:

| Form | Pattern | Example (invented) | Words / characters |
|---|---|---|---|
| Finding | [Actor] [verb] [consequence] | Factor X released by dying cells scales stem cell activation to tissue damage | 13 / 77 |
| Concept | [Concept] [verb] [biological outcome] | A dose-dependent damage signal matches stem cell output to tissue need | 11 / 70 |
| Mechanism | [Process] through [mechanism] | Dying cells set the scale of tissue repair through a dose-dependent signal to stem cells | 15 / 88 (trim) |

Choose the concept form when the named factor is unfamiliar to most readers; choose the finding
form when the actor is the news.

## Repairs

| Draft | Problem | Repair |
|---|---|---|
| A novel role for the FX-RY axis in ISC activation: insights from single-cell and lineage-tracing analyses in the irradiated mouse small intestine (22 words, 145 characters) | "novel"; three abbreviations; method list; twice the word guide | A dose-dependent damage signal matches stem cell output to tissue need |
| Analysis of factor X function in intestinal stem cells | Topic, no finding | Factor X sets how many intestinal stem cells divide after injury |
| How do stem cells sense tissue damage? | Question hides the answer | State the answer |
| Factor X is the first damage sensor in the gut | "first" is discouraged and hard to verify | Factor X senses epithelial damage in the gut |

## Alignment (craft guidance)

- The title's claim equals the Summary's central sentence, at the same or lower strength.
- Title terms are ledger terms and appear in the Summary and Introduction.
- The title does not promise generality (all tissues, all species) that the limitations
  subsection withdraws.
- Keywords (up to 10, comma separated; cell.md §3) add search terms the title lacks; do not
  repeat title words only.

## Deliverable

Offer three candidates, each with word and character counts, and name the preferred one with a
one-line reason. State any abbreviation that was kept and why it counts as common.
