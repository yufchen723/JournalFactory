# JournalFactory

Take a biology project from data to a submitted paper with Claude. Tell it what you have; JournalFactory learns the field from its papers, picks the journal from the evidence, plans the story and every figure, then helps you draw the figures and write the text to that journal's own rules, with a script that checks each rule and says where the rule comes from.

![JournalFactory overview](docs/overview.png)

**Top:** the nine stages. Claude says which stage a request belongs to and opens only that guide. **Left:** a full-width Cell figure built from the bundled templates (simulated data). **Right:** what the checks print (example output): figure files, manuscript text and journal fit.

Claude knows it as the `journal-factory` skill; the command line is `jf`. [中文说明](README.zh-CN.md)

## What you get

- **A field map before you write.** JournalFactory searches PubMed and Europe PMC with your queries, reads the papers into paper cards, checks every reference, and writes one page: what is known, what is argued about, which of your claims are open, extended or already taken.
- **A journal chosen by evidence, not by wish.** Thirteen journal profiles (Cell, Nature, Nature Genetics, Nature Cancer, Cancer Cell, Nature Communications and others). Your results are scored on eight dimensions and compared with each journal's bar, under three scenarios:

  | Scenario | Question it answers |
  | --- | --- |
  | As it is | Where does the paper fit today? |
  | Plus analysis | Where after work that needs no new data? |
  | Plus new data | Where after the experiment you are considering? |

- **A plan for every figure, with the gaps showing.** Each panel carries one of four marks, so a claim that still needs an experiment is never written as a result:

  | Mark | Meaning |
  | --- | --- |
  | have | data and panel exist |
  | draw | data exist, panel to be drawn |
  | needs analysis | no new data needed |
  | needs new data | experiment or cohort still to come |

