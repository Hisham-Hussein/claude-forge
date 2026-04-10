<stage name="6-accessibility">

## Stage 6: UX-ACCESSIBILITY.md (Conditional)

### Conditional Execution
This stage is **skipped** when the detected platform handles accessibility natively (e.g., Airtable Interface Designer generates accessible markup automatically). The skip decision is made in Phase 0 and recorded in the generation status manifest.

When skipped, the accessibility requirements already specified inline with each component in UX-COMPONENTS.md (Stage 4) are sufficient.

### Output
`.charter/UX-ACCESSIBILITY.md` — Section 9 of the output template (Accessibility)

### Dependencies
Stages 1-5 verified (all prior documents available)

### Inputs (re-read from disk)
- Story map
- Constraint manifest
- All 5 prior verified documents (DESIGN-PLAN, FLOWS, LAYOUTS, COMPONENTS, INTERACTIONS)

### References to Load
- `references/accessibility-wcag.md`

### Context7 Query (if constrained platform)
Query for: built-in accessibility features, ARIA support level, keyboard navigation support, screen reader compatibility, focus management capabilities.

Append findings to constraint manifest under `## Stage-Specific Constraints > ### Stage 6 Constraints`.

### Generation Instructions

#### Section 9: Accessibility

**Global requirements** (per template):
- Skip link: "Skip to main content" as first focusable element
- Landmark regions: `<nav>`, `<main>`, `<footer>` with `aria-label`
- Heading hierarchy: No skipped levels; visual size via CSS only
- Focus indicators: 3:1 contrast minimum, visible on all interactive elements
- Color independence: No information conveyed through color alone
- Text resize: All content accessible at 200% zoom without horizontal scroll

**Per-component accessibility:**

For each component in UX-COMPONENTS.md, verify against the validation checklist from accessibility-wcag reference:

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

**Key patterns** (from reference):
- Cards: `<article>` in `<ul>`, single `<a>` on title, `aria-labelledby`
- Filter chips: `role="toolbar"` with roving tabindex, `aria-pressed`
- Navigation: `<nav>` with `aria-current="page"`, skip link
- Results: `aria-live="polite"` region for filter count updates (debounced ~300ms)

This document consolidates and deepens the inline accessibility specs from UX-COMPONENTS.md. It does NOT contradict them — if a conflict is found, update UX-COMPONENTS.md to match.

### Verification Checks
No specific named checks from verify-ux-consistency.md apply to this document alone. The final cross-document sweep covers accessibility consistency.

</stage>
