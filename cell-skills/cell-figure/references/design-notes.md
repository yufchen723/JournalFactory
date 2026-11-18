# Design notes: type, line, colour, gray

Why the defaults are what they are. Cell rules are marked; the rest is house style.

## Type

| Element | Size | Why |
|---|---|---|
| Panel letter | 8 pt bold, capital | capital is the Cell rule; 8 pt is the top of Cell's range, so the letter is the largest text |
| Axis and panel titles | 7 pt | middle of Cell's 6–8 pt range |
| Tick labels, legends, annotations | 6 pt | bottom of the range; nothing smaller |

- Arial only (Cell rule). Arial substitutes with the same metrics (Liberation Sans, Arimo) keep
  the layout identical, so a draft made without Arial does not move when re-exported with it.
- Text stays text in the PDF (TrueType, embedded), so the typesetter can fix a typo and the
  audit can measure it.
- Mathtext shrinks sub/superscripts to 70%: use real characters (`cs.sub`, `cs.sup`).
- Rotated tick labels: 45°, right-anchored. If labels need rotating, consider flipping the plot.

## Line

| Element | Width |
|---|---|
| Axes, ticks, box outlines, error bars | 0.5 pt (Cell's minimum) |
| Data lines | 1.0 pt |
| Emphasis, scale bars | up to 1.5 pt (Cell's maximum) |

Hairlines (below 0.5 pt) vanish in print. In ggplot use `pt()`; a raw `linewidth` is not points.

## Colour

Default categorical order: blue `#0072B2`, orange `#E69F00`, sky `#56B4E9`, vermilion `#D55E00`,
purple `#CC79A7`, yellow `#F0E442`, gray `#7F7F7F`. It is the Okabe–Ito colour-blind-safe set
with green taken out of the default cycle, because Cell asks that red and green are not used
together and vermilion reads as red. Green `#009E73` is available when vermilion is not used.

- Entity colours are fixed once for the paper (cell types, regions, conditions) and stored with
  the project, not chosen per figure.
- More than seven categories: group, facet, or label directly. Do not extend the palette with
  near-duplicates.
- Sequential: viridis. Diverging: blue–white–red centred at zero. Not jet, rainbow, or red–green.
- Two-channel fluorescence: magenta and green, not red and green.
- Check with a colour-vision simulator (Cell points to Color Vision by Cal Henderson).

## Gray (Cell rule)

Fills between 10% and 80% black, at least 20% apart: at most four levels
(10, 33, 57, 80%). `cs.gray_fills(n)` / `cell_grays(n)`. For more groups use hatching or colour.

## Space

- Constrained layout with small pads; Cell asks for no more vertical space between parts than
  clarity needs.
- Panel letters at one fixed offset from each panel's top-left corner.
- Legends inside the panel when there is empty space; otherwise to the right, never floating
  between panels.
- Colour bars: slim, in an inset next to the panel, so the panel keeps its grid cell.

## Export

- Exact size in mm; no tight cropping.
- PDF for vector content; TIFF (LZW, RGB, flattened) for the same figure as raster. Cell prefers
  these two.
- 300 dpi colour or grayscale, 500 black and white, 1,000 line art (Cell rule); rasterised layers
  inside a PDF at 600 dpi.
- One file per figure, named "Figure 1.pdf", legends not in the image (Cell rule).
