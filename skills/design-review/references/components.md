# Components

Yes/no checks. "Yes" passes. Walk the groups the target touches. Every value comes from the concept's DESIGN.md, which the skill reads first; a check names the section, never the value.

The tag after each ID says what the target must include to answer the check: `see` (a picture is enough), `source` (needs the HTML, CSS or TSX), `product` (needs product code). SKILL.md says which tags each input gets.

Each line ends with its source: a DESIGN.md section, a Material page (key below), and `auto N` when `scripts/check.cjs` check N already tests it on the mockups.

**M3** before a question means Material decides when DESIGN.md has no rule on it (severity: Advisory; SKILL.md says how to apply it). If DESIGN.md has a rule, DESIGN.md is right.

Walk only the components the target uses, named as in DESIGN.md §5. A component §5 does not list has no checks here: use its Material page.

If §10 says the mockups draw some controls as plain elements, judge those against §5's names table and do not report "span is not a button".

Material keys are `https://m3.material.io/components/<name>/<tab>`; for example `buttons/guidelines` = https://m3.material.io/components/buttons/guidelines. Exceptions: `all-buttons` = https://m3.material.io/components/all-buttons; `usability` = https://m3.material.io/foundations/usability/overview.

## Buttons

- **CO-1** `see` Is there one main-action button per area, and one obvious main action on the page? *DESIGN.md §5 Button; all-buttons, usability*
- **CO-2** `see` Is each label 1–3 words, in §8's case, on one line, never truncated, naming its result ("Add to list", not "OK")? *DESIGN.md §8; buttons/guidelines*
- **CO-3** `see` Does each button have at most one icon, before the label? *DESIGN.md §5 Button; buttons/guidelines*
- **CO-4** `see` Are paired buttons side by side when there is room, in the same order at every width, and never stretched into a long bar on wide screens? *buttons/guidelines*
- **CO-5** `see` Does every text-only button read as a button, not as body text or a link? *DESIGN.md §4 "Clickable or not"; buttons/guidelines*
- **CO-6** `see` Are outline and text-only buttons kept off photos? *buttons/guidelines*
- **CO-7** `see` Are inverse variants used only on inverse surfaces? Do destructive actions use §5's destructive look and ask in a dialog first? *DESIGN.md §5 Button variants*

## Icon button

- **CO-8** `source` Does every icon button have an `aria-label` naming the action, shown as a tooltip on hover and focus with the same text? *DESIGN.md §5 Icon button; icon-buttons/accessibility, tooltips/guidelines*
- **CO-9** `see` Does a toggled state (Saved) change the icon as well as the fill, with `aria-pressed`? *DESIGN.md §4, §5; icon-buttons/guidelines*
- **CO-10** `see` Is the toggle form used only for actions with a real on state? *icon-buttons/overview*
- **CO-11** `see` Is the icon at least 3:1 against what is behind it? *icon-buttons/accessibility*

## Segmented switch, choice pills, tabs

- **CO-12** `see` Does each segmented switch hold two to five options of similar length, all text or all icons, on one line (scrolling sideways on a phone)? Over five, are they tabs or choice pills? *DESIGN.md §5 Segmented switch; segmented-buttons/guidelines*
- **CO-13** `source` Does a segmented switch set a value (radio group), while switching between views of a list uses tabs? *DESIGN.md §5 Segmented switch, Tabs, names table; segmented-buttons/accessibility, tabs/guidelines*
- **CO-14** `product` Do arrow keys move between options, Tab entering and leaving as one stop and landing on the chosen one (first, or rightmost in right-to-left pages, when none)? *DESIGN.md §5 names table; segmented-buttons/accessibility, radio-button/accessibility*
- **CO-15** `source` Do icon-only segments carry a name ("Grid view")? *segmented-buttons/accessibility*
- **CO-16** `see` M3 Does a single-choice group offer a way back to no choice (Any, All, Clear)? *radio-button/accessibility*
- **CO-17** `see` Do tabs show views of one list with counts ("Open 2"), the current one marked as §5 sets? Are counts four characters or fewer (999+) and read after the label? *DESIGN.md §5 Tabs; tabs/guidelines, badges/guidelines*
- **CO-18** `product` Do arrow keys move between tabs, with Space or Enter choosing? *tabs/accessibility*

## Chips, tags, filter pills

