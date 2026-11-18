# Discussion and "Limitations of the study" — drafting procedure

Adapted in structure from nature-skills (nature-shared/core/discussion-argument-language.md and nature-writing/static/fragments/section/discussion.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

The shared contract (paragraph jobs, repetition test, limitation anatomy) is in
`../../cell-shared/core/cell-results-discussion.md` §5–§6. Load it with this file.

## Cell rules (source: cell.md §3)

- The Discussion gives implications and context. It is not a repeat of Results.
- It includes a subsection headed "Limitations of the study", specific to the paper.
- It counts toward the limit of under 7,000 words (cell.md §2).
- "novel" and "first" discouraged; US spelling; no footnotes.

Not specified by Cell (see cell.md): a length for the Discussion or for the limitations
subsection; whether other subheadings are allowed; whether a concluding paragraph is expected;
where in the Discussion the subsection sits. This pack puts it last (craft guidance).

## Inputs needed

| Input | Used for |
|---|---|
| The Introduction's gap sentence | paragraph 1 answers it |
| The claim table | what may be synthesized; nothing else |
| The closest prior models and findings | positioning paragraphs |
| Every boundary noted while drafting Results | the limitations subsection |
| Reviewer or co-author objections not resolved by data | the limitations subsection |

## Procedure (craft guidance, not a journal rule)

1. **Answer the question.** Paragraph 1 states the answer to the Introduction's gap in two to
   four sentences, one level above the data. No figure callouts are needed here.
2. **List what changes.** For each prior model or finding the paper touches, write one line:
   explains / extends / contradicts / is consistent with, and why. Keep the two or three lines
   that matter; each becomes a paragraph.
3. **State one implication and one prediction.** The prediction must be testable and follow
   from the mechanism shown.
4. **Write "Limitations of the study".** Use the three-part anatomy: what is not shown, which
   claim it bounds, how it could be resolved.
5. **Run the repetition test.** Delete or convert every sentence that could sit in Results.
6. **Check verbs** against `../static/core/stance.md` §4. The Discussion may extend, but it marks
   the extension ("suggests", "may").
7. **Count** against the budget (900–1,200 words including limitations is a working target, not
   a Cell number).

## Paragraph openers

| Job | Weak | Strong |
|---|---|---|
| Answer | "In this study, we performed lineage tracing and …" | "Stem cells scale repair to injury by reading a signal whose amount is set by the number of dying cells." |
| Positioning | "Our results are consistent with previous studies." | "Niche signals were known to permit activation; our data add the variable that sets its extent." |
| Contradiction | "In contrast to others, we found …" | "Two studies reported activation without cell death; both used doses at which factor X is already saturating in our assay." |
| Implication | "This has important implications." | "A dose-dependent death signal predicts that chronic low-level damage will deplete stem cells over time." |

## Recap versus synthesis

| Recap (cut) | Synthesis (keep) |
|---|---|
| "We showed that factor X increased with dose (Figure 1A)." | "Because factor X scales with cell death, the tissue has a direct readout of how much repair is needed." |
| "Deletion of receptor Y blocked activation." | "The requirement for receptor Y places damage sensing in the stem cell itself, not in the niche." |

One clause of recap may anchor an interpretation. A sentence of recap may not.

## "Limitations of the study"

Heading: exactly `Limitations of the study` (Cell rule). Length: one paragraph, three to five
sentences, about 80–150 words (craft guidance).

Checklist of sources. Take only those that bound a claim in this paper:

| Source | Question to ask |
|---|---|
| Model system | Mouse only? Cell line only? One strain, sex or age? |
| Perturbation | Whole-tissue deletion? Acute versus chronic? Possible compensation? Off-target effects excluded how? |
| Measurement | Indirect readout? Resolution limit? Antibody or reporter validated how? |
| Sample | How many donors or animals? One cohort? |
| Inference | Which step in the causal chain is correlative? |
| Generality | Tested in one tissue or condition only? |
| Mechanism | Which link is missing (adaptor, direct target, kinetics)? |

Sentence pattern:

> We [did A], so [claim B] is limited to [scope]; [experiment C] would test [the open point].

Example (invented):

> **Limitations of the study**
>
> We deleted factor X in all epithelial cells, so the source cell type is not resolved;
> lineage-specific deletion would test whether enterocytes or secretory cells supply the
> signal. Human data come from organoids of four donors and do not address variation between
> individuals. We show that pathway Z is activated downstream of receptor Y but did not
> identify the adaptor that links them, and we tested irradiation only, so whether the same
> signal reports chemical or infectious damage remains open.

Reject:

- generic statements that fit any paper ("further studies are needed", "sample size was limited"
  without the number and the claim it affects);
- limitations that contradict a stronger sentence elsewhere in the paper (fix the stronger sentence);
- a list of future projects unrelated to a claim;
- arguments against an anticipated reviewer.

## Common faults

| Fault | Fix |
|---|---|
| Opens with a restatement of the Introduction | open with the answer |
| One paragraph per figure | organize by implication |
| New data or analyses | move to Results, or delete |
| Speculation in the indicative mood | mark with "may", "we propose" |
| Clinical promise from a mouse experiment | bound it; name the missing step |
| Limitations placed in the last sentence of a paragraph, without the heading | use the required subsection |
| Ends on "future studies will …" | end on the bounded conclusion or the limitations subsection |

## Deliverable

The Discussion with its limitations subsection, the word count, the list of prior work
positioned (as placeholders `[ref: …]` where a citation is needed), and a line confirming that
the opening answers the Introduction's gap sentence.
