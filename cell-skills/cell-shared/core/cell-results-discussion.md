# Cell Results and Discussion

Adapted in structure from nature-skills (nature-shared/core/nature-results-discussion.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

Use this file to plan, draft or audit Results subheadings, figure titles, the order of claims,
the Discussion and its "Limitations of the study" subsection.

## 1. Cell rules

| Rule | Source |
|---|---|
| Results are divided into subsections with short, informative subheadings that **state the finding**: "Factor X requires factor Y to function in process Z", not "Analysis of factors X and Y using approach Q" | cell.md §3 |
| Use similar wording in figure titles; re-use the Results subheadings as figure titles | cell.md §3, §4 |
| A figure title is brief, covers the whole figure, and cites no panels | cell.md §4 |
| No more than 7 figures and/or tables in the main paper | cell.md §2 |
| All figures are cited in the main text, in numerical order | cell.md §4 |
| Discussion gives implications and context; it does not repeat Results | cell.md §3 |
| Discussion includes a subsection "Limitations of the study", specific to the paper | cell.md §3 |
| "novel" and "first" discouraged | cell.md §3 |

Not specified by Cell (see cell.md): the number of Results subsections, a length for the
Discussion or for the limitations subsection, whether the Discussion may have other subheadings,
and whether one subsection must map to exactly one figure.

Everything below is craft guidance (not a journal rule).

## 2. One subsection, one claim, one display item (default)

Plan Results as a table before writing prose:

| # | Question raised by the previous result | Claim (= subheading = figure title) | Decisive evidence | Display item | See also |
|---|---|---|---|---|---|
| 1 | What changes after injury? | Dying epithelial cells release factor X in proportion to damage | dose series, tissue staining | Figure 1 | Figure S1 |
| 2 | What does factor X act on? | Factor X binds receptor Y on quiescent stem cells | binding assay, lineage reporter | Figure 2 | Figure S2 |
| … | | | | | |

- Write the subheading as a full statement with a verb. If it cannot be falsified, it is a topic.
- The figure title uses the same statement, or a shortened form of it.
- A subsection that needs two figures is usually two claims; split it or move one figure to the
  supplement.
- With at most 7 display items, the paper carries at most about 7 claim steps. Choose them first,
  then assign data.

Subheading repair:

| Topic label | Finding statement |
|---|---|
| Characterization of factor X expression | Factor X is produced by dying epithelial cells |
| Role of receptor Y in stem cells | Receptor Y is required for stem cell activation after injury |
| Single-cell analysis of the injured intestine | Injury expands a receptor Y–high stem cell state |

## 3. Claim escalation across the display items

Each subsection must add a claim one level above the previous one. Common arc for a mechanism paper:

`phenomenon → source or identity → necessity → sufficiency → mechanism → generality or human relevance → consequence`

Example allocation over 7 items:

| Item | Level | Example claim |
|---|---|---|
| Figure 1 | Phenomenon | Stem cell activation scales with the extent of damage |
| Figure 2 | Source | Dying epithelial cells release factor X |
| Figure 3 | Necessity | Factor X is required for damage-scaled activation |
| Figure 4 | Sufficiency | Factor X alone activates quiescent stem cells |
| Figure 5 | Mechanism | Factor X signals through receptor Y and pathway Z |
| Figure 6 | Generality | The factor X signal operates in human organoids |
| Figure 7 | Consequence | Excess factor X depletes the stem cell pool |

Tests:

- Delete a subsection. If the argument still holds, the subsection is support, not a step; merge
  it into a neighbor or move it to a Figure S.
- Two subsections with the same inferential conclusion are one step shown twice. Keep the
  stronger; the other becomes "See also Figure S…".
- A Resource or Theory article escalates differently (cell.md §2): a Resource needs the
  technical advance or dataset plus proof of principle; a Theory article needs testable predictions.

## 4. Inside a subsection

`question from the previous result → experiment and why it is decisive → result with figure callout → control or alternative excluded → one-sentence inference`

- Open with the question, not the method.
- Callouts are "Figure 1A", "Figures 1A and 1B", "Figure S1A", "Table S1" (see `terminology-ledger.md`).
- Keep exact statistics in the legend and STAR Methods; the text carries direction and magnitude
  (see `main-text-discipline.md`).
- End with the inference that sets up the next subsection. Local interpretation of the experiment
  just shown belongs here; field-level interpretation belongs in the Discussion.

## 5. Discussion that does not repeat Results

| Paragraph | Job | Not this |
|---|---|---|
| 1 | The answer to the Introduction's question, in one paragraph, one level above the data | A figure-by-figure recap |
| 2–3 | What the answer changes: relation to prior models, which earlier findings it explains or contradicts | A literature list with "consistent with" |
| 4 | Mechanistic or conceptual implication; a prediction that follows | New data or new analyses |
| 5 (optional) | Wider consequence (other tissues, disease), bounded | Clinical promise the data do not support |
| Subsection | **Limitations of the study** | A closing "Conclusion" paragraph in place of it |

Repetition test: a Discussion sentence that could be moved into Results unchanged is recap. Keep
at most one clause of recap per paragraph, as the anchor for an interpretation.

Modal strength: "show/demonstrate" for direct evidence in this paper; "suggest/indicate" for
inference; "may/could" for untested extension. Use the same verb for the same claim in the
Summary, Introduction close and Discussion.

## 6. "Limitations of the study"

Cell rule: the subsection is required and must be specific to the paper (cell.md §3).

Write it under exactly this heading, as the last part of the Discussion. Typical length: one
paragraph, three to five sentences (craft guidance).

For each limitation give three things:

1. **What** was not tested or cannot be concluded.
2. **Which claim** it bounds.
3. **How** it could be resolved, or why the main conclusion stands without it.

| Generic (reject) | Specific (accept) |
|---|---|
| "Further studies are needed to validate these findings." | "We deleted factor X in all epithelial cells; whether enterocytes or secretory cells are the relevant source remains to be tested with lineage-specific drivers." |
| "Our sample size was limited." | "Human data come from organoids of four donors, so variation between individuals in the factor X response is not resolved." |
| "The mechanism is not fully understood." | "We show that pathway Z is activated downstream of receptor Y but did not identify the adaptor that links them." |

Sources of real limitations: the model system (species, in vitro versus in vivo), the perturbation
(timing, specificity, compensation), the measurement (resolution, indirect readout), the sample
(number of donors or animals, sex, age), the inference (correlative step in a causal chain), and
anything a figure skill or reviewer flagged that the paper does not fix.

Do not use the subsection to pre-argue with reviewers or to list future plans unrelated to a claim.

## 7. Audit list

1. Every Results subheading states a finding; none starts with "Analysis of", "Characterization of", "Role of".
2. Each figure title matches its subheading in wording (Cell rule).
3. ≤ 7 main figures and/or tables; all cited in numerical order (Cell rule).
4. Removing any one subsection breaks the argument.
5. Discussion paragraph 1 answers the Introduction's question and matches the Summary in strength.
6. No Discussion paragraph is a recap.
7. "Limitations of the study" exists, names paper-specific limits, and ties each to a claim.
