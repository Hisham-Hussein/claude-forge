# Methodology: Clean Architecture + Vertical Slices + FDD

<overview>
This methodology combines three complementary approaches for AI-assisted development:

1. **Clean Architecture** - Separates business rules from infrastructure
2. **Vertical Slice Architecture** - Organizes by features, not layers
3. **Feature-Driven Development** - Atomic, testable work units

They answer different questions:
- Clean Architecture: "How do I separate concerns?"
- Vertical Slices: "How do I organize by features?"
- FDD: "How do I decompose into work units?"

**Note:** Examples throughout this document use an influencer marketing domain for illustration. Adapt all entity names, services, and features to match YOUR project's domain model.
</overview>

<clean_architecture>
## Clean Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│                    DOMAIN LAYER                      │
│  Entities │ Value Objects │ Domain Services │ Interfaces │
│           (Pure business logic, no dependencies)     │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│               APPLICATION LAYER                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │Feature A │ │Feature B │ │Feature C │  ← Slices  │
│  │ Use Case │ │ Use Case │ │ Use Case │            │
│  └──────────┘ └──────────┘ └──────────┘            │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│              INFRASTRUCTURE LAYER                    │
│  Repositories │ API Adapters │ Database │ External  │
│         (Implements Domain interfaces)               │
└─────────────────────────────────────────────────────┘
```

**Dependency Rule:** Dependencies point inward. Domain knows nothing about infrastructure.

**Key Principles:**
- Domain layer has ZERO external dependencies
- Interfaces defined in Domain, implemented in Infrastructure
- Use cases orchestrate domain logic
- Infrastructure is swappable
</clean_architecture>

<vertical_slices>
## Vertical Slice Architecture

**Principle:** Each phase delivers working end-to-end functionality.

```
Traditional (Layer-First):          Vertical Slices (Feature-First):
Phase 1: All domain entities        Phase 1: Discovery feature (E2E)
Phase 2: All use cases              Phase 2: Enrichment feature (E2E)
Phase 3: All adapters               Phase 3: Export feature (E2E)
Phase 4: All UI                     Phase 4: UI feature (E2E)
```

**Why Vertical Slices:**
- Each phase is shippable
- Faster feedback loops
- Parallel work possible
- Smaller blast radius
- Clear Definition of Done

**Within each slice, still use Clean Architecture layers.**
</vertical_slices>

<fdd_tasks>
## FDD-Style Task Decomposition

**Feature-Driven Development work unit:**

```
Feature: [Verb] [Object] [Context]
Example: "Calculate the total of a sale"

Task Breakdown:
├── Task 1: Create [Value Object/Entity]
│   ├── Input: Domain requirements
│   ├── Output: Tested domain object
│   └── Test: Unit tests for validation
│
├── Task 2: Create [Use Case/Handler]
│   ├── Input: Domain objects, interfaces
│   ├── Output: Working use case
│   └── Test: Unit tests with mocks
│
└── Task 3: Create [Adapter]
    ├── Input: Interface contract
    ├── Output: Working adapter
    └── Test: Integration tests
```

**Why explicit I/O/Test:**
- AI agents work better with clear contracts
- Verification is built-in
- Atomic commits possible
- Rollback points clear
</fdd_tasks>

<how_they_integrate>
## How They Work Together

```
/create-execution-plan (PROJECT LEVEL)
│
│  Output: Phases with stories, tasks with I/O/Test
│
└──> Pick a story (e.g., US-001)
     │
     └──> superpowers:writing-plans (FEATURE LEVEL)
          │
          │  Output: TDD steps per task
          │  ┌────────────────────────────────────┐
          │  │ Task 1: Create DiscoveryConfig     │
          │  │   Step 1: Write failing test       │
          │  │   Step 2: Run test (expect fail)   │
          │  │   Step 3: Minimal implementation   │
          │  │   Step 4: Run test (expect pass)   │
          │  │   Step 5: Commit                   │
          │  └────────────────────────────────────┘
          │
          └──> superpowers:executing-plans
               │
               └──> Code committed, story done
```

**The execution plan provides WHAT to build.**
**The writing-plans skill provides HOW to build each task.**
**The executing-plans skill DOES the work.**
</how_they_integrate>

<phase_transitions>
## Phase Transitions

**Principle:** Each phase's output is the next phase's input.

*Example (adapt to your project's domain):*
```
Phase N Output          →  Phase N+1 Input
────────────────────       ─────────────────────
Influencer entity          ✓ Entity to populate
InfluencerRepository       ✓ Repo to save discoveries
Database schema            ✓ Schema to write to
Seed data (niches)         ✓ Niches for classification
```

**Document transitions explicitly.** This prevents:
- Starting work without prerequisites
- Skipping foundational work
- Broken dependencies
</phase_transitions>

<definition_of_done>
## Definition of Done

**Standard DoD per story:**

- [ ] All acceptance criteria pass (functional tests)
- [ ] Domain logic has unit tests (>90% coverage)
- [ ] Use cases have unit tests (>80% coverage, mocked repos)
- [ ] Adapters have integration tests (happy path + errors)
- [ ] No regressions (all existing tests pass)
- [ ] Works end-to-end (manual or E2E test)
- [ ] Code committed with conventional commit message

**Standard DoD per phase:**

- [ ] All stories in phase meet their DoD
- [ ] Phase delivers working vertical slice
- [ ] Phase outputs documented for next phase
- [ ] E2E test for slice passes
</definition_of_done>
