# QA contract: before a figure is handed over

Adapted in structure from nature-skills (nature-figure/references/qa-contract.md), Apache-2.0; Cell rules from cell-shared/journal-formats/cell.md.

Three layers. All three, every time a figure is made or changed.

## 1. Gates on the live figure (before export)

`cs.save_cell()` runs them; `cs.run_gates(fig)` runs them alone.

| Gate | Passes when | On failure |
|---|---|---|
| Panel alignment | Panels in a shared grid row or column have edges within 1.5 pt | Blocks export. Fix the layout. A deliberate exception: `ax.set_gid("cell-aux")` and say why in the QA notes. |
| Text overlap | No text box overlaps another; nothing off the page | Blocks export. Shorten or move labels, widen the panel, reduce the number of labels. |
| Style | Text 6–8 pt, strokes 0.5–1.5 pt, letters A, B, C… without gaps, no red with green | REVIEW: fix, or record why it stands. |

R: patchwork aligns plot areas by construction; check alignment by eye on the preview and run
layer 2.

## 2. Audit of the exported files

```bash
python3 scripts/validate_cell_figure.py "Figure 1.pdf" "Figure 1.tiff"          # production
python3 scripts/validate_cell_figure.py "Figure 1.pdf" --stage initial           # first submission
python3 scripts/validate_cell_figure.py "Figure 1.tiff" --kind lineart           # 1,000 dpi rule
python3 scripts/validate_cell_figure.py GA.tiff --ga                             # graphical abstract
```

| Verdict | Meaning |
|---|---|
| PASS | No rule broken, nothing to review |
| REVIEW | Warnings: read each one, fix or justify |
| FIX BEFORE UPLOAD | A stated Cell rule is broken |
| NOT AUDITABLE | The file could not be read: say so, do not claim a pass |

What the PDF audit cannot see: text inside raster images, text converted to outlines, the content
of form XObjects from some illustration programs, and anything about meaning. A figure assembled
in Illustrator should be re-audited after its final export.

## 3. Eyes on the figure at printed size

Open the preview at 100% of print size (174 mm wide is about 6.85 inches) and go panel by panel.

**Reading**

- [ ] The claim is visible in five seconds without the legend.
- [ ] The hero panel is the most salient element.
- [ ] Panel letters are in citation order and all at the same offset.
- [ ] Every axis has a title with units; no bare variable names from code (`log2FC`, `nCount_RNA`).
- [ ] Gene symbols italic; no undefined abbreviations.

**Evidence**

- [ ] Individual points shown with every mean or box.
- [ ] The replicate unit is the biological one (patient, animal, section), not cells or pixels.
- [ ] Error bars mean the same thing in comparable panels.
- [ ] Asterisks match the legend; exact tests named in the legend.
- [ ] Axes that are compared share a scale; truncated axes are marked.
- [ ] Colour scales are labelled with what and in which units; diverging maps centred at zero.

**Images**

- [ ] Scale bar on every microscopy or tissue image, defined in the image or the legend.
- [ ] All images of a comparison at the same magnification, exposure and display range.
- [ ] Tissue maps of different modalities in the same orientation.
- [ ] No adjustment applied to part of an image; no AI processing.
- [ ] Each representative image has its quantification in the figure.

**Colour**

- [ ] Each entity has the same colour as in every other figure.
- [ ] No red with green; grays distinguishable in print.
- [ ] Still readable in grayscale for the key contrast.

**Consistency with the text**

- [ ] Figure title = Results subheading wording.
- [ ] Every panel is cited in the text, in order.
- [ ] Numbers in the figure equal the numbers in the text and legend.
- [ ] The legend ends with "See also Figure S…" where a supplemental figure belongs to it.

## What to report with the figure

```text
Files:        Figure N.pdf, Figure N.tiff (size W × H mm)
Gates:        alignment PASS · overlap PASS · style PASS/REVIEW (what)
File audit:   PASS / REVIEW (which warnings stand, and why)
Not checked:  (e.g. Arial substituted on this machine; text inside image panel C)
Legend facts: n, tests, error bars, scale bars
Exclusions:   none / rule + before and after counts
```

Never write "Cell-ready" when a gate did not run, a FAIL stands, or Arial was substituted.
