---
name: create-requirements
description: Transform BUSINESS-CASE.md into formal software requirements (SRS or User Stories). Use when user has completed /create-business-case and needs requirements documentation. Optionally accepts STORY-MAP.md from /create-story-map for journey-organized user stories with SM-XXX traceability.
---

<objective>
**Requirements Engineer Skill**

Transform business case documents into formal, traceable software requirements specifications.

**Inputs:**
- `.charter/BUSINESS-CASE.md` (required — 9-section format from `/create-business-case`)
- `.charter/STORY-MAP.md` (optional — from `/create-story-map`)

**Outputs:**
- `.charter/REQUIREMENTS.md` (SRS format) — formal functional/non-functional requirements
- `.charter/USER-STORIES.md` (Agile format) — Epic/Feature/Story hierarchy with acceptance criteria

**Methodology:** BABOK v3 + ISO/IEC 25010:2023 + INVEST criteria + MoSCoW prioritization

**Two modes:**
- **Business Case only:** Derives Epic/Feature/Story hierarchy from BR-XX groupings
- **Story Map + Business Case:** Inherits hierarchy from story map (Activity→Epic, Task→Feature, SM-XXX→US-XXX parent), each SM-XXX produces one or more US-XXX

**Core principle:** Skill 1 already extracted stakeholders, constraints, and business requirements. This skill TRANSFORMS business requirements (BR-XX) into software requirements — it doesn't re-extract.
</objective>

<quick_start>
**Usage:**
```
/create-requirements .charter/BUSINESS-CASE.md
/create-requirements .charter/BUSINESS-CASE.md assets/CLIENT-BRIEF.md
/create-requirements .charter/BUSINESS-CASE.md assets/CLIENT-BRIEF.md artifacts/research/api-specs.md
/create-requirements .charter/BUSINESS-CASE.md .charter/STORY-MAP.md
```

**What happens:**
1. Parses the 9-section BUSINESS-CASE.md format
2. Detects STORY-MAP.md if provided (enables story-map mode)
3. Loads reference documents (from Section 9.6 AND/OR command arguments) for detailed specifications
4. Extracts BR-XX requirements from Section 9 (BRD)
5. Asks: "SRS format, User Stories, or both?" (story-map mode defaults to User Stories)
6. Transforms BR-XX into software requirements with traceability
7. If story-map mode: inherits Activity→Epic, Task→Feature, SM-XXX→US-XXX hierarchy
8. Writes output to `.charter/`

**Output location:** `.charter/REQUIREMENTS.md` and/or `.charter/USER-STORIES.md`
</quick_start>

<essential_principles>

**This Skill Consumes Skill 1's Output:**

Skill 1 (`/create-business-case`) produces a 9-section BUSINESS-CASE.md:
```
Section 1: Executive Summary
Section 2: Problem Statement
Section 3: Proposed Solution
Section 4: Stakeholders         ← ALREADY EXTRACTED (reuse directly)
Section 5: Value Proposition
Section 6: Success Criteria
Section 7: Constraints          ← ALREADY EXTRACTED (reuse directly)
Section 8: Risks
Section 9: Business Requirements (BRD)  ← BR-XX IDs to transform
```

**DO NOT re-extract** stakeholders or constraints. Pull them directly from the document.

**Transformation, Not Extraction:**

| Skill 1 Output | This Skill's Job |
|----------------|------------------|
| BR-XX business requirements | Transform into FR-XX functional requirements OR User Stories |
| Stakeholders (Section 4) | Map to actors in Use Cases and "As a [role]" in stories |
| Constraints (Section 7) | Transform into NFR-XX non-functional requirements |
| Success Criteria (Section 6) | Derive acceptance criteria |

**Traceability is Mandatory:**

Every output requirement MUST link back to its source BR-XX:
```
FR-DISC-01: System shall discover influencers by hashtag search
  Source: BR-02 (BUSINESS-CASE.md, Section 9.3)
```

**Quality Attributes (BABOK):**
- **Atomic** — One requirement per statement
- **Testable** — Can be verified when implemented
- **Traceable** — Links to BR-XX source
- **Prioritized** — Has MoSCoW category

</essential_principles>

<reference_index>
**Domain Knowledge (read as needed):**

