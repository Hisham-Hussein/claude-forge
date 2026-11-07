// The outside check's screenshots, in <concept>/renders/check/. Usage: node shots.cjs <concept-folder>   (needs Playwright)
// Every page in each theme at 1440px; each main-language page at phone width; each entry of shots.json once, light, at 1440px.
// shots.json: [{ "page": "creators", "name": "empty", "query": "?state=empty", "click": "[data-act=add]" }]; query and click are optional.
// Long pages are cut into slices, because very tall images fail to open. Prints FAIL and exits 1 for an entry it cannot render.
const fs = require('fs'); const path = require('path'); const { execSync } = require('child_process');
function playwright() {
  const roots = [process.cwd(), ...(process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean)];
  try { const g = execSync('npm root -g', { encoding: 'utf8' }).trim(); roots.push(g, path.join(g, '@playwright/cli/node_modules')); } catch {}
  try { return require(require.resolve('playwright', { paths: roots })); }
  catch { console.error('Playwright not found. Run from a project that has it, or: npm i -g playwright && npx playwright install chromium'); process.exit(2); }
}
const root = path.resolve(process.argv[2] || '.'); const out = path.join(root, 'renders/check'); const SLICE = 1800;
const dir = fs.existsSync(path.join(root, 'src/pages')) ? path.join(root, 'src/pages') : path.join(root, 'src');
const pages = fs.readdirSync(dir).filter((f) => f.endsWith('.html')).sort().map((f) => ({ name: f.replace(/\.html$/, ''), rtl: /<html[^>]*\bdir=["']rtl["']/i.test(fs.readFileSync(path.join(dir, f), 'utf8')) }));
const list = fs.existsSync(path.join(root, 'shots.json')) ? JSON.parse(fs.readFileSync(path.join(root, 'shots.json'), 'utf8')) : [];
fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
const translation = (n) => /-[a-z]{2}$/.test(n) && pages.some((p) => p.name === n.slice(0, -3)); // creators-ar beside creators
const design = path.join(root, 'DESIGN.md'); const settings = fs.existsSync(design) && fs.readFileSync(design, 'utf8').match(/```json design-check\n([\s\S]*?)```/);
const themes = (settings && JSON.parse(settings[1]).themes) || ['light', 'dark'];
let count = 0; let failed = false;

async function shot(b, { page, label, width, scheme = 'light', query = '', click }) {
  const ctx = await b.newContext({ viewport: { width, height: width < 500 ? 844 : 900 }, colorScheme: scheme, isMobile: width < 500, hasTouch: width < 500, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  try {
    await p.goto(`file://${path.join(dir, page + '.html')}${query}`); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    if (click) { await p.click(click, { timeout: 3000 }); await p.waitForTimeout(400); }
    const height = await p.evaluate(() => document.documentElement.scrollHeight);
    if (click || height <= SLICE) { await p.screenshot({ path: path.join(out, `${label}.png`), fullPage: !click }); count++; }
    else for (let y = 0, i = 1, h = height; y < h; y += SLICE, i++) { // a page can change height while it is captured; a short tail joins the last slice
      h = await p.evaluate(() => document.documentElement.scrollHeight); const part = h - y < SLICE + 120 ? h - y : SLICE;
      await p.screenshot({ path: path.join(out, `${label}-part${i}.png`), fullPage: true, clip: { x: 0, y, width, height: part } }); count++; if (part > SLICE) break; }
  } catch (e) { console.log(`FAIL  ${label}: ${e.message.split('\n')[0]}`); failed = true; }
  await ctx.close();
}

(async () => {
  const b = await playwright().chromium.launch({ ignoreDefaultArgs: ['--hide-scrollbars'] });
  for (const { name } of pages) {
    for (const scheme of themes) await shot(b, { page: name, label: `${name}-${scheme}`, width: 1440, scheme });
    if (!translation(name)) await shot(b, { page: name, label: `${name}-phone`, width: 390 });
  }
  for (const e of list) await shot(b, { page: e.page, label: `${e.page}-${e.name}`, width: 1440, query: e.query, click: e.click });
  await b.close();
  console.log(`${failed ? 'FAIL' : 'PASS'}  ${count} screenshots in ${out}`); process.exit(failed ? 1 : 0);
})();
