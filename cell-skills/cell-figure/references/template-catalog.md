# Template catalogue

All templates draw into an axes you pass, use the Cell style, and return either the mappable or a
sentence for the legend. Python: `scripts/cell_templates.py`. R equivalents are short enough to
write inline with `theme_cell()`.

| Panel | Python | R (ggplot2) | Use for | Legend must say |
|---|---|---|---|---|
| Mean + points | `bar_points(ax, {"A": v1, "B": v2}, error="sem")` | `stat_summary(geom="col") + geom_jitter()` | few replicates per group | mean ± SEM or SD; n per group; test |
| Box + points | `box_points(ax, groups)` | `geom_boxplot(outlier.shape=NA) + geom_jitter()` | ≥ about 10 values per group | box and whisker definition; n |
| Paired | `paired_lines(ax, before, after)` | `geom_line(aes(group=id)) + geom_point()` | within-patient or within-section effects | n pairs; paired test |
| Volcano | `volcano(ax, log2fc, padj, labels)` | `geom_point() + ggrepel::geom_text_repel()` | differential genes or peaks | thresholds; test; correction |
| Heatmap | `heatmap(ax, M, rows, cols, center=0)` | `geom_tile() + scale_fill_cell_div()` or ComplexHeatmap | scaled expression, scores | what the colour is; scaling |
| Dot plot | `dot_plot(ax, frac, mean, rows, cols)` | `geom_point(aes(size=frac, colour=mean))` | markers by cluster | size and colour meaning |
| Composition | `stacked_composition(ax, table, rows, parts)` | `geom_col(position="fill")` | cell-type or region fractions | denominator |
| Spatial map | `spatial_map(ax, x, y, categories=…, pixel_um=…, bar_um=…)` | `geom_point(shape=15) + coord_fixed()` (rasterise) | tissue maps | scale bar; section id |

## Layouts

```python
cs.cell_figure("full", 100, nrows=2, ncols=3)                       # regular grid
cs.cell_mosaic([["A", "A", "B", "C"], ["D", "D", "E", "F"]], "full", 112)   # hero panels
cs.cell_mosaic([["A", "B"], ["C", "C"]], "single", 110)             # one-column figure
```

Widths by content (craft guidance):

| Width | Typical content |
|---|---|
| 85 mm | 1–3 simple plots, one image with its quantification |
| 114 mm | 3–5 panels, one heatmap with side plots |
| 174 mm | most Cell main figures: 5–10 panels with a hero panel |

Panel budget at 174 mm: with 7 pt text a plot needs about 28–35 mm of width to carry an axis title,
ticks and five tick labels. That gives four to five plots per row at most.

## Adapting your own plotting code

1. Call `cs.use_cell_style()` (or `theme_set(theme_cell())`) **after** imports such as scanpy or
   Seurat, which set their own styles.
2. Replace `plt.subplots(figsize=…)` with `cs.cell_figure(…)`; remove `tight_layout()` and
   `bbox_inches="tight"`.
3. Replace hard-coded font sizes below 6 with nothing (inherit the style).
4. Replace `savefig` with `cs.save_cell`.
5. Keep the data path and the statistics untouched; a restyle must not change a number.

## Demo

`python3 scripts/cell_templates.py --demo OUT` builds `assets/gallery/demo_full_width_simulated.png`
(six panels, 174 × 112 mm, simulated data) and prints the gate and audit results.
