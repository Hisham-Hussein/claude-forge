---
name: plan-project-roadmap
description: This skill should be used when the user asks to "create project roadmap", "plan project phases", "organize user stories into phases", "create phase roadmap", "plan implementation roadmap", or needs to transform user stories and architecture documents into a phased delivery plan. Produces ROADMAP.md (~200-400 lines) that feeds into /plan-phase-tasks.
---

# Plan Project Roadmap

## Overview

Transform USER-STORIES.md and architecture documents into a phased delivery roadmap. This skill answers "WHICH stories, WHEN, in what order?" — not "HOW to implement" (that's later skills).

**Pipeline Position:**

```
USER-STORIES.md + ARCHITECTURE-DOC.md
         ↓
/plan-project-roadmap (THIS) → ROADMAP.md
         ↓
/plan-phase-tasks → PHASE-N-PLAN.md
         ↓
superpowers:writing-plans → TDD Implementation Plan
```

**Output Size:** ~200-400 lines (small enough for LLM coherence)

## Quick Start

**Required Inputs:**
- `USER-STORIES.md` with acceptance criteria
- `ARCHITECTURE-DOC.md` or design document

**Output:**
- `ROADMAP.md` — phases, story assignments, transitions, success criteria

**Invoke:** `/plan-project-roadmap` or ask "create a project roadmap"

## Process

### Step 1: Read Input Documents

Read USER-STORIES.md and ARCHITECTURE-DOC.md completely. Extract:

- All user stories with IDs and priorities (must-have, should-have, nice-to-have)
- Technical architecture layers and constraints
- Domain entities and their relationships
- External integrations required

### Step 2: Identify Foundation Stories

Foundation stories are must-haves with no dependencies on other stories. These become Phase 1.

**Foundation criteria:**
- Creates core domain entities
- Establishes architectural patterns other stories depend on
- Has no user story dependencies (may have technical dependencies)

### Step 3: Organize Remaining Stories

Group remaining stories into phases based on:

1. **Dependency order** — Stories that depend on Phase 1 outputs go in Phase 2+
2. **Vertical slice delivery** — Each phase delivers working end-to-end value
3. **Priority** — Must-haves before should-haves before nice-to-haves
4. **Complexity balance** — Distribute complexity across phases

### Step 4: Define Phase Transitions

For each phase boundary, explicitly document:

- What Phase N produces
- What Phase N+1 requires
- How Phase N outputs become Phase N+1 inputs

### Step 5: Generate ROADMAP.md

Follow the output format below exactly.

## Output Format

```markdown
# Project Roadmap

> **For Claude:** Use `/plan-phase-tasks` to decompose each phase into executable tasks.

**Project:** [Name]
**Goal:** [One sentence]
**Total Phases:** [N]
**Methodology:** Clean Architecture + Vertical Slices + FDD

---

## Phase Overview

| Phase | Stories | Focus | Dependencies |
|-------|---------|-------|--------------|
| 1 | US-001, US-002 | Foundation | None |
| 2 | US-003, US-004 | Core Features | Phase 1 |
| ... | ... | ... | ... |

---

## Phase 1: [Name]

**Stories:**
- US-001: [Title] (must-have)
- US-002: [Title] (must-have)

**Phase Goal:** [What this phase delivers as working functionality]

**Dependencies:** None (foundation phase)

**Architecture Layers Touched:**
- Domain: [entities, value objects]
- Application: [use cases]
- Infrastructure: [adapters, storage]

**Success Criteria:**
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]

**Definition of Done:**
- All tests pass
- Domain layer complete for listed entities
- Basic storage adapter functional

**Transition to Phase 2:**
- Phase 1 produces: [concrete outputs]
- Phase 2 requires: [concrete inputs]
- Handoff: [how outputs enable next phase]

---

## Phase 2: [Name]
...

---

## Phase N: [Name] (Final)

**Completion Criteria:**
- All must-have stories complete
- All acceptance criteria verified
- End-to-end user workflows functional
```

## Verification Checklist

Before finalizing ROADMAP.md, verify:

**Story Coverage:**
- [ ] All user stories from USER-STORIES.md assigned to exactly one phase
- [ ] No story assigned to multiple phases
- [ ] Must-have stories in early phases

**Dependency Validity:**
- [ ] Phase dependencies form valid DAG (no circular dependencies)
- [ ] Foundation phase has no dependencies
- [ ] Each phase's dependencies are in earlier phases

**Vertical Slices:**
- [ ] Each phase delivers working end-to-end functionality
- [ ] Not just horizontal layers (not "all domain first, then all adapters")

**Transitions:**
- [ ] Every phase transition has explicit output→input mapping
- [ ] No phase requires inputs not produced by earlier phases

**Architecture Alignment:**
- [ ] Phases respect Clean Architecture dependency rules
- [ ] Domain layer established before adapters depend on it

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Horizontal slicing (all domain first) | Use vertical slices — each phase delivers working value |
| Missing transitions | Explicitly document what each phase produces/requires |
| Story in multiple phases | Each story belongs to exactly one phase |
| Circular dependencies | Re-order phases to form valid DAG |
| Foundation too large | Keep Phase 1 minimal — only true foundation |

## Handoff

After ROADMAP.md is complete:

1. **User reviews** phase organization and transitions
2. **User selects** a phase to detail
3. **Invoke** `/plan-phase-tasks` with the selected phase

Example:
```
"Phase 1 looks good. Let's detail Phase 1 tasks."
→ /plan-phase-tasks --phase 1
```

## Additional Resources

### References
- **`references/phase-organization.md`** — Detailed phase organization patterns
- **`references/verification.md`** — Extended verification checklists

### Examples
- **`examples/sample-roadmap.md`** — Complete working example