| Reference | When to Read | Content |
|-----------|--------------|---------|
| `references/srs-methodology.md` | Phase 3 (SRS output) | BABOK, ISO 25010, requirement classification, traceability patterns |
| `references/user-story-methodology.md` | Phase 4 (User Stories output) | INVEST criteria, Epic/Feature/Story hierarchy, vertical slicing, anti-patterns |
| `references/acceptance-criteria-methodology.md` | Phase 4 (writing AC) | Ten Questions, 6 Categories Framework, SMART/3C validation, edge case identification |

**Output Templates:**

| Template | When to Read | Content |
|----------|--------------|---------|
| `templates/srs-template.md` | Phase 7a | Full SRS document structure with placeholders |
| `templates/user-stories-template.md` | Phase 7b | User Stories backlog structure with placeholders |

**Loading pattern:** Read references BEFORE corresponding phases. Read templates WHEN generating output files.

**Loading sequence for Phase 4 (User Stories):**
1. **First:** Read `references/user-story-methodology.md` — understand story structure, INVEST criteria, Epic/Feature/Story hierarchy, and vertical slicing principles
2. **Second:** Read `references/acceptance-criteria-methodology.md` — learn how to write AC for those stories (assumes story context from step 1)

This sequence matters because acceptance criteria methodology references story components and assumes you understand what makes a good story.
</reference_index>

<intake>

**Arguments:**
- First argument (required): Path to BUSINESS-CASE.md
- Additional arguments (optional): STORY-MAP.md and/or reference documents

**Examples:**
```
/create-requirements .charter/BUSINESS-CASE.md
/create-requirements .charter/BUSINESS-CASE.md assets/CLIENT-BRIEF.md
/create-requirements .charter/BUSINESS-CASE.md .charter/STORY-MAP.md
/create-requirements .charter/BUSINESS-CASE.md .charter/STORY-MAP.md assets/CLIENT-BRIEF.md
```

**Parsing:**
1. Split `$ARGUMENTS` by spaces
2. First path = business case document
3. For remaining paths: detect STORY-MAP.md by checking for `SM-` IDs or `## Detailed Map` heading. If detected, store as story map document. All other remaining paths = explicit reference documents (store for Phase 1b).
4. If no arguments provided, check if `.charter/BUSINESS-CASE.md` exists. Also check if `.charter/STORY-MAP.md` exists — if so, ask user whether to use it.

**Mode detection:**
- If story map detected → **story-map mode** (hierarchy inherited from map)
- If no story map → **business-case mode** (hierarchy derived from BR-XX groupings)

**Validation:**
1. Read the business case document
2. Verify it has the 9-section structure (look for "## 9. Business Requirements")
3. If not a BUSINESS-CASE.md format, warn: "This document doesn't match Skill 1's output format. Run `/create-business-case` first, or confirm you want generic extraction."
4. If story map provided, verify it has SM-XXX IDs and Activity/Task structure

**After validation, ask output format:**

Use AskUserQuestion:
```
"What output format do you need?"
Options:
- User Stories only (Recommended when story map provided)  [default in story-map mode]
- SRS only (formal requirements specification)
- Both SRS and User Stories
```

In story-map mode, pre-select "User Stories only" as the recommended option since the story map's structure maps naturally to Agile hierarchy. SRS is still available if explicitly requested.

Proceed to Phase 1 with the user's choice.

</intake>

<phase_1_parse_business_case>
**Phase 1: Parse BUSINESS-CASE.md**

Extract structured data from each section:

**1.1 From Section 4 (Stakeholders)**
Parse the stakeholder table directly:
- Role, Type, Power/Interest, Needs, Engagement level
- These become actors for Use Cases and roles for User Stories

**1.2 From Section 7 (Constraints)**
Extract constraint categories:
- Timeline constraints → Schedule NFRs
- Budget constraints → Cost NFRs
- Technical constraints → Technology NFRs
- Team constraints → Capacity considerations
- Regulatory constraints → Compliance NFRs

**1.3 From Section 9.2 (Scope)**
Extract:
- In Scope items → Will generate requirements
- Out of Scope items → Document as "Won't Have" with rationale

**1.4 From Section 9.3 (Business Requirements Table)**
Parse the BR-XX table:
- ID (BR-01, BR-02, ...)
- Requirement text
- Priority (Must/Should/Could)
- Acceptance Criteria

