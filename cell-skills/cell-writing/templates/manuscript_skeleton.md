<!--
Cell research article: manuscript skeleton.
Adapted in structure from nature-skills (nature-writing/templates/), Apache-2.0;
Cell rules from cell-shared/journal-formats/cell.md (read on cell.com 2026-11-18).

Component order: cell.md section 3 (required at revision; initial submission is free format, section 1).
Limits in comments are Cell rules with their cell.md section. Lines marked "craft" are not journal rules.
Check with:  python scripts/cell_text_check.py this_file.md
Final format: editable, preferably Word; LaTeX also needs a PDF (section 3).
Whole paper: main text under 7,000 words INCLUDING main figure legends; STAR Methods, supplemental
legends and references excluded; no more than 7 figures and/or tables (section 2).
Style: US spelling; abbreviations minimal and defined at first use; gene symbols italic, proteins
roman; no footnotes outside the author list and tables; "novel" and "first" discouraged (section 3).
-->

# Title

<!-- about 10-12 words; <= 145 characters with spaces; no jargon or uncommon abbreviations;
     conveys the broad conceptual significance (s3). -->
[Title]

# Author list

<!-- Not specified in detail by cell.md. Footnotes are allowed here (s3). -->
[First Author,^1^ Second Author,^1,2^ and Corresponding Author^1,3,*^]

# Affiliations and footnotes

^1^[Department, Institution, City, State/Region, Postal code, Country]
^3^Lead contact

# Contact information

<!-- Exactly one lead contact, who must be a corresponding author (s3). -->
*Correspondence: [email]

# Summary

<!-- One paragraph; <= 150 words; background/purpose -> principal results with approach/model
     system and main conclusions -> broader significance; no citations; no non-standard
     abbreviations (s3). Budget per sentence: cell-shared/core/cell-summary.md (craft). -->
[Summary paragraph]

# Keywords

<!-- Up to 10, comma separated (s3). -->
[keyword 1, keyword 2, keyword 3]

# Introduction

<!-- Succinct; pertinent background; NO subheadings; ends with a brief statement of what was
     achieved (s3). Craft target 500-800 words. References: superscript numbers in order of first
     citation (s9). -->
[Paragraph 1: the biological problem and the specific phenomenon.]

[Paragraph 2: what is established.]

[Paragraph 3: the exact unknown.]

[Final paragraph: "Here, we show that ..." - what was achieved.]

# Results

<!-- Subsections with short, informative subheadings that STATE THE FINDING, e.g. "Factor X
     requires factor Y to function in process Z"; reuse the wording as figure titles (s3, s4).
     All figures cited in numerical order (s4). Supplemental callouts: Figure S1, Table S1,
     Data S1, Methods S1, Video S1 (s7). Craft: one subsection per display item, <= 7. -->

## [Finding 1, stated as a sentence]

[Question -> approach -> result (Figure 1A) -> control (Figure S1A) -> inference.]

## [Finding 2, stated as a sentence]

[Text (Figures 2A and 2B; Table S1).]

## [Finding 3, stated as a sentence]

[Text (Figure 3A).]

# Discussion

