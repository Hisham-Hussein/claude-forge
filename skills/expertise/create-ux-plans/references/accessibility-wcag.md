<overview>
Per-component WCAG 2.1/2.2 AA accessibility patterns for embedding directly into UX plan component specifications. Covers semantic HTML, ARIA roles/states, keyboard interaction, focus management, and abstract contrast specification.
</overview>

<first_rule>
Use native HTML elements before ARIA. `<button>` is inherently focusable, keyboard-activatable, and announced as "button" — adding `role="button"` to a `<div>` requires replicating all of this manually. Prescribe HTML elements, not just roles.
</first_rule>

<component_patterns>

## Cards

- APG Pattern: None — use semantic HTML only
- Each card: `<article>` element
- Card sets: `<ul>` / `<ol>` with `<li>` per card (screen readers announce "list, N items")
- Card title: Heading element (e.g., `<h3>`) as accessible name via `aria-labelledby`
- Container: `aria-label` describing the collection (e.g., "Hook catalog")
- Clickable card: Single `<a>` on title with `::after` stretched to cover full card area — avoids wrapping entire card in `<a>`
- Secondary interactive elements: Separate focusable elements; never nest `<a>` inside `<a>`
- Decorative images: `alt=""`; content images: descriptive `alt`
- Metadata (stars, date): Must have text content or `aria-label` — not icon-only
- Keyboard: Tab to card link, Enter to activate; minimize tab stops per card (one is ideal)

## Card Grids

**Grid vs List Decision:**
- **Use `<ul>` list** (default): Cards with single primary link, browsing/scanning use case
- **Use `role="grid"`**: Only when 2D arrow-key navigation AND multiple interactive elements per cell are essential

If Grid Pattern Is Used:
- Container: `role="grid"` with `aria-labelledby` or `aria-label`
- Rows: `role="row"`; Cells: `role="gridcell"` per card
- Focus: Roving tabindex — one cell `tabindex="0"`, others `tabindex="-1"`
- Arrow keys between cells; Home/End: first/last in row; Ctrl+Home/End: first/last in grid

## Filter Chips / Toggle Buttons

**Pattern Selection:**
- Multi-select (AND/OR, multiple active): `role="toolbar"` + toggle buttons with `aria-pressed`
- Single-select (one at a time): `role="radiogroup"` + `role="radio"` buttons
- Fewer than 3 chips: Individual buttons with `aria-pressed`, no toolbar

**Toolbar Keyboard Model:**

| Key | Action |
|-----|--------|
| Tab | Enter toolbar (focus first or last-focused chip) |
| Shift+Tab | Exit toolbar |
| Left/Right Arrow | Move focus between chips |
| Home | Focus first chip |
| End | Focus last chip |
| Space / Enter | Toggle chip's pressed state |

- `aria-live="polite"` region announcing aggregate state: "3 filters applied" or "Showing 12 of 24 hooks"
- Active state: Must use multiple visual signals (not color alone) — background, border, icon (checkmark), or text weight

## Badges / Status Indicators

- Purely decorative: `aria-hidden="true"`
- Informational (e.g., "New", star count): Must have text content accessible to screen readers
- Icon-only: Require `aria-label` or visually-hidden text span
- Dynamic (notification counts): `aria-live="polite"`
- Contrast: Text 4.5:1 against badge background; badge shape 3:1 against page background (non-text contrast, WCAG 1.4.11)

## Navigation Bar

**Pattern Selection:**
- Website navigation (page links): `<nav>` with Disclosure pattern (preferred)
- Application-style menus (actions/commands): Menubar pattern (complex, rarely needed)

**Disclosure Navigation:**
- Container: `<nav>` with `aria-label="Main navigation"`
- Links: `<a>` in `<ul>` / `<li>` structure
- Current page: `aria-current="page"` on active link
- Submenus: `<button>` trigger with `aria-expanded`, controlling nested `<ul>`
- Skip link: "Skip to main content" as first focusable element targeting `<main id="...">`

**Keyboard:** Tab between links; Enter activates; Space/Enter on submenu trigger toggles `aria-expanded`; Escape closes submenu

## Hero Section

- Container: `<section>` with `aria-labelledby` pointing to hero heading
- Heading: `<h1>` for page title (visual size via CSS, not heading level)
- Subtitle: `<p>`, NOT a heading element
- Background images: CSS `background-image` (decorative, no alt needed)
- Text over images: Ensure contrast; consider semi-transparent overlay
- CTA: Descriptive link/button text (not "Click here" or "Get Started")
- Auto-playing animations/video: Must have pause control (WCAG 2.2.2)

## Modals / Dialogs

Most ARIA-intensive common pattern.

**Focus Management:**
1. On open: Focus moves to first focusable element inside dialog
2. Focus trap: Tab/Shift+Tab cycle only through elements inside modal
3. On close: Focus returns to the trigger element

