(() => {
  'use strict';
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- mobile menu ---------- */
  const menuBtn = $('#menu-btn');
  const mnav = $('#mnav');
  const menuLabel = $('#menu-label');
  if (menuBtn && mnav) {
    const setOpen = (open) => {
      mnav.hidden = !open;
      menuBtn.setAttribute('aria-expanded', String(open));
      menuLabel.textContent = open ? '닫기' : '메뉴';
    };
    menuBtn.addEventListener('click', () => setOpen(mnav.hidden));
    mnav.addEventListener('click', (e) => { if (e.target.closest('a')) setOpen(false); });
  }

  /* ---------- hero: drawing balloons <-> parts list ---------- */
  const marks = $$('[data-k]');
  let touched = false;
  const light = (k) => marks.forEach((el) => el.classList.toggle('on', k !== null && el.dataset.k === k));
  marks.forEach((el) => {
    if (el.tagName === 'line') return;
    el.addEventListener('pointerenter', () => { touched = true; light(el.dataset.k); });
    el.addEventListener('pointerleave', () => light(null));
    el.addEventListener('focus', () => { touched = true; light(el.dataset.k); });
    el.addEventListener('blur', () => light(null));
  });
  /* one start-up pass along the line: each module lights in turn, then the line rests */
  const stage = $('#stage');
  if (!reduced && stage) {
    const order = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'];
    let i = 0;
    const step = () => {
      if (touched) return;
      if (i < order.length) { light(order[i++]); setTimeout(step, 240); }
      else setTimeout(() => { if (!touched) light(null); }, 500);
    };
    setTimeout(step, 900);
  }

  /* ---------- line-up filter ---------- */
  const chips = $$('.chip[data-f]');
  const cards = $$('.eq');
  const result = $('#result');
  chips.forEach((chip) => chip.addEventListener('click', () => {
    const f = chip.dataset.f;
    chips.forEach((c) => c.setAttribute('aria-pressed', String(c === chip)));
    let n = 0;
    cards.forEach((card) => {
      const show = f === 'all' || card.dataset.cat === f;
      card.hidden = !show;
      if (show) n++;
    });
    if (result) result.textContent = n + '개 설비';
  }));

  /* ---------- spec dialog ---------- */
  const dataEl = $('#eq-data');
  const dlg = $('#dlg');
  let DATA = {};
  try { DATA = JSON.parse(dataEl ? dataEl.textContent : '{}'); } catch (e) { DATA = {}; }
  const el = (id) => document.getElementById(id);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = (n) => n.toLocaleString('en-US');

  function planSVG(L, W) {
    /* one scale for every machine: 10 m of floor = 400 units, grid 1 m */
    const s = 0.04, ox = 68, oy = 8;
    const fw = 10000 * s, fh = 2500 * s;
    const mw = L * s, mh = W * s;
    let g = '';
    g += `<rect class="pl-floor" x="${ox}" y="${oy}" width="${fw}" height="${fh}"/>`;
    for (let x = 1; x < 10; x++) g += `<line class="pl-grid" x1="${ox + x * 40}" y1="${oy}" x2="${ox + x * 40}" y2="${oy + fh}"/>`;
    for (let y = 1; y < 2.5; y++) g += `<line class="pl-grid" x1="${ox}" y1="${oy + y * 40}" x2="${ox + fw}" y2="${oy + y * 40}"/>`;
    g += `<rect class="pl-m" x="${ox}" y="${oy}" width="${mw}" height="${mh}"/>`;
    /* flow arrow (left to right) inside the machine */
    const ay = oy + mh / 2, ax0 = ox + Math.min(10, mw * 0.15), ax1 = ox + mw - Math.min(10, mw * 0.15);
    if (mw > 40) {
      g += `<path class="pl-flow" d="M${ax0} ${ay}H${ax1}M${ax1 - 6} ${ay - 4}L${ax1} ${ay}L${ax1 - 6} ${ay + 4}"/>`;
      if (mw > 90) g += `<text class="pl-ft" x="${ax0}" y="${ay - 6}">물류</text>`;
    }
    /* L dimension under the floor, W dimension at the machine's right edge */
    const dy = oy + fh + 16;
    g += `<path class="pl-dim" d="M${ox} ${oy + fh + 4}V${dy + 4}M${ox + mw} ${oy + mh + 4}V${dy + 4}M${ox} ${dy}H${ox + mw}M${ox + 4} ${dy - 3}L${ox} ${dy}L${ox + 4} ${dy + 3}M${ox + mw - 4} ${dy - 3}L${ox + mw} ${dy}L${ox + mw - 4} ${dy + 3}"/>`;
    g += `<text class="pl-t" x="${ox + mw / 2}" y="${dy + 14}" text-anchor="middle">L ${fmt(L)}</text>`;
    /* W dimension on the left, outside the floor, so it never sits on the grid */
    const dx = ox - 10;
    g += `<path class="pl-dim" d="M${ox - 3} ${oy}H${dx - 4}M${ox - 3} ${oy + mh}H${dx - 4}M${dx} ${oy}V${oy + mh}M${dx - 3} ${oy + 4}L${dx} ${oy}L${dx + 3} ${oy + 4}M${dx - 3} ${oy + mh - 4}L${dx} ${oy + mh}L${dx + 3} ${oy + mh - 4}"/>`;
    g += `<text class="pl-t" x="${dx - 6}" y="${oy + mh / 2 + 4}" text-anchor="end">W ${fmt(W)}</text>`;
    return { g, vb: `0 0 ${ox + fw + 8} ${dy + 22}` };
  }

  let current = null;
  function show(i) {
    const d = DATA[current];
    if (!d) return;
    const im = d.images[i];
    const main = el('dlg-main');
    const img = el('dlg-img');
    main.className = 'dlg-main well ' + (im.kind || 'render');
    img.src = im.src;
    img.alt = im.alt;
    img.width = im.w; img.height = im.h;
    el('dlg-cap').textContent = im.alt;
    $$('#dlg-thumbs button').forEach((b, j) => b.setAttribute('aria-current', String(j === i)));
  }
  function openSpec(id) {
    const d = DATA[id];
    if (!d || !dlg) return;
    current = id;
    el('dlg-en').textContent = d.en;
    el('dlg-title').textContent = d.ko;
    el('dlg-desc').textContent = d.desc;
    el('dlg-cat').textContent = d.cat;
    el('dlg-spec').innerHTML = d.spec.map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${(Array.isArray(v) ? v : [v]).map((x) => `<span>${esc(x)}</span>`).join('')}</dd></div>`).join('');
    const th = el('dlg-thumbs');
    th.innerHTML = d.images.length > 1 ? d.images.map((im, j) => `<button type="button" class="well ${im.kind || 'render'}" data-i="${j}" aria-label="${esc(im.alt)}"><img src="${esc(im.src)}" alt="" loading="lazy"></button>`).join('') : '';
    th.hidden = d.images.length < 2;
    const plan = el('dlg-plan');
    if (d.dims) {
      const p = planSVG(d.dims[0], d.dims[1]);
      const svg = el('dlg-plan-svg');
      svg.setAttribute('viewBox', p.vb);
      svg.innerHTML = p.g;
      el('dlg-plan-cap').textContent = `평면도 · L ${fmt(d.dims[0])} × W ${fmt(d.dims[1])} × H ${fmt(d.dims[2])} mm`;
      plan.hidden = false;
    } else {
      plan.hidden = true;
    }
    show(0);
    if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
    const scroller = $('.dlg-in', dlg); if (scroller) scroller.scrollTop = 0;
    const body = $('.dlg-body', dlg); if (body) body.scrollTop = 0;
  }
  $$('[data-open]').forEach((b) => b.addEventListener('click', () => openSpec(b.dataset.open)));
  if (dlg) {
    el('dlg-thumbs').addEventListener('click', (e) => {
      const b = e.target.closest('button[data-i]');
      if (b) show(Number(b.dataset.i));
    });
    el('dlg-x').addEventListener('click', () => dlg.close());
    dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
  }

  /* ---------- copy buttons: clipboard first, text selection as fallback ---------- */
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-copy]');
    if (!btn) return;
    if (!btn.dataset.label) btn.dataset.label = btn.textContent;
    const flash = (msg) => {
      btn.textContent = msg;
      btn.classList.add('done');
      clearTimeout(btn._t);
      btn._t = setTimeout(() => { btn.textContent = btn.dataset.label; btn.classList.remove('done'); }, 1800);
    };
    const selectText = () => {
      const t = document.getElementById(btn.dataset.target);
      if (!t) { flash('직접 복사해 주세요'); return; }
      const r = document.createRange();
      r.selectNodeContents(t);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(r);
      flash('선택됨');
    };
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(btn.dataset.copy).then(() => flash('복사됨'), selectText);
      else selectText();
    } catch (err) { selectText(); }
  });
})();
