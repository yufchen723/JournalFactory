# Omics and spatial panels

Craft guidance for the panel types that single-cell, spatial and epigenomic papers need. Cell
rules are marked.

## Tissue maps (spots, pixels, cells)

- **Rasterise the marks, keep the rest vector.** `rasterized=True` (Python) or `ggrastr` (R) at
  600 dpi. A 174 mm figure with 500,000 vector squares exceeds Cell's 20 MB limit (Cell rule) and
  will not open in Illustrator.
- **Square markers sized to the pixel pitch** so the tissue looks continuous: marker side in
  points ≈ pitch in data units × points per data unit. Check at print size that neighbouring
  pixels touch without overlapping.
- **Equal aspect**, no axes, no frame: `cs.image_axes(ax)`.
- **Scale bar on every map** (Cell rule for microscopy images; apply it to tissue maps too).
  Give the length in the image or in the legend.
- **Same orientation for every modality and every tool.** Packages disagree on the y direction;
  flip once in the data, state it in STAR Methods, and compare against the H&E.
- **Same section order in every figure.** Fix the order once.
- **Show the H&E or the tissue outline** next to the first map of each section.
- **Categorical maps:** at most about 8 colours distinguishable at this size; group the rest as
  gray "Other" or split into small multiples (one highlighted class per map).
- **Continuous maps:** one colour scale per feature across all sections being compared; state
  whether values are counts, normalised, or scaled. Clip at stated percentiles, not by eye.
- **Small multiples of many sections:** representative sections in the main figure, the full
  cohort in a Figure S "related to" it.

## Embeddings (UMAP)

- Rasterise. Square aspect. No axis ticks; a small "UMAP 1 / UMAP 2" arrow pair is enough.
- Label clusters directly on the plot when there is room; otherwise a legend with large keys.
- An embedding is a picture, not evidence of separation: pair it with a quantified panel.

## Genome tracks

- Vector lines at 0.5 pt, filled coverage; same y range for tracks that are compared, with the
  range printed once.
- Gene model below, gene symbol italic, coordinates and genome build in the legend.
- Highlight the region the claim is about with a light gray band (10–20% black: Cell gray rule).

## Heatmaps

- Rows and columns ordered by a stated rule (clustering method, or biology), not by default.
- Diverging data centred at zero; sequential data from zero or a stated floor.
- Label a readable subset of rows (6 pt minimum is a Cell rule); give the full table as Table S.
- Annotation bars reuse the paper's entity colours.

## Dot plots and composition

- Dot plot: size = fraction expressing, colour = mean expression; both legends present.
- Composition bars: state the denominator (per section, per region, per patient).

## Statistics on omics panels

- The replicate is the patient or the section, not the cell or the pixel. Aggregate per sample
  before testing, or use a model with a sample term. See `../../cell-statistics/references/omics-and-spatial.md`.
- Show per-sample points over the summary so the reader sees the number of independent units.

## Image plates (H&E, immunofluorescence)

- No generative or AI-assisted alteration (Cell rule). Whole-image linear adjustments only, stated in the legend.
- At least 300 dpi at the placed size (Cell rule); check with the audit, which reports the
  effective resolution of every placed image.
- Same display range for images that are compared. Channel colours named in the panel; avoid
  red with green for two-channel overlays (Cell rule): use magenta and green, or show channels separately.
- Insets marked on the overview with a box at 0.5–1 pt; a scale bar for the inset too.
