# Building the prototype

```
<concept>/
├── DESIGN.md
├── DESIGN-REVIEW.md   signed by design-review
├── AGREED-LIST.md
├── OUTSIDE-CHECK.md
├── shots.json         what shots.cjs renders
├── inspiration-<source>/
├── src/
│   ├── pages/         HTML only
│   ├── css/           tokens.css, components.css
│   ├── js/            behaviour, one file per concern
│   ├── data/          sample data, wording
│   └── assets/        fonts/, photos/
├── renders/           screenshots
└── standalone/        the one-file prototype
```

Organise it as a good front-end developer would, with one job per file. In the settings block, `src` is `src/pages` and `css` is `src/css/tokens.css`. In Product first the screens live in the project's stack instead.

## What every screen needs

- **One source of style.** Tokens and components sit in `src/css/`, so a change reaches every screen. Pages carry no styles of their own.
- **Tokens exactly as DESIGN.md §2:** the same names and values, in a `:root` block, then `:root[data-theme="dark"]`, and `:root:not([data-theme="light"])` inside a device-dark media query.
- **Fonts self-hosted, open licence.** No outside requests, so a page opens anywhere.
- **Each language is its own page:** `<page>.html`, and `<page>-ar.html` (or the language's code) with `dir="rtl"` on `<html>` for right-to-left languages.
- **Clickable like the real product:** plain `<a href="other-page.html">` between pages, a language link, a theme switch that carries from page to page, menus, panels and dialogs that really open. Anything with no page yet says so; no dead links.
- **Real states:** whatever the list names is reachable, through a "Demo state" selector on the page and by URL (`?state=empty`), so a script can render it. Read the URL with `new URLSearchParams(window.PROTOTYPE_SEARCH ?? location.search)`, which also works in the stand-alone file.
- **Real images when the look uses them.** If the inspiration's look rests on photography, the screens need photographs: use the project's own, or open-licence stock saved in `assets/`, and record the source in §10. Grey silhouettes, tinted tiles and initials in place of photos remove the look itself, so they count as unfinished. Images in the sample data are shared across runs, like the data.
- **Density without losing the look.** Dense content is where concepts collapse into a generic admin kit. Keep the inspiration's scale and air: the title at its display size, rows with room, one line per cell. Put secondary data behind a column setting or into the detail view if the plan allows it, rather than shrinking everything. A cell that wraps to three lines, or a name cut in the middle, is a defect.
- **Asset paths as plain strings** in HTML, CSS, JS and data (`../assets/photos/a.jpg`), never put together at run time, so the stand-alone build can find them.
- **Focus rings as `outline`**, since check 4 reads it, and motion that stops with reduced motion.
- **Motion from the inspiration, built:** if the study found scroll or load animation, the prototype has it.

Then add the selectors to the settings block in DESIGN.md §9, naming this concept's classes. Write `shots.json` with every state, dialog and menu on the list:

```json
[{ "page": "creators", "name": "empty", "query": "?state=empty" },
 { "page": "creators", "name": "add-to-list", "click": "[data-act=add]" }]
```

Then run `scripts/shots.cjs` and `scripts/bundle.cjs`.

## Finished means

Every item on `AGREED-LIST.md`, in every language and theme, with nothing marked "later" or filled with placeholder text.
