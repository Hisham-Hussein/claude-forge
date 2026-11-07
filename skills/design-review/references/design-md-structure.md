# The structure of a DESIGN.md

Every concept's DESIGN.md has these eleven numbered sections, in this order. The review checks cite them by number, so a number never moves. A section that does not apply stays, with one line saying so (`## 7. Right to left` — "Not used: this product ships left to right only"). `scripts/check.cjs --structure` tests the headings, the named rules and the settings block; the review judges whether the content is enough for someone to build from.

| § | Heading | Must hold |
|---|---|---|
| 1 | Principles | What the design stands for, and what it rules out |
| 2 | Colour | A token table, one row per token: `` | `--name` | `light` | `dark` | job | ``, with `same` in the dark column when both themes match. Text and fill pairs. Which fills muted text stays off. Where meaning colours may appear. What other colours are allowed (derived layers). If the project uses a component library, the map from its variables to these tokens |
| 3 | Type | Each family's one job, per script, with weights. **Line height** rule. **Type scale** in px per script, with what each step is for |
| 4 | Shape, space, depth, motion | **Corners** (tokens and what uses each). **Spacing** (scale, page margin, content width, section gaps). **Depth**. **Motion** (a table of durations and easing, reduced motion). **Keyboard focus** (the ring and its variant on dark fills). **Click and tap areas** (mouse and touch sizes). **Interaction states** (hover, pressed, focus, selected, disabled, invalid, the second cue). **Clickable or not**. **Icons** (set, size, stroke) |
| 5 | Components | One table: component, mockup class, what the product uses, rules. Button variants. **Names for assistive technology** (the role and name of each component). Loading, empty, error and save states |
| 6 | Charts | Series colours and their order, ordered ramp, marks, grid, label sizes, reading without colour, hover and keyboard, phones, right to left |
| 7 | Right to left | Mirroring, what does not mirror, isolating Latin text, per-script rules |
| 8 | Content | Voice, case, numbers, dates, missing-value mark, messages, truncation |
| 9 | Checklist | The numbered checks every screen passes, then the settings block below |
| 10 | Open items | What is not finished or not decided. The review never reports these |
| 11 | Where we depart from Material 3 on purpose | Each departure with its reason. The review never reports these |

A header above §1 says where the concept came from: its inspiration, the reference CSS, the screens. With an inspiration, it also holds a numbered **Signatures** list: the three to six moves that make that look itself, and how each shows on a product screen.

## The settings block

`check.cjs` and `render.cjs` read one fenced block in §9. Its values repeat §3 and §4 in a form a script can use; a mismatch between them is a Major finding.

````markdown
```json design-check
{
  "css": "src/app.css",
  "spacing": [0, 4, 8, 12, 16, 24, 32, 48, 64],
  "type": { "ltr": [12, 14, 16, 20, 28, 40], "rtl": [13, 15, 17, 20, 28, 40] },
  "targets": { "mouse": 24, "touch": 44 },
  "selectors": { "controls": ".pill, .field" }
}
```
````

Required: `css` (from the concept folder; holds the tokens), `spacing`, `type` (`rtl` only with right-to-left pages).

Optional, with their defaults: `src` (`"src"`, the folder of `*.html` pages; `"src/pages"` when pages have their own folder), `themes` (`["light", "dark"]`), `targets` (24 and 44), `chartTextMin` (10.5), `hitAreas` (selector to the px a hit area adds past the mark), `selectors`:

| Key | Lists |
|---|---|
| `controls` | Controls beyond `button` and `a` that must reach the target sizes |
| `controlRows` | Rows whose whole height is the control's target |
| `controlOutlines` | Controls identified by their outline (non-text contrast) |
| `controlFills` | Controls identified by their fill, such as switch tracks |
| `controlsDrawnForShow` | Demo copies skipped by the non-text check |
| `disabled` | The class the mockups use for disabled |
| `textOnMedia` | Text on photos and decorative layers, skipped by the contrast check |
| `skipSpacing` | Elements skipped by the spacing check |
| `charts` | SVG charts (`svg.chart`) |

What the CSS must have: tokens in the first `:root` block; with a dark theme, a `:root[data-theme="dark"]` block and a `:root:not([data-theme="light"])` block inside the device-dark media query, holding the same values. Mockup focus rings are outlines, since check 4 reads `outline`.
