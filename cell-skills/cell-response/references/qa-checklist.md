# QA checklist

*Adapted in structure from nature-skills (nature-response/references/qa-checklist.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

Run before delivering any response, letter or audit. Craft guidance (not a journal rule) unless marked.

## A. Coverage

- [ ] Every editor instruction has an ID and an answer (in the cover letter, and in the response where relevant).
- [ ] Every reviewer comment is quoted in full and unchanged.
- [ ] No comment is skipped, merged away or answered only by cross-reference.
- [ ] Compound comments were split; each part is answered.
- [ ] General remarks ("descriptive", "overstated") are answered as items.

## B. Substance

- [ ] The first sentence of each response answers the comment.
- [ ] S1 items are met with data or a real change of claim, not prose.
- [ ] Each new result is stated with numbers, n and the panel.
- [ ] Each disagreement has a reason a neutral expert would accept, and a change made anyway.
- [ ] Each infeasible request has a concrete constraint, a substitute, and a stated limit.
- [ ] No response relies on data that are nowhere in the manuscript or supplement, unless marked as reviewer-only with a reason.

## C. Truthfulness

- [ ] No invented experiments, results, statistics, citations, panels, pages or lines.
- [ ] "We have…" appears only for work with status `DONE_VERIFIED` (or `DONE_REPORTED`, flagged).
- [ ] No promise remains in text to be submitted.
- [ ] Results that weakened are reported as such.
- [ ] Open facts are listed under `AUTHOR_INPUT_NEEDED`; none is hidden in fluent prose.

## D. Location

- [ ] Each response has a "Changes in the manuscript" line: a structural location, or "No change to the manuscript" with a reason.
- [ ] Figure and panel numbers are the revised ones; old numbers are mapped where needed.
- [ ] Page and line numbers appear only if the authors supplied them.

## E. Tone

- [ ] No blame of the reviewer; no "clearly", "obviously", "as already stated".
- [ ] No ritual thanks on every item.
- [ ] No defensiveness; no project history.
- [ ] "Novel" and "first" are not used in new manuscript text (**Cell rule**, cell.md §3: discouraged).

## F. Cell requirements at revision — Cell rule

- [ ] Cover letter and point-by-point response are both present (cell.md §1).
- [ ] The manuscript follows the component order (cell.md §3).
- [ ] STAR Methods format is used; no methods in the supplement (cell.md §7, §8).
- [ ] Resource availability has its three subsections (cell.md §3).
- [ ] "Limitations of the study" exists and is specific (cell.md §3).
- [ ] Legends carry statistics, n, error bars, "See also" (cell.md §4).
- [ ] Main text under 7,000 words including main legends; ≤ 7 display items (cell.md §2).
- [ ] Supplemental titles "related to Figure N" (cell.md §7).

Unverified items to tell the user about (not in cell.md): marked-manuscript format, who sees the point-by-point response, deadline. Cell rule (cell.md §1): the revision cover letter briefly summarises how the revision addresses the reviewer and editor comments and is confidential to the editor.

## G. Cover letter

- [ ] One page; states the main changes; answers each editor condition.
- [ ] Names what could not be done and why.
- [ ] States word count and display-item count.
- [ ] Contains nothing that contradicts the response.

## H. Package

- [ ] `references/package-consistency-audit.md` completed.
- [ ] `scripts/check_response_package.py` run on the current files; exit 0, or each finding explained.
- [ ] Readiness state reported honestly (`draft_with_placeholders` is a valid deliverable; a false `ready` is not).

## I. Final read as the reviewer

Read each response and ask:

1. Did they understand what I asked?
2. Did they do it, or tell me exactly why not?
3. Can I find the change in under a minute?
4. Is the claim now in line with the evidence?

Any "no" is an open item.
