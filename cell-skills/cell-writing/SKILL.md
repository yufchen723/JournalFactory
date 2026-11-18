---
name: cell-writing
description: Draft, restructure, compress or check the text of a manuscript for the journal Cell (Cell Press) from author-provided evidence - title, Summary (150 words), Highlights, eTOC blurb, Introduction, Results with finding-stating subheadings, Discussion with "Limitations of the study", STAR Methods, figure titles and legends, cover letter, and Cell-style polishing - using only the Cell rules recorded in cell-shared/journal-formats/cell.md and labeling everything else as craft guidance. Includes a stdlib checker (scripts/cell_text_check.py) for the countable limits. Not for figure production or for reviewer-response letters.
---

Adapted in structure from nature-skills (nature-writing/SKILL.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

# Cell Manuscript Writing — Router

## Routing protocol

For a new task follow steps 1–5. For a follow-up edit, reuse the choices and files already
loaded; load another file only when the scope changes.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares what is always loaded, the `part` and `stage`
axes, and the on-demand references with their conditions.

Read every file under `always_load`:

- `../cell-shared/journal-formats/cell.md` — the only source of Cell numbers and rules
- `../cell-shared/core/terminology-ledger.md`
- `static/core/stance.md`
- `static/core/workflow.md`

### 2. Detect the axis values

- `part` — title / summary / highlights / etoc / introduction / results / discussion /
  star-methods / legends / cover-letter. May be several. A request for "the whole paper" selects
  the template `templates/manuscript_skeleton.md` and the parts in the drafting order of
  `static/core/workflow.md`.
- `stage` — initial / revision / final (cell.md §1). Default: revision, because it is the
  strictest stage for text. At `initial`, report format rules as "needed later", not as failures.
- Article type — research article by default. Resource, Theory, Short article and Matters
  Arising have their own limits in cell.md §2; state which one applies.

Say the detected values in one line before drafting, so the author can correct them. This is a
progress note, not an approval gate.

### 3. Load the matching reference

For each selected part, read the file the manifest maps it to (one file per part). Do not read
all of `references/`. The `summary` part maps to `../cell-shared/core/cell-summary.md`, which
holds the rules, the sentence budget and the drafting procedure in one place.

### 4. Draft from the loaded material

Priority order when sources disagree:

1. `cell.md` — Cell rules. Never overridden by craft guidance.
2. `static/core/stance.md` — author evidence first; no invented results, numbers or references.
3. The part's reference file.
4. Shared contracts in `../cell-shared/core/` when the manifest condition is met.
5. `references/polishing.md` — sentence-level style, applied last.

Every statement about what Cell requires must carry its source as `cell.md §N`. If the rule is not
in cell.md, write `not specified by Cell (see cell.md)`. Do not substitute a Nature rule or a
number from memory. Label all other advice as craft guidance.

If evidence is missing, write a placeholder in square brackets and list it under
`Assumptions or missing inputs`. Do not invent content.

### 5. Check before returning

Run the checker when the output has a countable limit:

```bash
python scripts/cell_text_check.py manuscript.md                 # full draft, revision stage
python scripts/cell_text_check.py manuscript.md --stage initial # first submission
python scripts/cell_text_check.py --highlights highlights_etoc.md
python scripts/cell_text_check.py --self-test
```

Resolve the script path relative to this skill directory. Report its FAIL and WARN lines with
the draft. WARN lines are heuristics; read the context before acting.

## On-demand references (see manifest for the full conditions)

| Trigger | File |
|---|---|
| Summary (also the `summary` part file) | `../cell-shared/core/cell-summary.md` |
| Introduction funnel, exact gap, alignment with Results | `../cell-shared/core/cell-introduction.md` |
| Claim order across the 7 display items; Results versus Discussion; limitations | `../cell-shared/core/cell-results-discussion.md` |
| Text at or near 7,000 words; main text versus STAR Methods versus Figure S / Table S | `../cell-shared/core/main-text-discipline.md` |
| Audit of an existing draft for drift | `../cell-shared/core/consistency-sweep.md` |
| "Is this a Cell rule or advice?" | `references/source-basis.md` |
| Language-only edit of existing prose | `references/polishing.md` |
| Full-paper scaffold | `templates/manuscript_skeleton.md` |
| Front-matter file | `templates/highlights_etoc.md` |
| STAR Methods scaffold | `templates/star_methods_skeleton.md` |

## Boundaries

- This skill writes and checks text. Figure production rules (cell.md §5) and the graphical
  abstract (cell.md §6) belong to a figure skill; this skill only keeps their labels and titles
  consistent with the text.
- Revision correspondence (point-by-point response) is out of scope. cell.md §1 only records that
  a cover letter and a point-by-point response are required at revision.
- Journal policy text that was not read (journal-policies page, STAR Methods author guide PDF,
  final file requirements PDF; see the header of cell.md) is never paraphrased from memory.
- Sibling Cell skills, when installed next to this one (`cell-figure`, `cell-statistics`,
  `cell-response`, `cell-reviewer`), own figures, statistical reporting, revision letters and
  simulated review. Hand over to them; do not duplicate their rules here.
- Files under `vendor/` are reference text only. Do not run anything from them.
