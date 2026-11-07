// Shared by check.cjs and render.cjs: find Playwright, read a concept's settings from its DESIGN.md, list its pages.
const fs = require('fs'); const path = require('path'); const { execSync } = require('child_process');

function playwright() {
  const roots = [process.cwd(), ...(process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean)];
  try { const g = execSync('npm root -g', { encoding: 'utf8' }).trim(); roots.push(g, path.join(g, '@playwright/cli/node_modules')); } catch {}
  try { return require(require.resolve('playwright', { paths: roots })); }
  catch { console.error('Playwright not found. Run from a project that has it, or: npm i -g playwright && npx playwright install chromium'); process.exit(2); }
}

function args(argv) {
  const pos = argv.filter((a, i) => !a.startsWith('--') && argv[i - 1] !== '--design');
  const root = path.resolve(pos[0] || '.'); const at = argv.indexOf('--design');
  return { root, design: at >= 0 ? path.resolve(argv[at + 1]) : path.join(root, 'DESIGN.md'), structureOnly: argv.includes('--structure') };
}

// §9 of DESIGN.md holds one fenced block, opened with ```json design-check
function settings(md) {
  const m = md.match(/```json design-check\n([\s\S]*?)```/);
  if (!m) return null;
  const s = JSON.parse(m[1]);
  return { src: 'src', themes: ['light', 'dark'], targets: { mouse: 24, touch: 44 }, chartTextMin: 10.5, ...s, selectors: { ...(s.selectors || {}) } };
}

function pages(root, s) {
  const dir = path.join(root, s.src);
  return fs.readdirSync(dir).filter((f) => f.endsWith('.html') && !f.includes('.standalone')).sort().map((f) => {
    const html = fs.readFileSync(path.join(dir, f), 'utf8');
    return { name: f.replace(/\.html$/, ''), url: 'file://' + path.join(dir, f), rtl: /<html[^>]*\bdir=["']rtl["']/i.test(html) };
  });
}

module.exports = { playwright, args, settings, pages };
