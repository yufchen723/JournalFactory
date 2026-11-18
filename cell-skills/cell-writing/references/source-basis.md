# Source basis: what is official and what is craft advice

Structure of this file follows the nature-skills reference pattern (Apache-2.0); nature-skills has no equivalent file. Cell rules from cell-shared/journal-formats/cell.md.

Use this file when the author asks "is that a Cell requirement?", "where does that number come
from?", or "has this been checked?".

## 1. Three tiers

| Tier | Meaning | How it is marked in this pack |
|---|---|---|
| A. Official, read | Stated on a cell.com page read on 2026-11-18 and recorded in `../../cell-shared/journal-formats/cell.md` | "Cell rule (source: cell.md §N)" |
| B. Official, not re-read | Cell Press material that cell.md cites but that was not opened on that date | "from the author guide, confirm in the PDF" / "unverified" |
| C. Craft guidance | Writing practice; partly adapted from nature-skills (Apache-2.0) and from general scientific-writing convention | "craft guidance (not a journal rule)" |

If something is in none of the tiers, the pack says "not specified by Cell (see cell.md)".
It does not borrow a Nature rule.

## 2. Tier A — pages read (cell.md header)

| Key | Page | Used for |
|---|---|---|
| TYPES | cell.com/cell/information-for-authors/article-types | word and display-item limits (§2) |
| REVISE | cell.com/cell/information-for-authors/revise-manuscript | components, order, title, Summary, keywords, section rules, legends, tables, references (§3, §4, §9) |
| FINAL | cell.com/cell/information-for-authors/final-submission | highlights, eTOC blurb, graphical abstract requirement (§6) |
| FIG | cell.com/information-for-authors/figure-guidelines | figure production, image integrity (§5) |
| SI | cell.com/information-for-authors/supplemental-information | supplemental naming, limits, "methods never in the supplement" (§7) |
| GA | graphical abstract guidelines PDF, pages 1–2 | graphical abstract (§6) |
| STAR | cell.com/information-for-authors/star-authors-guide, landing page only | STAR Methods required at revision; key resources table; RRIDs (§8) |

## 3. Tier B — not read; confirm before relying on it

| Item | Status in cell.md | Affects |
|---|---|---|
| STAR Methods author guide PDF | not read | section headings list (§8), content of each STAR section, key resources table categories |
| Journal-policies page | not read | wording of resource-availability statements; generative-AI policy text; data and code deposition requirements |
| Final file requirements PDF | not read | production file details |
| Video guidelines | not read | Video S items |
| Initial-submission instructions | not among the pages read | cover letter at first submission; reviewer suggestions |

## 4. Rule-by-rule index for writing tasks

| Topic | Official value | cell.md | Tier |
|---|---|---|---|
| Main text length (research article) | under 7,000 words; main legends counted; STAR Methods, supplemental legends, references not counted | §2 | A |
| Display items | ≤ 7 figures and/or tables | §2 | A |
| Short article | ≤ 4,000 words incl. title, authors, affiliations, summary, legends; ≤ 4 items | §2 | A |
| Component order | Title … References (19 components) | §3 | A |
| Title | about 10–12 words; ≤ 145 characters with spaces | §3 | A |
| Summary | one paragraph; ≤ 150 words; no citations; no non-standard abbreviations | §3 | A |
| Keywords | up to 10, comma separated | §3 | A |
| Introduction | succinct; no subheadings; ends with what was achieved | §3 | A |
| Results subheadings | state the finding; reused as figure titles | §3, §4 | A |
| Discussion | no repeat of Results; "Limitations of the study" | §3 | A |
| Resource availability | three subsections | §3 | A |
| Novelty words | "novel", "first" discouraged | §3 | A |
| Style | US spelling; abbreviations; gene/protein typography; no footnotes | §3 | A |
| Legends | title; test and asterisks; replicates; measures and error bars; scale bars; "See also" | §4 | A |
| Highlights | ≤ 4; ≤ 85 characters with spaces; no abbreviations | §6 | A |
| eTOC blurb | ≤ 50 words; 2 sentences; third person | §6 | A |
| Supplemental naming | Figure S1, Table S1, Data S1, Methods S1, Video S1; "related to Figure N" | §7 | A |
| Supplemental figures | recommended ≤ 20 | §7 | A |
| STAR Methods required at revision | yes | §1, §8 | A |
| STAR section headings | five headings, one optional | §8 | B |
| References | numbered; "et al." after 10 authors; style example | §9 | A |
| Stage rules | initial free format; revision; final | §1 | A |

## 5. Tier C — craft guidance in this pack

None of the following is a Cell requirement:

- word budgets per section; the 6,700-word working target;
- the sentence budget of the Summary; "at least 60% results";
- paragraph counts and paragraph jobs for the Introduction and Discussion;
- one claim per display item; the escalation arc; the claim table;
- the three-part anatomy of a limitation and its length;
- legend layout (statistics sentence at the end), the 150–220-word target;
- callout punctuation ("Figures 1A and 1B");
- the two-sentence eTOC pattern and "[Author] et al." phrasing;
- verb calibration tables; the overclaim list beyond "novel" and "first";
- the cover-letter structure;
- the three-uses threshold for keeping an abbreviation;
- the drafting order in `../static/core/workflow.md`;
- the counting method and all heuristics in `scripts/cell_text_check.py`.

## 6. Open points in cell.md that affect writing

These are gaps or ambiguities, not rules. Do not resolve them by guessing.

1. Whether title, Summary, keywords and back matter count toward 7,000 words for a research
   article (stated only for the short article).
2. The word-counting method.
3. Whether the limits of §2 are enforced at initial submission.
4. Which abbreviations are "standard"; whether gene and protein symbols count as abbreviations
   in Highlights.
5. Whether the eTOC blurb must be exactly two sentences or at most two; how authors are named.
6. A minimum number of Highlights.
7. Where "Resource availability" sits relative to STAR Methods in the final layout.
8. What a "Methods S1" item may contain, given that methods never go in the supplement.
9. Whether "Figure" may be abbreviated, and the panel-callout form in running text.
10. Length limits for legends, Discussion, STAR Methods and reference count.
11. Whether a cover letter is required at initial submission, and its content.
12. Whether the Discussion may carry subheadings other than "Limitations of the study".

## 7. Third-party checklists

`vendor/cell-skills` and other community checklists are reference text only. Where they
disagree with cell.md, cell.md wins. Their numbers are not quoted in this pack.

## 8. When cell.md is out of date

Cell revises its author pages. cell.md is dated 2026-11-18. For a submission months later, or
when an editor's letter contradicts it, the editor and the live page win. Update cell.md first,
then the files that cite the changed section; do not patch a number in one reference file only.
