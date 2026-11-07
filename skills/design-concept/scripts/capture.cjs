// Capture an inspiration site. Usage: node capture.cjs <out-folder> <url> [<url> ...]   (needs Playwright)
// Per page, at 1440 and 390: <name>-<width>-fold.png, -full.jpg, -styles.json; at 1440 also frames of loading and of a slow scroll, and hover styles.
const fs = require('fs'); const path = require('path'); const { execSync } = require('child_process');
function playwright() {
  const roots = [process.cwd(), ...(process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean)];
  try { const g = execSync('npm root -g', { encoding: 'utf8' }).trim(); roots.push(g, path.join(g, '@playwright/cli/node_modules')); } catch {}
  try { return require(require.resolve('playwright', { paths: roots })); }
  catch { console.error('Playwright not found. Run from a project that has it, or: npm i -g playwright && npx playwright install chromium'); process.exit(2); }
}
const [out, ...urls] = process.argv.slice(2);
if (!out || !urls.length) { console.error('Usage: node capture.cjs <out-folder> <url> [<url> ...]'); process.exit(2); }
fs.mkdirSync(out, { recursive: true });
const nameOf = (u) => { const { pathname } = new URL(u); return pathname.replace(/^\/|\/$/g, '').replace(/[^\w-]+/g, '-') || 'home'; };

