# Statistical reporting

*Adapted in structure from nature-skills (nature-statistics/references/statistical-reporting.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

Everything here is **craft guidance (not a journal rule)** unless a line is marked **Cell rule**.

## 1. The replicate unit

The replicate unit is the smallest thing that was independently assigned to a condition or independently sampled from the population the claim is about.

| Claim is about | Replicate unit | Not the unit |
|---|---|---|
| A genotype or treatment in animals | animal (or litter or cage when the treatment is applied to it) | cells, sections, fields from one animal |
| A patient group | patient | samples, regions, cells from one patient |
| A cell-culture perturbation | independent experiment (separate day, passage or preparation) | wells of one plate |
| A tissue feature | tissue section from a distinct individual | spots or pixels in one section |

Rules of thumb:

- Ask "what would I have to repeat to get a new, independent value?" That is the unit.
- n for a test is the number of replicate units, not the number of measurements.
- If two candidate units exist (cells within animals), report both and say which one entered the test.

## 2. Biological versus technical replicates

- **Cell rule (cell.md §4)**: the legend states the number of biological and technical replicates for each result.
- Biological replicate: an independent biological source (animal, patient, independent culture).
- Technical replicate: a repeat measurement of the same biological source (duplicate wells, repeat runs, repeat sequencing lanes).
- Technical replicates describe measurement precision. Average or model them within each biological replicate; do not add them to n.
- cell.md does not define the two terms. Define them once in "Quantification and statistical analysis" for assays where the boundary is debatable (for example organoids from one donor, clones from one line).

## 3. Choosing and naming the test

- **Cell rule (cell.md §4)**: the legend names the test(s) and the panels each applies to.
- Name the exact variant: paired or unpaired, Welch or Student, one- or two-sided, the post-hoc procedure after ANOVA.
- Match the test to the design:

| Design | Common choice |
|---|---|
| Two independent groups | Welch's t test; Mann–Whitney U when the scale is ordinal or n is small and skewed |
| Two paired conditions | paired t test; Wilcoxon signed-rank |
| More than two groups, one factor | one-way ANOVA or Kruskal–Wallis, then a named post-hoc test |
| Two factors | two-way ANOVA; report the interaction term when the claim is a difference of differences |
| Repeated measures over time | mixed-effects model or repeated-measures ANOVA, not a t test per time point |
| Nested measurements | mixed-effects model with the biological unit as random effect, or per-unit aggregation |
| Time to event | Kaplan–Meier with log-rank; Cox model with hazard ratio and interval |
| Counts or proportions | Fisher's exact or chi-square; a count model for sequencing counts |
| Association | Pearson or Spearman, with n and the interval |

- State how assumptions were checked, or why the chosen test does not need them.
- A claim that an effect differs between two conditions needs a direct test of that difference (an interaction), not "significant in one, not in the other".

## 4. Multiple testing

- Define the family: all comparisons that support one claim, or all features tested in one screen.
- Few planned comparisons: Dunnett (against one control), Tukey (all pairs), Holm or Bonferroni.
- Many features (genes, peaks, regions): control the false discovery rate and report adjusted values. Say which method and what threshold.
- State the number of tests in the family when it is not obvious.
- Do not mix raw and adjusted p values in one panel without labelling them.

## 5. Effect sizes and uncertainty

- Give the size of the effect (difference in means, fold change, hazard ratio, correlation) with an interval where possible.
- **Cell rule (cell.md §4)**: define every measure and error bar ("Data are represented as mean ± SEM").
- SD describes spread of the data; SEM and confidence intervals describe uncertainty of the estimate. Pick the one that matches the statement.
- With n below about 5, show the points. **Cell rule (cell.md §5)**: plotting individual data points in addition to mean ± error is recommended.

## 6. p values

- **Cell rule (cell.md §4)**: the legend gives the p value each asterisk stands for.
- Exact p values (p = 0.013) are more informative than thresholds. cell.md does not require them — craft guidance.
- Give very small values as an inequality (p < 0.0001) rather than a long exponent, unless the exact value matters (for example genome-wide thresholds).
- "Not significant" is not "no effect". Report the estimate and interval.
- Write "p" consistently in one typographic form across figures, legends and text.

## 7. Minimum set for every quantitative result

| Item | Where it goes |
|---|---|
| Replicate unit and n (biological, technical) | legend (Cell rule), repeated in Quantification and statistical analysis |
| Summary measure and error bar | legend (Cell rule) |
| Test, variant, panels | legend (Cell rule); detail in Quantification and statistical analysis |
| Asterisk key or exact p | legend (Cell rule for the key) |
| Multiple-testing method | legend or Quantification and statistical analysis |
| Effect size and interval | Results text or legend |
| Exclusions, randomization, blinding | Quantification and statistical analysis |
| Software and version | key resources table and Quantification and statistical analysis |

Missing facts are author questions. Never fill them in.
