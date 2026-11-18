# Intake and routing

*Adapted in structure from nature-skills (nature-response/references/intake-and-routing.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

Craft guidance (not a journal rule). Use at the start of every job.

## 1. Task modes

| Mode | The user wants | Minimum input | Output |
|---|---|---|---|
| `triage-only` | To understand the reviews | Reviewer comments | Item list with category, severity, proposed action |
| `plan` | A work plan before experiments | Comments; decision letter if available | Revision plan table; ranked experiments |
| `draft` | Response text | Comments + author notes on what was done | Point-by-point response with open fields marked |
| `audit` | A check of an existing response | The draft response; ideally the manuscript | Findings; script output; fixes |
| `revise` | Edits to an existing response | The draft + the requested change | Revised passages |
| `cover-letter` | The letter to the editor | Decision letter + plan or response | Revision cover letter |
| `revision-package` | Everything | All of the above + revised manuscript | Plan, response, letter, audit |
| `appeal-like` | To contest a rejection | Decision letter + reports | Assessment first; see `difficult-cases.md` |

Pick the smallest mode that satisfies the request.

## 2. Read the decision letter

Extract, in this order:

1. Decision and whether a revised version is invited.
2. Conditions the editor sets ("the central mechanism needs independent support").
3. Which reviewer points the editor marks as essential or as optional.
4. Experiments the editor says are not required.
5. Deadline and resubmission instructions.
6. Required files and formats named in the letter.
7. Anything about what reviewers will see.

Give each instruction an ID (`E.1`, …). They enter the plan like reviewer comments and are answered in the cover letter.

Do not fill gaps from memory. Items 5–7 are not specified in cell.md; if the letter is silent, tell the user to check the letter, the submission system or cell.com.

## 3. Split and number the comments

- One concern per item. A paragraph with "and also" usually holds two.
- Keep the verbatim text with each item.
- Keep the reviewer's own numbering visible if they numbered their points (`R2.3` = Reviewer 2, their point 3). If you split their point 3, use `R2.3a`, `R2.3b` in the plan and say so.
- General remarks ("the paper is descriptive") are items too. They usually carry the highest severity.
- Praise is not an item. Do not answer it at length.

## 4. Readiness states

| State | Meaning | What may be written |
|---|---|---|
| `plan_only` | No work done yet | Plan; proposed actions; no "we have" sentences |
| `draft_with_placeholders` | Some work done; locations or results missing | Response text with `AUTHOR_INPUT_NEEDED` fields |
| `draft_complete_unverified` | Authors report all done; manuscript not seen | Full text; every location marked unverified |
| `ready` | All items done, located, audited | Final package |

State the readiness at the top of every output.

## 5. When to ask, when to proceed

Ask one short question when:

- the decision is unknown and package-level work depends on it;
- it is unclear whether an experiment was done or only planned;
- two reviewers conflict and the choice changes the science.

Proceed without asking when:

- the task is triage or a local wording edit;
- a missing fact can be carried as `AUTHOR_INPUT_NEEDED` without blocking the rest.

## 6. Stage reminder — Cell rule

At revision, Cell requires the manuscript in its component order with STAR Methods format, plus a cover letter and a point-by-point response (cell.md §1, §3, §8). A first submission was free format, so a revision often needs format work that no reviewer asked for. Add these as plan items with the prefix `F.` (format):

| ID | Item | Source |
|---|---|---|
| F.1 | Convert methods to STAR Methods; key resources table | cell.md §8 |
| F.2 | Resource availability with its three subsections | cell.md §3 |
| F.3 | Legends: test, asterisk key, n, error bars, "See also" | cell.md §4 |
| F.4 | "Limitations of the study" in the Discussion | cell.md §3 |
| F.5 | Supplemental titles "related to Figure N"; supplemental index | cell.md §7 |
| F.6 | Word and display-item limits | cell.md §2 |

Hand F.1–F.2 to `cell-data`, F.3 to `cell-statistics`.
