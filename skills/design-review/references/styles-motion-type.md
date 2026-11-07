# Styles: colour, type, shape, depth, motion, icons, spacing, charts

Yes/no checks. "Yes" passes. Walk the groups the target touches. Every value comes from the concept's DESIGN.md, which the skill reads first; a check names the section, never the value.

The tag after each ID says what the target must include to answer the check: `see` (a picture is enough), `source` (needs the HTML, CSS or TSX), `product` (needs product code). SKILL.md says which tags each input gets.

Each line ends with its source: a DESIGN.md section, a Material page (key below), and `auto N` when `scripts/check.cjs` check N already tests it on the mockups.

**M3** before a question means Material decides when DESIGN.md has no rule on it (severity: Advisory; SKILL.md says how to apply it). If DESIGN.md has a rule, DESIGN.md is right.

Never ask for Material's look here: no tonal palettes, no Roboto, no Material Symbols, no tonal elevation, no 48dp sizes.

| Key | Material page |
|---|---|
| roles | https://m3.material.io/styles/color/roles |
| apply | https://m3.material.io/styles/color/advanced/apply-colors |
| c-system | https://m3.material.io/styles/color/system/how-the-system-works |
| scale | https://m3.material.io/styles/typography/type-scale-tokens |
| type | https://m3.material.io/styles/typography/applying-type |
| editorial | https://m3.material.io/styles/typography/editorial-treatments |
| corners | https://m3.material.io/styles/shape/corner-radius-scale |
| elevation | https://m3.material.io/styles/elevation/applying-elevation |
| springs | https://m3.material.io/styles/motion/overview/how-it-works |
| easing | https://m3.material.io/styles/motion/easing-and-duration/applying-easing-and-duration |
| m-tokens | https://m3.material.io/styles/motion/easing-and-duration/tokens-specs |
| transitions | https://m3.material.io/styles/motion/transitions/applying-transitions |
| patterns | https://m3.material.io/styles/motion/transitions/transition-patterns |
| icons | https://m3.material.io/styles/icons/applying-icons |
| i-design | https://m3.material.io/styles/icons/designing-icons |
| s-overview | https://m3.material.io/styles/spacing/overview |
| s-tokens | https://m3.material.io/styles/spacing/tokens |
| tokens | https://m3.material.io/foundations/design-tokens/overview |

## Colour

