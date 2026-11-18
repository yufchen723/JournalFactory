# Response structure

*Adapted in structure from nature-skills (nature-response/references/response-structure.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

## 1. What Cell asks for at revision — Cell rule

From cell.md §1 (source page: revise-manuscript) and §8:

| Item | Rule |
|---|---|
| Cover letter | required with the revision |
| Point-by-point response | required with the revision |
| Manuscript components and order | as in cell.md §3 |
| STAR Methods format | **required** at revision and for acceptance |

That is all cell.md records. The following details are **not specified in cell.md — check cell.com (revise-manuscript page) or the decision letter**:

- (resolved: Cell rule (cell.md §1): the revision cover letter briefly summarises how the revision addresses the reviewer and editor comments and is confidential to the editor.)
- whether a marked-up manuscript (tracked changes, coloured text) is required, and its form;
- whether the response is one file or one per reviewer, and who sees it;
- length limits for the letter or response; whether figures may be embedded in the response;
- deadline and file naming.

Until checked, use the craft defaults below and tell the user which points are unverified.

## 2. The three documents — craft guidance (not a journal rule)

| Document | Reader | Job |
|---|---|---|
| Revision plan | authors only | Track every item to done. Never sent. |
| Point-by-point response | editor and reviewers | Answer each comment with evidence and location |
| Revision cover letter | editor | Summarise how the revision addresses the comments; raise anything for the editor's attention |

## 3. Point-by-point response: anatomy

```text
Title line: Response to reviewers — [manuscript ID], "[title]"

Opening (5–10 lines)
  - one sentence of thanks, specific
  - the main changes, as a short list (new experiments, reanalyses, reframing)
  - how changes are marked and how locations are given
  - renumbering note if figures changed ("former Figure 3 is now Figure 4")

Editor's points (if the letter set conditions)
  E.1 … response … location

Reviewer 1
  Comment R1.1   verbatim quote
  Response       answer first; evidence; what changed
  Changes in the manuscript   location; quoted new text if short

Reviewer 2 …
```

Per comment:

1. **Quote** the full comment, unchanged. Use a visual distinction (block quote or italic).
2. **Answer in the first sentence.** "We agree and have…", "We performed…", "We respectfully disagree because…".
3. **Evidence.** The result in one or two sentences with the numbers and the panel. Embed a small figure only when the data are not in the manuscript and reviewers need to see them; say that it is for reviewers only.
4. **Change.** Where it is in the manuscript (format in `action-mapping.md` §5). Quote new sentences when they are short.
5. **If nothing changed**, write "No change to the manuscript" and why.

Keep the field labels `Response:` and `Changes in the manuscript:` exactly. `scripts/check_response_package.py` relies on them.

## 4. Rules for the response

- Each answer stands alone. Repeat the answer for a duplicate concern; do not write "see our response to Reviewer 2".
- Refer to figures by their **new** numbers in the authors' text. Reviewers' quotes keep the old numbers; give a mapping when it helps ("Figure 2D, formerly Figure 3A").
- Use the same names for entities as the manuscript.
- Do not introduce data that appear nowhere in the manuscript or supplement without saying so and saying why.
- Length follows the comment. S4 items get one line. S1 items get what the evidence needs.

## 5. Revision cover letter: anatomy

```text
1. Manuscript ID, title, article type; "revised version".
2. One paragraph: the main concerns as the authors understood them, and
   the main changes that answer them (new experiments first).
3. Editor's conditions, each with a one-line answer (E.1, E.2 …).
4. Anything the editor should know that does not belong in the response:
   - a request the authors could not meet, with the substitute;
   - a disagreement that needs editorial judgment;
   - a conflict between reviewers and how it was resolved;
   - changes to authorship, title, article type, data access.
5. Compliance line: STAR Methods format, limits met (state the word count
   and number of display items), files included.
6. Signature of the corresponding author / lead contact.
```

One page. No repetition of the response. No sales language.

The cover letter is confidential to the editor (cell.md §1); the point-by-point response is written for the reviewers.

## 6. Manuscript-side requirements that reviewers will re-check

- New experiments are in STAR Methods, never in the supplement (**Cell rule**, cell.md §7, §8).
- New supplemental figures are titled "Figure S#. [title], related to Figure N" and named in the main legend with "See also Figure S#" (**Cell rule**, cell.md §4, §7).
- New legends state test, asterisk meaning, n biological and technical, error bars (**Cell rule**, cell.md §4).
- "Limitations of the study" reflects limits conceded in the response (**Cell rule** for the subsection's existence, cell.md §3).
- Main text stays under 7,000 words including main legends; no more than 7 figures and/or tables (**Cell rule**, cell.md §2).
