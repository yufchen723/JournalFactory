---
name: cell-shared
description: Internal shared-reference layer for the Cell skills (cell-writing and any later cell-* skill). Not a standalone workflow. Holds the one file of official Cell rules (journal-formats/cell.md) and shared writing contracts (Summary, Introduction, Results/Discussion, main-text length, terminology, consistency). Load only the specific file another Cell skill asks for.
---

Adapted in structure from nature-skills (nature-shared/SKILL.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

# Cell Shared References

Use this package only as a dependency of another Cell skill. Load the exact file named below;
do not preload the whole package. Return to the requesting skill for task logic and output format.

## The source-of-truth rule

- `journal-formats/cell.md` is the **only** source of Cell numbers, section names and formats.
  It records what was read on cell.com on 2026-11-18 and which pages were not read.
- Every other file in the Cell skills either cites it as `Cell rule (source: cell.md §N)` or labels
  its content `craft guidance (not a journal rule)`.
- If a needed rule is not in cell.md, write: `not specified by Cell (see cell.md)`.
  Do not fill the gap with a Nature rule or with a number from memory.
- cell.md §1 sets the stage (initial submission / revision / final files). Check the stage before
  calling anything a failure: initial submission is free format.

## Which file to load for what

| Need | File | Status of the content |
|---|---|---|
| Any Cell limit, component order, legend rule, front-matter rule, supplemental naming, reference style | `journal-formats/cell.md` | official (as read 2026-11-18) |
| Build or audit the Summary (≤ 150 words) | `core/cell-summary.md` | Cell rules + craft guidance |
| Build or audit the Introduction | `core/cell-introduction.md` | Cell rules + craft guidance |
| Results subheadings, figure titles, claim escalation, Discussion, Limitations of the study | `core/cell-results-discussion.md` | Cell rules + craft guidance |
| Fit under 7,000 words; decide main text vs STAR Methods vs Figure S / Table S | `core/main-text-discipline.md` | Cell rules + craft guidance |
| Fix names before drafting (terms, genes/proteins, figure and supplemental item names) | `core/terminology-ledger.md` | Cell rules + craft guidance |
| Audit an existing draft for drift (names, numbers, callouts, spelling) | `core/consistency-sweep.md` | Cell rules + craft guidance |

`manifest.yaml` lists the same files with load conditions for skills that route by manifest.

## What this package does not hold

- Figure production (widths, fonts, resolution): the rules are in cell.md §5; a figure skill applies them.
- Research-ethics and reporting-policy text: the Cell journal-policies page was not read (cell.md header).
  Say so when a task depends on it.
- A mechanical checker: use `../cell-writing/scripts/cell_text_check.py`.
