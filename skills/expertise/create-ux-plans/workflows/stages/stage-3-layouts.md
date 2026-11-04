<stage name="3-layouts">

## Stage 3: UX-LAYOUTS.md

### Output
`.charter/UX-LAYOUTS.md` — Section 4 of the output template (Page Layouts, each with its page-level data states)

In a lean plan this is the last document, so it carries everything a designer or prototype needs per page: structure, fields, states and microcopy.

### Dependencies
Stages 1-2 verified and approved (IA + flows validated)

### Inputs (re-read from disk)
- Story map
- Constraint manifest (including the UX Brief)
- **UX-DESIGN-PLAN.md** (verified — page inventory and content priorities)
- **UX-FLOWS.md** (verified — user journeys inform layout decisions)
- **Data model** files listed in the brief, if any (only the parts the pages display)
- **Design system** files listed in the brief, if any (its component list)

### References to Load
- `references/responsive-patterns.md`
- `references/data-states.md`

### Context7 Query (if constrained platform)
Query for: available layout components (grids, lists, forms, dashboards), field types, maximum fields per view, grouping/section capabilities, conditional visibility support.

Append findings to constraint manifest under `## Stage-Specific Constraints > ### Stage 3 Constraints`.

### Generation Instructions

#### Section 4: Page Layouts

For each page in the IA inventory, create a text-based wireframe specifying:

- **Content zones** and their placement
- **Element ordering** and reading flow
- **Spatial relationships** using abstract spacing (XS, S, M, L, XL)
- **Zone priority mapping** (which zones get P1/P2/P3/P4 content — from IA)
- **Field specifications** for data-displaying pages (field name, type, source, allowed values)
- **Data states** for the page (see below)

**Base tier from the brief.** Specify the brief's primary device in full as the base tier, then state what each other tier *changes* (not a full re-specification). The base tier gets the full specification because it is where most of the product's use happens; describing it as a reduced version of another tier hides decisions.

```
**Base tier ([primary device]):**
[Text-based wireframe showing content zones, element order, spatial relationships]

**[Other tier] changes:** [what changes]
**[Other tier] changes:** [what changes]
```

**Fields from the data model.** If the brief lists a data model, take each field's name, type and allowed values from it and cite where it comes from (table and column, or API schema property). If a page needs a field the model does not have, list it under **Data-model gaps** at the end of the document instead of inventing a source. If the brief says "none", derive fields from the story map as before.

**Components from the design system.** If the brief lists a design system, name its existing components in the wireframes where one fits (e.g., "data table", "sheet", "select"), so later work maps the layout straight onto real parts.

**Page data states.** For every page that shows dynamic data, add a data-states block using the data-states reference: loading (pattern), empty (each applicable type: first-use, no-results, user-cleared), error (what happened + why + recovery), partial (if the page has more than one data source), and success feedback for the page's main actions. Write exact microcopy for each.

**Languages.** If the brief lists more than one language, write every microcopy string, button label and page title in each language. If one of them is right-to-left, add a short mirroring note per page: what flips (layout direction, directional icons, progress and step order) and what does not (numbers, codes, handles and URLs in Latin script, media controls). State once for the whole plan that each page's `lang` and `dir` follow the chosen language, and that mixed-direction content (a Latin handle or number inside right-to-left text) is isolated so it reads in the right order.

**Competitor patterns:** Where an element follows a Competitor Patterns row the user decided as Adopt or Adapt, cite its CP-ID next to the element. Rows decided as Skip are not used.

**Informed by flows:** The verified flows (Stage 2) tell you which pages users visit in sequence. Ensure adjacent pages in common flows have consistent navigation patterns and logical content progression.

**Platform constraint check:** If constrained platform, verify every layout element maps to an available platform component. Flag infeasible elements and propose alternatives.

### Verification Checks
- `page-name-consistency` (Check 1)
- `navigation-table-completeness` (Check 2)
- `button-label-consistency` (Check 3)
- `empty-state-coverage` (Check 7)

</stage>
