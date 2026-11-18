# Consistency Sweep (Cell)

Adapted in structure from nature-skills (nature-shared/core/consistency-sweep.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

A retrospective audit of a draft that already exists. `terminology-ledger.md` fixes names before
drafting; this file finds the drift a revised manuscript has accumulated.

Use it before submission, after a revision round, or when the front-matter file, cover letter
and manuscript were edited separately. For a local edit, check only the affected terms, numbers
and callouts; widen the sweep when those show drift.

## 1. Sweep, then inspect

Count variants mechanically, then read each context before changing anything. Raw counts
over-report: sentence-initial capitals, first-use expansions and required inflections are
legitimate.

Mechanical first pass:

```bash
python ../../cell-writing/scripts/cell_text_check.py manuscript.md
python ../../cell-writing/scripts/cell_text_check.py --highlights highlights_etoc.md
```

The checker covers the countable Cell limits and the naming patterns marked "script" below.
Its findings are prompts to inspect, not automatic corrections.

## 2. Axes that are Cell rules

| Axis | Look for | Cell form | Source | Script |
|---|---|---|---|---|
| Supplemental naming | "Supplementary Figure 1", "Supplementary Table", "Extended Data Fig." | Figure S1, Table S1, Data S1, Methods S1, Video S1 | cell.md §7 | yes |
| Supplemental titles | S-figure title without its parent | "Figure S1. …, related to Figure 1" | cell.md §7 | yes |
| Legend pointers | main legend with supplemental support but no pointer | "See also Figure S1" | cell.md §4 | yes |
| Panel letters | "Figure 1a" in text against "A" in the figure | capital letters | cell.md §5 | yes |
| Callout order | Figure 4 cited before Figure 3; a figure never cited | all cited, in numerical order | cell.md §4 | partly |
| Subheading and figure title | Results subheading and figure title that state different things | similar wording | cell.md §3, §4 | no |
| Legend statistics | panel with asterisks but no test or p definition; no n; undefined error bars | all stated per legend | cell.md §4 | heuristic |
| Scale bars | image panel with no scale bar in image or legend | every scale bar defined | cell.md §4, §5 | heuristic |
| Section names | "Abstract", "Methods", "Experimental procedures"; a Discussion without "Limitations of the study" | Summary, STAR Methods, Limitations of the study | cell.md §3, §8 | yes |
| Spelling | "-ise", "-our", "analyse", "tumour" in a US text | US spelling | cell.md §3 | no |
| Gene and protein typography | gene symbol in roman, protein in italic | genes italic, proteins roman | cell.md §3 | no |
| Abbreviations | used before defined; defined twice; in the title or Highlights | defined at first use; absent from title and Highlights | cell.md §3, §6 | heuristic |
| Novelty words | "novel", "first", "for the first time" | remove | cell.md §3 | Summary and title |
| Footnotes | footnotes in the main text | only in the author list and tables | cell.md §3 | no |
| Main tables | "Table 1A", merged cells, color | one value per cell, black and white, lowercase superscript footnotes | cell.md §4 | no |
| Reference order | citation numbers out of order of first use | numbered by first citation | cell.md §9 | no |

## 3. Axes that are craft guidance (not journal rules)

| Axis | Look for | Typical real finding |
|---|---|---|
| Group names | every name for one condition | "control", "WT", "vehicle" used for the same group, or for three different groups |
| Cell-state names | one population under several labels | "Y^hi cells", "activated stem cells", "cluster 3" for the same cells |
| Reagent and line names | text against the key resources table | antibody clone in a legend not in the table |
| Units and doses | the same quantity in two units | "10 µM" in the legend, "0.01 mM" in STAR Methods |
| Number precision | one metric at two precisions | "2.3-fold" in the text, "2.31-fold" in the legend |
| Statistical terms | "SD", "s.d.", "Std"; "SEM" versus "SE" | mixed forms across legends |
| Tense | results in past tense, general conclusions in present | a list mixing both |
| Self-reference | "this study", "this work", "this paper", "this report" | one stray variant |
| Hyphenation | "stem-cell activation" versus "stem cell activation" | mixed compound modifiers |

## 4. Numbers must reconcile

- **Every n is derivable.** Animals, donors, cells and replicates in the Summary and Results
  must equal the legends, which must equal STAR Methods (Quantification and statistical
  analysis). Cell requires replicate numbers in legends (cell.md §4); the three places must agree.
- **One value, one precision, everywhere.** Check each number that appears in more than one of:
  Summary, Results, legend, Highlights, eTOC blurb, cover letter.
- **Biological versus technical replicates.** A legend that says "n = 3" must say three of what.
  The same word ("replicate") must not mean both in one paper.
- **Counts add up.** If 12 mice are split into groups of 5 and 6, find the missing animal or state
  the exclusion in STAR Methods.

## 5. Claims against the paper's own data

- A Results subheading states a finding (cell.md §3); check that the figure under the same title
  shows it at that strength.
- "All", "always", "completely", "specifically": find the panel. Name the exception if there is one.
- "Required" needs a loss-of-function result; "sufficient" needs a gain-of-function result;
  "drives" or "causes" needs both or a direct perturbation. Otherwise use "is associated with".
- Check for underclaiming: a Discussion that says "may contribute" where the Results show necessity.
- Summary, Highlights, eTOC blurb, Introduction close and Discussion opening must make the same
  claim at the same strength.
- Every item in "Limitations of the study" must not be contradicted by a stronger claim elsewhere.

## 6. Cross-document synchronization

After any change to the manuscript, re-check the files that quote it:

| File | What must match |
|---|---|
| Highlights and eTOC blurb (one Word file, cell.md §6) | terms, claim strength, numbers |
| Graphical abstract | terms and the single point shown (cell.md §6) |
| Key resources table | every reagent, line, dataset and software named in text and legends |
| Supplemental information index | every Figure S, Table S, Data S, Video S cited in the text; Document S1 first (cell.md §7) |
| Cover letter and response letter | title, claim wording, figure numbers |

## 7. Order of operations

1. Numbers and claims (sections 4 and 5). Fix content before wording.
2. Cell naming and structure axes (section 2).
3. Terminology and style axes (section 3).
4. Callout order and supplemental index, last, because earlier fixes renumber items.
5. Re-run the checker; recount the main text (the limit is under 7,000 words, cell.md §2).

Run more than one pass. Fixing one axis exposes the next.

## 8. Report format

| # | Location | Found | Rule type | Fix |
|---|---|---|---|---|
| 1 | Results, paragraph 4 | "Supplementary Figure 2B" | Cell rule (cell.md §7) | "Figure S2B" |
| 2 | Figure 3 legend | "n = 3" without unit of replication | Cell rule (cell.md §4) | "n = 3 mice per group" |
| 3 | Discussion, paragraph 2 | "vehicle" for the group called "control" elsewhere | craft | use "control" |

Always state the rule type, so the author can tell a journal requirement from a preference.
