# Workflow and output format

*Adapted in structure from nature-skills (nature-response/static/core/workflow.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

Craft guidance (not a journal rule) unless a line is marked **Cell rule**.

## Accepted inputs

Decision letter; reviewer reports; an earlier response draft; author notes on what was done; the revised or original manuscript (text, legends, figure list, supplemental index); new data summaries; the deadline; any portal instructions.

If reviewer boundaries or comment splits are unclear, flag it. Do not invent structure.

## Decision gate

Take the decision from the editor's letter. Package-level strategy depends on it.

| Editor's signal | Default strategy |
|---|---|
| Revision invited, new experiments expected | Evidence-first plan. Rank experiments; fix the central-claim concerns with data; long experiments start first. |
| Revision invited, mainly clarification | Bounded plan. Precise text, legend, statistics and presentation changes. No redesign. |
| Rejection with a door left open | Treat as a plan for a new submission; confirm with the editor what would be considered. |
| Rejection | `appeal-like`: see `references/difficult-cases.md`. Do not draft an appeal by default. |
| Unknown | Ask once. Meanwhile do comment-level triage, which does not depend on the label. |

The label sets the posture, not the severity of each comment. A statistics or integrity concern stays blocking inside a light revision. Cell's own decision categories are not specified in cell.md.

## Steps

1. **Fix mode and readiness** (`references/intake-and-routing.md`).
2. **Extract the editor's items** first: `E.1`, `E.2`, … Include which reviewer points the editor calls essential and any stated condition.
3. **Split reviewer comments** into single concerns: `R1.1`, `R1.2`, `R2.1`, … Keep the reviewer's order. Split a paragraph that holds two requests; keep the verbatim text for each.
4. **Classify** each item: category and severity (`references/comment-taxonomy.md`).
5. **Map to an action** and a work status (`references/action-mapping.md`). Find duplicates and conflicts across reviewers; decide once, in the plan.
6. **Rank experiments**: necessity for the central claim × feasibility. Offer a substitute for anything infeasible.
7. **Write the revision plan** (`templates/revision_plan.md`). This is the internal master document. Review it with the authors before drafting prose.
8. **Draft the point-by-point response** (`templates/point_by_point.md`, `references/response-structure.md`, `references/tone-and-stance.md`).
9. **Locate every change** in the revised manuscript: section and subheading, figure and panel, STAR Methods subsection, supplemental item. No location, no "done".
10. **Budget check.** After additions: main text under 7,000 words including main legends; no more than 7 main figures and/or tables (**Cell rule**, cell.md §2); recommended ≤ 20 supplemental figures (**Cell rule**, cell.md §7). Say what moved to make room.
11. **Front matter check.** Title, Summary, Highlights, eTOC blurb and graphical abstract still match the revised claims (limits in cell.md §3, §6).
12. **STAR Methods.** Confirm the revised manuscript uses the format (**Cell rule**, cell.md §1, §8) and that new experiments have methods, resources and statistics entered.
13. **Draft the cover letter** (`templates/revision_cover_letter.md`).
14. **Audit** (`references/package-consistency-audit.md`), run `scripts/check_response_package.py`, then `references/qa-checklist.md`.
15. **Report readiness**: `ready` only when no item is open.

For a local edit or audit, use only the steps that apply and return the passage or findings.

## Status vocabulary

| Field | Values |
|---|---|
| Action | see `references/action-mapping.md` |
| Work status | `DONE_VERIFIED` (location seen) · `DONE_REPORTED` (author says done, location not seen) · `IN_PROGRESS` · `PLANNED` · `NOT_FEASIBLE` · `DECLINED_WITH_REASON` · `AUTHOR_INPUT_NEEDED` |
| Blocks submission | yes / no |
| Package readiness | `plan_only` · `draft_with_placeholders` · `draft_complete_unverified` · `ready` |

## Output package

```text
Revision strategy summary
- Decision and source:
- Task mode / package readiness:
- Editor's essential items:
- Central-claim risks:
- Open author inputs:

Revision plan                    (table; templates/revision_plan.md)
Point-by-point response          (templates/point_by_point.md)
Revision cover letter            (templates/revision_cover_letter.md)
Package audit                    (budget, numbering, front matter, script output)
AUTHOR_INPUT_NEEDED              (short factual questions)
```

Return only the parts the mode asks for.
