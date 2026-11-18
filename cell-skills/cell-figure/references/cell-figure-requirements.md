# Cell figure requirements

The rules themselves are in `../../cell-shared/journal-formats/cell.md` §5 (production figures),
§4 (legends), §6 (graphical abstract), §7 (supplemental figures). This file says how the skill
applies them and where Cell is silent.

## What the scripts enforce

| Cell rule | In `cell_style` / `cell_theme.R` | In `validate_cell_figure.py` |
|---|---|---|
| Width 85 / 114 / 174 mm | figure created at that width; wider refused | FAIL above 174; WARN when not a column width |
| Fits one page; ≤ 165 × 200 mm recommended | warning above 200 mm | WARN above 200 mm; FAIL above one page |
| Arial only, embedded | Arial first; warning when substituted | FAIL other fonts or not embedded; WARN Arial substitute; FAIL Type 3 |
| Text about 6–8 pt | 7 / 6 / 8 pt defaults; base size outside 6–8 refused | WARN outside 6–8; FAIL below 5 |
| Capital panel letters | `label_panels`, `cell_tags()`; lowercase refused | checked on the live figure (A, B, C… without gaps) |
| Strokes 0.5–1.5 pt | 0.5 pt axes and ticks, 1 pt data lines | WARN outside the range |
| RGB | RGB export, alpha flattened | FAIL CMYK; WARN alpha channel |
| No red with green | default cycle has no green; `red_green_clash` | WARN when both are in vector elements |
| Gray fills 10–80%, ≥ 20% apart | `gray_fills(n)`, at most 4 | WARN |
| 300 / 500 / 1,000 dpi | `kind=` in `save_cell` | FAIL for placed images and raster files below the rule |
| TIFF or PDF preferred; LZW | PDF + LZW TIFF | format, compression |
| ≤ 20 MB | warning | FAIL |
| One layer | flattened on export | WARN multi-page TIFF |
| File name "Figure 1.tif" | — | INFO |

## Where Cell is silent (house choices, free to change)

- Size and weight of panel letters (we use 8 pt bold).
- The palette, apart from "no red with green".
- Tick length, legend frame, spine style.
- Height of a one-column figure.
- A hard minimum for text: Cell says "about 6–8 pt". We warn outside it and fail only below 5 pt.

## Stage

| Stage | What to run |
|---|---|
| First submission | `validate_cell_figure.py --stage initial`. Any format is accepted; small files (1–2 MB) help reviewers. Figures may sit in the manuscript. |
| Revision | Not required yet by Cell, but build to production rules now. |
| Final files | `validate_cell_figure.py` with no stage flag. Every FAIL must be fixed. Upload each main figure as its own file, legends in the manuscript. |

## Supplemental figures

- Named Figure S1, S2…; title ends "related to Figure N".
- They go into one PDF (Document S1) with their legends, Arial 10 pt for the document text,
  ≤ 50 MB. Up to 20 recommended; one supplemental figure may span pages.
- Same drawing rules as main figures (the SI "should match the standards of the main article").

## Image integrity (always, at every stage)

Whole-image adjustments only; spliced lanes marked; background never hidden; scale bar on every
microscopy image; stitched images declared; originals kept; no generative or AI-assisted creation
or alteration of research images. See cell.md §5.