- **cell-skills: a full skill pack for the journal Cell.** Built the way [nature-skills](https://github.com/Yuan1z0825/nature-skills) is built (router → manifest → small core → references on demand → check scripts), with Cell's own rules read on cell.com:

  | Skill | What it does | Check |
  | --- | --- | --- |
  | `cell-figure` | Python and R styles at 85 / 114 / 174 mm, Arial 6–8 pt, capital panel letters; eight panel templates; alignment and text-overlap gates; audit of the exported PDF or TIFF; graphical abstract mode | `jf cell figure`, `jf cell demo` |
  | `cell-writing` | Title, Summary, Highlights, eTOC blurb, Introduction, Results, Discussion with Limitations, STAR Methods, legends, cover letter | `jf cell text` |
  | `cell-statistics` | Replicate unit, tests, what a legend must state, pseudoreplication in single-cell and spatial data | `jf cell legends` |
  | `cell-reviewer` | Read your own paper the way a Cell referee and editor would | — |
  | `cell-response` | Revision plan, point-by-point response, revision cover letter, package consistency | `jf cell response` |
  | `cell-data` | Resource availability, key resources table, deposition, supplemental files | — |
  | `cell-citation` | Cell reference style and verification | `jf cell refs` |

- **A built-in studio.** One editable page per manuscript part: main text, front matter, each figure, the graphical abstract. Drag panels in millimetres, edit text in place, select anything and ask Claude, accept or reject Claude's suggestions. A Journal tab checks the page against the target journal while you work.
- **Schematics without image generators.** Local [BioCartoon](https://github.com/josephrich98/biocartoon) icon search and a hand-written SVG guide for workflow drawings and graphical abstracts.
- **Bundled reference skills** for Nature-family journals, Cancer Cell, figure craft, statistics and peer review, each pinned to a commit with its licence.

## The nine stages

| # | Stage | The question | You end with |
| --- | --- | --- | --- |
| 0 | Inventory | What do we have, and how solid is each result? | evidence table |
| 1 | Field | What does the field know, argue about and expect? | field map (Markdown + browsable page) |
| 2 | Journal | Which journal fits now, and which after what extra work? | fit table per scenario |
| 3 | Story | One sentence, then claims, then figures | plan with every gap marked |
| 4 | Figures | Build each figure to the journal's size, type and colour rules | figure files, checks clean |
| 5 | Text | Title to methods, in the journal's order and limits | manuscript within limits |
| 6 | Statistics | Replicate unit, tests, what reviewers will ask | statistics table, checklist |
| 7 | Submission | Cover letter, front matter, deposits, final files | submission folder |
| 8 | Revision | Reviewer reports to a plan and a reply | response package |

## A Cell figure in ten lines

```python
import sys; sys.path.insert(0, "cell-skills/cell-figure/scripts")
import cell_style as cs, cell_templates as ct

cs.use_cell_style()                                      # Arial, 7/6 pt, 0.5 pt axes, RGB
fig, axd = cs.cell_mosaic([["A", "A", "B"],
                           ["C", "D", "B"]], width="full", height_mm=120)   # 174 mm
ct.spatial_map(axd["A"], x, y, categories=region, pixel_um=10, bar_um=1000)   # scale bar included
ct.bar_points(axd["B"], {"Ctrl": ctrl, "Treated": treated}, ylabel="Signal (a.u.)")
cs.label_panels(axd)                                     # A, B, C …
cs.save_cell(fig, "out/Figure 1")                        # gates → PDF + TIFF → audit
```

`save_cell` refuses to export when panels are misaligned or text collides, writes the files at the exact size, and audits them: width, fonts and embedding, text size, stroke width, colour space, red with green, gray fills, image resolution, file size. R users get the same with `theme_cell()` and `save_cell_r()`.

Try it without any data:

```bash
bin/jf cell demo out/          # six-panel figure from simulated data, with the audit
```

## Install

**Claude Code:**

```bash
git clone https://github.com/yufchen723/JournalFactory ~/.claude/skills/journal-factory
~/.claude/skills/journal-factory/bin/jf doctor
```

Then ask Claude "which journal fits this project?", "plan the figures", "check Figure 2 against Cell", or "write the Summary".

**Needs:** Python ≥ 3.9. The figure code needs matplotlib, numpy and Pillow (R: ggplot2 and patchwork). Everything else is standard library.

**Optional:**

```bash
# BioCartoon icons, kept in a private environment inside the skill
python3 -m venv tools/biocartoon_env && tools/biocartoon_env/bin/pip install biocartoon==0.4.10
```

PDF and PNG export from the studio uses Playwright with Chromium, installed on first use.

## Commands

```
jf doctor                                   what is installed, what is missing
jf journals | journal <id> | compare <ids>  journal profiles and limits
jf fit projects/<p>/paper.json              evidence against each journal's bar, per scenario
jf field init|scan|merge|verify|html <slug> learn a field from its papers
jf paper init <dir> --journal cell --title "…"   manuscript workspace in the studio
jf studio --studio <dir>/.studio start      open the studio
jf count <text.md> --journal <id>           words per section against the limits
jf cell figure|demo|text|legends|response|refs   Cell checks
jf cartoon search|get|fetch …               BioCartoon icons (local catalogue)
```

## How sure are the journal numbers?

Every profile in `journals/` records how its limits were checked:

| Level | Meaning |
| --- | --- |
| `official` | read on the journal's own author pages, with the date |
| `secondary` | from other sources that agree |
| `memory` | not yet checked: confirm before formatting |

Cell is `official`: its author pages were read on 2026-11-18 and summarised, with the source of each rule, in [`cell-skills/cell-shared/journal-formats/cell.md`](cell-skills/cell-shared/journal-formats/cell.md). Three documents were not read and are marked as such: the STAR Methods author guide PDF, the journal-policies page and the final file requirements PDF. Journals change their rules; read their pages again before final files.

## Privacy and data

- **Your project stays on your computer.** Nothing about your data, patients or unpublished results is sent anywhere by the scripts. This repository ships with `projects/` and `fields/` empty.
- **Literature search** contacts PubMed, Europe PMC, iCite and bioRxiv with the search terms you wrote in `queries.tsv`, and nothing else.
- **The studio** listens on 127.0.0.1 only, behind a token.
- **Research images are never altered by generative tools.** Schematics only, and BioCartoon runs from its local catalogue; its upload commands are switched off.
- **Bundled skills are reference text.** Their installers, update hooks and scripts that call paid or outside services are not run.
- No data is sent to the author of this skill.

## Files

| Path | What it is |
| --- | --- |
| `SKILL.md` | what Claude reads first: stages, rules, commands |
| `references/` | one guide per stage, the studio guide, the skills catalogue |
| `journals/` | journal profiles: limits, figure rules, evidence bar, how verified |
| `cell-skills/` | the Cell skill pack ([README](cell-skills/README.md)) |
| `scripts/`, `bin/` | `jf`, PubMed and Europe PMC helpers |
| `studio/` | the built-in editor for text and figures |
| `templates/` | field queries, paper card, field-map page |
| `vendor/` | pinned outside skills with their licences |
| `fields/`, `projects/` | your field maps and paper files (empty here) |

## Credits

- **[nature-skills](https://github.com/Yuan1z0825/nature-skills)** (Apache-2.0): bundled in `vendor/`, and the architecture that `cell-skills` follows. See [`cell-skills/NOTICE.md`](cell-skills/NOTICE.md).
- **[Awesome-Journal-Skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills)** (MIT): Cell-Skills and Cancer-Cell-Skills checklists.
- **[claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)** by K-Dense (MIT): scientific visualization, venue templates, scientific writing, peer review.
- **[BioCartoon](https://github.com/josephrich98/biocartoon)** (BSD-2-Clause; icons carry their own licences): icon guides.
- **[schematic-figure](https://github.com/lgwrightlab/schematic-figure)** (MIT): SVG schematic guide.
- **[PaperLens](https://github.com/yufchen723/PaperLens)** (MIT): reading one paper in depth.
- The palette is the Okabe–Ito colour-blind-safe set. Journal rules are summarised from the journals' own author pages, which remain the authority.

Sources, commits and what was left out of each bundle: [`references/10_skills_catalogue.md`](references/10_skills_catalogue.md).

## License

MIT for JournalFactory's own text and code, see [LICENSE](LICENSE). Everything under `vendor/` keeps its own licence.
