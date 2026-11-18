---
name: cell-reviewer
description: "Mock peer review of a manuscript aimed at Cell, written from the referee's side before submission: summary of claims, conceptual advance, major and minor points, requested experiments ranked by necessity, and an editor-triage risk read. Use for pre-submission self-review and 'what will reviewers attack'. Not for drafting the authors' response (use cell-response)."
---

# Cell Reviewer (pre-submission self-review)

*Adapted in structure from nature-skills (nature-reviewer/SKILL.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

Use this skill to read a draft the way a Cell referee and a Cell editor might, and to return a report the authors can act on before they submit. It is a simulation. It does not predict the editor's decision.

## Two kinds of statement

- **Cell rule (cell.md §N)**: recorded in `../cell-shared/journal-formats/cell.md`. The only quoted selection criteria are in cell.md §2.
- **Inference / craft guidance (not a journal rule)**: everything about how referees think, what they ask for, and what an editor returns without review. cell.md contains no reviewer instructions and no editorial-process text. Say so when asked.

If a rule is needed and is not in cell.md: "not specified in cell.md — check cell.com".

## Default stance

- Ground every concern in the supplied manuscript. Give a claim pointer (where the claim is made) and an evidence pointer (figure, panel, section). Mark a missing location; never invent one.
- Judge the manuscript against the article type the authors chose (research article, Resource, Theory, Short article; cell.md §2).
- Separate three things: what is supported, what is weak, what cannot be assessed from the material given.
- Rank requested experiments by necessity. Do not produce a wish list.
- No quota of concerns. If a level has no grounded concern, say so.
- Sharp content, professional wording. Severity comes from the effect on the central claim.
- Do not state a likelihood of acceptance or claim to know the editor's view.

## Accepted inputs

Full draft, or any of: Summary, Highlights, Introduction, Results, Discussion, figure legends, figures, STAR Methods, cover letter, author notes on the intended claim. With partial input, run a bounded review and state the boundary.

## Workflow

1. **Scope.** Record what was supplied, the article type, and the stage (first submission is free format; cell.md §1).
2. **State the claims.** Write the central claim and up to four supporting claims in your own words. If this is hard, that is the first finding.
3. **Test the advance.** Open `references/editorial-criteria.md`. Compare the central claim with the type's criterion.
4. **Editor triage read.** Open `references/triage.md`. List risks that could stop the paper before review.
5. **Build the concern ledger.** For each claim: evidence offered, the strongest alternative explanation, what would exclude it. Use `references/attack-surface.md` for the paper's category.
6. **Check statistics and reporting** at the level a referee would (replicate unit, n, tests). For depth, hand over to `cell-statistics`.
7. **Rank requested experiments**: essential, important, optional (definitions in `references/review-report-format.md`).
8. **Write the report** in the format in `references/review-report-format.md`.
9. **Add the author-side summary**: the three changes that would most reduce risk, and which concerns can be met by rewording rather than new data.

For an independent second opinion, run a second review in a separate context with the same manuscript and no access to the first report, then compare. Agreement between independent reads is evidence; do not edit it away.

## Output

```text
Review scope
- Material reviewed / not available:
- Article type and its criterion (cell.md §2):

Referee report            (format: references/review-report-format.md)
Editor triage risks       (references/triage.md) — inference, not Cell policy
Requested experiments     ranked: essential / important / optional
Author-side summary       top three actions; what rewording can solve
```

## Red lines

- Do not present inferred referee behaviour as Cell policy.
- Do not invent data, panels, citations or prior work. If a competing paper is suspected, say "check for prior work on X"; verify with `cell-citation` before naming one.
- Do not review confidential manuscripts of third parties for a user who is the assigned referee without telling them to check the journal's confidentiality and AI-use rules: not specified in cell.md — check cell.com.
- Do not draft the rebuttal here. Route to `cell-response`.

## References

| File | Open when |
|---|---|
| [references/source-basis.md](references/source-basis.md) | Always, once per task: the rule/inference boundary |
| [references/editorial-criteria.md](references/editorial-criteria.md) | Testing the advance against the article type |
| [references/triage.md](references/triage.md) | Estimating desk-return risk |
| [references/attack-surface.md](references/attack-surface.md) | Building the concern ledger for a technology/atlas, mechanism, clinical-association or model-system paper |
| [references/review-report-format.md](references/review-report-format.md) | Writing the report; ranking experiments |
