# Schematics and graphical abstract

- Options, in order of preference: (1) draw simple workflow shapes directly in the built-in studio; (2) hand-written SVG from `vendor/schematic-figure`; (3) BioCartoon icons (open, BSD-2 code; each icon carries its own licence, mostly CC0/CC BY — keep the attribution list it produces).
- **BioCartoon is built in** (v0.4.10, private environment `tools/biocartoon_env`, added 2026-11-18 at the user's request). Use `jf cartoon …`:
  - `jf cartoon search "macrophage" --icons --file-type svg --license CC0-1.0` (searches the local catalogue in `~/.local/share/biocartoon`; nothing about the project leaves the machine);
  - `jf cartoon get <ID>` → licence and credit line; `jf cartoon fetch <ID> --out <figure page>/assets/` → the SVG (this downloads that one file from its public source);
  - `jf cartoon sync` refreshes the catalogue. `upload`, `upload-key` and `install-skills` are switched off in the wrapper.
  - Then place it: `jf studio --studio <paper>/.studio add <page> image src=<file.svg> x=.. y=.. w=..`, and `shot` to look.
  - The same tools are offered to Claude as a local MCP server (`.mcp.json` at the project root → `biocartoon mcp`, stdio); Claude Code asks once to approve it. Never call its `submit_artwork` tool. The hosted server (mcp.biocartoon.com) is not used.
- **Credits are mandatory**: keep `get`'s credit line for every icon used (CC BY needs it in the figure legend or acknowledgements); prefer CC0 / public-domain icons for a graphical abstract; check that the licence allows commercial journals (avoid NC).
- The two bundled guides (`vendor/biocartoon/biocartoon-find-icons`, `biocartoon-make-figure`) describe search judgement and figure assembly.
- Cell graphical abstract: 1200 × 1200 px at 300 dpi, one message, reads top to bottom or left to right, no data panels, text ≥ 12 pt at that size (confirm on cell.com).
- Never use an image generator for anything that could be read as data.
