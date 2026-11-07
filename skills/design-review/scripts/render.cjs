// Render every page of a concept to full-page PNGs in <concept>/renders: <page>.png and <page>-dark.png.
// Usage: node render.cjs <concept-folder> [--design path/to/DESIGN.md]   Reports broken images and sideways scroll.
const fs = require('fs'); const path = require('path');
const { playwright, args, settings, pages } = require('./shared.cjs');
const { root, design } = args(process.argv.slice(2));
const s = settings(fs.readFileSync(design, 'utf8')) || { src: 'src', themes: ['light', 'dark'] };
const out = path.join(root, 'renders'); fs.mkdirSync(out, { recursive: true });
(async () => {
  const b = await playwright().chromium.launch();
  for (const scheme of s.themes) {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 }, colorScheme: scheme });
    for (const page of pages(root, s)) {
      const file = `${page.name}${scheme === 'light' ? '' : '-' + scheme}.png`;
      await p.goto(page.url); await p.evaluate(() => document.fonts.ready);
      await p.evaluate(() => Promise.all([...document.images].map((i) => (i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; })))));
      const broken = await p.evaluate(() => [...document.images].filter((i) => !i.naturalWidth).length);
      const sideways = await p.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
      console.log(file, '| broken images:', broken, '| sideways scroll:', sideways);
      await p.screenshot({ path: path.join(out, file), fullPage: true });
    }
    await p.close();
  }
  await b.close();
})();
