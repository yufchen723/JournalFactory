# Skills catalogue (reviewed 2026-11-18)

All bundled copies are pinned snapshots, read as reference text. No installer, update hook or network script from them is run.

| Bundle | Source @ commit | Licence | Bundled | Left out, and why |
|---|---|---|---|---|
| `cell-skills/` | Journal Factory's own (v1.0.0, 2026-11-18); architecture and reasoning adapted from nature-skills @ 14ca6971; rules read on cell.com 2026-11-18 | own text and code; adapted parts Apache-2.0 (see `cell-skills/NOTICE.md`) | cell-figure (Python + R style, templates, gates, file audit, graphical abstract), cell-writing, cell-statistics, cell-reviewer, cell-response, cell-data, cell-citation, cell-shared | nature-figure's AI image-generation route (Cell does not allow it; nothing leaves the machine); no vendored script is copied or run |
| `vendor/nature-skills` | github.com/Yuan1z0825/nature-skills @ 14ca6971 | Apache-2.0 | nature-shared, -figure, -statistics, -writing, -response, -reviewer, -polishing, -data, -citation, -ref-verifier, -paper-card, -paper-xray | `install.sh` and the SessionStart auto-update hook (runs remote code each session); `nature-figure/assets/figures4papers` (size); the OpenRouter schematic generator and its guide (paid external image service); nature-downloader (bulk downloads); nature-academic-search MCP (institutional keys); nature-literature-pipeline (posts digests to chat services) |
| `vendor/cell-skills` | github.com/brycewang-stanford/Awesome-Journal-Skills @ 932eb233, `Cell-Skills/` | MIT | 12 checklists: fit, framing, summary, highlights, writing, figures, STAR Methods, data, citation, submission, rebuttal, workflow | nothing |
| `vendor/cancer-cell-skills` | same repo, `Cancer-Cell-Skills/` | MIT | 12 checklists | nothing |
| `vendor/k-dense` | github.com/K-Dense-AI/claude-scientific-skills @ ec59a29a | MIT | scientific-visualization, venue-templates (Cell Press style reviewed 2026-10-01), scientific-writing, peer-review, citation-management, paper-lookup | literature-review and research-lookup scripts (paid search CLI, OpenRouter); image-generation skills |
| `vendor/biocartoon` | github.com/josephrich98/biocartoon @ 9a7dd4c7 (v0.4.10) | BSD-2 (icons carry their own licences) | find-icons, make-figure guides | upload and create-icon skills (publish content); the tool itself is installed in `tools/biocartoon_env` (PyPI 0.4.10) behind `bin/jf-cartoon`, local catalogue only; hosted server not used |
| `vendor/schematic-figure` | github.com/lgwrightlab/schematic-figure @ 09d8b6e | see its LICENSE | hand-written SVG schematic guide | nothing |
| `studio/` | the lab's own Folio Studio 0.5.1 (`~/.claude/skills/folio-studio`) | MIT / own | full editor + server + CLI, with journal.py, journal.js and the Journal tab added | nothing; the installed Folio skill is not modified |
| `vendor/paperlens` | github.com/yufchen723/PaperLens (the lab's own) | MIT | SKILL.md | nothing |

Looked at and not bundled:

| Item | Reason |
|---|---|
| Imbad0202/academic-research-skills | CC BY-NC: ideas only |
| luwill/research-skills `lit-search` @ 5e5add48 (MIT) | design borrowed in `01_field_learning.md`; text is Chinese with a computer-science venue ranking |
| cookjohn/gs-skills | scrapes Google Scholar; stops at CAPTCHAs |
| openags/paper-search-mcp | has a Sci-Hub fallback |
| PaperQA2, STORM, gpt-researcher, LitLLM | each needs its own model key; not needed inside Claude Code |
| litstudy, citationchaser, paperfetcher | dormant |
| cyanheads/pubmed-mcp-server @ 84550677 (Apache-2.0) | optional; `scripts/pubmed.py` covers the need without an install |
| Haojae/scipilot-figure-skill, dvdsosa/scientific-writing-skills, lishix520/academic-paper-skills, anthropics/skills | overlap with the bundles above |

Caveat: the Cell and Cancer Cell checklists are third-party summaries of the journals' rules, not the rules. `journals/*.json` says how each number was verified.
