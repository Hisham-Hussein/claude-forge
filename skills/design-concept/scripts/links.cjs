// Check a prototype's links without a browser. Usage: node links.cjs <concept-folder> [<pages-folder>]
// Every local href and src in the page files must reach a file, and every #anchor an id on that page.
const fs = require('fs'); const path = require('path');
const root = path.resolve(process.argv[2] || '.'); const dir = process.argv[3] ? path.join(root, process.argv[3]) : fs.existsSync(path.join(root, 'src/pages')) ? path.join(root, 'src/pages') : path.join(root, 'src');
const pages = fs.readdirSync(dir).filter((f) => f.endsWith('.html')); const bad = []; let links = 0;
const read = (f) => fs.readFileSync(f, 'utf8');
const hasId = (html, id) => new RegExp(`\\bid=["']${id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}["']`).test(html);
for (const page of pages) { const html = read(path.join(dir, page));
  for (const [, attr, value] of html.matchAll(/\b(href|src)=["']([^"']*)["']/g)) {
    if (/^(https?:|mailto:|tel:|data:|javascript:)/.test(value)) continue;
    links++;
    if (attr === 'href' && (value === '' || value === '#')) { bad.push(`${page}: dead link href="${value}"`); continue; }
    const [file, anchor] = value.split('#'); const target = file ? path.resolve(dir, decodeURI(file.split('?')[0])) : path.join(dir, page);
    if (!fs.existsSync(target)) { bad.push(`${page}: ${value} not found`); continue; }
    if (anchor && target.endsWith('.html') && !hasId(read(target), anchor)) bad.push(`${page}: ${value} has no such id`);
  }
}
const review = path.join(root, 'DESIGN-REVIEW.md'); // Look first only: Product first builds in the project's stack
if (fs.existsSync(path.join(root, 'AGREED-LIST.md')) && !(fs.existsSync(review) && read(review).includes('design-md-sha256:'))) bad.push('DESIGN-REVIEW.md is missing or unsigned: design-review never passed this DESIGN.md');
console.log(`${bad.length ? 'FAIL' : 'PASS'}  links: ${pages.length} pages, ${links} local links, ${bad.length} bad`);
bad.slice(0, 40).forEach((x) => console.log('      ' + x));
process.exit(bad.length ? 1 : 0);
