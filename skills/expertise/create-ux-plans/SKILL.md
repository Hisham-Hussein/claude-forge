---
name: create-ux-plans
description: Plan UX patterns and design specifications. Use when asked to "create UX design", "create UX specifications", "help me plan the UX", "review UX plan", "audit UX compliance", "update UX plan", or "verify UX consistency". Handles the full UX spec lifecycle — create from story maps, review existing plans for quality/compliance, update plans for changed stories, and verify cross-document consistency.
---

<objective>
Manage the full UX specification lifecycle — create, review, update, and verify design-system-agnostic UX plans. Plans cover information architecture, visual hierarchy, component states with all applicable interactions, responsive behavior, data states with microcopy, accessibility, and user flows — enabling coding agents to implement UX without guesswork.
</objective>

<quick_start>
This skill detects existing UX plan files and routes to the appropriate workflow:

- **No `.charter/UX-*.md` files exist** → Create workflow (from story map)
- **Files exist + user says "review"** → Compliance audit (10-phase, severity-rated findings)
- **Files exist + user says "update"** → Incremental update (surgical edits, no regeneration)
- **Files exist + user says "verify"** → Consistency check (10 cross-document checks)

Each workflow is in `workflows/` — the routing section determines which to load.
</quick_start>

<success_criteria>
Per-workflow success criteria (each workflow file defines its own detailed criteria):

- **Create:** UX plan in `.charter/` with all 11 sections complete, 100% traceability, no severity 3+ heuristic gaps
- **Review:** Compliance report written to `.charter/UX-COMPLIANCE-REPORT.md` with verdict (PASS/PASS WITH NOTES/FAIL)
- **Update:** All changes applied, no stale PG-XXX references, verify-ux-consistency passes
- **Verify:** All 10 cross-document checks run, severity 3+ issues auto-fixed, summary reported
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

<auto_detect>

**BEFORE presenting the intake menu, check for existing output:**

1. Glob for `.charter/UX-DESIGN-PLAN.md` and `.charter/UX-*.md` files
2. If UX plan files exist → the plan has already been generated. Tell the user: "UX plan files already exist in `.charter/`. Options: **review** (compliance audit), **update** (apply changes), or **re-create** (regenerate from scratch)."
3. If no UX plan files exist → proceed to create workflow

This detection MUST happen before asking the user anything. If the user's invocation message already contains intent (e.g., "review the UX plans"), match that intent directly — do NOT ask again.

</auto_detect>

<intake>

What would you like to do?

1. Create a UX design plan from a story map
2. Review an existing UX plan (quality audit, compliance check, or implementation review)
3. Update a UX plan for new or changed stories
4. Verify consistency across UX plan files (lightweight cross-document check)
5. Something else

**If the user provided intent with the skill invocation, match it and proceed. Only wait for a response if intent is genuinely unclear.**

</intake>

<routing>

| Response | Workflow File |
|----------|----------|
| 1, "create", "generate", "new", "plan", "design" | `workflows/create-ux-plan.md` |
| 2, "review", "audit", "check", "compliance" | `workflows/review-ux-compliance.md` |
| 3, "update", "change", "modify", "revise" | `workflows/update-ux-plan.md` |
| 4, "verify", "consistency", "cross-check" | `workflows/verify-ux-consistency.md` |
| 5, other | Clarify intent, then route to appropriate workflow |

**MANDATORY: Once you determine the workflow, you MUST use the Read tool to load the workflow file from this skill's `workflows/` directory. Then follow that workflow exactly. Do NOT improvise or act on your own understanding of what "review" or "update" means. The workflow file contains the precise multi-phase process. Reading the workflow file is not optional — it is the entire point of the routing.**

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
| verify-ux-consistency.md | Lightweight cross-document consistency check — runs automatically after create, catches internal inconsistencies between split files |
| review-ux-compliance.md | Audit UX plan quality and/or implementation compliance — 10-phase review with severity-rated findings |
| update-ux-plan.md | Incrementally update a UX plan — merge, remove, or add pages; apply story-level changes — without regenerating from scratch |

</workflows_index>

<templates_index>

| Template | Purpose |
|----------|---------|
| ux-design-plan-template.md | 11-section output structure for UX-DESIGN-PLAN.md |
| ux-compliance-report-template.md | Compliance report output structure for review workflow |

</templates_index>
