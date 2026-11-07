# Building the prototype

```
<concept>/
├── DESIGN.md
├── DESIGN-REVIEW.md   signed by design-review
├── AGREED-LIST.md
├── PLAN-MATCH.md      where a UX plan covers the screens
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
- **Tokens exactly as DESIGN.md §2:** the same names and values, in a `:root` block, then `:root[data-theme="dark"]`, and `:root:not([data-theme="light"])` inside a device-dark media query. With one theme, set `"themes": ["light"]` in the settings block and leave the dark blocks out.
- **Fonts self-hosted, open licence.** No outside requests, so a page opens anywhere.
- **Each language is its own page:** `<page>.html`, and `<page>-ar.html` (or the language's code) with `dir="rtl"` on `<html>` for right-to-left languages.
- **Clickable like the real product:** plain `<a href="other-page.html">` between pages, a language link, a theme switch that carries from page to page, menus, panels and dialogs that really open. Anything with no page yet says so; no dead links.
- **Real states:** whatever the list names is reachable, through a "Demo state" selector on the page and by URL (`?state=empty`), so a script can render it. Read the URL with `new URLSearchParams(window.PROTOTYPE_SEARCH ?? location.search)`, which also works in the stand-alone file.
- **Real images when the look uses them.** If the inspiration's look rests on photography, the screens need photographs: use the project's own, or open-licence stock saved in `assets/`, and record the source in §10. Grey silhouettes, tinted tiles and initials in place of photos remove the look itself, so they count as unfinished. Images in the sample data are shared across runs, like the data.
- **Density without losing the look.** Dense content is where concepts collapse into a generic admin kit. Keep the inspiration's scale and air: the title at its display size, rows with room, one line per cell. Put secondary data behind a column setting or into the detail view if the plan allows it, rather than shrinking everything. A cell that wraps to three lines, or a name cut in the middle, is a defect.
- **Asset paths as plain strings** in HTML, CSS, JS and data (`../assets/photos/a.jpg`), never put together at run time, so the stand-alone build can find them.
- **One visible scrollbar.** The page's own. An area that needs its own scroll, such as a filters rail, shows its bar only on hover or keyboard focus (`scrollbar-color: transparent transparent`, then a colour on `:hover` and `:focus-within`), and nothing scrolls sideways. Check 9 fails any other. An open menu may keep a thin bar. While a dialog or sheet is open, the page behind it does not scroll, and a long sheet scrolls as one piece, never cut at the bottom.
- **Every language all the way down.** Everything the product itself writes appears in the page's language, in menus and dialogs too, sample names such as cities and saved searches included. Only what creators or users wrote themselves stays as written.
- **Menus open by their control.** Below the control by default, scrolling the page a little if needed, as a native list does; inside the screen and under any fixed bar; a long one scrolls inside, with one scrollbar, never two. A disabled menu item shows its reason in the menu, not in a tooltip over the control.
- **No unstyled browser controls.** A `<select>` opens the browser's own plain list, which CSS cannot style and screenshots never show. Every dropdown opens a menu built in the concept's look (`preventDefault` on the select's `mousedown`, or a button and a menu); check 9 fails any that does not. The same goes for date pickers and file inputs.
- **Focus rings as `outline`**, since check 4 reads it, and motion that stops with reduced motion.
- **Motion from the inspiration, built:** if the study found scroll or load animation, the prototype has it.

Then add the selectors to the settings block in DESIGN.md §9, naming this concept's classes. Write `shots.json` with every state, dialog and menu on the list. Content inside a scrolling area, such as a filters rail, does not show in a page screenshot, so give it a shot of its own:

```json
[{ "page": "creators", "name": "empty", "query": "?state=empty" },
 { "page": "creators", "name": "add-to-list", "click": "[data-act=add]" }]
```

Then run `scripts/shots.cjs` and `scripts/bundle.cjs`.

## Finished means

Every item on `AGREED-LIST.md`, in every language and theme, with nothing marked "later" or filled with placeholder text.
