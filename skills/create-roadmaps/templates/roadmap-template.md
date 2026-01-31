# Project Roadmap: [Product Name]

> **Generated from:** .charter/STORY-MAP.md + .charter/ARCHITECTURE-DOC.md
> **Generated on:** [date]
> **Methodology:** Vertical Slice Delivery with Wave-Based Parallelism

---

## Quick Reference

### Roadmap Overview

| Release | Slices | Stories | Wave Structure |
|---------|--------|---------|----------------|
| **[Release 1]** | [count] | [count] | W1 (seq) -> W2 (par) -> W3 (seq) |
| **[Release 2]** | [count] | [count] | W1 (seq) -> W2 (par) |
| **[Release N]** | [count] | [count] | ... |

### Release Summary

| Release | Delivers | Unlocks |
|---------|----------|---------|
| **[Release 1]** | [End-to-end capability] | [What becomes possible] |
| **[Release 2]** | [Additional capabilities] | [What becomes possible] |
| **[Release N]** | [Capabilities] | [What becomes possible] |

---

## Release: [Release 1 Name]

### Transitions

| Aspect | Details |
|--------|---------|
| **Produces** | [What this release delivers that downstream work depends on] |
| **Requires** | Nothing (first release) |
| **Unlocks** | [What becomes possible after this release] |

### Wave 1 (sequential -- foundation)

#### Slice 1: [Name -- Walking Skeleton]

[Brief description: what end-to-end capability this slice delivers]

| Story ID | Title | Source |
|----------|-------|--------|
| SM-XXX | [Story title] | BR-XX |
| SM-XXX | [Story title] | BR-XX |
| SM-XXX | [Story title] | BR-XX |

### Wave 2 (parallel -- independent slices)

#### Slice 2: [Name]

[Brief description of what this slice adds]

| Story ID | Title | Source |
|----------|-------|--------|
| SM-XXX | [Story title] | BR-XX |
| SM-XXX | [Story title] | BR-XX |

#### Slice 3: [Name]

[Brief description of what this slice adds]

| Story ID | Title | Source |
|----------|-------|--------|
| SM-XXX | [Story title] | BR-XX |
| SM-XXX | [Story title] | BR-XX |

### Wave 3 (sequential -- integration)

#### Slice 4: [Name]

[Brief description of what this slice integrates or validates]

| Story ID | Title | Source |
|----------|-------|--------|
| SM-XXX | [Story title] | BR-XX |

### Definition of Done

- [ ] [Functional completeness criteria]
- [ ] [Test coverage expectations]
- [ ] [End-to-end verification]
- [ ] [Deployment readiness]

---

## Release: [Release 2 Name]

### Transitions

| Aspect | Details |
|--------|---------|
| **Produces** | [What this release delivers] |
| **Requires** | [What must exist from Release 1] |
| **Unlocks** | [What becomes possible after] |

### Wave 1 (sequential -- foundation)

#### Slice N: [Name]

[Brief description]

| Story ID | Title | Source |
|----------|-------|--------|
| SM-XXX | [Story title] | BR-XX |

### Wave 2 (parallel -- independent slices)

#### Slice N+1: [Name]

[Brief description]

| Story ID | Title | Source |
|----------|-------|--------|
| SM-XXX | [Story title] | BR-XX |

#### Slice N+2: [Name]

[Brief description]

| Story ID | Title | Source |
|----------|-------|--------|
| SM-XXX | [Story title] | BR-XX |

### Definition of Done

- [ ] [Functional completeness criteria]
- [ ] [Test coverage expectations]
- [ ] [End-to-end verification]
- [ ] [Deployment readiness]

---

## Release: Future / Deferred

Stories not assigned to a concrete release. These remain in the backlog for future planning.

| Story ID | Title | Source | Reason Deferred |
|----------|-------|--------|-----------------|
| SM-XXX | [Story title] | BR-XX | [Why deferred] |

---

## Phase Numbering

Phases are numbered sequentially across all releases. Each slice = one phase.

| Phase | Release | Slice | Wave |
|-------|---------|-------|------|
| PHASE-1 | [Release 1] | [Slice 1 name] | W1 |
| PHASE-2 | [Release 1] | [Slice 2 name] | W2 |
| PHASE-3 | [Release 1] | [Slice 3 name] | W2 |
| PHASE-4 | [Release 1] | [Slice 4 name] | W3 |
| PHASE-5 | [Release 2] | [Slice 5 name] | W1 |
| PHASE-6 | [Release 2] | [Slice 6 name] | W2 |
| PHASE-7 | [Release 2] | [Slice 7 name] | W2 |

---

## Cross-Release Dependencies

| Dependency | From | To | Impact |
|------------|------|----|--------|
| [Entity/Service] | [Release.Slice] | [Release.Slice] | [What depends on what] |
| [Entity/Service] | [Release.Slice] | [Release.Slice] | [What depends on what] |

---

## Complementary Artifacts

- **Story map (journey view):** .charter/STORY-MAP.md (from `/create-story-map`)
- **Full story details with AC:** .charter/USER-STORIES.md (from `/create-requirements`)
- **Architecture reference:** .charter/ARCHITECTURE-DOC.md (from `/create-design-doc`)
- **Phase-level task breakdown:** Run `/plan-phase-tasks` for PHASE-N-PLAN.md files
