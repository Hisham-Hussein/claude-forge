<required_reading>

**Read these reference files NOW before generating the UX plan:**

1. references/nielsen-heuristics.md — validation checklist (used in Phase 5)
2. references/atomic-design.md — component classification + state taxonomy
3. references/accessibility-wcag.md — per-component accessibility patterns
4. references/responsive-patterns.md — breakpoint tiers + layout transformations
5. references/data-states.md — loading/empty/error/success patterns + microcopy
6. references/interaction-patterns.md — filter, card, animation, feedback patterns
7. references/visual-hierarchy.md — type roles, emphasis model, scanning patterns

Also read the output template: templates/ux-design-plan-template.md

</required_reading>

<inputs>

**Required:** Story Map (`.charter/STORY-MAP.md` or path provided by user)
**Optional:** User Stories with AC (`.charter/USER-STORIES.md` or path provided by user)

If no story map path is provided, check `.charter/STORY-MAP.md` first. If neither exists, ask the user.

If user stories exist but weren't specified, ask: "I found `.charter/USER-STORIES.md` — should I use it to enrich the plan with acceptance criteria detail?"

</inputs>

<process>

<phase name="1-parse-inputs">

## Phase 1: Parse Inputs

### Step 1: Read Story Map

Read the story map file. Extract and organize:

- **Backbone activities** (left-to-right across the top): These become candidate pages/views
- **Steps/Epics** (vertical under each activity): These become candidate sections within pages
- **User stories/Tasks** (lowest level): These become features and content blocks
- **Personas**: Identify primary and secondary user types
- **Release slices**: Identify MVP cut line — the UX plan targets MVP scope unless the user specifies otherwise
- **Cross-cutting concerns**: Note any that affect UX (accessibility, performance, branding decisions)
- **Resolved design decisions**: Extract any UX-relevant decisions already made

### Step 2: Read User Stories (if provided)

Extract from each story:
- Acceptance criteria (specific behaviors, edge cases)
- Interaction details not captured in the story map
- Error scenarios and validation rules

### Step 3: Confirm Scope

Ask the user: "The story map has [N] release slices. Should the UX plan target **MVP only**, or a specific slice?"

Default to MVP if the user doesn't specify.

</phase>

<phase name="2-derive-structure">

## Phase 2: Derive Structure (Sections 1-3 of output)

### Step 4: Derive Information Architecture

Use the **story-map-to-IA transformation algorithm**:

**4a. Page vs. Section vs. Action collapsing:**

For each backbone activity, apply in order:

1. Does this activity require a different layout than the previous activity? YES -> New page. NO -> continue.
2. Does the user perform this activity in a different temporal context? YES -> New page. NO -> continue.
3. Does the content volume exceed what fits as a section? YES -> New page. NO -> Section within existing page.
4. Would separating this into its own page break the user's flow? YES -> Keep as section. NO -> Separate page.

Activities that are purely external (e.g., "go to GitHub") become link/CTA actions, not pages.

**4b. Build page inventory:**

For each page identified:

| Field | Source |
|-------|--------|
| Page Name | From activity (noun-ified) |
| Source Activity | SM-XXX |
| Page Type | Infer: browse->listing, evaluate->detail, configure->form, monitor->dashboard, learn->landing |
| Content Priority | P1=backbone content, P2=steps/epics, P3=story details, P4=ambient/metadata |
| Entry Points | How users reach this page (from story map horizontal flow) |
| Exit Points | Where users go next |

**4c. Select navigation model:**

Use the navigation model decision matrix from the interaction-patterns reference:

| Application Type | Primary Model |
|-----------------|---------------|
| Content directory / catalog | Filtered view |
| SaaS dashboard | Hub-and-spoke |
| E-commerce | Hierarchical |
| Documentation | Hierarchical |
| Single-page marketing | Flat |
| Multi-step form | Sequential |

Specify navigation model **per-section**, not globally.

**4d. Flag gaps:**

- Orphan activities (not mapped to any page) -> Flag as IA gaps
- Pages with no source activity -> Flag as potentially unnecessary

### Step 5: Build Visual Hierarchy

Create the combined role-based + semantic hierarchy table covering every text and UI element. Use the type role taxonomy and emphasis model from the visual-hierarchy reference.

For each element assign:
- **Role-based name** (e.g., card-title, filter-label, page-title)
- **Type role** (heading-1 through heading-6, body, body-small, caption, label, overline, display, code)
- **Emphasis level** (high, medium, low, disabled)

Order from highest to lowest emphasis across the entire product.

Select a **scanning pattern** per page (F-pattern, Z-pattern, layer-cake, spotted) based on content density. Map content to scan zones.

### Step 6: Design Page Layouts

Create text-based wireframes for each page/view. Each layout specifies:

- Content zones and their placement
- Element ordering and reading flow
- Spatial relationships using the abstract spacing scale (XS, S, M, L, XL)
- Zone priority mapping (which zones get P1/P2/P3/P4 content)

