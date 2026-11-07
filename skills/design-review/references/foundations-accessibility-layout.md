# Foundations: accessibility, interaction, layout, right to left

Yes/no checks. "Yes" passes. Walk the groups the target touches. Every value comes from the concept's DESIGN.md, which the skill reads first; a check names the section, never the value.

The tag after each ID says what the target must include to answer the check: `see` (a picture is enough), `source` (needs the HTML, CSS or TSX), `product` (needs product code). SKILL.md says which tags each input gets.

Each line ends with its source: a DESIGN.md section, a Material page (key below), and `auto N` when `scripts/check.cjs` check N already tests it on the mockups.

**M3** before a question means Material decides when DESIGN.md has no rule on it (severity: Advisory; SKILL.md says how to apply it). If DESIGN.md has a rule, DESIGN.md is right.

| Key | Material page |
|---|---|
| contrast | https://m3.material.io/foundations/designing/color-contrast |
| structure | https://m3.material.io/foundations/designing/structure |
| flow | https://m3.material.io/foundations/designing/flow |
| elements | https://m3.material.io/foundations/designing/elements |
| designing | https://m3.material.io/foundations/designing/overview |
| usability | https://m3.material.io/foundations/usability/overview |
| states | https://m3.material.io/foundations/interaction/states/overview |
| layers | https://m3.material.io/foundations/interaction/states/state-layers |
| applying | https://m3.material.io/foundations/interaction/states/applying-states |
| inputs | https://m3.material.io/foundations/interaction/inputs |
| selection | https://m3.material.io/foundations/interaction/selection |
| bp | https://m3.material.io/foundations/layout/breakpoints/overview |
| expanded | https://m3.material.io/foundations/layout/breakpoints/expanded |
| spacing | https://m3.material.io/foundations/layout/grids-spacing/spacing |
| density | https://m3.material.io/foundations/layout/grids-spacing/density |
| panes | https://m3.material.io/foundations/layout/scaffold/panes |
| list-detail | https://m3.material.io/foundations/layout/canonical-examples/list-detail |
| supporting | https://m3.material.io/foundations/layout/canonical-examples/supporting-pane |
| rtl | https://m3.material.io/foundations/layout/bidirectionality-rtl |
| resizing | https://m3.material.io/foundations/writing/text-resizing |
| fab-a11y | https://m3.material.io/components/floating-action-button/accessibility |
| chips-a11y | https://m3.material.io/components/chips/accessibility |
| nav-bar | https://m3.material.io/components/navigation-bar/guidelines |

## Contrast and state cues

- **FA-1** `see` Does every text reach 4.5:1 (3:1 at 24px and up) on its real background, in each theme, with only disabled controls exempt? Does muted text stay off the fills §2 rules out? *DESIGN.md §2, §9.1; contrast; auto 1 (1440px only)*
- **FA-2** `see` Do fields, checkboxes and switch tracks reach 3:1 with the control outline token? *DESIGN.md §2, §9.2; contrast; auto 2*
- **FA-3** `see` Are selected and invalid states shown by a second cue, never colour alone (hover is the state layer alone, §4), as "Selected, second cue" lists them? *DESIGN.md §4 "Selected, second cue"; states*

## Page structure

- **FA-4** `source` Is there one `banner` (top bar), one `main`, one `search`, and one `contentinfo` if a footer exists, and does each repeated landmark have its own label without the role word in it? *DESIGN.md §5 names table "Page"; structure*
- **FA-5** `source` Is there one H1 (the page title), with headings going down one level at a time? *DESIGN.md §5 names table "Page"; structure*
- **FA-6** `source` Does source order match reading order (and its mirror in right-to-left pages)? *structure*
- **FA-7** `see` Is the most used action easy to find, and are items of the same level side by side? *structure*

## Targets

