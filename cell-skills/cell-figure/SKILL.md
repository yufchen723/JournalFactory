---
name: cell-figure
description: >-
  Plan, draw, revise, audit and export figures for a Cell (Cell Press) manuscript in Python or R:
  main figures, Figure S, and the graphical abstract. Sizes, fonts, lines, colour and file rules
  are Cell's own (85 / 114 / 174 mm, Arial, about 6-8 pt, capital panel letters, TIFF or PDF).
  Not for interactive dashboards or statistics-only analysis.
---

# Cell figure making — router

Version 1.0.0. Structure adapted from nature-skills `nature-figure` (Apache-2.0); every Cell number
comes from `../cell-shared/journal-formats/cell.md` (read on cell.com 2026-11-18). All code in
`scripts/` was written for this skill.

## Routing

### 0. Which kind of job is it?

| Request | Route |
|---|---|
| Graphical abstract | `references/graphical-abstract.md`. No data, no Python/R question. General-purpose AI image generators are not allowed by Cell for graphical abstracts. |
| Workflow drawing or mechanism schematic inside a figure | Journal Factory `references/09_schematics.md` (icons, SVG), then place it as a panel. |
| Check an existing file | `scripts/validate_cell_figure.py FILE`, then `references/qa-contract.md`. No backend question. |
| Plan or restructure a multi-panel figure | `static/core/contract.md` + `references/multipanel-evidence-architecture.md`. No backend question. |
| Draw or change a data figure | steps 1–4 below |

### 1. Load the core

Read `manifest.yaml`, then both `always_load` files: `static/core/contract.md` (what must be
decided before any code) and `static/core/stance.md` (defaults).

### 2. Resolve the backend (Python or R)

In this order: an explicit choice in the request → the language of the script or object the user
gave → a choice made earlier in this task → `python3 scripts/cell_figure_backend.py get`. If none,
ask once: **"Python or R? I will remember it."** and save with `... set python|r`. Planning and
auditing do not wait for this. One backend per figure: do not preview an R figure with matplotlib
or the reverse. The audit script reads exported files from either backend and draws nothing.

### 3. Load the backend fragment

`static/fragments/backend/python.md` or `static/fragments/backend/r.md`, not both.

### 4. Build in this order

1. **Contract** — claim, panel roles, archetype, stage (initial or production), width.
2. **Draw** — `cell_style` / `cell_theme.R`, templates from `references/template-catalog.md`.
3. **Gates before export** — alignment, text overlap, style (`save_cell` runs them and refuses to
   export on a failure).
4. **Audit the exported files** — `validate_cell_figure.py` on the PDF and the TIFF.
5. **Look at it** — open the preview at printed size and go through `references/qa-contract.md`
   panel by panel. The audits do not replace this.
6. **Legend facts** — hand the statistics, n and error-bar definitions to
   `../cell-writing/references/figure-legends.md`.

## Stage matters

Cell's figure rules are **production** rules. At first submission any format, size and resolution
is accepted. Run the audit with `--stage initial` for a first submission: it reports everything as
"needed later" and blocks nothing. Build at the production size anyway; it saves a second round.

## References (open only when needed)

| When | File |
|---|---|
| Exact Cell rules and what Cell does not specify | `references/cell-figure-requirements.md` |
| One figure = one claim; panel roles; main vs Figure S; seven-figure arc | `references/multipanel-evidence-architecture.md` |
| Python and R templates | `references/template-catalog.md` |
| Tissue maps, tracks, large point clouds, image plates | `references/omics-spatial-panels.md` |
| Colour, type, line and gray choices | `references/design-notes.md` |
| Before delivery | `references/qa-contract.md` |
| Graphical abstract | `references/graphical-abstract.md` |
| What is official and what is house style | `references/source-basis.md` |

## Do not

- Do not use Nature's numbers (89 / 183 mm, 5–7 pt, lowercase panel letters) for a Cell figure.
- Do not alter research images with generative or AI-assisted tools (Cell policy), including
  brightness, contrast or colour balance.
- Do not drop data to make a plot easier; rasterise or aggregate with a stated rule instead.
- Do not call a figure "Cell-ready" from the audit alone, or while Arial is substituted.
