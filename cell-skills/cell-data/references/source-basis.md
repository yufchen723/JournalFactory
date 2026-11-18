# Source basis for `cell-data`

*Adapted in structure from nature-skills (nature-data/references/source-basis.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

## What comes from Cell

Only `../../cell-shared/journal-formats/cell.md` (read on cell.com on 2026-11-18).

| Statement | Where |
|---|---|
| Resource availability is required, with three subsections: Lead contact · Materials availability · Data and code availability | cell.md §3 |
| Resource availability sits in the manuscript after the Discussion and before Acknowledgments | cell.md §3 (component order) |
| Lead contact: exactly one; must be a corresponding author | cell.md §3 |
| Key resources table: Cell Press Word template or webform; RRIDs for antibodies and genetically modified organisms | cell.md §8 |
| STAR Methods headings (from the author guide, not re-read; confirm): Key resources table · Experimental model and study participant details · Method details · Quantification and statistical analysis · Additional resources (optional) | cell.md §8 |
| STAR Methods required at revision and for acceptance, not at first submission | cell.md §1, §8 |
| Datasets, code and methods are cited and listed in the references (DOI where one exists) | cell.md §9 |
| Supplemental information rules: Document S1, naming, sizes, Excel for long tables, no methods in the supplement, non-proprietary formats for data and code, no file above 500 MB | cell.md §7 |
| Original unprocessed data available on request; figures are screened | cell.md §5 |
| AI used in the research itself is reported in STAR Methods | cell.md §3 |

## What was not read

cell.md states these pages were **not read**. Nothing from them may be given as a Cell rule.

| Page | What depends on it |
|---|---|
| Journal-policies page | The exact required wording of each Resource availability subsection; data-sharing and deposition policy; mandatory repositories; embargo and reviewer-access rules |
| STAR Methods author guide (PDF) | Key resources table categories and columns; what each STAR Methods section must contain |
| Final file requirements (PDF) | Production details for files |
| Video guidelines | Video S# format |

Tell the user to open the relevant page before finalising. Until then, mark template wording as "pattern, not Cell's required wording".

## Third-party checklists

The folders `vendor/cell-skills` and `vendor/cancer-cell-skills` contain checklists with their own statements about Cell (for example where Resource availability sits, a "three-bullet" data statement, a default repository). They are third-party and unverified. Where they disagree with cell.md, cell.md wins. Where cell.md is silent, their content is at most craft guidance and is labelled so.

## Craft guidance in this skill

- Repository choices by data type (`deposition.md`).
- Controlled access for human data (`deposition.md`).
- Key resources table categories and row conventions (`key-resources-table.md`), marked "confirm in the Cell Press template".
- Statement patterns in `templates/`.

## Use of nature-skills

The structure (inventory → access route → repository → statement → cross-check; no invented identifiers; "on request" flagged as weak) is adapted from nature-data. Nature's data-availability policy, statement placement and mandatory-deposition list are not imported.