- **FA-8** `source` On touch (390px), is every control at least the touch size §4 sets (fields and pills grow, checkboxes and icon buttons get a hit area, a switch's whole row is its target)? *DESIGN.md §4 "Click and tap areas", §9.3; structure; auto 3*
- **FA-9** `source` With a mouse (1440px), is every control at least the mouse size §4 sets? *DESIGN.md §4, §9.3; auto 3*

## Keyboard and focus

- **FA-10** `product` Can every journey on the screen be finished with the keyboard alone? *DESIGN.md §5 names table; flow*
- **FA-11** `product` M3 Is initial focus defined per screen, on the control for the most common goal (a search field on a search page)? *flow*
- **FA-12** `product` When a panel, dialog or menu opens, does focus move in, and on close return to the control that opened it? *DESIGN.md §5 names table "Panel, dialog, menu"; flow, panes*
- **FA-13** `product` Does Escape close every open menu, dialog, panel and tooltip, without clearing typed text? *DESIGN.md §5 (Tooltip, names table); inputs*
- **FA-14** `product` Is each complex widget (chart, segmented switch, single-choice pills, tabs) one Tab stop with arrow keys inside? *DESIGN.md §6 "Hover, tap, keyboard"; flow*
- **FA-15** `product` Does every element Tab reaches show the focus ring §4 sets, in its variant on dark or filled surfaces? In product code, do the real controls behind anything the mockup draws as a plain element show it too? *DESIGN.md §4 "Keyboard focus", §9.4; states; auto 4 (mockup elements that are focusable)*
- **FA-16** `product` Is no focus ring ever hidden under the pinned top bar, the selection bar or a toast? *DESIGN.md §5 Top bar; fab-a11y*
- **FA-17** `product` If the screen has keyboard shortcuts: do they use two keys, or work only while their component has focus, and are they listed? *flow*

## Accessible names

- **FA-18** `source` Does every icon-only control have a name that says its purpose, matching any visible label? *DESIGN.md §5 Icon button, names table; elements*
- **FA-19** `source` Where an action repeats on a screen (Save, More actions, View), does each name include its object ("Save Jane Doe")? *DESIGN.md §5 Icon button; elements*
- **FA-20** `source` Is no name repeating its role ("Close button")? *elements*
- **FA-21** `source` Are decorative icons hidden from assistive technology, and meaningful ones (status icons, brand marks with no word beside them) named? *DESIGN.md §5 names table "Platform counts"; elements*
- **FA-22** `source` Is every interactive element a native control or given the role in DESIGN.md's names table? *DESIGN.md §5 names table; designing*

## Interaction states

- **FA-23** `source` Do hover and pressed layers follow §4 "Interaction states" at its fixed values, one layer at a time? M3: if anything can be dragged, does it use a 16% layer? *DESIGN.md §4 "Interaction states"; layers*
- **FA-24** `source` Is a disabled control at the opacity §4 sets, with no hover, not clickable, and (M3) not focusable? *DESIGN.md §4; applying, layers*
- **FA-25** `see` M3 Are actions that can never be used on this screen hidden, rather than shown disabled? *applying*
- **FA-26** `source` Do containers (top bar, cards that are not clickable, dialogs) take no hover, focus or pressed state themselves, so at most one element is hovered and one pressed? *applying*
- **FA-27** `source` M3 Do links and rows that open a detail page show the hand cursor (Tailwind v4 gives buttons the arrow)? *inputs*
- **FA-28** `product` Can every sideways strip (carousel, segmented switch on a phone, scrolling table) scroll with the mouse wheel and a sideways trackpad swipe? *inputs*
- **FA-29** `product` Does Enter submit the search and the form that has focus? *inputs*
- **FA-30** `see` M3 Where selection is the main job (a working list), are row checkboxes always shown; where it is secondary (results), do they show on hover, stay once one is ticked, and always show on touch? *selection*

## Navigation

- **FA-31** `see` Does the top bar mark exactly one current page, with an underline (not colour alone) and `aria-current="page"`, with one navigation component per screen and size? *DESIGN.md §5 Top bar, names table; selection, nav-bar*
- **FA-32** `see` Do navigation labels show as text and never truncate or shrink, even at 200% text? *DESIGN.md §8 "Truncation"; nav-bar*

## Layout and widths

- **FA-33** `source` Is there no sideways scroll at any width from 360 to 1920px, including 720px (1440px at 200% zoom), and no scrollbar showing inside the page at rest (a panel that scrolls on its own shows its bar only on hover or focus; an open menu may keep one)? *DESIGN.md §9.9; bp; auto 9 (390, 720, 900, 1440, 1920)*
- **FA-34** `source` When the layout changes with width, do swapped parts do the same job (never a button turned into a chip)? Do navigation, search and filters change at the widths §5 sets, with nothing lost? *DESIGN.md §5 Top bar, Filter pill; bp*
- **FA-35** `see` M3 Is reading text (bios, notes, briefs, help) held to about 40–60 characters a line? *bp*
- **FA-36** `product` M3 Is a compact table a choice the person makes, never switched on by width, with text size and targets unchanged? *density, chips-a11y*
- **FA-37** `see` Are filters, sorting and the selection bar inside the pane they act on, outside the collection, and do they apply to every item? *expanded*
- **FA-38** `product` M3 Going back from a detail page to a list, are the list's scroll position, filters and selection kept? *list-detail*
- **FA-39** `see` M3 If a detail view opens beside the list: is the chosen row marked and there no back button; in the one-pane view, a back button and no mark; with nothing chosen, a useful empty state? *list-detail*
- **FA-40** `source` M3 On a phone, does a supporting panel become full screen or a bottom sheet rather than a narrow side panel? *bp, supporting*

## Text resizing

- **FA-41** `product` With text at 200% (product sets type in `rem`), does all text stay visible with no overlap or clipping, in every language, including fixed-height fields in the tallest script? *DESIGN.md §3 "Line height", "Type scale"; resizing; partly auto 9 (720px width, not 2× font size)*
- **FA-42** `product` When text grows, does padding stay as drawn while containers grow or reflow, and does any scroll it causes run up and down only? *DESIGN.md §3; resizing*

## Grouping and placement

- **FA-43** `see` Are related items grouped by space or a card, and unrelated ones clearly apart? *spacing*
- **FA-44** `see` Are photos and icons at the start of rows aligned and the same size on every row? *DESIGN.md §5; spacing*
- **FA-45** `see` Is each action next to the content it affects, and do key actions sit in the same place on every page? *spacing*

## Right to left (when §7 says the concept has it)

- **FA-46** `see` Is the whole layout mirrored with start and end (navigation, panel from the inline end, reading from top right), with no left/right padding or margins? *DESIGN.md §7; rtl*
- **FA-47** `source` Are handles, emails, phones, percentages and Latin numbers isolated left to right, the handle alone and not its whole line? *DESIGN.md §7; rtl*
- **FA-48** `source` Do names, bios, notes and captions sit in `<bdi>` in every language, with no `dir="auto"` on containers? *DESIGN.md §7; constitution; rtl*
- **FA-49** `see` Are things that show direction mirrored (back and forward arrows, trend arrows, time axes, carousel drift, progress bars and steps filling from the right), and brand marks, photos, numbers, clock and refresh icons not? *DESIGN.md §6 "Arabic", §7; rtl*
- **FA-50** `see` Does a filter pill's remove × sit at the end side? *DESIGN.md §5 Filter pill; rtl*
- **FA-51** `see` Is all interface text translated (handles, emails and Latin numbers stay as they are), and does each role use the font, case and letter-spacing §3 and §7 set for that script? *DESIGN.md §3, §7, §9.12*
