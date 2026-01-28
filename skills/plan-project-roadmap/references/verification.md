# Verification Checklists for Project Roadmaps

## Overview

These checklists ensure ROADMAP.md is complete, consistent, and ready for the next skill in the pipeline. Run through each checklist before finalizing.

## Pre-Generation Checklist

Before generating ROADMAP.md, verify inputs are complete:

### Input Documents

- [ ] USER-STORIES.md exists and is readable
- [ ] USER-STORIES.md has story IDs (US-XXX format)
- [ ] USER-STORIES.md has priorities (must-have, should-have, nice-to-have)
- [ ] USER-STORIES.md has acceptance criteria for each story
- [ ] ARCHITECTURE-DOC.md exists and is readable
- [ ] ARCHITECTURE-DOC.md defines layers (Domain, Application, Infrastructure)
- [ ] ARCHITECTURE-DOC.md identifies core entities
- [ ] ARCHITECTURE-DOC.md specifies technology stack

### Understanding Verification

- [ ] All user stories are understood (no ambiguous requirements)
- [ ] Architecture layers are clear
- [ ] External integrations are identified
- [ ] Technical constraints are documented

## Post-Generation Checklist

After generating ROADMAP.md, verify output quality:

### Story Coverage

- [ ] Every story from USER-STORIES.md appears in exactly one phase
- [ ] No stories are missing
- [ ] No stories are duplicated across phases
- [ ] Must-have stories are in early phases (1-2)
- [ ] Should-have stories are in middle phases
- [ ] Nice-to-have stories are in later phases

### Dependency Validity

- [ ] Phase 1 has no dependencies (foundation)
- [ ] Each phase's dependencies are only from earlier phases
- [ ] No circular dependencies exist
- [ ] Dependency graph is a valid DAG

**Validation Method:**
```
For each Phase N (where N > 1):
  For each dependency D:
    Assert: D is in Phase 1..N-1
```

### Vertical Slice Delivery

- [ ] Each phase delivers working end-to-end functionality
- [ ] Not organized by horizontal layers (not "all domain, then all application")
- [ ] Each phase can be demonstrated to stakeholders
- [ ] Each phase produces usable value

**Red Flags:**
- Phase with only domain tasks
- Phase with only infrastructure tasks
- Phase described as "preparation for..."
- Phase with no testable deliverable

### Transition Completeness

- [ ] Every phase (except last) has explicit transition to next phase
- [ ] Transitions specify what Phase N produces
- [ ] Transitions specify what Phase N+1 requires
- [ ] Handoff is clear (how outputs enable next phase)
- [ ] No phase starts with unmet prerequisites

**Validation Method:**
```
For each Phase N → Phase N+1 transition:
  For each "Phase N+1 requires" item:
    Assert: Item is in "Phase N produces" list
```

### Architecture Alignment

- [ ] Foundation phase establishes core domain entities
- [ ] Repository interfaces defined before implementations
- [ ] Dependencies flow inward (Infrastructure → Application → Domain)
- [ ] No adapter-to-adapter dependencies

### Success Criteria Quality

- [ ] Every phase has explicit success criteria
- [ ] Criteria are measurable (not vague)
- [ ] Criteria are testable
- [ ] Definition of Done is specified per phase

**Good Criteria:**
- "TikTok discovery returns 100+ influencers per query"
- "All unit tests pass with >90% coverage"
- "Can filter by at least 3 criteria"

**Bad Criteria:**
- "Discovery works"
- "Code is good"
- "Feature is complete"

## Common Issues and Fixes

### Issue: Story Missing from Roadmap

**Symptom:** USER-STORIES.md has US-007, but ROADMAP.md doesn't mention it.

**Fix:**
1. Find US-007 in USER-STORIES.md
2. Identify its dependencies and priority
3. Add to appropriate phase
4. Update phase story list and success criteria

### Issue: Circular Dependency

**Symptom:** Phase 3 depends on Phase 4 output.

**Fix:**
1. Identify what Phase 3 needs from Phase 4
2. Extract that component into Phase 2 or 3
3. Make both Phase 3 and 4 depend on the extracted phase
4. Re-validate dependency graph

### Issue: Horizontal Slicing

**Symptom:** Phase 1 is "All domain entities", Phase 2 is "All use cases".

**Fix:**
1. Identify primary features/capabilities
2. Reorganize so each phase delivers one feature E2E
3. Domain → Application → Infrastructure within each phase
4. Keep shared foundation in Phase 1 only

### Issue: Missing Foundation

**Symptom:** Phase 1 has user-facing features, core entities appear in Phase 2.

**Fix:**
1. Identify truly foundational stories (core entities, base infrastructure)
2. Create/modify Phase 1 to be foundation-only
3. Move user-facing features to Phase 2+
4. Ensure Phase 1 has no dependencies

### Issue: Vague Success Criteria

**Symptom:** "Phase complete when feature works."

**Fix:**
1. List specific acceptance criteria from stories
2. Add measurable metrics (counts, percentages)
3. Add testable conditions (can do X, Y, Z)
4. Include technical DoD (tests pass, coverage met)

## Validation Script (Manual)

Run this mental script to validate ROADMAP.md:

```
1. Count stories in USER-STORIES.md = N
2. Count story references in ROADMAP.md phases = M
3. Assert: N == M (no missing, no duplicates)

4. For each phase dependency:
   - Assert: dependency is in earlier phase

5. For each phase:
   - Assert: has success criteria
   - Assert: delivers working value
   - Assert: has transition to next (if not last)

6. Phase 1 check:
   - Assert: no dependencies
   - Assert: establishes foundation
   - Assert: all must-haves started here or in Phase 2
```

## Quality Metrics

### Good Roadmap Characteristics

| Metric | Target |
|--------|--------|
| Stories per phase | 2-4 |
| Phases total | 3-7 |
| Foundation phase size | 15-25% of total |
| Must-have completion | By Phase 2-3 |
| Transition clarity | 100% explicit |

### Warning Signs

| Warning | Likely Issue |
|---------|--------------|
| Phase 1 has 8 stories | Foundation too large, consider splitting |
| Phase 5 has 1 story | Consider combining with Phase 4 |
| 10+ phases | May be over-decomposed, consider consolidation |
| No transitions documented | Will cause integration confusion |
| All must-haves in Phase 1 | Foundation may be doing too much |
