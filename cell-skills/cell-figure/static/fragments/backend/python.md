# Backend: Python (matplotlib)

Adapted in structure from nature-skills (nature-figure/static/fragments/backend/python.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

**Python-only rule.** With Python chosen, all drawing, previews and exports are matplotlib. No R
graphics device for a quick look. If matplotlib or a package is missing, stop rendering and report it.

## Quick start

```python
import sys; sys.path.insert(0, "<JF>/cell-skills/cell-figure/scripts")
import cell_style as cs, cell_templates as ct

cs.use_cell_style()                                   # Arial, 7/6 pt, 0.5 pt axes, RGB, fonts embedded
fig, axd = cs.cell_mosaic([["A", "A", "B"],           # keys become the panel letters
                           ["C", "D", "B"]], width="full", height_mm=120)
ct.spatial_map(axd["A"], x, y, categories=region, colors=REGION_COLOURS, pixel_um=10, bar_um=1000)
note = ct.bar_points(axd["B"], {"Ctrl": ctrl, "Treated": trt}, ylabel="Signal (a.u.)")   # returns legend text
...
cs.label_panels(axd)                                  # capital, bold, 8 pt, same offset on every panel
report = cs.save_cell(fig, "out/Figure 1")           # gates -> PDF + LZW TIFF -> file audit -> preview PNG
```

`save_cell` does, in order:

1. alignment gate (panel edges in a shared row or column agree within 1.5 pt);
2. text-overlap gate (no text on text, nothing off the page);
3. style check (text 6–8 pt, strokes 0.5–1.5 pt, letters A, B, C…, red with green);
4. writes `Figure 1.pdf` (vector, TrueType text, rasterised layers at 600 dpi) and `Figure 1.tiff`
   (300 dpi, RGB, LZW, flattened) at the **exact** figure size;
5. runs `validate_cell_figure.py` on both and writes `Figure 1.qa.json`;
6. writes `Figure 1.preview.png` for the visual check.

A failed alignment or overlap gate raises `CellFigureError` and nothing is exported. Use
`strict=False` only for a draft, and say it is a draft.

## Things that go wrong

| Symptom | Fix |
|---|---|
| "Arial is not installed" | The figure is drawn in Liberation Sans (same metrics). Fine for drafts and first submission; re-export on a machine with Arial for production. |
| Text at 4.9 pt in the PDF audit | A mathtext sub/superscript. Use `cs.sub()` / `cs.sup()`. |
| Width changed after export | Something passed `bbox_inches="tight"`. Do not; set the size and let constrained layout fit. |
| PDF above 20 MB | Too many vector marks. Pass `rasterized=True` for point clouds above about 20,000 points. |
| Alignment gate fails on an image panel | Use `cs.image_axes(ax)` (keeps the frame in its grid cell), or mark a deliberate exception with `ax.set_gid("cell-aux")` and note why. |
| Colour bar pushes a panel out of line | Use the templates' inset colour bar (`ct._colorbar`), not `fig.colorbar(ax=...)`. |
| Line art or black-and-white figure | `cs.save_cell(fig, stem, kind="lineart")` (1,000 dpi) or `kind="bw"` (500 dpi). |

## Useful calls

- `cs.cell_figure("single" | "mid" | "full" | mm, height_mm, nrows, ncols)` — regular grids.
- `cs.gray_fills(n)` — at most four grays that satisfy Cell's gray rule.
- `cs.red_green_clash(colours)` — True when a set mixes red and green.
- `cs.scale_bar(ax, length_in_data_units, "1 mm")` — required on tissue and microscopy images.
- `cs.graphical_abstract_canvas()` — 1200 × 1200 px at 300 dpi.
- `python cell_templates.py --demo OUT` — a six-panel test figure from simulated data.

More: `references/template-catalog.md`, `references/omics-spatial-panels.md`, `references/qa-contract.md`.
