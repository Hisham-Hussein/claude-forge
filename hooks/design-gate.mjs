// Gate for design-concept: nothing gets built in a concept folder until design-review has passed its DESIGN.md.
// A concept folder is one holding AGREED-LIST.md; outside those this hook does nothing.
//  - Calling the design-review skill leaves a marker for the session.
//  - DESIGN-REVIEW.md, and stamp.cjs which signs it, are refused without that marker.
//  - Screens (src/) and build commands are refused until DESIGN-REVIEW.md carries the hash of the current DESIGN.md.
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { basename, dirname, isAbsolute, join, relative, resolve } from 'node:path';

const input = JSON.parse(readFileSync(0, 'utf8') || '{}');
const { tool_name: tool, tool_input: args = {}, session_id: session = 'none', cwd = process.cwd() } = input;
const marker = join(tmpdir(), 'claude-design-gate', String(session).replace(/\W/g, '_'));
const refuse = (why) => { process.stderr.write(`design-gate: ${why}\n`); process.exit(2); };

const conceptOf = (p) => { for (let d = resolve(cwd, p); d !== dirname(d); d = dirname(d)) if (existsSync(join(d, 'AGREED-LIST.md'))) return d; return null; };
export const designHash = (md) => createHash('sha256').update(md.replace(/```json design-check\n[\s\S]*?```/, '')).digest('hex');
const passed = (concept) => {
  const design = join(concept, 'DESIGN.md'); const review = join(concept, 'DESIGN-REVIEW.md');
  if (!existsSync(design) || !existsSync(review)) return false;
  return readFileSync(review, 'utf8').includes(`design-md-sha256: ${designHash(readFileSync(design, 'utf8'))}`);
};
const needReview = (concept) => `${concept} has no passed design review for its current DESIGN.md. Run the claude-forge:design-review skill on it first; it signs DESIGN-REVIEW.md. Nothing is built before that.`;
const needSkill = 'DESIGN-REVIEW.md is written only by the claude-forge:design-review skill. Run that skill with the Skill tool first.';

if (tool === 'Skill') {
  if (/(^|:)design-review$/.test(String(args.skill))) { mkdirSync(dirname(marker), { recursive: true }); writeFileSync(marker, new Date().toISOString()); }
  process.exit(0);
}

if (['Write', 'Edit', 'MultiEdit', 'NotebookEdit'].includes(tool)) {
  const file = args.file_path || args.notebook_path; if (!file) process.exit(0);
  const concept = conceptOf(dirname(resolve(cwd, file))); if (!concept) process.exit(0);
  if (basename(file) === 'DESIGN-REVIEW.md') { if (!existsSync(marker)) refuse(needSkill); process.exit(0); }
  if (relative(concept, resolve(cwd, file)).split('/')[0] === 'src' && !passed(concept)) refuse(needReview(concept));
  process.exit(0);
}

if (tool === 'Bash') {
  const command = String(args.command || '');
  const paths = command.split(/[\s;|&()<>'"=]+/).filter((t) => t.includes('/'));
  const concept = [cwd, ...paths].map((p) => conceptOf(isAbsolute(p) ? p : resolve(cwd, p))).find(Boolean);
  if (!concept) process.exit(0);
  if (/DESIGN-REVIEW\.md|stamp\.cjs/.test(command) && !/^\s*(cat|grep|ls|head|tail)\b/.test(command) && !existsSync(marker)) refuse(needSkill);
  if (passed(concept)) process.exit(0);
  const others = command.replace(/\b(node\s+)?\S*skills\/(design-review|design-concept)\/scripts\/\S+/g, ''); // the skills' own capture, check and render scripts run before the review
  const writesSrc = /(>|\btee\b|\bcp\b|\bmv\b|\brsync\b|\bsed\s+-i|\bmkdir\b|\btouch\b|\bln\b|\bunzip\b|\btar\b)[^;&|]*\bsrc\b/.test(command);
  const runsCode = /(^|[\s;&|(])(node|python3?|deno|bun|npx|npm|pnpm|sh|bash|zsh|perl|ruby)\s/.test(others);
  if (writesSrc || runsCode) refuse(needReview(concept));
}
process.exit(0);