- **CO-19** `see` Does an outline mean clickable: interactive pills outlined, static tags and labels a fill or plain text, never an outline, and never mixed into one row with interactive pills? *DESIGN.md §4 "Clickable or not"; chips/accessibility*
- **CO-20** `see` Does a set filter pill show its label, the value and a remove × that is its own button named "Remove {name}", whose target does not overlap the pill's own? *DESIGN.md §5 Filter pill, names table; chips/guidelines*
- **CO-21** `product` Does pressing the pill open its editor, and does an "All filters" control open the panel so every filter is reachable when pills overflow or hide on narrow screens? *DESIGN.md §5 Filter pill; chips/guidelines, chips/accessibility*
- **CO-22** `see` Is each pill set either single or multiple choice, with chosen pills showing a checkmark? *DESIGN.md §4, §5 Choice pills; chips/guidelines*
- **CO-23** `see` Are pill labels short positive nouns (20 characters or fewer)? *chips/guidelines*
- **CO-24** `see` Are pills at least 8px apart, or the gap §5 sets? *DESIGN.md §5 Choice pills; chips/guidelines*
- **CO-25** `see` Is a pill never the step that completes a task? *chips/guidelines*
- **CO-26** `see` Do quality labels follow the number they judge, in their fixed colours? Does each status use its one look wherever it shows? *DESIGN.md §5 Quality label, Creator status*

## Checkbox and switch

- **CO-27** `see` Does select-all show a dash when some rows are ticked (`aria-checked="mixed"`) and tick all on click? *DESIGN.md §5 Checkbox, names table; checkbox/guidelines*
- **CO-28** `source` Is each checkbox named by its row, and does clicking the row's label toggle it? *DESIGN.md §5 names table; checkbox/accessibility*
- **CO-29** `see` Are checkboxes, not switches, used for lists of options and inside the filter panel (which applies on its footer button)? *checkbox/guidelines, switch/guidelines*
- **CO-30** `see` Does every switch take effect at once, never choose between two opposing views, and have a label on the start side saying what "on" does? *DESIGN.md §5 Switch; switch/guidelines, switch/accessibility*

## Text field, select, date, range

- **CO-31** `see` Does every field have a visible label above it (a real `<label>`), never only a placeholder? *DESIGN.md §5 Text field, names table; text-fields/guidelines*
- **CO-32** `see` M3 Are required fields marked with an explained asterisk that is part of the name? *text-fields/guidelines*
- **CO-33** `see` Does an invalid field show the error outline and a message under it with an alert icon, replacing any help text, saying how to fix it, linked with `aria-describedby` and `aria-invalid`? *DESIGN.md §4 Invalid, §5 names table; text-fields/guidelines, text-fields/accessibility*
- **CO-34** `see` Are form errors shown at the field, all at once, and only general failures (network) in an error state? *DESIGN.md §5 Error state; dialogs/guidelines*
- **CO-35** `source` Are trailing icon buttons in fields named by their job ("Clear search")? *text-fields/accessibility*
- **CO-36** `see` Is the unit or currency named once nearby ("Price · USD"), as a field suffix with a name when a field takes a price? *DESIGN.md §8 Numbers; text-fields/guidelines*
- **CO-37** `see` M3 Are read-only values shown as text, or as a field only when it says read-only? *text-fields/guidelines*
- **CO-38** `see` Are fields bounded in width on wide screens? *text-fields/guidelines*
- **CO-39** `product` Does a select open a menu with the chosen option ticked; a date field a calendar, showing §8's date format; a range two fields joined by "to"? *DESIGN.md §5 Select, date, range*
- **CO-40** `product` Can every date be typed without the calendar, with the format in help text, each day read in full, and Page Up/Down (Shift for years) moving months? *date-pickers/accessibility*

## Search

- **CO-41** `see` Does the search field start with the search icon, with hint text that says what can be searched and that is also its name? *DESIGN.md §5 Text field; search/guidelines, search/accessibility*
- **CO-42** `product` Are suggestions or results announced when they appear? *search/accessibility*
- **CO-43** `product` Can the person clear the query and close suggestions with Escape, and does the query stay in the field after the search? *search/guidelines*

## Menu

- **CO-44** `see` Does the menu follow §5 Menu (surface, outline, corners, depth), items with the hover layer, the chosen option ticked (not colour alone), a destructive item last in the error colour after a divider? *DESIGN.md §5 Menu; menus/accessibility*
- **CO-45** `product` Does focus go to the first item on open, with arrows, typeahead and Escape working, and Escape returning focus to the trigger? *DESIGN.md §5 names table; menus/accessibility*
- **CO-46** `see` Are unavailable items shown disabled, not removed? *menus/guidelines*
- **CO-47** `see` Does no menu item hold a second control (button, switch)? *menus/guidelines*
- **CO-48** `product` Does the trigger keep its look and show only its pressed state while open? *DESIGN.md §4 "Pressed, open menu"; menus/overview*
- **CO-49** `product` M3 On a phone, does a long menu become a sheet? *menus/guidelines*

## Card, data table, list row

- **CO-50** `see` Is each card either wholly clickable with no buttons inside, or a plain container whose buttons and links are each a Tab stop? Is a tile never clickable while also holding a button? *cards/guidelines*
- **CO-51** `source` Do only clickable cards and rows show a hover, at the layer §4 sets? *DESIGN.md §4, §5 Data table; cards/guidelines*
- **CO-52** `see` Does each table row have one selection control, the checkbox carrying the selection (not the row fill alone)? *DESIGN.md §5 Checkbox; lists/guidelines*
- **CO-53** `see` Do column heads use §3's label style, number columns sit right-aligned with units in the head, and the first column stay pinned on narrow screens as §5 sets? *DESIGN.md §5 Data table*
- **CO-54** `see` Do dividers group rather than split every item, with no screen of hairlines and borders everywhere? *divider/guidelines*

