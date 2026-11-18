# Comment taxonomy

*Adapted in structure from nature-skills (nature-response/references/comment-taxonomy.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

Craft guidance (not a journal rule). Classify every item by **category** and **severity** before choosing an action.

## 1. Categories

| Code | Category | Typical wording from a reviewer | Usual owner |
|---|---|---|---|
| `ADV` | Advance and significance | "incremental", "descriptive", "unclear what is new" | lead author; framing |
| `CLAIM` | Claim exceeds evidence | "the data do not show that X causes Y" | lead author; experiments or scope |
| `MECH` | Mechanism incomplete | "how does X act on Y?", "is it direct?" | experiments |
| `CTRL` | Missing control or specificity | "a second guide", "isotype control", "rescue" | experiments |
| `ALT` | Alternative explanation | "could this be due to cell composition?" | experiments or analysis |
| `GEN` | Generality | "one cell line", "one cohort", "mouse only" | experiments or scope |
| `STAT` | Statistics and replication | "what is n?", "multiple testing", "pseudoreplication" | `cell-statistics` |
| `METH` | Methods and reproducibility | "how were cells gated?", "parameters not given" | STAR Methods |
| `DATA` | Data, code, materials access | "accession not accessible", "code?" | `cell-data` |
| `LIT` | Prior work | "ref. X showed this", "please cite" | `cell-citation` |
| `PRES` | Presentation | figure legibility, order, labels, wording | figures and text |
| `INTEG` | Image or data integrity | "lanes appear spliced", "same image in two panels" | corresponding author, at once |
| `ETH` | Ethics and consent | approvals, consent, animal protocols | corresponding author |
| `SCOPE` | Request beyond the paper | a new project's worth of work | editor guidance |
| `FMT` | Journal format | limits, sections, STAR Methods | format items `F.` |

One item, one primary category. Add a secondary one if needed (`CLAIM/STAT`).

## 2. Severity

| Level | Definition | Consequence |
|---|---|---|
| **S1 central** | If unresolved, the central claim does not stand, or the editor named it as a condition | Must be met with data or a real change of claim. Blocks submission. |
| **S2 supporting** | Affects a supporting claim, generality or a key control | Data preferred; narrowing the claim is acceptable |
| **S3 clarity** | Understanding, methods detail, presentation | Text, legend or figure edit |
| **S4 minor** | Typos, citations, labels | Fix and say "Corrected" |

Rules:

- Severity comes from the effect on the paper, not from the reviewer's tone or the length of the comment.
- An editor-flagged item is S1 regardless of how the reviewer phrased it.
- `INTEG` and `ETH` are always S1.
- A mild sentence can be S1 ("I was not fully convinced that X is upstream of Y").
- The same concern from two reviewers moves up one level.

## 3. Reading between the lines

| What the reviewer wrote | What usually needs answering |
|---|---|
| "The study is largely descriptive." | The advance; a tested hypothesis; or a change of article type (cell.md §2) |
| "The authors should tone down their claims." | Title, Summary, Highlights, subheadings; not one sentence in the Discussion |
| "It would be interesting to…" | Often optional. Check the editor's letter before spending months on it. |
| "It is essential that…" / "must" | S1 or S2 |
| "I could not find…" | It may be there but hard to find. Still a presentation failure to fix. |
| "Have the authors considered…" | An alternative explanation that needs an explicit answer |
| A list of ten small figure problems | Collectively: the reviewer does not trust the figures. Fix all; say so once. |

## 4. Cross-reviewer view (plan only)

Record in the revision plan, not in the response text:

- **Duplicates**: R1.2 = R3.1. One action, two full answers.
- **Conflicts**: R1 wants the section cut, R2 wants it expanded. One decision, explained to each on its merits.
- **Clusters**: several items resolved by one experiment. Mark the experiment as high value.

## 5. Output for triage

```markdown
| ID | Verbatim (short) | Category | Severity | Editor flagged? | Duplicate / conflict | Proposed action |
|---|---|---|---|---|---|---|
| R1.1 | "…one knockdown…" | CTRL | S1 | yes (E.2) | = R3.2 | NEW_EXPERIMENT |
```
