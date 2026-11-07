// Uses the screens the way a person does, and pictures the result, in <concept>/renders/walk/. Usage: node walk.cjs <concept-folder>   (needs Playwright)
// On every page, at a laptop size with scrollbars showing, it clicks each kind of control once and saves what opened. Main language in each theme; other languages light.
// FAIL: a browser default left on screen (date, file or colour input, number spinner, unstyled checkbox or radio, alert), a menu or dialog running off the screen or opening away from its control, or a script error.
// A check of the pictures is still needed: this finds what opens, not whether it looks finished.
const fs = require('fs'); const path = require('path'); const { execSync } = require('child_process');
function playwright() {
  const roots = [process.cwd(), ...(process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean)];
  try { const g = execSync('npm root -g', { encoding: 'utf8' }).trim(); roots.push(g, path.join(g, '@playwright/cli/node_modules')); } catch {}
  try { return require(require.resolve('playwright', { paths: roots })); }
  catch { console.error('Playwright not found. Run from a project that has it, or: npm i -g playwright && npx playwright install chromium'); process.exit(2); }
}
const root = path.resolve(process.argv[2] || '.'); const out = path.join(root, 'renders/walk');
const dir = fs.existsSync(path.join(root, 'src/pages')) ? path.join(root, 'src/pages') : path.join(root, 'src');
const pages = fs.readdirSync(dir).filter((f) => f.endsWith('.html')).sort().map((f) => f.replace(/\.html$/, ''));
const translation = (n) => /-[a-z]{2}$/.test(n) && pages.includes(n.slice(0, -3));
const design = path.join(root, 'DESIGN.md'); const settings = fs.existsSync(design) && fs.readFileSync(design, 'utf8').match(/```json design-check\n([\s\S]*?)```/);
const themes = (settings && JSON.parse(settings[1]).themes) || ['light', 'dark'];
fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
const MAX = 40; const problems = new Set(); let count = 0;

// One entry per kind of control, so forty identical row buttons are clicked once.
const controls = () => { const seen = new Set(); const found = [];
  [...document.querySelectorAll('button, select, summary, [role=tab], [aria-haspopup]')].forEach((el, i) => { const r = el.getBoundingClientRect(); if (!r.width || !r.height || el.disabled || el.closest('[aria-hidden="true"]')) return;
    const key = [el.tagName, el.dataset.act || '', Object.keys(el.dataset).sort().join(), String(el.className).split(' ').slice(0, 2).join(), el.getAttribute('role') || ''].join('|');
    if (seen.has(key)) return; seen.add(key); found.push({ i, label: (el.dataset.act || el.getAttribute('aria-label') || el.textContent || el.tagName).trim().slice(0, 28) }); }); return found; };
const defaults = (from) => { const bad = []; const shown = (el) => el.getBoundingClientRect().width > 1;
  document.querySelectorAll('input[type=date], input[type=time], input[type=datetime-local], input[type=month], input[type=color], input[type=file], input[type=number]').forEach((el) => { if (shown(el)) bad.push(`browser ${el.type} input`); });
  document.querySelectorAll('input[type=checkbox], input[type=radio]').forEach((el) => { if (shown(el) && getComputedStyle(el).appearance !== 'none') bad.push(`unstyled ${el.type}`); });
  document.querySelectorAll('.menu, [role=menu], [role=dialog], [role=listbox], dialog[open]').forEach((el) => { const r = el.getBoundingClientRect(); const W = document.documentElement.clientWidth; if (r.width && (r.left < -1 || r.top < -1 || r.right > W + 1 || r.bottom > innerHeight + 1)) bad.push(`${el.className || el.tagName} runs off the screen`);
    if (from && r.width && el.matches('.menu, [role=menu], [role=listbox]') && Math.min(Math.abs(r.top - from.bottom), Math.abs(from.top - r.bottom)) > 24) bad.push('menu opens away from its control'); });
  return bad; };

async function walk(b, page, scheme) {
  const ctx = await b.newContext({ viewport: { width: 1536, height: 730 }, colorScheme: scheme, reducedMotion: 'reduce' }); await ctx.addInitScript(() => { try { localStorage.clear(); } catch {} }); const p = await ctx.newPage(); // each click starts clean: a theme switch must not carry over
  const url = `file://${path.join(dir, page + '.html')}`; let current = '';
  p.on('pageerror', (e) => problems.add(`${page}: script error after ${current}: ${e.message.slice(0, 100)}`));
  p.on('dialog', (d) => { problems.add(`${page}: browser ${d.type()} box after ${current}`); d.dismiss().catch(() => {}); });
  const fresh = async () => { await p.goto(url); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250); };
  await fresh(); (await p.evaluate(defaults)).forEach((f) => problems.add(`${page}: ${f}`));
  const list = (await p.evaluate(controls)).slice(0, MAX);
  for (const [n, c] of list.entries()) { current = c.label; await fresh();
    const before = await p.evaluate(() => document.body.innerHTML.length);
    const target = p.locator('button, select, summary, [role=tab], [aria-haspopup]').nth(c.i); let from;
    try { await target.scrollIntoViewIfNeeded({ timeout: 1000 }); from = await target.boundingBox(); await target.click({ timeout: 1500 }); await p.waitForTimeout(350); } catch { continue; }
    if (!p.url().startsWith(url)) continue;
    if (await p.evaluate(() => document.body.innerHTML.length) === before) continue;
    (from = (await target.boundingBox().catch(() => null)) || from, await p.evaluate(defaults, from && { top: from.y, bottom: from.y + from.height })).forEach((f) => problems.add(`${page} after "${c.label}": ${f}`));
    await p.screenshot({ path: path.join(out, `${page}-${scheme}-${String(n + 1).padStart(2, '0')}-${c.label.replace(/[^\p{L}\p{N}]+/gu, '-').toLowerCase()}.png`) }); count++; }
  await ctx.close();
}

(async () => {
  const b = await playwright().chromium.launch({ ignoreDefaultArgs: ['--hide-scrollbars'] });
  for (const page of pages) for (const scheme of translation(page) ? [themes[0]] : themes) await walk(b, page, scheme);
  await b.close();
  [...problems].forEach((f) => console.log(`      ${f}`));
  console.log(`${problems.size ? 'FAIL' : 'PASS'}  ${count} pictures of opened controls in ${out}`); process.exit(problems.size ? 1 : 0);
})();
