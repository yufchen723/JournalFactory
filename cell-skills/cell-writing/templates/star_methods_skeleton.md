<!--
Cell STAR Methods skeleton.
Adapted in structure from nature-skills (nature-writing/references/examples/method/section-skeleton.md),
Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

Cell rules (cell.md):
- Required at revision and for acceptance; not at first submission (s1, s8).
- Replaces "Experimental procedures"; part of the main article, not supplemental (s8).
- Methods never go in the supplement (s7).
- Not counted toward the 7,000-word main-text limit (s2).
- Key resources table: Cell Press Word template or webform; RRIDs for antibodies and genetically
  modified organisms (s8).
- AI used in the research itself is reported here (s3).
- Position in the manuscript: after Tables, before References (s3).
- "Resource availability" (Lead contact / Materials availability / Data and code availability) is a
  separate required manuscript component, listed after the Discussion (s3). It is not in this file.

SECTION HEADINGS BELOW: from the author guide, NOT re-read on 2026-11-18; confirm in the PDF (s8).
The key resources table columns and row categories are NOT in cell.md: use the Cell Press template
as supplied. The table here is a working inventory only.

Content notes under each heading are craft guidance, not journal rules.
Never invent an identifier, approval number, version or accession. Use [placeholders].
-->

# STAR Methods

## Key resources table

<!-- Working inventory. Transfer to the Cell Press template or webform. One resource per row.
     Sweep Results, legends and Method details: every named reagent, line, dataset and tool
     needs a row. Names must match the text. -->

| Resource (name as used in the text) | Type | Source | Identifier |
|---|---|---|---|
| [Anti-factor X antibody] | antibody | [vendor] | [Cat# needed]; [RRID needed] |
| [Fx conditional mouse line] | genetically modified organism | [source or "this paper"] | [RRID needed] |
| [Cell line] | cell line | [source] | [identifier] |
| [Dataset generated in this study] | deposited data | this paper | [repository: accession] |
| [Public dataset reused] | deposited data | [reference] | [repository: accession] |
| [Analysis code] | software | this paper | [DOI] |
| [Software] | software | [developer or reference] | [version; URL or RRID] |

## Experimental model and study participant details

<!-- Who or what was studied. Procedures go under Method details. -->

### [Mice / other organism]

[Strain and source; sex; age; number; housing; genotype; ethics approval body and protocol
number: [needed].]

### [Cell lines / primary cultures / organoids]

[Origin; sex of donor if known; culture conditions; authentication and contamination testing:
[needed].]

### [Human participants or samples]

[Number; relevant characteristics; consent; approving body and approval number: [needed].
Delete if not applicable.]

## Method details

<!-- One subheading per technique, in order of first use in Results. Enough detail to repeat:
     amounts, times, temperatures, instruments and settings, software versions, non-default
     parameters. Cite a published protocol and state every change. No results. -->

### [Technique 1, e.g., tissue injury model]

[Procedure.]

### [Technique 2, e.g., immunofluorescence and imaging]

[Procedure. Image acquisition settings. Any adjustment not applied to the whole image is
explained here and in the legend (cell.md s5).]

### [Technique 3, e.g., sequencing library preparation]

[Procedure.]

### [Computational analysis]

[Input -> processing steps with parameter values -> output. Software and versions as in the key
resources table.]

### [Use of AI tools in the research]

[Only if AI was used in the research itself (cell.md s3). Delete if not applicable.]

## Quantification and statistical analysis

<!-- Must agree with every legend: Cell requires each legend to state the tests, the meaning of
     asterisks, replicate numbers and error-bar definitions (cell.md s4). -->

- Software: [name, version].
- Definition of n: [what n is for each type of experiment: animals, donors, cells, fields,
  independent experiments].
- Biological and technical replicates: [how each is defined in this paper].
- Summary statistics: [center and dispersion used, e.g., mean ± SEM; where individual points
  are shown].
- Tests: [test per comparison type; one- or two-sided; correction for multiple comparisons].
- Significance threshold and symbols: [e.g., *p < 0.05, **p < 0.01, ***p < 0.001].
- Exclusions: [criteria; whether any data were excluded].
- Randomization, blinding, sample-size determination: [what was done, or a statement that none
  was done].

## Additional resources

<!-- Optional (cell.md s8). External resources created for this paper, e.g., a website.
     Delete if unused. -->

[Description and URL.]

<!--
Conversion checklist (from a free-text methods section):
[ ] Section renamed "STAR Methods"
[ ] Every resource in text and legends has a row in the key resources table
[ ] Antibodies and genetically modified organisms carry RRIDs (Cell rule, s8)
[ ] No methods left in the supplement (Cell rule, s7)
[ ] Statistics text gathered under Quantification and statistical analysis
[ ] n, tests and error terms agree with every legend (Cell rule for legends, s4)
[ ] Manuscript has Resource availability with three subsections (Cell rule, s3)
[ ] Headings confirmed against the STAR Methods author guide PDF (not re-read; s8)
-->
