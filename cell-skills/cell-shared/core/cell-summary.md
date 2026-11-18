# The Cell Summary

Adapted in structure from nature-skills (nature-shared/core/nature-abstract.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

Use this file to draft, compress or audit the Summary of a Cell research article.
Cell calls the abstract the "Summary" (cell.md §3, §10).

## 1. Cell rules (source: cell.md §3)

| Rule | Value |
|---|---|
| Form | one paragraph |
| Length | ≤ 150 words |
| Content | background/purpose; principal results with the approach/model system and main conclusions; broader significance |
| Citations | none |
| Abbreviations | no non-standard abbreviations |
| Novelty words | Cell discourages "novel" and "first" ("overused … difficult to verify"). This is a manuscript-wide style rule; apply it here first |
| Spelling | US |

Not specified by Cell (see cell.md): whether the Summary may use "we"; whether numbers or
statistics may appear; which abbreviations count as "standard"; how words are counted
(hyphenated terms, numbers with units).

Stage: cell.md §1 puts component rules at revision. Write to the limit from the first draft anyway;
a 150-word Summary is cheaper to write once than to cut later (craft guidance).

## 2. The four moves (Cell's own content list, in order)

`background/purpose → principal results with approach/model system → conclusions → broader significance`

The Summary is the shortest chain that makes the central finding understandable, credible and
consequential. It is not a compressed Introduction and not a list of the figures.

## 3. Sentence-by-sentence budget (craft guidance, not a journal rule)

Six or seven sentences. The budget sums to 150; stay under it.

| # | Move | Job | Words |
|---|---|---|---|
| 1 | Background | The biological problem, in terms a non-specialist biologist follows | 20–25 |
| 2 | Purpose / gap | The exact unknown ("how / whether / which … is unclear"). May merge with 1 | 10–20 |
| 3 | Approach + central result | Model system and approach, joined to the main finding ("Using A in B, we show that …") | 25–30 |
| 4 | Decisive support | The mechanism or the necessity/sufficiency result that makes 3 credible | 20–25 |
| 5 | Second support or boundary | Only if it changes how 3 is read (generality, human relevance, a limit) | 15–20 |
| 6 | Conclusion | What the results establish, one level above the data | 15–20 |
| 7 | Broader significance | Why it matters beyond the system studied; bounded | 10–20 |

Rules of thumb:

- At least 60% of the words belong to moves 3–6 (results and conclusion). Background over 45 words
  is too long.
- One main claim. A second claim earns a sentence only if the main claim needs it.
- Name the model system once (species, tissue or cell type). Cell asks for it.
- A number appears only when the magnitude is the finding.
- Sentences 6 and 7 may merge when the conclusion already states the significance.

## 4. Worked example (invented biology, 145 words)

> Tissues must replace damaged cells without exhausting their stem cell pools, but how stem
> cells sense the extent of damage is unclear. Here, we show that factor X, a secreted protein
> released by dying epithelial cells, sets the number of stem cells that enter the cell cycle
> after injury. Using lineage tracing and conditional deletion in the mouse intestine, we find
> that factor X binds receptor Y on quiescent stem cells and activates pathway Z in proportion
> to the number of dying cells. Loss of factor X or receptor Y prevents stem cell activation
> and delays repair, whereas excess factor X depletes the stem cell pool. Factor X levels also
> track with damage in human intestinal organoids. These findings identify a dose-dependent
> damage signal that matches stem cell output to tissue need and suggest that tuning this
> signal could improve repair without stem cell loss.

Map: sentence 1 = moves 1–2; sentence 2 = central result; sentence 3 = approach, model system,
mechanism; sentence 4 = necessity and the cost of excess; sentence 5 = human relevance;
sentence 6 = conclusion and significance.

## 5. What to remove

| Found in the draft | Why | Fix |
|---|---|---|
| Reference numbers, "(Author et al., 2020)" | Cell rule: no citations | Delete; state the fact without attribution |
| Lab shorthand or assay acronyms | Cell rule: no non-standard abbreviations | Spell out, or describe ("single-cell RNA sequencing") |
| "novel", "first", "for the first time" | Cell discourages them | State what was found; let the finding carry the news |
| "Here we performed / analyzed / profiled …" as the main verb | Reports activity, not a result (craft) | Lead with the finding; put the method in a "Using …" phrase |
| A sentence per figure | A list is not an argument (craft) | Keep the claim chain, drop same-level results |
| "These results provide insights into …" | Empty significance (craft) | Name what changes: a mechanism, a rule, a testable prediction |
| Second paragraph | Cell rule: one paragraph | Merge |

## 6. Alignment checks (craft guidance)

- The main claim in the Summary = the last sentence of the Introduction = the first Discussion
  paragraph, at the same strength.
- Every result in the Summary is shown in a main figure, not only in a supplemental figure.
- Verbs match the evidence: "show" for direct evidence, "suggest" for inference.
- Terms match the Terminology Ledger; no term appears in the Summary only.
- The Highlights and the eTOC blurb restate the same claim; they do not add a new one
  (see `../../cell-writing/references/highlights.md`, `etoc-blurb.md`).

## 7. Drafting procedure (craft guidance, not a journal rule)

Write the Summary after Results and Discussion are stable.

Inputs: the central claim (one-sentence argument), two or three decisive results from the claim
table, the model system and approach, the boundary from "Limitations of the study", ledger terms.

1. **Result sentence first.** "Here, we show that [actor] [does what] in [system]."
2. **Support.** One sentence for the mechanism; one for necessity/sufficiency or consequence.
3. **Gap.** One sentence ending in the exact unknown that the result sentence answers.
4. **Background.** At most one sentence before the gap, or merged with it.
5. **Conclusion and significance.** One sentence, two at most. Bounded.
6. **Count.** Over 150: cut background first, then the second support, then adjectives. Never
   cut the model system or the conclusion.
7. **Sweep** for citations, abbreviations, "novel"/"first", terms not in the ledger.
8. **Check** with `cell_text_check.py`: FAIL above 150 words, on citations, or on more than one
   paragraph; WARN on novelty words and possible abbreviations.

Compression moves:

| From | To |
|---|---|
| "It has been well established that tissues must …" | "Tissues must …" |
| "In this study, we used a combination of A and B to demonstrate that" | "Using A and B, we show that" |
| "plays an important role in the regulation of" | "regulates" |
| "Our findings provide important insights into the mechanisms by which" | "These findings identify" |
| Two results with the same subject in two sentences | one sentence with "and" or "whereas" |
| Abbreviation defined and used once | the spelled-out term only |

Abbreviations: Cell allows only standard ones but the pages read give no list (see cell.md).
Working rule: keep an abbreviation only if a biologist outside the subfield reads it without a
definition (DNA, RNA, ATP). Introduce an unfamiliar gene or protein symbol with what it is
("the secreted protein factor X").

Emphasis by article type (types and limits: cell.md §2; the emphasis is craft guidance):

| Type | Emphasis |
|---|---|
| Research article | finding → mechanism → consequence |
| Resource | what the resource is and covers → proof of principle → the biological insight it gave |
| Theory | the problem → the model → its testable predictions |
| Short article | the summary counts inside the 4,000-word total; keep it well under 150 |

Deliverable: the text, its word count with the counting method, a sentence → move map, and any
abbreviation kept or placeholder used.

## 8. Audit list

1. One paragraph, ≤ 150 words. Run `cell_text_check.py`.
2. No citations; no non-standard abbreviations; no "novel"/"first".
3. Model system and approach named once.
4. One main claim; each further sentence supports or bounds it.
5. Final sentence states a bounded significance, not a promise.
6. Claim strength equals that of the Introduction close and the Discussion opening.
