---
name: plan-phase-tasks
description: This skill should be used when the user asks to "plan phase tasks", "decompose phase into tasks", "create phase plan", "break down phase N", "detail phase implementation", or needs to transform a phase from ROADMAP.md into atomic tasks with I/O/Test. Produces PHASE-N-PLAN.md (~150-300 lines) that feeds into superpowers:writing-plans.
---

# Plan Phase Tasks

## Overview

Transform a single phase from ROADMAP.md into atomic, TDD-ready tasks. This skill answers "WHAT tasks exist for this phase?" — not "HOW to implement each task" (that's superpowers:writing-plans).

**Pipeline Position:**

```
ROADMAP.md (from /plan-project-roadmap)
         ↓
/plan-phase-tasks (THIS) → PHASE-N-PLAN.md
         ↓
superpowers:writing-plans → TDD Implementation Plan
         ↓
superpowers:executing-plans → Code
```

**Output Size:** ~150-300 lines per phase (focused, verifiable)

## Quick Start

**Required Inputs:**
- `ROADMAP.md` (from /plan-project-roadmap)
- Phase number to decompose
- `ARCHITECTURE-DOC.md` for technical context

**Output:**
- `PHASE-N-PLAN.md` — stories with atomic tasks, each having I/O/Test

**Invoke:** `/plan-phase-tasks --phase 1` or ask "break down phase 1 tasks"

## Process

### Step 1: Load Phase Context

Read ROADMAP.md and extract for the selected phase:

- Phase goal and success criteria
- Stories assigned to this phase
- Dependencies from earlier phases
- Phase transitions (what this phase produces)

### Step 2: Load Story Details

For each story in the phase, read USER-STORIES.md to get:

- Full acceptance criteria
- Priority (must-have, should-have, nice-to-have)
- Any notes or constraints

### Step 3: Decompose Each Story into Tasks

For each story, identify atomic tasks. Each task is:

- **One logical unit of work** — creates/modifies one component
- **Has clear boundaries** — explicit Input/Output/Test
- **Architecture-aligned** — respects Clean Architecture layers

**Task decomposition pattern:**

```
Story: US-XXX
├── Task 1: Create domain entity
├── Task 2: Create value objects
├── Task 3: Create domain service (if needed)
├── Task 4: Create application use case
├── Task 5: Create storage adapter
├── Task 6: Create integration test
└── Task 7: Wire up and verify
```

### Step 4: Define I/O/Test for Each Task

Every task MUST have:

| Component | Description |
|-----------|-------------|
| **Input** | What this task needs to start (files, data, prior tasks) |
| **Output** | What this task produces (files, interfaces, functionality) |
| **Test** | How to verify correctness (unit test, integration test, manual check) |

### Step 5: Verify Architecture Alignment

For each task, verify:

- Layer placement (Domain, Application, Infrastructure)
- Pattern usage (Entity, Repository, Service, Use Case)
- Dependency direction (inward only)

### Step 6: Generate PHASE-N-PLAN.md

Follow the output format below exactly.

## Output Format

```markdown
# Phase N Plan: [Phase Name]

> **For Claude:** Use `superpowers:writing-plans` to create TDD implementation plans for each story's tasks.

**Phase:** N of M
**Goal:** [Phase goal from ROADMAP.md]
**Stories:** US-XXX, US-YYY
**Prerequisites:** [What must exist from earlier phases]

---

## Story: US-XXX — [Title]

**Priority:** must-have | should-have | nice-to-have

### Acceptance Criteria

(Copy from USER-STORIES.md)

- AC1: [Criterion]
- AC2: [Criterion]

### Tasks

#### Task 1: Create [Component]

**Type:** Create | Modify | Test | Infrastructure

**Layer:** Domain | Application | Infrastructure

**Input:**
- [What this task needs]
- [Prior task outputs if any]

**Output:**
- [Files created/modified]
- [Interfaces exposed]

**Files (estimated):**
- `domain/entities/foo.py` — Create
- `domain/value_objects/bar.py` — Create

**Test Strategy:**
- Unit: [What to unit test]
- Integration: [If applicable]

**Architecture Alignment:**
- Pattern: Entity | Repository | Service | Use Case | Adapter
- Dependencies: [What this depends on]
- Dependents: [What depends on this]

**Commit:** `feat(domain): add Foo entity with Bar value object`

---

#### Task 2: Create [Component]
...

---

## Story: US-YYY — [Title]
...

---

## Phase Verification

### Pre-Implementation Checks
- [ ] All tasks have explicit I/O/Test
- [ ] Tasks ordered by dependency (no forward references)
- [ ] Architecture layers respected
- [ ] Acceptance criteria mapped to tasks

### Post-Implementation Checks
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Success criteria from ROADMAP.md met
- [ ] Phase outputs ready for next phase

### Handoff to Next Phase
- **Produces:** [Concrete outputs]
- **Enables:** [What Phase N+1 can now do]
```

## Task Structure Requirements

**Every task MUST have:**

```text
Task X: [Description]
├── Input: What this task needs to start
├── Output: What this task produces
├── Test: How to verify correctness
└── Commit: Conventional commit message
```

**Why this matters:** Explicit I/O/Test minimizes AI coding errors. Ambiguous requirements cause implementation drift.

## Verification Checklist

Before finalizing PHASE-N-PLAN.md:

**Task Quality:**
- [ ] Every task has Input, Output, Test defined
- [ ] No task is "implement feature" (too vague)
- [ ] Tasks are atomic (one logical unit each)

**Dependency Order:**
- [ ] Tasks listed in dependency order
- [ ] No task references output from later task
- [ ] Domain tasks before adapters that use them

**Architecture Alignment:**
- [ ] Each task specifies layer and pattern
- [ ] Dependencies flow inward (Infrastructure → Application → Domain)
- [ ] No adapter directly depends on another adapter

**Acceptance Criteria Coverage:**
- [ ] Every AC has at least one task covering it
- [ ] Test strategy covers all AC verification

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Vague tasks ("implement login") | Specific ("create User entity with email/password") |
| Missing I/O | Every task needs explicit Input/Output |
| Missing test strategy | Every task needs verification approach |
| Wrong dependency order | Domain → Application → Infrastructure |
| Tasks too large | Break into smaller atomic units |
| Cross-layer tasks | One layer per task |

## Handoff to Superpowers

After PHASE-N-PLAN.md is complete:

1. **User reviews** task breakdown and I/O/Test definitions
2. **User selects** a story to implement
3. **Invoke** `superpowers:writing-plans` with the story's tasks

Example workflow:
```
"Phase 1 tasks look good. Let's implement US-001."
→ superpowers:writing-plans

writing-plans will:
1. Take the tasks from PHASE-1-PLAN.md
2. Create TDD-ready steps with exact file paths
3. Include complete code snippets
4. Produce docs/plans/YYYY-MM-DD-us-001.md
```

**Integration Contract:**

| This Skill Produces | writing-plans Expects |
|---------------------|----------------------|
| Tasks with I/O/Test | Tasks to decompose into steps |
| Estimated file paths | Exact file paths with line numbers |
| Test strategy | Complete test code |
| Commit message | Commit commands |

## Additional Resources

### References
- **`references/task-decomposition.md`** — FDD-style task patterns
- **`references/verification.md`** — Extended verification checklists

### Examples
- **`examples/sample-phase-plan.md`** — Complete working example
