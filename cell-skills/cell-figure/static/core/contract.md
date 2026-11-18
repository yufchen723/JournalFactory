# Figure contract: decide these before any code

Adapted in structure from nature-skills (nature-figure/static/core/contract.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

A figure is an argument. Write the contract first, show it to the user when the figure is new, then draw.

## The six lines

```text
1 Claim        one sentence the figure must defend = the Results subheading = the figure title
2 Evidence     panel -> its job in the argument (see multipanel-evidence-architecture.md)
3 Archetype    quantitative grid | schematic-led composite | image plate + quantification | asymmetric mixed
4 Backend      Python or R, one per figure
5 Size, stage  single 85 mm | mid 114 mm | full 174 mm; height <= 200 mm; initial or production
6 Legend facts test, n (biological / technical), error bars, scale bars, "See also Figure S…"
```

Cell asks that figure titles reuse the Results subheadings (cell.md §4). So line 1 is written once
and used three times: subheading, figure title, contract.

## Rules that hold for every figure

**Cell rules (cell.md §5)**

- Width 85, 114 or 174 mm; each figure fits one page; recommended at most 165 × 200 mm.
- Arial only, embedded; text about 6–8 pt at print size.
- Capital panel letters.
- Strokes 0.5–1.5 pt.
- RGB; red and green not together; gray fills 10–80% black and at least 20% apart.
- Production files: TIFF or PDF preferred, at most 20 MB, one file per figure with all panels,
  no title or legend inside the image.
- Resolution at print size: 300 dpi colour or grayscale, 500 black and white, 1,000 line art.
- Scale bar on every microscopy image. Individual data points next to means (recommended).
- No generative or AI-assisted creation or alteration of research images.

**Craft rules (not journal rules; from the nature-figure contract)**

- **Data integrity.** Use every observation the user gave. Never drop rows to make a plot lighter:
  rasterise the marks or aggregate with a stated rule. Record any exclusion (before/after counts,
  rule, reason).
- **Claims, not tables.** Do not turn each results table into its own panel.
- **Paired effects.** When the effect is within patient, section or sample, show the paired
  differences, not two overlapping distributions.
- **One backend.** All drawing, previews and exports come from the chosen language.
- **Exact size.** Set the figure size in mm and export without "tight" cropping, which changes
  the physical width.
- **Gates.** Panel alignment (1.5 pt), no colliding text, then the file audit. A failed gate
  blocks delivery; a gate that could not run is reported as not run, never as passed.

## Missing runtime

If the chosen language or a package is missing, stop rendering, keep checking what can be checked,
and report the exact blocker with the install command. Do not switch language to get a picture.

## Privacy

Figure code, legends and reports do not print private paths, patient identifiers or sample names
that could identify a person. Use the study's public sample labels.
