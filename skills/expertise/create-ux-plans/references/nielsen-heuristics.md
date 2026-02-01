<overview>
A 50-question quality gate that validates UX plan documents for completeness. Each of Nielsen's 10 heuristics becomes a set of spec-level probes detecting **omissions** — behaviors, states, and edge cases the spec failed to define, which would force a coding agent to improvise.
</overview>

<decision_rules>

## Core Reframe

Traditional: "Does this interface satisfy the heuristic?"
Spec-level: "Does this spec **define enough** for the heuristic to be satisfiable when implemented?"

## Severity Scale for Spec Gaps

| Rating | Meaning | Action |
|--------|---------|--------|
| 0 | Not applicable to this project | Skip |
| 1 | Cosmetic gap — unlikely to cause confusion | Note, don't block |
| 2 | Minor gap — one component missing a secondary state | Fix if in scope |
| 3 | Major gap — primary interaction has undefined behavior | Must fix before output |
| 4 | Catastrophic gap — entire heuristic unaddressed | Block output |

## The Meta-Test

For every interaction/state in the spec ask: **"If a developer reads ONLY this spec and a design system, would they know exactly what to build?"** If "they'd have to guess about X," map the gap:

| Guess about... | Heuristic |
|----------------|-----------|
| Visual feedback | H1 |
| Terminology | H2 |
| Undo/reset | H3 |
| Interaction consistency | H4 |
| Edge cases | H5 |
| What's visible | H6 |
| Keyboard shortcuts | H7 |
| Information priority | H8 |
| Error messages | H9 |
| Help text | H10 |

## Static Content Exception

For purely static, non-interactive content: skip H1 (no state changes), H5 (no user input), H9 (no failures possible). Skip gracefully — don't force every heuristic onto every component.

## Cross-Heuristic Consistency Checks

Run after individual checks:
- H1 + H9: Every error state must include both the message AND a clear system status indication
- H3 + H6: Every escape hatch must be visually discoverable, not just functionally available
- H4 + H2: Consistent terminology must also be domain-appropriate terminology
- H5 + H9: Prevention and recovery must cover the same error types

## Two-Pass Validation Process

1. **First pass**: Read entire spec for overall impressions. Note which heuristics seem well-addressed vs absent.
2. **Second pass**: Go heuristic-by-heuristic through the checklist below. Record specific gaps with section references.

</decision_rules>

<validation_checklist>

## H1: Visibility of System Status

1. Is a loading state defined for every data-fetching component?
2. Are transition behaviors specified between state changes?
3. Are progress indicators defined for multi-step processes?
4. Are active/selected states visually distinct and specified?
5. Is feedback timing specified for user actions?

## H2: Match Between System and Real World

6. Does user-facing terminology match the target audience's vocabulary?
7. Are labels and category names validated against user mental models?
8. Is internal/technical jargon absent from user-facing elements?
9. Does the IA match how users think about the domain?
10. Are visual metaphors grounded in real-world analogs?

## H3: User Control and Freedom

11. Is a reset/clear mechanism defined for every filter or selection?
12. Can each interactive state change be undone?
13. Is back/return navigation defined for multi-page flows?
14. Can overlays/modals/expanded views be dismissed?
15. Is an escape hatch specified for every interactive state?

## H4: Consistency and Standards

16. Is terminology consistent throughout the entire spec?
17. Do similar elements use identical interaction patterns?
18. Does the spec follow web platform conventions?
19. Are visual hierarchy role names used consistently?
20. Are state names (active/selected/disabled) used consistently?

## H5: Error Prevention

21. Are zero-result / empty states defined?
22. Are impossible state combinations prevented by design?
23. Is input validation defined for text inputs?
24. Are destructive actions guarded with confirmation?
25. Are network/API failure scenarios addressed?

## H6: Recognition Rather Than Recall

26. Are all primary actions visible (not hidden in menus)?
27. Is the current state visually indicated at all times?
28. Are filter/option lists always visible (not collapsed)?
29. Can each view be understood without remembering other views?
30. Is contextual help provided for unfamiliar features?

## H7: Flexibility and Efficiency of Use

31. Are filter/view states reflected in shareable URLs?
32. Is keyboard navigation specified for all interactive elements?
33. Are multiple pathways defined for key tasks?
34. Do cross-component shortcuts exist? (e.g., card tag applies filter)
35. Are different user types (novice/expert) considered?

