# cell-skills

Journal Factory's own skill pack for the journal **Cell** (Cell Press). Version 1.0.0 (2026-11-18).

Built the way `nature-skills` is built (router `SKILL.md` → `manifest.yaml` → small always-loaded
core → references opened on demand → scripts that check the result), with Cell's own rules in
place of Nature's.

- **Rules:** one file, `cell-shared/journal-formats/cell.md`, read on cell.com on 2026-11-18.
  Every skill quotes it by section; nothing else may state a Cell number.
- **Logic and structure:** adapted from nature-skills @14ca6971 (Apache-2.0). See `NOTICE.md`.
- **Code:** written for this pack. No vendored script is copied or executed.

## Skills

| Skill | Use it for | Check script (`jf cell …`) |
|---|---|---|
| `cell-figure` | Plan, draw (Python or R), audit and export main figures, Figure S, graphical abstract | `figure` (file audit), `demo` |
| `cell-writing` | Title, Summary, Highlights, eTOC blurb, Introduction, Results, Discussion + Limitations, STAR Methods, legends, cover letter | `text` |
| `cell-statistics` | Replicate unit, tests, what a legend must state, Quantification and statistical analysis | `legends` |
| `cell-reviewer` | Self-review as a Cell referee and editor would read it | — |
| `cell-response` | Revision plan, point-by-point response, revision cover letter, package consistency | `response` |
| `cell-data` | Resource availability, key resources table, deposition, supplemental files | — |
| `cell-citation` | Cell reference style, in-text citations, verification | `refs` |
| `cell-shared` | Internal layer: the journal format file and shared writing logic | — |

## Which stage of Journal Factory uses which skill

| Journal Factory stage | Skill |
|---|---|
| 3 Story and structure | `cell-figure/references/multipanel-evidence-architecture.md`, `cell-shared/core/cell-results-discussion.md` |
| 4 Figures | `cell-figure` |
| 5 Text | `cell-writing` |
| 6 Statistics and reporting | `cell-statistics`, `cell-data` |
| 7 Submission | `cell-writing` (cover letter, front matter), `cell-data`, `cell-citation` |
| 8 Revision | `cell-reviewer`, `cell-response` |

## What is different from nature-skills

| | nature-skills | cell-skills |
|---|---|---|
| Figure widths | 89 / 183 mm | 85 / 114 / 174 mm |
| Text in figures | 5–7 pt, Arial or Helvetica | about 6–8 pt, Arial only |
| Panel letters | lowercase bold | capital |
| Abstract | summary paragraph | Summary ≤ 150 words + Highlights + eTOC blurb + graphical abstract |
| Methods | Methods | STAR Methods + key resources table |
| Extra figures | Extended Data | Figure S, "related to Figure N" |
| AI image generation | optional route | removed (Cell does not allow it for research images or graphical abstracts) |
| Scripts | run from the vendored pack | rewritten here; stdlib + matplotlib / ggplot2 |

## Relation to `vendor/cell-skills`

`vendor/cell-skills` is the third-party checklist pack (MIT), kept unchanged as reference text.
This pack replaces it as the first thing to read for Cell. Where the two disagree, `cell.md` wins.

## Maintenance

- Cell changes its pages: re-read them in a browser, update `cell.md` (date at the top) and
  `journals/cell.json`, then run `python3 cell-figure/tests/test_cell_figure.py` and each script's
  `--self-test`.
- Not yet read on cell.com: the STAR Methods author guide PDF, the journal-policies page
  (resource availability wording, generative-AI policy), the final file requirements PDF.
