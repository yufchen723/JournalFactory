/* Folio Studio ribbon — PowerPoint-style top bar (Home / Insert / Shape Format / Arrange / View / Review).
   Text commands act on the selection inside the text box being edited, or on whole selected text boxes;
   shape / arrange commands act on every selected block. Uses the internals editor.js exposes as window.FolioAPI. */
(() => {
'use strict';
const F = window.FolioAPI; if (!F) return;
const { S, $, $$, page } = F;
if (new URLSearchParams(location.search).get('print') === '1') return;

// ---------- tabs and layout
function setTopH() { document.documentElement.style.setProperty('--topH', $('#topbar').offsetHeight + 'px'); }
function showTab(t) { $$('#rtabs button').forEach(x => x.classList.toggle('on', x.dataset.rt === t)); $$('.rpanel').forEach(p => p.classList.toggle('on', p.dataset.rt === t)); setTopH(); }
$$('#rtabs button').forEach(b => b.onclick = () => showTab(b.dataset.rt));
window.addEventListener('resize', setTopH); setTopH();
// buttons must not take focus, so the caret / selection in the text box survives a click
$('#topbar').addEventListener('pointerdown', e => { const b = e.target.closest('button'); if (b && $('#ribbon').contains(b)) e.preventDefault(); });

// ---------- shapes gallery
const SHAPES = [['rect', 'Rectangle'], ['roundrect', 'Rounded rectangle'], ['ellipse', 'Oval'], ['triangle', 'Triangle'], ['rarrow', 'Block arrow'], ['chevron', 'Chevron'], ['line', 'Line'], ['arrow', 'Arrow'], ['darrow', 'Double arrow']];
const isLine = k => /^(line|arrow|darrow)$/.test(k);
for (const host of $$('.shapes')) host.innerHTML = SHAPES.map(([k, n]) =>
  `<button data-shape="${k}" title="${n}">${F.shapeSVG({ shape: k, w: 14, h: isLine(k) ? 6 : 10, sw: 1.3, fill: isLine(k) ? undefined : '#DCE6F5', stroke: '#2F528F' })}<span>${n}</span></button>`).join('');
$$('.dd .ddb').forEach(b => b.onclick = e => { e.stopPropagation(); const m = b.nextElementSibling; const open = !m.classList.contains('open'); $$('.ddm.open').forEach(x => x.classList.remove('open')); m.classList.toggle('open', open);
  if (open) { const r = b.getBoundingClientRect(); m.style.left = Math.min(r.left, window.innerWidth - 290) + 'px'; m.style.top = r.bottom + 2 + 'px'; } });
document.addEventListener('pointerdown', e => { if (!e.target.closest('.dd')) $$('.ddm.open').forEach(x => x.classList.remove('open')); });
$$('[data-shape]').forEach(b => b.onclick = () => { $$('.ddm.open').forEach(x => x.classList.remove('open')); insertShape(b.dataset.shape); });

// ---------- helpers
const pg = () => S.doc.page || {};
const unit = () => Math.min(60, Math.max(10, (pg().w_mm || 180) / 22));     // default insert size scales with the page
function viewCentre() {
  const v = $('#viewport').getBoundingClientRect(), r = page.getBoundingClientRect(), k = F.PX_PER_MM * S.zoom;
  const cx = ((Math.max(v.left, r.left) + Math.min(v.right, r.right)) / 2 - r.left) / k, cy = ((Math.max(v.top, r.top) + Math.min(v.bottom, r.bottom)) / 2 - r.top) / k;
  return { x: isFinite(cx) ? cx : 20, y: isFinite(cy) ? cy : 20 };
}
const topZ = () => Math.max(0, ...S.doc.blocks.map(b => b.z || 0)) + 1;
function rerender(ids) { F.render(); F.selectMany(ids.filter(id => F.blockById(id))); refresh(); }
function each(fn, why, opts = {}) {
  if (S.editing && !opts.keepEditing) F.commitEdit();
  const bs = F.selBlocks(); if (!bs.length) { F.toast('Select a block first'); return; }
  F.pushUndo(); bs.forEach(fn); F.markDirty(why + (bs.length > 1 ? ` (${bs.length} blocks)` : ' ' + bs[0].id)); rerender(bs.map(b => b.id));
}
function stripInline(b, prop) {
  if (!b.html) return;
  const d = new DOMParser().parseFromString('<body>' + b.html, 'text/html').body;
  d.querySelectorAll('[style]').forEach(x => x.style.removeProperty(prop));
  b.html = F.cleanHTML(d.innerHTML);
}
function scaleInline(b, k) {
  if (!b.html) return;
  const d = new DOMParser().parseFromString('<body>' + b.html, 'text/html').body;
  d.querySelectorAll('[style]').forEach(x => { const m = /^([\d.]+)pt$/.exec(x.style.fontSize); if (m) x.style.fontSize = Math.round(+m[1] * k * 2) / 2 + 'pt'; });
  b.html = F.cleanHTML(d.innerHTML);
}

// ---------- insert
function insertText() {
  if (S.editing) F.commitEdit();
  const u = unit(), c = viewCentre(), w = u * 3, h = u * 0.9;
  const b = { id: F.uid('t'), type: 'text', text: 'Text', pt: (S.doc.style && S.doc.style.text_pt) || 8, z: topZ() };
  if (S.doc.mode !== 'flow') Object.assign(b, { x: +(c.x - w / 2).toFixed(1), y: +(c.y - h / 2).toFixed(1), w: +w.toFixed(1), h: +h.toFixed(1) });
  F.pushUndo(); S.doc.blocks.push(b); F.render(); F.select(b.id); F.markDirty('add text box'); F.startEdit(b.id, { all: true });
}
function insertShape(kind) {
  if (S.doc.mode === 'flow') return F.toast('Shapes need a canvas folio');
  if (S.editing) F.commitEdit();
  const u = unit(), c = viewCentre(), w = u * 2.5, h = isLine(kind) ? Math.max(3, u * 0.25) : u * 1.6;
  const b = { id: F.uid('shp'), type: 'shape', shape: kind, x: +(c.x - w / 2).toFixed(1), y: +(c.y - h / 2).toFixed(1), w: +w.toFixed(1), h: +h.toFixed(1), z: topZ() };
  if (isLine(kind)) Object.assign(b, { stroke: '#1F2937', sw: Math.max(1.5, +(u / 20).toFixed(1)) });
  else Object.assign(b, { fill: '#4472C4', stroke: '#2F528F', sw: Math.max(1, +(u / 30).toFixed(1)) });
  F.pushUndo(); S.doc.blocks.push(b); F.render(); F.select(b.id); F.markDirty('add ' + kind); F.showSelToolsForBlock($(`.blk[data-id="${b.id}"]`, page)); refresh();
}

// ---------- clipboard (blocks)
function copyBlocks() { const bs = F.selBlocks(); if (!bs.length) return false; S.clip = JSON.stringify(bs); F.toast(`Copied ${bs.length} block(s)`); return true; }
function pasteBlocks(src) {
  const list = JSON.parse(src || S.clip || '[]'); if (!list.length) return;
  if (S.editing) F.commitEdit();
  const off = unit() / 4, z = topZ(), ids = [];
  F.pushUndo();
  const gmap = {};      // pasted groups become new groups
  for (const b of list) { const n = Object.assign({}, b, { id: F.uid(b.type === 'image' ? 'img' : b.type === 'shape' ? 'shp' : 't'), z: z + (b.z || 0) }); delete n.locked; if (n.group) n.group = gmap[n.group] || (gmap[n.group] = F.uid('g')); if (n.x != null) { n.x = +(n.x + off).toFixed(2); n.y = +(n.y + off).toFixed(2); } S.doc.blocks.push(n); ids.push(n.id); }
  F.markDirty(`paste ${ids.length} block(s)`); rerender(ids);
  if (!src) S.clip = JSON.stringify(list.map(b => Object.assign({}, b, b.x != null ? { x: b.x + off, y: b.y + off } : {})));
}
function deleteBlocks() { const bs = F.selBlocks(); if (!bs.length) return; if (S.editing) F.commitEdit(); F.pushUndo(); S.doc.blocks = S.doc.blocks.filter(b => !S.multi.has(b.id)); F.select(null); F.hideSelTools(); F.render(); F.markDirty(`delete ${bs.length} block(s)`); }
const inField = () => { const a = document.activeElement; return /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName) || a.isContentEditable; };
document.addEventListener('keydown', e => {
  const mod = e.metaKey || e.ctrlKey, k = e.key.toLowerCase();
  if (mod && e.shiftKey && (e.key === '>' || e.key === '.' || e.key === '<' || e.key === ',')) { e.preventDefault(); e.stopPropagation(); stepSize(e.key === '>' || e.key === '.' ? 1 : -1); return; }
  if (inField() || !mod) return;
  const textSel = getSelection() && !getSelection().isCollapsed && page.contains(getSelection().anchorNode);
  if (k === 'c' && !textSel) { if (copyBlocks()) e.preventDefault(); }
  else if (k === 'x' && !textSel) { if (copyBlocks()) { e.preventDefault(); deleteBlocks(); } }
  else if (k === 'd') { e.preventDefault(); const bs = F.selBlocks(); if (bs.length) pasteBlocks(JSON.stringify(bs)); }
  else if (k === 'g') { e.preventDefault(); e.shiftKey ? F.ungroupSel() : F.groupSel(); }
}, true);
document.addEventListener('paste', e => {
  if (inField() || !S.clip || !$('#askBox').hidden) return;
  if ([...(e.clipboardData?.items || [])].some(i => i.type.startsWith('image/'))) return;   // images: editor.js inserts them
  e.preventDefault(); pasteBlocks();
});

// ---------- text formatting
function restoreSel() { const m = F.editEl(); if (!m) return null; m.focus(); if (S.editRange) { const s = getSelection(); s.removeAllRanges(); s.addRange(S.editRange); } return m; }
function onText(fn, why) {
  if (S.editing) { const m = restoreSel(); fn(m, true); S.editRange = getSelection().rangeCount ? getSelection().getRangeAt(0).cloneRange() : null; refresh(); return; }
  const ts = F.selBlocks().filter(b => b.type === 'text'); if (!ts.length) return F.toast('Select a text box, or click into one');
  const ids = ts.map(b => b.id);
  for (const id of ids) { F.startEdit(id, { all: true }); fn(F.editEl(), false); F.commitEdit(); }
  F.selectMany(ids); refresh();
}
const exec = (c, v) => document.execCommand(c, false, v);
function sizeSel(m, pt) {
  const sl = getSelection(); if (!sl.rangeCount) return;
  if (sl.isCollapsed) {           // caret only: what is typed next gets the size
    const sp = document.createElement('span'); sp.style.fontSize = pt + 'pt'; sp.textContent = '​';
    const r = sl.getRangeAt(0); r.insertNode(sp); const r2 = document.createRange(); r2.setStart(sp.firstChild, 1); r2.collapse(true); sl.removeAllRanges(); sl.addRange(r2); return;
  }
  exec('styleWithCSS', false); exec('fontSize', '7');
  const spans = [];
  for (const f of $$('font[size="7"]', m)) { const sp = document.createElement('span'); sp.style.fontSize = pt + 'pt'; sp.append(...f.childNodes); f.replaceWith(sp); $$('[style]', sp).forEach(x => x.style.removeProperty('font-size')); spans.push(sp); }
  for (const x of $$('span', m)) if (/xxx-large/.test(x.style.fontSize)) { x.style.fontSize = pt + 'pt'; spans.push(x); }
  if (spans.length) { const r = document.createRange(); r.setStartBefore(spans[0]); r.setEndAfter(spans[spans.length - 1]); sl.removeAllRanges(); sl.addRange(r); }
}
function curPt() {
  if (S.editing && S.editRange) { let n = S.editRange.startContainer; if (n.nodeType === 3) n = n.parentElement; return Math.round(parseFloat(getComputedStyle(n).fontSize) * 0.75 * 2) / 2; }
  const b = F.blockById(S.sel); return b && b.type === 'text' ? (b.pt || (S.doc.style && S.doc.style.text_pt) || 8) : null;
}
const SIZES = [6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 44, 48, 54, 60, 66, 72, 80, 96, 120, 144];
function stepSize(dir) {
  if (S.editing) { const p = curPt() || 12; const n = dir > 0 ? (SIZES.find(s => s > p) || p + 12) : ([...SIZES].reverse().find(s => s < p) || Math.max(1, p - 1)); onText(m => sizeSel(m, n)); return; }
  each(b => { if (b.type !== 'text') return; const p = b.pt || (S.doc.style && S.doc.style.text_pt) || 8; const n = dir > 0 ? (SIZES.find(s => s > p) || p + 12) : ([...SIZES].reverse().find(s => s < p) || Math.max(1, p - 1)); scaleInline(b, n / p); b.pt = n; }, dir > 0 ? 'grow text' : 'shrink text');
}
function setSize(pt) {
  if (!(pt > 0)) return;
  if (S.editing) return onText(m => sizeSel(m, pt));
  each(b => { if (b.type === 'text') { b.pt = pt; stripInline(b, 'font-size'); } }, 'font size ' + pt);
}
function setFont(name) {
  if (!name) return;
  if (S.editing) return onText(() => { exec('styleWithCSS', false); exec('fontName', name); });
  each(b => { if (b.type === 'text') { b.font = name; stripInline(b, 'font-family'); } }, 'font ' + name);
}
function setColor(c) {
  if (S.editing) return onText(() => { exec('styleWithCSS', false); exec('foreColor', c); });
  each(b => { if (b.type === 'text') { b.color = c; stripInline(b, 'color'); } }, 'text colour');
}
function setHilite(c) { onText(() => { exec('styleWithCSS', true); exec('hiliteColor', c); exec('styleWithCSS', false); }); }
const ALIGN = { justifyLeft: 'left', justifyCenter: 'center', justifyRight: 'right', justifyFull: 'justify' };
const TEXTCMDS = new Set(['bold', 'italic', 'underline', 'strikeThrough', 'superscript', 'subscript', 'insertUnorderedList', 'insertOrderedList', 'indent', 'outdent', 'removeFormat']);
function blockText(prop, v, why) {
  const set = b => { if (b.type === 'text') { if (v == null) delete b[prop]; else b[prop] = v; } };
  if (S.editing) {   // keep typing: style the live element, save the block
    const b = F.blockById(S.editing); F.pushUndo(); set(b); const m = F.editEl();
    if (prop === 'lh') m.style.lineHeight = v || '';
    if (prop === 'valign') { const on = v && v !== 'top'; m.style.display = on ? 'flex' : ''; m.style.flexDirection = on ? 'column' : ''; m.style.justifyContent = v === 'middle' ? 'center' : v === 'bottom' ? 'flex-end' : ''; }
    F.markDirty(why); restoreSel(); return;
  }
  each(set, why);
}

// ---------- fill / outline / line
function fill(c) { each(b => { if (b.type === 'shape') b.fill = c; else b.bg = c; }, 'fill'); }
function outline(c) { each(b => { if (b.type === 'shape') b.stroke = c; else { b.border = c; if (b.bw == null) b.bw = 1; } }, 'outline'); }
function weight(w) { each(b => { if (b.type === 'shape') b.sw = w; else { b.bw = w; if (!b.border) b.border = '#000000'; } }, 'line weight ' + w); }

// ---------- arrange
function order(mode) {
  if (S.editing) F.commitEdit();
  const bs = F.selBlocks(); if (!bs.length) return F.toast('Select a block first');
  F.pushUndo();
  const zs = S.doc.blocks.map(b => b.z || 0), hi = Math.max(...zs), lo = Math.min(...zs);
  const sorted = [...bs].sort((a, b) => (a.z || 0) - (b.z || 0));
  sorted.forEach((b, i) => { if (mode === 'front') b.z = hi + 1 + i; else if (mode === 'back') b.z = lo - sorted.length + i; else b.z = (b.z || 0) + (mode === 'forward' ? 1 : -1); });
  F.markDirty('order ' + mode); rerender(bs.map(b => b.id));
}
function align(mode) {
  const bs = F.selBlocks().filter(b => b.x != null); if (!bs.length) return F.toast('Select blocks to align');
  const one = bs.length === 1, P = pg();
  const x0 = one ? 0 : Math.min(...bs.map(b => b.x)), x1 = one ? P.w_mm : Math.max(...bs.map(b => b.x + b.w));
  const y0 = one ? 0 : Math.min(...bs.map(b => b.y)), y1 = one ? P.h_mm : Math.max(...bs.map(b => b.y + b.h));
  each(b => {
    if (mode === 'L') b.x = x0; if (mode === 'R') b.x = x1 - b.w; if (mode === 'C') b.x = (x0 + x1) / 2 - b.w / 2;
    if (mode === 'T') b.y = y0; if (mode === 'B') b.y = y1 - b.h; if (mode === 'M') b.y = (y0 + y1) / 2 - b.h / 2;
    b.x = +b.x.toFixed(2); b.y = +b.y.toFixed(2);
  }, 'align ' + mode);
}
function distribute(axis) {
  const bs = F.selBlocks().filter(b => b.x != null); if (bs.length < 3) return F.toast('Select 3 or more blocks to distribute');
  const P = axis === 'H' ? 'x' : 'y', D = axis === 'H' ? 'w' : 'h';
  const s = [...bs].sort((a, b) => a[P] - b[P]); const span = s[s.length - 1][P] + s[s.length - 1][D] - s[0][P]; const gap = (span - s.reduce((t, b) => t + b[D], 0)) / (s.length - 1);
  F.pushUndo(); let at = s[0][P]; for (const b of s) { b[P] = +at.toFixed(2); at += b[D] + gap; }
  F.markDirty('distribute ' + axis); rerender(bs.map(b => b.id));
}
function lockToggle() { const bs = F.selBlocks(); if (!bs.length) return; const lock = !bs.every(b => b.locked); each(b => { if (lock) b.locked = true; else delete b.locked; }, lock ? 'lock' : 'unlock'); F.toast(lock ? 'Locked' : 'Unlocked'); }
function ask() {
  if (S.editing) F.commitEdit();
  if (S.multi.size > 1) F.showSelToolsForGroup();
  else if (S.sel) F.showSelToolsForBlock($(`.blk[data-id="${S.sel}"]`, page));
  else S.anchor = null;
  F.hideSelTools(); F.openAsk();
}

// ---------- command dispatch
const CMD = {
  textbox: insertText, picture: () => $('#fileInput').click(),
  copy: copyBlocks, cut: () => { if (copyBlocks()) deleteBlocks(); }, paste: () => pasteBlocks(), duplicate: () => { const bs = F.selBlocks(); if (bs.length) pasteBlocks(JSON.stringify(bs)); },
  delete: deleteBlocks, lock: lockToggle,
  front: () => order('front'), back: () => order('back'), forward: () => order('forward'), backward: () => order('backward'),
  alignL: () => align('L'), alignC: () => align('C'), alignR: () => align('R'), alignT: () => align('T'), alignM: () => align('M'), alignB: () => align('B'),
  distH: () => distribute('H'), distV: () => distribute('V'),
  rotL: () => each(b => { b.rotate = (((b.rotate || 0) - 90) % 360 + 360) % 360; }, 'rotate'), rotR: () => each(b => { b.rotate = ((b.rotate || 0) + 90) % 360; }, 'rotate'),
  nofill: () => each(b => { if (b.type === 'shape') b.fill = 'none'; else delete b.bg; }, 'no fill'),
  noline: () => each(b => { if (b.type === 'shape') b.stroke = 'none'; else { delete b.border; delete b.bw; } }, 'no outline'),
  vtop: () => blockText('valign', null, 'text top'), vmiddle: () => blockText('valign', 'middle', 'text middle'), vbottom: () => blockText('valign', 'bottom', 'text bottom'),
  grow: () => stepSize(1), shrink: () => stepSize(-1),
  zoom100: () => F.setZoom(1), ask,
  group: () => F.groupSel(), ungroup: () => F.ungroupSel(),
  crop: () => { if (S.cropping) return F.endCrop(); const b = F.blockById(S.sel); if (!b || b.type !== 'image') return F.toast('Select a picture to crop'); F.startCrop(b.id); },
  resetCrop: () => { const b = F.blockById(S.sel); if (!b || b.type !== 'image' || !b.crop) return F.toast('Select a cropped picture'); F.resetCrop(b.id); },
};
$('#ribbon').addEventListener('click', e => {
  const b = e.target.closest('button[data-cmd]'); if (!b) return;
  const c = b.dataset.cmd;
  if (CMD[c]) return CMD[c]();
  if (ALIGN[c]) { if (S.editing) return onText(() => exec(c)); return each(x => { if (x.type === 'text') { x.align = ALIGN[c]; stripInline(x, 'text-align'); } }, 'align ' + ALIGN[c]); }
  if (TEXTCMDS.has(c)) return onText(() => { exec('styleWithCSS', false); exec(c); });
});
$('#btnAskTop').onclick = ask;
const onEnter = (el, fn) => { el.addEventListener('change', () => fn(el.value)); el.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); fn(el.value); if (S.editing) restoreSel(); } e.stopPropagation(); }); };
onEnter($('#fontSize'), v => setSize(parseFloat(v)));
onEnter($('#fontName'), v => setFont(v.trim()));
const bindColor = (id, bar, fn) => { const i = $(id); $(bar).style.background = i.value; i.addEventListener('input', () => $(bar).style.background = i.value); i.addEventListener('change', () => fn(i.value)); };
bindColor('#fontColor', '#fontColorBar', setColor); bindColor('#hiliteColor', '#hiliteBar', setHilite);
bindColor('#fillColor', '#fillBar', fill); bindColor('#fillColor2', '#fillBar2', fill);
bindColor('#lineColor', '#lineBar', outline); bindColor('#lineColor2', '#lineBar2', outline);
$('#lineSpacing').onchange = e => { const v = e.target.value; e.target.value = ''; if (v) blockText('lh', +v, 'line spacing ' + v); };
$('#lineWeight').onchange = e => { const v = +e.target.value; e.target.value = ''; if (v) weight(v); };
$('#lineDash').onchange = e => { const v = e.target.value; e.target.value = ''; if (v) each(b => { if (v === 'solid') delete b.dash; else b.dash = v; }, 'dash ' + v); };
onEnter($('#cornerR'), v => each(b => { if (v === '') delete b.radius; else b.radius = +v; }, 'corner radius'));
for (const [id, k] of [['#geoX', 'x'], ['#geoY', 'y'], ['#geoW', 'w'], ['#geoH', 'h'], ['#geoR', 'rotate']])
  onEnter($(id), v => { if (v === '' || !S.sel) return; const b = F.blockById(S.sel); if (!b) return; if (S.editing) F.commitEdit(); F.pushUndo(); b[k] = +(+v).toFixed(2); F.markDirty(`${k} ${b.id}`); rerender([...S.multi]); });

