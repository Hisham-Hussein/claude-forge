// Sign a passed review: adds DESIGN.md's hash to <concept>/DESIGN-REVIEW.md. Usage: node stamp.cjs <concept-folder>
// The hash leaves out the settings block, which is filled in during the build. hooks/design-gate.mjs reads it.
const fs = require('fs'); const path = require('path'); const { createHash } = require('crypto');
const root = path.resolve(process.argv[2] || '.'); const design = path.join(root, 'DESIGN.md'); const review = path.join(root, 'DESIGN-REVIEW.md');
if (!fs.existsSync(design) || !fs.existsSync(review)) { console.error('Need DESIGN.md and DESIGN-REVIEW.md in ' + root); process.exit(2); }
const hash = createHash('sha256').update(fs.readFileSync(design, 'utf8').replace(/```json design-check\n[\s\S]*?```/, '')).digest('hex');
const text = fs.readFileSync(review, 'utf8').replace(/\n?design-md-sha256: \w+\n?/g, '\n').trimEnd();
fs.writeFileSync(review, `${text}\n\ndesign-md-sha256: ${hash}\n`); console.log('Signed', review);
