# Task Decomposition: FDD-Style Atomic Tasks

## Overview

Every task must have explicit Input/Output/Test. This structure minimizes AI coding errors by:
- Making requirements unambiguous
- Providing clear success criteria
- Enabling atomic commits
- Supporting TDD workflow

**Note:** Examples throughout use an influencer marketing domain for illustration. Adapt all entity names, value objects, services, and components to match YOUR project's domain.

## Task Template

```markdown
### Task X.Y: [Verb] [Object]

**Type:** Create | Modify | Test | Infrastructure

**Layer:** Domain | Application | Infrastructure | UI

**Input:**
- [What this task needs to start]
- [Prerequisites, dependencies, contracts]

**Output:**
- [File(s) created or modified]
- [Artifact(s) produced]

**Files (estimated):**
- `path/to/file.py` — Create
- `path/to/other.py` — Modify

**Test Strategy:**
- Unit: [What to unit test]
- Integration: [If applicable]

**Architecture Alignment:**
- Pattern: Entity | Repository | Service | Use Case | Adapter
- Dependencies: [What this depends on]
- Dependents: [What depends on this]

**Commit:** `feat|fix|refactor(scope): message`
```

## Decomposition by Clean Architecture Layer

### Domain Layer Tasks

**Entities:**

*Example:*
```markdown
### Task 1.1: Create Influencer entity

**Type:** Create
**Layer:** Domain

**Input:**
- Business rules from USER-STORIES.md (US-001 AC)
- Entity relationship diagram from architecture doc

**Output:**
- Influencer entity with validation logic
- Type definitions for required fields

**Files (estimated):**
- `domain/entities/influencer.py` — Create

**Test Strategy:**
- Unit: validation rules, required fields, optional fields

**Architecture Alignment:**
- Pattern: Entity
- Dependencies: None (domain core)
- Dependents: Repository interface, use cases

**Commit:** `feat(domain): add Influencer entity`
```

**Value Objects:**

*Example:*
```markdown
### Task 1.2: Create FollowerCount value object

**Type:** Create
**Layer:** Domain

**Input:**
- Business constraints (min: 10K, max: 100M)
- Validation rules from AC

**Output:**
- Immutable FollowerCount value object
- Validation on construction

**Files (estimated):**
- `domain/value_objects/follower_count.py` — Create

**Test Strategy:**
- Unit: validation, immutability, equality

**Architecture Alignment:**
- Pattern: Value Object
- Dependencies: None
- Dependents: Influencer entity

**Commit:** `feat(domain): add FollowerCount value object`
```

**Domain Services:**

*Example:*
```markdown
### Task 1.3: Create EngagementCalculator service

**Type:** Create
**Layer:** Domain

**Input:**
- Engagement formula from business case
- Input metrics (followers, likes, comments)

**Output:**
- Pure function that calculates engagement rate
- No side effects

**Files (estimated):**
- `domain/services/engagement_calculator.py` — Create

**Test Strategy:**
- Unit: calculation accuracy, edge cases (zero followers)

**Architecture Alignment:**
- Pattern: Domain Service
- Dependencies: None (pure business logic)
- Dependents: Use cases

**Commit:** `feat(domain): add EngagementCalculator service`
```

**Repository Interfaces:**

*Example:*
```markdown
### Task 1.4: Define InfluencerRepository interface

**Type:** Create
**Layer:** Domain

**Input:**
- Use case requirements
- CRUD operations needed

**Output:**
- Abstract interface defining repository contract
- Method signatures with types

**Files (estimated):**
- `domain/repositories/influencer_repository.py` — Create

**Test Strategy:**
- N/A (interface only, tested via implementations)

**Architecture Alignment:**
- Pattern: Repository Interface
- Dependencies: Influencer entity
- Dependents: Repository implementations, use cases

**Commit:** `feat(domain): define InfluencerRepository interface`
```

### Application Layer Tasks

**Use Cases:**

*Example:*
```markdown
### Task 2.1: Create DiscoverInfluencers use case

**Type:** Create
**Layer:** Application

**Input:**
- InfluencerRepository interface
- DiscoveryConfig value object
- Platform adapter interface

**Output:**
- Use case orchestrating discovery flow
- Returns list of discovered influencers

**Files (estimated):**
- `application/discovery/discover_influencers.py` — Create

**Test Strategy:**
- Unit: with mocked repository and adapter
- Integration: full flow with test doubles

**Architecture Alignment:**
- Pattern: Use Case
- Dependencies: Domain entities, repository interface
- Dependents: API handlers, CLI commands

**Commit:** `feat(app): add DiscoverInfluencers use case`
```

### Infrastructure Layer Tasks

**Repository Implementations:**

*Example:*
```markdown
### Task 3.1: Implement SQLiteInfluencerRepository

**Type:** Create
**Layer:** Infrastructure

**Input:**
- InfluencerRepository interface
- Database schema
- Connection configuration

**Output:**
- Working repository implementation
- CRUD operations against SQLite

**Files (estimated):**
- `adapters/storage/sqlite_influencer_repository.py` — Create

**Test Strategy:**
- Integration: against test SQLite database
- Covers: save, find_by_id, find_all, update, delete

**Architecture Alignment:**
- Pattern: Repository Implementation
- Dependencies: InfluencerRepository interface, Influencer entity
- Dependents: Use cases (via DI)

**Commit:** `feat(adapters): implement SQLiteInfluencerRepository`
```

**External Adapters:**