// ---------- reflect the current selection in the ribbon
function refresh() {
  if (!S.doc) return;
  const b = F.blockById(S.sel), editing = !!S.editing;
  for (const btn of $$('#ribbon [data-state]')) { let on = false; if (editing) { try { on = document.queryCommandState(btn.dataset.state); } catch {} } btn.classList.toggle('on', on); }
  const fs = $('#fontSize'), fn = $('#fontName');
  if (document.activeElement !== fs) fs.value = curPt() ?? '';
  if (document.activeElement !== fn) {
    let f = '';
    if (editing && S.editRange) { let n = S.editRange.startContainer; if (n.nodeType === 3) n = n.parentElement; f = getComputedStyle(n).fontFamily; }
    else if (b && b.type === 'text') f = b.font || (S.doc.style && S.doc.style.font) || '';
    fn.value = (f.split(',')[0] || '').replace(/["']/g, '').trim();
  }
  for (const [id, k] of [['#geoX', 'x'], ['#geoY', 'y'], ['#geoW', 'w'], ['#geoH', 'h'], ['#geoR', 'rotate']]) { const el = $(id); if (document.activeElement !== el) el.value = b && b[k] != null ? +(+b[k]).toFixed(2) : (b && k === 'rotate' ? 0 : ''); }
  const cr = $('#cornerR'); if (document.activeElement !== cr) cr.value = b && b.radius != null ? b.radius : '';
  $('#ribbon').classList.toggle('editing', editing);
  $$('#ribbon [data-crop]').forEach(x => x.classList.toggle('on', !!S.cropping));
}
document.addEventListener('folio:selection', () => { clearTimeout(refresh._t); refresh._t = setTimeout(refresh, 30); });
// keyboard T inserts a text box at the view centre (editor.js handles I / S / 0)
document.addEventListener('keydown', e => { if (!inField() && !e.metaKey && !e.ctrlKey && !e.altKey && e.key.toLowerCase() === 't') { e.preventDefault(); e.stopImmediatePropagation(); insertText(); } }, true);
refresh();
})();
