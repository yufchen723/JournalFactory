# Multi-panel evidence architecture for a Cell paper

Adapted in structure from nature-skills (nature-figure/references/multipanel-evidence-architecture.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

Craft guidance, not journal policy, except where marked "Cell rule". The source reasoning was
written for Nature figures; the logic carries over, the numbers do not.

## The constraint that shapes everything

**Cell rule:** at most 7 figures and/or tables in the main paper, under 7,000 words including
main legends. Supplemental figures are recommended to stay at or below 20 and each is tied to a
main figure ("related to Figure N").

So a Cell figure is denser than a Nature figure, and the supplement is organised *by main figure*.
Plan each main figure together with its Figure S partner(s).

## Start from the figure-level claim

```text
Results subheading (= figure title):
Figure-level claim:
What could overturn it:
Decisive evidence:
Panels:
  A — question | evidence role | comparison needed
  B — ...
Moved to Figure S (related to this figure):
```

One figure = one claim is the default. Several findings may share a figure when all are needed to
establish, qualify or bound the same claim. A panel that can vanish without weakening the claim
goes to Figure S or is deleted.

## Panel roles

Choose the smallest sufficient set; give each panel a different job.

| Role | Question it answers |
|---|---|
| Setup or schematic | What system, design or workflow is tested? |
| Representative example | What does it look like in one concrete case? |
| Primary quantification | Does the effect exist across the cohort? |
| Control or baseline | Does it beat the credible alternative? |
| Decomposition | Which component, cell type or region carries it? |
| Stratification | Does it hold across patients, sections, conditions? |
| Orthogonal validation | Is it recovered by another assay or data type? |
| Perturbation | Does it change as predicted when the proposed cause is disrupted? |
| Boundary | Where does it weaken or fail? |
| Mechanism | What bounded explanation is supported? |

Weak: four panels that redraw one result under four metrics.
Strong: design → decisive comparison → who carries it → orthogonal check → perturbation.

**Pairing rule for image + number:** every representative image is followed by its quantification
across all samples in the same figure, with n stated. An image alone is an anecdote; Cell
reviewers ask for the count.

## Evidence-chain archetypes

- **Capability ladder (technology figure).** What it is → it works (quality metrics) → it beats or
  matches the alternative on the same tissue → it holds under harder conditions → what new
  measurement it makes possible. Cell's Resource format asks for exactly this: a proof of principle
  that the method opens questions in several areas (cell.md §2).
- **Scale to instance (atlas figure).** Cohort map → composition → spatial organisation →
  one resolved structure → a representative case that explains the aggregate.
- **Discovery sequence (mechanism figure).** Observation → candidate → association across the
  cohort → orthogonal assay → perturbation → rescue or prediction.
- **Validation envelope (claim under attack).** Establish → control → replicate in an independent
  cohort → stress-test → bound.

## The seven-figure arc

Across figures, each one asks a deeper question than the one before. A common shape:

```text
Fig 1  What is new here: the system or technology, and that it works
Fig 2  The landscape it reveals
Fig 3  The organising principle in that landscape
Fig 4  Who talks to whom / what regulates it
Fig 5  A specific mechanism
Fig 6  Functional or clinical consequence
Fig 7  Perturbation that tests the mechanism; model
```

This is an archetype, not a template. If two figures can both be summarised as "the atlas shows X",
merge them or sharpen the later one around a discriminating test. Seven is a ceiling, not a target.

## Visual hierarchy follows evidence hierarchy

- The decisive panel is the largest, or sits top-left or centre.
- Controls and robustness panels are small.
- A schematic earns main-figure space only in Figure 1 or where the design cannot be understood
  without it.

## Main figure or Figure S?

| Keep in the main figure | Move to Figure S (related to Figure N) |
|---|---|
| The panel the claim rests on | The same result in every sample |
| One representative image + cohort quantification | Additional representative images |
| The decisive control | Parameter sweeps, QC, alternative thresholds |
| The orthogonal validation | A second metric that tells the same story |
| The perturbation result | Dose series, time courses beyond the key point |

Methods schematics and extended methods never go to the supplement text: Cell puts all methods
in STAR Methods (cell.md §7).

## Audit before drawing

1. Can each panel's role be named in three words?
2. Do two panels share a role? Merge or demote one.
3. Is the replicate unit the same across comparable panels?
4. Does the figure title state a finding, and does it match the Results subheading?
5. Does every image have a scale bar and a quantification?
6. Is everything displaced accounted for in a Figure S "related to" this figure?
7. Does the next figure ask a different question?
