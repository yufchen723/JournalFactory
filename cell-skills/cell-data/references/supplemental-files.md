# Supplemental information files

Source: cell.md §7 (cell.com supplemental-information page), plus §2, §4 and §9 where noted. Supplemental rules belong to the final-files stage (cell.md §1); at first submission report gaps as "needed later". Titles and legends of supplemental items are a manuscript component at revision (cell.md §3).

## 1. Rules — Cell rule (cell.md §7)

| Topic | Rule |
|---|---|
| How much | No strict limit; **recommended ≤ 20 supplemental figures**. Combine related items. One supplemental figure may span pages. |
| Titles | Name the main item they belong to: "Figure S1. [title], related to Figure 1" |
| Naming | **Figure S1, Table S1, Data S1, Methods S1, Video S1**. Never "Supplementary Figure 1". |
| Primary PDF, "Document S1" | A4 or Letter; **≤ 50 MB**; **Arial 10 pt**; contains figures with legends, tables that fit ≤ 3 pages, notes, supplemental references; **no title, authors or page numbers** |
| Methods | **Never in the supplement.** They belong in STAR Methods. |
| Long tables | Tables longer than 3 pages: **Excel** |
| Data and code | Non-proprietary formats |
| File size | No file above **500 MB** |
| Supplemental references | Numbered independently; references cited only in the supplement appear only there |
| Index | The manuscript carries a "Supplemental information" index, Document S1 first |

Related rules:

- Short article: ≤ 4 supplemental figures and ≤ 8 supplemental items in total (cell.md §2).
- Supplemental legends must state statistics, n, error bars and scale bars like main legends (cell.md §4).
- Main legends point to related items: "See also Figure S1" (cell.md §4).
- Supplemental item legends do not count toward the 7,000 words (cell.md §2).
- Full gels go in the supplement when lanes were removed or rearranged in a main figure (cell.md §5).
- "Supplemental information titles and legends" is a section of the manuscript, before the figure titles and legends (cell.md §3).

## 2. Open points

"Methods S1" appears in the naming list of cell.md §7, and the same section says methods never go in the supplement. cell.md does not explain what a Methods S# item may contain. **Not specified in cell.md — check cell.com** (supplemental-information page) before creating a Methods S# file. Until checked, put all methods in STAR Methods.

Also not specified in cell.md: video format and size (the video guidelines were not read); whether each Excel table needs a title sheet; file-naming conventions for upload; whether supplemental figures must also follow the main-figure production rules of cell.md §5.

## 3. What goes where — craft guidance (not a journal rule)

| Content | Put it in |
|---|---|
| Supporting figure for a main figure | Figure S#, in Document S1, "related to Figure N" |
| Small table (≤ 3 pages) | Table S#, in Document S1 |
| Large table (gene lists, sample metadata, statistics per feature) | Table S#, separate Excel file |
| Protocol detail, parameters, pipelines | STAR Methods (Cell rule) |
| Large datasets | A repository (see `deposition.md`); list under Resource availability |
| Code | An archive with a DOI; small scripts may be Data S# in a non-proprietary format |
| Movies | Video S# |
| Uncropped gels and blots | Supplemental figure or Data S# |

## 4. Document S1 assembly checklist

- [ ] One PDF; A4 or Letter; ≤ 50 MB; Arial 10 pt.
- [ ] No title page, author list or page numbers.
- [ ] Order: Figures S1…Sn, each followed by its legend; then small tables; then notes; then supplemental references.
- [ ] Each figure title ends "related to Figure N" (or to a table or STAR Methods section if that is what it supports — confirm the allowed targets on cell.com).
- [ ] Legends state test, asterisk meaning, n, error bars, scale bars.
- [ ] No methods text.
- [ ] Supplemental references numbered from 1, independent of the main list.

## 5. Excel table checklist — craft guidance

- [ ] One file per Table S#; file name carries the item name.
- [ ] A title and a column key on the first sheet or in the first rows.
- [ ] One value per cell; no merged cells; no colour as the only carrier of meaning.
- [ ] Gene names protected from spreadsheet auto-conversion (format the column as text).
- [ ] Units in column headers.
- [ ] Adjusted and raw p values in separate, labelled columns.

## 6. The supplemental index in the manuscript

Document S1 first, then each separate file, with title and the main item it relates to. Template: `../templates/supplemental_index.md`.

## 7. Consistency checks

- [ ] Every supplemental item is cited in the main text or STAR Methods, in order.
- [ ] Every "See also Figure S#" in a main legend matches a "related to Figure N" title, in both directions.
- [ ] After revision renumbering, "related to" targets use the new main-figure numbers.
- [ ] Supplemental figure count ≤ 20 (recommended), or the excess is justified by combining.
- [ ] Each file is under its size limit (Document S1 ≤ 50 MB; any file ≤ 500 MB).
- [ ] Items named with "S", never "Supplementary".

## 8. Common failures

| Failure | Fix |
|---|---|
| "Supplementary Methods" document | Move to STAR Methods |
| "Supplementary Figure 3" | Rename "Figure S3" |
| Supplemental title without "related to" | Add the main item |
| A 12-page table inside the PDF | Convert to Excel |
| 35 supplemental figures | Combine related ones; move raw data to a repository |
| Page numbers and a title page in Document S1 | Remove |
| Supplement-only references merged into the main list | Separate, numbered independently |
