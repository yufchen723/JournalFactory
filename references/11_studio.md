# The built-in studio (writing + figure editor)

Journal Factory carries its own copy of the lab's Folio Studio editor (taken from Folio 0.5.1, MIT, same author) with a **Journal** tab added. It is independent of the installed Folio skill: nothing in `~/.claude/skills/folio-studio` is used or changed. Command: `$JF/bin/jf-studio` (or `jf studio …`); it takes the same commands as `folio`. Always pass `--studio <paper dir>/.studio`.

## Journal features (what this copy adds)

- `jf paper init <dir> --journal <id> --title "…" [--figures 7] [--supp 7]` → main text in the journal's section order, front matter (highlights, in brief, cover letter), one canvas page per figure at the journal's widest column, graphical abstract for Cell Press.
- `jf studio --studio <dir>/.studio journal ls | show <id> | set <page> <id> [--width single|mid|double]` · `check <page> [--json]`.
- **Journal tab in the page**: journal picker · page-width buttons (panels are not moved) · **Check** (lists problems; click one to select its block; ✳ sends them to Claude as an Edit) · live word count · journal-specific Ask/Edit presets · jump between manuscript parts.
- **Check covers**: figures — page width and height, text size range, panel-letter case and size, font, panels outside the page, raster resolution at placed size, thin lines; text — Summary/Abstract, In brief, Highlights (count and characters), Methods and reference limits, main-text words, missing sections. It cannot read text inside raster panels: say so.
- Every check prints how the journal's numbers were verified (`official` / `secondary` / `memory`). Never say a page "meets the journal's rules" without that qualifier.
- Profiles are read from `<paper dir>/.studio/journals` (per-paper overrides) then `$JF/journals`.

Everything below is the editor's own guide (how the page works, the CLI, delivering and answering Ask/Edit requests, hand-off message, file layout, safety). Read "folio" as "page" and `folio` as `jf-studio`.

---

# Folio Studio

One document model, three layouts. A **folio** is a page made of **blocks** — text blocks (Markdown) and image blocks (PNG/JPG/SVG/PDF panels). A multi-panel figure, an A0 poster and a paper's main text are all folios; they differ only in layout:

- `mode: canvas` — fixed page in mm, blocks placed absolutely (figures, posters, slides);
- `mode: flow` — blocks stacked in order on a page with margins (main text, methods, legends).

The in-page Claude **is this session**: it answers Ask/Edit requests in the terminal with its full context, literature tools and file access, and can change the folio itself. The page is also fully editable by the user: drag/resize panels, edit any text (legends, labels, paragraphs), add or remove blocks, undo, versions.

Skill version: 0.5.1 (CHANGELOG at the end).

## 0. Start of every task

