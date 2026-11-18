# Journal adaptation: one line, any journal

The nine stages are the same for every journal. What changes is the profile the stages read:
`journals/<id>.json`. `jf adapt` picks that profile and prints how each stage is set for it.

## Three ways in

| The user says | Run | What happens |
|---|---|---|
| a journal ("for Nature", "Cancer Cell", "NC") | `jf adapt <name>` | name, id or common abbreviation is matched to a built-in profile |
| "which journal?" / nothing | `jf adapt auto --paper projects/<p>/paper.json [--scenario <s>]` | journals are ordered by fit to the evidence scores; the highest-tier one that fits is set up. None fits: say so, show what is short (`jf fit`), do not pick one anyway |
| a journal that is not built in | `jf adapt "<Journal>" --new [--family cell-press\|nature\|science\|other] [--tier n]` | a draft profile is written from the publisher-family template: structure filled, **every limit empty**, `verified: memory`, with a list of what to read on the journal's site |

Add `--set projects/<p>/paper.json` to record the journal as the project's target. Changing the target of an existing project is the user's decision: ask first.

## After `--new`: finish the profile before formatting

1. Open the journal's author pages in a browser (many publisher sites refuse automated fetches). Read: article types, manuscript preparation, figure/artwork guide, final files.
2. Fill `limits`, correct `figure`, `sections`, `front_matter`, `methods`, `supplemental`; add each page to `sources` with `status: read` and the date; set `verified.level` to `official` (or `secondary` when only third-party guides were read) and remove `to_confirm` items as they are done.
3. Set `bar` from 3–5 recent papers of that journal in the field scan (`journals/_dimensions.json`). Until then the bar is the template's and `jf fit` for this journal means little: say so.
4. Never fill a limit from memory or from another journal of the same publisher.

## What follows the profile automatically

| Stage | Reads from the profile | Tool |
|---|---|---|
| 2 Journal | `bar`, `tier` | `jf fit`, `jf adapt auto` |
| 3 Story | `limits.main_display_items`, `supplemental` | plan report |
| 4 Figures | `figure`: widths, fonts, type size, panel-letter case, strokes, resolution, formats | `scripts/journal_style.py` (`use_journal`, `mosaic`, `label_panels`, `save`), `jf figure`, `jf demo`, studio Journal tab |
| 5 Text | `limits`, `sections`, `front_matter` | `jf count`, studio Journal tab |
| 6 Statistics | `methods` | `jf cell legends` (journal-neutral check of what a legend states) |
| 7 Submission | `extras`, `front_matter` | guide 07 |
| 8 Revision | — | `jf cell response` (journal-neutral) |

Figure code is the same for every journal:

```python
import sys; sys.path.insert(0, "$JF/scripts")
import journal_style as js
js.use_journal("nature")                 # warns when the profile is not `official`
fig, axd = js.mosaic([["A", "A", "B"], ["C", "D", "B"]], width="full", height_mm=120)
js.templates.volcano(axd["C"], log2fc, padj, labels=genes)
js.label_panels(axd)                     # a, b, c for Nature; A, B, C for Cell Press
js.save(fig, "out/Figure 1")             # gates -> PDF (+ TIFF when the journal lists it) -> audit
```

Write mosaic keys as capitals; `label_panels` prints them in the journal's case.

## What does not follow automatically

- **Writing conventions** (how a Nature summary paragraph differs from a Cell Summary; Extended Data versus Figure S) live in the skill packs, not in the profile: `cell-skills/` for Cell, `vendor/nature-skills` for Nature-family, `vendor/cancer-cell-skills`, `vendor/k-dense/venue-templates` for the rest. `jf adapt` names the pack to open.
- **Cell-only checks** (`jf cell text`: Highlights, eTOC, STAR Methods headings; gray-fill rule in the figure audit) apply only when the target is Cell. Do not run them on another journal's files and report the result as that journal's rule.
- **Retargeting an existing manuscript** (e.g. Cell → Nature Communications) is a rewrite plan, not a reformat: display-item count, word limit, abstract form, methods and extra-figure naming all change. Run `jf adapt <new>` and `jf compare <old> <new>`, list the differences, and propose the plan before touching text or figures.

## `jf line`: where the project stands

`jf line projects/<p>/paper.json --workspace <manuscript dir>` prints the nine stations with what exists at each (scores, paper cards, target and fit, plan report, figure pages with panels, words written). Stations 6–8 are marked by hand in `paper.json` under `stages`. Use it to open a session ("where are we?") and to name the next station.
