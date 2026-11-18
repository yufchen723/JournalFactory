# Resource availability

## 1. What cell.md says — Cell rule

| Rule | Where |
|---|---|
| The section is **required** | cell.md §3 |
| It has three subsections: **Lead contact · Materials availability · Data and code availability** | cell.md §3 |
| Position: after the Discussion, before Acknowledgments | cell.md §3 (component order) |
| Lead contact: **exactly one**; must be a corresponding author | cell.md §3 |
| Component order applies at revision; a first submission is free format | cell.md §1 |
| Datasets and code are cited and listed in the references, with DOI where one exists | cell.md §9 |

**The exact required wording lives on the journal-policies page, which was NOT read.** Before finalising, open the journal-policies page on cell.com (and the STAR Methods author guide) and compare each subsection with the wording given there. Until then, treat every sentence pattern below as a pattern, not as Cell's text.

Note on position: some third-party checklists place this section inside STAR Methods. cell.md §3 lists it as its own component after the Discussion. Follow cell.md and confirm on cell.com.

## 2. The three subsections — craft guidance (not a journal rule)

### Lead contact

Purpose: one named person who answers requests for resources.

- One person, a corresponding author (**Cell rule**).
- Name and e-mail.
- If there are several corresponding authors, still one lead contact.

Pattern:

```text
Requests for further information and resources should be directed to and will be
fulfilled by the lead contact, [Name] ([e-mail]).
```

### Materials availability

Purpose: say what unique materials the study generated and how to get them.

Cover each kind: plasmids, cell lines, organisms/strains, antibodies, compounds, custom devices or arrays.

| Situation | Pattern |
|---|---|
| Nothing new | "This study did not generate new unique reagents." |
| Deposited | "[Plasmids] generated in this study have been deposited at [repository] ([identifiers])." |
| Available from the lab | "[Lines] generated in this study are available from the lead contact with a completed materials transfer agreement." |
| Restricted | "[Material] is limited because [reason]; [what can be shared and how]." |

State restrictions concretely. "Reasonable request" without conditions tells the reader nothing.

### Data and code availability

Purpose: for every dataset and every piece of original code, where it is and how it is accessed.

Address three things explicitly, even when the answer is "none":

1. **Data**: each data type, its repository, its identifier, and when it becomes public.
2. **Code**: original code, its archive and identifier.
3. **Anything else** needed to reanalyse the data.

Patterns:

```text
[Data type] data have been deposited at [repository] and are publicly available as of
the date of publication. Accession numbers are listed in the key resources table.

This paper analyzes existing, publicly available data. The accession numbers are listed
in the key resources table.

[Human data type] have been deposited at [controlled-access repository] under accession
[ID]. Access requires approval by [committee] because [consent/legal reason]; requests
are made through [route].

All original code has been deposited at [archive] and is publicly available as of the
date of publication. The DOI is listed in the key resources table.

This paper does not report original code.

Any additional information required to reanalyze the data reported in this paper is
available from the lead contact upon request.
```

Whether Cell requires these sentences, a bullet layout, or particular phrases is on the page that was not read. Check it.

## 3. Audit checklist

Cell rules:

- [ ] Section present, with exactly the three subsection headings (cell.md §3).
- [ ] One lead contact, who is a corresponding author (cell.md §3).
- [ ] Section placed after the Discussion (cell.md §3).
- [ ] Deposited datasets and code with a DOI are in the reference list (cell.md §9).

Craft guidance:

- [ ] Every dataset in the inventory is named with repository and identifier.
- [ ] Every identifier matches the key resources table character for character.
- [ ] Reused public datasets are listed with their accessions and cited.
- [ ] Restricted data state who decides access, on what criteria, and how to apply.
- [ ] Code is archived with a persistent identifier, not only a link to a live repository.
- [ ] The version of the code that produced the paper is the archived one.
- [ ] No "available on request" for data that could be deposited.
- [ ] Reviewer access (private links or tokens) is arranged for data not yet public. Cell's procedure for this is not specified in cell.md.
- [ ] Statements are true today. "Have been deposited" only when the accession exists.

## 4. Common failures

| Failure | Fix |
|---|---|
| Two lead contacts | Choose one (Cell rule) |
| "Data are available upon reasonable request" for sequencing data | Deposit; give the accession |
| Accession reserved but data not uploaded | Upload before submission; verify the link |
| Code "on GitHub" with no archive | Archive a release and cite its DOI |
| Section silent on code | State "This paper does not report original code" if true |
| Human data posted openly without checking consent | Stop; check the ethics approval; use controlled access |
| Identifier in the text differs from the key resources table | Correct both from the repository record |
| Raw images or source data never mentioned | State where they are; cell.md §5 says originals are available on request |

## 5. Hand-offs

- Repository choice and controlled access: `deposition.md`.
- Table rows for deposited data and software: `key-resources-table.md`.
- Dataset and code citations: `cell-citation`.
