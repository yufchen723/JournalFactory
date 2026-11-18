# Polishing to Cell style

Adapted in structure from nature-skills (nature-polishing/SKILL.md and references/style-guardrails.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

Use this file for language-only edits of existing prose and as the last pass on any draft.
Polishing changes wording. It does not change claims, numbers, references or the order of the
argument. If a sentence cannot be fixed without changing its claim, flag it.

## 1. Cell style rules (source: cell.md §3 unless noted)

| Rule | Apply as |
|---|---|
| US spelling | "analyze", "color", "tumor", "signaling", "labeled", "center", "program", "gray" |
| Abbreviations minimal | spell out anything used fewer than about three times (the threshold is craft) |
| Abbreviations defined at first use | define once in the main text; do not redefine |
| Abbreviations avoided in the title | rewrite the title around what the thing is |
| No non-standard abbreviations in the Summary | spell out assay names and lab shorthand |
| No abbreviations in Highlights | cell.md §6 |
| Gene symbols italic, proteins roman | *Fx* (gene, transcript, allele); Fx or factor X (protein) |
| "novel" and "first" discouraged ("overused … difficult to verify") | delete; state the finding |
| No footnotes outside the author list and tables | move the content into the sentence or delete |
| eTOC blurb in the third person | cell.md §6 |
| Supplemental items: Figure S1, Table S1, Data S1, Methods S1, Video S1 | never "Supplementary Figure 1" (cell.md §7) |
| Section names | Summary, STAR Methods, Limitations of the study, Resource availability, Declaration of interests |
| Panel letters capital | Figure 1A, not Figure 1a (cell.md §5 fixes the labels; the callout form is craft) |
| References | numbered by first citation, superscript; "et al." only after 10 authors in the list (cell.md §9) |

Not specified by Cell (see cell.md): the serial comma; number style (numerals versus words);
unit spacing; hyphenation; capitalization of headings; tense by section; use of "we";
species-specific gene nomenclature; whether "Figure" may be abbreviated; "data are" versus
"data is" (the cell.md example reads "Data are represented as mean ± SEM"). For each, choose one
form, record it in the Terminology Ledger, and apply it everywhere.

## 2. US spelling: common conversions

| British | US |
|---|---|
| -ise / -isation (characterise, localisation) | -ize / -ization |
| -yse (analyse, catalyse) | -yze |
| -our (tumour, colour, behaviour) | -or |
| -re (centre, fibre, litre) | -er |
| -lled / -lling (labelled, signalling, modelling) | -led / -ling |
| -ogue (analogue, catalogue) | -og |
| ae / oe (haematopoietic, oestrogen, foetal, anaemia) | e (hematopoietic, estrogen, fetal, anemia) |
| grey, programme, whilst, towards, sulphur | gray, program, while, toward, sulfur |
| aetiology, oedema, leukaemia, ischaemia | etiology, edema, leukemia, ischemia |

Do not convert: proper names, journal titles, quoted text, database field names, gene names.

## 3. Gene and protein typography

Cell rule: gene symbols italic, proteins roman (cell.md §3). Case conventions by species are
not specified by Cell (see cell.md); follow the organism's nomenclature authority and record
the choice in the ledger.

| Entity | Typography |
|---|---|
| Gene, allele, transcript, locus, genotype | italic |
| Protein, complex, activity | roman |
| "expression of *Fx*" (transcript) versus "Fx levels" (protein) | choose by what was measured |
| Reporter and Cre lines, genotypes | italic for the allele designation |
| Knockout described as loss of the protein | "Fx-deficient" roman; "*Fx*^−/−^" italic |

Typical slips: a roman gene symbol in a figure title; an italic protein in a legend; one
symbol used for gene and protein in the same sentence without distinction.

## 4. Novelty and overclaim sweep

| Remove or replace | With |
|---|---|
| novel, new (as a claim), first, for the first time | nothing; or "previously unrecognized" only if the Introduction documents the gap |
| unprecedented, remarkable, striking, dramatically | the measured size of the effect |
| clearly, obviously, undoubtedly | nothing |
| prove, conclusively | show, demonstrate |
| key, critical, crucial, essential (without a loss-of-function result) | "contributes to", or the result itself |
| master regulator, paradigm shift, breakthrough | the mechanism in plain words |

The first row is a Cell rule (cell.md §3). The rest is craft guidance.

## 5. Sentence-level edits (craft guidance, not a journal rule)

- One main proposition per sentence. Split at "and" when two results share a sentence.
- Subject and verb close together; the new information at the end.
- Active voice for what the authors did and found; passive is acceptable in STAR Methods.
- Past tense for what was done and observed; present tense for what the result establishes.
- Delete openers: "It is worth noting that", "Interestingly", "Importantly", "As expected".
- "(Figure 1A)" at the clause end replaces "As shown in Figure 1A".
- Replace nominalizations: "performed an analysis of" → "analyzed".
- Numerals with units; one space between value and unit; the same unit for the same quantity.
- "Compared with" for comparisons; "respectively" only when the pairing would otherwise be unclear.
- "Significant" only for a statistical result; otherwise "substantial", "marked".
- "Which" after a comma, "that" without.

## 6. What polishing must not touch

- Numbers, units, n, p values, doses.
- The strength of a claim (do not turn "suggests" into "shows", or the reverse).
- Reference numbers and their order.
- Ledger terms (do not introduce synonyms for variety).
- Quoted Cell wording in required headings ("Limitations of the study", "Lead contact").
- Text the author marked as fixed.

If the source has a factual or logical problem, report it in the notes; do not repair it silently.

## 7. Order of the polishing pass

1. Ledger: build or load it; fix term variants.
2. Cell rules of section 1 (spelling, abbreviations, typography, novelty words, naming).
3. Sentence-level edits of section 5.
4. Recount against limits; rerun `cell_text_check.py`.
5. For a whole manuscript, finish with `../../cell-shared/core/consistency-sweep.md`.

## 8. Output

Return the edited text and a short change log:

| # | Location | Before | After | Reason (Cell rule §N / craft) |
|---|---|---|---|---|
| 1 | Summary, sentence 2 | "a novel factor" | "a secreted factor" | Cell rule, cell.md §3 |
| 2 | Results, paragraph 3 | "tumour" | "tumor" | Cell rule, cell.md §3 |
| 3 | Discussion, paragraph 1 | "It is important to note that X" | "X" | craft |

List separately anything flagged but not changed (possible overclaim, unclear antecedent,
number that does not match a legend).
