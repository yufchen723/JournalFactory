# Statistics for single-cell, spatial and other nested omics data

All of this file is **craft guidance (not a journal rule)**. cell.md says nothing specific about single-cell or spatial statistics. The only Cell rules that touch it are the legend requirements (cell.md §4): test, asterisk meaning, biological and technical n, measures and error bars.

## 1. The core problem: the measured unit is not the replicate unit

| Level | Example | Independent? |
|---|---|---|
| Biological unit | patient, animal, donor | yes |
| Sample | tumor region, tissue block, section | partly: sections from one patient are correlated |
| Measured unit | cell, nucleus, spot, pixel, bin, field of view | no: nested in the sample |

Cells or spots from one sample share genetics, processing, batch and tissue context. Treating 50,000 spots as n = 50,000 makes almost any difference "significant". This is pseudoreplication.

Test for it with one question: **if the whole experiment were repeated, what would be new?** New patients. Not new spots from the same section.

## 2. Two sound routes

### A. Aggregate to the biological unit

- Compute one value per sample (mean, median, fraction, pseudobulk count) and test across samples.
- Simple, transparent, robust. n is the number of samples.
- Loses within-sample information; needs enough samples (with 3 versus 3, only large effects are detectable — say so).
- For differential expression: sum counts per sample and cell type (pseudobulk), then use a count model built for bulk data.

### B. Model the hierarchy

- Mixed-effects model with the biological unit as a random effect (and section within patient where relevant).
- Keeps cell-level resolution and unequal cell numbers.
- State the formula, the random-effect structure, the software, and how p values were derived.
- A random effect does not rescue a design where condition is confounded with a single sample per group.

Pick one route per analysis and state it in the legend ("statistics on per-patient means") and in "Quantification and statistical analysis".

## 3. Reporting n for nested data

Give all levels, and name the one that was tested.

```text
n = 48,210 spots from 12 sections of 6 patients; test on per-patient means (n = 6).
```

- Never give only the sub-unit count. `scripts/legend_stats_check.py` flags this.
- Paired designs (two regions from the same patient): say so and use a paired test or a patient random effect.
- Several sections per patient: say whether they were averaged or modelled.

## 4. Spatial autocorrelation

Neighbouring spots or pixels are more alike than distant ones, even within one section. Consequences:

- Standard tests on spots overstate significance twice: once for nesting in the sample, once for spatial dependence.
- Correlation between two spatial maps (gene A versus gene B across spots) is inflated by shared smooth gradients. Use a null that preserves spatial structure (for example spatially constrained permutation, or random shifts and rotations within the tissue mask), or test across samples.
- Co-localization and neighbourhood enrichment need a stated null: what was permuted, within what region, how many times, and whether tissue boundaries were respected.
- Statistics such as Moran's I or Geary's C describe autocorrelation in one sample. A cohort-level claim still needs replication across samples.
- Distance-to-feature analyses (distance to a boundary or a structure): compare per-sample summaries, or model with sample as random effect. Report how the feature was annotated and by whom.
- Smoothing, imputation or enhancement increases autocorrelation. Report whether statistics used raw or smoothed values.

## 5. Circular analysis (double dipping)

- Clusters defined from expression, then tested for differential expression between those clusters on the same data: the p values are not valid tests. Present markers as descriptive, or validate in held-out samples or by an orthogonal method.
- Regions selected because they look different, then tested for that difference: same problem.
- Thresholds or resolution parameters tuned until the result is significant: report how parameters were fixed.

## 6. Multiple testing across features

| Family | What to report |
|---|---|
| Genes, peaks, proteins | model, covariates, FDR method, threshold, number of features tested after filtering |
| Gene sets or motifs | the database and version, background set, FDR across sets |
| Regions or niches × features | the full grid is the family; say how many tests |
| Ligand–receptor pairs × cell-type pairs | the family is very large; report the null and the adjustment |
| Many resolutions, clusterings or seeds | report stability across them, not the best one |

- Filtering before testing must not use the test outcome.
- Report effect size next to the adjusted p value (log fold change, difference in fraction). With many cells, tiny effects reach any threshold.
- State whether thresholds are on raw or adjusted values, in every legend that shows them.

## 7. Composition and deconvolution

- Cell-type fractions sum to one. A rise in one type forces a fall in others. Use a compositional method or interpret with care.
- Deconvolved proportions carry method error. Do not treat them as counts. Report the reference used and any validation.
- Label-transfer or classifier-based annotations: report the confidence threshold and the fraction left unassigned.

## 8. Batch and confounding

- If condition and batch (run, slide, chip, day) are aligned, the effect cannot be separated. Say so in "Limitations of the study" rather than correcting it away.
- State the integration or correction method and whether statistics were computed before or after it.

## 9. Minimum statement in "Quantification and statistical analysis"

1. The replicate unit for cohort-level claims.
2. Route A or B for each analysis family.
3. The spatial null, if any spatial statistic is used.
4. The multiple-testing family and method.
5. Which analyses are descriptive and carry no inferential p value.
