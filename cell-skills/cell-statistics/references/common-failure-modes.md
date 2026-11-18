# Common statistical failure modes

*Adapted in structure from nature-skills (nature-statistics/references/common-failure-modes.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

**Craft guidance (not a journal rule)** unless marked. Each entry: how to spot it, why it matters, the fix.

## 1. Pseudoreplication

- **Spot it**: n in the hundreds or thousands for a bench experiment; n given in cells, fields, spots; very small p values with few animals.
- **Why**: sub-units share a source; the test assumes they do not.
- **Fix**: aggregate per biological unit, or use a mixed model. Report both levels of n. See `omics-and-spatial.md`.

## 2. Technical replicates counted as n

- **Spot it**: "n = 3" with one experiment; triplicate wells; repeat injections of one sample.
- **Fix**: average within the biological replicate. **Cell rule (cell.md §4)**: the legend states biological and technical replicates separately.

## 3. Many comparisons, no correction

- **Spot it**: a t test at each time point or dose; all-pairs comparisons with one test name; a panel with ten asterisks.
- **Fix**: one model across groups with a named post-hoc test, or an explicit correction. State the family.

## 4. Wrong test for the design

- t test for more than two groups.
- Unpaired test for paired samples (same animal before and after; two regions of one tissue).
- Parametric test on bounded or heavily skewed data with n = 3.
- Repeated measures analysed as independent groups.
- **Fix**: match test to design (table in `statistical-reporting.md`).

## 5. "Significant here, not significant there"

- **Spot it**: a conclusion that an effect is specific to one condition because p < 0.05 in that condition and p > 0.05 in another.
- **Fix**: test the difference between the effects directly (interaction term).

## 6. Undefined error bars and measures

- **Spot it**: bars with whiskers and no definition; SEM in one figure and SD in the next without saying so.
- **Fix**: **Cell rule (cell.md §4)**: define every measure and error bar in the legend.

## 7. Bars that hide the data

- **Spot it**: bar charts with n of 3 to 6 and no points.
- **Fix**: show the points. **Cell rule (cell.md §5)**: individual data points are recommended in addition to mean ± error.

## 8. Significance used as importance

- **Spot it**: "markedly", "strongly", "dramatically" backed only by a p value; huge n and a tiny difference.
- **Fix**: report the effect size and interval; describe the size in plain numbers.

## 9. Absence of evidence read as evidence of absence

- **Spot it**: "had no effect", "was unchanged" from a non-significant test with small n.
- **Fix**: report the estimate and interval; write "we did not detect a difference".

## 10. Correlation written as mechanism

- **Spot it**: "drives", "regulates", "is required for" on a correlation or co-localization.
- **Fix**: use association wording, or add a perturbation. Put the boundary in "Limitations of the study" (**Cell rule**, cell.md §3: the subsection is required).

## 11. Selection and circularity

- Clusters or regions defined from the same data used to test them.
- Cut-points for survival chosen to minimise the p value.
- "Representative" examples chosen after seeing the outcome.
- **Fix**: predefine, cross-validate, or validate in independent samples; state the rule used.

## 12. Unreported exclusions and outliers

- **Spot it**: group sizes that differ from the stated design with no explanation.
- **Fix**: state the criterion, when it was set, and how many were removed per group.

## 13. Comparing across experiments

- **Spot it**: a control from one day against a treatment from another; a control lane reused across figures.
- **Fix**: **Cell rule (cell.md §5)**: compare only data that belong together (same experiment); the same image appears in two figures only for the same experiment, with the reason in the legend.

## 14. Normalization that removes the variance

- **Spot it**: control set to 1 with no error bar, then a one-sample or two-sample test against it.
- **Fix**: normalize within replicate to a reference that keeps control variance, or use a paired or ratio test and say so.

## 15. Legends and methods disagree

- **Spot it**: test names, error-bar types or n differ between legend, Results and STAR Methods.
- **Fix**: run the agreement audit in `quantification-and-statistical-analysis.md`.

## 16. Asterisks without a key

- **Spot it**: stars in the image, nothing in the legend; a key with levels that never appear.
- **Fix**: **Cell rule (cell.md §4)**: give the p value each asterisk stands for.

## Severity guide

| Label | Meaning |
|---|---|
| P0 | The inference behind a central claim is invalid as analysed (pseudoreplication, circular test, wrong unit) |
| P1 | A required legend item is missing (cell.md §4), or a correction or test variant is missing for a supporting claim |
| P2 | Clarity: wording, consistency, effect-size reporting |
