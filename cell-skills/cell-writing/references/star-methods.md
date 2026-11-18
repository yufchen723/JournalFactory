# STAR Methods

Adapted in structure from nature-skills (nature-writing/references/method.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

## What was and was not verified

cell.md §8 rests on the STAR authors' guide **landing page** and the revise-manuscript page.
The **STAR Methods author guide PDF was not read** on 2026-11-18, and the journal-policies page
(resource availability wording) was not read either. Treat every structural detail below that is
not in the first table as unverified, and open the PDF before finalizing.

## Cell rules (source: cell.md §3, §7, §8)

| Rule | Source |
|---|---|
| STAR Methods are required at revision and for acceptance; not at first submission | cell.md §1, §8 |
| They replace "Experimental procedures" and are part of the main article, not supplemental | cell.md §8 |
| STAR Methods text does not count toward the 7,000-word limit | cell.md §2 |
| **Methods never go in the supplement** | cell.md §7 |
| Key resources table: Cell Press Word template or webform | cell.md §8 |
| RRIDs for antibodies and genetically modified organisms | cell.md §8 |
| In the manuscript order, STAR Methods come after the Tables and before the References | cell.md §3 |
| "Resource availability" is required, with three subsections: Lead contact, Materials availability, Data and code availability | cell.md §3 |
| Exactly one lead contact, who must be a corresponding author | cell.md §3 |
| AI used in the research itself is reported in STAR Methods | cell.md §3 |
| Adjustments to images that are not applied to the whole image are explained in the legend and the methods | cell.md §5 |
| Datasets, code and methods are cited and listed in the references, with a DOI where one exists | cell.md §9 |

## Section headings

**From the author guide, not re-read on 2026-11-18; confirm in the PDF** (cell.md §8):

1. Key resources table
2. Experimental model and study participant details
3. Method details
4. Quantification and statistical analysis
5. Additional resources (optional)

Position of "Resource availability": cell.md §3 lists it as a manuscript component after the
Discussion and before the Acknowledgments. Whether it is also repeated or placed inside STAR
Methods is not specified by Cell (see cell.md). Follow cell.md §3 and confirm in the PDF.

Not specified by Cell (see cell.md): the row categories and column names of the key resources
table (use the Cell Press template as supplied; do not rebuild it from memory); the exact
wording of the three resource-availability statements; required content of each STAR section;
a length limit for STAR Methods; heading capitalization.

## What goes in each section (craft guidance, not a journal rule)

The assignments below follow the plain meaning of the headings. Confirm against the PDF.

| Section | Put here | Do not put here |
|---|---|---|
| Key resources table | every antibody, organism or strain, cell line, reagent, kit, oligonucleotide, plasmid, deposited dataset, software and algorithm used, each with source and identifier | procedures |
| Experimental model and study participant details | species, strain, sex, age, housing; cell line origin and authentication; participant numbers and characteristics; ethics approvals and consent | experimental procedures on those models |
| Method details | each procedure in enough detail to repeat it; grouped by technique under subheadings | statistics; results |
| Quantification and statistical analysis | per analysis: software, test, what n is, what is plotted (center and dispersion), multiple-testing correction, exclusion criteria, randomization and blinding if used | description of the wet-lab procedure |
| Additional resources | external websites or resources created for the paper | anything that belongs in the table |

## Key resources table

Cell rules: use the template or webform; give RRIDs for antibodies and genetically modified
organisms (cell.md §8).

Craft guidance:

- Build it from the text, not from memory: sweep Results, legends and Method details for every
  named reagent, line, dataset and tool; each must have a row.
- One resource per row; the identifier is specific (catalog number and RRID, accession number,
  DOI, version).
- Data and code generated in this paper get their own rows with the accession or DOI, and
  match the "Data and code availability" statement.
- Never invent an identifier. Missing ones are placeholders: `[RRID needed]`, `[Cat# needed]`.
- Names in the table equal the ledger names used in text and legends.

## Method details: writing rules (craft guidance)

- One subheading per technique; order follows first use in Results.
- Past tense, active or passive, consistent within the paper.
- Give what a competent reader needs to repeat the work: amounts, times, temperatures,
  instrument and settings, software and version, parameters that differ from defaults.
- Cite a published protocol and state every change from it. "As previously described" alone is
  not enough to repeat the work.
- Refer to reagents by the name used in the key resources table.
- Computational methods: input, each processing step with its parameter values, output; the code
  location is given under "Data and code availability".
- No results, no interpretation, no figure-by-figure narrative.

## Quantification and statistical analysis: checklist (craft guidance)

Cell requires each legend to state the tests, the meaning of asterisks, replicate numbers and
error-bar definitions (cell.md §4). This section must agree with every legend.

- [ ] For each test: name, one- or two-sided, software and version.
- [ ] What n represents in each experiment (animals, donors, cells, fields, independent experiments).
- [ ] Biological versus technical replicates defined once and used consistently.
- [ ] Center and dispersion for each plot type (mean ± SEM, median with interquartile range).
- [ ] Multiple-comparison correction and the significance threshold.
- [ ] Inclusion and exclusion criteria; whether any data were excluded.
- [ ] Randomization, blinding and sample-size determination, or a statement that none was done.

## Converting a free-text methods section

| Step | Action |
|---|---|
| 1 | Rename the section "STAR Methods". Remove "Experimental procedures" / "Materials and methods" |
| 2 | Extract every resource into the key resources table |
| 3 | Move model and participant descriptions under their heading |
| 4 | Sort the procedures under Method details by technique |
| 5 | Gather all statistics text under Quantification and statistical analysis |
| 6 | Pull any "Supplemental methods" back in: methods never go in the supplement (cell.md §7) |
| 7 | Check that the manuscript has Resource availability with its three subsections (cell.md §3) |
| 8 | Reconcile n, tests and error terms with every legend |

A "Methods S1" supplemental item type exists in cell.md §7 naming. cell.md does not say what
it may contain, while stating that methods do not go in the supplement. Do not use it for
procedures; ask the editor if in doubt.

## Stage (cell.md §1)

At initial submission the STAR format is not required. A plain methods section is acceptable
then; report "STAR Methods format needed at revision" instead of a failure. Building the key
resources table early is still cheaper than reconstructing it later (craft guidance).

## Deliverable

Use `../templates/star_methods_skeleton.md`. Return the filled sections, the list of placeholders
(identifiers, approvals, versions), and a table of legend ↔ statistics-section mismatches.
