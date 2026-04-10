<stage name="1-design-plan">

## Stage 1: UX-DESIGN-PLAN.md

### Output
`.charter/UX-DESIGN-PLAN.md` — Sections 1-3 of the output template (`templates/ux-design-plan-template.md`)

### Dependencies
Stage 0 complete (constraint manifest and story map available)

### Inputs (re-read from disk)
- Story map (path from generation status manifest)
- User stories (if available)
- Constraint manifest (`.charter/UX-CONSTRAINTS.md`)

### References to Load
- `references/visual-hierarchy.md`
- `references/interaction-patterns.md`

### Context7 Query (if constrained platform)
Query for: maximum pages/views supported, navigation model limitations, layout grid constraints, available component types.

Append findings to constraint manifest under `## Stage-Specific Constraints > ### Stage 1 Constraints`.

### Generation Instructions

#### Section 1: Overview & Design Principles

Derive from the story map:
- **Product summary:** 1-2 sentences — what is this product and who is it for
- **Guiding UX principles:** 3-5 principles specific to THIS product (not generic heuristics). Each states why it matters for these users.

#### Section 2: Information Architecture

**Story-map-to-IA transformation algorithm:**

For each backbone activity, apply in order:
1. Does this activity require a different layout than the previous? → New page
2. Does the user perform this in a different temporal context? → New page
3. Does the content volume exceed what fits as a section? → New page
4. Would separating this break the user's flow? → Keep as section

Activities that are purely external (e.g., "go to GitHub") → link/CTA actions, not pages.

**Build page inventory** using the template's Section 2 format:
- Page ID (PG-XXX), Page Name, Source Activity (SM-XXX), Page Type (listing/detail/form/dashboard/landing), Nav Level
- Content priority per page (P1 through P4)
- Entry and exit points (from story map horizontal flow)

**Select navigation model** per-section using the decision matrix from interaction-patterns reference:
- Content directory → filtered view
- SaaS dashboard → hub-and-spoke
- E-commerce → hierarchical
- Multi-step form → sequential

**Flag gaps:**
- Orphan activities (not mapped to any page) → IA gaps
- Pages with no source activity → potentially unnecessary

**Platform constraint check:** If constrained platform, verify page count and navigation model are feasible against Stage 1 constraints. Adjust and document if needed.

#### Section 3: Visual Hierarchy Map

Create the role-based + semantic hierarchy table. For each text and UI element assign:
- **Role-based name** (e.g., card-title, filter-label, page-title)
- **Type role** (heading-1 through heading-6, body, body-small, caption, label, overline, display, code) — from visual-hierarchy reference
- **Emphasis level** (high, medium, low, disabled)

Order from highest to lowest emphasis across the entire product.

Select a **scanning pattern** per page (F-pattern, Z-pattern, layer-cake, spotted) based on content density. Map content to scan zones.

### Verification Checks
- `story-id-consistency` (Check 8 from verify-ux-consistency.md)

</stage>