**ARIA:**
- Container: `role="dialog"` (or `<dialog>` element)
- `aria-labelledby` → dialog title; `aria-describedby` → dialog content
- Background: `aria-hidden="true"` on rest of page (or `inert` attribute)

**Keyboard:** Tab cycles inside; Shift+Tab reverse cycles; Escape closes and returns focus to trigger

## Forms

- Every input: Associated `<label>` via `for` attribute (or wrapping)
- Required fields: `aria-required="true"` + visual indicator (not asterisk alone)
- Errors: `aria-describedby` linking input to error text; `aria-invalid="true"` when invalid
- Error summary: `role="alert"` or `aria-live="assertive"` at top of form
- Groups: `<fieldset>` with `<legend>` for radio buttons, checkbox groups, related fields
- Inline validation: Announce errors on blur (not every keystroke)
- Form-level validation: Announce on submit; move focus to first error or error summary

</component_patterns>

<aria_pattern_tiers>

## Tier 1: Nearly Every Application

| Pattern | Use Case | Key ARIA |
|---------|----------|----------|
| Disclosure | Expandable sections, nav submenus, FAQs | `aria-expanded`, `aria-controls` |
| Dialog (Modal) | Confirmations, forms, detail views | `role="dialog"`, focus trap |
| Button (Toggle) | Filters, settings, on/off | `aria-pressed` |
| Landmark Regions | Page structure | `<nav>`, `<main>`, `<aside>`, `<footer>` |

## Tier 2: Content-Rich Applications

| Pattern | Use Case | Key ARIA |
|---------|----------|----------|
| Toolbar | Grouped controls (filter bars) | `role="toolbar"`, roving tabindex |
| Tabs | Tabbed content panels | `role="tablist"`, `role="tab"`, `role="tabpanel"` |
| Listbox | Custom select inputs | `role="listbox"`, `role="option"`, `aria-selected` |
| Combobox | Autocomplete, search suggestions | `role="combobox"`, `aria-autocomplete` |

## Tier 3: Specialized

| Pattern | Use Case | Key ARIA |
|---------|----------|----------|
| Grid | Data tables, 2D navigable layouts | `role="grid"`, `role="gridcell"` |
| Menubar | Application-style menus | `role="menubar"`, `role="menuitem"` |
| Tree | Hierarchical navigation | `role="tree"`, `role="treeitem"` |
| Feed | Infinite scroll content | `role="feed"`, `role="article"` |

## Live Regions

| Attribute | Urgency | Use Case |
|-----------|---------|----------|
| `aria-live="polite"` | Low — wait for pause | Filter result counts, status updates |
| `aria-live="assertive"` | High — interrupt | Error messages, critical alerts |
| `role="alert"` | High (implies assertive) | Form errors, system errors |
| `role="status"` | Low (implies polite) | Success messages, progress updates |

</aria_pattern_tiers>

<focus_management>

## Three Core Focus Patterns

### 1. Focus Trap
**When:** Modal dialogs, full-screen overlays, any UI blocking background interaction.
- Tab cycles forward through focusable elements inside container
- Shift+Tab cycles backward; focus wraps at boundaries
- Escape exits trap and returns focus to trigger
- **Critical:** Must always have escape mechanism. Trap with no exit violates WCAG 2.1.2 (No Keyboard Trap)

### 2. Roving Tabindex
**When:** Composite widgets — toolbars, tab lists, radio groups, grid cells.
- Widget is a **single tab stop** in page tab order
- Arrow keys move focus between items within widget
- Only currently focused item has `tabindex="0"`; all others `tabindex="-1"`
- Widget remembers last-focused item on re-entry
- Tab/Shift+Tab exits the widget
- **Alternative:** `aria-activedescendant` — container keeps DOM focus while visually indicating active descendant

### 3. Focus Return
**When:** After any action that removes/hides the focused element.
- Modal closes: Focus returns to trigger element
- Item deleted: Focus moves to next item (or previous if last)
- Disclosure collapses: Focus stays on trigger button
- Submenu closes: Focus returns to parent menu item
- **Anti-pattern:** Focus disappearing to `<body>` — forces keyboard user to Tab from page top

## Focus Indicator Requirements

| Criterion | Level | Requirement |
|-----------|-------|-------------|
| 2.4.7 Focus Visible | AA | Visible focus indicator must exist |
| 1.4.11 Non-text Contrast | AA | Focus indicator 3:1 contrast against adjacent colors |
| 2.4.11 Focus Not Obscured | AA (2.2) | Focused component not entirely hidden by other content |
| 2.4.13 Focus Appearance | AAA (2.2) | Indicator area >= 2px perimeter; 3:1 contrast change |

Best practice: Aim for AAA (2.4.13) even when targeting AA.

