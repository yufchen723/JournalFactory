# Results — drafting procedure

Adapted in structure from nature-skills (nature-writing/references/experiments.md and static/fragments/section/experiments.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

The shared contract (claim table, escalation, subsection anatomy) is in
`../../cell-shared/core/cell-results-discussion.md`; placement and compression are in
`../../cell-shared/core/main-text-discipline.md`. Load both with this file.

## Cell rules

| Rule | Source |
|---|---|
| Subsections with short, informative subheadings that state the finding | cell.md §3 |
| Model: "Factor X requires factor Y to function in process Z"; not "Analysis of factors X and Y using approach Q" | cell.md §3 |
| Similar wording in the figure titles; subheadings are reused as figure titles | cell.md §3, §4 |
| ≤ 7 main figures and/or tables | cell.md §2 |
| All figures cited in the main text, in numerical order | cell.md §4 |
| Supplemental items named Figure S1, Table S1, Data S1, Methods S1, Video S1 | cell.md §7 |
| Unpublished data and personal communications: in text only | cell.md §9 |
| Counts toward the limit of under 7,000 words | cell.md §2 |

Not specified by Cell (see cell.md): callout punctuation, number of subsections, a subheading
length, whether statistics may appear in the text.

## Procedure (craft guidance, not a journal rule)

1. **Fix the claim table** (workflow step 3). One row per display item.
2. **Write all subheadings first**, as a list. Read them in order with nothing else. They should
   read as the paper's argument. If two say the same thing, merge the rows.
3. **Copy each subheading to its figure title.** Shorten only if needed.
4. **Draft each subsection** with the five-part anatomy below.
5. **Place callouts** at the clause that states the observation, in order of first citation.
6. **Move procedure and statistics out** (to STAR Methods and legends).
7. **Count**; compare with the budget (about 500–600 words per display item).
8. **Run** `cell_text_check.py`: it warns on topic-style subheadings, callout order, lowercase
   panel letters and non-Cell supplemental naming.

## Subsection anatomy

| Part | Sentences | Content |
|---|---|---|
| Question | 1 | What the previous result left open |
| Approach | 1 | The experiment and why it decides the question; method named in a phrase |
| Result | 2–4 | Observation with direction and magnitude; callout to each panel |
| Control or alternative | 1–2 | The control that makes the result interpretable; pointer to Figure S |
| Inference | 1 | What this establishes; leads to the next question |

Example (invented):

> **Factor X is required for damage-scaled stem cell activation**
>
> Because factor X rose with the number of dying cells, we asked whether stem cells depend on
> it. We deleted *Fx* in the epithelium before irradiation. In control mice, the number of
> dividing stem cells increased with dose; after deletion, it stayed at baseline at every dose
> (Figures 2A and 2B), and repair was delayed by 2 days (Figure 2C). Stem cell numbers before
> injury were unchanged (Table 1), and a second deletion strategy gave the same result
> (Figure S2A). Factor X is therefore required for stem cells to scale their response to damage.

## Subheadings

| Test | Pass | Fail |
|---|---|---|
| Has a finite verb | "Receptor Y is required for stem cell activation" | "Receptor Y in stem cell activation" |
| States a result, not an activity | "Injury expands a receptor Y–high stem cell state" | "Single-cell analysis of injured intestine" |
| Could be wrong | "Factor X alone activates quiescent stem cells" | "Functional characterization of factor X" |
| Uses ledger terms | same names as the figure labels | a synonym used nowhere else |
| Strength matches the data | "is associated with" for correlation | "drives" without a perturbation |

Keep them short enough to serve as a figure title. Cell gives no length (see cell.md); about 60–90
characters works for both uses.

## Callouts

- Form used in this pack (craft; Cell fixes only the item names and capital panel letters):
  "Figure 1A", "Figures 1A and 1B", "Figures 1A–1C", "Figure S1A", "Table 1", "Table S1",
  "Video S1".
- First citations run in numerical order: Figure 1 before Figure 2 (Cell rule). Within a figure,
  cite panels in order where the logic allows (craft).
- Every main figure is cited (Cell rule). Every supplemental item is cited at least once, in the
  text or by "See also" in a legend (craft).
- Put the callout in parentheses at the end of the clause. Avoid "As shown in Figure 1A, …".

## What stays out of Results

| Item | Goes to |
|---|---|
| Reagents, doses, timings, instrument settings | STAR Methods |
| Test names, exact p values, n | legend, and Quantification and statistical analysis |
| How to read the plot | legend |
| Robustness and reagent validation | Figure S with a short pointer |
| Field-level interpretation, comparison with models | Discussion |
| Result that changes the reading of a claim | stays in Results, however inconvenient |

## Article-type variants (cell.md §2; emphasis is craft guidance)

| Type | Results must show |
|---|---|
| Research article | a conceptual advance through an escalating chain of claims |
| Resource | the technical advance with proof of principle, or the database with the biological insight it yields |
| Theory | the model and its testable predictions |
| Short article | the same logic in ≤ 4 display items |

## Deliverable

The subheading list alone (as an argument check), then the prose, the word count per subsection,
the callout order, and the list of items moved to STAR Methods or the supplement.
