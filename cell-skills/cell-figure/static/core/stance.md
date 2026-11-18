# Default stance

Adapted in structure from nature-skills (nature-figure/static/core/stance.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

Everything here is craft guidance unless marked "Cell rule".

## Composition

- Classify first: quantitative grid, schematic-led composite, image plate + quantification, or
  asymmetric mixed figure.
- One **hero panel** carries the claim; the others support it. Do not fill the page with
  equal-sized plots.
- A Cell main figure usually has 5–10 panels. Seven figures is the ceiling for the whole paper
  (Cell rule), so each figure has to carry one full step of the argument; overflow goes to
  Figure S "related to Figure N".
- Read order left to right, top to bottom; letters follow the order the text cites them
  (Cell rule: figures are cited in numerical order; keep panels in order too).
- Keep vertical gaps as small as clarity allows (Cell rule).

## Type

- 7 pt for axis titles, 6 pt for ticks and legends, 8 pt bold capital panel letters. The 6–8 pt
  range and the capitals are Cell rules; the split is house style.
- Gene symbols italic, proteins roman (Cell style rule for text; apply it in figures too).
- Write subscripts and superscripts as real characters (`cs.sub(2)`, `cs.sup(-5)`): mathtext
  shrinks them to 70%, which is 4.9 pt under a 7 pt label.
- Sentence case for labels. Units in parentheses: "Distance (µm)".

## Colour

- One palette per paper. Fix the colour of each recurring entity (cell type, region, condition)
  once and reuse it in every figure.
- Never red with green (Cell rule). Default categorical set: blue, orange, sky blue, vermilion,
  purple, yellow, gray. Sequential: viridis. Diverging: blue–white–red centred at zero.
- No rainbow maps. No colour as the only distinction when shape or position can also carry it.
- White background for plots; black only for fluorescence image plates.

## Evidence on the page

- Show individual data points with every mean or box (Cell recommendation).
- Do not print a value on every bar. The axis carries values; print only the number the panel argues.
- Direct labels beat legends when positions are fixed.
- Same uncertainty definition in every comparable panel, and the same replicate unit.
- Statistics, n, error bars and scale bars are part of the figure: collect them while drawing and
  pass them to the legend.

## When not to use this skill

Interactive or web plots; exploratory plots with no manuscript target; layout done by hand in
Illustrator (use the Journal Factory studio for placement, then run the audit on its export).
