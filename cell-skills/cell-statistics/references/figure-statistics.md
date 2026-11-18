# Figure-legend statistics

*Adapted in structure from nature-skills (nature-statistics/references/figure-statistics.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

## 1. What a Cell legend must state — Cell rule (cell.md §4)

Applies to main and supplemental legends. Required at revision and for final files; a first submission is free format (cell.md §1).

| Item | Cell's wording or example |
|---|---|
| Statistical test(s) and the panels they apply to | "*p < 0.05, **p < 0.01 by Student's t test (A, F, and H) or by two-way ANOVA (K and L)" |
| The p value each asterisk stands for | same example |
| Number of biological and technical replicates for each result | — |
| What every measure and error bar is | "Data are represented as mean ± SEM" |
| Every scale bar (in the image or in the legend) | — |
| Related supplemental items | "See also Figure S1" |

Also from cell.md:

- The legend starts with a brief title for the whole figure, then describes each panel (§4).
- Panel labels are capital letters (§5).
- Supplemental figure titles end "related to Figure N" (§7).
- Recommended: individual data points in addition to mean ± error (§5).
- Titles and legends sit in the manuscript, never inside the image file (§4).

## 2. How to write it — craft guidance (not a journal rule)

Put shared statistics in one closing block; put panel-specific n in the panel sentence.

```text
Figure 2. Factor X is required for expansion of cell type A
(A) Experimental scheme.
(B) Fraction of cell type A in control and knockout mice (n = 6 mice per group;
    each dot is one mouse, mean of 2 technical replicates).
(C) Signal per cell (n = 1,240 cells from 5 mice per group; statistics on per-mouse means).
Data are represented as mean ± SEM. *p < 0.05, **p < 0.01 by two-tailed Welch's t test (B)
or linear mixed model with mouse as random effect (C). ns, not significant.
See also Figure S2 and Table S1.
```

Checks for each panel:

- **n has a unit.** "n = 6" is incomplete; "n = 6 mice" is complete.
- **n is the replicate unit.** If the legend gives cells, spots or fields, it also gives the animals, patients or independent experiments they came from, and says which level was tested.
- **Biological and technical are both stated** where both exist. If there were no technical replicates, say what one data point is.
- **Each dot is defined.** One animal, one cell, one field, one experiment.
- **Every asterisk level in the image has a key**, and the key has no level that the image does not use.
- **"ns" is defined** if it appears.
- **The test names the variant**: paired or unpaired, one- or two-sided, the post-hoc test, the correction.
- **Adjusted values are labelled** as adjusted.
- **Representative images** say how many biological replicates showed the same result.

## 3. Plot elements that need a definition — craft guidance

| Element | State |
|---|---|
| Bar or dot with error bar | centre (mean, median) and spread (SD, SEM, 95% CI) |
| Box plot | centre line, box limits, whisker rule, whether outliers are shown |
| Violin plot | what the inner marks are; n per group; kernel settings only if they matter |
| Line with shaded band | line (mean, fit) and band (SEM, CI) |
| Heatmap | value shown (z-score per row, log fold change), scale limits, clustering method |
| Dot plot (expression) | what dot size and colour encode |
| Survival curve | censoring marks, numbers at risk if space allows, test |
| Scatter with fit | model, coefficient, interval, n |

## 4. Consistency checks — craft guidance

- The n in the legend equals the number of points visible in the panel.
- The test in the legend is the test described in "Quantification and statistical analysis".
- The Results text quotes the same statistic as the legend.
- A panel moved to the supplement takes its statistics with it; the main legend's panel letters in the test sentence are updated.
- Supplemental legends meet the same standard as main legends (**Cell rule**, cell.md §4).

## 5. Common legend failures

- Asterisks in the image, no key in the legend.
- "Error bars are shown" without saying what they are.
- "n = 3" with no unit, or with three wells of one experiment.
- "n = 5,000 cells" with a p value computed on cells.
- "Student's t test" for more than two groups.
- One sentence "Statistics as in Figure 1" in a later legend. Each legend must stand alone.
- "See also" missing although a supplemental figure is "related to" this figure.

## 6. Tool

```bash
python scripts/legend_stats_check.py legends.md
```

It flags, per legend: no test name, no asterisk key, undefined "ns", no n, n in cells/spots/fields only, no measure or error-bar definition, no "See also" (main) or "related to Figure N" (supplemental), and images without a scale-bar statement. WARN items map to cell.md §4 and §7; the "n in sub-units only" warning is craft guidance. It reads text only.
