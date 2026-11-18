# Stage 4 · Figures

- Size comes from the profile: `jf journal <id>` → widths, text size, panel letters. Draw at final size; never scale a finished figure.
- matplotlib: `pdf.fonttype 42`, `svg.fonttype none`, Arial/Helvetica, text 6–8 pt (Cell) or 5–7 pt (Nature), lines 0.5–1 pt. R: `cairo_pdf` or `svglite`.
- Vector for line art and text; raster (≥ 300 dpi at final size) only for images and dense maps (`rasterized=True` for > 50k points).
- Colour: one entity = one colour in every figure; colour-blind safe; never red/green alone; sequential maps perceptually uniform; diverging centred at 0.
- Every panel states n and the unit (patients, sections), the test, and what error bars are. Spatial maps carry a scale bar.
- Assemble in the built-in studio (`jf paper init`): one canvas page per figure at the journal width; Journal tab → Check.
- `jf check-figure <file> --journal <id>` before hand-off: width, height, fonts, smallest text, resolution.
- Craft guides: `vendor/nature-skills/nature-figure`, `vendor/k-dense/scientific-visualization`, `vendor/cell-skills/skills/cell-figures`.
- Image integrity: no generative alteration of data images; same processing across compared panels; disclose stitching and contrast changes.
