# Workflow: Generate Execution Plan

<required_reading>
**Read these reference files NOW:**
1. references/methodology.md
2. references/task-decomposition.md
3. templates/execution-plan.md
</required_reading>

<process>

## Step 1: Load and Analyze Documents

**Read in order:**
1. USER-STORIES.md → Extract all stories, AC, MoSCoW priorities
2. ARCHITECTURE-DOC.md → Extract domain model, layers, interfaces
3. Optional docs → Extract constraints, tech decisions, domain context

**Build mental model:**
- What entities exist?
- What use cases are defined?
- What interfaces need implementation?
- What are the domain services?
- What external adapters are needed?

## Step 2: Group Stories into Vertical Slices

**Principle:** Each phase must deliver working end-to-end functionality.

**Grouping rules:**
1. Start with Must-have stories
2. Group by feature area (Epic/Feature)
3. Ensure each group can work independently
4. Dependencies flow forward (Phase N output → Phase N+1 input)

**Phase template:**
```
Phase N: [Vertical Slice Name]
├── Goal: [Working functionality when phase complete]
├── Stories: [US-XXX, US-YYY, ...]
├── Depends on: [Previous phase outputs]
└── Delivers: [What next phase can use]
```

## Step 3: Order Phases by Priority and Dependencies

**Ordering rules:**
1. Must-have before Should-have before Could-have
2. Foundation before features (domain entities before use cases)
3. Core before extensions (basic CRUD before advanced filters)
4. Dependencies respected (can't use what doesn't exist)

**First phase typically includes:**
- Core domain entities
- Repository interfaces
- Database schema
- Seed data (if needed)

## Step 4: Decompose Stories into Tasks

**For each story, decompose by Clean Architecture layer:**

```
Story US-XXX: [Story Name]
│
├── Layer: Domain
│   ├── Task X.1: Create [Entity/Value Object]
│   │   ├── Input: Requirements from AC
│   │   ├── Output: domain/entities/[name].ts
│   │   ├── Test: Unit test for validation rules
│   │   └── Commit: "feat(domain): add [name] entity"
│   │
│   └── Task X.2: Create [Domain Service] (if needed)
│       ├── Input: Entities, business rules from AC
│       ├── Output: domain/services/[name].ts
│       ├── Test: Unit test for business logic
│       └── Commit: "feat(domain): add [name] service"
│
├── Layer: Application
│   └── Task X.3: Create [Use Case]
│       ├── Input: Domain entities, interface contracts
│       ├── Output: application/[feature]/[usecase].ts
│       ├── Test: Unit test with mocked repositories
│       └── Commit: "feat(app): add [usecase] use case"
│
├── Layer: Infrastructure
│   ├── Task X.4: Create [Repository Implementation]
│   │   ├── Input: Repository interface from domain
│   │   ├── Output: adapters/storage/[repo].ts
│   │   ├── Test: Integration test against DB
│   │   └── Commit: "feat(adapters): implement [repo]"
│   │
│   └── Task X.5: Create [External Adapter] (if needed)
│       ├── Input: Adapter interface from domain
│       ├── Output: adapters/[concern]/[adapter].ts
│       ├── Test: Integration test with mocks/stubs
│       └── Commit: "feat(adapters): implement [adapter]"
│
└── Layer: UI (if applicable)
    └── Task X.6: Create [Component/Page]
        ├── Input: Use case, design specs
        ├── Output: ui/[feature]/[component].tsx
        ├── Test: Component test
        └── Commit: "feat(ui): add [component]"
```

**Task sizing:**
- Each task should be completable in one focused session
- If task feels too large, split further
- Aim for single-file changes when possible

## Step 5: Define Phase Transitions

**Document how output flows to next phase:**

```
| From Phase | To Phase | Output → Input |
|------------|----------|----------------|
| 1 | 2 | Influencer entity → Entity to enrich |
| 1 | 2 | Repository interface → Repo to implement |
| 2 | 3 | Discovery results → Data to display |
```

## Step 6: Write Definition of Done per Phase

**Standard DoD (customize as needed):**

```
### Definition of Done - Phase N

- [ ] All stories' acceptance criteria pass
- [ ] Domain: Unit tests >90% coverage
- [ ] Application: Unit tests >80% coverage (mocked repos)
- [ ] Adapters: Integration tests (happy path + error cases)
- [ ] UI: Component tests for critical paths
- [ ] No regressions (all existing tests pass)
- [ ] E2E: Vertical slice works end-to-end
- [ ] All commits follow conventional commit format
```

## Step 7: Generate Outputs

**1. EXECUTION-PLAN.md**

Use template from `templates/execution-plan.md`:
- Fill Executive Summary
- Fill Phase Overview table
- Fill each Phase Detail section
- Fill Phase Transitions table
- Fill Story-to-Phase Mapping appendix
- Fill Full AC Reference appendix

**2. jira-import.csv (if requested)**

Use format from `templates/jira-import.csv`:
```csv
Summary,Issue Type,Priority,Epic Link,Fix Version,Description,Acceptance Criteria
"[Story name]",Story,[Priority],[Epic],[Phase N],"[Full story text]","[AC1|AC2|AC3]"
```

## Step 8: Validate Plan

**Checklist:**
- [ ] All user stories appear exactly once
- [ ] Must-haves in Phases 1-2
- [ ] Each phase has clear goal and deliverable
- [ ] Every task has Input/Output/Test
- [ ] Phase transitions are explicit
- [ ] DoD is testable
- [ ] No circular dependencies

**Ask user to review before finalizing.**

</process>

<success_criteria>
This workflow is complete when:

- [ ] EXECUTION-PLAN.md written with all sections
- [ ] All stories assigned to phases
- [ ] All tasks have explicit I/O/Test
- [ ] Phase transitions documented
- [ ] jira-import.csv generated (if requested)
- [ ] User has reviewed and approved plan
</success_criteria>