**1.5 From Section 6 (Success Criteria)**
Extract KPIs and targets — these inform acceptance criteria for derived requirements.

**1.6 Present Parsing Summary**

```
## Business Case Parsing Summary

**Stakeholders found:** [count] ([list roles])
**Constraints identified:** [count] (Timeline: X, Budget: X, Technical: X, ...)
**Business Requirements (BR-XX):** [count] (Must: X, Should: X, Could: X)
**In-Scope items:** [count]
**Out-of-Scope items:** [count]

Ready to transform into [SRS / User Stories / Both].
```

Proceed to Phase 1b.
</phase_1_parse_business_case>

<phase_1b_reference_documents>
**Phase 1b: Load Reference Documents**

Collect references from two sources:

**1. From Section 9.6 (automatic):**
If Section 9.6 (Reference Documents) exists in the business case, collect all document paths listed in the reference table.

**2. From command arguments (explicit):**
If reference documents were passed as arguments in the intake phase, add them to the collection.

**3. Merge and deduplicate:**
Combine both sources. If the same document appears in both, load it only once.

**4. Load all collected references:**
For each reference document:
- Read the document
- Extract detailed specifications (data types, validation rules, thresholds, enumerations)

**5. Use these details throughout the transformation process:**
- Field specifications → Functional requirements
- Validation rules → Acceptance criteria
- Integration dependencies → Non-functional requirements
- Enumerations → Requirement precision

**Example:** BR-04 says "classify into size buckets" → Reference doc specifies exact thresholds (Nano=1K-10K, Micro=10K-100K, etc.) → Both the functional requirement AND acceptance criteria should include these thresholds.

**If no references from either source:** Proceed without additional context. Output may lack implementation-level precision.

Proceed to Phase 1c (if story map provided) or Phase 2.
</phase_1b_reference_documents>

<phase_1c_parse_story_map>
**Phase 1c: Parse Story Map (story-map mode only)**

Skip this phase entirely if no STORY-MAP.md was provided.

**1c.1 Extract Structure**

Parse the story map's hierarchical organization:
- **Activities** (top-level journey steps) → will become Epics in Phase 4
- **Tasks** (under each Activity) → will become Features in Phase 4
- **Stories** (SM-XXX IDs under each Task) → will become US-XXX parents in Phase 4

**1c.2 Extract SM-XXX Registry**

Build a registry of all story map stories. Use the Traceability table as the primary source (each row maps SM-XXX to Title, BR-XX, and Release):