## H8: Aesthetic and Minimalist Design

36. Is a clear information hierarchy defined with emphasis levels?
37. Is content per component limited to essential information?
38. Is information density appropriate for the scanning task?
39. Are secondary/tertiary elements appropriately de-emphasized?
40. Can every element's presence be traced to a user need?

## H9: Help Users Recognize, Diagnose, and Recover from Errors

41. Is an error state defined for every component that can fail?
42. Are error messages specified with exact microcopy?
43. Does every error state include a recovery action?
44. Are error messages contextual (near the failed element)?
45. Are error messages free of technical jargon?

## H10: Help and Documentation

46. Is first-use/onboarding guidance defined?
47. Is contextual help provided for unfamiliar terminology?
48. Does the landing experience clearly communicate purpose and usage?
49. Are links to external documentation specified where relevant?
50. Do empty states include guidance on what to do?

</validation_checklist>

<examples>

## Compliant vs Non-Compliant Spec Text

### H1 — System Status
- **Compliant**: "When the user clicks a category chip, the chip transitions to its active state immediately. The hook grid displays skeleton cards (matching card dimensions) for up to 500ms while results update. If results return in under 100ms, no skeleton is shown."
- **Non-compliant**: "Users can filter hooks by category."

### H3 — User Control and Freedom
- **Compliant**: "A 'Clear all' text button appears in the filter bar when any filter is active. Clicking it deselects all chips and returns the grid to the full unfiltered catalog. Each chip can be deselected by clicking it again (toggle). URL query parameters update to match, so the browser back button also serves as undo."
- **Non-compliant**: "Users select filter chips to narrow results."

### H4 — Consistency
- **Compliant**: "All toggle-type interactive elements (category chips, event chips) use identical interaction patterns: click to toggle, active state shows filled background with high-emphasis text, inactive shows outlined background with medium-emphasis text. The term 'chip' is used consistently — never 'tag', 'badge', or 'pill'."
- **Non-compliant**: "Category tags can be selected. Event filter pills toggle on and off."

### H5 — Error Prevention
- **Compliant**: "When active filters produce zero matching hooks, the grid area displays: Heading: 'No hooks match these filters'. Body: 'Try removing a filter or clearing all filters to see more hooks.' Action: 'Clear all filters' button that resets to default."
- **Non-compliant**: "The grid displays matching hooks based on the selected filters."

### H8 — Minimalist Design
- **Compliant**: "Hook card displays exactly 5 elements in strict hierarchy: (1) Hook name — heading-3, high emphasis; (2) Description — body-text, medium emphasis, truncated to 2 lines; (3) Category badge — body-small; (4) Star count — caption, low emphasis; (5) External link icon — low emphasis. No additional metadata on card surface."
- **Non-compliant**: "Cards show hook name, description, category, event type, star count, last updated, author, language, license, and repository URL."

### H9 — Error Recovery
- **Compliant**: "If the hook catalog fails to load: Icon: warning, medium emphasis. Heading: 'Unable to load hooks'. Body: 'The hook catalog is temporarily unavailable. This usually resolves within a few minutes.' Action: 'Try again' button that reloads the page."
- **Non-compliant**: "Show an error message if data fails to load."

</examples>

<anti_patterns>

1. **Default-only specs**: Defining only the "loaded/happy" state; no loading, skeleton, error, or empty states
2. **One-way interactions**: Defining filter application but not filter clearing/reset/undo
3. **Open-then-what**: Modal/overlay specs that define opening but not closing/dismissal
4. **Jargon leak**: Internal project terms (manifest, enrichment, lifecycle event) appearing in user-facing UI
5. **Terminology drift**: Calling the same element "chip" in one section, "tag" in another, "badge" in a third
6. **Happy-path-only**: No zero-result states, no API failure handling, no malformed-URL handling
7. **Data-driven bloat**: Including fields "because they're in the API" rather than because the user needs them
8. **Flat hierarchy**: All information at the same visual weight with no defined emphasis levels
9. **Generic errors**: "Something went wrong" without specific microcopy, placement, or recovery action
10. **Invisible escape hatches**: Reset/undo mechanisms that exist functionally but have no visible UI affordance

</anti_patterns>
