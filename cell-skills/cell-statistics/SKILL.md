---
name: cell-statistics
description: "Audit or draft the statistical reporting of a Cell manuscript: replicate unit, biological vs technical replicates, tests, multiple testing, figure-legend statistics, and the STAR Methods section 'Quantification and statistical analysis'. Use for legend statistics checks, pseudoreplication in single-cell or spatial data, and reviewer concerns about statistics. Computes new analyses only when the user supplies data and asks."
---

# Cell Statistics Reporting — Router

*Adapted in structure from nature-skills (nature-statistics/SKILL.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

A reporting and review skill. It makes the statistics of a Cell manuscript transparent and consistent between figure legends and STAR Methods. It does not replace a statistician and it does not reanalyse data unless the user supplies the data and asks.

## Two kinds of statement

Every piece of advice in this skill carries one of two labels:

- **Cell rule (cell.md §N)**: stated on cell.com and recorded in `../cell-shared/journal-formats/cell.md`.
- **Craft guidance (not a journal rule)**: good statistical practice. Never present it to the user as Cell policy.

If a rule is needed and is not in cell.md, write: "not specified in cell.md — check cell.com".

## Routing protocol

1. Read [manifest.yaml](manifest.yaml) and every file under `always_load`:
   - `references/source-basis.md` — what is a Cell rule and what is not.
   - `references/statistical-reporting.md` — replicate unit, tests, multiple testing, effect sizes.
2. Identify the task (table below) and the stage. Cell applies legend and STAR Methods rules at **revision**, not at first submission (cell.md §1). For a first-submission draft, report missing items as "needed at revision", not as failures.
3. Open on-demand references only when their condition in the manifest is met.

| Task | Open |
|---|---|
| Check or write figure legends | `references/figure-statistics.md`; run `scripts/legend_stats_check.py` |
| Write "Quantification and statistical analysis" | `references/quantification-and-statistical-analysis.md` |
| Single-cell, spatial, imaging or other nested data | `references/omics-and-spatial.md` |
| Nested data, many comparisons, small n, strong p-value language | `references/common-failure-modes.md` |
| Final QA, severity labels, reviewer risk | `references/reviewer-checklist.md` |

## Workflow

1. **Classify the task**: audit, rewrite, draft, legend alignment, reviewer-response support, or reanalysis with supplied data.
2. **Extract the design**: groups, time points, endpoints, pairing or blocking, repeated measures, exclusions, randomization, blinding.
3. **Fix the replicate unit**: for each result, name the independent unit (animal, patient, independent culture) and separate it from technical replicates and from sub-units (cells, fields, spots).
4. **Map each claim to an analysis**: comparison, test or model, correction, effect estimate, uncertainty.
5. **Check the legends** against cell.md §4 (test, asterisk meaning, biological and technical n, measures and error bars, "See also").
6. **Check agreement** between legends, Results text and "Quantification and statistical analysis".
7. **Draft or revise**. Keep claims inside the design. Do not turn association into mechanism.
8. **Run final QA** with `references/reviewer-checklist.md`.

## Script

```bash
python scripts/legend_stats_check.py legends.md      # exit 1 if any WARN
python scripts/legend_stats_check.py --self-test
```

Resolve the path relative to this skill directory. The script is a text lint. It cannot see the image and does not judge whether a test is appropriate.

## Output format

```text
Statistics review scope
- Input reviewed / stage (first submission, revision, final):
- Missing material:
- Replicate unit per result:

Issues
- [P0/P1/P2] Issue — Cell rule (cell.md §N) or craft guidance
  Evidence from the supplied text:
  Why it matters:
  Fix:

Ready-to-paste text
[legend sentence or Quantification and statistical analysis paragraph]

AUTHOR_INPUT_NEEDED
- [short factual questions only]
```

## Red lines

- Do not invent p values, sample sizes, tests, corrections, software versions, exclusion rules or power calculations. Write `AUTHOR_INPUT_NEEDED`.
- Do not accept "n = number of cells, spots, fields or images" as independent replication without checking the hierarchy.
- Do not recommend a final test while the replicate unit is unclear.
- Do not use "significant" to mean large, important or causal.
- Do not state a Cell requirement that is not in cell.md.
