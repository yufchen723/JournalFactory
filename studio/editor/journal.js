/* Folio Studio 0.6.0 — Journal tab: pick the journal, set its page width, check the page against its rules,
   count words, and ask Claude with journal-specific presets. Hides itself when the server has no journal API. */
(() => {
  const A = window.FolioAPI; if (!A) return;
  const { S, $, $$, api, esc, toast } = A;
  let J = [], cur = null;
  const doc = () => S.doc || S.folio || {};
  const tab = $('#rtJournal');
  const BASE = { ask: A.PRESETS.ask.slice(), edit: A.PRESETS.edit.slice() };
  function presets(j) {
    A.PRESETS.ask = BASE.ask.slice(); A.PRESETS.edit = BASE.edit.slice();
    if (!j) return [];
    const n = j.name, flow = doc().mode === 'flow';
    const ask = flow ? [`Does this meet ${n}'s bar? What would a reviewer ask?`, `What does the field already know about this? (field map)`, `Is this claim supported by the figure it cites?`]
      : [`Does this figure follow ${n}'s rules?`, `What is the one message of this figure?`, `Which panel would a ${n} reviewer question?`];
    const edit = flow ? [`Rewrite in ${n} style`, `Cut to the ${n} word limit`, `Draft the figure legend from the panels`, `Add verified citations`]
      : [`Fit to ${n} width and text sizes`, `Fix panel letters for ${n}`, `Redo panel at final size`];
    A.PRESETS.ask = ask.concat(BASE.ask); A.PRESETS.edit = edit.concat(BASE.edit);
    return ask.concat(edit);
  }
  function paint() {
    const d = doc(); cur = J.find(j => j.id === d.journal) || null;
    $('#jSel').value = cur ? cur.id : '';
    const flow = d.mode === 'flow';
    $('#jWidthG').hidden = flow || !cur || (d.paper || {}).role === 'graphical_abstract';
    $('#jInfo').textContent = cur ? (flow ? `Main text about ${cur.main_text_words || '—'} words · abstract ${cur.abstract_words || '—'} · ${cur.main_display_items || '—'} display items` :
      `Text ${cur.font_pt.min}–${cur.font_pt.max} pt · letters ${cur.panel_label.case === 'upper' ? 'A B C' : 'a b c'} ${cur.panel_label.pt} pt · max height ${cur.max_height_mm} mm`) + ` · rules: ${cur.verified}` : 'Choose a journal to get its sizes, limits and checks.';
    $('#jWidths').innerHTML = cur ? Object.entries(cur.widths_mm).map(([k, v]) => `<button data-w="${v}" class="${Math.abs((d.page || {}).w_mm - v) < 0.6 ? 'on' : ''}" title="${k} column">${k}<br>${v} mm</button>`).join('') : '';
    $$('#jWidths button').forEach(b => b.onclick = () => { A.pushUndo && A.pushUndo(); d.page.w_mm = +b.dataset.w; A.markDirty && A.markDirty(); A.render(); A.fit && A.fit(); paint(); toast(`Page width ${b.dataset.w} mm. Panels were not moved.`); });
    const ps = presets(cur);
    $('#jAsk').innerHTML = ps.slice(0, 4).map(p => `<button data-p="${esc(p)}">${esc(p)}</button>`).join('');
    $$('#jAsk button').forEach(b => b.onclick = () => A.openAsk({ tab: A.PRESETS.edit.includes(b.dataset.p) ? 'edit' : 'ask', text: b.dataset.p }));
    count();
  }
  const words = t => ((t || '').replace(/<[^>]+>|[*_`#>|]/g, ' ').match(/[A-Za-z0-9][\w'’\-/.%]*/g) || []).length;
  function count() {
    const d = doc(); if (d.mode !== 'flow') { $('#jCount').textContent = ''; return; }
    const n = (d.blocks || []).filter(b => b.type === 'text').reduce((s, b) => s + words(b.text), 0);
    $('#jCount').textContent = `${n} words on this page` + (cur && cur.main_text_words ? ` · main-text limit about ${cur.main_text_words}` : '');
  }
  async function check() {
    const d = doc(); if (!d.journal) return toast('Choose a journal first.');
    let r; try { r = await api(`/api/folio/${S.fid || d.id}/check`); } catch (e) { return toast('Check failed: ' + e.message); }
    let p = $('#jPanel'); if (!p) { p = document.createElement('div'); p.id = 'jPanel'; document.body.appendChild(p); }
    const mark = { error: '✗', warn: '!', ok: '✓', info: '·' };
    p.innerHTML = `<header><span>${esc(r.name)} check · ${r.errors} problem${r.errors === 1 ? '' : 's'}, ${r.warnings} warning${r.warnings === 1 ? '' : 's'}</span><span><button id="jAskFix" title="Send the problems to Claude">✳</button><button id="jClose">×</button></span></header>` +
      r.items.map(i => `<div class="ji ${i.level}" ${i.block ? `data-b="${esc(i.block)}"` : ''}><b>${mark[i.level]}</b><span>${esc(i.msg)}</span></div>`).join('') +
      ((r.counts.sections || []).length ? '<table>' + r.counts.sections.map(s => `<tr><td>${s.words}</td><td>${esc(s.section)}</td></tr>`).join('') + '</table>' : '');
    $('#jClose').onclick = () => p.remove();
    $('#jAskFix').onclick = () => A.openAsk({ tab: 'edit', text: `Fix these ${r.name} check problems:\n` + r.items.filter(i => i.level === 'error' || i.level === 'warn').map(i => `- ${i.msg}${i.block ? ' [' + i.block + ']' : ''}`).join('\n') });
    $$('#jPanel .ji[data-b]').forEach(e => e.onclick = () => { const b = A.blockById(e.dataset.b); if (b) { A.select(b.id); const el = document.querySelector(`[data-id="${CSS.escape(b.id)}"]`); el && el.scrollIntoView({ block: 'center', behavior: 'smooth' }); } });
  }
  async function nav() {
    try {
      const fs = await api('/api/folios'); const sel = $('#jNav');
      sel.innerHTML = '<option value="">Manuscript parts…</option>' + fs.map(f => `<option value="${esc(f.id)}">${esc(f.title || f.id)}</option>`).join('');
      sel.onchange = () => { if (sel.value && A.openFolio) A.openFolio(sel.value); sel.value = ''; };
    } catch (e) { }
  }
  (async () => {
    try { J = await api('/api/journals'); } catch (e) { return; }      // older server: tab stays hidden
    if (!Array.isArray(J) || !J.length) return;
    tab.hidden = false;
    $('#jSel').insertAdjacentHTML('beforeend', J.map(j => `<option value="${esc(j.id)}">${esc(j.name)}</option>`).join(''));
    $('#jSel').onchange = e => { const d = doc(); A.pushUndo && A.pushUndo(); if (e.target.value) d.journal = e.target.value; else delete d.journal; A.markDirty && A.markDirty(); paint(); };
    $('#jCheck').onclick = check;
    tab.addEventListener('click', () => { paint(); nav(); });
    let last = null; setInterval(() => { const d = doc(); const k = (d.id || '') + '|' + (d.journal || '') + '|' + (d.page || {}).w_mm; if (k !== last) { last = k; paint(); } else if (tab.classList.contains('on')) count(); }, 1200);
  })();
})();
