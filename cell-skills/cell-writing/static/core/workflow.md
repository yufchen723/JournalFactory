# Writing workflow (cell-writing)

Adapted in structure from nature-skills (nature-writing/static/core/workflow.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

Use all steps for a new section or a full manuscript. For a title, one paragraph or a follow-up
edit, apply only the relevant steps and reuse the established claim and terms.
Steps 1–4 plan, 5–7 draft, 8–9 check, 10 handles revision.

The step order is craft guidance (not a journal rule). The limits quoted are Cell rules with
their cell.md section.

## 1. Write the one-sentence argument

> In [system], [actor] [does what] through [mechanism], shown by [decisive evidence], which
> explains [biological question]; it does not show [boundary].

Every part must serve this sentence. If it cannot be written, the paper has no argument yet;
tell the author.

## 2. Build the Terminology Ledger

Extract recurring terms, gene and protein names, group names, abbreviations and item names
(Figure 1A, Figure S1A, Table S1, Video S1). Lock them.
See `../../../cell-shared/core/terminology-ledger.md`.

## 3. Build the claim table (Results plan)

One row per display item, at most 7 rows (cell.md §2).

| # | Claim = Results subheading = figure title | Decisive evidence | Display item | Supplemental support |
|---|---|---|---|---|

- Each claim states a finding (cell.md §3).
- Each row is one step above the previous one.
- Anything that is not a step is support: supplemental figure, table, or STAR Methods.

See `../../../cell-shared/core/cell-results-discussion.md` and, for placement,
`../../../cell-shared/core/main-text-discipline.md`.

## 4. Set the word budget

Main text under 7,000 words including main figure legends; STAR Methods, supplemental legends and
references excluded (cell.md §2). Fix a split before drafting (craft guidance):

| Introduction | Results | Discussion + limitations | Main legends | Target total |
|---|---|---|---|---|
| 500–800 | 3,600–4,200 | 900–1,200 | 1,000–1,500 | about 6,700 |

## 5. Draft in this order

| Order | Part | Why here |
|---|---|---|
| 1 | Figure titles and legends | They fix what each figure shows; titles come from the claim table |
| 2 | Results | Written against the figures, one subsection per claim |
| 3 | Introduction | The gap is the question the Results answer; ends with what was achieved |
| 4 | Discussion and "Limitations of the study" | Synthesis after the claims are fixed |
| 5 | STAR Methods | Receives every procedure removed from Results and legends |
| 6 | Summary | Compresses the finished argument to 150 words |
| 7 | Title, keywords | Title ≤ 145 characters; up to 10 keywords |
| 8 | Highlights, eTOC blurb | Final-stage file; derived from the Summary and claim table |
| 9 | Cover letter | Quotes the final title and claim |

Each paragraph has one job: context, gap, question, result, control, inference, implication or
limitation. If a paragraph carries two, split it.

## 6. Draft from evidence outward

- Keep each claim next to its figure callout.
- Text carries direction and magnitude; the legend carries test, n and error definition; STAR
  Methods carries procedure.
- Calibrate verbs to evidence (`stance.md` §4).

## 7. Remove what Cell discourages or forbids

| Item | Rule | Source |
|---|---|---|
| "novel", "first" | discouraged | cell.md §3 |
| Subheadings in the Introduction | not allowed | cell.md §3 |
| Citations or non-standard abbreviations in the Summary | not allowed | cell.md §3 |
| Abbreviations in Highlights; "we" in the eTOC blurb | not allowed | cell.md §6 |
| "Supplementary Figure 1", "Extended Data" | use Figure S1, Table S1 | cell.md §7 |
| Methods in the supplement | belong in STAR Methods | cell.md §7 |
| Footnotes in the text | only in the author list and tables | cell.md §3 |

## 8. Check alignment

| Pair | Must agree on |
|---|---|
| Summary ↔ Introduction close ↔ Discussion opening | the central claim and its strength |
| Results subheading ↔ figure title | wording (cell.md §3, §4) |
| Text callouts ↔ legends | panel letters, order of first citation (cell.md §4) |
| Legends ↔ STAR Methods | n, tests, error definitions |
| Main legend ↔ supplemental titles | "See also Figure S1" ↔ "related to Figure 1" (cell.md §4, §7) |
| Highlights, eTOC blurb, cover letter ↔ manuscript | terms, numbers, claim strength |

For a full audit load `../../../cell-shared/core/consistency-sweep.md`.

## 9. Run the checker and return prose plus notes

```bash
python scripts/cell_text_check.py manuscript.md [--stage initial]
python scripts/cell_text_check.py --highlights highlights_etoc.md
```

Return:

1. the draft;
2. counts against each limit, with the counting method (Cell does not specify one; see cell.md);
3. `Assumptions or missing inputs`;
4. checker FAIL and WARN lines that remain, each with a proposed fix;
5. for a compression task, the compression record of `main-text-discipline.md` §8.

## 10. Revise by targeted edit

- Change the paragraphs the author flagged; keep the rest verbatim.
- If a fix forces a change elsewhere (a renamed term, a renumbered figure), make it everywhere
  and say so.
- Every added sentence triggers the deletion check (`main-text-discipline.md` §6). Recount.
- Keep the ledger stable unless the author changes a term.
- After the edit, rerun only the checks that the change touches, then the checker.