Use mobile-first specification: describe mobile fully as base tier, then state what each wider tier *adds*.

</phase>

<phase name="3-specify-components">

## Phase 3: Specify Components & Behavior (Sections 5-8 of output)

### Step 7: Specify Components

Organize by Atomic Design hierarchy:
- **Atoms**: Indivisible building blocks (buttons, badges, icons, inputs, text elements)
- **Molecules**: Functional groups of atoms (search bar, card header, metadata row, chip)
- **Organisms**: Complex page sections (card grid, filter section, hero, navigation bar)

For each component, use the state applicability matrix from atomic-design reference. Document ALL applicable states using emphasis-based descriptions (not pixel values):

| State | Visual Description | Behavior |
|-------|-------------------|----------|
| Default | [appearance at rest] | [what user can do] |
| Hover | [emphasis change] | [feedback purpose] |
| Focus | [focus ring, 3:1 contrast] | [keyboard interaction] |
| Active | [pressed appearance] | [what happens] |
| ... | ... | ... |

Include accessibility inline with each component: semantic HTML element, ARIA attributes, keyboard behavior. Use patterns from accessibility-wcag reference.

### Step 8: Define Interaction Patterns

For every interactive element specify:
- **Primary action**: Click/tap result
- **Feedback model**: Optimistic vs pessimistic (use decision rules from interaction-patterns reference)
- **Animation**: Duration category (short/medium/long) + easing (ease-out default)
- **Keyboard**: Tab focus, Enter/Space activation, Escape dismissal
- **Mobile variant**: Touch target size, gesture differences
- **Reduced motion fallback**: What happens when animations are disabled

For filter interactions specifically, define:
- Filter placement pattern (sidebar, top bar, chips)
- Application method (interactive/batch/hybrid)
- Boolean logic (AND between facets, OR within facets)
- Clear/reset mechanism (per-filter + global "Clear All")
- No-results handling with exact microcopy
- URL persistence (filter state in URL for sharing)

Trace each interaction to its source: SM-XXX or US-XXX.

### Step 9: Define Responsive Behavior

Use semantic viewport tiers from responsive-patterns reference:
- **Mobile**: Single-column, touch-primary, portrait
- **Tablet**: Multi-column possible, touch-primary
- **Desktop**: Full multi-column, pointer-primary
- (Optional) **Wide**: Desktop with max-width constraint

For each component specify the transformation pattern at each tier:
- Column drop, stack, collapse, replace, hide, reposition, resize, reorder

Use the responsive specification table format:

| Aspect | Mobile | Tablet | Desktop |
|--------|--------|--------|---------|
| Layout | ... | ... | ... |
| Navigation | ... | ... | ... |
| Content visibility | ... | ... | ... |
| Touch targets | 44x44 min | 44x44 min | 24x24 min |
| Typography scale | ... | ... | ... |

### Step 10: Define Data States

For every component that displays dynamic content, define ALL states using patterns from data-states reference:

- **Loading**: Skeleton/spinner/none based on duration matrix (<1s=none, 1-10s=skeleton, 10s+=progress bar). Render skeleton after ~300ms delay.
- **Empty**: Headline + body + CTA. Use appropriate empty state type (first-use, no-data, no-results, user-cleared).
- **Error**: What happened + why + recovery action. Contextual placement. No technical jargon.
- **Success**: Scaled to action significance (routine=none/subtle, standard=toast, important=banner, critical=full page).
- **Partial**: Primary experience failed = error page. Secondary experience failed = degraded with inline error.

Include exact microcopy for each state.

</phase>

<phase name="4-accessibility-flows">

## Phase 4: Accessibility & Flows (Sections 9-10 of output)

### Step 11: Define Accessibility

For each component, verify against the accessibility validation checklist from accessibility-wcag reference:

- [ ] Semantic HTML element specified (not just ARIA role)
- [ ] ARIA roles/states listed (only where native HTML insufficient)
- [ ] Keyboard interaction model defined
- [ ] Focus management pattern identified (trap / roving tabindex / return)
- [ ] Accessible name specified
- [ ] Contrast requirements stated abstractly (4.5:1 text, 3:1 non-text)
- [ ] Color independence ensured (multiple signals for every state)
- [ ] Dynamic changes use appropriate `aria-live` level
- [ ] Touch target size meets minimum
- [ ] Focus indicator visible with 3:1 contrast

Key patterns to apply:
- Cards: `<article>` in `<ul>`, single `<a>` on title, `aria-labelledby`
- Filter chips: `role="toolbar"` with roving tabindex, `aria-pressed`
- Navigation: `<nav>` with `aria-current="page"`, skip link
- Results: `aria-live="polite"` region for filter count updates (debounced ~300ms)

### Step 12: Map User Flows

For each major user task from the story map, create a step-by-step flow:

- Entry point (how does the user start?)
- Steps (what does the user do at each point?)
- Decision points (what if the user does X instead of Y?)
- Error recovery paths (what happens when something fails mid-flow?)
- Exit point (where does the flow end?)

