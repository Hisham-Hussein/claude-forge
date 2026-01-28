# Verification Checklists for Phase Plans

## Overview

These checklists ensure PHASE-N-PLAN.md is complete, consistent, and ready for superpowers:writing-plans. Run through each checklist before finalizing.

## Pre-Generation Checklist

Before generating PHASE-N-PLAN.md, verify inputs are complete:

### Input Documents

- [ ] ROADMAP.md exists (from /plan-project-roadmap)
- [ ] Selected phase number is valid (exists in ROADMAP.md)
- [ ] USER-STORIES.md available for AC details
- [ ] ARCHITECTURE-DOC.md available for layer guidance

### Phase Context

- [ ] Phase goal understood from ROADMAP.md
- [ ] Phase stories identified
- [ ] Prerequisites from earlier phases documented
- [ ] Phase success criteria available

## Post-Generation Checklist

After generating PHASE-N-PLAN.md, verify output quality:

### Task Quality

- [ ] Every task has Input defined
- [ ] Every task has Output defined
- [ ] Every task has Test strategy defined
- [ ] Every task has commit message
- [ ] No task is too vague ("implement feature")
- [ ] Tasks are atomic (one logical unit each)

**Vague Task Examples (AVOID):**
- "Implement discovery" → too broad
- "Add functionality" → meaningless
- "Set up stuff" → unclear

**Good Task Examples:**
- "Create Influencer entity with validation"
- "Implement SQLiteInfluencerRepository"
- "Add FollowerCount filter to use case"

### Dependency Order

- [ ] Tasks listed in valid dependency order
- [ ] Domain tasks before application tasks using them
- [ ] Application tasks before infrastructure tasks
- [ ] No task references output from later task
- [ ] Infrastructure tasks after interfaces they implement

**Validation Method:**
```
For each Task T at position P:
  For each dependency D in T.Input:
    If D is another task's output:
      Assert: That task is at position < P
```

### Architecture Alignment

- [ ] Each task specifies layer (Domain, Application, Infrastructure, UI)
- [ ] Each task specifies pattern (Entity, Repository, Service, etc.)
- [ ] Dependencies flow inward only
- [ ] No Infrastructure → Infrastructure direct dependencies
- [ ] Domain layer has no outward dependencies

**Layer Order Validation:**
```
Domain tasks MUST come before:
  - Application tasks that use domain entities
  - Infrastructure tasks that implement domain interfaces

Application tasks MUST come before:
  - Infrastructure tasks that depend on use cases
  - UI tasks that call use cases
```

### Acceptance Criteria Coverage

- [ ] Every AC from phase stories has at least one task
- [ ] No orphan ACs (ACs without corresponding tasks)
- [ ] No orphan tasks (tasks without AC justification)
- [ ] Test strategy covers all AC verification

**Mapping Validation:**
```
For each AC in phase stories:
  Assert: At least one task references this AC
  Assert: Task test strategy covers AC verification
```

### File Path Consistency

- [ ] File paths follow project conventions
- [ ] Domain files in `domain/` directory tree
- [ ] Application files in `application/` directory tree
- [ ] Infrastructure files in `adapters/` directory tree
- [ ] Test files mirror source structure in `tests/`

### Commit Message Quality

- [ ] All commits follow conventional format
- [ ] Scope matches layer (`domain`, `app`, `adapters`, `ui`)
- [ ] Type matches task type (`feat`, `fix`, `refactor`, `test`)
- [ ] Message describes what changes, not how

**Good Commits:**
- `feat(domain): add Influencer entity with validation`
- `feat(app): add DiscoverInfluencers use case`
- `fix(adapters): handle API timeout in TikTokAdapter`

**Bad Commits:**
- `update code` → no scope, vague message
- `feat: stuff` → vague, no scope
- `WIP` → not a real commit message

## Common Issues and Fixes

### Issue: Task Missing I/O/Test

**Symptom:** Task has description but no structured requirements.

**Fix:**
1. Identify what the task needs to start (Input)
2. Identify what the task produces (Output)
3. Identify how to verify correctness (Test)
4. Add all three to task definition

### Issue: Wrong Dependency Order

**Symptom:** Task 3 needs output from Task 5.

**Fix:**
1. Identify the dependency chain
2. Reorder tasks so dependencies come first
3. If circular, extract shared component into earlier task
4. Re-validate order

### Issue: Cross-Layer Task

**Symptom:** Single task touches Domain AND Infrastructure.

**Fix:**
1. Split into two tasks
2. First task: Domain work
3. Second task: Infrastructure work
4. Second task depends on first
5. Each task has single layer

### Issue: Task Too Large

**Symptom:** Task has 5+ files or multiple unrelated changes.

**Fix:**
1. Identify natural boundaries within task
2. Split into smaller tasks
3. Each task should be single-file or closely related files
4. Connect with explicit dependencies

### Issue: Orphan AC (No Task)

**Symptom:** AC exists but no task covers it.

**Fix:**
1. Create task specifically for this AC
2. Define I/O/Test for the task
3. Place in correct position per dependencies
4. Ensure test strategy covers AC

### Issue: Orphan Task (No AC)

**Symptom:** Task exists but doesn't trace to any AC.

**Fix:**
1. Review if task is actually needed
2. If needed: identify which AC it supports (may be implicit)
3. If not needed: remove task
4. Add AC reference to task if keeping

## Validation Script (Manual)

Run this mental script to validate PHASE-N-PLAN.md:

```
1. For each task:
   a. Assert: Has Input
   b. Assert: Has Output
   c. Assert: Has Test strategy
   d. Assert: Has commit message

2. Build dependency graph:
   a. For each task, record dependencies from Input
   b. Assert: No forward dependencies
   c. Assert: No circular dependencies

3. Check layer order:
   a. List all Domain tasks
   b. List all Application tasks
   c. List all Infrastructure tasks
   d. Assert: Domain positions < Application positions (for dependent tasks)
   e. Assert: Application positions < Infrastructure positions (for dependent tasks)

4. Map ACs to tasks:
   a. List all ACs from phase stories
   b. For each AC, find covering task(s)
   c. Assert: All ACs have at least one task

5. Validate handoff:
   a. For each story, check tasks are Superpowers-ready
   b. Assert: Tasks have enough detail for writing-plans
```

## Quality Metrics

### Good Phase Plan Characteristics

| Metric | Target |
|--------|--------|
| Tasks per story | 3-7 |
| I/O/Test completeness | 100% |
| Single-layer tasks | >90% |
| Valid dependency order | 100% |
| AC coverage | 100% |

### Warning Signs

| Warning | Likely Issue |
|---------|--------------|
| Task without Test | Will cause verification problems |
| 10+ tasks per story | Story may be too large, consider splitting |
| Multi-layer task | Violates single responsibility |
| "TBD" in I/O/Test | Not ready for implementation |
| Same file in 3+ tasks | May need refactoring strategy |

## Integration Readiness

### Ready for superpowers:writing-plans When:

- [ ] All tasks have I/O/Test defined
- [ ] Tasks are in valid dependency order
- [ ] Single layer per task
- [ ] File paths are realistic
- [ ] Test strategy is specific enough
- [ ] Commit messages are well-formed

### Not Ready If:

- Any task says "TBD" or "TODO"
- Tasks have forward dependencies
- Tasks span multiple layers
- No test strategy defined
- Vague file paths ("somewhere in domain/")