For each SM-XXX entry, capture:
- SM-XXX ID
- Title
- Parent Activity and Task — locate the SM-XXX in the `## Detailed Map` section; it sits under an `#### Task` heading, whose parent `### Activity` heading is the Activity. The Traceability table does not contain Activity/Task columns, so this must come from the heading structure.
- Release assignment (from Traceability table's Release column)
- Source BR-XX reference(s) (from Traceability table's BR-XX column)

Preserve SM-XXX IDs exactly as they appear in the story map. Do not renumber or reformat them.

**1c.4 Cross-Reference with Business Case**

Verify that BR-XX references in the story map exist in the business case's Section 9.3. Flag any mismatches:
- SM-XXX references a BR-XX not in the business case → warn
- BR-XX in business case has no SM-XXX coverage → note as gap (may be intentional deferral)

**1c.5 Present Story Map Parsing Summary**

```
## Story Map Parsing Summary

**Activities found:** [count] ([list names])
**Tasks found:** [count]
**Stories (SM-XXX):** [count] ([for each release label found: label: count])
**BR-XX coverage:** [X]/[Y] business requirements mapped to SM-XXX stories
**Gaps:** [list any BR-XX without SM-XXX coverage]

Story map hierarchy will be used for Epic/Feature/Story structure.
```

Proceed to Phase 2.
</phase_1c_parse_story_map>

<phase_2_clarification>
**Phase 2: Targeted Clarification**

Only ask questions that the BUSINESS-CASE.md doesn't answer. Skip questions if the document is comprehensive.

**2.1 NFR Questions (only if not in Section 7)**

| Characteristic | Question | When to Ask |
|----------------|----------|-------------|
| Performance | "Any response time targets?" | If not in constraints |
| Reliability | "Availability expectations?" | If not in constraints |
| Security | "Security requirements beyond standard?" | If not in constraints |
| Scalability | "Expected data volume growth?" | If not in constraints |

**2.2 Prioritization Validation**

"The BRD lists [X] Must-haves. The 60% rule suggests Must-haves should be ≤60% of scope. Would you like to review priorities?"

Only ask if Must-haves exceed 60%.

**2.3 User Story Specifics (if User Stories selected)**

Skip in story-map mode — hierarchy is inherited from the story map.

"For User Story output, should I:"
- Group by Epic (feature area) — Recommended
- Group by Actor (user role)
- Flat list (no hierarchy)

Proceed to Phase 3.
</phase_2_clarification>

<phase_3_transform_requirements>
**Phase 3: Transform BR-XX to Software Requirements**

**3.1 Functional Requirements (FR-XX)**

For each BR-XX, derive one or more functional requirements:

**Transformation pattern:**
```
BR-XX: "The business needs [capability] so that [benefit]"
    ↓
FR-[DOMAIN]-XX: "The system shall [specific behavior] [constraint]"
```

**Domain prefixes** (derive from the business case domain):
| Domain Area | Prefix | Example |
|-------------|--------|---------|
| Discovery | DISC | FR-DISC-01 |
| Enrichment | ENRICH | FR-ENRICH-01 |
| Classification | CLASS | FR-CLASS-01 |
| Search/Filter | SEARCH | FR-SEARCH-01 |
| Outreach | OUT | FR-OUT-01 |
| Status/Tracking | TRACK | FR-TRACK-01 |
| Data Management | DATA | FR-DATA-01 |
| User Interface | UI | FR-UI-01 |
| Export/Import | IO | FR-IO-01 |
| Authentication | AUTH | FR-AUTH-01 |

**One BR may spawn multiple FRs:**
```
BR-06: "searchable interface for niche, country, platform, size"
    ↓
FR-SEARCH-01: System shall filter influencers by niche
FR-SEARCH-02: System shall filter influencers by country
FR-SEARCH-03: System shall filter influencers by platform
FR-SEARCH-04: System shall filter influencers by follower size bucket
FR-SEARCH-05: System shall support combined filters (AND logic)
```

**Data-model-driven derivation (beyond BR text):**
```
BR-06: "searchable interface for niche, country, platform, size"
    -> (from BR text)
FR-SEARCH-01 through FR-SEARCH-05 (as above)
    -> (from data model cross-reference)
FR-SEARCH-06: System shall filter by city (data model has City as Enum with predefined values)
FR-SEARCH-07: System shall filter by status (data model has Status as Enum with 7 values)
FR-SEARCH-08: System shall filter by gender (data model has Gender as Enum; brand matching needs)
```

**Rule:** When a BR mentions "search and filter," and reference documents
include a data model, check it for ALL discrete/enumerable fields — each
is a potential filter candidate. If no data model exists, decompose only
the filter dimensions named in the BR text.

**3.2 Non-Functional Requirements (NFR-XX)**

Transform constraints into ISO 25010 categories:

| Constraint Type | ISO 25010 Category | NFR Prefix |
|-----------------|-------------------|------------|
| "within X seconds" | Performance Efficiency | NFR-PERF |
| "available 24/7" | Reliability | NFR-REL |
| "secure storage" | Security | NFR-SEC |
| "handle N records" | Flexibility (Scalability) | NFR-FLEX |
| "easy to use" | Interaction Capability | NFR-INT |
| "must integrate with" | Compatibility | NFR-COMPAT |
| "testable/maintainable" | Maintainability | NFR-MAINT |

**3.3 Transition Requirements (TRANS-XX)**

Derive from:
- Data migration needs mentioned in the business case
- Integration with existing systems (e.g., Respond.io)
- Training or adoption requirements

**3.4 Traceability**

Every derived requirement MUST include:
```
Source: BR-XX (BUSINESS-CASE.md, Section 9.3)
```

</phase_3_transform_requirements>

<phase_3_5_reference_verification>
**Phase 3.5: Reference Document Verification**

After transforming all BR-XX into FR/NFR requirements, verify completeness
against reference documents loaded in Phase 1b.

**3.5.1 Data Model Field Verification**

If the reference documents contain a data model or field specification:

For EACH field in the source data model:
1. Is there an FR that covers storing/collecting this field? If not, add one.
2. Does the FR's acceptance criteria include the field's data type? If not, add it.
3. Does the FR's acceptance criteria include the field's validation rules? If not, add them.
4. Does the FR's acceptance criteria include enumerated values (if applicable)? If not, add them.
5. Is the field's data source (Profile/Enrichment/Derived/Outreach/System) consistent with the FR's domain area? If not, flag.

**3.5.2 Filterable Field Verification**

If a search/filter BR exists:

For EACH field with a discrete/enumerable data type (Enum, Boolean, predefined list):
1. Would users naturally want to filter by this field?
2. If yes, is there an FR-SEARCH requirement for this filter?
3. If not, add one with appropriate priority (Must if the field is core to brand matching, Should otherwise).

**3.5.3 Present Verification Results**

```
## Reference Document Verification

**Data model fields:** [X]/[Y] covered by FRs
**Gaps found:** [list any uncovered fields]
**Additional filters identified:** [list any new filter FRs added]
**Validation rules transferred:** [count]
```

Proceed to Phase 3.6.
</phase_3_5_reference_verification>

<phase_3_6_implicit_requirements>
**Phase 3.6: Implicit Requirements**

After transforming all explicit BR-XX items, identify requirements implied by
system behavior but not stated in any BR:

**Check 1: Data Integrity**
- Does the system collect data in multiple rounds? -> Derive deduplication requirement
- Does the system collect from multiple sources? -> Derive conflict resolution requirement
- Does the system allow concurrent edits? -> Derive concurrency control requirement

**Check 2: Operational Ordering**
- Do source documents specify priority/ordering among items? -> Derive ordering requirement
- Is there a natural sequence for processing steps? -> Derive sequencing requirement

**Check 3: Stakeholder Workflows**
- For each stakeholder in Section 4: does at least one FR address their stated Needs?
- If a stakeholder has a need (e.g., "Quality assurance interface, spot-check workflows") but no FR covers it, derive one.

**Check 4: System-Managed Fields** (if reference documents include a data model)
- For each field marked as "System" source: is there an FR that specifies when/how the system populates it?
- Common system fields: auto-generated IDs, timestamps, derived calculations, default values.
- If no data model exists, check whether the BRs imply auto-generated fields (IDs, timestamps) and derive FRs for those.

Mark implicit requirements with source: "Implicit from [triggering requirement/behavior]"

Proceed to Phase 4.
</phase_3_6_implicit_requirements>

<phase_4_transform_user_stories>
**Phase 4: Transform to User Stories (if selected)**

**4.1 Build Epic/Feature/Story Hierarchy**

**Business-case mode (no story map) — derive from BR-XX:**
```
Epic: [Major capability area from BR-XX groupings]
  └── Feature: [Specific capability from single BR-XX]
        └── User Story: [Atomic user interaction]
```

**Story-map mode — inherit from story map structure:**
```
Epic: [Activity name from story map]  (Activity goal + persona)
  └── Feature: [Task name from story map]  (Task under that Activity)
        └── User Story: US-XXX [from SM-XXX]  (one or more US per SM story)
```

Each SM-XXX produces one or more US-XXX stories. When an SM-XXX is too large to pass INVEST (particularly "S" for Small), split into multiple US-XXX stories that each retain `**Parent:** SM-XXX`. Use sequential numbering (US-014, US-015, etc.) — the Parent field provides traceability. The US-XXX inherits:
- **Epic** from the SM-XXX's parent Activity
- **Feature** from the SM-XXX's parent Task
- **Release** from the SM-XXX's release assignment (MVP, R2, etc.)
- **Source BR-XX** from the SM-XXX's traceability (carried from the story map)

**Story-map mode example:**
```
Epic: Influencer Discovery (Activity: "Discover Influencers")
  └── Feature: Platform Discovery (Task: "Search by Hashtag")
        └── US-001: TikTok hashtag discovery  (Parent: SM-001, Source: BR-02)
        └── US-002: TikTok discovery rate limiting  (Parent: SM-001, Source: BR-02)
        └── US-003: Discovery progress tracking  (Parent: SM-002, Source: BR-02)
```

**4.2 Story Format**

**Business-case mode:**
```markdown
#### US-XXX: [Story Title]

**Source:** BR-XX (BUSINESS-CASE.md, Section 9.3)
**Epic:** [Parent epic]
**Feature:** [Parent feature]

As a [role from Section 4 stakeholders],
I want [specific capability derived from BR-XX],
So that [benefit — often from BR-XX or Section 5].

**Acceptance Criteria:**
- [ ] [Criterion derived from BR-XX acceptance criteria or Section 6 KPIs]
- [ ] [Additional testable criterion]
- [ ] [Edge case handling]

**Priority:** [Must/Should/Could] | **Size:** [S/M/L] | **INVEST:** ✓
```

**Story-map mode** — adds Parent and Release fields:
```markdown
#### US-XXX: [Story Title]

**Parent:** SM-XXX (STORY-MAP.md)
**Source:** BR-XX (BUSINESS-CASE.md, Section 9.3)
**Epic:** [Activity name from story map]
**Feature:** [Task name from story map]
**Release:** [exact release label from story map — e.g., MVP, R2, R3, R4]

As a [role from Section 4 stakeholders],
I want [specific capability — elaborated from SM-XXX title using BR-XX detail],
So that [benefit — from BR-XX or Section 5].

**Acceptance Criteria:**
- [ ] [Criterion derived from BR-XX acceptance criteria or Section 6 KPIs]
- [ ] [Additional testable criterion]
- [ ] [Edge case handling]

**Priority:** [Must/Should/Could] | **Size:** [S/M/L] | **INVEST:** ✓
```

> **Format note:** The `**Parent:** SM-XXX` field is machine-parsed by downstream tools (trace-phase-stories.py). It is the primary traceability contract — the Traceability table at the end of USER-STORIES.md is for human reference only. Both must be present and consistent. Preserve the format exactly — bold markers must wrap `Parent:` including the colon.

**Key difference:** In story-map mode, the story title and capability come from the SM-XXX story in the map, but the full "As a/I want/So that" card and acceptance criteria are ELABORATED here — the story map only had compact IDs and titles, not full specification cards.

**4.3 INVEST Validation**

Before finalizing each story, verify:
- **I**ndependent: Can be developed without other stories
- **N**egotiable: Implementation details not prescribed
- **V**aluable: Delivers clear user benefit
- **E**stimable: Scope is clear enough to estimate
- **S**mall: Completable in one sprint (split if too large)
- **T**estable: Acceptance criteria are verifiable

Flag stories that fail INVEST and suggest splits.

**4.4 Acceptance Criteria Formats**

**Use Checklist format** for simple stories:
```markdown
**Acceptance Criteria:**
- [ ] User can select niche from dropdown
- [ ] Results update within 2 seconds
- [ ] Empty state shows "No matches found"
```

**Use Given/When/Then** for complex scenarios:
```markdown
**Acceptance Criteria:**

**Scenario: Filter by multiple niches**
Given I am on the influencer search page
And there are influencers tagged with "fitness" and "beauty"
When I select both "fitness" and "beauty" from the niche filter
Then I should see influencers tagged with either niche
And the result count should reflect the combined total
```

**4.5 Vertical Slicing**

If a story is too large, split VERTICALLY (end-to-end thin slice), not horizontally (by layer):

**Bad (horizontal):**
- Story A: Build database schema for filters
- Story B: Build API for filters
- Story C: Build UI for filters

**Good (vertical):**
- Story A: Basic niche filter (one dropdown, simple query, results display)
- Story B: Add country filter (extends filter UI, query, results)
- Story C: Add combined filter logic (AND/OR selection)

</phase_4_transform_user_stories>

<phase_5_prioritization>
**Phase 5: Prioritization & Validation**

**5.1 Inherit Priorities from BRD**

BR-XX priorities (Must/Should/Could) flow to derived requirements:
- BR-XX is Must → All FR-XX derived from it are Must
- BR-XX is Should → Derived FR-XX are Should (unless explicitly elevated)
- BR-XX is Could → Derived FR-XX are Could

**5.2 Apply 60% Rule**

Count Must-have requirements. If >60% of total:
```
Warning: Must-haves represent [X]% of scope (guideline: ≤60%).
Consider reviewing priorities for these requirements: [list candidates for demotion]
```

**5.3 Kano Validation (for User Stories)**

For each Must-have story, verify:
- "If missing, would users be actively dissatisfied?" → Confirms Must
- "If missing, would users not notice?" → Move to Could

For each Could-have, check:
- "Would this delight users?" → Mark as Differentiator

</phase_5_prioritization>

<phase_6_quality_verification>
**Phase 6: Quality Verification**

Before output, verify each requirement:

| Check | Question | Fix |
|-------|----------|-----|
| Atomic | One thing per requirement? | Split |
| Testable | Can write a test for this? | Add measurable criteria |
| Traceable | Links to BR-XX? | Add source reference |
| Prioritized | Has MoSCoW category? | Assign priority |
| Unambiguous | Single interpretation? | Rewrite with precision |

**Common fixes:**
- "Fast search" → "Search returns results within 2 seconds for up to 10,000 records"
- "Easy to use" → "New user can complete core workflow within 5 minutes without training"

**6.2 Document-Level Verification**

After verifying individual requirements, check document-level consistency:

| Check | Method |
|-------|--------|
| Count accuracy | Manually count FR, NFR, TRANS totals; verify they match summary table |
| Priority percentages | Recalculate Must/Should/Could percentages from counts |
| Traceability completeness | Every BR-XX has at least one FR in the traceability matrix |
| Cross-reference integrity | Every FR-XX referenced in the traceability matrix exists in Section 2 |
| No orphan requirements | Every FR-XX in Section 2 appears in the traceability matrix |

</phase_6_quality_verification>

<phase_7_output_srs>
**Phase 7a: Generate REQUIREMENTS.md (SRS Format)**

**Read template:** `templates/srs-template.md`

Write to `.charter/REQUIREMENTS.md` using the template structure. Fill in all placeholders with transformed requirements from previous phases.

</phase_7_output_srs>

<phase_7_output_stories>
**Phase 7b: Generate USER-STORIES.md (Agile Format)**

**Read template:** `templates/user-stories-template.md`

Write to `.charter/USER-STORIES.md` using the template structure. Fill in all placeholders with user stories from previous phases.

</phase_7_output_stories>

<phase_8_completion>
**Phase 8: Completion**

**8.1 Confirm Output**

Report to user:
```
Requirements generation complete.

**Mode:** [business-case | story-map]
**Files written:**
- .charter/REQUIREMENTS.md ([X] functional, [Y] non-functional requirements) [if selected]
- .charter/USER-STORIES.md ([Z] stories across [N] epics) [if selected]

**Coverage:**
- [X]/[Y] BR-XX requirements transformed
- [X]/[Y] SM-XXX stories expanded to US-XXX [story-map mode only]

**Priorities:**
- Must: [count] ([%])
- Should: [count] ([%])
- Could: [count] ([%])

**Traceability:** All requirements link to source BR-XX IDs.
[Story-map mode: All US-XXX link to parent SM-XXX IDs.]
```

**8.2 Offer Refinement**

"Would you like to:
1. Adjust any priorities?
2. Split large stories further?
3. Add requirements I may have missed?
4. Proceed to `/create-design-doc`?
5. Proceed to `/plan-project-roadmap`? [if story map was used]"

</phase_8_completion>

<success_criteria>
Requirements generation is complete when:
- [ ] BUSINESS-CASE.md parsed (all 9 sections)
- [ ] Section 9.6 reference documents loaded (if present)
- [ ] Stakeholders reused from Section 4 (not re-extracted)
- [ ] Constraints reused from Section 7 (not re-extracted)
- [ ] All BR-XX transformed to FR-XX and/or User Stories
- [ ] NFRs derived from constraints using ISO 25010 taxonomy
- [ ] All requirements have BR-XX traceability
- [ ] MoSCoW priorities assigned (inherited from BRD)
- [ ] 60% rule validated
- [ ] Output files written to `.charter/`
- [ ] User confirmed or adjusted output

**Additional checks for story-map mode:**
- [ ] STORY-MAP.md parsed (Activities, Tasks, SM-XXX IDs, releases)
- [ ] Every SM-XXX has **at least one** US-XXX child story
- [ ] Epic names match Activity names from story map
- [ ] Feature names match Task names from story map
- [ ] Release assignments preserved from story map
- [ ] BR-XX references in story map cross-checked against business case
- [ ] Traceability table uses SM-XXX → US-XXX format
</success_criteria>