const measure = () => {
  const hex = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return c; const [r, g, b, a] = m[1].split(',').map(parseFloat); const h = '#' + [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join(''); return a !== undefined && a < 1 ? `${h} @${a}` : h; };
  const seen = (c) => c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent';
  const count = {}; const tally = (k, v, n = 1) => { (count[k] = count[k] || {})[v] = (count[k][v] || 0) + n; };
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
    const s = getComputedStyle(el); if (s.visibility === 'hidden' || s.display === 'none' || +s.opacity === 0) continue;
    if (seen(s.backgroundColor)) tally('backgrounds', hex(s.backgroundColor), r.width * r.height);
    if (s.backgroundImage.includes('gradient')) tally('gradients', s.backgroundImage.slice(0, 120));
    const text = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (text) { const n = el.textContent.trim().length; tally('textColours', hex(s.color), n); tally('fonts', s.fontFamily.split(',')[0].replace(/["']/g, '').trim(), n); tally('type', `${s.fontSize}/${s.lineHeight} w${s.fontWeight} ls${s.letterSpacing} ${s.textTransform}`, n); }
    if (s.borderTopWidth !== '0px' && s.borderTopStyle !== 'none' && seen(s.borderTopColor)) tally('borders', `${s.borderTopWidth} ${hex(s.borderTopColor)}`);
    if (s.borderTopLeftRadius !== '0px') tally('radii', s.borderTopLeftRadius);
    if (s.boxShadow !== 'none') tally('shadows', s.boxShadow);
    if (s.transitionDuration !== '0s') tally('transitions', `${s.transitionProperty} ${s.transitionDuration} ${s.transitionTimingFunction}`.slice(0, 120));
    if (s.animationName !== 'none') tally('animations', `${s.animationName} ${s.animationDuration} ${s.animationTimingFunction}`);
    for (const p of ['paddingTop', 'paddingLeft', 'marginBottom', 'rowGap', 'columnGap']) { const v = parseFloat(s[p]); if (v > 0) tally('spacing', `${Math.round(v)}px`); }
  }
  const top = (o, n) => Object.entries(o || {}).sort((a, b) => b[1] - a[1]).slice(0, n).map(([v, c]) => [v, Math.round(c)]);
  const sample = (sel) => [...document.querySelectorAll(sel)].filter((e) => e.getBoundingClientRect().width).slice(0, 4).map((e) => { const s = getComputedStyle(e); return { text: e.textContent.trim().replace(/\s+/g, ' ').slice(0, 70), font: s.fontFamily, size: s.fontSize, weight: s.fontWeight, lineHeight: s.lineHeight, tracking: s.letterSpacing, colour: hex(s.color) }; });
  const buttons = [...document.querySelectorAll('a, button')].filter((e) => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.height > 24 && r.height < 90 && (seen(s.backgroundColor) || s.borderTopWidth !== '0px'); }).slice(0, 8).map((e) => { const s = getComputedStyle(e); return { text: e.textContent.trim().slice(0, 40), background: hex(s.backgroundColor), colour: hex(s.color), radius: s.borderTopLeftRadius, padding: s.padding, border: `${s.borderTopWidth} ${hex(s.borderTopColor)}`, font: `${s.fontSize} w${s.fontWeight}` }; });
  const vars = {}; for (const sheet of document.styleSheets) { try { for (const rule of sheet.cssRules) if (rule.selectorText === ':root' || rule.selectorText === 'html') for (const k of rule.style) if (k.startsWith('--')) vars[k] = rule.style.getPropertyValue(k).trim(); } catch {} }
  const faces = [...document.fonts].filter((f) => f.status === 'loaded').map((f) => `${f.family} ${f.weight} ${f.style}`);
  const out = { title: document.title, pageHeight: document.body.scrollHeight, h1: sample('h1'), h2: sample('h2'), h3: sample('h3'), body: sample('p'), buttons, rootVariables: vars, fontsLoaded: [...new Set(faces)] };
  for (const [k, n] of [['backgrounds', 12], ['textColours', 10], ['fonts', 8], ['type', 16], ['borders', 8], ['radii', 10], ['shadows', 6], ['gradients', 6], ['transitions', 10], ['animations', 10], ['spacing', 20]]) out[k] = top(count[k], n);
  return out;
};

const hover = async (p) => { // what the main buttons and links turn into on hover
  const found = []; const items = await p.locator('a:visible, button:visible').all();
  for (const item of items.slice(0, 40)) { if (found.length >= 6) break;
    const read = () => item.evaluate((e) => { const s = getComputedStyle(e); return { background: s.backgroundColor, colour: s.color, border: s.borderTopColor, transform: s.transform, shadow: s.boxShadow, opacity: s.opacity }; });
    try { const before = await read(); await item.hover({ timeout: 800 }); await p.waitForTimeout(450); const after = await read();
      if (JSON.stringify(before) !== JSON.stringify(after)) found.push({ text: (await item.textContent()).trim().slice(0, 40), before, after }); } catch {}
  }
  return found;
};

(async () => {
  const b = await playwright().chromium.launch();
  for (const url of urls) { const name = nameOf(url);
    for (const width of [1440, 390]) {
      const ctx = await b.newContext({ viewport: { width, height: width > 500 ? 900 : 844 }, isMobile: width < 500, hasTouch: width < 500 });
      const p = await ctx.newPage(); const base = path.join(out, `${name}-${width}`);
      try {
        await p.goto(url, { timeout: 60000, waitUntil: 'domcontentloaded' });
        if (width === 1440) for (const ms of [300, 900, 1800]) { await p.waitForTimeout(ms === 300 ? 300 : ms / 2); await p.screenshot({ path: `${base}-load-${ms}ms.jpg`, type: 'jpeg', quality: 60 }); }
        await p.waitForTimeout(2200);
        for (const t of ['Accept all', 'Accept All', 'Accept', 'Allow all', 'I agree', 'Got it']) { const c = p.getByRole('button', { name: t, exact: true }); if (await c.count()) { await c.first().click().catch(() => {}); break; } }
        await p.screenshot({ path: `${base}-fold.png` });
        const height = await p.evaluate(() => document.body.scrollHeight); let frame = 0;
        for (let y = 0; y < height; y += 450) { await p.evaluate((v) => window.scrollTo(0, v), y); await p.waitForTimeout(350);
          if (width === 1440 && frame < 24) await p.screenshot({ path: `${base}-scroll-${String(frame++).padStart(2, '0')}.jpg`, type: 'jpeg', quality: 55 }); }
        await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(800);
        await p.screenshot({ path: `${base}-full.jpg`, fullPage: true, type: 'jpeg', quality: 60 });
        const data = await p.evaluate(measure); if (width === 1440) data.hover = await hover(p);
        fs.writeFileSync(`${base}-styles.json`, JSON.stringify({ url, width, ...data }, null, 2));
        console.log('OK', name, width, data.title, 'height', data.pageHeight);
      } catch (e) { console.log('FAIL', name, width, e.message.split('\n')[0]); process.exitCode = 1; }
      await ctx.close();
    }
  }
  await b.close();
})();
