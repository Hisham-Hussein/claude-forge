---
name: create-ux-plans
description: Use when a project has a story map (STORY-MAP.md) and needs UX specifications before implementation begins. Bridges the gap between story mapping and coding by specifying what users see and how they interact. Use when asked to "create a UX plan", "design the UX", "UX specification", "specify components and interactions", or when the planning pipeline needs a visual and behavioral specification layer.
---

<objective>
Generate comprehensive, design-system-agnostic UX specifications from story maps. Produces plans covering information architecture, visual hierarchy, component states with all applicable interactions, responsive behavior, data states with microcopy, accessibility, and user flows — enabling coding agents to implement UX without guesswork.
</objective>

<quick_start>
Invoke with a story map to generate a UX-DESIGN-PLAN.md:

1. Provide the story map path (defaults to `.charter/STORY-MAP.md`)
2. Optionally provide user stories for richer acceptance criteria
3. The workflow derives page structure, specifies every component with all states, validates against Nielsen's heuristics, and writes output to `.charter/`

For the full process, see `workflows/create-ux-plan.md`.
</quick_start>

<success_criteria>
- UX plan written to `.charter/` with all 11 sections complete (no placeholders)
- Every component has all applicable states documented
- Visual hierarchy uses role-based + semantic naming (no colors, fonts, or pixel values)
- Traceability matrix shows 100% coverage of in-scope story map activities
- Nielsen's heuristic validation passes with no severity 3+ gaps
- Responsive behavior explicit for all tiers (mobile, tablet, desktop minimum)
- A coding agent reading the output + a design system can implement without guesswork
</success_criteria>

<essential_principles>

<principle name="specify-dont-decorate">
The UX plan describes structure, behavior, and hierarchy. It never prescribes colors, fonts, or pixel values. Those belong to the design system. Write "heading-3, medium emphasis" not "#1E40AF, 24px."
</principle>

<principle name="every-state-matters">
A component without all its states defined is an incomplete component. Default-only specs guarantee agent improvisation. Every interactive component must define: default, hover, focus, active, and any applicable system states (loading, error, empty, selected, disabled).
</principle>

<principle name="trace-everything">
Every UX decision must link to a story map activity (SM-XXX) or user story (US-XXX). If a UX element can't be traced, it either shouldn't exist or the story map has a gap. The traceability matrix in Section 11 is not optional.
</principle>

<principle name="abstract-visual-specify-behavioral">
"High emphasis, positioned top-left" is good. "#1E40AF, 24px, left: 16px" is not. But "clicking the chip toggles the filter and updates the grid immediately" IS specific enough. Be abstract about appearance, precise about behavior.
</principle>

<principle name="accessibility-is-structural">
Semantic HTML choices, focus management, and keyboard navigation are part of the component spec, not a bolt-on appendix. Accessibility lives within each component specification, not in a separate section.
</principle>

</essential_principles>

<intake>

What would you like to do?

1. Create a UX design plan from a story map
2. Review implementation against an existing UX plan
3. Update a UX plan for new or changed stories
4. Something else

**Wait for response before proceeding.**

</intake>

<routing>

| Response | Workflow |
|----------|----------|
| 1, "create", "generate", "new", "plan", "design" | `workflows/create-ux-plan.md` |
| 2, "review", "audit", "check", "compliance" | `workflows/review-ux-compliance.md` |
| 3, "update", "change", "modify", "revise" | `workflows/update-ux-plan.md` |
| 4, other | Clarify intent, then route to appropriate workflow |

**After reading the workflow, follow it exactly.**

</routing>

<reference_index>

All domain knowledge in `references/`:

**Validation:** nielsen-heuristics.md (50-question quality gate for plan validation)
**Components:** atomic-design.md (classification + state completeness discipline)
**Accessibility:** accessibility-wcag.md (per-component ARIA, keyboard, focus, contrast)
**Layout:** responsive-patterns.md (breakpoint tiers, layout transformations, touch targets, typography scaling)
**Data States:** data-states.md (loading, empty, error, success, partial state patterns + microcopy)
**Behavior:** interaction-patterns.md (filter, card, animation, feedback, navigation, micro-interactions)
**Visual:** visual-hierarchy.md (type roles, emphasis model, scanning patterns, spatial hierarchy)

</reference_index>

<workflows_index>

| Workflow | Purpose |
|----------|---------|
| create-ux-plan.md | Generate UX-DESIGN-PLAN.md from a story map (+ optional user stories) |
| review-ux-compliance.md | Audit implementation against an existing UX plan (future) |
| update-ux-plan.md | Update a UX plan for new or changed stories (future) |

</workflows_index>

<templates_index>

| Template | Purpose |
|----------|---------|
| ux-design-plan-template.md | 11-section output structure for UX-DESIGN-PLAN.md |

</templates_index>
