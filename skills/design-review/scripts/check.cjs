// The DESIGN.md checklist (§9), run on every page of a concept. Usage: node check.cjs <concept-folder> [--design path/to/DESIGN.md] [--structure]
// The concept's own values come from the `json design-check` block in its DESIGN.md (references/design-md-structure.md).
// 0 structure    DESIGN.md has every section and rule the structure requires, and its settings block
// 1 contrast     every visible text against its real background, in each theme, at 1440px (WCAG AA: 4.5, large text 3)
// 2 non-text     outlines that identify a control reach 3:1, in each theme (WCAG 1.4.11)
// 3 targets      every control at 390px with touch and at 1440px with a mouse reaches the sizes in the settings
// 4 focus        every element Tab reaches shows a solid outline ring of 2px or more on :focus-visible
// 5 spacing      every margin, padding and gap is on the spacing scale, at 390, 900 and 1440px (above the scale's top: auto margins, skipped)
// 6 type         every text size is on the type scale at 390, 900 and 1440px (right-to-left pages have their own steps)
// 7 chart text   chart labels reach the minimum size on screen at 390, 900 and 1440px
// 8 tokens       every colour token in DESIGN.md has the same value in the CSS; both dark blocks agree
// 9 sizes        no sideways scroll, no scrollbar showing inside the page and no control cut off by its box or too narrow for its longest option, and no select opening the browser's plain list, at 390, 720 (1440 at 200% zoom), 900, 1280, 1440 and 1920px
// 10 motion      nothing moves when the device asks for reduced motion
// --structure runs check 0 alone, with no browser. Prints PASS/FAIL per check with the offending elements; exit code 1 if any check fails.
const fs = require('fs'); const path = require('path');
const { playwright, args, settings, pages } = require('./shared.cjs');
const { root, design, structureOnly } = args(process.argv.slice(2));
const WIDTHS = [390, 900, 1440];
const results = {}; const add = (k, v) => (results[k] = results[k] || []).push(v);
const KEYS = ['0 structure', '1 contrast', '2 non-text', '3 targets', '4 focus', '5 spacing', '6 type', '7 chart text', '8 tokens', '9 sizes', '10 motion'];

