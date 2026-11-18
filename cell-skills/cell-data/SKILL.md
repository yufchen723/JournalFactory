---
name: cell-data
description: "Draft or audit the data, code, materials and supplemental side of a Cell manuscript: the Resource availability section (Lead contact, Materials availability, Data and code availability), the key resources table with RRIDs, a deposition plan for sequencing, imaging and code, and the supplemental files (Document S1, naming, sizes, Excel tables). Not for data cleaning or statistical analysis."
---

# Cell Data, Resources and Supplemental Files

*Adapted in structure from nature-skills (nature-data/SKILL.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

## Two kinds of statement

- **Cell rule (cell.md §N)**: recorded in `../cell-shared/journal-formats/cell.md`.
- **Craft guidance (not a journal rule)**: general practice for deposition and resource reporting. Never present it as Cell policy.

Important gaps. cell.md lists as **not read**: the journal-policies page (the exact required wording of Resource availability), the STAR Methods author guide PDF (key resources table details), and the final file requirements PDF. For anything that depends on them: "not specified in cell.md — check cell.com", and tell the user which page to open.

## Default stance

- Inventory first. List every dataset, code item and unique material before writing a statement.
- One access route per item: public repository, controlled access, within the paper, reused public data, restricted third-party data.
- Do not invent accession numbers, DOIs, RRIDs, catalogue numbers, licences, embargo dates, approvals or access committees. Write `AUTHOR_INPUT_NEEDED`.
- "Available on request" for data that could be deposited is weak. Flag it. Whether Cell accepts it is not specified in cell.md.
- Stage matters: STAR Methods and the manuscript component order are required at revision; supplemental and production rules at final files (cell.md §1). For a first submission, report gaps as "needed later", but advise depositing early so reviewers can access the data (craft guidance).

## Workflow

1. **Identify the stage** and article type.
2. **Inventory** data, code, materials, and software. One row each: what, where it is now, who controls it, any restriction.
3. **Assign an access route** and a repository to each (`references/deposition.md`).
4. **Draft Resource availability** with its three subsections (`references/resource-availability.md`, `templates/resource_availability.md`).
5. **Build the key resources table** (`references/key-resources-table.md`, `templates/key_resources_table.md`).
6. **Cite datasets and code** in the reference list where they have a DOI (cell.md §9; see `cell-citation`).
7. **Plan the supplemental files** (`references/supplemental-files.md`, `templates/supplemental_index.md`).
8. **Cross-check**: every identifier appears identically in Resource availability, the key resources table, STAR Methods and the references.
9. **Return** ready-to-paste text plus the open fields.

For a wording edit or audit of one statement, check that statement only; do not demand a full inventory.

## Output

```text
Scope and stage
Inventory table            item · type · route · repository · identifier · status
Resource availability      ready-to-paste, three subsections
Key resources table        rows, with missing identifiers marked
Supplemental plan          index with file type and size checks
Open items                 AUTHOR_INPUT_NEEDED
To confirm on cell.com     the pages not read (journal policies, STAR Methods guide)
```

## Red lines

- No invented identifiers of any kind.
- No statement that data "have been deposited" before the authors confirm the accession exists.
- No methods in supplemental files (**Cell rule**, cell.md §7).
- No claim about Cell's required wording, embargo rules, or accepted repositories: those pages were not read.
- No advice that would expose identifiable human data. Controlled access is decided by the authors' ethics approval and data-use agreements, not by this skill.

## References and templates

| File | Open when |
|---|---|
| [references/source-basis.md](references/source-basis.md) | Once per task: what is a Cell rule and what was not read |
| [references/resource-availability.md](references/resource-availability.md) | Writing or auditing the Resource availability section |
| [references/key-resources-table.md](references/key-resources-table.md) | Building the key resources table; RRIDs |
| [references/deposition.md](references/deposition.md) | Choosing repositories; controlled access for human data |
| [references/supplemental-files.md](references/supplemental-files.md) | Document S1, naming, sizes, Excel tables, the supplemental index |
| [templates/resource_availability.md](templates/resource_availability.md) | Ready-to-fill section |
| [templates/key_resources_table.md](templates/key_resources_table.md) | Ready-to-fill table |
| [templates/supplemental_index.md](templates/supplemental_index.md) | Ready-to-fill index and file checklist |
