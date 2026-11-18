# Statistics QA checklist (reviewer's eye)

*Adapted in structure from nature-skills (nature-statistics/references/reviewer-checklist.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

Run before delivering an audit or a revised text. Tag each open item P0, P1 or P2 (see `common-failure-modes.md`).

## A. Cell rules (cell.md) — required at revision and final

- [ ] Every main and supplemental legend names the statistical test(s) and the panels (§4).
- [ ] Every legend gives the p value each asterisk stands for (§4).
- [ ] Every legend gives the number of biological and technical replicates for each result (§4).
- [ ] Every legend defines each measure and error bar (§4).
- [ ] Every main legend with related supplemental items says "See also Figure S…" (§4).
- [ ] Every supplemental figure title says "related to Figure N" (§7).
- [ ] Statistical methods are in STAR Methods, not in the supplement (§7, §8).
- [ ] Compared data come from the same experiment (§5).
- [ ] Individual data points are shown where feasible (recommended, §5).
- [ ] Main legends still fit the 7,000-word main-text count, which includes them (§2).

For a first submission, list unmet items as "needed at revision" (§1).

## B. Design and replication — craft guidance (not a journal rule)

- [ ] The replicate unit is named for every result.
- [ ] n counts replicate units, not measurements.
- [ ] Nested data are aggregated or modelled; both levels of n are given.
- [ ] Paired and repeated designs are analysed as such.
- [ ] Exclusions, randomization and blinding are stated, including "none".

## C. Tests and corrections — craft guidance

- [ ] Each test fits the design and the variant is named.
- [ ] Multiple comparisons are corrected; the family is stated.
- [ ] Claims of a difference between effects rest on a direct test.
- [ ] Adjusted values are labelled as adjusted.
- [ ] Spatial statistics state their null.

## D. Reporting — craft guidance

- [ ] Effect sizes and intervals accompany p values for central claims.
- [ ] "No effect" statements are worded as "not detected" with the estimate.
- [ ] Wording strength matches the design (association versus causal).
- [ ] Software and versions appear in the key resources table and in "Quantification and statistical analysis".

## E. Agreement

- [ ] Legend, Results text and "Quantification and statistical analysis" give the same test, n and error-bar type for each panel.
- [ ] No test is described in STAR Methods that no figure uses.
- [ ] Panels added or moved in revision carry their statistics; panel letters in test sentences are current.
- [ ] `scripts/legend_stats_check.py` was run on the current legends; remaining warnings are explained.

## F. Questions a statistical referee is likely to ask

| Trigger in the manuscript | Likely question |
|---|---|
| n in cells, spots, fields | "What is the number of independent animals or patients, and was the test done at that level?" |
| Many panels, each with stars | "Were the comparisons corrected, and what was the family?" |
| Bars without points | "Please show individual data points." |
| Small cohort, survival split | "How was the cut-point chosen? Is there an independent cohort?" |
| Clusters then markers | "Are these p values from the same data used for clustering?" |
| Spatial co-localization | "What null model accounts for spatial autocorrelation?" |
| One experiment shown | "How many times was this repeated, with what result?" |
| "No difference" | "Was the study powered to detect one? Give the interval." |

## G. Delivery

- [ ] Each issue is labelled Cell rule (with §) or craft guidance.
- [ ] No invented numbers. Open facts are listed under `AUTHOR_INPUT_NEEDED`.
- [ ] The stage (first submission, revision, final) is stated at the top of the report.
