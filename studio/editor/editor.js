/* Folio Studio editor — one document model (text + image blocks), two layouts (canvas, flow).
   Talks to server.py; the Claude that answers Ask/Edit is the terminal session that started the studio. */
(() => {
'use strict';
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const qs = new URLSearchParams(location.search);
const TOKEN = qs.get('t') || (document.cookie.match(/folio_t=([\w\-]+)/) || [])[1] || '';
const PRINT = qs.get('print') === '1';
const PX_PER_MM = 96 / 25.4;
const LS = { get: (k, d) => { try { const v = localStorage.getItem('folio.' + k); return v == null ? d : JSON.parse(v); } catch { return d; } }, set: (k, v) => { try { localStorage.setItem('folio.' + k, JSON.stringify(v)); } catch {} } };

const api = async (path, body, method) => {
  const r = await fetch(path + (path.includes('?') ? '&' : '?') + 't=' + encodeURIComponent(TOKEN), {
    method: method || (body ? 'POST' : 'GET'), headers: { 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
  if (!r.ok) throw new Error((await r.text()).slice(0, 200));
  return r.json();
};
const toast = (m, ms = 2200) => { const t = $('#toast'); t.textContent = m; t.hidden = false; clearTimeout(t._t); t._t = setTimeout(() => t.hidden = true, ms); };
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const uid = p => (p || 'b') + Math.random().toString(36).slice(2, 7);
const round = (v, s = 0.5) => Math.round(v / s) * s;

// ---------- tiny markdown (bold, italic, sup/sub, code, headings, bullets, line breaks)
function inline(s) {
  s = esc(s);
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>')
       .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
       .replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g, '$1<i>$2</i>')
       .replace(/\^([^^\s]+)\^/g, '<sup>$1</sup>')
       .replace(/~([^~\s]+)~/g, '<sub>$1</sub>')
       .replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, '<a href="$2" target="_blank">$1</a>');
  return s;
}
function md(src) {
  const lines = String(src ?? '').replace(/\r/g, '').split('\n');
  let out = '', para = [], list = null;
  const endList = () => { if (list) { out += `</${list}>`; list = null; } };
  const endPara = () => { if (para.length) { out += '<p>' + para.map(inline).join('<br>') + '</p>'; para = []; } };
  for (const ln of lines) {
    const h = ln.match(/^(#{1,3})\s+(.*)$/);
    const ul = ln.match(/^\s*[-•*]\s+(.*)$/), ol = ln.match(/^\s*\d+[.)]\s+(.*)$/);
    if (h) { endPara(); endList(); out += `<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`; }
    else if (ul || ol) { endPara(); const t = ul ? 'ul' : 'ol'; if (list !== t) { endList(); out += `<${t}>`; list = t; } out += '<li>' + inline((ul || ol)[1]) + '</li>'; }
    else if (!ln.trim()) { endPara(); endList(); }
    else { endList(); para.push(ln); }
  }
  endPara(); endList();
  return out;
}
// rich text typed in the page is stored as sanitised HTML (b.html) next to a Markdown mirror (b.text) for Claude
const RT_TAGS = new Set(['B', 'STRONG', 'I', 'EM', 'U', 'S', 'STRIKE', 'SUP', 'SUB', 'SPAN', 'FONT', 'P', 'DIV', 'BR', 'UL', 'OL', 'LI', 'A', 'H1', 'H2', 'H3']);
const RT_STYLES = ['font-size', 'font-family', 'color', 'background-color', 'font-weight', 'font-style', 'text-decoration', 'text-decoration-line', 'text-align', 'margin-left', 'padding-left', 'line-height'];
const parseBody = html => new DOMParser().parseFromString('<!doctype html><body>' + (html || ''), 'text/html').body;
function cleanHTML(html) {
  const body = parseBody(html);
  const walk = node => {
    for (const c of [...node.childNodes]) {
      if (c.nodeType === 3) continue;
      if (c.nodeType !== 1) { c.remove(); continue; }
      if (!RT_TAGS.has(c.tagName)) { if (/^(SCRIPT|STYLE|IFRAME|OBJECT|EMBED|svg|SVG|IMG|VIDEO|AUDIO|LINK|META)$/.test(c.tagName)) c.remove(); else { walk(c); c.replaceWith(...c.childNodes); } continue; }
      let el = c;
      if (c.tagName === 'FONT') { const sp = c.ownerDocument.createElement('span'); if (c.getAttribute('color')) sp.style.color = c.getAttribute('color'); if (c.getAttribute('face')) sp.style.fontFamily = c.getAttribute('face'); sp.setAttribute('style', (sp.getAttribute('style') || '') + (c.getAttribute('style') || '')); sp.append(...c.childNodes); c.replaceWith(sp); el = sp; }
      const keep = []; for (const pr of RT_STYLES) { const v = el.style.getPropertyValue(pr); if (v && !/url\(|expression/i.test(v)) keep.push([pr, v]); }
      const href = el.tagName === 'A' ? el.getAttribute('href') : null;
      for (const at of [...el.attributes]) el.removeAttribute(at.name);
      for (const [pr, v] of keep) el.style.setProperty(pr, v);
      if (href && /^https?:/i.test(href)) { el.setAttribute('href', href); el.setAttribute('target', '_blank'); }
      walk(el);
      if (el.tagName === 'SPAN' && !el.getAttribute('style')) el.replaceWith(...el.childNodes);
    }
  };
  walk(body);
  return body.innerHTML.replace(/<(p|div)><\/\1>/g, '');
}
function htmlToMd(html) {
  const lines = [];
  const isB = c => /^(B|STRONG)$/.test(c.tagName) || /^(bold|bolder|[6-9]00)$/.test(c.style.fontWeight);
  const isI = c => /^(I|EM)$/.test(c.tagName) || c.style.fontStyle === 'italic';
  const inl = n => [...n.childNodes].map(c => {
    if (c.nodeType === 3) return c.nodeValue;
    if (c.nodeType !== 1 || /^(UL|OL)$/.test(c.tagName)) return '';
    if (c.tagName === 'BR') return '\n';
    const x = inl(c); if (!x.trim()) return x;
    if (c.tagName === 'SUP') return `^${x}^`; if (c.tagName === 'SUB') return `~${x}~`;
    if (c.tagName === 'A') return `[${x}](${c.getAttribute('href') || ''})`;
    let y = x; if (isI(c)) y = `*${y}*`; if (isB(c)) y = `**${y}**`; return y;
  }).join('');
  const block = (n, depth) => {
    let buf = '';
    const flush = () => { if (buf.trim()) lines.push(...buf.replace(/^\n+|\n+$/g, '').split('\n')); buf = ''; };
    for (const c of n.childNodes) {
      if (c.nodeType === 1 && /^(UL|OL)$/.test(c.tagName)) {
        flush(); let k = 1;
        for (const li of c.children) {
          if (li.tagName !== 'LI') continue;
          lines.push('  '.repeat(depth) + (c.tagName === 'OL' ? `${k++}. ` : '- ') + inl(li).replace(/\n+/g, ' ').trim());
          for (const sub of li.children) if (/^(UL|OL)$/.test(sub.tagName)) block({ childNodes: [sub] }, depth + 1);
        }
      } else if (c.nodeType === 1 && /^(P|DIV|H1|H2|H3)$/.test(c.tagName)) {
        flush();
        if ([...c.children].some(x => /^(UL|OL|P|DIV)$/.test(x.tagName))) block(c, depth);
        else lines.push((c.tagName[0] === 'H' ? '#'.repeat(+c.tagName[1]) + ' ' : '') + inl(c).replace(/\n$/, ''));
      } else buf += c.nodeType === 1 ? inl({ childNodes: [c] }) : (c.nodeValue || '');
    }
    flush();
  };
  block(parseBody(html), 0);
  return lines.join('\n').replace(/\n{3,}/g, '\n\n').trim();
}
// shapes: drawn in the block's own mm box (re-drawn on resize, so strokes keep their width)
function shapeSVG(b) {
  const w = Math.max(0.5, b.w || 10), h = Math.max(0.5, b.h || 10);
  const line = /^(line|arrow|darrow)$/.test(b.shape);
  const sw = (b.sw ?? (line ? 1.5 : 1)) * 25.4 / 72, st = esc(b.stroke ?? (line ? '#1F2937' : '#2F528F')), fill = esc(b.fill ?? (line ? 'none' : '#4472C4'));
  const dash = b.dash === 'dash' ? `stroke-dasharray="${(sw * 4).toFixed(2)} ${(sw * 3).toFixed(2)}"` : b.dash === 'dot' ? `stroke-dasharray="0.01 ${(sw * 2).toFixed(2)}" stroke-linecap="round"` : '';
  const ss = `stroke="${st}" stroke-width="${sw.toFixed(3)}" ${dash} stroke-linejoin="round"`, i = sw / 2, f = v => (+v).toFixed(2);
  let g = '';
  switch (b.shape) {
    case 'ellipse': g = `<ellipse cx="${f(w / 2)}" cy="${f(h / 2)}" rx="${f(w / 2 - i)}" ry="${f(h / 2 - i)}" fill="${fill}" ${ss}/>`; break;
    case 'roundrect': { const r = Math.min(b.radius ?? Math.min(w, h) * 0.18, w / 2, h / 2); g = `<rect x="${f(i)}" y="${f(i)}" width="${f(w - sw)}" height="${f(h - sw)}" rx="${f(r)}" fill="${fill}" ${ss}/>`; break; }
    case 'triangle': g = `<polygon points="${f(w / 2)},${f(i)} ${f(w - i)},${f(h - i)} ${f(i)},${f(h - i)}" fill="${fill}" ${ss}/>`; break;
    case 'rarrow': { const hl = Math.min(w * 0.45, h * 0.9), t = h * 0.25; g = `<polygon points="${f(i)},${f(t)} ${f(w - hl)},${f(t)} ${f(w - hl)},${f(i)} ${f(w - i)},${f(h / 2)} ${f(w - hl)},${f(h - i)} ${f(w - hl)},${f(h - t)} ${f(i)},${f(h - t)}" fill="${fill}" ${ss}/>`; break; }
    case 'chevron': { const d = Math.min(w * 0.4, h * 0.5); g = `<polygon points="${f(i)},${f(i)} ${f(w - d)},${f(i)} ${f(w - i)},${f(h / 2)} ${f(w - d)},${f(h - i)} ${f(i)},${f(h - i)} ${f(d)},${f(h / 2)}" fill="${fill}" ${ss}/>`; break; }
    case 'line': case 'arrow': case 'darrow': {
      const y = h / 2, hl = Math.max(sw * 4, 1.2), hw = hl * 0.45;
      const x1 = b.shape === 'darrow' ? hl * 0.9 : 0, x2 = b.shape === 'line' ? w : w - hl * 0.9;
      g = `<line x1="${f(x1)}" y1="${f(y)}" x2="${f(x2)}" y2="${f(y)}" ${ss} fill="none"/>`;
      if (b.shape !== 'line') g += `<polygon points="${f(w)},${f(y)} ${f(w - hl)},${f(y - hw)} ${f(w - hl)},${f(y + hw)}" fill="${st}"/>`;
      if (b.shape === 'darrow') g += `<polygon points="0,${f(y)} ${f(hl)},${f(y - hw)} ${f(hl)},${f(y + hw)}" fill="${st}"/>`;
      break;
    }
    default: g = `<rect x="${f(i)}" y="${f(i)}" width="${f(w - sw)}" height="${f(h - sw)}" fill="${fill}" ${ss}/>`;
  }
  return `<svg viewBox="0 0 ${f(w)} ${f(h)}" width="100%" height="100%" preserveAspectRatio="none" style="display:block;overflow:visible">${g}</svg>`;
}
function boxStyle(el, b) {
  if (b.border && b.border !== 'none') el.style.border = `${b.bw ?? 1}pt ${b.dash === 'dash' ? 'dashed' : b.dash === 'dot' ? 'dotted' : 'solid'} ${b.border}`;
  if (b.radius != null) el.style.borderRadius = b.radius + 'mm';
}
function mdTable(src) { // markdown with simple pipe tables for answers
  const blocks = String(src ?? '').split(/\n(?=\|)/);
  return src.split(/\n{2,}/).map(chunk => {
    const ls = chunk.trim().split('\n');
    if (ls.length >= 2 && /^\|/.test(ls[0]) && /^\|?\s*:?-+/.test(ls[1])) {
      const rows = ls.filter((l, i) => i !== 1).map(l => l.replace(/^\||\|$/g, '').split('|').map(c => inline(c.trim())));
      return '<table><tr>' + rows[0].map(c => `<th>${c}</th>`).join('') + '</tr>' + rows.slice(1).map(r => '<tr>' + r.map(c => `<td>${c}</td>`).join('') + '</tr>').join('') + '</table>';
    }
    return md(chunk);
  }).join('');
}

// ---------- state
const S = { fid: null, doc: null, hash: null, zoom: 1, sel: null, multi: new Set(), editing: null, dirty: false, undo: [], redo: [], review: { threads: [], notes: [], suggestions: [] }, side: null, anchor: null, images: [], tab: 'ask', snap: true };
const page = $('#page'), wrap = $('#pageWrap'), viewport = $('#viewport');

// ---------- load / save
async function loadFolios() {
  const list = await api('/api/folios');
  const sel = $('#folioSelect');
  sel.innerHTML = list.map(f => `<option value="${esc(f.id)}">${esc(f.title || f.id)}</option>`).join('');
  const want = qs.get('folio') || LS.get('last', null) || (list[0] && list[0].id);
  if (want) { sel.value = want; await openFolio(want); }
}
async function openFolio(fid) {
  S.fid = fid; LS.set('last', fid); history.replaceState(null, '', '?t=' + TOKEN + '&folio=' + fid + (PRINT ? '&print=1' : ''));
  S.doc = await api('/api/folio/' + fid); S.hash = S.doc._hash; S.undo = []; S.redo = []; S.sel = null; S.multi = new Set(); S.dirty = false; S.ops = 0; undoState();
  document.title = (S.doc.title || fid) + ' · Folio Studio';
  render();
  if (!PRINT) { await loadReview(); loadVersions(); requestAnimationFrame(fit); }   // every opened (or newly made) folio starts fitted and centred
}
let saveTimer = null;
function markDirty(why) {
  S.ops = (S.ops || 0) + 1;            // changes since the last save; the server keeps one version per 5
  S.dirty = true; $('#saveState').textContent = 'editing…';
  clearTimeout(saveTimer); saveTimer = setTimeout(() => save(why), 700);
}
async function save(why) {
  if (!S.dirty) return;
  $('#saveState').textContent = 'saving…';
  try {
    const ops = S.ops || 1, first = !!S.archiveFirst; S.ops = 0; S.archiveFirst = false;
    const r = await api('/api/folio/' + S.fid, { doc: S.doc, why: why || 'editor', ops, archive_first: first });
    S.hash = r.hash; S.dirty = false; $('#saveState').textContent = 'saved'; loadVersions();
  } catch (e) { $('#saveState').textContent = 'save failed'; toast('Save failed: ' + e.message); }
}
const UNDO_DEPTH = 20;                 // undo / redo reach back 20 operations
function pushUndo() { S.undo.push(JSON.stringify(S.doc.blocks)); if (S.undo.length > UNDO_DEPTH) S.undo.shift(); S.redo = []; undoState(); }
function undo() { if (!S.undo.length) return toast('Nothing to undo (last ' + UNDO_DEPTH + ' operations are kept)'); S.redo.push(JSON.stringify(S.doc.blocks)); if (S.redo.length > UNDO_DEPTH) S.redo.shift(); S.doc.blocks = JSON.parse(S.undo.pop()); render(); markDirty('undo'); undoState(); }
function redo() { if (!S.redo.length) return; S.undo.push(JSON.stringify(S.doc.blocks)); if (S.undo.length > UNDO_DEPTH) S.undo.shift(); S.doc.blocks = JSON.parse(S.redo.pop()); render(); markDirty('redo'); undoState(); }
function undoState() { const u = $('#btnUndo'), r = $('#btnRedo'); if (u) { u.disabled = !S.undo.length; u.title = `Undo (Ctrl/⌘Z) · ${S.undo.length}/${UNDO_DEPTH}`; } if (r) { r.disabled = !S.redo.length; r.title = `Redo (Ctrl/⌘⇧Z) · ${S.redo.length}`; } }

// ---------- render
function blockById(id) { return S.doc.blocks.find(b => b.id === id); }
function render() {
  const d = S.doc, pg = d.page || {};
  const flow = d.mode === 'flow';
  page.className = flow ? 'flow' : '';
  if ($('#btnGrid').classList.contains('on') && !PRINT) page.classList.add('grid');
  page.style.width = (pg.w_mm || 180) + 'mm';
  page.style.height = flow ? 'auto' : (pg.h_mm || 120) + 'mm';
  if (flow) { page.style.minHeight = (pg.h_mm || 297) + 'mm'; page.style.setProperty('--margin', (pg.margin_mm ?? 15) + 'mm'); }
  page.style.fontFamily = (d.style && d.style.font) || 'Arial, Helvetica, sans-serif';
  page.innerHTML = '';
  $('#modeBadge').textContent = d.mode || 'canvas';
  for (const b of d.blocks) page.appendChild(renderBlock(b));
  applyZoom();
  decorate();
  paintSel();
}
function renderBlock(b) {
  const el = document.createElement('div');
  el.className = 'blk ' + b.type + (b.role ? ' ' + b.role : '') + (b.fit === 'cover' ? ' cover' : b.fit === 'fill' ? ' fill' : '') + (b.hidden ? ' hidden' : '');
  el.dataset.id = b.id;
  const flow = S.doc.mode === 'flow';
  if (!flow) { el.style.left = b.x + 'mm'; el.style.top = b.y + 'mm'; }
  el.style.width = (b.w != null ? b.w + 'mm' : (flow ? '100%' : '40mm'));
  if (!flow) el.style.height = (b.h ?? 20) + 'mm';
  else if (b.type === 'image') el.style.height = (b.h ?? 60) + 'mm';
  if (b.rotate) el.style.transform = `rotate(${b.rotate}deg)`;
  if (b.z != null) el.style.zIndex = b.z;
  if (b.type === 'image') {
    const im = document.createElement('img');
    im.src = `/assets/${S.fid}/${b.src}?t=${TOKEN}`; im.alt = b.alt || b.id; im.draggable = false;
    const clip = document.createElement('div'); clip.className = 'clip'; clip.appendChild(im);
    el.appendChild(clip); boxStyle(el, b); applyCrop(el, b);
  } else if (b.type === 'shape') {
    const sv = document.createElement('div'); sv.className = 'shp'; sv.innerHTML = shapeSVG(b); el.appendChild(sv);
  } else {
    const m = document.createElement('div');
    m.className = 'md'; m.innerHTML = b.html ? cleanHTML(b.html) : md(b.text || '');
    if (b.lh) m.style.lineHeight = b.lh;
    if (b.valign && b.valign !== 'top') { m.style.display = 'flex'; m.style.flexDirection = 'column'; m.style.justifyContent = b.valign === 'middle' ? 'center' : 'flex-end'; }
    boxStyle(el, b);
    m.style.fontSize = (b.pt || (S.doc.style && S.doc.style.text_pt) || 8) + 'pt';
    if (b.align) m.style.textAlign = b.align;
    if (b.color) m.style.color = b.color;
    if (b.font) m.style.fontFamily = b.font;
    if (b.bg) el.style.background = b.bg;
    if (b.pad != null) m.style.padding = b.pad + 'mm';
    el.appendChild(m);
  }
  if (!PRINT) {
    for (const h of ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w']) { const hd = document.createElement('div'); hd.className = 'handle ' + h; hd.dataset.h = h; el.appendChild(hd); }
    const dim = document.createElement('div'); dim.className = 'dim'; el.appendChild(dim);
    const chips = document.createElement('div'); chips.className = 'chips'; el.appendChild(chips);
  }
  return el;
}
// crop = {l, t, r, b}: fractions of the picture cut away on each side; the block box is the visible part
function applyCrop(el, b) {
  const im = $('.clip img', el); if (!im) return;
  const c = b.crop, cropping = S.cropping === b.id;
  const place = (img, cc) => { const fw = 1 - cc.l - cc.r, fh = 1 - cc.t - cc.b; Object.assign(img.style, { position: 'absolute', left: (-cc.l / fw * 100) + '%', top: (-cc.t / fh * 100) + '%', width: (100 / fw) + '%', height: (100 / fh) + '%', objectFit: 'fill', maxWidth: 'none', maxHeight: 'none' }); };
  if (c) place(im, c); else im.removeAttribute('style');
  el.classList.toggle('cropping', cropping);
  let g = $('.cropghost', el);
  if (cropping) {
    if (!g) { g = document.createElement('img'); g.className = 'cropghost'; g.src = im.src; g.draggable = false; el.insertBefore(g, el.firstChild); }
    place(g, c || { l: 0, t: 0, r: 0, b: 0 });
  } else if (g) g.remove();
}
function startCrop(id) {
  const b = blockById(id); if (!b || b.type !== 'image' || S.doc.mode === 'flow') return;
  if (S.editing) commitEdit();
  const im = $(`.blk[data-id="${id}"] .clip img`, page);
  if (!b.crop && im && im.naturalWidth) {     // first crop: fit the box to the picture itself (no letterbox)
    pushUndo();
    const ar = im.naturalWidth / im.naturalHeight;
    if (b.w / b.h > ar) { const w = b.h * ar; b.x = +(b.x + (b.w - w) / 2).toFixed(2); b.w = +w.toFixed(2); }
    else { const h = b.w / ar; b.y = +(b.y + (b.h - h) / 2).toFixed(2); b.h = +h.toFixed(2); }
    b.crop = { l: 0, t: 0, r: 0, b: 0 }; markDirty('crop ' + id);
  }
  S.cropping = id; render(); select(id); hideSelTools();
  toast('Crop: drag the black handles to trim, drag the picture to move it · Enter / Esc to finish', 4000);
}
function endCrop() {
  const id = S.cropping; if (!id) return; S.cropping = null;
  const b = blockById(id); if (b && b.crop && !(b.crop.l || b.crop.t || b.crop.r || b.crop.b)) { delete b.crop; markDirty('crop ' + id); }
  render(); select(id);
}
function resetCrop(id) {
  const b = blockById(id); if (!b || !b.crop) return;
  pushUndo(); const c = b.crop, Wf = b.w / (1 - c.l - c.r), Hf = b.h / (1 - c.t - c.b);
  b.x = +(b.x - c.l * Wf).toFixed(2); b.y = +(b.y - c.t * Hf).toFixed(2); b.w = +Wf.toFixed(2); b.h = +Hf.toFixed(2); delete b.crop;
  if (S.cropping === id) b.crop = { l: 0, t: 0, r: 0, b: 0 };
  markDirty('reset crop ' + id); render(); select(id);
}
// groups: blocks sharing b.group select, move and resize together; a second click selects one member
const groupIds = b => b && b.group ? S.doc.blocks.filter(x => x.group === b.group).map(x => x.id) : (b ? [b.id] : []);
function selGroup() {
  const bs = selBlocks(); if (bs.length < 2) return null; const g = bs[0].group;
  if (!g || bs.some(b => b.group !== g)) return null;
  return S.doc.blocks.filter(b => b.group === g).length === bs.length ? g : null;
}
const bboxOf = bs => { const x0 = Math.min(...bs.map(b => b.x)), y0 = Math.min(...bs.map(b => b.y)); return { x: x0, y: y0, w: Math.max(...bs.map(b => b.x + b.w)) - x0, h: Math.max(...bs.map(b => b.y + b.h)) - y0 }; };
const gbox = document.createElement('div'); gbox.id = 'gbox'; gbox.hidden = true;
for (const h of ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w']) { const hd = document.createElement('div'); hd.className = 'handle ' + h; hd.dataset.h = h; gbox.appendChild(hd); }
function updateGbox() {
  const g = !PRINT && S.doc && S.doc.mode !== 'flow' && selGroup();
  if (!g) { gbox.hidden = true; return; }
  if (!gbox.isConnected) page.appendChild(gbox);
  const bb = bboxOf(selBlocks()); Object.assign(gbox.style, { left: bb.x + 'mm', top: bb.y + 'mm', width: bb.w + 'mm', height: bb.h + 'mm' }); gbox.hidden = false;
}
function groupSel() {
  if (S.editing) commitEdit();
  const bs = selBlocks(); if (bs.length < 2) return toast('Select two or more blocks to group');
  pushUndo(); const gid = uid('g'); bs.forEach(b => b.group = gid); markDirty(`group ${bs.length} blocks`); paintSel(); toast(`Grouped ${bs.length} blocks`);
}
function ungroupSel() {
  const bs = selBlocks().filter(b => b.group); if (!bs.length) return toast('Nothing grouped in the selection');
  pushUndo(); bs.forEach(b => delete b.group); markDirty(`ungroup ${bs.length} blocks`); paintSel(); toast('Ungrouped');
}
function updateDim(el, b) { const d = $('.dim', el); if (d) d.textContent = `${b.id} · ${(b.x ?? 0).toFixed(1)},${(b.y ?? 0).toFixed(1)} · ${(b.w ?? 0).toFixed(1)}×${(b.h ?? 0).toFixed(1)} mm`; }
function decorate() {
  if (PRINT) return;
  const notes = S.review.notes.filter(n => !n.hidden), sugs = S.review.suggestions.filter(s => s.status === 'pending');
  for (const el of $$('.blk', page)) {
    const b = blockById(el.dataset.id); if (!b) continue;
    updateDim(el, b);
    const chips = $('.chips', el); chips.innerHTML = '';
    const nn = notes.filter(n => n.block === b.id).length;
    const ns = sugs.filter(s => s.block === b.id).length;
    el.classList.toggle('hasSug', ns > 0);
    if (nn) { const c = document.createElement('span'); c.className = 'chip'; c.textContent = '💬 ' + nn; c.title = 'Notes on this block'; c.onclick = e => { e.stopPropagation(); showNotes(b.id, c); }; chips.appendChild(c); }
    if (ns) { const c = document.createElement('span'); c.className = 'chip sug'; c.textContent = '✎ ' + ns; c.title = 'Claude suggests a change'; c.onclick = e => { e.stopPropagation(); showSuggestions(b.id, c); }; chips.appendChild(c); }
  }
  const added = sugs.filter(s => s.op === 'add');
  $('#threadCount').textContent = S.review.threads.filter(t => t.status !== 'done').length || '';
  $('#noteCount').textContent = notes.length || '';
  if (added.length && !$('#addSugBanner')) { const bnr = document.createElement('div'); bnr.id = 'addSugBanner'; bnr.className = 'chip sug'; bnr.style.cssText = 'position:fixed;top:calc(var(--topH) + 8px);left:50%;transform:translateX(-50%);z-index:35;font-size:12px;padding:4px 10px'; bnr.textContent = `✎ Claude suggests adding ${added.length} block(s) — review`; bnr.onclick = () => showSuggestions(null, bnr); document.body.appendChild(bnr); }
  else if (!added.length && $('#addSugBanner')) $('#addSugBanner').remove();
}

// ---------- zoom
function applyZoom() { wrap.style.transform = PRINT ? 'none' : `scale(${S.zoom})`; const sz = $('#pageSizer'), k = PRINT ? 1 : S.zoom; sz.style.width = page.offsetWidth * k + 'px'; sz.style.height = page.offsetHeight * k + 'px'; $('#zoom').value = Math.round(S.zoom * 100); $('#zoomVal').textContent = Math.round(S.zoom * 100) + '%'; }
function setZoom(z) {                 // keeps the point at the centre of the canvas in place
  const cx = (viewport.scrollLeft + viewport.clientWidth / 2) / Math.max(1, viewport.scrollWidth), cy = (viewport.scrollTop + viewport.clientHeight / 2) / Math.max(1, viewport.scrollHeight);
  S.zoom = Math.min(4, Math.max(.25, z)); applyZoom(); LS.set('zoom.' + S.fid, S.zoom);
  viewport.scrollLeft = cx * viewport.scrollWidth - viewport.clientWidth / 2; viewport.scrollTop = cy * viewport.scrollHeight - viewport.clientHeight / 2;
}
function fit() { const vw = viewport.clientWidth - 80, vh = viewport.clientHeight - 80; setZoom(Math.min(vw / page.offsetWidth, vh / page.offsetHeight, 3)); centre(); }
function centre() { viewport.scrollLeft = (viewport.scrollWidth - viewport.clientWidth) / 2; viewport.scrollTop = (viewport.scrollHeight - viewport.clientHeight) / 2; }
const ZOOMS = [25, 33, 50, 67, 75, 90, 100, 110, 125, 150, 175, 200, 250, 300, 400];   // − / + steps (PowerPoint-like)
function zoomStep(d) { const p = Math.round(S.zoom * 100), n = d > 0 ? ZOOMS.find(v => v > p + 0.5) : [...ZOOMS].reverse().find(v => v < p - 0.5); setZoom((n || (d > 0 ? 400 : 25)) / 100); }
$('#zoomIn').onclick = () => zoomStep(1); $('#zoomOut').onclick = () => zoomStep(-1);
$('#zoom').oninput = e => setZoom(e.target.value / 100);
$('#zoom').onchange = e => e.target.blur();   // give the arrow keys back to nudging
$('#btnFit').onclick = fit;
viewport.addEventListener('wheel', e => { if (e.ctrlKey || e.metaKey) { e.preventDefault(); setZoom(S.zoom * (e.deltaY < 0 ? 1.1 : 0.9)); } }, { passive: false });

// an image resized from an edge (n/e/s/w) stretches to the new box instead of letterboxing (fit=fill);
// corners and Shift keep the aspect. Cropped pictures already fill their frame.
function stretchImage(b, el) {
  if (b.fit === 'fill') return;
  b.fit = 'fill';
  if (el) { el.classList.remove('cover'); el.classList.add('fill'); }
}

// ---------- pointer: select, drag, resize
function pageMM(e) { const r = page.getBoundingClientRect(); return { x: (e.clientX - r.left) / S.zoom / PX_PER_MM, y: (e.clientY - r.top) / S.zoom / PX_PER_MM }; }
// selection = S.multi (ids); S.sel = the primary block (last clicked). One block shows handles,
// a group shows dashed outlines and moves together.
function paintSel() {
  document.dispatchEvent(new CustomEvent('folio:selection'));
  const many = S.multi.size > 1;
  for (const el of $$('.blk', page)) { const on = S.multi.has(el.dataset.id); el.classList.toggle('selected', on && !many); el.classList.toggle('multi', on && many); }
  updateGbox();
}
function select(id, toggle) {
  if (toggle && id) {
    if (S.multi.has(id)) S.multi.delete(id); else S.multi.add(id);
    S.sel = S.multi.has(id) ? id : ([...S.multi].pop() || null);
  } else { S.multi = new Set(id ? [id] : []); S.sel = id || null; }
  paintSel();
}
function selectMany(ids) { S.multi = new Set(ids); S.sel = ids.length ? ids[ids.length - 1] : null; paintSel(); }
function toggleIds(ids) { const on = ids.every(id => S.multi.has(id)); for (const id of ids) on ? S.multi.delete(id) : S.multi.add(id); S.sel = on ? ([...S.multi].pop() || null) : ids[ids.length - 1]; paintSel(); }
const selBlocks = () => S.doc.blocks.filter(b => S.multi.has(b.id));
const marquee = document.createElement('div'); marquee.id = 'marquee'; marquee.hidden = true;
let drag = null;
// rubber band (PowerPoint-style): starts on empty page, on a locked background, or in the grey area around the page
function startMarquee(e, hit, toggle) {
  hideSelTools();
  const p = pageMM(e);
  drag = { marquee: true, sx: p.x, sy: p.y, base: toggle ? [...S.multi] : [], hit, toggle, moved: false };
  if (!marquee.isConnected) wrap.appendChild(marquee);     // on the page wrapper, so it also shows outside the page
  page.setPointerCapture(e.pointerId); e.preventDefault();
}
viewport.addEventListener('pointerdown', e => {
  if (PRINT || S.shotMode || e.button !== 0 || page.contains(e.target) || S.doc.mode === 'flow') return;
  if (e.offsetX > viewport.clientWidth || e.offsetY > viewport.clientHeight) return;   // scrollbars
  if (S.editing) commitEdit();
  if (S.cropping) endCrop();
  startMarquee(e, null, e.shiftKey || e.metaKey || e.ctrlKey);
});
page.addEventListener('pointerdown', e => {
  if (PRINT || S.shotMode) return;
  const h = e.target.closest('.handle');
  const el = e.target.closest('.blk');
  const b = el ? blockById(el.dataset.id) : null;
  const toggle = e.shiftKey || e.metaKey || e.ctrlKey;
  const flow = S.doc.mode === 'flow';
  if (S.editing && (!b || S.editing !== b.id)) commitEdit();
  if (b && S.editing === b.id) return;      // typing inside
  const gh = e.target.closest('#gbox .handle');
  if (gh) {                                 // resize a whole group: members scale with the group box
    const bs = selBlocks(), p0 = pageMM(e);
    drag = { gresize: gh.dataset.h, id: bs[0].id, sx: p0.x, sy: p0.y, bb: bboxOf(bs), moved: false,
      items: bs.map(x => ({ b: x, x: x.x, y: x.y, w: x.w, h: x.h, el: $(`.blk[data-id="${x.id}"]`, page) })) };
    page.setPointerCapture(e.pointerId); e.preventDefault(); return;
  }
  if (S.cropping) {
    if (b && b.id === S.cropping) {         // crop: handles trim, the picture pans under the frame
      const p0 = pageMM(e);
      drag = { crop: h ? h.dataset.h : 'pan', id: b.id, sx: p0.x, sy: p0.y, o: { x: b.x, y: b.y, w: b.w, h: b.h }, c0: Object.assign({ l: 0, t: 0, r: 0, b: 0 }, b.crop), el, moved: false };
      el.setPointerCapture(e.pointerId); e.preventDefault(); return;
    }
    endCrop();
  }
  if (b && e.target.closest('.chips')) { if (!S.multi.has(b.id)) select(b.id); return; }
  // Alt-drag inside a text block selects words (Ask / Translate on a phrase) instead of moving the block
  if (b && b.type === 'text' && e.altKey && e.target.closest('.md')) { if (!S.multi.has(b.id)) select(b.id); return; }
  if (flow) {                              // flow: blocks stack, only images resize; text is selectable
    if (!b) { select(null); hideSelTools(); return; }
    if (toggle && !h) { toggleIds(groupIds(b)); return; }
    if (!S.multi.has(b.id) || h) select(b.id);
    if (!h || b.type !== 'image') return;
  }
  const p = pageMM(e);
  // empty page, or a locked background block (boxes, bars): rubber-band selection
  if (!flow && (!b || (b.locked && !h && !(S.multi.size > 1 && S.multi.has(b.id))))) { startMarquee(e, b ? b.id : null, toggle); return; }
  if (toggle && !h) { toggleIds(groupIds(b)); hideSelTools(); e.preventDefault(); return; }   // add / remove (a grouped block brings its group)
  const inGroup = S.multi.has(b.id) && S.multi.size > 1;
  if (h) select(b.id); else if (!inGroup) { selectMany(groupIds(b)); S.sel = b.id; }
  const el2 = $(`.blk[data-id="${b.id}"]`, page);
  const items = (h ? [b] : selBlocks()).map(x => ({ b: x, x: x.x || 0, y: x.y || 0, el: $(`.blk[data-id="${x.id}"]`, page) }));
  drag = { id: b.id, h: h ? h.dataset.h : null, sx: p.x, sy: p.y, o: { x: b.x || 0, y: b.y || 0, w: b.w || 0, h: b.h || 0 }, items, inGroup, moved: false, aspect: b.type === 'image' ? ((b.w || 1) / (b.h || 1)) : null, el };
  (el2 || el).setPointerCapture(e.pointerId);
  e.preventDefault();
});
page.addEventListener('pointermove', e => {
  if (!drag) return;
  const p = pageMM(e);
  let dx = p.x - drag.sx, dy = p.y - drag.sy;
  if (!drag.moved && Math.hypot(dx, dy) * PX_PER_MM * S.zoom < 3) return;
  if (drag.marquee) {
    drag.moved = true;
    const x = Math.min(p.x, drag.sx), y = Math.min(p.y, drag.sy), w = Math.abs(dx), hh = Math.abs(dy);
    Object.assign(marquee.style, { left: x + 'mm', top: y + 'mm', width: w + 'mm', height: hh + 'mm' }); marquee.hidden = false;
    // every text box, picture and shape mostly inside the rectangle (≥ 60 % of its area: a text box whose frame
    // is a little larger than its text still counts); locked backgrounds (boxes, bars) only when wholly inside
    const share = b => { const ix = Math.max(0, Math.min(b.x + b.w, x + w) - Math.max(b.x, x)), iy = Math.max(0, Math.min(b.y + b.h, y + hh) - Math.max(b.y, y)); return b.w > 0 && b.h > 0 ? ix * iy / (b.w * b.h) : 0; };
    const inside = S.doc.blocks.filter(b => !b.hidden && (b.locked ? share(b) > 0.999 : share(b) >= 0.6)).map(b => b.id);
    const inSet = new Set(inside);
    const whole = inside.filter(id => { const b = blockById(id); return !b.group || S.doc.blocks.every(x => x.group !== b.group || inSet.has(x.id)); });
    selectMany([...new Set([...drag.base, ...whole])]);
    return;
  }
  const b = blockById(drag.id); if (!b) return;
  if (!drag.moved) { pushUndo(); drag.moved = true; hideSelTools(); }
  if (drag.gresize) {
    const o = drag.bb, g = drag.gresize; let x = o.x, y = o.y, w = o.w, hh = o.h;
    if (g.includes('e')) w = o.w + dx; if (g.includes('s')) hh = o.h + dy;
    if (g.includes('w')) { x = o.x + dx; w = o.w - dx; } if (g.includes('n')) { y = o.y + dy; hh = o.h - dy; }
    if (g.length === 2 || e.shiftKey) { if (g === 'n' || g === 's') w = hh * o.w / o.h; else hh = w * o.h / o.w; if (g.includes('n')) y = o.y + o.h - hh; if (g.includes('w')) x = o.x + o.w - w; }
    w = Math.max(2, w); hh = Math.max(2, hh);
    const sx = w / o.w, sy = hh / o.h;
    const free = g.length === 1 && !e.shiftKey;   // edge handle of a group: pictures stretch with it
    for (const it of drag.items) {
      if (free && it.b.type === 'image') stretchImage(it.b, it.el);
      Object.assign(it.b, { x: +(x + (it.x - o.x) * sx).toFixed(2), y: +(y + (it.y - o.y) * sy).toFixed(2), w: +(it.w * sx).toFixed(2), h: +(it.h * sy).toFixed(2) });
      if (it.el) { Object.assign(it.el.style, { left: it.b.x + 'mm', top: it.b.y + 'mm', width: it.b.w + 'mm', height: it.b.h + 'mm' }); if (it.b.type === 'shape') $('.shp', it.el).innerHTML = shapeSVG(it.b); }
    }
    updateGbox(); return;
  }
  if (drag.crop) {
    const b2 = blockById(drag.id), o = drag.o, c0 = drag.c0, Wf = o.w / (1 - c0.l - c0.r), Hf = o.h / (1 - c0.t - c0.b), k = drag.crop;
    const cl = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
    const c = Object.assign({}, c0); let { x, y, w, h: hh } = o;
    if (k === 'pan') {
      c.l = cl(c0.l - dx / Wf, 0, c0.l + c0.r); c.r = c0.l + c0.r - c.l;
      c.t = cl(c0.t - dy / Hf, 0, c0.t + c0.b); c.b = c0.t + c0.b - c.t;
    } else {
      if (k.includes('e')) { c.r = cl(c0.r - dx / Wf, 0, 1 - c.l - 0.02); w = Wf * (1 - c.l - c.r); }
      if (k.includes('w')) { c.l = cl(c0.l + dx / Wf, 0, 1 - c.r - 0.02); w = Wf * (1 - c.l - c.r); x = o.x + (c.l - c0.l) * Wf; }
      if (k.includes('s')) { c.b = cl(c0.b - dy / Hf, 0, 1 - c.t - 0.02); hh = Hf * (1 - c.t - c.b); }
      if (k.includes('n')) { c.t = cl(c0.t + dy / Hf, 0, 1 - c.b - 0.02); hh = Hf * (1 - c.t - c.b); y = o.y + (c.t - c0.t) * Hf; }
    }
    for (const q of ['l', 't', 'r', 'b']) c[q] = +c[q].toFixed(4);
    Object.assign(b2, { crop: c, x: +x.toFixed(2), y: +y.toFixed(2), w: +w.toFixed(2), h: +hh.toFixed(2) });
    Object.assign(drag.el.style, { left: b2.x + 'mm', top: b2.y + 'mm', width: b2.w + 'mm', height: b2.h + 'mm' });
    applyCrop(drag.el, b2); updateDim(drag.el, b2); return;
  }
  const snap = v => S.snap ? round(v, 1) : round(v, 0.1);
  const o = drag.o, flow = S.doc.mode === 'flow';
  if (!drag.h) {
    // move the primary block with snapping, the rest of the group by the same offset
    const ddx = snap(o.x + dx) - o.x, ddy = snap(o.y + dy) - o.y;
    for (const it of drag.items) {
      it.b.x = +(it.x + ddx).toFixed(2); it.b.y = +(it.y + ddy).toFixed(2);
      if (it.el) { it.el.style.left = it.b.x + 'mm'; it.el.style.top = it.b.y + 'mm'; updateDim(it.el, it.b); }
    }
    updateGbox(); return;
  }
  const h = drag.h; let x = o.x, y = o.y, w = o.w, hh = o.h;
  if (h.includes('e')) w = o.w + dx; if (h.includes('s')) hh = o.h + dy;
  if (h.includes('w')) { x = o.x + dx; w = o.w - dx; } if (h.includes('n')) { y = o.y + dy; hh = o.h - dy; }
  if (drag.aspect && (e.shiftKey || h.length === 2 || flow)) { if (h === 'n' || h === 's') w = hh * drag.aspect; else hh = w / drag.aspect; if (h.includes('n')) y = o.y + o.h - hh; if (h.includes('w')) x = o.x + o.w - w; }
  b.w = Math.max(2, snap(w)); b.h = Math.max(2, snap(hh)); if (!flow) { b.x = snap(x); b.y = snap(y); }
  const el = drag.el;
  if (b.type === 'image' && h.length === 1 && !e.shiftKey && !flow) stretchImage(b, el);   // edge handle: free (non-proportional) stretch
  if (!flow) { el.style.left = b.x + 'mm'; el.style.top = b.y + 'mm'; el.style.height = b.h + 'mm'; } else if (b.type === 'image') el.style.height = b.h + 'mm';
  el.style.width = b.w + 'mm';
  if (b.type === 'shape') $('.shp', el).innerHTML = shapeSVG(b);
  updateDim(el, b);
});
page.addEventListener('pointerup', e => {
  if (!drag) return;
  const d = drag; drag = null;
  if (d.marquee) {
    marquee.hidden = true;
    if (!d.moved) { if (d.hit) { select(d.hit, d.toggle); if (S.multi.size === 1) showSelToolsForBlock($(`.blk[data-id="${d.hit}"]`, page)); } else if (!d.toggle) select(null); }
    else if (S.multi.size > 1) showSelToolsForGroup();
    else if (S.multi.size === 1) showSelToolsForBlock($(`.blk[data-id="${S.sel}"]`, page));
    return;
  }
  if (d.gresize || d.crop) { if (d.moved) markDirty((d.crop ? 'crop ' : 'resize group ') + d.id); return; }
  if (d.moved) { markDirty(d.items.length > 1 && !d.h ? `move ${d.items.length} blocks` : 'move/resize ' + d.id); if (S.multi.size > 1) showSelToolsForGroup(); return; }
  if (S.shotMode) return;
  if (d.inGroup) select(d.id);              // plain click on a selected group / member: just that block
  if (S.multi.size > 1) { showSelToolsForGroup(); return; }
  const sel = window.getSelection(); if (!sel || sel.isCollapsed || !page.contains(sel.anchorNode)) showSelToolsForBlock(d.el);
});
window.addEventListener('keydown', e => { if (e.key === 'Alt') document.body.classList.add('alt'); });
window.addEventListener('keyup', e => { if (e.key === 'Alt') document.body.classList.remove('alt'); });
window.addEventListener('blur', () => document.body.classList.remove('alt'));
page.addEventListener('dblclick', e => {
  if (PRINT) return;
  const el = e.target.closest('.blk'); if (!el) return;
  if (el.classList.contains('text')) startEdit(el.dataset.id);
  else if (el.classList.contains('image') && !S.cropping) startCrop(el.dataset.id);
});

// ---------- text editing (markdown source in place)
function editEl() { return S.editing ? $(`.blk[data-id="${S.editing}"] .md`, page) : null; }
function startEdit(id, opts = {}) {
  if (S.editing) commitEdit();
  const b = blockById(id), el = $(`.blk[data-id="${id}"]`, page); if (!b || !el || b.type !== 'text') return;
  S.editing = id; hideSelTools();
  const m = $('.md', el);
  S.editStart = m.innerHTML;
  if (!m.innerHTML.trim()) m.innerHTML = '<div><br></div>';
  m.contentEditable = 'true'; m.spellcheck = false; el.classList.add('editing');
  m.focus();
  const r = document.createRange(); r.selectNodeContents(m); if (!opts.all) r.collapse(false);
  const sl = getSelection(); sl.removeAllRanges(); sl.addRange(r); S.editRange = r.cloneRange();
  m.onkeydown = ev => {
    if (ev.key === 'Escape') { ev.preventDefault(); commitEdit(); }
    else if (ev.key === 'Tab') { ev.preventDefault(); document.execCommand(ev.shiftKey ? 'outdent' : 'indent'); }
    ev.stopPropagation();
  };
  m.onblur = () => setTimeout(() => { const ae = document.activeElement; if (S.editing === id && !(ae && ae.closest('#topbar'))) commitEdit(); }, 80);
  document.dispatchEvent(new CustomEvent('folio:selection'));
}
function commitEdit() {
  const id = S.editing; if (!id) return;
  const el = $(`.blk[data-id="${id}"]`, page), b = blockById(id);
  S.editing = null; S.editRange = null;
  if (!el || !b) return;
  const m = $('.md', el); m.contentEditable = 'false'; m.onkeydown = m.onblur = null; el.classList.remove('editing');
  if (m.innerHTML !== S.editStart) {
    pushUndo();
    const html = cleanHTML(m.innerHTML);
    b.html = html; b.text = htmlToMd(html);
    m.innerHTML = html; markDirty('text ' + id);
  }
  const sl = getSelection(); if (sl && page.contains(sl.anchorNode)) sl.removeAllRanges();
  document.dispatchEvent(new CustomEvent('folio:selection'));
}
// keep the caret / selection of the box being edited, so ribbon pickers can act on it
document.addEventListener('selectionchange', () => {
  const m = editEl(); const sl = getSelection();
  if (m && sl.rangeCount && m.contains(sl.anchorNode)) { S.editRange = sl.getRangeAt(0).cloneRange(); document.dispatchEvent(new CustomEvent('folio:selection')); }
});

// ---------- keyboard
document.addEventListener('keydown', e => {
  if (PRINT) return;
  const a = document.activeElement;   // a focused button / slider / checkbox is not a typing field: keys still drive the canvas
  const inField = (a.tagName === 'INPUT' && !/^(range|checkbox|radio|button|color|file)$/.test(a.type)) || /^(TEXTAREA|SELECT)$/.test(a.tagName) || a.isContentEditable;
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'z') { if (inField) return; e.preventDefault(); e.shiftKey ? redo() : undo(); return; }
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 's') { e.preventDefault(); S.dirty = true; save('manual'); return; }
  if (inField) return;
  if (S.shotMode) { if (e.key === 'Escape') endShot(); if (e.key.toLowerCase() === 'a') { shoot(null); } return; }
  if (S.cropping && (e.key === 'Escape' || e.key === 'Enter')) { e.preventDefault(); endCrop(); return; }
  if (e.key === 'Escape') { select(null); hideSelTools(); closeAsk(); return; }
  if (e.key.toLowerCase() === 's' && !e.metaKey) { startShot(); return; }
  if (e.key.toLowerCase() === 't' && !e.metaKey) { addText(); return; }
  if (e.key.toLowerCase() === 'i' && !e.metaKey) { $('#fileInput').click(); return; }
  if (e.key === '0' && !e.metaKey) { fit(); return; }
  if ((e.key === '+' || e.key === '=' || e.key === '-') && !e.metaKey && !e.ctrlKey) { e.preventDefault(); zoomStep(e.key === '-' ? -1 : 1); return; }
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'a') { e.preventDefault(); selectMany(S.doc.blocks.filter(x => !x.locked && !x.hidden).map(x => x.id)); if (S.multi.size > 1) showSelToolsForGroup(); return; }
  if (!S.sel) return;
  const b = blockById(S.sel); if (!b) return;
  const bs = selBlocks(), what = bs.length > 1 ? `${bs.length} blocks` : b.id;
  if (e.key === 'Enter' && b.type === 'text' && bs.length === 1) { e.preventDefault(); startEdit(b.id); return; }
  if (e.key === 'Delete' || e.key === 'Backspace') { pushUndo(); S.doc.blocks = S.doc.blocks.filter(x => !S.multi.has(x.id)); select(null); hideSelTools(); render(); markDirty('delete ' + what); return; }
  if (e.key.startsWith('Arrow') && S.doc.mode !== 'flow') {
    e.preventDefault(); if (a !== document.body && !page.contains(a)) a.blur(); const st = e.shiftKey ? 5 : (e.altKey ? 0.1 : 0.5);
    pushUndo();
    for (const x of bs) {
      if (e.key === 'ArrowLeft') x.x -= st; if (e.key === 'ArrowRight') x.x += st; if (e.key === 'ArrowUp') x.y -= st; if (e.key === 'ArrowDown') x.y += st;
      x.x = +x.x.toFixed(2); x.y = +x.y.toFixed(2);
      const el = $(`.blk[data-id="${x.id}"]`, page); if (el) { el.style.left = x.x + 'mm'; el.style.top = x.y + 'mm'; updateDim(el, x); }
    }
    markDirty('nudge ' + what); updateGbox();
  }
  if (e.key === '[' || e.key === ']') { pushUndo(); for (const x of bs) x.z = (x.z || 0) + (e.key === ']' ? 1 : -1); render(); markDirty('z ' + what); }
  if (e.key.toLowerCase() === 'l' && !e.metaKey && !e.ctrlKey) { pushUndo(); const lock = !bs.every(x => x.locked); for (const x of bs) { if (lock) x.locked = true; else delete x.locked; } render(); markDirty((lock ? 'lock ' : 'unlock ') + what); toast((lock ? 'Locked ' : 'Unlocked ') + what); }
});

// ---------- add blocks
function addText() {
  pushUndo();
  const flow = S.doc.mode === 'flow';
  const b = { id: uid('t'), type: 'text', text: 'New text', pt: (S.doc.style && S.doc.style.text_pt) || 8 };
  if (!flow) Object.assign(b, { x: 10, y: 10, w: 50, h: 12 });
  S.doc.blocks.push(b); render(); select(b.id); markDirty('add text'); startEdit(b.id, { all: true });
}
$('#fileInput').onchange = async e => { for (const f of e.target.files) await addImageFile(f); e.target.value = ''; };
async function addImageFile(f, at) {
  const data = await readFile(f);
  const r = await api(`/api/folio/${S.fid}/upload`, { name: f.name, data });
  const dim = await imgSize(data).catch(() => ({ w: 4, h: 3 }));
  pushUndo();
  const flow = S.doc.mode === 'flow';
  const w = flow ? Math.min(120, (S.doc.page.w_mm || 180) - 2 * (S.doc.page.margin_mm ?? 15)) : 60;
  const b = { id: uid('img'), type: 'image', src: r.src, w, h: +(w * dim.h / dim.w).toFixed(1) };
  if (!flow) { b.x = at ? at.x : 10; b.y = at ? at.y : 10; }
  S.doc.blocks.push(b); render(); select(b.id); markDirty('add image');
}
const readFile = f => new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(r.result); r.onerror = rej; r.readAsDataURL(f); });
const imgSize = src => new Promise((res, rej) => { const i = new Image(); i.onload = () => res({ w: i.naturalWidth, h: i.naturalHeight }); i.onerror = rej; i.src = src; });
// paste / drop images onto the page (not into the Ask box)
document.addEventListener('paste', e => {
  if ($('#askBox').contains(document.activeElement) || !$('#askBox').hidden) return;
  if (/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) return;
  const items = [...(e.clipboardData?.items || [])].filter(i => i.type.startsWith('image/'));
  if (items.length) { e.preventDefault(); items.forEach(i => addImageFile(i.getAsFile())); }
});
viewport.addEventListener('dragover', e => { if (!$('#askBox').contains(e.target)) e.preventDefault(); });
viewport.addEventListener('drop', e => { if ($('#askBox').contains(e.target)) return; e.preventDefault(); const p = pageMM(e); [...e.dataTransfer.files].filter(f => f.type.startsWith('image/')).forEach(f => addImageFile(f, p)); });

// ---------- selection tools (✳ Ask/Edit, 文 Translate)
const selTools = $('#selTools');
function hideSelTools() { selTools.hidden = true; }
function showSelToolsAt(x, y) { selTools.hidden = false; selTools.style.left = Math.min(window.innerWidth - 90, x) + 'px'; selTools.style.top = Math.max($('#topbar').offsetHeight + 6, y - 38) + 'px'; }
function showSelToolsForBlock(el) {
  const b = blockById(el.dataset.id); const r = el.getBoundingClientRect();
  S.range = null;
  S.anchor = { block: b.id, type: b.type, quote: b.type === 'text' ? (b.text || '').slice(0, 300) : '', label: b.id, bbox: { x: b.x, y: b.y, w: b.w, h: b.h } };
  showSelToolsAt(r.left + r.width / 2 - 30, r.top);
}
function showSelToolsForGroup() {
  const bs = selBlocks(); if (!bs.length) return;
  const x0 = Math.min(...bs.map(b => b.x)), y0 = Math.min(...bs.map(b => b.y));
  const x1 = Math.max(...bs.map(b => b.x + b.w)), y1 = Math.max(...bs.map(b => b.y + b.h));
  S.range = null;
  S.anchor = { block: S.sel, blocks: bs.map(b => b.id), type: 'group', label: `${bs.length} blocks`,
    quote: bs.filter(b => b.type === 'text').map(b => b.text || '').join(' | ').slice(0, 300),
    bbox: { x: +x0.toFixed(1), y: +y0.toFixed(1), w: +(x1 - x0).toFixed(1), h: +(y1 - y0).toFixed(1) } };
  const pr = page.getBoundingClientRect(), k = PX_PER_MM * S.zoom;
  showSelToolsAt(pr.left + ((x0 + x1) / 2) * k - 30, pr.top + y0 * k);
}
document.addEventListener('selectionchange', () => {
  if (PRINT) return;
  const sel = window.getSelection();
  if (!sel || sel.isCollapsed || !sel.rangeCount) return;
  const rng = sel.getRangeAt(0);
  if (!page.contains(rng.commonAncestorContainer)) return;
  if (S.editing) return;
  const text = sel.toString().trim(); if (!text) return;
  const el = rng.commonAncestorContainer.nodeType === 1 ? rng.commonAncestorContainer.closest('.blk') : rng.commonAncestorContainer.parentElement.closest('.blk');
  if (!el) return;
  const b = blockById(el.dataset.id);
  S.anchor = { block: b.id, type: 'text', quote: text, label: b.id, bbox: { x: b.x, y: b.y, w: b.w, h: b.h } };
  S.range = rng.cloneRange();
  const r = rng.getBoundingClientRect();
  showSelToolsAt(r.left + r.width / 2 - 30, r.top);
});
$('#askBtn').onclick = () => { highlightAnchor(); openAsk(); hideSelTools(); };
$('#trBtn').onclick = () => { translateSel(); hideSelTools(); };
function highlightAnchor() {
  clearHighlight();
  if (S.range && CSS.highlights) { CSS.highlights.set('folio-sel', new Highlight(S.range)); }
  else if (S.anchor) { const el = $(`.blk[data-id="${S.anchor.block}"]`, page); el && el.classList.add('hl'); }
}
function clearHighlight() { CSS.highlights && CSS.highlights.delete('folio-sel'); $$('.blk.hl', page).forEach(el => el.classList.remove('hl')); }

// ---------- Ask / Edit box
const askBox = $('#askBox');
const PRESETS = {
  ask: ['Explain simply', 'What does it mean biologically?', 'Can I trust this?', 'What do other studies show?', 'Write it as a paper sentence', 'Is this layout clear?'],
  edit: ['Fix text', 'Shorten to N words', 'Align panels', 'Resize to fit', 'Redo figure', 'Add citations', 'Move / remove']
};
function openAsk(opts = {}) {
  askBox.hidden = false;
  if (!askBox.style.left) { askBox.style.left = Math.max(10, window.innerWidth - 460) + 'px'; askBox.style.top = ($('#topbar').offsetHeight + 12) + 'px'; }
  setTab(opts.tab || S.tab);
  const a = S.anchor;
  $('#askAnchor').textContent = a ? `Selected · ${a.blocks ? a.blocks.length + ' blocks (' + a.blocks.slice(0, 4).join(', ') + (a.blocks.length > 4 ? ', …' : '') + ')' : a.block}${a.quote ? ' · “' + a.quote.slice(0, 80).replace(/\s+/g, ' ') + (a.quote.length > 80 ? '…' : '') + '”' : ''}` : 'Whole folio';
  if (opts.image) addAskImage(opts.image, opts.imageName);
  if (opts.text) $('#askText').value = opts.text;
  setTimeout(() => $('#askText').focus(), 30);
}
function closeAsk() { askBox.hidden = true; clearHighlight(); }
$('#askClose').onclick = closeAsk;
function setTab(t) { S.tab = t; $$('#askHead .tab').forEach(b => b.classList.toggle('on', b.dataset.tab === t)); $('#askScope').hidden = t !== 'edit'; $('#askPresets').innerHTML = PRESETS[t].map(p => `<button data-p="${esc(p)}">${esc(p)}</button>`).join(''); $$('#askPresets button').forEach(b => b.onclick = () => { const ta = $('#askText'); ta.value = (ta.value ? ta.value + '\n' : '') + b.dataset.p + (b.dataset.p.endsWith('?') ? '' : ': '); ta.focus(); }); }
$$('#askHead .tab').forEach(b => b.onclick = () => setTab(b.dataset.tab));
// drag the box by its header
(function () { let d = null; const h = $('#askHead'); h.addEventListener('pointerdown', e => { if (e.target.tagName === 'BUTTON') return; d = { x: e.clientX - askBox.offsetLeft, y: e.clientY - askBox.offsetTop }; h.setPointerCapture(e.pointerId); }); h.addEventListener('pointermove', e => { if (!d) return; askBox.style.left = Math.max(0, e.clientX - d.x) + 'px'; askBox.style.top = Math.max($('#topbar').offsetHeight, e.clientY - d.y) + 'px'; }); h.addEventListener('pointerup', () => d = null); })();
// images in the box
function addAskImage(dataUrl, name) {
  if (S.images.length >= 8) return toast('At most 8 images per request');
  downscale(dataUrl, 2000).then(d => { S.images.push({ data: d, name: name || 'image' }); renderAskImages(); });
}
function renderAskImages() { $('#askImages').innerHTML = S.images.map((im, i) => `<div class="im"><img src="${im.data}" title="${esc(im.name)}"><span class="x" data-i="${i}">✕</span></div>`).join(''); $$('#askImages .x').forEach(x => x.onclick = () => { S.images.splice(+x.dataset.i, 1); renderAskImages(); }); }
function downscale(dataUrl, max) {
  return new Promise(res => { const i = new Image(); i.onload = () => { const s = Math.min(1, max / Math.max(i.width, i.height)); if (s >= 1) return res(dataUrl); const c = document.createElement('canvas'); c.width = i.width * s; c.height = i.height * s; c.getContext('2d').drawImage(i, 0, 0, c.width, c.height); res(c.toDataURL(dataUrl.startsWith('data:image/png') ? 'image/png' : 'image/jpeg', 0.9)); }; i.onerror = () => res(dataUrl); i.src = dataUrl; });
}
$('#askAttach').onclick = () => $('#askFile').click();
$('#askFile').onchange = async e => { for (const f of e.target.files) addAskImage(await readFile(f), f.name); e.target.value = ''; };
$('#askText').addEventListener('paste', async e => { const items = [...(e.clipboardData?.items || [])].filter(i => i.type.startsWith('image/')); if (!items.length) return; e.preventDefault(); for (const it of items) { const f = it.getAsFile(); addAskImage(await readFile(f), f.name || 'pasted.png'); } });
askBox.addEventListener('dragover', e => { e.preventDefault(); e.stopPropagation(); askBox.classList.add('drag'); });
askBox.addEventListener('dragleave', e => { if (!askBox.contains(e.relatedTarget)) askBox.classList.remove('drag'); });
askBox.addEventListener('drop', async e => {
  e.preventDefault(); e.stopPropagation(); askBox.classList.remove('drag');
  for (const f of [...e.dataTransfer.files].filter(f => f.type.startsWith('image/'))) addAskImage(await readFile(f), f.name);
  const url = e.dataTransfer.getData('text/uri-list') || e.dataTransfer.getData('text/plain');
  if (url && /^https?:|^data:image/.test(url) && !e.dataTransfer.files.length) { try { const b = await (await fetch(url)).blob(); addAskImage(await readFile(b), 'dropped'); } catch {} }
});
// drag a page image into the box: make img draggable with its src
page.addEventListener('dragstart', e => { const img = e.target.closest('.blk.image img'); if (img) e.dataTransfer.setData('text/uri-list', img.src); });
$('#askSend').onclick = async () => {
  const text = $('#askText').value.trim();
  if (!text && !S.images.length) return toast('Write a question or attach an image');
  const req = { folio: S.fid, type: S.tab, text, anchor: S.anchor, images: S.images, confirm: $('#askConfirm').checked, page_hash: S.hash };
  try {
    const r = await api('/api/request', req);
    toast(`Sent to Claude (${r.id}). Answers arrive in Threads.`);
    $('#askText').value = ''; S.images = []; renderAskImages(); closeAsk(); openSide('threads'); await loadReview();
  } catch (e) { toast('Send failed: ' + e.message); }
};

// ---------- Translate
const LANGS = [['zh-Hans', '中文（简体）'], ['zh-Hant', '中文（繁體）'], ['en', 'English'], ['ja', '日本語'], ['ko', '한국어'], ['es', 'Español'], ['fr', 'Français'], ['de', 'Deutsch'], ['pt', 'Português'], ['it', 'Italiano'], ['ru', 'Русский'], ['ar', 'العربية'], ['hi', 'हिन्दी'], ['vi', 'Tiếng Việt'], ['th', 'ไทย'], ['tr', 'Türkçe'], ['nl', 'Nederlands'], ['pl', 'Polski'], ['sv', 'Svenska'], ['id', 'Bahasa Indonesia']];
$('#trLang').innerHTML = LANGS.map(([c, n]) => `<option value="${c}">${n}</option>`).join('');
$('#trLang').value = LS.get('translateTo', 'zh-Hans');
$('#trLang').onchange = () => { LS.set('translateTo', $('#trLang').value); translateSel(S.trText); };
$('#trClose').onclick = () => $('#trPop').hidden = true;
async function translateSel(text) {
  text = text || (S.anchor && S.anchor.quote) || ''; if (!text) return;
  S.trText = text; const pop = $('#trPop'); pop.hidden = false;
  if (!pop.style.left) { pop.style.left = Math.max(10, (selTools.offsetLeft || 200)) + 'px'; pop.style.top = (parseInt(selTools.style.top) || 100) + 40 + 'px'; }
  $('#trSrc').textContent = text; $('#trOut').textContent = '…';
  try { const r = await api('/api/translate', { text, target: $('#trLang').value }); $('#trOut').textContent = r.ok ? r.translation : (r.error === 'unavailable' ? 'Claude CLI not available on this machine — ask this session instead (✳ Ask).' : 'Error: ' + r.error); }
  catch (e) { $('#trOut').textContent = 'Error: ' + e.message; }
}
(function () { let d = null; const h = $('.trHead'), pop = $('#trPop'); h.addEventListener('pointerdown', e => { if (/BUTTON|SELECT/.test(e.target.tagName)) return; d = { x: e.clientX - pop.offsetLeft, y: e.clientY - pop.offsetTop }; h.setPointerCapture(e.pointerId); }); h.addEventListener('pointermove', e => { if (d) { pop.style.left = e.clientX - d.x + 'px'; pop.style.top = e.clientY - d.y + 'px'; } }); h.addEventListener('pointerup', () => d = null); })();

// ---------- Screenshot (region → server render → Ask box)
const shotLayer = $('#shotLayer'), shotRect = $('#shotRect');
function startShot() { if (S.editing) commitEdit(); S.shotMode = true; shotLayer.hidden = false; shotRect.style.display = 'none'; hideSelTools(); $('#btnShot').classList.add('on'); }
function endShot() { S.shotMode = false; shotLayer.hidden = true; shotRect.style.display = 'none'; $('#btnShot').classList.remove('on'); }
$('#btnShot').onclick = () => S.shotMode ? endShot() : startShot();
let shotDrag = null;
shotLayer.addEventListener('pointerdown', e => { const p = pageMM(e); shotDrag = { x: p.x, y: p.y }; shotRect.style.display = 'block'; setRect(p, p); shotLayer.setPointerCapture(e.pointerId); });
shotLayer.addEventListener('pointermove', e => { if (shotDrag) setRect(shotDrag, pageMM(e)); });
shotLayer.addEventListener('pointerup', e => { if (!shotDrag) return; const p = pageMM(e); const r = norm(shotDrag, p); shotDrag = null; if (r.w < 2 || r.h < 2) { shotRect.style.display = 'none'; return; } shoot(r); });
function norm(a, b) { return { x: +Math.min(a.x, b.x).toFixed(1), y: +Math.min(a.y, b.y).toFixed(1), w: +Math.abs(a.x - b.x).toFixed(1), h: +Math.abs(a.y - b.y).toFixed(1) }; }
function setRect(a, b) { const r = norm(a, b); shotRect.style.left = r.x + 'mm'; shotRect.style.top = r.y + 'mm'; shotRect.style.width = r.w + 'mm'; shotRect.style.height = r.h + 'mm'; }
async function shoot(region) {
  toast('Rendering screenshot…', 4000);
  let r;
  try { r = await api(`/api/folio/${S.fid}/screenshot`, { region }); } catch (e) { endShot(); return toast('Screenshot failed: ' + e.message); }
  if (!r.ok && r.error === 'playwright-missing') {       // client-side fallback
    const data = await clientRender(region);
    r = await api(`/api/folio/${S.fid}/screenshot`, { region, data });
    r.renderer = 'client';
  }
  endShot();
  if (!r.ok) return toast('Screenshot failed: ' + r.error);
  S.anchor = { block: r.blocks[0] || null, blocks: r.blocks, type: 'screenshot', quote: '', label: 'screenshot', region: r.region, file: r.file };
  openAsk({ image: r.data, imageName: r.file, text: '' });
  $('#askAnchor').textContent = `Screenshot · ${region ? `${region.w}×${region.h} mm at ${region.x},${region.y}` : 'whole page'} · blocks: ${r.blocks.join(', ') || 'none'} · saved ${r.file}`;
  toast(`Screenshot attached (${r.renderer} render). Describe what to change.`);
}
async function clientRender(region) {   // draws images + plain text only; used when Playwright is missing on this machine
  const pg = S.doc.page || {}; const reg = region || { x: 0, y: 0, w: pg.w_mm || 180, h: pg.h_mm || 120 };
  const sc = 4; const c = document.createElement('canvas'); c.width = reg.w * sc; c.height = reg.h * sc; const g = c.getContext('2d');
  g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height); g.translate(-reg.x * sc, -reg.y * sc);
  for (const b of S.doc.blocks) {
    if (b.hidden) continue;
    if (b.type === 'image') { const img = $(`.blk[data-id="${b.id}"] img`, page); if (img && img.complete) { const ar = img.naturalWidth / img.naturalHeight, bw = b.w, bh = b.h; let w = bw, h = bw / ar; if (h > bh) { h = bh; w = bh * ar; } g.drawImage(img, (b.x + (bw - w) / 2) * sc, (b.y + (bh - h) / 2) * sc, w * sc, h * sc); } }
    else { g.fillStyle = b.color || '#000'; const pt = b.pt || 8; g.font = `${(b.text || '').startsWith('**') ? 'bold ' : ''}${pt / 72 * 25.4 * sc}px Arial`; const lines = String(b.text || '').replace(/[*_`]/g, '').split('\n'); let y = b.y + pt / 72 * 25.4; for (const ln of lines) { g.fillText(ln, b.x * sc, y * sc, b.w * sc); y += pt / 72 * 25.4 * 1.3; } }
  }
  return c.toDataURL('image/png');
}

// ---------- side panel: threads & notes
async function loadReview() { S.review = await api(`/api/folio/${S.fid}/review`); decorate(); if (S.side) renderSide(); }
function openSide(which) { S.side = which; $('#side').hidden = false; $('#btnThreads').classList.toggle('on', which === 'threads'); $('#btnNotes').classList.toggle('on', which === 'notes'); $('#sideTitle').textContent = which === 'threads' ? 'Threads' : 'Notes'; renderSide(); }
function closeSide() { S.side = null; $('#side').hidden = true; $('#btnThreads').classList.remove('on'); $('#btnNotes').classList.remove('on'); }
$('#btnThreads').onclick = () => S.side === 'threads' ? closeSide() : openSide('threads');
$('#btnNotes').onclick = () => S.side === 'notes' ? closeSide() : openSide('notes');
$('#sideClose').onclick = closeSide;
$('#sideExpand').onclick = () => $$('#sideBody details').forEach(d => d.open = true);
$('#sideCollapse').onclick = () => $$('#sideBody details').forEach(d => d.open = false);
const openState = {};
function renderSide() {
  const body = $('#sideBody');
  if (S.side === 'threads') {
    const ts = [...S.review.threads].reverse();
    body.innerHTML = ts.length ? ts.map(t => {
      const r = t.request, a = r.anchor || {};
      const imgs = (r.attachments || []).map(p => `<img src="/review/${S.fid}/${p}?t=${TOKEN}" onclick="window.open(this.src)">`).join('');
      return `<details class="thread" data-k="${t.id}" ${openState[t.id] ?? t.status !== 'done' ? 'open' : ''}>
        <summary><span class="st ${t.status}">${esc(t.status)}</span><b>${r.type === 'edit' ? 'Edit' : 'Ask'}</b> <span class="muted">${esc(r.time.slice(5, 16).replace('T', ' '))}</span> <span class="muted">${esc(a.block || '')}</span></summary>
        <div class="body">${a.quote ? `<div class="quote">${esc(a.quote)}</div>` : ''}<div class="q">${r.type === 'edit' ? 'Edit' : 'Q'}: ${esc(r.text)}</div>${imgs ? `<div class="thumbs">${imgs}</div>` : ''}
        ${t.answers.map(x => `<div class="q">A <span class="muted">${esc(x.time.slice(11, 16))}</span></div><div class="ans">${mdTable(x.text)}</div>${x.changed && x.changed.length ? `<div class="muted">Changed: ${esc(x.changed.join(', '))}</div>` : ''}`).join('')}
        ${t.status !== 'done' ? '<div class="muted">Waiting for the Claude session in the terminal…</div>' : ''}
        </div></details>`;
    }).join('') : '<div class="muted">No conversations yet. Select text or a block and click ✳.</div>';
  } else {
    const ns = S.review.notes.filter(n => !n.hidden).reverse();
    body.innerHTML = ns.length ? ns.map(n => `<div class="noteItem" data-id="${n.id}">
      <div class="meta"><span>${n.kind === 'edit' ? '✎ Edit' : '💬 Note'}</span><span>${esc(n.time.slice(5, 16).replace('T', ' '))}</span><span>${esc(n.block || '')}</span><span class="grow"></span><button class="mini ed">✎</button><button class="mini del">🗑</button></div>
      ${n.quote ? `<div class="quote">${esc(n.quote)}</div>` : ''}<div class="q">${esc(n.request)}</div><div class="ans">${mdTable(n.answer)}</div></div>`).join('') : '<div class="muted">No notes yet. Every answered Ask / Edit becomes a note on its block.</div>';
    $$('.noteItem', body).forEach(el => {
      const n = S.review.notes.find(x => x.id === el.dataset.id);
      $('.del', el).onclick = async () => { if (!el._c) { el._c = true; $('.del', el).textContent = 'confirm?'; return; } await api(`/api/folio/${S.fid}/notes/delete`, { id: n.id }); loadReview(); };
      $('.ed', el).onclick = () => { el.innerHTML = `<textarea class="rq">${esc(n.request)}</textarea><textarea class="an">${esc(n.answer)}</textarea><div><button class="mini sv">Save</button> <button class="mini cx">Cancel</button></div>`; $('.sv', el).onclick = async () => { await api(`/api/folio/${S.fid}/notes/update`, { id: n.id, request: $('.rq', el).value, answer: $('.an', el).value }); loadReview(); }; $('.cx', el).onclick = renderSide; };
    });
  }
  $$('details.thread', body).forEach(d => d.addEventListener('toggle', () => openState[d.dataset.k] = d.open));
}
function showNotes(blockId, at) {
  const pop = $('#notePop'); const ns = S.review.notes.filter(n => !n.hidden && n.block === blockId);
  pop.innerHTML = `<div style="display:flex;align-items:center"><b>Notes · ${esc(blockId)}</b><span class="grow"></span><button class="mini" id="npClose">✕</button></div>` + ns.map(n => `<div class="sug">${n.quote ? `<div class="quote">${esc(n.quote)}</div>` : ''}<div class="q">${esc(n.request)}</div><div class="ans">${mdTable(n.answer)}</div></div>`).join('');
  place(pop, at); $('#npClose').onclick = () => pop.hidden = true;
}
function showSuggestions(blockId, at) {
  const pop = $('#sugPop'); const ss = S.review.suggestions.filter(s => s.status === 'pending' && (blockId ? s.block === blockId : s.op === 'add'));
  pop.innerHTML = `<div style="display:flex;align-items:center"><b>Claude suggests · ${esc(blockId || 'new blocks')}</b><span class="grow"></span><button class="mini" id="spClose">✕</button></div>` + ss.map(s => {
    let body = '';
    if (s.op === 'delete') body = '<div class="old">Remove this block</div>';
    else if (s.op === 'add') body = `<div class="new">Add ${esc(s.new.type)} block ${esc(s.new.id)}${s.new.text ? ': ' + esc(s.new.text.slice(0, 200)) : ''}</div>`;
    else { const b = blockById(s.block) || {}; for (const [k, v] of Object.entries(s.new || {})) { if (k === 'text') body += `<div class="old">${esc(b.text || '')}</div><div class="new">${esc(v)}</div>`; else body += `<div class="geo">${esc(k)}: ${esc(JSON.stringify(b[k]))} → <b>${esc(JSON.stringify(v))}</b></div>`; } }
    return `<div class="sug">${s.why ? `<div class="muted">${esc(s.why)}</div>` : ''}${body}<div class="acts"><button class="mini primary" data-a="accept" data-id="${s.id}">Accept</button><button class="mini" data-a="reject" data-id="${s.id}">Reject</button></div></div>`;
  }).join('');
  place(pop, at); $('#spClose').onclick = () => pop.hidden = true;
  $$('button[data-a]', pop).forEach(b => b.onclick = async () => { await api(`/api/folio/${S.fid}/suggestion/${b.dataset.id}/${b.dataset.a}`, {}); pop.hidden = true; });
}
function place(pop, at) { pop.hidden = false; const r = at.getBoundingClientRect(); pop.style.left = Math.min(window.innerWidth - 380, r.left) + 'px'; pop.style.top = Math.min(window.innerHeight - 300, r.bottom + 6) + 'px'; }
document.addEventListener('pointerdown', e => { if (!selTools.contains(e.target) && !page.contains(e.target)) hideSelTools(); for (const id of ['#sugPop', '#notePop']) { const p = $(id); if (!p.hidden && !p.contains(e.target) && !e.target.closest('.chip')) p.hidden = true; } });

// ---------- versions / export / grid / snap
async function loadVersions() {
  const vs = await api(`/api/folio/${S.fid}/versions`).catch(() => []);
  $('#versions').innerHTML = '<option value="">Versions (' + vs.length + ') · one per 5 changes</option>' + vs.slice().reverse().map(v => `<option value="${esc(v)}">${esc(v.replace('__folio.json', '').replace('_', ' '))}</option>`).join('');
}
$('#versions').onchange = async e => {
  const v = e.target.value; if (!v) return;
  const doc = await api(`/api/folio/${S.fid}/version/${v}`);
  if (confirm(`Restore version ${v}? The current state is archived first.`)) { pushUndo(); S.doc.blocks = doc.blocks; S.doc.page = doc.page || S.doc.page; render(); S.archiveFirst = true; markDirty('restore ' + v); }
  e.target.value = '';
};
$('#btnExport').onclick = async () => {
  toast('Exporting PDF…', 5000);
  try { const r = await api(`/api/folio/${S.fid}/export`, { format: 'pdf' }); if (r.ok) toast('Exported: ' + r.path, 6000); else if (r.error === 'playwright-missing') { toast(r.setup === 'installing' ? 'The PDF engine (Playwright) is still downloading — using the browser print dialog this time' : 'Playwright missing (run: folio setup) — using the browser print dialog', 6000); window.print(); } else toast('Export failed: ' + r.error); }
  catch (e) { toast('Export failed: ' + e.message); }
};
$('#btnSnap').onclick = () => { S.snap = !S.snap; $('#btnSnap').classList.toggle('on', S.snap); };
$('#btnGrid').onclick = () => { $('#btnGrid').classList.toggle('on'); page.classList.toggle('grid', $('#btnGrid').classList.contains('on')); };
$('#btnUndo').onclick = undo; $('#btnRedo').onclick = redo;
window.FolioAPI = { PRESETS, setTab, openFolio, S, $, $$, page, esc, uid, round, toast, api, render, blockById, selBlocks, select, selectMany, paintSel, pushUndo, markDirty, undo, redo,
  startEdit, commitEdit, editEl, startCrop, endCrop, resetCrop, zoomStep, centre, groupSel, ungroupSel, groupIds, updateGbox, cleanHTML, htmlToMd, md, shapeSVG, addText, addImageFile, showSelToolsForBlock, showSelToolsForGroup, openAsk, hideSelTools, fit, setZoom, PX_PER_MM };
$('#folioSelect').onchange = e => openFolio(e.target.value);

// ---------- live events from the server
function connectEvents() {
  const es = new EventSource('/api/events?t=' + TOKEN);
  es.onmessage = async ev => {
    let d; try { d = JSON.parse(ev.data); } catch { return; }
    if (d.folio && d.folio !== S.fid) return;
    if (d.type === 'folio' && d.hash !== S.hash) {
      if (S.dirty || S.editing) { S.pendingReload = true; toast('Claude changed this folio — your edit will be saved, then reloaded'); return; }
      const keep = [...S.multi]; S.doc = await api('/api/folio/' + S.fid); S.hash = S.doc._hash; render(); selectMany(keep.filter(id => blockById(id))); if (d.why !== 'editor') toast('Updated by Claude: ' + (d.why || ''));
    }
    if (['request', 'thread', 'notes', 'suggestions'].includes(d.type)) { await loadReview(); if (d.type === 'thread' && d.status === 'done') toast('Claude answered — see Threads'); }
  };
  es.onerror = () => { es.close(); setTimeout(connectEvents, 3000); };
}
setInterval(async () => { if (S.pendingReload && !S.dirty && !S.editing) { S.pendingReload = false; const keep = [...S.multi]; S.doc = await api('/api/folio/' + S.fid); S.hash = S.doc._hash; render(); selectMany(keep.filter(id => blockById(id))); } }, 1500);

// ---------- boot
window.addEventListener('resize', () => { if (!PRINT) applyZoom(); });
if (PRINT) { document.body.classList.add('print'); document.documentElement.classList.add('print'); }
loadFolios().then(() => { if (!PRINT) connectEvents(); if (PRINT) { document.title = 'print'; } }).catch(e => toast('Load failed: ' + e.message, 8000));
window.Folio = S;
})();
