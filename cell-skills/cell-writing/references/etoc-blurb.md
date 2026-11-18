# eTOC blurb ("In brief")

Structure of this file follows the nature-skills reference pattern (Apache-2.0); nature-skills has no equivalent file. Cell rules from cell-shared/journal-formats/cell.md.

## Cell rules (source: cell.md §6)

| Rule | Value |
|---|---|
| Length | ≤ 50 words, 2 sentences |
| Person | third person (no "we") |
| Content | context and significance |
| Audience | a general scientific audience |
| File | one Word file with the Highlights, separate from the manuscript |
| Stage | final (production) files (cell.md §1) |

Also applies: "novel" and "first" discouraged; US spelling (cell.md §3).

Not specified by Cell (see cell.md): how the authors are named ("[Author] et al." or "The
authors"); whether a heading is required; whether abbreviations are allowed; the counting method.

## Counting method

- Words: whitespace-separated tokens containing a letter or digit. "et al." counts as two.
- Sentences: split at ". ", "! " or "? " followed by a capital letter; "et al.", "e.g." and
  decimals do not end a sentence.
- First person: any of we, our, ours, us, I, my.
- `python scripts/cell_text_check.py --highlights highlights_etoc.md` applies all three. More
  than 50 words, more than 2 sentences, or a first-person word is a FAIL.

## How it differs from the Summary and the Highlights

| Item | Reader | Carries |
|---|---|---|
| Summary (≤ 150 words) | scientists deciding whether to read | question, approach, results, conclusion |
| Highlights (≤ 4 × 85 characters) | scanners | the findings |
| eTOC blurb (≤ 50 words) | any scientist browsing the table of contents | why the question matters and what the answer means |

The blurb is not a shortened Summary. Drop the approach and the supporting results. Keep the
problem and the meaning of the answer.

## Pattern (craft guidance, not a journal rule)

Two sentences:

1. **Context.** The biological problem in plain words (10–18 words).
2. **Finding and significance.** "[Author] et al. show / identify / find that …, which / revealing
   / explaining …" (25–35 words).

Or one sentence that does both, when the context fits in an opening clause.

Naming the authors in the third person ("[Author] et al.") is a convention seen in published
Cell Press blurbs; it is not stated in cell.md. Confirm against a recent issue or the proof.

## Worked examples (invented biology)

Accepted (47 words, 2 sentences, third person):

> Tissue repair must scale with injury without exhausting stem cells. [Author] et al. identify
> factor X, a protein released by dying epithelial cells, as a dose-dependent signal that
> activates quiescent intestinal stem cells through receptor Y and thereby matches stem cell
> output to the extent of damage.

Rejected:

> We found that factor X activates ISCs. Our results show that it acts through receptor Y. This
> is the first damage sensor of its kind.

| Problem | Rule |
|---|---|
| "We", "Our" | third person (cell.md §6) |
| Three sentences | 2 sentences (cell.md §6) |
| "ISCs" | not for a general audience (cell.md §6; abbreviations not specified) |
| "first" | discouraged (cell.md §3) |
| No context, no significance | content rule (cell.md §6) |

## Writing steps (craft guidance)

1. Copy the first and last sentences of the Summary.
2. Rewrite the first as a problem any scientist recognizes; remove field terms.
3. Rewrite the last in the third person with one concrete finding and one consequence.
4. Replace abbreviations and symbols a general reader would not know with descriptions.
5. Count words and sentences. Over 50: remove the mechanism detail before the significance.
6. Check terms against the ledger and claim strength against the Summary.

Verbs for sentence 2: show, identify, find, demonstrate, reveal, uncover. Match the verb to the
evidence as in the manuscript (`../static/core/stance.md` §4).

## Checks

1. ≤ 50 words; ≤ 2 sentences; no we/our/us/I (Cell rules).
2. Context and significance both present (Cell rule).
3. A scientist from another field understands every word (Cell rule: general audience).
4. No "novel"/"first" (Cell rule, cell.md §3).
5. The finding is the Summary's central claim, not a secondary result (craft).
6. No number unless the number is the news (craft).

## Deliverable

The blurb, its word and sentence counts, and the checker output. Use
`../templates/highlights_etoc.md`. Replace "[Author]" with the first author's family name
only when the author confirms the form.
