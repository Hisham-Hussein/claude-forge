# Phase {N} Plan: {Slice Name}

## Metadata
- **Phase:** {N}
- **Release:** {Release name from ROADMAP.md, e.g., MVP}
- **Wave:** {Wave number and label, e.g., Wave 2 (parallel)}
- **Source Stories:** {SM-XXX, SM-XXX, SM-XXX (from ROADMAP.md)}
- **Derived User Stories:** {US-XXX, US-XXX, US-XXX (from trace script)}
- **Date Generated:** {YYYY-MM-DD}
- **Architecture Layers Touched:** {e.g., Domain, Application, Adapters}
- **UX Inputs Loaded:** {one of:}
  - `Yes — Design OS export (sections: X, Y, Z)` — when `--has-ui` set and export exists
  - `Yes — UX-DESIGN-PLAN.md, UX-COMPONENTS.md, UX-INTERACTIONS.md, UX-FLOWS.md, DESIGN-TOKENS.md (filtered via traceability matrix); Design OS export not available` — when `--has-ui` set, no export, traceability has matches
  - `No — traceability matrix has no entries for this phase's stories; UX patterns deferred to superpowers:writing-plans` — when `--has-ui` set, no export, traceability yields nothing
  - `N/A — --has-ui not set` — when flag omitted

## Story Summary

{Brief overview of the phase's scope: which user stories are included, total task count, and how the stories relate to each other within this phase.}

| Story | Name | Layer Coverage | Task Count |
|-------|------|---------------|------------|
| US-XXX | {Story name} | Domain, Application, Adapters | {N} |
| US-XXX | {Story name} | Adapters only | {N} |

## Task Decomposition

{FDD-style task trees. One tree per US-XXX story, ordered by story dependency (independent stories first, then stories that depend on their outputs). Document order is the default sequential execution order — superpowers:writing-plans processes stories top-to-bottom. The Parallelism Analysis section below may override this by grouping independent stories for simultaneous dispatch. Within each story, tasks follow layer order: Domain -> Application -> Adapters.}

### Story US-XXX: {Story Name}

#### Layer: Domain

**Task 1: {Create [Entity/Value Object]}** (`{file path}`)
- **Input:** {Requirements from acceptance criteria}
- **Output:** {Tested domain object}
- **Test:** {Unit tests for validation rules}

#### Layer: Application

**Task 2: {Create [Use Case/Handler]}** (`{file path}`)
- **Input:** {Domain objects, interface contracts}
- **Output:** {Working use case}
- **Test:** {Unit tests with mocked dependencies}

#### Layer: Adapters

**Task 3: {Create [Adapter Implementation]}** (`{file path}`)
- **Input:** {Interface contract from domain}
- **Output:** {Working adapter}
- **Test:** {Integration tests}
- **Reference:** {design-os-export/sections/[section-name]/ (if UI task with Design OS export)}

---

{Repeat for each US-XXX in this phase. Not every story touches all three layers. UI-only stories may have only Adapters tasks; data pipeline stories may skip Application. Omit layers not needed. Separate each story with a horizontal rule (---).}

{For UI tasks when --has-ui is set and Design OS export exists: include Reference field pointing to the relevant section directory. For UI tasks when --has-ui is set but no export: omit Reference field and embed UX specs (component layout, interaction patterns, accessibility requirements) directly in the task Input field.}

## Parallelism Analysis

{Stories are INVEST-independent per upstream /create-requirements. This section confirms independence and flags any implementation-level conflicts (e.g., multiple stories modifying the same file).}

### Parallel Group 1 (can run simultaneously)
- US-XXX: {Story Name} — {why independent}
- US-XXX: {Story Name} — {why independent}

### Sequential Dependencies (if any)
- US-XXX must complete before US-XXX because {reason}

### Recommended Execution Order
1. {Parallel Group 1 stories} — dispatch to parallel agents
2. {Sequential story} — after group 1 completes
3. {Parallel Group 2 stories} — dispatch to parallel agents

> **For Claude — superpowers:writing-plans:**
> This PHASE-N-PLAN.md is the spec input for `superpowers:writing-plans`.
> Feed the Task Decomposition section (story by story) into `writing-plans`
> to produce a detailed implementation plan with TDD steps
> (RED-GREEN-REFACTOR) baked into each task. The Parallelism Analysis
> section determines agent dispatch order via
> `superpowers:dispatching-parallel-agents`. Do not modify the Metadata
> or Story Summary sections — they are reference context, not work items.
