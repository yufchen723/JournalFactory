# Example: a revision with one central experiment, one narrowed claim, one infeasible request

*Adapted in structure from nature-skills (nature-response/examples/), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

Synthetic example. The biology is invented and generic ("factor X", "cell type A"). It shows the shape of the output, not content to reuse.

## Input

```text
Editor: We invite a revised manuscript. It will be essential to establish that
factor X is required for the expansion of cell type A (Reviewer 1, point 1).

Reviewer 1
1. The conclusion that factor X drives expansion of cell type A rests on a
   correlation across samples. A loss-of-function experiment is needed.
2. In Figure 2, n is given as the number of cells. How many animals were used?

Reviewer 2
1. The authors should confirm the finding in a second, independent patient cohort.
2. Figure 4C has no scale bar.

Author notes
- Knockdown of factor X done with two guides in the organoid model; cell type A
  fraction fell from 31% to 12% and 14%; 4 independent experiments. New Figure 3E, F.
- Figure 2: 5 animals per group. Re-tested on per-animal means; still p = 0.008.
- No second cohort exists. A public dataset with 40 samples has factor X
  expression and cell type A scores; association holds (rho = 0.52).
- Scale bar added.
- Former Figure 4 is now Figure 5 because a new Figure 4 was inserted.
```

## Revision plan (excerpt)

| ID | Comment | Cat. | Sev. | Action | Evidence | Where in manuscript | Status | Blocks? |
|---|---|---|---|---|---|---|---|---|
| E.1 | X required for expansion of A | MECH | S1 | NEW_EXPERIMENT | knockdown, 2 guides, 4 experiments | Figure 3E, F; Results; STAR Methods | DONE_REPORTED | yes |
| R1.1 | correlation only | CLAIM | S1 | NEW_EXPERIMENT + TEXT_NARROW | as E.1; "drives" → "is required for" in the organoid model | title, Summary, Results | DONE_REPORTED | yes |
| R1.2 | n in cells | STAT | S2 | STATS_FIX | per-animal means, n = 5 | Figure 2 legend; Quantification and statistical analysis | DONE_REPORTED | yes |
| R2.1 | second cohort | GEN | S2 | NOT_FEASIBLE + NEW_ANALYSIS + LIMITATION | public dataset, n = 40 | Figure S6; Limitations of the study | DONE_REPORTED | no |
| R2.2 | scale bar | PRES | S4 | FIGURE_EDIT | — | Figure 5C | DONE_REPORTED | no |

Side effects entered: new Figure S6 needs "related to Figure 4" and "See also Figure S6" in the Figure 4 legend; renumbering Figure 4 → 5; recount words (two new legends).

## Point-by-point response (excerpt)

```markdown
## Reviewer 1

### Comment R1.1

> The conclusion that factor X drives expansion of cell type A rests on a
> correlation across samples. A loss-of-function experiment is needed.

**Response:** We agree and performed this experiment. Knockdown of factor X with two
independent guides reduced the fraction of cell type A in the organoid model from 31% to
12% and 14% (n = 4 independent experiments; Figure 3E and F). The data now support a
requirement for factor X in this model. They do not show that factor X is sufficient, and
we have replaced "drives" with "is required for" throughout.

**Changes in the manuscript:** Results, "Factor X is required for expansion of cell type A",
paragraphs 3-4; Figure 3E, F (new); STAR Methods, Method details, "Knockdown of factor X";
title and Summary reworded.

### Comment R1.2

> In Figure 2, n is given as the number of cells. How many animals were used?

**Response:** Five animals per group were used. We agree that the animal is the
appropriate unit. We repeated the test on per-animal means; the difference remains
(p = 0.008, Welch's t test, n = 5 animals per group). The legend now gives both the
number of cells and the number of animals and states which was tested.

**Changes in the manuscript:** Figure 2 legend; STAR Methods, Quantification and
statistical analysis, paragraph 2.

## Reviewer 2

### Comment R2.1

> The authors should confirm the finding in a second, independent patient cohort.

**Response:** We do not have access to a second cohort with matched tissue. To address
the concern about generality, we analyzed a public dataset of 40 samples, in which
factor X expression is associated with the cell type A score (Spearman's rho = 0.52;
Figure S6). This supports the association but is not a replication of the tissue
analysis, and we now say so.

**Changes in the manuscript:** Figure S6 (new), related to Figure 4; Results,
"Factor X marks cell type A across patients", last paragraph; Discussion, Limitations of
the study, sentence 2.

### Comment R2.2

> Figure 4C has no scale bar.

**Response:** Corrected. This panel is now Figure 5C.

**Changes in the manuscript:** Figure 5C.
```

## Cover-letter points

- E.1 answered with the knockdown (Figure 3E, F).
- For the editor's attention: no second cohort (R2.1); a public dataset is used instead and the limit is stated.
- Counts after revision: `AUTHOR_INPUT_NEEDED` (words including main legends; display items).

## What the example shows

- The S1 item is met with data and a narrowed verb, not with argument.
- The statistics item changes the legend and "Quantification and statistical analysis" together (**Cell rule** for the legend content, cell.md §4).
- The infeasible request gets a constraint, a substitute, and a limitation.
- The reviewer's "Figure 4C" stays in the quote; the authors' text uses the new number.
- Status stays `DONE_REPORTED` until the locations are seen in the revised manuscript. Package readiness: `draft_complete_unverified`.
- No "we will".
