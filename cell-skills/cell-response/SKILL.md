---
name: cell-response
description: "Plan, draft, audit or revise a Cell revision package: revision plan, point-by-point response to reviewers, revision cover letter, and the consistency check between response and revised manuscript (figure renumbering, 'related to Figure N', highlights and eTOC still true, 7,000-word and 7-item limits). Use after reviews arrive. Mock review belongs to cell-reviewer; first-submission cover letters do not belong here."
---

# Cell Reviewer Response — Router

*Adapted in structure from nature-skills (nature-response/SKILL.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.*

## Two kinds of statement

- **Cell rule (cell.md §N)**: recorded in `../cell-shared/journal-formats/cell.md`.
- **Craft guidance (not a journal rule)**: how to plan and write a response. Never present it as Cell policy.

If a rule is needed and is not in cell.md: "not specified in cell.md — check cell.com". The decision letter and the editor's instructions override this skill.

## Routing protocol

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml), then every file under `always_load`:

- `static/core/stance.md` — purpose, default stance, red lines, source hierarchy.
- `static/core/workflow.md` — inputs, the workflow, the output package.

### 2. Identify mode and decision inline

There is no content axis. The variation is identified at run time:

- **task mode**: `triage-only` / `plan` / `draft` / `audit` / `revise` / `cover-letter` / `revision-package` / `appeal-like`.
- **decision**: take it from the editor's letter. If it is not supplied and the work depends on it, ask once. Do not infer it from the number or tone of comments.

Use `references/intake-and-routing.md` to fix mode, minimum inputs and readiness before drafting.

For a local edit or a bounded audit, return the passage or the findings and the missing facts. Do not expand into a full package unless asked.

### 3. Run the workflow

Follow `static/core/workflow.md`: extract editor and reviewer items, classify, map each to an action and its evidence, build the revision plan, draft, map to manuscript locations, audit the package.

What Cell requires at revision (**Cell rule**, cell.md §1, §3, §8):

- a cover letter and a point-by-point response;
- the manuscript components in Cell's order;
- STAR Methods format.

### 4. Open references only when needed

Use the `references.on_demand` table in the manifest.

### 5. Scripts and templates

```bash
python scripts/check_response_package.py response.md --manuscript manuscript.md
python scripts/check_response_package.py --self-test
```

Resolve the path relative to this skill directory. The script checks that every comment has a response and a manuscript location, that figure and panel references exist in the manuscript's legends, and lists promises ("we will", "future work"). It is mechanical; it does not judge whether a response answers the comment.

Templates: `templates/revision_plan.md`, `templates/point_by_point.md`, `templates/revision_cover_letter.md`. Worked example: `examples/major-revision-example.md`.

## Red lines

- Do not invent experiments, results, citations, figure panels, line numbers, editor instructions or manuscript changes. Write `AUTHOR_INPUT_NEEDED`.
- Do not write "we have added" for work that is not done. Action, work status and package readiness are separate fields.
- Do not soften or shorten a reviewer's comment when quoting it.
- Do not leave a promise in a response that is submitted: each "we will" becomes done, or is removed and explained.
- Do not state a Cell requirement that is not in cell.md.
