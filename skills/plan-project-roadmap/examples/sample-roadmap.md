# Project Roadmap

> **For Claude:** Use `/plan-phase-tasks` to decompose each phase into executable tasks.

**Project:** Boom Influencer Database
**Goal:** Build an influencer database system so Boom can immediately match influencers to brand requests
**Total Phases:** 5
**Methodology:** Clean Architecture + Vertical Slices + FDD

---

## Phase Overview

| Phase | Stories | Focus | Dependencies |
|-------|---------|-------|--------------|
| 1 | US-001, US-002 | Foundation | None |
| 2 | US-003, US-004 | TikTok Discovery | Phase 1 |
| 3 | US-005, US-006 | Data Enrichment | Phase 2 |
| 4 | US-007, US-008 | Export & Matching | Phase 3 |
| 5 | US-009, US-010 | Web Interface | Phase 4 |

---

## Phase 1: Foundation

**Stories:**
- US-001: Core Influencer Entity (must-have)
- US-002: Database Setup and Seeding (must-have)

**Phase Goal:** Establish core domain model and data persistence layer

**Dependencies:** None (foundation phase)

**Architecture Layers Touched:**
- Domain: Influencer entity, FollowerCount/EngagementRate value objects
- Application: Basic repository interface
- Infrastructure: SQLite adapter, seed data loader

**Success Criteria:**
- [ ] Influencer entity validates all required fields (platform, handle, followers)
- [ ] Repository saves and retrieves influencers without data loss
- [ ] 50+ seed influencers loaded from CSV
- [ ] All unit tests pass (>90% domain coverage)

**Definition of Done:**
- All tests pass
- Domain layer complete for Influencer
- SQLite repository functional
- Seed data loaded and queryable

**Transition to Phase 2:**
- Phase 1 produces:
  - Influencer entity with validation
  - InfluencerRepository interface
  - SQLiteInfluencerRepository implementation
  - Seeded database with reference data
- Phase 2 requires:
  - Entity to store discovered influencers
  - Repository to persist discoveries
  - Database schema ready for new records
- Handoff: Discovery will create Influencer instances and save via repository

---

## Phase 2: TikTok Discovery

**Stories:**
- US-003: TikTok Hashtag Discovery (must-have)
- US-004: Discovery Configuration (must-have)

**Phase Goal:** Automated discovery of influencers from TikTok based on hashtags

**Dependencies:** Phase 1 (Influencer entity, Repository)

**Architecture Layers Touched:**
- Domain: DiscoveryConfig, DiscoveryResult value objects
- Application: DiscoverInfluencers use case
- Infrastructure: TikTokDiscoveryAdapter

**Success Criteria:**
- [ ] Discovery returns 100+ influencers per hashtag query
- [ ] Results include required metrics (followers, engagement)
- [ ] Discovered influencers persist to database
- [ ] Discovery is configurable (hashtags, min followers)
- [ ] Handles API rate limits gracefully

**Definition of Done:**
- TikTok adapter functional
- Use case orchestrates full flow
- Integration tests with recorded API responses
- Can run discovery unattended

**Transition to Phase 3:**
- Phase 2 produces:
  - Populated database with TikTok influencers
  - Discovery configuration patterns
  - Working API integration
- Phase 3 requires:
  - Influencers to enrich
  - Established patterns for API integration
- Handoff: Enrichment will read discovered influencers and add contact info

---

## Phase 3: Data Enrichment

**Stories:**
- US-005: Contact Information Extraction (should-have)
- US-006: Social Link Discovery (should-have)

**Phase Goal:** Enrich influencer profiles with contact information and cross-platform links

**Dependencies:** Phase 2 (discovered influencers to enrich)

**Architecture Layers Touched:**
- Domain: ContactInfo, SocialLinks value objects
- Application: EnrichInfluencer use case
- Infrastructure: ContactExtractor, SocialLinkResolver adapters

**Success Criteria:**
- [ ] Extract email from 60%+ of profiles
- [ ] Find Instagram/YouTube links for 40%+ of TikTok influencers
- [ ] Enrichment is idempotent (safe to re-run)
- [ ] Handles missing data gracefully

**Definition of Done:**
- Contact extraction working
- Social link resolution working
- Enrichment use case orchestrates both
- Can enrich batch of influencers

**Transition to Phase 4:**
- Phase 3 produces:
  - Enriched influencer profiles
  - Contact info where available
  - Cross-platform links
- Phase 4 requires:
  - Complete influencer data for export
  - Searchable profiles for matching
- Handoff: Export and matching use complete influencer profiles

---

## Phase 4: Export & Matching

**Stories:**
- US-007: CSV/Excel Export (should-have)
- US-008: Basic Influencer Matching (should-have)

**Phase Goal:** Enable export of influencer data and basic matching to brand requirements

**Dependencies:** Phase 3 (enriched influencer data)

**Architecture Layers Touched:**
- Domain: ExportConfig, MatchCriteria value objects
- Application: ExportInfluencers, MatchInfluencers use cases
- Infrastructure: CSVExporter, ExcelExporter adapters

**Success Criteria:**
- [ ] Export to CSV with all fields
- [ ] Export to Excel with formatting
- [ ] Match by niche, follower range, engagement minimum
- [ ] Match returns ranked results

**Definition of Done:**
- Export adapters functional
- Matching algorithm implemented
- CLI commands for both operations
- Integration tests pass

**Transition to Phase 5:**
- Phase 4 produces:
  - Working export functionality
  - Basic matching capability
  - CLI interface for operations
- Phase 5 requires:
  - All core functionality complete
  - Stable API for UI to consume
- Handoff: UI wraps existing use cases with web interface

---

## Phase 5: Web Interface (Final)

**Stories:**
- US-009: Influencer Browse & Filter UI (nice-to-have)
- US-010: Export & Match UI (nice-to-have)

**Phase Goal:** Web interface for browsing, filtering, and exporting influencers

**Dependencies:** Phase 4 (all core functionality)

**Architecture Layers Touched:**
- UI: React components, pages
- Application: API handlers (if needed)

**Success Criteria:**
- [ ] Browse influencers with pagination
- [ ] Filter by niche, followers, engagement
- [ ] Trigger export from UI
- [ ] Run match query from UI
- [ ] View match results

**Definition of Done:**
- UI components complete
- All pages functional
- E2E tests pass
- Can complete full workflow in browser

**Completion Criteria:**
- All must-have stories complete (US-001 through US-004)
- All should-have stories complete (US-005 through US-008)
- Nice-to-have stories complete (US-009, US-010)
- End-to-end user workflow functional
- System ready for production use
