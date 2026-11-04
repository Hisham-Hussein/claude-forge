<stage name="5-interactions">

## Stage 5: UX-INTERACTIONS.md

### Output
`.charter/UX-INTERACTIONS.md` — Sections 6-8 of the output template (Interaction Patterns + Responsive Behavior + Component Data States)

### Dependencies
Stages 1-4 verified (IA + flows + layouts + components available). Full depth only.

### Inputs (re-read from disk)
- Story map
- Constraint manifest (including the UX Brief)
- **Design system** files listed in the brief, if any (motion and interaction-state rules)
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
- **Animation:** Duration category (short/medium/long) + easing (ease-out default). If the brief lists a design system with motion rules, name its duration and easing roles instead.
- **Keyboard:** Tab focus, Enter/Space activation, Escape dismissal
- **Other-tier variant:** For each tier other than the brief's base tier, what differs (touch target size, gestures, hover-only affordances that need a touch equivalent)
- **Reduced motion fallback:** What happens when animations are disabled
- **Source:** SM-XXX / US-XXX

**Filter interactions** get expanded specification:
- Placement pattern (sidebar, top bar, chips)
- Application method (interactive/batch/hybrid)
- Multi-select behaviour (single vs. multi per facet)
- Boolean logic (AND between facets, OR within facets)
- Clear/reset mechanism (per-filter + global "Clear All")
- Default value per filter
- No-results handling with exact microcopy
- URL persistence (filter state in URL for sharing)

**State machines:** For every status field whose value changes over time (from the layouts' field specifications), write a state machine in the template's format: every allowed value as a state, every transition with its exact trigger (button label or system event), initial and terminal states marked, and failure transitions. The consistency and review workflows check status values and transitions against these.

#### Section 7: Responsive Behavior

Use semantic viewport tiers from responsive-patterns reference:
- **Mobile:** Single-column, touch-primary, portrait (44x44 min targets)
- **Tablet:** Multi-column possible, touch-primary (44x44 min targets)
- **Desktop:** Full multi-column, pointer-primary (24x24 min targets)

Start from the brief's base tier (the primary device). For each component, specify the transformation pattern at each other tier: column drop, stack, collapse, replace, hide, reposition, resize, reorder.

Use the per-component responsive table from Section 7 of `templates/ux-design-plan-template.md` (base tier column first).

#### Section 8: Component Data States

Page-level data states already live with each page in UX-LAYOUTS.md. This section covers components whose states differ from their page's, for example a panel that loads or fails on its own while the rest of the page is shown. Reference the page's states rather than repeating them. If no component's states differ from its page's, write "None: all components share their page's states (UX-LAYOUTS.md)."

For every such component (from UX-COMPONENTS.md), define ALL states using data-states reference:

- **Loading:** Skeleton/spinner/none based on duration matrix (<1s=none, 1-10s=skeleton, 10s+=progress bar). Render skeleton after ~300ms delay.
- **Empty:** Headline + body + CTA. Type: first-use / no-data / no-results / user-cleared.
- **Error:** What happened + why + recovery action. Contextual placement. No technical jargon.
- **Success:** Scaled to action significance (routine=none, standard=toast, important=banner, critical=full page).
- **Partial:** Primary failed = error page. Secondary failed = degraded with inline error.

Include **exact microcopy** for each state, in every language the brief lists.

### Verification Checks
- `status-value-consistency` (Check 6 — cross-check against components)
- `cross-reference-validity` (Check 9)

</stage>
