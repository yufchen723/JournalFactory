# Key resources table

## 1. What cell.md says — Cell rule (cell.md §8)

- The key resources table is the first section of STAR Methods. (Heading list from the author guide, not re-read on 2026-11-18; confirm in the PDF.)
- Use the **Cell Press Word template or the webform**.
- **RRIDs for antibodies and genetically modified organisms.**
- STAR Methods is required at revision and for acceptance, not at first submission (cell.md §1, §8).
- STAR Methods is part of the main article and is not counted in the 7,000 words (cell.md §2).

Nothing else about the table is in cell.md. The categories, columns and row conventions below are **craft guidance — confirm in the Cell Press template** (the STAR Methods author guide PDF was not read).

## 2. Layout — confirm in the Cell Press template

Three columns are customary:

| REAGENT or RESOURCE | SOURCE | IDENTIFIER |
|---|---|---|
| what it is, specific enough to reorder or re-download | company, lab, repository or paper | catalogue number, RRID, accession, DOI, URL |

Customary categories, in this order — **confirm in the Cell Press template**:

| Category | Typical rows | Identifier to give |
|---|---|---|
| Antibodies | each antibody, with host and clone where relevant | catalogue number and **RRID** (Cell rule) |
| Bacterial and virus strains | competent cells, viral vectors and serotypes | catalogue or repository number |
| Biological samples | patient tissue, primary cells, sera | source institution; cohort or biobank ID (no personal identifiers) |
| Chemicals, peptides, and recombinant proteins | inhibitors, cytokines, enzymes | catalogue number; CAS where useful |
| Critical commercial assays | kits | catalogue number |
| Deposited data | datasets generated here; public datasets reused | repository and accession or DOI |
| Experimental models: Cell lines | each line | catalogue number; RRID where one exists |
| Experimental models: Organisms/strains | mouse, fly, fish, worm, plant strains | stock number; **RRID for genetically modified organisms** (Cell rule) |
| Oligonucleotides | primers, guides, probes | sequence, or pointer to a supplemental table if many |
| Recombinant DNA | plasmids | repository number or "this paper" |
| Software and algorithms | each tool with version | URL; RRID where one exists; DOI for archived code |
| Other | instruments, arrays, slides, special consumables | catalogue or model number |

Delete categories that have no rows, if the template allows it — confirm.

## 3. Row conventions — craft guidance (not a journal rule)

- **One resource per row.** Not "antibodies (see Table S2)" unless the template allows a pointer for long lists.
- **Source "This paper"** for resources generated in the study; the identifier is the accession, repository number or "N/A".
- **RRIDs.** Required by cell.md §8 for antibodies and genetically modified organisms. Write them as `RRID:AB_…` for antibodies and in the matching form for organisms (for example a stock-centre RRID). Look each one up in the RRID portal; do not construct an RRID by pattern. If none exists, say so and give the catalogue and lot number. Whether Cell asks authors to register a missing RRID is not specified in cell.md.
- **Software**: name, version, source. The version must match "Quantification and statistical analysis".
- **Deposited data**: one row per accession. Reused public data get rows too, with the original paper as source.
- **Oligonucleotides**: if more than about ten, put sequences in a supplemental Excel table and point to it — confirm the template permits this.
- **No personal identifiers** for human samples.
- **Consistency**: the same name for a resource in the table, Method details and legends.

## 4. Building the table

1. Walk through Method details and every figure legend. List every reagent, model, dataset and tool named.
2. Add what is used but unnamed (secondary antibodies, competent cells, analysis packages).
3. For each row, collect source and identifier from the vial, order record, repository record or stock centre. Not from memory.
4. Look up RRIDs. Record "not found" honestly.
5. Sort into categories.
6. Cross-check against Resource availability: every deposited dataset and code archive appears in both, with identical identifiers.

## 5. Audit checklist

Cell rules:

- [ ] The table is in the Cell Press Word template or entered in the webform (cell.md §8).
- [ ] Every antibody has an RRID (cell.md §8).
- [ ] Every genetically modified organism has an RRID (cell.md §8).

Craft guidance:

- [ ] Every resource named in Method details has a row; every row is used in the paper.
- [ ] No identifier is invented or guessed; missing ones are marked.
- [ ] Software rows carry versions.
- [ ] Deposited-data rows match Resource availability exactly.
- [ ] New resources from the revision were added.
- [ ] Categories and column headings match the current Cell Press template.

## 6. Common failures

| Failure | Fix |
|---|---|
| Antibody rows with catalogue number only | Add the RRID (Cell rule) |
| Mouse strains named by nickname | Full strain name, stock number, RRID |
| "Custom scripts" with no source | Archive the code; give the DOI |
| Kit named in Methods, absent from table | Add the row |
| Table built from the first submission, not updated at revision | Re-walk the revised Methods |
| RRID copied from another paper | Verify in the RRID portal against the catalogue number |

Template: `../templates/key_resources_table.md`.