<!-- Implications and context; not a repeat of Results (s3). -->
[Paragraph 1: the answer to the Introduction's question.]

[Paragraphs 2-4: what the answer changes; relation to prior work; a prediction.]

## Limitations of the study

<!-- Required subsection; specific to this paper (s3). Craft: what is not shown, which claim it
     bounds, how it could be resolved. -->
[Limitations paragraph]

# Resource availability

<!-- Required; three subsections (s3). Exact statement wording: journal-policies page, not read
     (see cell.md header). Do not invent accession numbers or DOIs. -->

## Lead contact

[Requests for further information and resources should be directed to the lead contact, Name (email).]

## Materials availability

[Statement on newly generated materials.]

## Data and code availability

[Where the data are deposited, with accession numbers. Where the code is, with DOI. Whom to ask
for additional information.]

# Acknowledgments

[Funding and thanks.]

# Author contributions

<!-- Required; CRediT taxonomy encouraged; initials (s3). -->
[Conceptualization, A.B. and C.D.; methodology, ...; investigation, ...; writing - original draft, ...]

# Declaration of interests

<!-- Required; must match the form; if none: "The authors declare no competing interests." (s3). -->
[The authors declare no competing interests.]

# Declaration of generative AI and AI-assisted technologies

<!-- Only if generative AI was used in preparing the manuscript (not for grammar/spelling/
     reference tools). AI used in the research itself is reported in STAR Methods (s3).
     Delete this section if not applicable. Exact wording: journal-policies page, not read. -->
[Statement, or delete the section.]

# Supplemental information titles and legends

<!-- Index of supplemental items, Document S1 first (s7). Titles name the parent item:
     "Figure S1. [title], related to Figure 1". Recommended <= 20 supplemental figures. Legends
     follow the same rules as main legends (s4). Not counted toward 7,000 words (s2).
     Methods never go in the supplement (s7). Tables longer than 3 pages: Excel (s7). -->

Document S1. Figures S1-S[n] [and Tables S1-S[n]]

Table S[n]. [Title], related to Figure [N]

Figure S1. [Title], related to Figure 1
(A) [Panel.] [n; measure and error bars; test and asterisk meanings; scale bars.]

# Figure titles and legends

<!-- Counted toward 7,000 words (s2). Each figure: a brief title for the whole figure, no panel
     citations in it; then each panel. Must state: statistical test(s) and the p value each
     asterisk stands for; number of biological and technical replicates; what every measure and
     error bar is; every scale bar; "See also Figure S1" (s4). Panel labels are capital letters
     (s5). Legends are never inside the image file (s4). Craft target 150-220 words each. -->

Figure 1. [Title = Results subheading 1]
(A) [What the panel shows.]
(B) [What the panel shows.] Scale bars, [value] µm.
n = [number] [unit: mice / donors / independent experiments] per group; [technical replicates].
Data are represented as mean ± [SEM/SD]. *p < 0.05, **p < 0.01 by [test] (A) or [test] (B).
See also Figure S1.

Figure 2. [Title = Results subheading 2]
(A) [...]
[Replicates. Measures and error bars. Tests and asterisks.] See also Figure S[n] and Table S[n].

# Tables

<!-- Main tables count toward the 7 display items (s2). Word table tool; black and white; one
     value per cell; no "Table 1A/1B"; a title; footnotes with superscript lowercase letters (s4). -->

Table 1. [Title]

| [Column] | [Column]^a^ |
|---|---|
| [value] | [value] |

^a^[Footnote.]

# STAR Methods

<!-- Required at revision and for acceptance, not at first submission (s1, s8). Part of the main
     article; not counted toward 7,000 words (s2). Section headings below are from the author
     guide, NOT re-read on 2026-11-18: confirm in the PDF (s8).
     See templates/star_methods_skeleton.md. -->

## Key resources table

<!-- Cell Press Word template or webform; RRIDs for antibodies and genetically modified
     organisms (s8). -->
[Insert the table from the Cell Press template.]

## Experimental model and study participant details

[Text]

## Method details

[Text]

## Quantification and statistical analysis

[Text]

## Additional resources

<!-- Optional (s8). Delete if unused. -->

# References

<!-- Numbered in order of first citation (s9). "et al." only after 10 author names. Style:
     Sondheimer, N., and Lindquist, S. (2000). Rnq1: an epigenetic modifier of protein function
     in yeast. Mol. Cell 5, 163-172. 10.1016/S1097-2765(00)80412-8.
     Preprints allowed with a DOI. Unpublished data, personal communications and abstracts: in
     text only. Datasets, code and methods are cited and listed. -->
1. [Author, A., and Author, B. (Year). Title. Journal Volume, pages. DOI.]
