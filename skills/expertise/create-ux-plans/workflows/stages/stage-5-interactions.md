<stage name="5-interactions">

## Stage 5: UX-INTERACTIONS.md

### Output
`.charter/UX-INTERACTIONS.md` — Sections 6-8 of the output template (Interaction Patterns + Responsive Behavior + Data States)

### Dependencies
Stages 1-4 verified (IA + flows + layouts + components available)

### Inputs (re-read from disk)
- Story map
- Constraint manifest
- **UX-DESIGN-PLAN.md** (IA, visual hierarchy)
- **UX-FLOWS.md** (interaction sequences)
- **UX-LAYOUTS.md** (spatial context for interactions)
- **UX-COMPONENTS.md** (component inventory and states)

### References to Load
- `references/interaction-patterns.md`
- `references/responsive-patterns.md`
- `references/data-states.md`

### Context7 Query (if constrained platform)
Query for: supported automation triggers, animation capabilities, conditional logic syntax, responsive behavior support, data state handling patterns, filter/search capabilities.

Append findings to constraint manifest under `## Stage-Specific Constraints > ### Stage 5 Constraints`.

### Generation Instructions

#### Section 6: Interaction Patterns

For every interactive component (from UX-COMPONENTS.md), specify:
- **Trigger:** User action or system event
- **Response:** What changes in the UI
- **Feedback model:** Optimistic vs. pessimistic (use decision rules from interaction-patterns reference)
- **Animation:** Duration category (short/medium/long) + easing (ease-out default)
- **Keyboard:** Tab focus, Enter/Space activation, Escape dismissal
- **Mobile variant:** Touch target size, gesture differences
- **Reduced motion fallback:** What happens when animations are disabled
- **Source:** SM-XXX / US-XXX

**Filter interactions** get expanded specification:
- Placement pattern (sidebar, top bar, chips)
- Application method (interactive/batch/hybrid)
- Boolean logic (AND between facets, OR within facets)
- Clear/reset mechanism (per-filter + global "Clear All")
- No-results handling with exact microcopy
- URL persistence (filter state in URL for sharing)

#### Section 7: Responsive Behavior

Use semantic viewport tiers from responsive-patterns reference:
- **Mobile:** Single-column, touch-primary, portrait (44x44 min targets)
- **Tablet:** Multi-column possible, touch-primary (44x44 min targets)
- **Desktop:** Full multi-column, pointer-primary (24x24 min targets)

For each component, specify the transformation pattern at each tier: column drop, stack, collapse, replace, hide, reposition, resize, reorder.

Use the responsive specification table format from the template.

#### Section 8: Data States

For every component that displays dynamic content (from UX-COMPONENTS.md), define ALL states using data-states reference:

- **Loading:** Skeleton/spinner/none based on duration matrix (<1s=none, 1-10s=skeleton, 10s+=progress bar). Render skeleton after ~300ms delay.
- **Empty:** Headline + body + CTA. Type: first-use / no-data / no-results / user-cleared.
- **Error:** What happened + why + recovery action. Contextual placement. No technical jargon.
- **Success:** Scaled to action significance (routine=none, standard=toast, important=banner, critical=full page).
- **Partial:** Primary failed = error page. Secondary failed = degraded with inline error.

Include **exact microcopy** for each state.

### Verification Checks
- `status-value-consistency` (Check 6 — cross-check against components)
- `cross-reference-validity` (Check 9)

</stage>
