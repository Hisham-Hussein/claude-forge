# Task Decomposition: FDD-Style Atomic Tasks

<overview>
Every task must have explicit Input/Output/Test. This structure minimizes AI coding errors by:
- Making requirements unambiguous
- Providing clear success criteria
- Enabling atomic commits
- Supporting TDD workflow
</overview>

<task_template>
## Task Template

```markdown
### Task X.Y: [Verb] [Object]

**Layer:** Domain | Application | Infrastructure | UI

**Input:**
- [What this task needs to start]
- [Prerequisites, dependencies, contracts]

**Output:**
- [File(s) created or modified]
- [Artifact(s) produced]

**Test:**
- [How to verify correctness]
- [Test type: unit | integration | e2e]

**Commit:** `feat|fix|refactor(scope): message`
```
</task_template>

<decomposition_by_layer>
## Decomposition by Clean Architecture Layer

### Domain Layer Tasks

**Entities:**
```markdown
### Task 1.1: Create Influencer entity

**Layer:** Domain
**Input:** Business rules from USER-STORIES.md (US-001 AC)
**Output:** domain/entities/Influencer.ts
**Test:** Unit test - validation rules, required fields
**Commit:** `feat(domain): add Influencer entity`
```

**Value Objects:**
```markdown
### Task 1.2: Create FollowerCount value object

**Layer:** Domain
**Input:** Business constraints (min: 10K, max: 100M)
**Output:** domain/value-objects/FollowerCount.ts
**Test:** Unit test - validation, immutability
**Commit:** `feat(domain): add FollowerCount value object`
```

**Domain Services:**
```markdown
### Task 1.3: Create EngagementCalculator service

**Layer:** Domain
**Input:** Engagement formula from business case
**Output:** domain/services/EngagementCalculator.ts
**Test:** Unit test - calculation accuracy
**Commit:** `feat(domain): add EngagementCalculator service`
```

**Repository Interfaces:**
```markdown
### Task 1.4: Define InfluencerRepository interface

**Layer:** Domain
**Input:** Use case requirements
**Output:** domain/repositories/InfluencerRepository.ts
**Test:** N/A (interface only)
**Commit:** `feat(domain): define InfluencerRepository interface`
```

### Application Layer Tasks

**Use Cases:**
```markdown
### Task 2.1: Create DiscoverInfluencers use case

**Layer:** Application
**Input:** InfluencerRepository interface, DiscoveryConfig
**Output:** application/discovery/DiscoverInfluencers.ts
**Test:** Unit test with mocked repository
**Commit:** `feat(app): add DiscoverInfluencers use case`
```

### Infrastructure Layer Tasks

**Repository Implementations:**
```markdown
### Task 3.1: Implement ConvexInfluencerRepository

**Layer:** Infrastructure
**Input:** InfluencerRepository interface, Convex schema
**Output:** adapters/storage/ConvexInfluencerRepository.ts
**Test:** Integration test against Convex
**Commit:** `feat(adapters): implement ConvexInfluencerRepository`
```

**External Adapters:**
```markdown
### Task 3.2: Implement TikTokDiscoveryAdapter

**Layer:** Infrastructure
**Input:** DiscoveryAdapter interface, TikTok API docs
**Output:** adapters/platforms/TikTokDiscoveryAdapter.ts
**Test:** Integration test with API mocks
**Commit:** `feat(adapters): implement TikTokDiscoveryAdapter`
```

### UI Layer Tasks

**Components:**
```markdown
### Task 4.1: Create InfluencerCard component

**Layer:** UI
**Input:** Design specs, Influencer entity
**Output:** ui/components/InfluencerCard.tsx
**Test:** Component test - renders correctly
**Commit:** `feat(ui): add InfluencerCard component`
```

**Pages:**
```markdown
### Task 4.2: Create InfluencerListPage

**Layer:** UI
**Input:** InfluencerCard, GetInfluencers use case
**Output:** ui/pages/InfluencerListPage.tsx
**Test:** E2E test - loads and displays influencers
**Commit:** `feat(ui): add InfluencerListPage`
```
</decomposition_by_layer>

<sizing_guidance>
## Task Sizing Guidance

**Right-sized task:**
- Completable in one focused session
- Single-file change (ideal)
- Clear start and end
- Testable in isolation

**Too large - split it:**
- Multiple unrelated changes
- Multiple files in different layers
- "And then also..." in description
- No clear stopping point

**Too small - combine:**
- Trivial one-liner
- Only makes sense with another task
- No meaningful test possible
</sizing_guidance>

<commit_conventions>
## Commit Conventions

**Format:** `type(scope): message`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructure
- `test`: Test addition/modification
- `docs`: Documentation
- `chore`: Maintenance

**Scopes:**
- `domain`: Domain layer
- `app`: Application layer
- `adapters`: Infrastructure layer
- `ui`: UI layer
- `config`: Configuration

**Examples:**
```
feat(domain): add Influencer entity with validation
feat(app): add DiscoverInfluencers use case
feat(adapters): implement TikTokDiscoveryAdapter
feat(ui): add InfluencerCard component
fix(domain): correct engagement rate calculation
test(app): add unit tests for DiscoverInfluencers
```
</commit_conventions>

<from_ac_to_test>
## From Acceptance Criteria to Tests

**Every AC becomes at least one test.**

AC in User Story:
```markdown
- [ ] User can filter by minimum follower count (10K, 50K, 100K, 500K, 1M)
```

Becomes test:
```typescript
describe('InfluencerFilter', () => {
  it('should filter by minimum follower count 10K', () => {
    // Arrange
    const influencers = [/* mix of follower counts */];
    const filter = { minFollowers: 10_000 };

    // Act
    const result = filterInfluencers(influencers, filter);

    // Assert
    expect(result.every(i => i.followers >= 10_000)).toBe(true);
  });

  // Repeat for 50K, 100K, 500K, 1M thresholds
});
```

**The Input/Output/Test structure maps directly to TDD:**
- Input → Arrange
- Output → Expected result
- Test → Assert
</from_ac_to_test>
