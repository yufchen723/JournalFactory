# Package consistency audit

*Adapted in structure from nature-skills (nature-response/references/package-consistency-audit.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

`qa-checklist.md` asks whether the response is complete and well judged. This file asks whether the files agree with each other. Run both.

**The coupling rule (craft guidance).** A revision package is coupled: response, cover letter, manuscript text, legends, figures, supplemental files, front-matter file. A change in one can silently falsify another. Re-run this audit after every manuscript edit.

## 1. Figure and panel renumbering

Revisions insert panels and figures. Every reference must follow.

- [ ] Build a mapping table old → new for every figure and panel that moved.
- [ ] Main text cites all figures, in numerical order (**Cell rule**, cell.md §4).
- [ ] Every panel cited in the text exists in the legend, and every panel in the legend is cited.
- [ ] Panel letters are capitals (**Cell rule**, cell.md §5).
- [ ] The test sentence in each legend names current panel letters ("by t test (A, F, and H)").
- [ ] The response uses new numbers in the authors' text; reviewer quotes keep the old ones; the mapping is given where confusion is possible.
- [ ] STAR Methods and supplemental legends that cite main panels are updated.
- [ ] No "Table 1A/1B" (**Cell rule**, cell.md §4).

```bash
python scripts/check_response_package.py response.md --manuscript manuscript.md
```

The script finds figure, panel and table references in the response that are absent from the manuscript's legends. It does not check the manuscript's own in-text citations.

## 2. Supplemental items

- [ ] Each supplemental figure title reads "Figure S#. [title], related to Figure N" (**Cell rule**, cell.md §7).
- [ ] The N in "related to Figure N" is the **new** number of the main figure.
- [ ] The main legend names its related items: "See also Figure S#" (**Cell rule**, cell.md §4). Check both directions.
- [ ] Naming: Figure S1, Table S1, Data S1, Methods S1, Video S1; never "Supplementary Figure 1" (**Cell rule**, cell.md §7).
- [ ] Supplemental figures are numbered in order; recommended ≤ 20 (**Cell rule**, cell.md §7).
- [ ] The manuscript's "Supplemental information" index lists every item, Document S1 first (**Cell rule**, cell.md §7).
- [ ] No methods in the supplement (**Cell rule**, cell.md §7).
- [ ] Tables longer than 3 pages are Excel files (**Cell rule**, cell.md §7).

## 3. Legends

- [ ] Each new or changed legend has: figure title without panel citations, test(s), p value per asterisk, n biological and technical, measure and error bars, scale bars, "See also" (**Cell rule**, cell.md §4).
- [ ] Figure titles re-use the Results subheadings where possible (**Cell rule**, cell.md §4).
- [ ] Run `../cell-statistics/scripts/legend_stats_check.py` on the legends.

## 4. Limits after additions — Cell rule (cell.md §2)

| Limit | Check |
|---|---|
| Main text under 7,000 words, **including main figure legends**; excluding STAR Methods, supplemental legends, references | Recount after every round. New legends count. |
| No more than 7 figures and/or tables in the main paper | Count figures + tables together |
| Short article: ≤ 4,000 words, ≤ 4 display items, ≤ 4 supplemental figures, ≤ 8 supplemental items | if applicable |
| Summary ≤ 150 words; title ≤ 145 characters with spaces; ≤ 10 keywords (cell.md §3) | Recheck if reworded |

Report the counts in the cover letter. If over, state what moved where (see `difficult-cases.md` §11).

## 5. Front matter still true — Cell rule for limits (cell.md §3, §6)

A narrowed or changed claim must change everywhere it is stated.

- [ ] Title: still accurate; ≤ 145 characters with spaces.
- [ ] Summary: matches revised results; ≤ 150 words; no citations.
- [ ] Highlights: up to 4; each ≤ 85 characters with spaces; no abbreviations; each still supported.
- [ ] eTOC blurb: ≤ 50 words, 2 sentences, third person; still true.
- [ ] Graphical abstract: shows the revised conclusion; no data items; no element the revision removed.
- [ ] Results subheadings and figure titles state the revised findings.
- [ ] "Limitations of the study" includes every limit conceded in the response.
- [ ] Keywords still fit.

Highlights, eTOC blurb and graphical abstract are final-file items (cell.md §1, §6). If they already exist at revision, audit them; if not, note "needed later".

## 6. Response versus manuscript

- [ ] Every "we have added / revised" in the response has a location, and the text or panel is there.
- [ ] Every quoted new sentence in the response appears verbatim in the manuscript. A later edit to that sentence is mirrored in the response.
- [ ] Numbers quoted in the response (n, p, effect sizes) equal those in the legend and Results.
- [ ] Deletions ripple: a panel or sentence removed late is not still described in the response as added.
- [ ] No promise remains ("we will", "future work" as an answer). The script lists candidates.
- [ ] The cover letter's list of main changes matches the response.

## 7. STAR Methods and resources

- [ ] Every new experiment has a Method details entry and, if quantitative, an entry in "Quantification and statistical analysis".
- [ ] New antibodies, organisms, cell lines, software and datasets are in the key resources table; RRIDs for antibodies and genetically modified organisms (**Cell rule**, cell.md §8).
- [ ] New datasets and code appear in Resource availability (**Cell rule**, cell.md §3) and are cited in the reference list where they have a DOI (cell.md §9).

## 8. References

- [ ] New references are verified against the source (`cell-citation`).
- [ ] Numbering follows order of first citation after insertions (**Cell rule**, cell.md §9).
- [ ] Preprints that have since been published are replaced (**Cell rule**, cell.md §9).
- [ ] References cited only in the supplement appear only in the supplemental list (**Cell rule**, cell.md §7).

## 9. Delivery gate

Deliver as `ready` only when sections 1–8 pass, the script exits 0, and the promise list is empty or each entry is justified (for example "future work" inside a quoted Discussion sentence).
