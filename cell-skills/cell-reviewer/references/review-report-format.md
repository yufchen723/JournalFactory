# Review report format

*Adapted in structure from nature-skills (nature-reviewer/references/report-structure.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

cell.md contains no referee report form. This format is **craft guidance (not a journal rule)**: the shape a careful referee report usually takes. For Cell's own referee instructions: not specified in cell.md — check cell.com.

## 1. Report skeleton

```text
REFEREE REPORT (simulated, pre-submission)

1. Summary of the claims
   Two to five sentences in the referee's words: the question, the approach,
   the central claim, the main supporting claims.

2. Conceptual advance
   What is new relative to what was known. How it compares with the
   article-type criterion (cell.md §2). Who would be interested.
   Marked as assessment, with the literature boundary stated.

3. Assessment of the evidence
   Which claims are supported, which are weak, which cannot be assessed.

4. Major points
   M1, M2, ... each with: claim pointer, evidence pointer, the concern,
   the alternative explanation, what would resolve it, necessity rank.

5. Minor points
   m1, m2, ... clarity, presentation, missing details, wording strength.

6. Requested experiments and analyses, ranked
   Essential / Important / Optional (table below).

7. Statistics and reporting
   Replicate unit, n, tests, legend completeness (cell.md §4).

8. Presentation
   Title, Summary, subheadings, figures, limits (cell.md §2–§5).

9. Assessment boundary
   What was not supplied and therefore not reviewed.
```

## 2. One major point

```text
M2. The link between factor X and process Z is correlative.
Claim:     Summary, sentence 3; Results, "Factor X drives process Z".
Evidence:  Figure 3B–D (co-occurrence across samples); Figure S4.
Concern:   The data show that X and Z vary together. They do not show direction
           or dependence. A shared upstream cause (for example cell density)
           would give the same pattern.
Resolve:   (a) Perturb X and measure Z in the model of Figure 2 [essential], or
           (b) reword the claim to an association and state the limit in
               "Limitations of the study" [acceptable if the paper is a Resource].
Blocking:  Yes for a research article as currently titled.
```

Rules:

- One concern per point.
- Quote or point; do not paraphrase the claim into something easier to attack.
- Offer a way out that matches the article type. Not every concern needs a new experiment.
- "Blocking: Yes" only when the central claim cannot stand until the point is resolved.

## 3. Ranking requested experiments

| Rank | Definition | Typical example |
|---|---|---|
| **Essential** | Without it, a central claim is unsupported or an obvious alternative stays open | Perturbation for a causal claim; an independent cohort for a clinical association; the missing control that defines specificity |
| **Important** | Strengthens a supporting claim or generality; its absence can be handled by narrowing the claim | Second model system; orthogonal validation of a key measurement; dose or time dependence |
| **Optional** | Would be nice; does not change the conclusion | Extra cell types; deeper characterisation; additional visualisation |

For each request also record:

- **Feasibility**: weeks, months, or not feasible with the authors' system (author input).
- **Substitute**: an existing dataset or reanalysis that would answer the same question.
- **Text-only route**: the rewording that would make the experiment unnecessary.

Output table:

```markdown
| # | Request | Serves point | Rank | Feasibility | Substitute or text-only route |
|---|---|---|---|---|---|
| 1 | Knock down factor X, measure Z | M2 | Essential | AUTHOR_INPUT_NEEDED | Reword to association; move claim to Discussion |
```

## 4. Minor points

Keep them short. Typical content:

- Undefined abbreviations; inconsistent names for the same entity.
- Legends missing test, n, asterisk key, error-bar definition, scale bar (**Cell rule**, cell.md §4).
- Results subheadings that name an analysis instead of a finding (**Cell rule**, cell.md §3).
- "Novel" and "first" (**Cell rule**, cell.md §3: discouraged).
- Figures cited out of order (**Cell rule**, cell.md §4).
- Overlong main text or more than 7 display items (**Cell rule**, cell.md §2).

At first submission, format items are "needed later", not grounds for criticism (cell.md §1).

## 5. Tone

- Write as a colleague who wants the paper to be right.
- State the concern, the reason, and the remedy. No rhetorical questions.
- Do not speculate about motives.
- Acknowledge strengths specifically, in one or two sentences, not as a ritual.

## 6. Author-side summary (after the report)

```text
Top three actions:      [the changes that most reduce risk]
Solvable by rewording:  [points M?, m?]
Needs new data:         [points M?], with the essential requests
Open facts:             AUTHOR_INPUT_NEEDED list
```

Label this block "author-side", so it is not mistaken for part of the referee report.
