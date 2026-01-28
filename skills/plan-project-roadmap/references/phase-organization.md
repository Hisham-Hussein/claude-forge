# Phase Organization: Patterns and Principles

## Overview

This reference provides detailed guidance for organizing user stories into phases. The goal is to create a roadmap where each phase delivers working vertical slices while respecting Clean Architecture dependencies.

**Note:** Examples throughout use an influencer marketing domain for illustration. Adapt all entity names, services, and features to match YOUR project's domain.

## Methodology Summary

### Clean Architecture + Vertical Slices + FDD

| Approach | Question Answered |
|----------|-------------------|
| **Clean Architecture** | How do I separate concerns? |
| **Vertical Slices** | How do I organize by features? |
| **FDD** | How do I decompose into work units? |

### Layer Dependencies

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

## Vertical Slices vs Horizontal Layers

### Traditional (Layer-First) — AVOID

```
Phase 1: All domain entities
Phase 2: All use cases
Phase 3: All adapters
Phase 4: All UI
```

**Problems:**
- No working software until Phase 4
- Can't demo progress
- Long feedback loops
- Integration surprises late

### Vertical Slices (Feature-First) — USE THIS

```
Phase 1: Discovery feature (Domain → Application → Infrastructure)
Phase 2: Enrichment feature (Domain → Application → Infrastructure)
Phase 3: Export feature (Domain → Application → Infrastructure)
Phase 4: UI layer (adds UI to all features)
```

**Benefits:**
- Each phase is shippable
- Faster feedback loops
- Parallel work possible
- Smaller blast radius
- Clear Definition of Done

**Within each slice, still follow Clean Architecture layer order.**

## Foundation Phase Identification

### What Makes a Foundation Story?

Foundation stories create the core that other features depend on. They:

1. **Create core domain entities** — the nouns of your system
2. **Establish patterns** — how things connect
3. **Have no story dependencies** — may have technical dependencies
4. **Are must-haves** — can't ship without them

### Foundation Phase Checklist

- [ ] Core domain entities defined
- [ ] Essential value objects created
- [ ] Repository interfaces declared
- [ ] Basic storage adapter working
- [ ] Seed/reference data loaded
- [ ] Development environment functional

### Example Foundation Phase

```markdown
## Phase 1: Foundation

**Stories:**
- US-001: Core Influencer entity
- US-002: Database setup and seeding

**What this establishes:**
- Influencer entity with validation
- InfluencerRepository interface
- ConvexInfluencerRepository implementation
- Niche and Platform reference data
- Development database populated

**What depends on this:**
- All discovery features need Influencer entity
- All storage features need Repository
- All classification features need reference data
```

## Phase Dependency Patterns

### Valid Dependency Graph

```
Phase 1 (Foundation)
    │
    ├── Phase 2 (Core Feature A)
    │       │
    │       └── Phase 4 (Feature A Enhancement)
    │
    └── Phase 3 (Core Feature B)
            │
            └── Phase 5 (Feature B Enhancement)
```

**Rules:**
- Arrows point forward (no backward dependencies)
- Each phase depends only on earlier phases
- Parallel phases have common ancestor

### Invalid Dependency Graph

```
Phase 1 ─── Phase 2 ─── Phase 3
    ↑                       │
    └───────────────────────┘  ← INVALID: Circular dependency
```

**If you find a circular dependency:**
1. Identify the shared concept causing the cycle
2. Extract it into an earlier phase
3. Make both phases depend on that earlier phase

## Phase Transition Documentation

### Explicit Transition Format

```markdown
**Transition to Phase N+1:**

| Phase N Produces | Phase N+1 Requires |
|------------------|-------------------|
| Influencer entity | ✓ Entity to enrich |
| InfluencerRepository | ✓ Storage for enriched data |
| Basic validation | ✓ Validation to extend |

**Handoff:**
- Phase N outputs stored in `domain/entities/`
- Phase N+1 imports and extends these
- No breaking changes to Phase N interfaces
```

### Why Explicit Transitions Matter

- Prevents starting without prerequisites
- Enables parallel planning
- Documents integration points
- Catches missing dependencies early

## Phase Sizing Guidelines

### Right-Sized Phase

| Characteristic | Target |
|----------------|--------|
| Stories | 2-4 user stories |
| Duration estimate | 1-2 weeks |
| Deliverable | Working vertical slice |
| Testability | Can demo/test independently |

### Phase Too Large — Split It

Signs:
- More than 5 stories
- Would take 3+ weeks
- Multiple unrelated features
- "And then also..." thinking

Solution:
- Identify natural boundaries
- Create two smaller phases
- Connect with explicit transitions

### Phase Too Small — Consider Combining

Signs:
- Only 1 story
- Less than 3 tasks
- Can't demo meaningfully
- Only partial functionality

Solution:
- Look for related story to combine
- Or accept as small phase if dependencies require it

## Priority-Based Organization

### MoSCoW in Phases

```
Must-have stories:   Phases 1-N (early phases)
Should-have stories: Phases N+1 to M (middle phases)
Nice-to-have stories: Phases M+1+ (later phases, may be cut)
```

### Priority to Phase Mapping

| Priority | Phase Placement | Rationale |
|----------|-----------------|-----------|
| Must-have | Phases 1-2 | Core value, can't ship without |
| Should-have | Phases 3-4 | Important but not blocking |
| Nice-to-have | Phases 5+ | If time permits |

### Handling Priority Conflicts

If a should-have story is needed by a must-have:
1. Re-evaluate the dependency
2. Consider elevating to must-have
3. Or extract the needed part into must-have phase

## Common Mistakes and Corrections

| Mistake | Why It's Wrong | Correction |
|---------|----------------|------------|
| Horizontal slicing | No working software until late | Use vertical slices |
| Missing transitions | Unclear dependencies | Document explicitly |
| Foundation too large | Delays first deliverable | Keep Phase 1 minimal |
| Story in multiple phases | Unclear ownership, double work | One phase per story |
| Circular dependencies | Impossible to execute | Re-order or extract |
| No success criteria | Can't verify completion | Add measurable criteria |

## Success Criteria Templates

### Phase Success Criteria

```markdown
**Success Criteria:**
- [ ] [Functional criterion - what works]
- [ ] [Quality criterion - how well]
- [ ] [Technical criterion - what's in place]
```

### Examples

```markdown
## Phase 1: Foundation

**Success Criteria:**
- [ ] Influencer entity validates all required fields
- [ ] Repository saves and retrieves without data loss
- [ ] 50+ seed influencers loaded correctly
- [ ] All unit tests pass
```

```markdown
## Phase 2: Discovery

**Success Criteria:**
- [ ] TikTok discovery returns 100+ influencers per query
- [ ] Results match filter criteria
- [ ] Discovered influencers persist to database
- [ ] Discovery can run unattended
```

## Definition of Done

### Per Story DoD

- [ ] All acceptance criteria pass (functional tests)
- [ ] Domain logic has unit tests (>90% coverage)
- [ ] Use cases have unit tests (>80% coverage)
- [ ] Adapters have integration tests
- [ ] No regressions (all existing tests pass)
- [ ] Works end-to-end
- [ ] Code committed with conventional message

### Per Phase DoD

- [ ] All stories in phase meet their DoD
- [ ] Phase delivers working vertical slice
- [ ] Phase outputs documented for next phase
- [ ] E2E test for slice passes
- [ ] Can demo to stakeholders
