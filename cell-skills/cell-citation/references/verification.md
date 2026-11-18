# Reference verification

*Adapted in structure from nature-skills (nature-ref-verifier/SKILL.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

**Craft guidance (not a journal rule)**, except the lines marked Cell rule. cell.md does not describe a verification procedure. This file sets the working standard for the pack:

> Every reference is checked against PubMed or its DOI record before it is used. Nothing is cited from memory.

This applies with special force to references suggested by a language model. Model-recalled references can be wrong in any field, or not exist at all.

## 1. Three checks per reference

| Check | Question | Source of truth |
|---|---|---|
| **Existence** | Is there a real record with this DOI or PMID? | DOI resolver / publisher page; PubMed |
| **Metadata** | Do authors, year, title, journal, volume, pages and DOI in the list match the record? | The same record |
| **Support** | Does the paper show what the citing sentence says? | Abstract at minimum; full text for specific claims |

A reference passes only with all three.

## 2. Procedure

1. **Start from an identifier.** DOI or PMID. If there is none, search PubMed by title and first author, then take the identifier from the hit. Never start from a remembered citation string.
2. **Open the record.** PubMed entry or the DOI landing page. Confirm the title matches the paper you mean.
3. **Take the metadata from the record**, not from memory or from another paper's reference list. Export it (CSL-JSON, RIS, or the reference manager's import by identifier).
4. **Compare fields**: all authors and their order, year, title, journal, volume, pages or article number, DOI.
5. **Read for support.** Find the result in the abstract or text. Note system and conditions. Grade: direct / partial / background / none.
6. **Check status**: retraction, correction, expression of concern; preprint versus published version.
7. **Log it** (table in §5).

Tools: use whatever verified access is available in the session (PubMed lookup, DOI resolution, a reference manager). `scripts/cell_refs.py` does not verify; it has no network access.

If no lookup tool is available, do not mark anything verified. Return the list as `UNVERIFIED` and ask the author to check or to provide exported records.

## 3. Preprints — Cell rule (cell.md §9)

- A preprint may be cited if it has a DOI, in the form "Preprint at bioRxiv, …".
- Replace it by the published version when one exists.

Craft routine:

- For each preprint, search for a published version (the preprint server's "now published in" link; PubMed by title and authors).
- If published: replace the entry, then **re-check support**. Published versions can differ from the preprint in results and claims.
- Repeat at every revision round and before final files.

## 4. What may not be listed — Cell rule (cell.md §9)

- Unpublished data, personal communications and abstracts: text only.
- So "in preparation", "submitted", "manuscript under review" entries leave the list. If the work is on a preprint server with a DOI, cite the preprint.

## 5. Verification log

```markdown
| # | DOI / PMID | Record opened | Metadata | Support for the citing sentence | Status flags | Verified on | Result |
|---|---|---|---|---|---|---|---|
| 12 | 10.xxxx/… | PubMed | match | direct (abstract) | none | 2026-11-18 | PASS |
| 13 | none found | — | — | — | — | — | FAIL: not found |
| 14 | 10.1101/… | bioRxiv | match | partial: shown in vitro only | published version exists | 2026-11-18 | REPLACE |
```

Result values: `PASS` · `FIX_METADATA` · `REPLACE` (preprint published; retracted; better source) · `REWORD` (source gives partial support) · `FAIL` (not found, or does not support) · `UNVERIFIED` (not checked).

Only `PASS` entries go into a submitted manuscript.

## 6. Common failure patterns

| Pattern | How it shows | Action |
|---|---|---|
| Fabricated reference | Plausible authors and journal; DOI does not resolve; no PubMed hit | Remove; find a real source for the claim or drop the claim |
| Chimera | Real authors with another paper's title or journal | Find the intended paper; rebuild from its record |
| Wrong year, volume or pages | Online-first year versus issue year; article number mistaken for pages | Take from the record |
| Wrong or truncated author list | "et al." too early; missing middle authors | Export from the record; list up to 10 (**Cell rule**) |
| DOI of a different article | DOI resolves to another paper | Correct from the record |
| Title matches, claim does not | The paper is on the topic but does not show the result | `REWORD` or replace |
| Citing a review for a primary finding | — | Cite the primary paper; keep the review as background |
| Citation copied from another paper's list | Error inherited | Verify at the source |
| Preprint superseded | Published version exists | Replace (**Cell rule**) and re-check |
| Retracted or corrected paper | Flag on the record | Remove or cite with care and say why |
| Duplicate | Same paper under two numbers, or preprint and published version both listed | Merge |

## 7. Datasets and code — Cell rule (cell.md §9)

Datasets, code and methods are cited and listed, with DOI where one exists. Verify these like papers:

- The accession or DOI resolves and holds what the paper says.
- The entry matches the key resources table and Resource availability (see `cell-data`).

## 8. Final gate

- [ ] Every entry has result `PASS` with a date.
- [ ] No entry was added after the last verification pass.
- [ ] Preprints were re-checked for published versions in this round.
- [ ] `python scripts/cell_refs.py check refs.txt` reports no errors; warnings are explained.
- [ ] The list of anything unverifiable has been given to the authors.
