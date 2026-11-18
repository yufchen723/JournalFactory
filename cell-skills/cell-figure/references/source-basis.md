# Source basis

| Layer | Source | Status |
|---|---|---|
| Sizes, fonts, lines, colour, resolution, file types, image integrity | cell.com figure guidelines, read 2026-11-18 | official; summarised in `cell-shared/journal-formats/cell.md` §5 |
| Legends, figure titles | cell.com "Revise your manuscript", read 2026-11-18 | official; cell.md §4 |
| Graphical abstract | Cell Press graphical abstract guidelines (PDF), pages 1–2 read 2026-11-18 | official; examples on pages 3–8 not read |
| Supplemental figures | cell.com supplemental information, read 2026-11-18 | official; cell.md §7 |
| Skill architecture (router, manifest, core contract, backend fragments, gates, QA contract) | nature-skills `nature-figure` @14ca6971 | Apache-2.0; structure and reasoning adapted, text rewritten |
| Multi-panel logic | nature-skills `multipanel-evidence-architecture.md` | adapted; presented as craft guidance |
| Palette | Okabe–Ito colour-blind-safe set, reordered | public; house choice |
| Code in `scripts/` | written for this skill | no code copied from nature-skills; its scripts were read, not run |

Not included from nature-figure, and why:

- The OpenRouter / image-generation route: Cell does not allow general-purpose generative AI for
  graphical abstracts or research images, and Journal Factory sends nothing about the project to
  outside services.
- The PyMuPDF collision audit: replaced by a text-overlap gate on the live matplotlib figure and
  a dependency-free PDF audit.
- Nature-specific material (Extended Data, flagship legend limits, NMI rules).

Re-read the cell.com pages before final files: journals change their rules, and the date above is
the only guarantee this file gives.