// Section numbers are fixed because the review checks cite them; titles may vary a little.
const SECTIONS = [[1, /principles/i], [2, /colou?r/i], [3, /type/i], [4, /shape/i], [5, /components/i], [6, /charts/i], [7, /right to left|rtl/i], [8, /content/i], [9, /checklist/i], [10, /open items/i], [11, /depart/i]];
const RULES = { 3: ['Line height', 'Type scale'], 4: ['Corners', 'Spacing', 'Depth', 'Motion', 'Keyboard focus', 'Click and tap areas', 'Interaction states', 'Clickable or not', 'Icons'], 5: ['Names for assistive technology'] };
function structure(md, s) {
  const parts = md.split(/^## /m).slice(1);
  for (const [n, title] of SECTIONS) {
    const part = parts.find((p) => p.startsWith(`${n}. `));
    if (!part || !title.test(part.split('\n')[0])) { add('0 structure', `§${n} missing (expected a heading "## ${n}. …" matching ${title})`); continue; }
    for (const rule of RULES[n] || []) if (!part.includes(rule)) add('0 structure', `§${n}: no "${rule}" rule`);
  }
  if (![...md.matchAll(/\|\s*`(--[\w-]+)`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`/g)].length) add('0 structure', '§2: no token table (| `--name` | `light` | `dark` | job |)');
  if (!s) add('0 structure', '§9: no ```json design-check settings block');
  else for (const k of ['css', 'spacing', 'type']) if (!s[k]) add('0 structure', `§9 settings: "${k}" missing`);
}

const inPage = {
  contrast: (skip) => {
    const lum = (c) => { const [r, g, b] = c.map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
    const parse = (s) => { const m = s.match(/(rgba?|color)\((?:srgb )?([^)]+)\)/); if (!m) return null; const p = m[2].split(/[ ,/]+/).filter(Boolean).map(Number); // rgb() or color(srgb …) from color-mix
      const c = m[1] === 'color' ? p.slice(0, 3).map((v) => v * 255) : p.slice(0, 3); return { c, a: p[3] ?? 1 }; };
    const blend = (top, under) => top.c.map((v, i) => v * top.a + under[i] * (1 - top.a));
    const bgOf = (el) => { const stack = []; for (let n = el; n; n = n.parentElement) { const s = getComputedStyle(n); if (s.backgroundImage !== 'none' || n.tagName === 'IMG') return null; const b = parse(s.backgroundColor); if (b && b.a > 0) { stack.push(b); if (b.a === 1) break; } }
      let c = [255, 255, 255]; for (let i = stack.length - 1; i >= 0; i--) c = blend(stack[i], c); return c; };
    const out = [];
    for (const el of document.querySelectorAll('body *')) {
      const own = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()); if (!own) continue;
      const r = el.getBoundingClientRect(); const s = getComputedStyle(el); if (!r.width || s.visibility === 'hidden' || +s.opacity === 0) continue;
      if (el.closest(skip)) continue; // text on photos, decorative layers, disabled controls (exempt)
      const fg = parse(s.color); const bg = bgOf(el); if (!fg || !bg) continue;
      const f = blend(fg, bg); const L1 = lum(f), L2 = lum(bg); const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
      const px = parseFloat(s.fontSize); const large = px >= 24 || (px >= 18.66 && +s.fontWeight >= 700);
      if (ratio < (large ? 3 : 4.5)) out.push(`${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]} "${el.textContent.trim().slice(0, 28)}" ${ratio.toFixed(2)}`);
    }
    return out;
  },
  nontext: ({ outlines, fills, skip }) => {
    const lum = (c) => { const [r, g, b] = c.map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
    const parse = (s) => { const m = s.match(/(rgba?|color)\((?:srgb )?([^)]+)\)/); if (!m) return null; const p = m[2].split(/[ ,/]+/).filter(Boolean).map(Number); // rgb() or color(srgb …) from color-mix
      const c = m[1] === 'color' ? p.slice(0, 3).map((v) => v * 255) : p.slice(0, 3); return { c, a: p[3] ?? 1 }; };
    const blend = (top, under) => top.c.map((v, i) => v * top.a + under[i] * (1 - top.a));
    const bgOf = (el) => { const stack = []; for (let n = el; n; n = n.parentElement) { const b = parse(getComputedStyle(n).backgroundColor); if (b && b.a > 0) { stack.push(b); if (b.a === 1) break; } }
      let c = [255, 255, 255]; for (let i = stack.length - 1; i >= 0; i--) c = blend(stack[i], c); return c; };
    const out = [];
    for (const el of document.querySelectorAll([outlines, fills].filter(Boolean).join(', ') || 'none-of-these')) {
      const r = el.getBoundingClientRect(); if (!r.width || el.closest(skip)) continue;
      const s = getComputedStyle(el); const under = bgOf(el.parentElement);
      const mark = parse(fills && el.matches(fills) ? s.backgroundColor : s.borderTopColor); if (!mark) continue; // a switch track shows its fill, the rest their outline
      const m = blend(mark, under); const L1 = lum(m), L2 = lum(under); const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
      if (ratio < 3) out.push(`.${String(el.className).split(' ').join('.')} ${ratio.toFixed(2)}`);
    }
    return out;
  },
  chartText: ({ charts, min }) => [...document.querySelectorAll(charts)].flatMap((svg) => { const w = svg.getBoundingClientRect().width; if (!w) return [];
    const k = w / svg.viewBox.baseVal.width;
    return [...svg.querySelectorAll('text')].map((t) => parseFloat(getComputedStyle(t).fontSize) * k).filter((px) => px < min - 0.1)
      .slice(0, 1).map((px) => `${String(svg.className.baseVal)} ${svg.viewBox.baseVal.width}: ${px.toFixed(1)}px`); }),
  targets: ({ min, controls, rows, hitAreas, skip }) => [...document.querySelectorAll(controls)].filter((el) => {
    const r = el.getBoundingClientRect(); const s = getComputedStyle(el); if (!r.width || s.visibility === 'hidden' || el.closest(skip)) return false;
    const row = rows && el.closest(rows); if (row && row.getBoundingClientRect().height >= min) return false; // the whole row is the target
    const hit = Object.entries(hitAreas).reduce((n, [sel, px]) => (el.matches(sel) ? px : n), 0); // a hit area that reaches past the mark (::after)
    return r.width + hit < min || r.height + hit < min;
  }).map((el) => { const r = el.getBoundingClientRect(); return `${el.tagName.toLowerCase()}.${String(el.className).split(' ').join('.')} ${Math.round(r.width)}x${Math.round(r.height)}`; }),
  type: (steps) => { const bad = {}; for (const el of document.querySelectorAll('body *')) { if (el.closest('svg')) continue;
      const own = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()); if (!own) continue;
      const v = Math.round(parseFloat(getComputedStyle(el).fontSize) * 2) / 2; if (!steps.includes(v)) bad[`.${String(el.className).split(' ')[0] || el.tagName.toLowerCase()} ${v}px`] = 1; }
    return Object.keys(bad); },
  spacing: ({ scale, skip }) => { const top = Math.max(...scale); const bad = {}; for (const el of document.querySelectorAll('body *')) { if (el.closest('svg') || (skip && el.matches(skip))) continue; const s = getComputedStyle(el);
      for (const p of ['marginTop', 'marginBottom', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight', 'rowGap', 'columnGap']) { const v = parseFloat(s[p]); if (!isNaN(v) && Math.abs(v) <= top && !scale.includes(Math.abs(Math.round(v)))) { const k = `.${String(el.className).split(' ')[0] || el.tagName.toLowerCase()} ${p} ${Math.round(v)}px`; bad[k] = 1; } } }
    return Object.keys(bad); },
};

function tokens(md, s) {
  const file = path.join(root, s.css); if (!fs.existsSync(file)) return add('8 tokens', `${s.css} not found`);
  const css = fs.readFileSync(file, 'utf8'); const dual = s.themes.includes('dark');
  const val = (block, t) => { const m = block.match(new RegExp(`${t}:\\s*([^;]+);`)); return m && m[1].trim(); };
  const light = css.split(':root[data-theme="dark"]')[0]; let dark = '';
  if (dual) {
    if (!css.includes(':root[data-theme="dark"]') || !css.includes(':root:not([data-theme="light"])')) return add('8 tokens', 'dark theme needs both a :root[data-theme="dark"] block and a device-dark :root:not([data-theme="light"]) block');
    dark = css.split(':root[data-theme="dark"]')[1].split('}')[0]; const media = css.split(':root:not([data-theme="light"])')[1].split('}')[0];
    const list = (block) => Object.fromEntries([...block.matchAll(/(--[\w-]+):\s*([^;]+);/g)].map(([, t, v]) => [t, v.trim()]));
    const [td, tm] = [list(dark), list(media)];
    for (const t of new Set([...Object.keys(td), ...Object.keys(tm)])) if (td[t] !== tm[t]) add('8 tokens', `${t}: [data-theme="dark"] ${td[t]}, device-dark block ${tm[t]}`);
  }
  for (const [, t, l, d] of md.matchAll(/\|\s*`(--[\w-]+)`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`/g)) { // rows like | `--ink` | `#221C15` | `#ECE8E1` |
    if (val(light, t) !== l) add('8 tokens', `${t} light: DESIGN.md ${l}, ${s.css} ${val(light, t)}`);
    if (dual && d !== 'same' && val(dark, t) !== d) add('8 tokens', `${t} dark: DESIGN.md ${d}, ${s.css} ${val(dark, t)}`);
  }
}

function report(keys) {
  let failed = false;
  for (const k of keys) {
    const list = [...new Set(results[k] || [])]; console.log(`${list.length ? 'FAIL' : 'PASS'}  ${k}${list.length ? ` (${list.length})` : ''}`);
    list.slice(0, 40).forEach((x) => console.log('      ' + x)); if (list.length > 40) console.log(`      … ${list.length - 40} more`); if (list.length) failed = true;
  }
  process.exit(failed ? 1 : 0);
}

(async () => {
  if (!fs.existsSync(design)) { console.error(`DESIGN.md not found at ${design}. Pass --design <path>.`); process.exit(2); }
  const md = fs.readFileSync(design, 'utf8'); const s = settings(md);
  structure(md, s);
  if (structureOnly) report(['0 structure']);
  if (!s || !s.css || !s.spacing || !s.type) report(['0 structure']); // the page checks need the settings
  const sel = s.selectors; const disabled = ['[aria-disabled="true"]', sel.disabled].filter(Boolean).join(', ');
  const skipText = ['svg', '[aria-hidden="true"]', ':disabled', disabled, sel.textOnMedia].filter(Boolean).join(', ');
  const skipControl = [disabled, sel.controlsDrawnForShow].filter(Boolean).join(', ');
  const controls = ['button', 'a', sel.controls].filter(Boolean).join(', ');
  const skipTarget = ['[aria-hidden="true"]', sel.disabled].filter(Boolean).join(', ');
  const b = await playwright().chromium.launch({ ignoreDefaultArgs: ['--hide-scrollbars'] }); // headless hides scrollbars unless told not to
  for (const { name, url, rtl } of pages(root, s)) {
    const steps = s.type[rtl ? 'rtl' : 'ltr'] || s.type.ltr; const tag = rtl ? 'rtl' : 'ltr';
    const open = async (opts) => { const p = await b.newPage(opts); await p.goto(url); await p.evaluate(() => document.fonts.ready); return p; };
    for (const scheme of s.themes) {
      const p = await open({ viewport: { width: 1440, height: 900 }, colorScheme: scheme, reducedMotion: 'reduce' });
      for (const f of await p.evaluate(inPage.contrast, skipText)) add('1 contrast', `${name} ${scheme}: ${f}`);
      for (const f of await p.evaluate(inPage.nontext, { outlines: sel.controlOutlines, fills: sel.controlFills, skip: skipControl })) add('2 non-text', `${name} ${scheme}: ${f}`);
      if (scheme === s.themes[0]) {
        const n = await p.evaluate(() => document.getAnimations().filter((a) => a.playState === 'running').length); if (n) add('10 motion', `${name}: ${n} running`);
        const stops = await p.evaluate(() => document.querySelectorAll('button, a[href], input, [tabindex]').length); // 4 focus: Tab through
        for (let i = 0; i < stops; i++) { await p.keyboard.press('Tab');
          const r = await p.evaluate(() => { const el = document.activeElement; if (!el || el === document.body) return null; const st = getComputedStyle(el);
            const ring = el.matches(':focus-visible') && st.outlineStyle === 'solid' && parseFloat(st.outlineWidth) >= 2; // the brand ring, not the browser default
            return ring ? null : `${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]} "${el.textContent.trim().slice(0, 20)}"`; });
          if (r) add('4 focus', `${name}: ${r}`); }
      }
      await p.close();
    }
    for (const width of [...WIDTHS, 720, 1280, 1920]) {
      const p = await open({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
      if (await p.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth)) add('9 sizes', `${name} at ${width}px`);
      for (const f of await p.evaluate(() => [...document.querySelectorAll('body *')].flatMap((el) => { if (!el.offsetWidth) return []; const st = getComputedStyle(el); if (!/auto|scroll/.test(st.overflowX + st.overflowY)) return []; if (/^(transparent|rgba\(0, 0, 0, 0\))/.test(st.scrollbarColor)) return []; const bw = (k) => parseFloat(st[k]) || 0; const v = el.offsetWidth - el.clientWidth - bw('borderLeftWidth') - bw('borderRightWidth') > 0.5; const h = el.offsetHeight - el.clientHeight - bw('borderTopWidth') - bw('borderBottomWidth') > 0.5; return v || h ? [`${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]} ${v ? 'vertical' : ''}${h ? ' sideways' : ''}`] : []; }))) add('9 sizes', `${name} at ${width}px: scrollbar showing inside the page on ${f}`);
      for (const f of await p.evaluate(() => [...document.querySelectorAll('button, select, input, a, label, td *')].flatMap((el) => { const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2 || el.closest('.sr-only, [aria-hidden="true"]')) return []; for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) { const st = getComputedStyle(a); if (/auto|scroll/.test(st.overflowX)) return []; if (/hidden|clip/.test(st.overflowX)) { const c = a.getBoundingClientRect(); return r.right > c.right + 1 || r.left < c.left - 1 ? [`${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]}`] : []; } } return []; }))) add('9 sizes', `${name} at ${width}px: cut off by its box: ${f}`);
      for (const f of await p.evaluate(() => { const c = document.createElement('canvas').getContext('2d'); return [...document.querySelectorAll('select')].flatMap((el) => { if (!el.offsetWidth) return []; const st = getComputedStyle(el); c.font = `${st.fontWeight} ${st.fontSize} ${st.fontFamily}`; const room = el.clientWidth - parseFloat(st.paddingLeft) - parseFloat(st.paddingRight); const long = [...el.options].find((o) => c.measureText(o.text).width > room + 1); return long ? [long.text] : []; }); })) add('9 sizes', `${name} at ${width}px: select too narrow for "${f}"`);
      if (width === 1920) { const plain = await p.evaluate(() => [...document.querySelectorAll('select')].filter((el) => el.offsetWidth).filter((el) => el.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true, button: 0 }))).length); if (plain) add('9 sizes', `${name}: ${plain} select(s) open the browser's plain list, not a styled menu`); }
      if (WIDTHS.includes(width)) {
        for (const f of await p.evaluate(inPage.spacing, { scale: s.spacing, skip: sel.skipSpacing })) add('5 spacing', `${f} (${width})`);
        for (const f of await p.evaluate(inPage.type, steps)) add('6 type', `${tag} ${f} (${width})`);
        for (const f of await p.evaluate(inPage.chartText, { charts: sel.charts || 'svg.chart', min: s.chartTextMin })) add('7 chart text', `${name} at ${width}px: ${f}`);
        if (width === 1440) for (const f of await p.evaluate(inPage.targets, { min: s.targets.mouse, controls, rows: sel.controlRows, hitAreas: s.hitAreas || {}, skip: skipTarget })) add('3 targets', `${name} (mouse): ${f}`);
      }
      await p.close();
    }
    const m = await open({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, reducedMotion: 'reduce' });
    for (const f of await m.evaluate(inPage.targets, { min: s.targets.touch, controls, rows: sel.controlRows, hitAreas: s.hitAreas || {}, skip: skipTarget })) add('3 targets', `${name}: ${f}`);
    await m.close();
  }
  await b.close();
  tokens(md, s);
  report(KEYS);
})();
