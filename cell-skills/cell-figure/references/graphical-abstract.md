# Graphical abstract (required for Cell)

Rules from the Cell Press graphical abstract guidelines, pages 1–2 (cell.md §6). The worked
examples on pages 3–8 of that PDF were not read; open it before finalising.

## Cell rules

| Item | Rule |
|---|---|
| Form | One single-panel image (a split panel is allowed); reads top to bottom or left to right, with a clear start and end |
| Content | The take-home message of **this** paper; new findings, not background; **no data items of any type** |
| Distinct | Not a copy of a model figure or diagram in the paper |
| Context | Show the biological context: location, tissue or cell type, species |
| Speculation | Leave out speculative features unless they are visibly marked as such |
| Simplicity | One process or one point; no clutter; little text; simple labels |
| Colour | Use it to guide attention; avoid heavy saturated primaries; avoid red/green and red/black contrasts |
| Size | **1200 × 1200 pixels at 300 dpi** (101.6 mm square) |
| Font | **Arial, 8–12 pt** |
| File | TIFF, PDF or JPG |
| Rights | Only original elements or elements licensed for commercial use; BioRender is accepted with the right licence and their template |
| AI | General-purpose generative AI tools **may not** be used to create it. Generative features inside dedicated scientific illustration tools (e.g. BioRender) are allowed |

## Workflow

1. **One sentence.** Write the take-home message. If it needs "and", choose the half that the
   title carries.
2. **Three to five nouns.** The objects the reader must see (for example: tissue section →
   measurement → spatial unit → cell state → outcome).
3. **Direction.** Left to right for a process; top to bottom for scale (tissue → region → cell →
   molecule); split panel for a contrast (A versus B).
4. **Sketch in boxes** on a 100 × 100 grid before any icon work. Check the start and the end are obvious.
5. **Draw** as an editable vector: Journal Factory `references/09_schematics.md` (local BioCartoon
   icons keep their credit lines; check each icon's licence allows commercial use). No image generators.
6. **Text pass.** At most about 25 words in total. Every label 8–12 pt Arial.
7. **Check:**

```bash
python3 scripts/validate_cell_figure.py graphical_abstract.tiff --ga
python3 scripts/validate_cell_figure.py graphical_abstract.pdf  --ga
```

8. **Human check.** A co-author who did not draw it states the message after five seconds.
   If the statement differs from step 1, redraw.

## Canvas in Python

```python
import cell_style as cs
cs.use_cell_style(base_pt=8)
fig, ax = cs.graphical_abstract_canvas()      # 4 × 4 in = 1200 px at 300 dpi; coordinates 0–100
ax.text(50, 94, "Title-level message", ha="center", fontsize=10, fontweight="bold")
fig.savefig("graphical_abstract.tiff", dpi=300, pil_kwargs={"compression": "tiff_lzw"})
fig.savefig("graphical_abstract.pdf")
```

In the Journal Factory studio the `graphical_abstract` page is already a square page; export it
at 1200 px.

## Common reasons a graphical abstract is sent back (craft guidance)

- It is Figure 1A or the model figure again.
- It contains a plot, a heatmap or a UMAP (data items are not allowed).
- Text below 8 pt, or a paragraph of text.
- No start and end; the eye does not know where to go.
- It shows the workflow of the study instead of the finding.
