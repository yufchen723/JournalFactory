# Notice

cell-skills is part of Journal Factory.

It adapts the architecture and parts of the reasoning of **nature-skills**
(github.com/Yuan1z0825/nature-skills, commit 14ca6971, Apache License 2.0; licence text in
`../vendor/nature-skills/LICENSE`):

- the layout of each skill (router `SKILL.md`, `manifest.yaml`, `static/core`, backend fragments,
  on-demand `references/`, `templates/`, `tests/`);
- the figure contract, the default stance, the multi-panel evidence architecture and the QA
  contract of `nature-figure`;
- the structure of `nature-writing`, `nature-polishing`, `nature-statistics`, `nature-reviewer`,
  `nature-response`, `nature-data`, `nature-citation` and `nature-shared`.

Changes: all text was rewritten for Cell; journal rules were replaced by Cell's own
(`cell-shared/journal-formats/cell.md`); Nature-specific material and the AI image-generation
route were removed; all scripts were written new and none of the nature-skills code is included.
Files adapted from a specific nature-skills file say so in their first lines.

Ideas for Cell checklists were also taken from **Cell-Skills** in
github.com/brycewang-stanford/Awesome-Journal-Skills (commit 932eb233, MIT), kept unchanged in
`../vendor/cell-skills`.

Journal rules are quoted or summarised from cell.com (Cell Press, Elsevier) for the purpose of
following them; the pages themselves remain the authority.