1. **Where it lives**: `$JF/studio/` (inside Journal Factory). CLI: `$JF/bin/jf-studio` (written `folio` below).
2. **One studio per project and per Claude session**: `<paper dir>/.studio/` holds `folios.json` (registry), `studio.json` (token, port, owner `session_id`), `server_url.txt`, `server.log`. Set `export FOLIO_STUDIO=<paper dir>/.studio` or run from the project root.
3. **Dependencies**: Python ≥ 3.9 stdlib only for the server. Server-side screenshots and PDF / PNG export use Playwright + Chromium: **`folio start` installs them automatically the first time** (background `pip install playwright` + `python -m playwright install chromium`, one-time ~150 MB into the user's Playwright cache; status `~/.cache/folio-studio/playwright_setup.json`, log `playwright_setup.log` beside it). Until it finishes the page falls back to a browser-rendered screenshot and the print dialog. `folio setup` runs the install in the foreground (retry after a failure; a failure is not retried automatically for 24 h); `FOLIO_NO_AUTO_INSTALL=1` turns the automatic install off. On Linux a missing system library needs `python3 -m playwright install-deps chromium` (sudo) — tell the user rather than running it. Translate uses the local `claude` CLI (fast model, no tools).
4. **Voice**: answers follow the lab's §0.3 rules from the omics-report-compiler skill — answer first, bullets, numbers in bold, 1–3 verified citations, ≤ ~150 words.

## 1. Lifecycle

```
Input (panels / md / docx / pptx / existing folio)
  → folio init           build folio.json + assets/
  → folio start          studio server, link in the terminal
  → the user edits in the page; Claude edits via CLI; both see changes live
  → Ask / Edit / Screenshot → inbox → this session answers (threads + notes)
  → Claude proposes → user accepts (suggestions)
  → folio export         PDF / PNG at exact page size
```

### 1.1 Build (`folio init`)

```
folio init <dir> --title "Figure 3" --mode canvas --size 180x120 --cols 2 --from a.png b.png …
folio init <dir> --title "Main text" --mode flow   --size 210x297 --md main.md [--from fig1.png]
folio init <dir> --title "Poster"    --mode canvas --size 841x1189 --from … --md abstract.md
```

- **Figure from panels**: panels go to `assets/`, each gets `label_x` (bold letter) + `panel_x` blocks laid out on a grid, plus a `legend` block at the bottom. Then refine positions with `folio set`.
- **Paper from Markdown**: one text block per paragraph/heading (`t001…`); images become `panel_x` + `cap_x`.
- **docx / pptx input**: convert first (`pandoc -t gfm` for docx; the pptx skill's extractor for slides; `pdftoppm`/`pdfimages` for a PDF figure), then `folio init`. Say what was not carried over (tracked changes, fonts, grouped shapes).
- **Panels should be vector where possible** (SVG/PDF): text inside a PNG panel cannot be edited in the page — only re-plotted (Edit → "Redo figure", which this session does by editing the plotting script and re-running).
- After `init`, run `folio show <id>` and `folio shot <id>` and **look at the PNG with the Read tool** before telling the user it is ready.

### 1.2 Open (`folio start`)

- `folio start` (or `bash studio/start_studio.sh`) starts the server detached, binds 127.0.0.1 with a token, keeps port and token across restarts. It prints `http://127.0.0.1:<port>/?t=<token>`; add `&folio=<id>` to open a specific folio.
- Record this session's id in `studio.json` (`CLAUDE_SESSION_ID` or `--session`). Never answer requests of a studio owned by another session.
- Open the link with the first option that works: Claude desktop preview panel → VS Code Simple Browser → system browser → `ssh -N -L <port>:127.0.0.1:<port> user@host` for a remote machine.
- Then set up the three delivery layers (§3) and send the hand-off message (§5).

### 1.3 In the page (what the user can do)

- **Select a block**: click. **Move**: drag — text blocks move exactly like images, selected or not. **Resize**: handles — corners scale a picture proportionally (Shift forces that on any handle); the top / bottom / left / right handles stretch it freely, non-proportionally (the image switches to `fit: fill` so it fills the new box instead of letterboxing; also for pictures inside a group resized from an edge). **Nudge**: arrow keys move the selected block(s) (0.5 mm; Shift 5 mm; Alt 0.1 mm), also while focus is still on a ribbon button or the zoom slider (only typing fields — text inputs, the Ask box, a text box being edited — keep the arrows). **Z-order**: `[` `]`. **Delete**: Delete key. Snap to 1 mm grid (toggle), grid overlay, zoom (⌘-wheel, − / + buttons stepping 25 · 33 · 50 · 67 · 75 · 90 · 100 · 110 · 125 · 150 · 175 · 200 · 250 · 300 · 400 %, the `-` / `+` keys, slider in 5 % steps, `0` = fit). Zooming keeps the centre of the view in place.
- **Page placement**: the page sits in the centre of the canvas (scrolls when larger than the window). Every folio that is opened — including a newly generated poster or figure — starts fitted to the window and centred, never in the top-left corner.
- **Select several** (canvas): Shift/⌘/Ctrl-click adds or removes a block; press on any empty spot — blank page, a locked background block, or the grey area around the page — and drag a rectangle (PowerPoint rubber band) to select every text box, picture and shape mostly inside it (≥ 60 % of its area, so a text frame a little larger than its text still counts); locked backgrounds (a section's box, bars) come along only when wholly enclosed; groups only when all members qualify; Shift/⌘ while starting adds to the selection; ⌘/Ctrl-A = all unlocked blocks. Dragging any member moves the whole group (snap applies to the dragged block, the rest keep their offsets); arrows, `[` `]`, Delete and Lock act on the group; a plain click on a member reduces to that block. ✳ on a group sends an Ask/Edit with anchor `type: group`, `blocks: [...]` and the union bbox.
- **Group** (Ctrl/⌘G; ungroup Ctrl/⌘⇧G; Home ▸ Group · picture, Arrange ▸ Group): grouped blocks share `group`; a click selects the whole group, a second click selects one member (to type in it or move it alone); the group box's handles scale every member's position and size (corners keep the proportions; text sizes stay). Rubber band takes a group only when all of it is inside; copy/paste makes a new group.
- **Crop a picture** (double-click it, or Crop in Home / Shape Format): the frame shows the kept part, the cut-away part is faded; black handles trim, dragging inside moves the picture under the frame; Enter / Esc / click outside finishes; Reset crop shows the whole picture again. Stored as `crop: {l, t, r, b}` (fractions cut from each side); the block box is the visible part.
- **Undo / versions**: ↶ ↷ reach back the last **20** operations (per page session). A version is archived **once per 5 changes** (page edits, Claude's edits and accepted suggestions all count; one autosave can carry several), plus the initial state and the state before a restore; the Versions menu (Review tab) restores any of them.
- **Lock** (`L`): toggles `locked` on the selection. Locked blocks (backgrounds, boxes, bars) can't be grabbed — pressing on them starts a rubber band — but move when part of a group.
- **Ribbon** (PowerPoint-style top bar; quick-access ↶ ↷ always visible):
  - *Home*: Clipboard (paste / cut / copy / duplicate blocks), Insert (Text Box, Picture, Shapes ▾), Font (font, size in pt, A⁺ A⁻, B I U S, x² x₂, font colour, highlight, clear), Paragraph (bullets, numbering, list level ⇤ ⇥, align L/C/R/justify, line spacing, vertical align top/middle/bottom), Drawing (fill, outline), Arrange (front, back, delete, lock), Group · picture, **Guides** (snap, grid) and **Zoom** (− slider + , %, Fit, 100 %). There is no separate View tab.
  - *Insert*: text box, picture, shape gallery (rectangle, rounded rectangle, oval, triangle, block arrow, chevron, line, arrow, double arrow).
  - *Shape Format*: fill / no fill, outline / no outline, weight (pt), dash, corner radius, X Y W H (mm), rotation.
  - *Arrange*: order (front / forward / backward / back), align and distribute (to the selection; one block → the page), rotate 90°, lock, delete. *Review*: Ask Claude, screenshot, versions, export.
  - Font commands act on the highlighted text while a box is being edited, otherwise on every selected text box (size, font, colour and alignment then become block properties).
- **Edit text** (rich, like PowerPoint): double-click a text box (or Enter) and type; Ctrl/⌘ B/I/U, Tab / Shift-Tab change list level, Ctrl/⌘⇧> / < grow / shrink; Esc or click away saves. **Alt-drag** inside a text box selects words for Ask/Translate (in flow mode a plain drag does).
- **Clipboard**: Ctrl/⌘ C / X / V / D copy, cut, paste, duplicate blocks (pasted blocks are offset and unlocked).
- **Add**: `+ Text`, `+ Image` (or paste / drop an image onto the page).
- **Ask / Edit (✳)**: select text, or click a block → ✳ → Ask or Edit tab, presets, free text, **images by paste / drag / 📎** (≤ 8, downscaled to 2000 px). Sent to the inbox; the answer appears in **Threads** and becomes a **note** (💬 chip on the block).
- **📷 Screenshot** (`S`): drag a rectangle on the page (or `A` = whole page). The server renders that region with Chromium at 3× (exactly what export will produce), saves it to `folio_review/screenshots/`, records which blocks it covers, and opens the Ask box with the image attached. Claude receives the PNG path and the block ids.
- **文 Translate**: select text → instant translation (local Claude CLI, nothing saved).
- **Suggestions (✎ chip, dashed outline)**: a change Claude proposed; shows old → new; Accept applies it, Reject discards it.
- **Versions**: one archived `folio.json` per 5 changes (see Undo / versions); the Versions menu restores any state (the current one is archived first).
- **Export**: PDF at the exact page size (Playwright) or the browser print dialog.
- Autosave 0.7 s after each change. If Claude changes the file while the user is mid-edit, the page reloads once the edit is saved.

## 2. Claude's side (CLI)

Always go through the CLI (or the API) rather than editing `folio.json` by hand while the server runs, so every change is archived, broadcast to the page and attributed.

```
folio ls                                  folios in this studio, link
folio show <id> [block]                   blocks with geometry and text
folio set <id> <block> x=10 y=4.5 w=60    geometry / style / text=… (applies at once)
folio text <id> <block> --file new.md     replace a block's text
folio add <id> text  id=note1 x=.. y=.. w=.. h=.. text="…" pt=8
folio add <id> image src=/path/panel.png x=.. y=.. w=..     (h from the image aspect)
folio rm <id> <block>
folio suggest <id> <block> w=60 h=25 --why "match panel a"   the user accepts in the page
folio suggest <id> <block> --file new_legend.md --why "…"
folio suggest <id> --add type=text text="…" x=.. y=.. w=.. h=.. --why "…"
folio suggest <id> --delete <block> --why "…"
folio shot <id> [--block panel_b | --region x,y,w,h] [--scale 3]   → PNG path; open it with Read
folio export <id> --pdf | --png
folio pending [show|hook|seen <rid>|working <rid>]
folio answer <id> <rid> --file answer.md [--changed panel_b,legend]
```

**Rich text.** A text block edited in the page carries `html` (sanitised: b/i/u/s/sup/sub, span styles for size, font, colour, highlight, lists, alignment) and `text`, its Markdown mirror (bold, italic, sup/sub, `- ` and `1. ` lists). Read `text`; inline sizes and colours exist only in `html`. `folio text` / `set text=…` / an accepted text suggestion replace the block's text and drop its `html` — say so when you overwrite a block the user formatted by hand. Block-level text style: `pt, font, color, align, lh` (line height), `valign` (top|middle|bottom), `bg`, `border`, `bw` (pt), `dash`, `radius` (mm).

**Shapes.** `folio add <id> shape shape=roundrect x=.. y=.. w=.. h=.. fill=#4472C4 stroke=#2F528F sw=1` — `shape` ∈ rect, roundrect, ellipse, triangle, rarrow, chevron, line, arrow, darrow; `fill` / `stroke` colour or `none`, `sw` pt, `dash` dash|dot, `radius` mm, `rotate` deg. Lines and arrows run left → right through the middle of their box; rotate for other angles.

**Direct change vs suggestion.** Apply directly (`set`, `text`, `add`, `rm`) when the user asked for exactly that in an Edit request or in the terminal. Use `suggest` when Claude is proposing (layout fixes it noticed, wording changes to the user's own text, anything in a paper's prose). Never silently rewrite the user's prose.

**Screenshot loop — mandatory for layout work.** Claude cannot see the page. After any geometry change, run `folio shot <id> --block <b>` (or a region) and **look at the PNG with Read** before reporting; fix overlaps, clipped text and misalignment you see. For a whole-page check use `folio shot <id>`.

**Precision.** Geometry is in mm; text size in pt. Journal defaults: single column 88 mm, double 180 mm, max height ~ 240 mm; labels 8–10 pt bold; legend/axis text 6–8 pt; A0 poster 841 × 1189 mm with 40–60 mm margins, body ≥ 24 pt, title ≥ 72 pt.

## 3. Delivering Ask/Edit requests to this session

Set up all three whenever the server runs; they back each other up.

1. **Watcher (primary)**: `bash $JF/studio/wait_event.sh <paper dir>/.studio` with Bash `run_in_background` and no timeout. It polls every 20 s and exits only on a real event (pending request, `FOLIO_REQUEST` / `FOLIO_SUGGESTION` / `FOLIO_NOTE` / `Traceback` line, server stopped). After handling an event, start a new waiter silently in the same turn; write nothing in the chat for an idle restart.
2. **Hook (backup)**: `UserPromptSubmit` → `python3 $JF/studio/folio_hook.py` in `<project>/.claude/settings.json`. It prints pending requests of this session's studio with every user message. Create it when the studio is first set up and tell the user it exists.
3. **Turn-end check**: before finishing any reply while the server runs, `folio pending hook`; answer anything listed in the same turn.

## 4. Answering

**Ask** (`folio pending` → read → answer):
1. `folio pending seen <rid>`; read the block (`folio show <id> <block>`), its neighbours if layout matters, and **every attached image with Read** (screenshots, pasted figures). Read `follows` threads first (`folio_review/threads/<rid>.json`).
2. For scientific questions search the literature (mechanism + comparative evidence), as in the omics-report-compiler §A6. For layout questions take a `folio shot` of the region.
3. Answer with the §0.3 template (Answer / Evidence / Caveat / Next; ≤ ~150 words), in the project's explanation language, terms in English. `folio answer <id> <rid> --file a.md`. One line in the terminal.

**Edit**:
1. Classify: text, geometry, restyle, re-plot (needs the plotting script), structural, new content.
2. Text and geometry under ~5 min: apply directly, `folio shot` the result, look at it, then `folio answer … --changed <blocks>` describing what changed (before → after values).
3. Re-plots, anything that changes numbers, or anything the user set `ask before re-running`: post a plan as the answer (status stays `working`), wait for the user's OK in a follow-up request or in the terminal.
4. Changes to the user's prose: `folio suggest` rather than `set`, and say so in the answer.
5. Every answered Edit becomes an Edit note on the block.

**Screenshot requests** (anchor type `screenshot`): the request carries `region` and `blocks`; open the image, judge alignment/overlap/size relative to the page, act as an Edit.

## 5. Terminal hand-off message (after init / start / rebuild)

```
<One sentence: what was built (folio id, mode, page size, number of blocks).>

**Open:** <http://127.0.0.1:<port>/?t=<token>&folio=<id>>
- Another machine: `ssh -N -L <port>:127.0.0.1:<port> <user>@<host>`, then the same link.
- Checked: folio shot <id> looked at; export tested (or: Playwright missing → browser print only).

**In the page**
- Top ribbon works like PowerPoint: Home (font, size, bold, bullets / numbering, alignment, insert text box / picture / shapes), Insert, Shape Format, Arrange, Review (snap, grid and zoom − / + are on Home); ↶ ↷ always at the top. Arrow keys move the selected object; the page opens fitted and centred.
- Drag any block (text, image or shape) to move it; handles resize; double-click a text box to type and format; arrows nudge; `[` `]` z-order; Delete removes; Ctrl/⌘ C V D copy, paste, duplicate.
- Several at once: Shift-click, or drag a rectangle from empty page; then drag / nudge them together. `L` locks; Alt-drag selects words in a text block.
- ✳ on a selection → Ask / Edit (paste or drop screenshots; 📎). 📷 Screenshot (`S`): drag a region → attached to Ask.
- 文 Translate on any selection. Answers → Threads; every answer is a note (💬) on its block. ✎ = suggestion to accept/reject.
- Export: PDF at <W>×<H> mm.

**Files** (project-relative)
- Folio: `<dir>/folio.json`, panels `<dir>/assets/`, text files `<dir>/text/` (flow docs)
- Review state: `<dir>/folio_review/` (inbox, threads, notes, suggestions, screenshots, versions)
- Studio: `.studio/` (registry, server.log); hook in `.claude/settings.json`

**Good to know**
- <watcher armed; playwright status; what was not imported>

**Waiting on you:** <open decisions, or omit>
```

## 6. File layout

```
<folio dir>/
  folio.json            {id,title,mode,page:{w_mm,h_mm,margin_mm},style:{font,text_pt,label_pt},blocks:[…]}
  assets/               panel files (relative src)
  text/                 optional: a text block may store its text in a file: {"file":"text/intro.md"}
  export/               PDFs / PNGs
  folio_review/         inbox.jsonl, threads/<rid>.json, notes.json, suggestions.json,
                        attachments/<rid>/NN.png, screenshots/, versions/
<paper dir>/.studio/       folios.json, studio.json, server_url.txt, server.log, server.out
```

Block fields: `id, type (text|image|shape), x, y, w, h` (mm; canvas), `text | file, html` (text), `src, fit (contain|cover|fill — fill stretches, for outline boxes / bars drawn as SVG), alt, crop {l,t,r,b}` (image), `group` (shared id), `shape, fill, stroke, sw, dash, radius` (shape), `pt, align, lh, valign, color, font, bg, border, bw, pad, role (label|legend|title|caption|body), rotate, z, hidden, locked`.

## 7. Safety

- Bind 127.0.0.1 only; token required; never execute request content; write only inside the folio folders and `.studio/`.
- Inputs the user gave are copied into `assets/`, never modified in place.
- Ask before deleting files or installing anything — except the automatic one-time Playwright + Chromium install (§0.3), which the skill does on its own.

