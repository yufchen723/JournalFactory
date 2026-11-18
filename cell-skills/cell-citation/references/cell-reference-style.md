# Cell reference style

## 1. The rules — Cell rule (cell.md §9, source: cell.com revise-manuscript page)

| Rule | Text in cell.md |
|---|---|
| Order | Numbered in order of first citation |
| In text | Superscript numbers |
| Authors | "et al." only after **10** author names |
| Format | see the official example below |
| Preprints | Allowed with a DOI ("Preprint at bioRxiv, …"); replace by the published version when it exists |
| Not in the list | Unpublished data, personal communications, abstracts: in text only |
| Data, code, methods | Cited and listed (DOI where one exists) |
| Supplement | Supplemental references numbered independently; references cited only in the supplement appear only there (cell.md §7) |

### The official example

cell.md records one complete example:

```text
Sondheimer, N., and Lindquist, S. (2000). Rnq1: an epigenetic modifier of protein function in yeast. Mol. Cell 5, 163–172. 10.1016/S1097-2765(00)80412-8.
```

and one fragment, for preprints: `Preprint at bioRxiv, …`

No other examples (book, chapter, dataset, software, website, article number instead of pages) are in cell.md. For those: **not specified in cell.md — check cell.com** or a recent Cell article.

## 2. What the example fixes

Reading the example element by element:

| Element | Form in the example |
|---|---|
| Author | Surname, comma, initials with periods and no spaces: `Sondheimer, N.` |
| Between authors | comma |
| Last author | preceded by `, and` — also when there are only two authors |
| Year | in parentheses directly after the authors, then a period: `(2000).` |
| Title | sentence case, ends with a period |
| Journal | abbreviated with periods: `Mol. Cell` |
| Volume | after the journal, no punctuation between: `Mol. Cell 5` |
| Pages | after a comma; range with an en dash: `, 163–172.` |
| DOI | bare, no `https://doi.org/` and no `doi:`; followed by a period |
| Not present | issue number, month, "pp.", "vol." |

The general pattern, with the 10-author rule:

```text
Author, A.B., Author, C.D., and Author, E.F. (year). Title. Journal Abbrev. vol, pages. DOI.
Author1, A., Author2, B., … Author10, J., et al. (year). Title. Journal Abbrev. vol, pages. DOI.
```

## 3. Interpretation and open points

Marked as interpretation where cell.md is not explicit.

| Point | Status |
|---|---|
| "et al. only after 10 author names" | Rule. Interpretation used here: up to 10 authors are all listed; with more than 10, the first 10 are listed, then "et al.". Whether an 11-author paper may be listed in full is not specified in cell.md. |
| Punctuation before "et al." | Not shown in cell.md. The script writes `…, Author10, J., et al. (year).` Check a recent Cell article. |
| Italics or bold for journal or volume | Not specified in cell.md. The example as recorded is plain text. |
| Journal abbreviations | The example abbreviates. Which abbreviation list applies is not specified in cell.md; use the standard (NLM/ISO 4) abbreviation and check. |
| Articles with an article number instead of pages | Not specified. Common practice: the article number in the page position. |
| Exact preprint entry | Only "Preprint at bioRxiv, …" is recorded. The script writes `Author, A. (year). Title. Preprint at bioRxiv, DOI.` Confirm on cell.com. |
| Books, chapters, theses, websites, software, datasets | Format not specified in cell.md. Datasets and code must be cited and listed, with DOI where one exists; the entry form needs checking. |
| Lettered references (12a, 12b) | Not mentioned in cell.md. Numbering "in order of first citation" implies one number per reference; the script flags lettered entries as a craft check. |
| Maximum number of references | Not specified in cell.md. |
| References and the word limit | References do not count toward the 7,000 words (cell.md §2). |

## 4. Formatting with the script — tool note

```bash
python scripts/cell_refs.py format refs.json --number
```

Input: a JSON list. Each entry is CSL-JSON (as exported by reference managers or DOI content negotiation) or the simple form:

```json
[
  {
    "authors": ["Sondheimer, N.", "Lindquist, S."],
    "year": 2000,
    "title": "Rnq1: an epigenetic modifier of protein function in yeast",
    "journal_abbrev": "Mol. Cell",
    "volume": "5",
    "pages": "163-172",
    "doi": "10.1016/S1097-2765(00)80412-8"
  }
]
```

Behaviour:

- Initials are built from given names (`Jean-Pierre` → `J.-P.`).
- More than 10 authors → first 10, then `et al.`
- `https://doi.org/` is stripped; hyphens in page ranges become en dashes.
- The journal name is **not** abbreviated; a warning is printed if no abbreviation was supplied.
- Entries of type preprint (or with a preprint server as container) use the `Preprint at <server>, <DOI>.` form.
- Missing fields are reported on stderr and never filled in.
- `--number` numbers in input order. The order must already be order of first citation.

## 5. Converting from other styles — craft guidance (not a journal rule)

| From | Change |
|---|---|
| Year at the end, bold volume (Nature-like) | Move `(year).` after the authors; plain volume |
| "&" before the last author | `, and` |
| Initials first ("N. Sondheimer") | `Sondheimer, N.` |
| "et al." after 3 or 5 authors | List up to 10 |
| Author–date in-text citations | Superscript numbers in order of first citation |
| Alphabetical list | Re-order by first citation |
| `https://doi.org/10.…` | Bare DOI |
| Journal names in full | Abbreviate |

Use a reference manager for the conversion of a full manuscript; then lint with `cell_refs.py check`.

## 6. Checklist

- [ ] Every entry matches the pattern of the official example.
- [ ] Up to 10 authors listed in full; "et al." only beyond 10.
- [ ] `, and` before the last author.
- [ ] Year in parentheses after the authors.
- [ ] DOI present where one exists, in bare form.
- [ ] Preprints have a DOI and the "Preprint at" form; published versions substituted.
- [ ] No unpublished data, personal communications or abstracts in the list.
- [ ] Datasets and code cited and listed.
- [ ] List numbered in order of first citation; no duplicates; no lettered entries.
- [ ] Supplement-only references are in the supplemental list only.
