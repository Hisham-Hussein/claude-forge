<stage name="3-layouts">

## Stage 3: UX-LAYOUTS.md

### Output
`.charter/UX-LAYOUTS.md` — Section 4 of the output template (Page Layouts)

### Dependencies
Stages 1-2 verified and approved (IA + flows validated)

### Inputs (re-read from disk)
- Story map
- Constraint manifest
- **UX-DESIGN-PLAN.md** (verified — page inventory and content priorities)
- **UX-FLOWS.md** (verified — user journeys inform layout decisions)

### References to Load
- `references/responsive-patterns.md`

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

Use **mobile-first specification**: describe mobile fully as base tier, then state what each wider tier *adds* (not a full re-specification).

```
**Base tier (mobile):**
[Text-based wireframe showing content zones, element order, spatial relationships]

**Tablet adds:** [what changes]
**Desktop adds:** [what changes]
```

**Informed by flows:** The verified flows (Stage 2) tell you which pages users visit in sequence. Ensure adjacent pages in common flows have consistent navigation patterns and logical content progression.

**Platform constraint check:** If constrained platform, verify every layout element maps to an available platform component. Flag infeasible elements and propose alternatives.

### Verification Checks
- `page-name-consistency` (Check 1)
- `navigation-table-completeness` (Check 2)
- `button-label-consistency` (Check 3)

</stage>
