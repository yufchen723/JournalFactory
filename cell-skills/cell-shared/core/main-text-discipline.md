# Main-Text Discipline for a Cell Article

Adapted in structure from nature-skills (nature-shared/core/main-text-discipline.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

Use this file when the main text must fit Cell's length limit, when deciding where a result or a
detail lives, and after every revision round that added text.

## 1. Cell rules

| Rule | Source |
|---|---|
| Research article (also Resource, Theory, Matters Arising): main text **under 7,000 words** | cell.md §2 |
| The count **includes main figure legends** | cell.md §2 |
| The count **excludes** STAR Methods text, supplemental item legends and references | cell.md §2 |
| No more than **7** figures and/or tables | cell.md §2 |
| Short article: ≤ 4,000 words counting title, authors, affiliations, summary and legends; ≤ 4 display items; ≤ 4 supplemental figures; ≤ 8 supplemental items | cell.md §2 |
| Methods never go in the supplement; they belong in STAR Methods | cell.md §7 |
| Recommended ≤ 20 supplemental figures; combine related items | cell.md §7 |
| Legends must carry test, asterisk meaning, replicates, measure and error-bar definition, scale bars, "See also" | cell.md §4 |

Not specified by Cell (see cell.md): for a research article, whether the title, Summary,
keywords, Resource availability, acknowledgments, author contributions, declarations and main
table titles count toward 7,000; and the counting method. The checker counts
Introduction + Results + Discussion + main figure legends and prints the Summary separately.
If the total is within about 200 words of the limit, ask the editor or cut.

Everything below is craft guidance (not a journal rule).

## 2. A working budget

Fix the budget before drafting. Adjust the split, not the total. Aim for 6,700 so later edits fit.

| Part | Words | Note |
|---|---|---|
| Introduction | 500–800 | no subheadings |
| Results | 3,600–4,200 | about 500–600 per display item |
| Discussion with Limitations of the study | 900–1,200 | limitations 80–150 |
| Main figure legends | 1,000–1,500 | 150–220 per figure; legends are inside the limit |
| Total | < 7,000 | |

Legends are the hidden cost. Seven legends at 300 words each use 30% of the paper.

## 3. Classify every result before placing it

| Class | Test | Destination |
|---|---|---|
| Core finding | Advances the central claim | Main text + main figure |
| Necessary support | The reader must see it to accept a core finding (key control, specificity) | Main figure panel, one clause in the text |
| Qualification | Bounds or changes how the claim is read | Main text, and "Limitations of the study" if unresolved |
| Robustness | Same conclusion under another condition, reagent, replicate cohort, threshold | Figure S, cited with "See also Figure S…" or one parenthetical callout |
| Validation of tools | Knockdown efficiency, antibody specificity, gating, quality control | Figure S; procedure in STAR Methods |
| Extended data | Full gene lists, all clusters, screens, full gels | Table S (Excel if longer than 3 pages), Data S, Figure S |
| Procedure | How it was done | STAR Methods, never the supplement |
| Statistics detail | Test, n, exact p, error definition | Legend (required) + Quantification and statistical analysis in STAR Methods |

Classify by function in this paper. A control can be the core finding of one paper and a
supplemental panel in another.

Do not use placement to hide a result. If an observation changes the direction, size or scope of
the central conclusion, it stays in the main text.

## 4. What moves where

| Found in Results | Move to |
|---|---|
| Reagent names, concentrations, time courses, instrument settings | STAR Methods (Method details); reagents in the key resources table |
| "Cells were transfected with … and after 48 h …" | STAR Methods; keep "after depletion of factor X" |
| Test names, exact p values, n per group | Legend; text keeps direction and effect size |
| Description of how to read a plot | Legend |
| A second system showing the same thing | Figure S + "See also Figure S2" in the legend |
| Full list of hits or differentially expressed genes | Table S |
| Analysis parameters and software versions | STAR Methods + key resources table |
| Explanation written to answer a reviewer | Response letter; keep one clause if a reader needs it |

| Found in a legend | Move to |
|---|---|
| Interpretation ("showing that factor X is required") | Results text |
| Protocol detail beyond what identifies the panel | STAR Methods |
| Repeated statistics sentence in every panel | One closing sentence for the figure |

## 5. How to compress, in order of yield

1. **Cut a claim step.** If the paper has more claim steps than display items, one subsection is
   support. Demote it to a Figure S and one sentence.
2. **Cut the recap.** Delete Discussion sentences that restate Results. Delete Results openings
   that restate the previous subsection.
3. **Cut method from Results.** One clause of approach per experiment.
4. **Cut legend prose.** Title, then panels as noun phrases; one statistics sentence; one
   "See also". No methods narrative.
5. **Cut background.** Introduction facts not used later.
6. **Cut sentence-level padding.** "It is important to note that", "Interestingly", "In order to",
   "As shown in Figure 1A, we found that" → "(Figure 1A)".
7. **Merge callouts.** "Figures 2A and 2B" in one sentence, not two sentences.

Do not compress by removing: the model system, the n and test in legends, limits of a claim, or
the "Limitations of the study" subsection.

## 6. Prevent revision growth

Each added sentence triggers a deletion check on the same paragraph:

1. Name the job of the new sentence.
2. Find the sentence that already does that job. Replace it; do not append.
3. Recount the section and update the budget table.

For reviewer-driven text ask: does this tell the reader what was found, or tell a reviewer why an
objection fails? The second kind goes in the response letter, with at most one clause in the paper.

## 7. Paragraph necessity test

For every Results paragraph answer in one line:

- Which claim step does it serve?
- What can the reader not conclude without it?
- Is its result shown in a main figure?

Two "no" answers: move to the supplement or delete.

## 8. Compression record

When asked to shorten, return the text and this table.

| Section | Before | After | What moved | Where |
|---|---|---|---|---|
| Results 3 | 720 | 540 | dose controls | Figure S3, legend "See also" |

State the counting method used and that Cell does not specify one (see cell.md).
Run `../../cell-writing/scripts/cell_text_check.py` for the total.
