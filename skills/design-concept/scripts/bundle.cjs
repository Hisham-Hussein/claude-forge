// Build the one-file prototype: <concept>/standalone/<concept>.html. Usage: node bundle.cjs <concept-folder> [<first-page>]
// Every page, with its CSS and JS, and every asset once. The file shows one page at a time in a frame and follows links, so it opens anywhere.
const fs = require('fs'); const path = require('path');
const root = path.resolve(process.argv[2] || '.'); const src = path.join(root, 'src');
const dir = fs.existsSync(path.join(src, 'pages')) ? path.join(src, 'pages') : src;
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]));
const TYPES = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.gif': 'image/gif', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.otf': 'font/otf' };
const assets = Object.fromEntries(walk(src).filter((f) => TYPES[path.extname(f).toLowerCase()]).map((f) => [path.relative(src, f), { type: TYPES[path.extname(f).toLowerCase()], data: fs.readFileSync(f).toString('base64') }]));
const noEnd = (s) => s.replace(/<\/script/gi, '<\\/script');
const pages = {};
for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.html'))) {
  let html = fs.readFileSync(path.join(dir, f), 'utf8');
  html = html.replace(/<link[^>]*rel=["']stylesheet["'][^>]*>/gi, (tag) => { const href = tag.match(/href=["']([^"']+)/)?.[1]; const file = href && path.resolve(dir, href); return file && fs.existsSync(file) ? `<style>${fs.readFileSync(file, 'utf8')}</style>` : tag; });
  html = html.replace(/<script([^>]*)\bsrc=["']([^"']+)["']([^>]*)><\/script>/gi, (tag, a, href, b) => { const file = path.resolve(dir, href); return fs.existsSync(file) ? `<script${a}${b}>${noEnd(fs.readFileSync(file, 'utf8'))}</script>` : tag; });
  pages[f.replace(/\.html$/, '')] = html;
}
const names = Object.keys(pages).sort(); const first = process.argv[3] || names.find((n) => !/-ar$/.test(n)) || names[0];
const shell = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${path.basename(root)}</title>
<style>html,body,iframe{margin:0;width:100%;height:100%;border:0;display:block}</style></head><body><iframe id="f" title="Prototype"></iframe>
<script type="application/json" id="pages">${noEnd(JSON.stringify(pages))}</script><script type="application/json" id="assets">${noEnd(JSON.stringify(assets))}</script>
<script>
const pages = JSON.parse(document.getElementById('pages').textContent), assets = JSON.parse(document.getElementById('assets').textContent), frame = document.getElementById('f');
const urls = Object.entries(assets).map(([p, a]) => { const bytes = Uint8Array.from(atob(a.data), (c) => c.charCodeAt(0)); return [p, URL.createObjectURL(new Blob([bytes], { type: a.type }))]; }).sort((a, b) => b[0].length - a[0].length);
const esc = (s) => s.replace(/[.*+?^\${}()|[\\]\\\\]/g, '\\\\$&');
const patched = {}; const withAssets = (n) => patched[n] ??= urls.reduce((h, [p, u]) => h.replace(new RegExp('[\\\\w./-]*' + esc(p), 'g'), u), pages[n]);
function open(name, search) {
  const script = '<script>window.PROTOTYPE_SEARCH=' + JSON.stringify(search || '') + ';<\\/script>';
  frame.srcdoc = withAssets(name).replace(/<head[^>]*>/i, (m) => m + script);
}
frame.addEventListener('load', () => { const doc = frame.contentDocument; if (!doc) return;
  doc.addEventListener('click', (e) => { const a = e.target.closest && e.target.closest('a[href]'); if (!a) return;
    const m = a.getAttribute('href').match(/([^/?#]+)\\.html(\\?[^#]*)?/); if (!m || !pages[m[1]]) return;
    e.preventDefault(); open(m[1], m[2]); }); });
open(${JSON.stringify(first)}, location.search);
</script></body></html>`;
fs.mkdirSync(path.join(root, 'standalone'), { recursive: true });
const file = path.join(root, 'standalone', `${path.basename(root)}.html`); fs.writeFileSync(file, shell);
console.log(`PASS  ${names.length} pages, ${Object.keys(assets).length} assets, ${(fs.statSync(file).size / 1048576).toFixed(1)} MB: ${file}`);
