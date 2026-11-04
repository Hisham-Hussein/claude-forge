<stage name="4-components">

## Stage 4: UX-COMPONENTS.md

### Output
`.charter/UX-COMPONENTS.md` — Section 5 of the output template (Component Specifications)

### Dependencies
Stages 1-3 verified (IA + flows + layouts available). Runs at full depth only; a lean plan skips Stages 4-6.

### Inputs (re-read from disk)
- Story map
- Constraint manifest (including the UX Brief)
- **UX-DESIGN-PLAN.md** (page inventory, visual hierarchy)
- **UX-FLOWS.md** (which components appear in which flows)
- **UX-LAYOUTS.md** (which components are placed where)
- **Design system** files listed in the brief, if any (component list and state rules)

### References to Load
- `references/atomic-design.md`
- `references/data-states.md`

### Context7 Query (if constrained platform)
Query for: available UI component types, component state support (hover, focus, active, disabled), conditional formatting capabilities, button/action types, input field types and validation options.

Append findings to constraint manifest under `## Stage-Specific Constraints > ### Stage 4 Constraints`.

### Generation Instructions

#### Section 5: Component Specifications

**If the brief lists a design system,** start with a **component inventory**: a table of every element in the layouts, the design-system component it uses, the pages it is used in (PG-XXX), and its source (SM-XXX). The design system already defines those components' interaction states, focus and keyboard behaviour; restating them creates a second source that drifts. Then write full specifications (below) only for:
- components the design system does not have, and
- existing components used with product-specific behaviour (for example, a table whose rows can be selected for a bulk action): specify only the added behaviour and states.

**If the brief says "none",** specify every component as below.

Organize the full specifications by Atomic Design hierarchy:
- **Atoms:** Indivisible building blocks (buttons, badges, icons, inputs, text elements)
- **Molecules:** Functional groups of atoms (search bar, card header, metadata row, chip)
- **Organisms:** Complex page sections (card grid, filter section, hero, navigation bar)

**Derive components from layouts:** Every element in a layout wireframe must map to a component spec or an inventory row. Every component spec must trace to a layout that uses it.

For each component, use the **state applicability matrix** from atomic-design reference. Document ALL applicable states:

| State | Visual Description | Behavior |
|-------|-------------------|----------|
| Default | [appearance at rest — emphasis-based, not pixel values] | [user affordance] |
| Hover | [emphasis change] | [feedback purpose] |
| Focus | [focus ring, 3:1 contrast] | [keyboard interaction] |
| Active | [pressed appearance] | [action result] |
| Disabled | [reduced emphasis] | [why disabled, how to enable] |
| Selected | [selection indicator] | [selection behavior] |
| Loading | [skeleton/spinner] | [what triggers load] |
| Error | [error indicator] | [error message + recovery] |
| Empty | [empty indicator] | [CTA to populate] |

Only include states applicable to the component type (per matrix).

**Accessibility inline:** For each component, specify semantic HTML element, ARIA attributes, and keyboard behavior. This is per-component, not a separate section.

**Trace everything:** Each component links to SM-XXX / US-XXX via its Purpose field, and lists the pages it appears on in a **Used in: PG-XXX** line (the consistency check that every page has component coverage reads it).

**Button tables:** Every button in the layouts needs a defined behaviour, including buttons built from design-system components (the design system defines how a button looks and responds, not what it does in this product). Write two tables, which the verify, review and update workflows read:
- **Button automation table:** location (PG-XXX), label, trigger, what the system does, result in the UI, error handling, confirmation (for destructive actions).
- **Navigation buttons table:** from (PG-XXX), label, to (PG-XXX).

**Platform constraint check:** If constrained platform, verify each component maps to an available platform component type. Replace infeasible components with platform-native alternatives and document the trade-off.

### Verification Checks
- `button-target-consistency` (Check 4)
- `component-pattern-assignment` (Check 5)
- `status-value-consistency` (Check 6)

</stage>
