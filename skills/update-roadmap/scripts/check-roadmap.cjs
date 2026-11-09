// Checks roadmap/ after an update: the size limits, and that every line that left ACTIVE.md, QUEUE.md or LOG.md still exists.
// Usage: node check-roadmap.cjs [project-root] [--base <git-ref>]   Run before committing: it compares with the last commit (default HEAD).
// Exit codes: 0 pass, 1 fail, 2 could not run.
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');

const LIMITS = { 'ACTIVE.md': { lines: 200, kb: 40 }, 'QUEUE.md': { lines: 200, kb: 60 } };
const WATCHED = ['ACTIVE.md', 'QUEUE.md', 'LOG.md'];
const KEPT_WORDS = 0.7; // A changed line counts as edited, not lost, when one current line keeps this share of its words.

const args = process.argv.slice(2); const baseAt = args.indexOf('--base');
const base = baseAt >= 0 ? args.splice(baseAt, 2)[1] : 'HEAD';
const root = path.resolve(args[0] || '.'); const dir = path.join(root, 'roadmap');
if (!fs.existsSync(dir)) { console.error(`No roadmap/ folder in ${root}`); process.exit(2); }

const lines = (text) => text.split('\n').map((l) => l.trim()).filter((l) => /[\p{L}\p{N}].{10}/u.test(l));
const words = (l) => new Set(l.toLowerCase().match(/[\p{L}\p{N}]+/gu) || []);
const atBase = (name) => {
  try { return execFileSync('git', ['show', `${base}:roadmap/${name}`], { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], maxBuffer: 1 << 26 }); }
  catch { return null; }
};
const allMarkdown = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => {
  const p = path.join(d, e.name); return e.isDirectory() ? allMarkdown(p) : e.name.endsWith('.md') ? [p] : [];
});

try { execFileSync('git', ['rev-parse', '--verify', `${base}^{commit}`], { cwd: root, stdio: 'ignore' }); }
catch { console.error(`Not a git repository, or no commit at ${base}: cannot compare`); process.exit(2); }

let failed = false;
for (const [name, limit] of Object.entries(LIMITS)) {
  const file = path.join(dir, name); if (!fs.existsSync(file)) continue;
  const text = fs.readFileSync(file, 'utf8'); const count = text.split('\n').length - 1; const kb = Buffer.byteLength(text) / 1024;
  const over = count > limit.lines || kb > limit.kb; failed ||= over;
  console.log(`${over ? 'FAIL' : 'PASS'}  ${name}: ${count} lines (limit ${limit.lines}), ${kb.toFixed(1)} KB (limit ${limit.kb})`);
}

const everywhere = new Set(allMarkdown(dir).flatMap((f) => lines(fs.readFileSync(f, 'utf8'))));
const lost = []; let moved = 0; let edited = 0;
for (const name of WATCHED) {
  const before = atBase(name); if (before === null) continue;
  const file = path.join(dir, name); const now = fs.existsSync(file) ? lines(fs.readFileSync(file, 'utf8')) : [];
  const stillHere = new Set(now); const nowWords = now.map(words);
  for (const line of lines(before)) {
    if (stillHere.has(line)) continue;
    if (everywhere.has(line)) { moved++; continue; }
    const had = words(line);
    if (nowWords.some((w) => [...had].filter((x) => w.has(x)).length / had.size >= KEPT_WORDS)) { edited++; continue; }
    lost.push(`${name}: ${line.slice(0, 120)}`);
  }
}
failed ||= lost.length > 0;
console.log(`${lost.length ? 'FAIL' : 'PASS'}  Lines since ${base}: ${moved} moved, ${edited} edited in place, ${lost.length} lost`);
for (const l of lost.slice(0, 40)) console.log(`      LOST ${l}`);
if (lost.length > 40) console.log(`      … and ${lost.length - 40} more`);
process.exit(failed ? 1 : 0);
