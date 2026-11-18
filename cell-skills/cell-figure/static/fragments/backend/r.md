# Backend: R (ggplot2 / patchwork)

Adapted in structure from nature-skills (nature-figure/static/fragments/backend/r.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

**R-only rule.** With R chosen, all drawing, previews and exports are R. No matplotlib preview.
If R or a package is missing, stop rendering and report the blocker with the install command.
The Python audit script only reads the exported files; it draws nothing.

## Quick start

```r
source("<JF>/cell-skills/cell-figure/scripts/cell_theme.R")
library(ggplot2); library(patchwork)
theme_set(theme_cell())                     # Arial, 7/6 pt, 0.5 pt axes

p1 <- ggplot(d, aes(group, value, fill = group)) +
  stat_summary(fun = mean, geom = "col", alpha = .55, colour = "black", linewidth = pt(0.5), width = .6) +
  geom_jitter(width = .12, size = .6) +     # individual points (Cell recommendation)
  scale_fill_cell(guide = "none")

p <- (p1 | p2) / p3 + cell_tags()           # capital letters A, B, C
save_cell_r(p, "out/Figure 1", width = "full", height_mm = 110)   # PDF + LZW TIFF + audit
```

## Rules of thumb

- **Line widths in points:** always `linewidth = pt(0.5)`. A raw ggplot `linewidth = 0.5` is
  1.07 pt; `0.2` is 0.43 pt, under Cell's 0.5 pt minimum.
- **Text sizes:** `theme_cell()` sets theme text. `geom_text(size = )` is in mm: use
  `size = 6 / .pt` for 6 pt.
- **Colour bars:** `guide = guide_colourbar_cell()`; the default ticks are thinner than 0.5 pt.
- **Palette:** `scale_colour_cell()`, `scale_fill_cell()`, `scale_fill_cell_seq()` (viridis),
  `scale_fill_cell_div()` (blue–white–red). No `scale_*_distiller(palette = "RdYlGn")`, no rainbow.
- **Large point clouds:** `ggrastr::rasterise(geom_point(...), dpi = 600)`.
- **Heatmaps with ComplexHeatmap:** set `gp = gpar(fontsize = 6, fontfamily = "Arial")` on every
  text argument and draw inside `cairo_pdf(width = 174/25.4, ...)`; ComplexHeatmap ignores ggplot themes.
- **Seurat / ArchR plots:** they return ggplot objects; add `+ theme_cell()` last, and check the
  point size and legend text again, because these packages set their own sizes.
- **Panel alignment:** patchwork aligns plot areas. Fixed-aspect panels (`coord_fixed`) break it;
  give them their own row or column.

## Things that go wrong

| Symptom | Fix |
|---|---|
| Arial missing | The device substitutes a font; the audit names it. Re-export with Arial for production. |
| `cairo_pdf` unavailable | The function falls back to `pdf()` with Helvetica; the audit will flag the font. Install Cairo support. |
| Strokes under 0.5 pt in the audit | A geom or guide with a raw `linewidth`. Marker outlines also show up here; those are acceptable. |
| Tags are lowercase | `plot_annotation(tag_levels = "a")` somewhere; use `cell_tags()`. |

Tested with ggplot2 + patchwork under cairo. `ragg` is used for TIFF when installed, otherwise base `tiff()`.