- **ST-1** `see` Does each fill appear only with its paired text, as §2's token table pairs them? *DESIGN.md §2; roles, apply*
- **ST-2** `see` Are container fills never used as text or icon colours? *DESIGN.md §2; roles*
- **ST-3** `source` Is every colour a token from DESIGN.md §2 (in product code the project's theme tokens), with no raw hex, no framework palette colour (`text-gray-500`) and no opacity trick beyond the derived layers §2 allows? *DESIGN.md §2 "No other colours"; constitution, §12; apply, tokens; partly auto 8 (only that DESIGN.md and the CSS agree)*
- **ST-4** `source` Does each outline use the token §2 gives its job (dividers and card borders, pills, fields and other controls)? *DESIGN.md §2; roles; contrast of controls auto 2*
- **ST-5** `see` Do meaning colours (good, warning, error) appear only where §2 allows them, never as decoration, and never taken from photos or chart colours? *DESIGN.md §1.3, §2; apply*
- **ST-6** `source` Does each region (top bar, page, cards, panels) keep the same colour role at every width? *roles*
- **ST-7** `see` Do inverse surfaces use the inverse set only: inverse fill, its paired text, and the inverse button variants of §5? *DESIGN.md §5 Button variants; roles*
- **ST-8** `source` If §2 maps a component library's variables, is each one set as the table says, hover and skeleton layers included? *DESIGN.md §2, §5 Loading*
- **ST-9** `product` M3 With the OS "more contrast" or forced-colours setting, do boundaries stay visible and selected states still show when fills are removed? *c-system*

## Type

- **ST-10** `source` Is every text size on the type scale (each script's steps), and in product code set in `rem`? *DESIGN.md §3 "Type scale", §9.6; scale; auto 6 (sizes, not the unit)*
- **ST-11** `see` Does each font family do the one job §3 gives it, in every script? *DESIGN.md §3*
- **ST-12** `see` M3 Do neighbouring levels of hierarchy differ by more than one small step (not 15 vs 14 for title vs body)? *scale*
- **ST-13** `source` Do line heights follow §3 "Line height" for reading, display and each script? *DESIGN.md §3 "Line height"; type, scale*
- **ST-14** `see` Does no fixed-height control (fields, search, pills) clip the tallest script? *DESIGN.md §3; scale*
- **ST-15** `see` Are light weights used only at the sizes §3 allows, never for reading or small text? *DESIGN.md §3; editorial*
- **ST-16** `see` Are number columns right-aligned in tabular figures? M3: do counts, credits, stats and chart tooltips use tabular figures too? *DESIGN.md §5 Data table; type*
- **ST-17** `see` Do links look as §4 sets, never shown by colour alone? *DESIGN.md §4; type*
- **ST-18** `see` Are large display sizes used only for what §3 lists, the same way on every screen? *DESIGN.md §3; editorial*

## Shape and depth

- **ST-19** `source` Is every corner one of §4's shape tokens, full rounding only where §4 puts it? *DESIGN.md §4 "Corners"; corners*
- **ST-20** `see` M3 Where a rounded element sits close inside a rounded container, is its radius about outer minus gap, not the same value? *corners*
- **ST-21** `see` Is depth shown only the ways §4 "Depth" allows, shadows included? *DESIGN.md §1.5, §4 "Depth"; elevation*
- **ST-22** `see` Does every dialog and panel sit on the scrim §2 and §4 set? *DESIGN.md §2, §4; elevation*
- **ST-23** `see` Does the interface stay clear of everything §1 rules out? *DESIGN.md §1.6*

## Motion

- **ST-24** `product` Do state changes use the duration and easing in §4's Motion table, with no overshoot or bounce unless §4 asks for it? *DESIGN.md §4 "Motion"; springs, m-tokens*
- **ST-25** `product` Do entering parts decelerate and leaving parts accelerate at §4's durations, leaving always shorter than entering? *DESIGN.md §4 Motion table; easing*
- **ST-26** `product` Does each transition move on one axis from the edge where the part lives (panel from the inline end, toast from the bottom, menus from their trigger), mirrored in Arabic? *DESIGN.md §5 Panel, Toast, §7; patterns*
- **ST-27** `product` M3 Does old content fade out before new content fades in, with no long cross-fade? *transitions*
- **ST-28** `product` M3 When data arrives, does it replace a skeleton of the same shape with a quick fade and no layout shift? *DESIGN.md §5 Loading (shape only); patterns*
- **ST-29** `product` With reduced motion on, do looping motions stop and do slides and scales become short fades, so nothing jump-cuts? *DESIGN.md §4, §9.10; transitions; auto 10 (looping motion at load only, not open and close transitions)*

## Icons

- **ST-30** `see` Are all icons from the set §4 names, at its size and stroke, in the text colour, with brand marks as §4 says? *DESIGN.md §4 "Icons", §11; icons, i-design*
- **ST-31** `see` Is each icon centred on the line of the text beside it? *icons*
- **ST-32** `see` M3 In dark, do icons and text look no heavier than in light (by eye, on the `-dark` renders)? *icons, editorial*

## Spacing

- **ST-33** `source` Is every margin, padding and gap on §4's spacing scale, and do page margin, content width and section gaps match §4? *DESIGN.md §4 "Spacing", §9.5; s-tokens; auto 5 (the steps)*
- **ST-34** `source` Is space inside a group set with padding and gap on the parent, not margins on children? *s-overview*

## Charts

- **ST-35** `see` Does colour follow §6's fixed series order, ordered categories its ramp, never colour by rank? *DESIGN.md §6*
- **ST-36** `see` Can every chart be read without colour: direct labels or a legend with values, printed bar values, a table view? Are values in text colours, not the series colour? *DESIGN.md §6*
- **ST-37** `see` Are marks, grid and labels as §6 sets them, at any width? *DESIGN.md §6, §9.7; label size auto 7*
- **ST-38** `source` On phones, does each chart follow §6? *DESIGN.md §6 "Phones"*
- **ST-39** `see` Do forecasts and headline figures, where a chart has them, follow §6? *DESIGN.md §6*
