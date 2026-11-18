# Figure titles and legends

Structure of this file follows the nature-skills reference pattern (Apache-2.0); nature-skills has no equivalent file. Cell rules from cell-shared/journal-formats/cell.md.

## Cell rules (source: cell.md §4 unless noted)

| Rule | Detail |
|---|---|
| Title | each figure has a brief title for the whole figure; no panel citations in it |
| Title wording | re-use the Results subheading (also cell.md §3) |
| Legend | describes each panel after the title |
| Statistics | the statistical test(s) and the p value each asterisk stands for, e.g. "*p < 0.05, **p < 0.01 by Student's t test (A, F, and H) or by two-way ANOVA (K and L)" |
| Replicates | the number of biological and technical replicates for each result |
| Measures | what every measure and error bar is, e.g. "Data are represented as mean ± SEM" |
| Scale bars | every scale bar defined, in the image or in the legend; a scale bar on every microscopy image (cell.md §5) |
| Supplemental pointer | "See also Figure S1" |
| Scope | the same requirements apply to main and supplemental legends |
| Citation | all figures cited in the main text, in numerical order |
| Location | titles and legends in one "figures" section of the manuscript, never inside the image file |
| Panel labels | capital letters (cell.md §5) |
| Supplemental titles | "Figure S1. [title], related to Figure 1" (cell.md §7) |
| Length | main figure legends count toward the limit of under 7,000 words; supplemental legends do not (cell.md §2) |

Image-integrity statements that belong in a legend (cell.md §5):

- adjustments not applied to the whole image: explained in legend and methods;
- gel lanes removed or rearranged: marked in the image and stated in the legend;
- the same image used in two figures: only for the same experiment, with the reason in the legend;
- stitched images: stated in the legend.

Not specified by Cell (see cell.md): a word limit per legend; the punctuation after
"Figure 1"; how panels are introduced ("(A)"); where in the legend the statistics sentence and
"See also" sit; whether exact p values are preferred over asterisks.

## Layout used in this pack (craft guidance, not a journal rule)

```
Figure N. [Title = Results subheading; a finding; no panel letters]
(A) [What the panel shows: measurement, system, condition.]
(B) [...]
(C and D) [...]
[Replicates for each result.] [Measure and error bars.] [Tests and asterisk meanings, by panel.]
[Scale bars.] See also Figure SN.
```

Panel statistics may also sit inside each panel sentence when tests differ panel by panel. Pick
one layout and keep it across all figures.

## Worked example (invented biology)

> **Figure 2. Factor X is required for damage-scaled stem cell activation**
> (A) Representative images of dividing stem cells in control and *Fx*-deleted crypts 48 h
> after irradiation. Scale bars, 20 µm.
> (B) Dividing stem cells per crypt at the indicated doses.
> (C) Epithelial repair score over time after 12 Gy.
> n = 6 mice per group from two independent experiments; 30 crypts were counted per mouse and
> averaged (B and C). Data are represented as mean ± SEM. *p < 0.05, **p < 0.01 by two-way
> ANOVA with a multiple-comparison correction (B and C). See also Figure S2.

Supplemental legend:

> **Figure S2. A second deletion strategy confirms the requirement for factor X, related to
> Figure 2**
> (A) Dividing stem cells per crypt after inducible deletion of *Fx*. n = 4 mice per group,
> one experiment. Data are represented as mean ± SD. **p < 0.01 by Student's t test.

## The five required statements, one by one

| Statement | Complete | Incomplete |
|---|---|---|
| Test | "by two-way ANOVA (B and C) or Student's t test (D)" | "statistical significance was assessed" |
| Asterisks | "*p < 0.05, **p < 0.01, ***p < 0.001" for every symbol used in the figure | asterisks in the image, none defined |
| Replicates | "n = 6 mice per group, two independent experiments; three technical replicates per sample" | "n = 3" (three of what?) |
| Measure and error | "Bars show mean ± SEM; points are individual mice" / "Boxes show median and interquartile range" | error bars drawn, not named |
| Scale bars | "Scale bars, 50 µm (A) and 10 µm (insets)" | "Scale bar as indicated" with no value anywhere |

Biological versus technical replicates (craft wording): say what the independent unit is
(animal, donor, culture, experiment) and separately how many measurements were taken per unit.
Use the same words as the Quantification and statistical analysis section.

Cell recommends plotting individual data points in addition to mean ± error (cell.md §5); when
points are shown, say what a point is.

## Titles

- Copy the Results subheading. Shorten only when it is too long to sit above the figure.
- A finding, with a verb: "Factor X binds receptor Y on quiescent stem cells".
- No panel citations ("(A–C)") in the title (Cell rule).
- A figure that is a schematic or a study design still takes a title that states what it
  establishes or shows ("Experimental design for graded epithelial injury").

## Keeping legends short (they count toward 7,000 words)

| Cut | Keep |
|---|---|
| Interpretation ("showing that X is required") | what is plotted |
| Protocol detail beyond what identifies the panel | condition, time point, dose |
| The statistics sentence repeated per panel | one sentence with panel letters |
| "Representative" without n | "representative of n = 3 experiments" |
| Definitions already printed in the figure | abbreviations a reader meets only in the figure |

Working target: 150–220 words per main legend (craft guidance; Cell gives no number).

## Checker coverage

`cell_text_check.py` warns, per legend, when it finds no test name or p definition, no n or
replicate statement, no measure or error definition, image words without "scale bar", a main
legend without "See also", a supplemental title without "related to", or panel letters in a
title. These are text heuristics: a schematic needs no statistics, and a figure with no
supplemental support needs no "See also". Read each warning against the figure.

## Deliverable

All main legends in one section, then supplemental titles and legends, with: word count of the
main legends; a table of figure title ↔ Results subheading; and per figure a tick list
(test, asterisks, n, measure/error, scale bars, See also). Mark every missing fact as a
placeholder (`[n = ?]`, `[test?]`); never guess a test or an n.
