# Building the prototype

```
<concept>/
├── DESIGN.md
├── AGREED-LIST.md
├── inspiration-<source>/
├── src/         pages, one CSS file for tokens and components, one JS file
├── assets/      fonts, photos
└── renders/     screenshots (from design-review's render.cjs)
```

This is the layout design-review's scripts expect. In Product first the screens live in the project's stack instead.

## What every screen needs

- **One source of style.** All tokens and components sit in the one CSS file, so a change reaches every screen. Pages carry no styles of their own.
- **Tokens exactly as DESIGN.md §2:** the same names and values, in a `:root` block, then `:root[data-theme="dark"]`, and `:root:not([data-theme="light"])` inside a device-dark media query.
- **Fonts self-hosted, open licence.** No outside requests, so a page opens anywhere.
- **Each language is its own page:** `<page>.html`, and `<page>-ar.html` (or the language's code) with `dir="rtl"` on `<html>` for right-to-left languages.
- **Clickable like the real product:** plain `<a href="other-page.html">` between pages, a language link, a theme switch that carries from page to page, menus, panels and dialogs that really open. Anything with no page yet says so; no dead links.
- **Real states:** whatever the list names is reachable by URL (`?state=empty`), so a script can render it. Nothing on the page shows that switch: no demo footer or selector in the screenshots.
- **Real images when the look uses them.** If the inspiration's look rests on photography, the screens need photographs: use the project's own, or open-licence stock saved in `assets/`, and record the source in §10. Grey silhouettes, tinted tiles and initials in place of photos remove the look itself, so they count as unfinished. Images in the sample data are shared across runs, like the data.
- **Density without losing the look.** Dense content is where concepts collapse into a generic admin kit. Keep the inspiration's scale and air: the title at its display size, rows with room, one line per cell. Put secondary data behind a column setting or into the detail view if the plan allows it, rather than shrinking everything. A cell that wraps to three lines, or a name cut in the middle, is a defect.
- **Screens read as the product.** No notes to the reviewer, no "sample data" labels, no line saying figures are invented.
- **Focus rings as `outline`**, since check 4 reads it, and motion that stops with reduced motion.
- **Motion from the inspiration, built:** if the study found scroll or load animation, the prototype has it.

Then fill in the settings block in DESIGN.md §9 so its selectors name this concept's classes.

## Finished means

Every item on `AGREED-LIST.md`, in every language and theme, with nothing marked "later" or filled with placeholder text.
