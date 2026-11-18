# Writing "Quantification and statistical analysis"

How to write this STAR Methods section and keep it in agreement with the legends.

## 1. What cell.md says — Cell rule

- STAR Methods is required at revision and for acceptance, not at first submission (cell.md §1, §8).
- It is part of the main article. Methods never go in the supplement (cell.md §7, §8).
- STAR Methods text does not count toward the 7,000-word limit (cell.md §2).
- The section headings are: Key resources table · Experimental model and study participant details · Method details · Quantification and statistical analysis · Additional resources (optional). cell.md takes these from the author guide and did **not** re-read it on 2026-11-18. Confirm the headings in the STAR Methods author guide PDF.
- AI used in the research itself is reported in STAR Methods (cell.md §3).

What this section must contain is **not specified in cell.md — check cell.com** (STAR Methods author guide). Everything below is craft guidance (not a journal rule).

## 2. Division of labour with the legends

| Legend (Cell rule, cell.md §4) | Quantification and statistical analysis (craft) |
|---|---|
| Test name and panels | Why that test; assumptions; model formula |
| p value per asterisk | Threshold, sidedness, correction method and family |
| n biological and technical, per result | Definition of a biological and a technical replicate for each assay |
| Measure and error bar | How the measure was computed from raw data |
| — | Exclusions, randomization, blinding, sample-size rationale |
| — | Software, version, packages, key parameters |

The legend says **what** was done for each panel. This section says **how and why**, once, for the paper. Neither may contradict the other.

## 3. Suggested structure

Use short subheadings. One subsection per analysis family rather than per figure.

1. **General statement.** Replicate definitions, summary measure conventions, significance threshold, sidedness, software.
2. **Sample size, randomization, blinding, exclusions.** State what was done. If nothing was done, say so plainly ("No statistical method was used to predetermine sample size").
3. **Quantification of each assay.** How raw output became the plotted number: image segmentation and thresholds, gating, normalization, what was averaged over what.
4. **Statistical tests for standard comparisons.** Test, variant, correction, the figures they serve.
5. **Models for nested or repeated data.** Fixed and random effects, the unit of the random effect, how p values were obtained.
6. **High-dimensional analyses.** Differential testing model, covariates, multiple-testing method, thresholds (see `omics-and-spatial.md`).
7. **Survival or clinical association**, if present: cohort definition, cut-point rule, covariates.

## 4. Sentence patterns

Fill only with facts the authors supply. Brackets are author input.

```text
Statistical details of each experiment, including the test used, the value and meaning
of n, and the definition of center and dispersion, are given in the figure legends.

A biological replicate is [one animal / one independent culture started from a separate
vial on a separate day]. Technical replicates ([n] wells per condition) were averaged
before analysis.

For measurements on single cells, values were [averaged per animal / analyzed with a
linear mixed model with animal as a random effect], so that n is the number of animals.

Comparisons among more than two groups used [one-way ANOVA with Dunnett's test against
the control group]. p values from [N] comparisons were adjusted by the [Holm] method.

[N] samples were excluded because [criterion fixed before analysis]. Investigators were
[blinded / not blinded] to group during [step].

Analyses were run in [software, version] with [packages, versions].
```

Do not paste the first pattern alone. A section that only says "see legends" explains nothing.

## 5. Agreement audit: legends versus this section

Build a table and resolve every mismatch before submission.

| Figure panel | Test in legend | Test in this section | n and unit in legend | Unit defined here | Correction | Match? |
|---|---|---|---|---|---|---|
| 2B | Welch's t test | Welch's t test | 6 mice | animal | none (single comparison) | yes |
| 2C | mixed model | not described | 1,240 cells / 5 mice | animal | — | **no: add model** |

Typical mismatches:

- The legend says "Student's t test"; this section says "non-parametric tests were used throughout".
- The legend gives SEM; this section says data are mean ± SD.
- A test named in this section is used in no figure (left over from an earlier version).
- A panel added in revision has a test that this section never mentions.
- Software in this section is missing from the key resources table, or the reverse.
- The threshold here is "adjusted p < 0.05"; the figure shows unadjusted asterisks.

## 6. Stage notes

- First submission: the section may sit in a conventional Methods part. Flag missing items as "needed at revision".
- Revision: required in STAR Methods format. Re-run the agreement audit after every new panel.
- Word count: this section is outside the 7,000-word main-text limit (cell.md §2), but legends are inside it. Move explanation from legends to here; keep the required legend items in the legend.
