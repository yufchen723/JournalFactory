---
name: cell-citation
description: "Format, lint and verify references for a Cell manuscript: numbered in order of first citation with superscript in-text numbers, 'et al.' only after 10 authors, 'Author, A.B., and Author, C. (year). Title. Journal vol, pages. DOI.' Includes a script that formats JSON/CSL-JSON into Cell style and lints a plain-text list, and a verification routine (every reference checked against PubMed/DOI; never cite from memory)."
---

# Cell Citation

*Adapted in structure from nature-skills (nature-citation/SKILL.md and nature-ref-verifier/SKILL.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

## Two kinds of statement

- **Cell rule (cell.md §9)**: recorded in `../cell-shared/journal-formats/cell.md`.
- **Craft guidance (not a journal rule)**: verification practice and choices cell.md leaves open.

If a rule is needed and is not in cell.md: "not specified in cell.md — check cell.com".

Warning about older material: some third-party checklists (including `vendor/cell-skills/skills/cell-citation`) describe Cell references as author–date in the text with an alphabetical list. cell.md §9, read on cell.com on 2026-11-18, says **numbered in order of first citation, superscript numbers in the text**. cell.md wins.

## The style in brief — Cell rule (cell.md §9)

- Numbered in order of first citation; in-text superscript numbers.
- "et al." only after **10** author names.
- `Sondheimer, N., and Lindquist, S. (2000). Rnq1: an epigenetic modifier of protein function in yeast. Mol. Cell 5, 163–172. 10.1016/S1097-2765(00)80412-8.`
- Preprints allowed with a DOI ("Preprint at bioRxiv, …"); replace by the published version when it exists.
- Unpublished data, personal communications, abstracts: in the text only, not in the list.
- Datasets, code and methods are cited and listed (DOI where one exists).
- Supplemental references are numbered independently; references cited only in the supplement appear only there (cell.md §7).
- No citations in the Summary (cell.md §3). Avoid numbered citations inside figure artwork (cell.md §5).

## Default stance

- **Never cite from memory.** A reference enters the manuscript only after its record has been checked against PubMed or the DOI landing page.
- A related title is not support. Check that the paper shows what the sentence says.
- Do not invent or complete missing fields (authors, year, volume, pages, DOI). Mark them and look them up.
- A reference manager with a Cell style file does the formatting in real manuscripts. The script here is for small lists, checks and spot fixes.

## Workflow

1. **Collect** the references to be used, with DOIs or PMIDs.
2. **Verify each one** (`references/verification.md`): existence, metadata, and that it supports the claim. Replace preprints that have been published.
3. **Format** (`references/cell-reference-style.md`), by reference manager or `scripts/cell_refs.py format`.
4. **Place in-text citations** (`references/in-text.md`); number by first citation.
5. **Lint** the final list: `scripts/cell_refs.py check`.
6. **Report** what was verified, what could not be verified, and what was replaced.

## Script

```bash
python scripts/cell_refs.py format refs.json [--number]   # JSON or CSL-JSON -> Cell style
python scripts/cell_refs.py check refs.txt [--json]       # lint a plain-text list
python scripts/cell_refs.py --self-test
```

Resolve the path relative to this skill directory. The script has **no network access**: it formats and lints what it is given and cannot tell whether a reference exists. It does not abbreviate journal names; supply `container-title-short` or `journal_abbrev`.

`check` flags: year not in parentheses after the authors, no ", and " before the last author, "&", initials-first names, "et al." before 10 names, more than 10 names without "et al.", missing DOI, DOI written as a URL, duplicates (by DOI or by first author + year + title), lettered entries (12a), breaks in numbering, preprint form, unpublished items in the list.

## Output

```text
Reference report
- Verified (source checked, date): n
- Replaced (preprint -> published): list
- Not verifiable / AUTHOR_INPUT_NEEDED: list
- Style lint: script output, remaining findings explained

Formatted reference list   (numbered in order of first citation)
```

## Red lines

- No reference that has not been checked against a primary record.
- No fabricated DOI, PMID, volume or page.
- No citation of a paper for a claim it does not make.
- No unpublished data, personal communications or abstracts in the list (Cell rule).
- No statement of a Cell reference rule that is not in cell.md §9.

## References

| File | Open when |
|---|---|
| [references/cell-reference-style.md](references/cell-reference-style.md) | Formatting entries; the official example; open points |
| [references/in-text.md](references/in-text.md) | Placing and numbering citations in the text, legends, STAR Methods, supplement |
| [references/verification.md](references/verification.md) | Checking that each reference exists, is correct, and supports the claim |
