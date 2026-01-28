# Phase 1 Plan: Foundation

> **For Claude:** Use `superpowers:writing-plans` to create TDD implementation plans for each story's tasks.

**Phase:** 1 of 5
**Goal:** Establish core domain model and data persistence layer
**Stories:** US-001, US-002
**Prerequisites:** None (foundation phase)

---

## Story: US-001 — Core Influencer Entity

**Priority:** must-have

### Acceptance Criteria

- AC1: Influencer has required fields: platform, platform_id, handle, display_name
- AC2: Influencer has metrics: followers, following, likes, engagement_rate
- AC3: Follower count validated (minimum 10,000)
- AC4: Engagement rate calculated correctly (likes+comments / followers)
- AC5: Influencer can be serialized to/from JSON

### Tasks

#### Task 1.1: Create FollowerCount value object

**Type:** Create
**Layer:** Domain

**Input:**
- Business constraint: minimum 10,000 followers
- Immutability requirement

**Output:**
- FollowerCount value object with validation
- Comparison methods (gt, lt, eq)

**Files (estimated):**
- `domain/value_objects/follower_count.py` — Create

**Test Strategy:**
- Unit: validation rejects < 10K, accepts >= 10K
- Unit: immutability (cannot change after creation)
- Unit: comparison operators work correctly

**Architecture Alignment:**
- Pattern: Value Object
- Dependencies: None
- Dependents: Influencer entity

**Commit:** `feat(domain): add FollowerCount value object`

---

#### Task 1.2: Create EngagementRate value object

**Type:** Create
**Layer:** Domain

**Input:**
- Calculation formula: (likes + comments) / followers
- Range constraint: 0.0 to 1.0 (0% to 100%)

**Output:**
- EngagementRate value object with validation
- Factory method from metrics

**Files (estimated):**
- `domain/value_objects/engagement_rate.py` — Create

**Test Strategy:**
- Unit: validates range 0.0-1.0
- Unit: calculates correctly from metrics
- Unit: handles edge case (zero followers)

**Architecture Alignment:**
- Pattern: Value Object
- Dependencies: None
- Dependents: Influencer entity

**Commit:** `feat(domain): add EngagementRate value object`

---

#### Task 1.3: Create Platform enum

**Type:** Create
**Layer:** Domain

**Input:**
- Supported platforms: TikTok, Instagram, YouTube, Snapchat

**Output:**
- Platform enum with string values
- Validation helper

**Files (estimated):**
- `domain/value_objects/platform.py` — Create

**Test Strategy:**
- Unit: all platforms have correct values
- Unit: from_string conversion works

**Architecture Alignment:**
- Pattern: Value Object (Enum)
- Dependencies: None
- Dependents: Influencer entity

**Commit:** `feat(domain): add Platform enum`

---

#### Task 1.4: Create Influencer entity

**Type:** Create
**Layer:** Domain

**Input:**
- FollowerCount value object (Task 1.1)
- EngagementRate value object (Task 1.2)
- Platform enum (Task 1.3)
- Required fields from AC1, AC2

**Output:**
- Influencer entity with all fields
- Validation on construction
- JSON serialization

**Files (estimated):**
- `domain/entities/influencer.py` — Create

**Test Strategy:**
- Unit: requires all mandatory fields
- Unit: validates follower count via value object
- Unit: serializes to/from JSON correctly
- Unit: equality based on platform + platform_id

**Architecture Alignment:**
- Pattern: Entity
- Dependencies: FollowerCount, EngagementRate, Platform
- Dependents: Repository interface, use cases

**Commit:** `feat(domain): add Influencer entity`

---

#### Task 1.5: Define InfluencerRepository interface

**Type:** Create
**Layer:** Domain

**Input:**
- CRUD operations needed
- Query patterns (by platform, by handle)

**Output:**
- Abstract InfluencerRepository interface
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

---

## Story: US-002 — Database Setup and Seeding

**Priority:** must-have

### Acceptance Criteria

- AC1: SQLite database created with influencer table
- AC2: Repository implementation saves influencers
- AC3: Repository implementation retrieves by ID
- AC4: Repository implementation queries by platform
- AC5: 50+ seed influencers loaded from CSV

### Tasks

#### Task 2.1: Create database schema

**Type:** Infrastructure
**Layer:** Infrastructure

**Input:**
- Influencer entity fields
- SQLite best practices

**Output:**
- Schema definition
- Migration/setup script

**Files (estimated):**
- `adapters/storage/schema.sql` — Create
- `adapters/storage/migrations/001_initial.py` — Create

**Test Strategy:**
- Integration: schema creates successfully
- Integration: all columns have correct types

**Architecture Alignment:**
- Pattern: Infrastructure Setup
- Dependencies: Influencer entity (for field mapping)
- Dependents: Repository implementation

**Commit:** `feat(adapters): add SQLite schema for influencers`

---

#### Task 2.2: Implement SQLiteInfluencerRepository

**Type:** Create
**Layer:** Infrastructure

**Input:**
- InfluencerRepository interface (Task 1.5)
- Database schema (Task 2.1)
- SQLite connection configuration

**Output:**
- Working repository implementation
- CRUD operations against SQLite

**Files (estimated):**
- `adapters/storage/sqlite_influencer_repository.py` — Create

**Test Strategy:**
- Integration: save and retrieve roundtrip
- Integration: find_by_id returns correct entity
- Integration: find_by_platform filters correctly
- Integration: handles not found gracefully

**Architecture Alignment:**
- Pattern: Repository Implementation
- Dependencies: InfluencerRepository interface, schema
- Dependents: Use cases, seeding

**Commit:** `feat(adapters): implement SQLiteInfluencerRepository`

---

#### Task 2.3: Create seed data CSV

**Type:** Infrastructure
**Layer:** Infrastructure

**Input:**
- Sample influencer data
- At least 50 records
- Mix of platforms

**Output:**
- CSV file with seed data
- Variety of niches, follower counts

**Files (estimated):**
- `data/seed_influencers.csv` — Create

**Test Strategy:**
- Manual: CSV is valid and parseable
- Manual: contains 50+ records

**Architecture Alignment:**
- Pattern: Test Data
- Dependencies: None
- Dependents: Seed loader

**Commit:** `chore(data): add seed influencer CSV`

---

#### Task 2.4: Create seed loader script

**Type:** Create
**Layer:** Infrastructure

**Input:**
- Seed CSV (Task 2.3)
- SQLiteInfluencerRepository (Task 2.2)

**Output:**
- Script that loads CSV into database
- Idempotent (safe to re-run)

**Files (estimated):**
- `execution/seed_database.py` — Create

**Test Strategy:**
- Integration: loads all records
- Integration: re-running doesn't duplicate
- Integration: validates data during load

**Architecture Alignment:**
- Pattern: Setup Script
- Dependencies: Repository, seed CSV
- Dependents: Development environment setup

**Commit:** `feat(execution): add database seeding script`

---

## Phase Verification

### Pre-Implementation Checks
- [x] All tasks have explicit I/O/Test
- [x] Tasks ordered by dependency
- [x] Architecture layers respected
- [x] Acceptance criteria mapped to tasks

### Post-Implementation Checks
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] 50+ influencers seeded
- [ ] Can query by platform
- [ ] Can retrieve by ID

### Handoff to Next Phase
- **Produces:**
  - Influencer entity with validation
  - InfluencerRepository interface
  - SQLiteInfluencerRepository implementation
  - Seeded database with 50+ records
- **Enables:**
  - Phase 2 can store discovered influencers
  - Phase 2 can query existing records
  - Phase 2 has patterns to follow