Use bulleted sequences. Add Mermaid diagrams for complex branching flows.

</phase>

<phase name="5-validate-output">

## Phase 5: Validate & Output (Sections 11 + quality gates)

### Step 13: Build Traceability Matrix

Create a table linking every UX decision to its source:

| UX Element | Section | Source ID | Source Description |
|------------|---------|-----------|-------------------|
| [element] | [section ref] | SM-XXX / US-XXX | [activity/story name] |

**Coverage check**: Every story map activity in scope must have at least one UX element. Flag any gaps.

**Orphan check**: Every UX element must trace to a source. Flag any elements without traceability — they are either invented requirements (remove) or story map gaps (flag for user).

### Step 14: Validate Against Nielsen's Heuristics

Run the 50-question quality gate from nielsen-heuristics reference.

Use the two-pass validation:
1. **First pass**: Read entire plan for overall impressions. Note which heuristics seem well-addressed vs absent.
2. **Second pass**: Go heuristic-by-heuristic (H1 through H10). Record specific gaps with severity ratings.

**Severity scale:**
| Rating | Meaning | Action |
|--------|---------|--------|
| 0 | Not applicable | Skip |
| 1 | Cosmetic gap | Note, don't block |
| 2 | Minor gap — one component missing a secondary state | Fix if in scope |
| 3 | Major gap — primary interaction has undefined behavior | Must fix before output |
| 4 | Catastrophic gap — entire heuristic unaddressed | Block output |

Fix all severity 3+ gaps before proceeding. Report severity 1-2 as notes at the bottom of the plan.

Run cross-heuristic consistency checks:
- H1 + H9: Every error state includes both message AND system status indication
- H3 + H6: Every escape hatch is visually discoverable
- H4 + H2: Consistent terminology is also domain-appropriate terminology
- H5 + H9: Prevention and recovery cover the same error types

### Step 15: Check Output Length

If total output exceeds ~500 lines, split semantically:

```
.charter/
  UX-DESIGN-PLAN.md          (Sections 1-3: overview, IA, hierarchy)
  UX-LAYOUTS.md              (Section 4: page layouts)
  UX-COMPONENTS.md           (Section 5: component specs with states)
  UX-INTERACTIONS.md         (Sections 6-8: interactions, responsive, data states)
  UX-ACCESSIBILITY.md        (Section 9: accessibility)
  UX-FLOWS.md                (Sections 10-11: user flows + traceability)
```

If ~500 lines or fewer, write a single `UX-DESIGN-PLAN.md`.

### Step 16: Write Output

Write the plan to the project's `.charter/` directory. Use the template from `templates/ux-design-plan-template.md` as the output structure.

Report to user:
- Files written and their locations
- Number of components specified
- Number of pages/views in IA
- Traceability coverage (% of story map activities with UX elements)
- Nielsen's heuristic validation summary (pass/warn/fail per heuristic)
- Any severity 1-2 gaps noted for future attention

</phase>

</process>

<anti_patterns>

- **Template-filling without analysis**: Mechanically filling sections without adapting to the project's needs. Every section must derive from the story map, not be filled generically.
- **Over-specification**: Prescribing CSS classes, framework-specific patterns, or implementation details. The plan is technology-agnostic.
- **Under-specification**: Leaving states undefined, saying "standard behavior" without defining it. If a developer would have to guess, specify it.
- **Design system leakage**: Including colors, fonts, or pixel values. Use role-based names and emphasis levels only.
- **Missing traceability**: UX elements that don't trace to any SM-XXX or US-XXX requirement.
- **Desktop-first bias**: Specifying desktop layout in detail, leaving mobile as "it stacks." Mobile is the base tier.
- **Accessibility as appendix**: Treating accessibility as a separate section rather than per-component inline specs.
- **Invented requirements**: Adding UX elements not backed by any story map activity. If the element is needed, flag the story map gap.
- **Default-only components**: Specifying only the happy/loaded state. Every interactive component needs all applicable states.
- **Happy-path-only flows**: User flows that only cover the success path. Error recovery and decision branches are required.

</anti_patterns>

<success_criteria>

The UX plan is complete when:

- [ ] All 11 sections of the template are filled with project-specific content (no placeholders)
- [ ] Every component has all applicable states documented (per state applicability matrix)
- [ ] Visual hierarchy uses combined role-based + semantic naming (no pixel values, no colors)
- [ ] Every UX decision traces to a source ID (SM-XXX or US-XXX)
- [ ] Nielsen's heuristic validation passes with no severity 3+ gaps remaining
- [ ] Responsive behavior is explicit for all tiers (mobile, tablet, desktop minimum)
- [ ] Accessibility requirements are inline with each component spec
- [ ] Data states (loading, empty, error, success) defined with exact microcopy for all dynamic components
- [ ] Output respects 500-line splitting rule
- [ ] A coding agent reading the output + a design system can implement without guesswork
- [ ] Traceability matrix shows 100% coverage of in-scope story map activities

</success_criteria>