</focus_management>

<contrast_specification>

## Three-Layer Contrast Model

| Requirement | WCAG SC | Ratio | Applies To |
|-------------|---------|-------|------------|
| Text contrast | 1.4.3 | 4.5:1 (normal) / 3:1 (large text) | All readable text |
| Non-text contrast | 1.4.11 | 3:1 | UI components (buttons, inputs, icons, borders) and graphical objects |
| Focus indicator contrast | 1.4.11 + 2.4.7 | 3:1 | Focus rings against adjacent colors |

"Large text" = 18pt (24px) or 14pt bold (18.66px bold).

## Abstract Specification Patterns

**Emphasis-Based:**
- High/medium/low emphasis text: Must meet 4.5:1 text contrast
- UI components (buttons, chips, inputs): Must meet 3:1 non-text contrast
- Decorative elements: No contrast requirement (marked `aria-hidden`)

**State-Based:**
- Default: UI boundary 3:1 against background
- Hover: Visually distinct (additional signal beyond color change)
- Active/Pressed: Clearly differentiated; 3:1 contrast
- Focus: Indicator 3:1 against adjacent colors
- Disabled: Exempt from contrast requirements but must be perceivable as disabled through non-color signals

**Color-Independence (WCAG 1.4.1):**
- No information conveyed through color alone
- Active filter chips: Differentiated by icon/weight/border — not solely color
- Status indicators: Text labels or icons alongside color coding
- Error states: Icon + text, not just red coloring

**Theme Constraint:** All contrast requirements apply independently in both light and dark themes.

</contrast_specification>

<touch_targets>

| Standard | Minimum Size | Level |
|----------|-------------|-------|
| WCAG 2.5.5 | 44 x 44 CSS px | AAA |
| WCAG 2.5.8 | 24 x 24 CSS px | AA (WCAG 2.2) |
| Apple HIG | 44 x 44 pt | Best Practice |
| Material Design | 48 x 48 dp | Best Practice |

WCAG 2.5.8 spacing exception: Targets < 24x24 allowed if a 24px-diameter circle centered on the target doesn't intersect adjacent targets. Inline text links are exempt.

</touch_targets>

<decision_rules>

## Key Decisions

1. **Grid vs List for card layouts**: Default to `<ul>` list. Only use `role="grid"` when 2D arrow-key navigation AND multiple interactive elements per cell are required.

2. **Toolbar vs individual buttons for filters**: Use `role="toolbar"` for 3+ chips (single tab stop, arrow navigation). Use individual buttons for < 3 chips.

3. **Multi-select vs single-select filters**: Multi-select -> `role="toolbar"` + `aria-pressed`. Single-select -> `role="radiogroup"` + `role="radio"`.

4. **Disclosure vs Menubar for navigation**: Use Disclosure for website navigation (links to pages). Use Menubar only for application-style menus (actions/commands).

5. **`<dialog>` vs custom `role="dialog"`**: Prefer native `<dialog>` with `.showModal()` — provides built-in focus trapping, backdrop, and Escape-to-close.

6. **One tab stop per composite widget**: Filter chips, tab lists, radio groups = single tab stop with internal arrow keys. This keeps page tab order short.

7. **aria-live debouncing**: If filters update results on every toggle, only announce the final state after ~300ms debounce, not intermediate states.

</decision_rules>

<anti_patterns>

- `role="button"` on a `<button>` (redundant)
- `aria-label` duplicating visible text (double announcement)
- `role="navigation"` on `<nav>` (redundant — `<nav>` implies it)
- `role="checkbox"` without `aria-checked` (missing required state)
- Wrapping entire card in `<a>` (screen reader reads all card content as link text)
- Icon-only display without `aria-label` or visually-hidden text
- Generic link text ("Read more") without context
- Focus disappearing to `<body>` after dynamic action
- Focus trap with no escape mechanism (violates WCAG 2.1.2)
- Announcing every intermediate filter state via `aria-live` (chatty)
- Skipping heading levels for visual sizing (use CSS instead)
- Color as sole differentiator for any state change

</anti_patterns>

<validation_checklist>

For every component in a UX plan, verify:

- [ ] Semantic HTML element specified (not just ARIA role)
- [ ] ARIA roles/states listed (only where native HTML insufficient)
- [ ] Keyboard interaction model defined (which keys do what)
- [ ] Focus management pattern identified (trap / roving / return)
- [ ] Accessible name specified (visible text, `aria-label`, or `aria-labelledby`)
- [ ] Contrast requirements stated abstractly (ratios + semantic roles)
- [ ] Color independence ensured (multiple signals for every state)
- [ ] Dynamic changes announce via appropriate `aria-live` level
- [ ] Touch target size meets tier-appropriate minimum
- [ ] Focus indicator visible with 3:1 contrast

</validation_checklist>
