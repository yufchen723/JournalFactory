# Highlights

Structure of this file follows the nature-skills reference pattern (Apache-2.0); nature-skills has no equivalent file. Cell rules from cell-shared/journal-formats/cell.md.

## Cell rules (source: cell.md §6)

| Rule | Value |
|---|---|
| Number | up to 4 bullets |
| Length | each ≤ 85 characters with spaces |
| Abbreviations | none |
| Content | the core findings |
| File | one Word file with the eTOC blurb, separate from the manuscript |
| Stage | final (production) files (cell.md §1) |

Also applies: "novel" and "first" discouraged; US spelling (cell.md §3).

Not specified by Cell (see cell.md): a minimum number of bullets; whether bullets are full
sentences or fragments; tense; end punctuation; whether a gene or protein symbol counts as an
abbreviation.

## Counting method

Count every character of the bullet text, including spaces and punctuation. Do not count the
bullet marker, the space after it, or line-end whitespace. Markup that will not print (the
asterisks around an italic gene symbol) is not counted.

Three ways to count:

```bash
# 1. the checker (strips the bullet marker and Markdown emphasis)
python scripts/cell_text_check.py --highlights highlights_etoc.md

# 2. one line of Python
python3 -c "import sys; [print(len(l.strip()), l.strip()) for l in sys.stdin if l.strip()]" < bullets.txt
```

3. In Word: select the bullet text without the paragraph mark → Review → Word Count →
   "Characters (with spaces)".

A ruler for the eye (85 characters):

```
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345
```

## Worked examples (invented biology)

Accepted set:

| # | Bullet | Characters |
|---|---|---|
| 1 | Dying epithelial cells release factor X in proportion to tissue damage | 70 |
| 2 | Factor X binds receptor Y on quiescent stem cells to trigger cell cycle entry | 77 |
| 3 | Loss of factor X delays intestinal repair; excess depletes the stem cell pool | 77 |
| 4 | A dose-dependent damage signal matches stem cell output to tissue need | 70 |

Repairs:

| Draft | Characters | Problem | Repair | Characters |
|---|---|---|---|---|
| Factor X, which is released by dying epithelial cells, increases in proportion to the amount of tissue damage | 109 | 24 over; relative clause | Dying epithelial cells release factor X in proportion to tissue damage | 70 |
| Receptor Y is required for the activation of quiescent intestinal stem cells following injury | 93 | 8 over; nominalization | Receptor Y is required for stem cell activation after injury | 60 |
| scRNA-seq reveals a receptor Y-high stem cell state after injury | 64 | abbreviation | Injury expands a stem cell state with high receptor Y expression | 64 |
| We show for the first time that FX-RY signaling in ISCs acts as a dose-dependent sensor of tissue damage | 104 | 19 over; abbreviations; "first"; "We show that" | A dose-dependent damage signal matches stem cell output to tissue need | 70 |

Note on the third row: spelling out the abbreviation ("Single-cell RNA sequencing reveals a
receptor Y-high stem cell state after injury") gives 81 characters and passes, but spends the
bullet on the method. State the finding instead.

## How to write them (craft guidance, not a journal rule)

1. Take the claim table (workflow step 3). Pick the three or four steps a reader must keep:
   usually the phenomenon or source, the mechanism, the causal test, the consequence.
2. Write each as subject–verb–object in the present tense. Start with the actor, not "We".
3. One finding per bullet. No "and" joining two findings unless they are one contrast (bullet 3).
4. No method unless the method is the advance (a Resource article).
5. Spell out every abbreviation. If the spelled-out form does not fit, rewrite the bullet around
   the finding.
6. Keep the same form across bullets (all sentences without a final period, or all with).
7. Order them as the paper's argument runs. The last bullet carries the concept or consequence.

Compression moves:

| From | To |
|---|---|
| "is required for the activation of" | "activates" or "is required for … activation" |
| "following", "upon", "in response to" | "after" |
| "in the context of" | "in" |
| "leads to a reduction in" | "reduces" |
| "which is released by dying cells" | "Dying cells release" |
| "a population of cells that" | "cells that" |
| species and tissue in every bullet | once, in the first bullet |

## Abbreviation heuristic

The checker flags any token with two or more capital letters, or letters followed by digits
(for example "ISC", "scRNA-seq", "FX-RY", "IL6"). Gene and protein symbols match this pattern
too. For each flag decide:

| Token is | Action |
|---|---|
| An assay, cell type or lab shorthand | spell out or rewrite |
| A gene or protein symbol that is the paper's subject | usually kept; Cell does not say (see cell.md). Prefer a description when it fits |
| DNA, RNA and the like | not flagged; universally read |

## Alignment (craft guidance)

- Each bullet maps to a Results subheading and uses ledger terms.
- No bullet claims more than the Summary does.
- Bullets do not repeat each other, and do not repeat the title word for word.
- The eTOC blurb gives context and significance; the bullets give findings.

## Deliverable

A table of bullets with character counts, the checker output, and any flagged token with the
decision taken. Use `../templates/highlights_etoc.md`.
