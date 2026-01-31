# [Project Name] Execution Plan

**Generated:** [Date]
**Methodology:** Clean Architecture + Vertical Slices + FDD
**Source Documents:**
- USER-STORIES.md ([X] stories)
- ARCHITECTURE-DOC.md
- [Optional documents listed]

---

## Executive Summary

**Total Stories:** [X]
**Total Phases:** [N]
**Priority Distribution:**
- Must-have: [X] stories
- Should-have: [Y] stories
- Could-have: [Z] stories

**Key Deliverables:**
1. Phase 1: [Working functionality]
2. Phase 2: [Working functionality]
3. ...

---

## Phase Overview

| Phase | Name | Stories | Priority Focus | Deliverable |
|-------|------|---------|----------------|-------------|
| 1 | [Name] | [N] | Must | [Working increment] |
| 2 | [Name] | [N] | Must | [Working increment] |
| 3 | [Name] | [N] | Should | [Working increment] |
| ... | ... | ... | ... | ... |

---

## Phase 1: [Name]

### Goal
[One sentence describing the working increment this phase delivers]

### Vertical Slice
[What end-to-end functionality works when this phase is complete]

### Stories Included

| ID | Story | Size | Priority | AC Count |
|----|-------|------|----------|----------|
| US-001 | [Story name] | [S/M/L] | Must | [N] |
| US-002 | [Story name] | [S/M/L] | Must | [N] |

### Task Breakdown

#### US-001: [Story Name]

##### Layer: Domain

**Task 1.1: [Create Entity/VO]**
- **Input:** [Requirements from AC]
- **Output:** [File path]
- **Test:** [Test type and what it verifies]
- **Commit:** `feat(domain): [message]`

**Task 1.2: [Create Domain Service]** (if needed)
- **Input:** [Dependencies]
- **Output:** [File path]
- **Test:** [Test type and what it verifies]
- **Commit:** `feat(domain): [message]`

##### Layer: Application

**Task 1.3: [Create Use Case]**
- **Input:** [Domain objects, interfaces]
- **Output:** [File path]
- **Test:** [Unit test with mocked repos]
- **Commit:** `feat(app): [message]`

##### Layer: Infrastructure

**Task 1.4: [Create Repository Implementation]**
- **Input:** [Interface from domain]
- **Output:** [File path]
- **Test:** [Integration test]
- **Commit:** `feat(adapters): [message]`

**Task 1.5: [Create External Adapter]** (if needed)
- **Input:** [Interface, API docs]
- **Output:** [File path]
- **Test:** [Integration test with mocks]
- **Commit:** `feat(adapters): [message]`

##### Layer: UI (if applicable)

**Task 1.6: [Create Component/Page]**
- **Input:** [Use case, design specs]
- **Output:** [File path]
- **Test:** [Component/E2E test]
- **Commit:** `feat(ui): [message]`

#### US-002: [Story Name]

[Same structure as above]

### Phase Input (Prerequisites)
- [ ] [What must exist before starting this phase]
- [ ] [Dependencies from previous phases]

### Phase Output (Deliverables)
- [ ] [What this phase produces]
- [ ] [What next phase can use]

### Definition of Done
- [ ] All stories' acceptance criteria pass
- [ ] Domain: Unit tests >90% coverage
- [ ] Application: Unit tests >80% coverage (mocked repos)
- [ ] Adapters: Integration tests (happy path + error cases)
- [ ] UI: Component tests for critical paths (if applicable)
- [ ] No regressions (all existing tests pass)
- [ ] E2E: Vertical slice works end-to-end
- [ ] All commits follow conventional commit format

### Testing Requirements

| Story | Unit Tests | Integration | E2E |
|-------|------------|-------------|-----|
| US-001 | [What to unit test] | [What to integration test] | [E2E scenario] |
| US-002 | [What to unit test] | [What to integration test] | [E2E scenario] |

---

## Phase 2: [Name]

[Same structure as Phase 1]

---

## Phase Transitions

| From Phase | To Phase | Output → Input |
|------------|----------|----------------|
| 1 | 2 | [Entity] → [Entity to use] |
| 1 | 2 | [Interface] → [Interface to implement] |
| 2 | 3 | [Result] → [Data to display] |

---

## Risk Mitigation Per Phase

| Phase | Risk | Mitigation |
|-------|------|------------|
| 1 | [Risk description] | [Mitigation strategy] |
| 2 | [Risk description] | [Mitigation strategy] |

---

## Appendix A: Story-to-Phase Mapping

| Story ID | Story Name | Phase | Priority | Status |
|----------|------------|-------|----------|--------|
| US-001 | [Name] | 1 | Must | Planned |
| US-002 | [Name] | 1 | Must | Planned |
| US-003 | [Name] | 2 | Must | Planned |
| ... | ... | ... | ... | ... |

---

## Appendix B: Full Acceptance Criteria Reference

### US-001: [Story Name]
- [ ] [AC 1]
- [ ] [AC 2]
- [ ] [AC 3]

### US-002: [Story Name]
- [ ] [AC 1]
- [ ] [AC 2]

[Include all stories with their AC for reference during TDD]

---

## Appendix C: Integration with Development Skills

**After this plan is created, use:**

1. **Pick a story from current phase**

2. **Create implementation plan:**
   ```
   superpowers:writing-plans for [US-XXX]
   ```
   This creates detailed TDD steps for each task.

3. **Execute the plan:**
   ```
   superpowers:executing-plans
   ```
   This implements each step with Red-Green-Refactor.

4. **When phase complete, move to next phase**
