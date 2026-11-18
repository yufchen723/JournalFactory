# Deposition: where data, images and code go

*Adapted in structure from nature-skills (nature-data/references/repository-and-identifiers.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

**This whole file is general craft guidance (not a journal rule).** cell.md does not list required or accepted repositories, and Cell's data-sharing policy is on the journal-policies page, which was not read. Before deposition decisions are final: "not specified in cell.md — check cell.com". Repository names below are common community choices, given as examples; check each repository's current scope and terms on its own site.

The Cell rules that touch deposition:

- Resource availability must state data and code availability (cell.md §3).
- Datasets and code are cited and listed in the references, DOI where one exists (cell.md §9).
- Supplemental data and code use non-proprietary formats; no supplemental file above 500 MB (cell.md §7). Large data therefore belong in a repository, not in the supplement.
- Original unprocessed data are available on request (cell.md §5).

## 1. Order of preference

1. A community repository for that data type (curated, structured metadata, stable accession).
2. A general repository that issues a DOI.
3. Supplemental files, only for small items within the limits of cell.md §7.
4. "From the lead contact", only with a concrete legal or ethical reason.

## 2. Common choices by data type (examples)

| Data | Typical repository type | Examples | Identifier |
|---|---|---|---|
| Sequencing, non-human or non-identifiable: raw reads + processed matrices | functional-genomics and read archives | GEO with SRA; ArrayExpress/BioStudies with ENA | series and run accessions |
| Human sequencing with re-identification risk | controlled-access archives | dbGaP; EGA | study and dataset accessions |
| Single-cell and spatial omics | as for sequencing; add processed objects, coordinates and matched tissue images | same; large images to an image archive | accession + DOI |
| Microscopy and histology images | bioimage archives | BioImage Archive; IDR for reference image sets | accession |
| Proteomics | ProteomeXchange members | PRIDE; MassIVE | PXD/MSV identifiers |
| Metabolomics | metabolomics repositories | MetaboLights; Metabolomics Workbench | study identifier |
| Structures and maps | structural archives | PDB; EMDB; EMPIAR for raw cryo-EM | entry codes |
| Flow cytometry | cytometry repositories | FlowRepository | repository identifier |
| Plasmids | plasmid repositories | Addgene | plasmid numbers |
| Other datasets, source data, intermediate files | general repositories with DOI | Zenodo; Figshare; Dryad; Mendeley Data | DOI |
| Code | version control **plus** an archived release | GitHub or GitLab plus Zenodo, or Software Heritage | DOI or SWHID |

## 3. What to deposit for sequencing and spatial data

- Raw data (FASTQ or the instrument's primary output).
- Processed data used in the figures: count matrices, peak or fragment files, spatial coordinates, cell or spot annotations.
- For spatial assays: the tissue image used for registration and the alignment, so maps can be reproduced.
- Sample metadata: one row per sample with species, tissue, condition, donor or animal ID (coded), assay, batch.
- A README mapping files to figures.

Reviewers and later users mostly need the processed objects. Depositing only raw reads is a common complaint.

## 4. Human data and controlled access

Decide from the consent form and ethics approval, not from convenience.

| Question | Consequence |
|---|---|
| Does consent allow public sharing of individual-level genomic data? | If not, controlled access |
| Could the data re-identify a person (germline variants, raw reads, rare-disease metadata, facial or whole-slide images with labels)? | Controlled access or de-identification |
| Are there national or institutional rules on export or storage? | They determine the archive and the access committee |
| Can a processed, non-identifiable layer be public (count matrices, summary statistics)? | Often yes; deposit it openly and say so |

A controlled-access statement names: the archive and accession; who decides (data access committee); the criteria; how to apply; expected time. Never write "available on request" as a substitute for this.

Remove direct identifiers from all metadata. Code donor IDs. Check image labels and slide barcodes.

## 5. Code

- Archive the exact version that produced the figures; tag it; get a DOI.
- Include: environment or dependency file with versions, a README with run order, and small test data or a pointer to the deposited data.
- State the licence.
- Cite the archive in the reference list (cell.md §9) and list it in the key resources table.
- Third-party tools: cite and list with versions; do not re-deposit them.

## 6. Timing

- Deposit before submission where possible; use private or embargoed records with reviewer access.
- Make records public by publication. What Cell requires about timing and reviewer access is not specified in cell.md — check cell.com.
- Verify every accession resolves, and that the record contains what the paper says, before each submission round.

## 7. Inventory table (output)

```markdown
| Item | Type | Size | Human? | Route | Repository | Identifier | Public when | In KRT | In references |
|---|---|---|---|---|---|---|---|---|---|
| Spatial assay raw + processed | sequencing | [ ] | yes | controlled / open processed layer | [ ] | AUTHOR_INPUT_NEEDED | publication | [ ] | [ ] |
| Analysis code | code | — | — | public archive | [ ] | AUTHOR_INPUT_NEEDED | publication | [ ] | [ ] |
```

## 8. Red flags

- A repository chosen because it is easy, when a community repository exists for the data type.
- A dataset larger than the 500 MB supplemental limit planned as a supplemental file.
- Identifiable human data in an open repository.
- A live code repository with no archived release.
- Accessions that exist but hold no files.
