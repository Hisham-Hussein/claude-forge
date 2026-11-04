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
- Competitor research files the brief lists, if any

### References to Load
- `references/visual-hierarchy.md`
- `references/interaction-patterns.md`
- `references/competitor-research.md` (only when the brief lists competitor research)

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
- Page ID (PG-XXX), Page Name, Source Stories (the SM-XXX stories or activities the page serves), Page Type (listing/detail/form/dashboard/landing), Nav Level
- Content priority per page (P1 through P4)
- An **entry points** table (where users arrive, from the story map horizontal flow) and a **navigation table** (every link between pages: from, label, to), in the template's Section 2 format. The consistency checks and the update workflow read both tables.

**Select navigation model** per-section using the decision matrix from interaction-patterns reference:
- Content directory → filtered view
- SaaS dashboard → hub-and-spoke
- E-commerce → hierarchical
- Multi-step form → sequential

**Competitor patterns:** If the brief lists competitor research, read it and write the **Competitor Patterns** table at the end of Section 2, following `references/competitor-research.md`: one row per pattern that serves an in-scope story, with a recommendation (Adopt / Adapt / Skip) and a Decision column the user fills in at this stage's approval; patterns that serve no story go under Story-map gaps. Build the page inventory and navigation from the story map only. The table proposes; it changes nothing until the user decides. After the decisions (create workflow, Step G), apply the rows decided Adopt or Adapt to the page inventory and navigation, cite each one's CP-ID where it changes them, and re-verify the document.

**Flag gaps:**
- Orphan activities (not mapped to any page) → IA gaps
- Pages with no source activity → potentially unnecessary

**Platform constraint check:** If constrained platform, verify page count and navigation model are feasible against Stage 1 constraints. Adjust and document if needed.

**Languages:** If the UX brief lists more than one language, say in the navigation model where the user chooses the language and whether the choice is per user or per page.

#### Section 3: Visual Hierarchy Map

Create the role-based + semantic hierarchy table. For each text and UI element assign:
- **Role-based name** (e.g., card-title, filter-label, page-title)
- **Type role** (heading-1 through heading-6, body, body-small, caption, label, overline, display, code) — from visual-hierarchy reference. If the UX brief lists a design system that names its own type roles, use its role names instead, so the plan and the design system speak the same vocabulary.
- **Emphasis level** (high, medium, low, disabled)

Order from highest to lowest emphasis across the entire product.

Select a **scanning pattern** per page (F-pattern, Z-pattern, layer-cake, spotted) based on content density. Map content to scan zones. If the brief lists a right-to-left language, state that the pattern mirrors for it (an F-pattern starts top-right).

### Verification Checks
- `story-id-consistency` (Check 8 from verify-ux-consistency.md)

</stage>
