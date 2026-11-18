# Action mapping

*Adapted in structure from nature-skills (nature-response/references/action-mapping.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

Craft guidance (not a journal rule) unless marked. Every item gets one action, one work status, one evidence entry and one location.

## 1. Action labels

| Label | Meaning | Evidence the response must show |
|---|---|---|
| `NEW_EXPERIMENT` | New bench or in vivo work | New panel(s), n, statistics, methods |
| `NEW_ANALYSIS` | Reanalysis of existing data | New panel or table; method in STAR Methods |
| `EXISTING_DATA` | Data existed but were not shown or were hard to find | Panel added or moved; pointer |
| `TEXT_CLARIFY` | Explanation, definition, methods detail | Quoted new text |
| `TEXT_NARROW` | Claim reduced to what the data support | Old and new wording; every place it changed (title, Summary, Highlights, subheadings) |
| `LIMITATION` | Concern acknowledged as a limit | Sentence in "Limitations of the study" |
| `FIGURE_EDIT` | Labels, colours, layout, scale bars | Figure and panel |
| `STATS_FIX` | Test, n, correction or legend statistics changed | Legend and "Quantification and statistical analysis" |
| `CITE` | Reference added or corrected | Verified reference; sentence where cited |
| `DATA_ACCESS` | Accession, code, materials | Identifier; Resource availability; key resources table |
| `DISAGREE` | Request declined with reasons | Reason a neutral expert accepts; what changed anyway |
| `NOT_FEASIBLE` | Cannot be done | Why; the substitute evidence; the stated limit |
| `OUT_OF_SCOPE` | Beyond this paper | Why; ideally editor's agreement; limit stated |

Combine when needed: `NEW_ANALYSIS + TEXT_NARROW`.

## 2. Default action by category and severity

| Category | S1 | S2 | S3–S4 |
|---|---|---|---|
| ADV | reframing across front matter; often NEW_EXPERIMENT | TEXT_CLARIFY | — |
| CLAIM / MECH | NEW_EXPERIMENT, else TEXT_NARROW + LIMITATION | NEW_ANALYSIS or TEXT_NARROW | TEXT_CLARIFY |
| CTRL / ALT | NEW_EXPERIMENT | NEW_EXPERIMENT or EXISTING_DATA | TEXT_CLARIFY |
| GEN | NEW_EXPERIMENT or TEXT_NARROW | LIMITATION | — |
| STAT | STATS_FIX + NEW_ANALYSIS | STATS_FIX | STATS_FIX |
| METH | TEXT_CLARIFY (STAR Methods) | same | same |
| DATA | DATA_ACCESS | same | same |
| LIT | CITE + TEXT_CLARIFY (distinguish the work) | CITE | CITE |
| PRES | FIGURE_EDIT / TEXT_CLARIFY | same | same |
| INTEG / ETH | provide originals and explanation; involve the corresponding author | — | — |
| SCOPE | ask the editor; OUT_OF_SCOPE + LIMITATION | same | — |

`DISAGREE` is never the default for S1. If the authors believe an S1 request is wrong, the answer still needs evidence.

## 3. Ranking experiments

Score each requested experiment on two axes.

| | Feasible in the revision period | Long or uncertain |
|---|---|---|
| **Needed for the central claim** | Do first | Start now; ask the editor about time or an agreed substitute |
| **Supports a secondary claim** | Do if capacity allows | Replace by narrowing or a limitation |
| **Optional** | Do only if nearly free | Decline politely |

- One experiment that answers several comments ranks above its single-comment score.
- A requested experiment that could disprove the central claim is the most important one. Do it early.
- Record for each: owner, start, expected result date, the figure it will enter, what happens if the result is negative.

## 4. Work status

`DONE_VERIFIED` · `DONE_REPORTED` · `IN_PROGRESS` · `PLANNED` · `NOT_FEASIBLE` · `DECLINED_WITH_REASON` · `AUTHOR_INPUT_NEEDED`

Wording follows status:

| Status | Allowed in the response text |
|---|---|
| DONE_VERIFIED | "We performed…", "We have added…" with location |
| DONE_REPORTED | Same wording, flagged internally as unverified until the location is seen |
| IN_PROGRESS / PLANNED | Nothing final. Draft carries `AUTHOR_INPUT_NEEDED`; never "we will" in a submitted response |
| NOT_FEASIBLE / DECLINED | The reason, the substitute, the limit added |

## 5. Location format

A location lets the reviewer find the change without searching. Line numbers change between versions; anchor to structure.

```text
Results, "Factor X is required for expansion of cell type A", paragraph 2
Figure 3C and D (new); Figure S4 (new), related to Figure 3
STAR Methods, Method details, "Knockdown and rescue"
STAR Methods, Quantification and statistical analysis, paragraph 3
Discussion, Limitations of the study, sentence 2
Key resources table, "Recombinant DNA"
```

Add page and line of the marked version only if the authors supply them. Never invent them.

## 6. Side effects to enter in the plan

Each action can break something else. Add a plan row for each side effect.

| Action | Side effect to check |
|---|---|
| New main panel | 7-item limit; figure size; legend words count toward 7,000 (**Cell rule**, cell.md §2) |
| New supplemental figure | "related to Figure N" title; "See also" in the main legend; supplemental index; recommended ≤ 20 (**Cell rule**, cell.md §4, §7) |
| Panel moved or renumbered | every citation of it in text, legends, response |
| New experiment | STAR Methods entries; key resources table; statistics |
| Claim narrowed | title, Summary, Highlights, eTOC blurb, graphical abstract, subheadings |
| New reference | verified against the source; numbering order (**Cell rule**, cell.md §9) |
| New dataset or code | Resource availability; key resources table |
