# Terminology Ledger (Cell)

Adapted in structure from nature-skills (nature-shared/core/terminology-ledger.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

One name for one thing, fixed before drafting. This file is preventive; `consistency-sweep.md`
finds drift in a draft that already exists.

## 1. Cell rules that the ledger enforces

| Item | Cell form | Source |
|---|---|---|
| Supplemental items | Figure S1, Table S1, Data S1, Methods S1, Video S1. Never "Supplementary Figure 1" | cell.md §7 |
| Supplemental figure title | "Figure S1. [title], related to Figure 1" | cell.md §7 |
| Pointer from a main legend | "See also Figure S1" | cell.md §4 |
| Primary supplemental PDF | "Document S1" | cell.md §7 |
| Panel labels | capital letters (A, B, C) | cell.md §5 |
| Main tables | Table 1, Table 2; no "Table 1A/1B" | cell.md §4 |
| Methods section name | STAR Methods (not "Experimental procedures", not "Methods") | cell.md §8 |
| Abstract name | Summary | cell.md §3 |
| Genes and proteins | gene symbols italic, proteins roman | cell.md §3 |
| Abbreviations | minimal; defined at first use; avoided in the title; none in Highlights; no non-standard ones in the Summary | cell.md §3, §6 |
| Spelling | US | cell.md §3 |
| Novelty words | "novel", "first" discouraged | cell.md §3 |
| Section names | Summary, Introduction, Results, Discussion, Limitations of the study, Resource availability (Lead contact, Materials availability, Data and code availability), Acknowledgments, Author contributions, Declaration of interests | cell.md §3 |

Not specified by Cell (see cell.md): the exact in-text callout pattern for panels ("Figure 1A",
"Figures 1A and 1B", "Figures 1A–1C"); whether "Figure" may be abbreviated; species-specific
gene and protein capitalization; number and unit style; the serial comma. For these, pick one
form, record it in the ledger, and keep it. The defaults in section 3 are craft guidance.

## 2. Build the ledger on first contact

Before drafting or editing, extract every recurring term:

- genes, proteins, alleles, mouse lines, cell lines, species
- cell types and cell states (and what defines each)
- methods, assays, datasets, cohorts, software
- conditions and groups (control names, treatment names, time points)
- metrics, units, statistical symbols
- abbreviations with their full forms
- figure, table and supplemental item names

Show a compact table with the first output:

| Canonical term | First-use form | Variants seen | Decision |
|---|---|---|---|
| factor X (protein) | factor X | "FactorX", "FX" | "factor X"; no abbreviation |
| *Fx* (mouse gene) | *Fx* | "Fx", "FX gene" | italic for gene and transcript; roman for protein |
| receptor Y–high stem cells | receptor Y–high (Y^hi) stem cells | "Y+ cells", "Y-high SCs" | "Y^hi stem cells" after first use |
| single-cell RNA sequencing | single-cell RNA sequencing (scRNA-seq) | "scRNAseq", "single cell RNA-seq" | spell out once, then "scRNA-seq" |
| control group | control | "WT", "vehicle", "untreated" | name each control by what it is; never interchange |

Flag collisions: one concept under two names, or one name for two concepts. Ask the author only
when the choice is ambiguous or field-sensitive; otherwise adopt the most frequent form and say so.

## 3. Default forms where Cell is silent (craft guidance, not a journal rule)

| Item | Default | Reason |
|---|---|---|
| Panel callout | "Figure 1A"; "Figures 1A and 1B"; "Figures 1A–1C"; "Figure S1A" | matches the capital panel labels and the "Figure S1" naming |
| "Figure" | spelled out everywhere | cell.md writes "Figure 1", "Figure S1", "See also Figure S1" |
| Gene/protein case | follow the organism's nomenclature authority | Cell only fixes italic versus roman |
| Statistics symbols | lowercase "p", "n" as in the cell.md legend example ("*p < 0.05") | keeps legends and text identical |
| Error terms | "SEM", "SD" written the same way in every legend | cell.md example: "mean ± SEM" |
| Self-reference | "this study" throughout | avoids "this work/paper/report" drift |

## 4. Where an abbreviation may appear

| Location | Rule | Source |
|---|---|---|
| Title | avoid; no jargon or uncommon abbreviations | cell.md §3 |
| Summary | no non-standard abbreviations | cell.md §3 |
| Highlights | no abbreviations | cell.md §6 |
| Main text | minimal; define at first use | cell.md §3 |
| Legends | define again if a reader may start at the figure | craft guidance |
| eTOC blurb | not specified by Cell (see cell.md); write for a general scientific audience | cell.md §6 |

Keep an abbreviation only if the term appears at least three times in the main text
(craft guidance). Otherwise spell it out and save the reader the lookup.

## 5. Lock and enforce

- Use only canonical forms. Do not vary terms for style.
- Define each abbreviation once in the main text; then use the short form.
- Results subheadings and figure titles use ledger terms, because Cell reuses one as the other.
- Highlights, eTOC blurb, cover letter and graphical-abstract labels use the same terms.
- If the author renames a term, change every occurrence in the manuscript, legends, supplemental
  legends, STAR Methods and front-matter file, then update the ledger.

## 6. Do not invent terms

Do not coin names for the author's cell states, factors or methods. If a name is missing or used
in two ways, flag it and ask. Never fill the gap with a guessed name.