## Toast, notice, dialog, panel

- **CO-55** `see` Is each message in the right component: a dialog only for one blocking task or a risky confirmation; inline notices for success and errors at the place; toasts for short news? *DESIGN.md §5 Dialog, Notice, Toast; dialogs/guidelines*
- **CO-56** `see` Does the toast follow §5 Toast: one at a time, one line, no inline link, at most one action? Does a toast with Undo stay until used or dismissed, and one without close on its own with its news also on the page? *DESIGN.md §5 Toast; snackbar/guidelines*
- **CO-57** `product` Is the toast announced (role status) without taking focus, closable with Escape, reachable from the keyboard (M3: by a listed shortcut), and does it avoid covering the navigation, the selection bar, a panel's main action and the focused control? *DESIGN.md §5 names table; snackbar/accessibility*
- **CO-58** `see` Does each dialog have at most two actions: cancel (quiet, never disabled) before the main action (at the inline end, named for its result, disabled until a choice is made)? *DESIGN.md §5 Dialog; dialogs/guidelines, all-buttons*
- **CO-59** `product` Does focus start on the first field, stay inside, and Escape close the dialog? Do confirmations use the alert dialog role? Do title and buttons stay pinned when the content scrolls? *DESIGN.md §5 Dialog; dialogs/accessibility*
- **CO-60** `product` M3 Does closing a panel or dialog with unsaved changes ask before discarding? *dialogs/guidelines*
- **CO-61** `see` Do filters and work beside the page open in the panel, not a dialog? Is the panel at the width §5 sets, from the inline end, with a close button in its header, groups, a footer with clear and the main action showing the result count, scrolling up and down only, role `dialog`, beside at most two other panes? *DESIGN.md §5 Panel; side-sheets/guidelines*

## Tooltip

- **CO-62** `see` Is nothing that matters only in a tooltip? *DESIGN.md §5 Tooltip; tooltips/guidelines*
- **CO-63** `source` Is there no tooltip that repeats a label already shown (full text of truncated items excepted)? *tooltips/guidelines*
- **CO-64** `product` Is the tooltip anchored above its element (M3: 4px away), opening on hover, focus or a tap, role `tooltip`, referenced by its trigger, closed by Escape? *DESIGN.md §5 Tooltip; tooltips/guidelines, tooltips/accessibility*
- **CO-65** `product` M3 Does one tooltip show at a time, hiding about 1.5s after the pointer leaves? *tooltips/guidelines*

## Loading, progress, empty, error, save state

- **CO-66** `product` Does a load under 200ms show nothing and a longer one skeletons in the content's shape, one indicator per group rather than per item? *DESIGN.md §5 Progress, Loading; progress-indicators/guidelines*
- **CO-67** `see` Does every job over 5 seconds show what it is doing, a measured bar, "312 of 500 … about 4 minutes left", a way to stop, and that the person can leave the page? *DESIGN.md §5 Progress; progress-indicators/guidelines*
- **CO-68** `source` Does every loading indicator have a name saying what loads ("Loading results")? *progress-indicators/accessibility*
- **CO-69** `see` Does every data view have loading, empty and error states; empty saying why with ways out; error saying what failed, that work is kept, with Try again? *DESIGN.md §1.7, §5 Empty state, Error state, §9.13; constitution*
- **CO-70** `see` Does everything edited in place show its saving, saved and failed states as §5 Save state sets, and does a failed save revert? *DESIGN.md §5 Save state; constitution*

## Top bar, selection bar, filter row

- **CO-71** `see` Does the top bar hold what §5 Top bar lists, pinned, with at most two other page actions? *DESIGN.md §5 Top bar; app-bars/guidelines*
- **CO-72** `product` Does the phone menu close on choosing an item, Escape and an outside click, and return focus to the menu button? *DESIGN.md §5 Top bar; navigation-drawer/accessibility*
- **CO-73** `source` M3 Do the selection bar and the filter row use the `toolbar` role, with one emphasised action? *toolbars/accessibility*

## Carousel

- **CO-74** `see` Does the section head hold the "See all" link and the pause button, with nothing on the strip? *DESIGN.md §5 Carousel; carousel/guidelines*
- **CO-75** `source` Are duplicated tiles hidden from screen readers and the Tab order? *carousel/accessibility*
- **CO-76** `product` M3 Does focus land on the first tile, arrows move between tiles, and each tile say its position and the total? *carousel/accessibility*
- **CO-77** `product` Does the strip pause on hover, on focus inside and with its button, and stand fully still with reduced motion? *DESIGN.md §4 Motion; carousel/guidelines; auto 10 (still at load)*