*Example:*
```markdown
### Task 3.2: Implement TikTokDiscoveryAdapter

**Type:** Create
**Layer:** Infrastructure

**Input:**
- DiscoveryAdapter interface
- TikTok API documentation
- API credentials configuration

**Output:**
- Working adapter calling TikTok API
- Transforms API response to domain entities

**Files (estimated):**
- `adapters/platforms/tiktok_discovery_adapter.py` — Create

**Test Strategy:**
- Integration: with VCR/recorded responses
- Unit: response transformation logic

**Architecture Alignment:**
- Pattern: Adapter
- Dependencies: DiscoveryAdapter interface
- Dependents: DiscoverInfluencers use case

**Commit:** `feat(adapters): implement TikTokDiscoveryAdapter`
```

### UI Layer Tasks

**Components:**

*Example:*
```markdown
### Task 4.1: Create InfluencerCard component

**Type:** Create
**Layer:** UI

**Input:**
- Design specs
- Influencer entity shape
- Component library (if any)

**Output:**
- Reusable card component
- Displays influencer summary

**Files (estimated):**
- `ui/components/InfluencerCard.tsx` — Create

**Test Strategy:**
- Component: renders correctly with various data
- Visual: matches design specs

**Architecture Alignment:**
- Pattern: Presentation Component
- Dependencies: Influencer data shape
- Dependents: List pages, detail pages

**Commit:** `feat(ui): add InfluencerCard component`
```

## Task Sizing Guidance

### Right-Sized Task

| Characteristic | Target |
|----------------|--------|
| Completable in | One focused session |
| File changes | Single file (ideal), 2-3 max |
| Clear boundaries | Obvious start and end |
| Testable | Can verify in isolation |

### Too Large — Split It

Signs:
- Multiple unrelated changes
- Multiple files in different layers
- "And then also..." in description
- No clear stopping point
- Would take more than a day

Solution:
- Identify natural boundaries
- Create separate tasks for each boundary
- Connect with dependencies

### Too Small — Consider Combining

Signs:
- Trivial one-liner
- Only makes sense with another task
- No meaningful test possible
- Takes less than 15 minutes

Solution:
- Combine with related task
- Keep if dependency order requires it

## Commit Conventions

**Format:** `type(scope): message`

**Types:**
| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructure (no behavior change) |
| `test` | Test addition/modification |
| `docs` | Documentation |
| `chore` | Maintenance |

**Scopes:**
| Scope | Layer |
|-------|-------|
| `domain` | Domain layer |
| `app` | Application layer |
| `adapters` | Infrastructure layer |
| `ui` | UI layer |
| `config` | Configuration |

**Examples:**
```
feat(domain): add Influencer entity with validation
feat(app): add DiscoverInfluencers use case
feat(adapters): implement TikTokDiscoveryAdapter
feat(ui): add InfluencerCard component
fix(domain): correct engagement rate calculation
test(app): add unit tests for DiscoverInfluencers
```

## From Acceptance Criteria to Tasks

### Mapping Pattern

Every AC should trace to at least one task, and every task should trace back to at least one AC.

**AC → Task Mapping Example:**

```markdown
AC: "User can filter by minimum follower count (10K, 50K, 100K, 500K, 1M)"

Tasks created:
1. Task 2.3: Create FollowerCountFilter value object
2. Task 2.4: Add filtering to GetInfluencers use case
3. Task 3.5: Implement filter in repository query
4. Task 4.3: Add filter UI component
```

### From AC to Test

The I/O/Test structure maps directly to TDD:

| I/O/Test | TDD Phase |
|----------|-----------|
| Input | Arrange |
| Output | Expected result |
| Test | Assert |

**Example:**

AC:
```markdown
- [ ] User can filter by minimum follower count (10K, 50K, 100K, 500K, 1M)
```

Test:
```python
def test_filter_by_minimum_followers_10k():
    # Arrange (Input)
    influencers = [/* mix of follower counts */]
    filter_config = FilterConfig(min_followers=10_000)

    # Act
    result = filter_influencers(influencers, filter_config)

    # Assert (Output)
    assert all(i.followers >= 10_000 for i in result)
```

## Integration with superpowers:writing-plans

### What This Skill Produces

| Output | Detail |
|--------|--------|
| Tasks with I/O/Test | Clear contracts |
| Estimated file paths | `domain/entities/foo.py` |
| Test strategy | Unit, integration categories |
| Commit messages | Conventional format |

### What writing-plans Adds

| Input | Output |
|-------|--------|
| Tasks with I/O/Test | TDD steps |
| Estimated file paths | Exact paths with line numbers |
| Test strategy | Complete test code |
| Commit messages | Commit commands with full message |

### Handoff Example

This skill produces:
```markdown
### Task 1.1: Create Influencer entity

**Files (estimated):**
- `domain/entities/influencer.py` — Create

**Test Strategy:**
- Unit: validation rules, required fields
```

writing-plans produces:
```markdown
### Task 1.1: Create Influencer entity

**Files:**
- Create: `domain/entities/influencer.py`
- Test: `tests/domain/entities/test_influencer.py`

**Step 1: Write the failing test**
```python
def test_influencer_requires_platform_id():
    with pytest.raises(ValueError, match="platform_id required"):
        Influencer(platform_id=None, ...)
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/domain/entities/test_influencer.py::test_influencer_requires_platform_id -v`
Expected: FAIL with "NameError: name 'Influencer' is not defined"
...
```
