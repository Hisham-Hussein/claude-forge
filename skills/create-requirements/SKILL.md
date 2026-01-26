---
name: create-requirements
description: Transform BUSINESS-CASE.md (from /create-business-case) into formal requirements. Outputs SRS format and/or User Stories with Use Case and BPMN diagrams. Use when user has completed Skill 1 and needs software requirements.
---

<objective>
**Requirements Engineer Skill**

Transform business case documents into formal, traceable software requirements specifications.

**Input:** `.charter/BUSINESS-CASE.md` (9-section format from `/create-business-case`)
**Outputs:**
- `.charter/REQUIREMENTS.md` (SRS format) — formal functional/non-functional requirements
- `.charter/USER-STORIES.md` (Agile format) — Epic/Feature/Story hierarchy with acceptance criteria
- Embedded diagrams: Use Case diagrams + BPMN process diagrams (via `/build-diagrams`)

**Methodology:** BABOK v3 + ISO/IEC 25010:2023 + INVEST criteria + MoSCoW prioritization

**Core principle:** Skill 1 already extracted stakeholders, constraints, and business requirements. This skill TRANSFORMS business requirements (BR-XX) into software requirements — it doesn't re-extract.
</objective>

<quick_start>
**Usage:**
```
/create-requirements .charter/BUSINESS-CASE.md
```

**What happens:**
1. Parses the 9-section BUSINESS-CASE.md format
2. Extracts BR-XX requirements from Section 9 (BRD)
3. Asks: "SRS format, User Stories, or both?"
4. Transforms BR-XX into software requirements with traceability
5. Generates Use Case and BPMN diagrams (invokes `/build-diagrams`)
6. Writes output to `.charter/`

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

**Diagram Generation (CRITICAL):**
- **NEVER write Mermaid code directly** — Always delegate to `/build-diagrams` skill via the Skill tool
- This ensures proper syntax, hex colors, platform compatibility, and accessibility
- See Phase 5 for exact invocation instructions

</essential_principles>

<intake>

Read the input document path from `$ARGUMENTS`. If no path provided, check if `.charter/BUSINESS-CASE.md` exists.

**Validation:**
1. Read the document
2. Verify it has the 9-section structure (look for "## 9. Business Requirements")
3. If not a BUSINESS-CASE.md format, warn: "This document doesn't match Skill 1's output format. Run `/create-business-case` first, or confirm you want generic extraction."

**After validation, ask output format:**

Use AskUserQuestion:
```
"What output format do you need?"
Options:
- SRS only (formal requirements specification)
- User Stories only (Agile backlog format)
- Both SRS and User Stories (Recommended)
```

Proceed to Phase 1 with the user's choice.

</intake>

<phase_1_parse_business_case>
## Phase 1: Parse BUSINESS-CASE.md

Extract structured data from each section:

### 1.1 From Section 4 (Stakeholders)
Parse the stakeholder table directly:
- Role, Type, Power/Interest, Needs, Engagement level
- These become actors for Use Cases and roles for User Stories

### 1.2 From Section 7 (Constraints)
Extract constraint categories:
- Timeline constraints → Schedule NFRs
- Budget constraints → Cost NFRs
- Technical constraints → Technology NFRs
- Team constraints → Capacity considerations
- Regulatory constraints → Compliance NFRs

### 1.3 From Section 9.2 (Scope)
Extract:
- In Scope items → Will generate requirements
- Out of Scope items → Document as "Won't Have" with rationale

### 1.4 From Section 9.3 (Business Requirements Table)
Parse the BR-XX table:
- ID (BR-01, BR-02, ...)
- Requirement text
- Priority (Must/Should/Could)
- Acceptance Criteria

### 1.5 From Section 6 (Success Criteria)
Extract KPIs and targets — these inform acceptance criteria for derived requirements.

### 1.6 Present Parsing Summary

```
## Business Case Parsing Summary

**Stakeholders found:** [count] ([list roles])
**Constraints identified:** [count] (Timeline: X, Budget: X, Technical: X, ...)
**Business Requirements (BR-XX):** [count] (Must: X, Should: X, Could: X)
**In-Scope items:** [count]
**Out-of-Scope items:** [count]

Ready to transform into [SRS / User Stories / Both].
```

Proceed to Phase 2.
</phase_1_parse_business_case>

<phase_2_clarification>
## Phase 2: Targeted Clarification

Only ask questions that the BUSINESS-CASE.md doesn't answer. Skip questions if the document is comprehensive.

### 2.1 NFR Questions (only if not in Section 7)

| Characteristic | Question | When to Ask |
|----------------|----------|-------------|
| Performance | "Any response time targets?" | If not in constraints |
| Reliability | "Availability expectations?" | If not in constraints |
| Security | "Security requirements beyond standard?" | If not in constraints |
| Scalability | "Expected data volume growth?" | If not in constraints |

### 2.2 Prioritization Validation

"The BRD lists [X] Must-haves. The 60% rule suggests Must-haves should be ≤60% of scope. Would you like to review priorities?"

Only ask if Must-haves exceed 60%.

### 2.3 User Story Specifics (if User Stories selected)

"For User Story output, should I:"
- Group by Epic (feature area) — Recommended
- Group by Actor (user role)
- Flat list (no hierarchy)

Proceed to Phase 3.
</phase_2_clarification>

<phase_3_transform_requirements>
## Phase 3: Transform BR-XX to Software Requirements

### 3.1 Functional Requirements (FR-XX)

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

### 3.2 Non-Functional Requirements (NFR-XX)

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

### 3.3 Transition Requirements (TRANS-XX)

Derive from:
- Data migration needs mentioned in the business case
- Integration with existing systems (e.g., Respond.io)
- Training or adoption requirements

### 3.4 Traceability

Every derived requirement MUST include:
```
Source: BR-XX (BUSINESS-CASE.md, Section 9.3)
```

</phase_3_transform_requirements>

<phase_4_transform_user_stories>
## Phase 4: Transform BR-XX to User Stories (if selected)

### 4.1 Build Epic/Feature/Story Hierarchy

**From BR-XX, derive:**
```
Epic: [Major capability area from BR-XX groupings]
  └── Feature: [Specific capability from single BR-XX]
        └── User Story: [Atomic user interaction]
```

**Example:**
```
Epic: Influencer Discovery System (from BR-01, BR-02, BR-03)
  └── Feature: Platform Discovery (from BR-02)
        └── Story: As a data collector, I want to trigger TikTok discovery by hashtag
        └── Story: As a data collector, I want to see discovery progress in real-time
```

### 4.2 Story Format

```markdown
## Story: [Brief title]

**Source:** BR-XX (BUSINESS-CASE.md, Section 9.3)
**Epic:** [Parent epic]
**Feature:** [Parent feature]

As a [role from Section 4 stakeholders],
I want [specific capability derived from BR-XX],
So that [benefit — often from BR-XX or Section 5].

### Acceptance Criteria

- [ ] [Criterion derived from BR-XX acceptance criteria or Section 6 KPIs]
- [ ] [Additional testable criterion]
- [ ] [Edge case handling]
```

### 4.3 INVEST Validation

Before finalizing each story, verify:
- **I**ndependent: Can be developed without other stories
- **N**egotiable: Implementation details not prescribed
- **V**aluable: Delivers clear user benefit
- **E**stimable: Scope is clear enough to estimate
- **S**mall: Completable in one sprint (split if too large)
- **T**estable: Acceptance criteria are verifiable

Flag stories that fail INVEST and suggest splits.

### 4.4 Acceptance Criteria Formats

**Use Checklist format** for simple stories:
```markdown
### Acceptance Criteria
- [ ] User can select niche from dropdown
- [ ] Results update within 2 seconds
- [ ] Empty state shows "No matches found"
```

**Use Given/When/Then** for complex scenarios:
```markdown
### Acceptance Criteria

**Scenario: Filter by multiple niches**
Given I am on the influencer search page
And there are influencers tagged with "fitness" and "beauty"
When I select both "fitness" and "beauty" from the niche filter
Then I should see influencers tagged with either niche
And the result count should reflect the combined total
```

### 4.5 Vertical Slicing

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

<phase_5_generate_diagrams>
## Phase 5: Generate Diagrams

<critical>
**NEVER create Mermaid diagrams inline.** You MUST delegate to the `/build-diagrams` skill using the Skill tool.

Why: The build-diagrams skill ensures:
- Correct Mermaid syntax (verified via Context7)
- Platform-appropriate rendering (GitHub vs VSCode)
- Hex color theming (color names fail on GitHub)
- Complexity limits (≤15 nodes)
- Accessibility compliance

If you write Mermaid directly, you bypass all these safeguards.
</critical>

### 5.1 Use Case Diagram

**MUST use Skill tool to invoke `/build-diagrams`:**

```
Skill tool invocation:
  skill: "build-diagrams"
  args: "flowchart --title=\"Use Case Diagram\" --target=github"
```

**Before invoking, prepare this context to provide when build-diagrams asks:**
- **Actors**: From Section 4 (Stakeholders) — filter to primary/secondary users only (CEO, Data Collectors, Campaign Managers, Reviewers)
- **Use Cases**: From BR-XX requirements — one use case per major capability
- **Connections**: Show which actor performs which use case
- **Layout**: LR (left-to-right) with actors on left, use cases on right in a subgraph

**After build-diagrams completes**, copy the generated Mermaid code block into the output document.

### 5.2 BPMN Process Diagram

**MUST use Skill tool to invoke `/build-diagrams`:**

```
Skill tool invocation:
  skill: "build-diagrams"
  args: "flowchart --title=\"Process Flow (BPMN)\" --target=github"
```

**Before invoking, prepare this context to provide when build-diagrams asks:**
- **Start/End events**: From Section 2 (Problem Statement) — what triggers the process, what's the outcome
- **Activities**: From BR-XX requirements — each capability becomes an activity node
- **Decision gateways**: From business rules and constraints — branching logic
- **Sequence flow**: Logical workflow order derived from the domain
- **Layout**: TD (top-to-bottom) for process flows

**After build-diagrams completes**, copy the generated Mermaid code block into the output document.

### 5.3 Diagram Placement

Embed the diagrams generated by `/build-diagrams` in output documents:
- **REQUIREMENTS.md**: Use Case diagram after Section 1 (Introduction), before Section 3 (Functional Requirements)
- **USER-STORIES.md**: BPMN diagram in the Overview section before Epic Summary

### 5.4 Verification

Before proceeding to Phase 6, confirm:
- [ ] Use Case diagram was generated via `/build-diagrams` Skill tool (not inline)
- [ ] BPMN diagram was generated via `/build-diagrams` Skill tool (not inline)
- [ ] Both diagrams render without errors
- [ ] Diagrams use hex colors (e.g., `#1976D2`), not color names (e.g., `blue`)

</phase_5_generate_diagrams>

<phase_6_prioritization>
## Phase 6: Prioritization & Validation

### 6.1 Inherit Priorities from BRD

BR-XX priorities (Must/Should/Could) flow to derived requirements:
- BR-XX is Must → All FR-XX derived from it are Must
- BR-XX is Should → Derived FR-XX are Should (unless explicitly elevated)
- BR-XX is Could → Derived FR-XX are Could

### 6.2 Apply 60% Rule

Count Must-have requirements. If >60% of total:
```
Warning: Must-haves represent [X]% of scope (guideline: ≤60%).
Consider reviewing priorities for these requirements: [list candidates for demotion]
```

### 6.3 Kano Validation (for User Stories)

For each Must-have story, verify:
- "If missing, would users be actively dissatisfied?" → Confirms Must
- "If missing, would users not notice?" → Move to Could

For each Could-have, check:
- "Would this delight users?" → Mark as Differentiator

</phase_6_prioritization>

<phase_7_quality_verification>
## Phase 7: Quality Verification

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

</phase_7_quality_verification>

<phase_8_output_srs>
## Phase 8a: Generate REQUIREMENTS.md (SRS Format)

Write to `.charter/REQUIREMENTS.md`:

```markdown
# Software Requirements Specification

> Generated from: .charter/BUSINESS-CASE.md
> Generated on: [date]
> Methodology: BABOK v3 + ISO/IEC 25010:2023

## 1. Introduction

### 1.1 Purpose
[Derived from Section 1 Executive Summary]

### 1.2 Scope
[From Section 9.2]

### 1.3 Stakeholders

[Table from Section 4, reformatted]

## 2. Use Case Diagram

<!-- IMPORTANT: Do NOT write Mermaid here directly. -->
<!-- Insert the diagram generated by /build-diagrams skill (Phase 5.1) -->

```mermaid
[Paste output from /build-diagrams skill here]
```

## 3. Functional Requirements

### 3.1 [Domain Area]

- [ ] **FR-[PREFIX]-01**: The system shall [behavior]
  - Source: BR-XX (BUSINESS-CASE.md, Section 9.3)
  - Priority: [Must/Should/Could] | Rationale: [why]
  - Acceptance Criteria: [from BR-XX or Section 6]

[Repeat for all functional requirements]

## 4. Non-Functional Requirements

### 4.1 Performance (ISO 25010: Performance Efficiency)

- [ ] **NFR-PERF-01**: [measurable performance target]
  - Source: Section 7 (Constraints) / BR-XX
  - Priority: [Must/Should/Could]

### 4.2 Reliability (ISO 25010: Reliability)
[...]

### 4.3 Security (ISO 25010: Security)
[...]

### 4.4 Scalability (ISO 25010: Flexibility)
[...]

### 4.5 Interaction Capability (ISO 25010: Usability)
[...]

### 4.6 Maintainability (ISO 25010: Maintainability)
[...]

## 5. Transition Requirements

- [ ] **TRANS-01**: [migration/integration requirement]
  - Source: Section 9.5 (Dependencies) / Section 3

## 6. Out of Scope (Won't Have)

| Requirement | Rationale | Revisit Trigger |
|-------------|-----------|-----------------|
| [From Section 9.2 Out of Scope] | [why excluded] | [when to reconsider] |

## 7. Traceability Matrix

| BR-XX | Functional Reqs | NFRs | User Stories |
|-------|-----------------|------|--------------|
| BR-01 | FR-DISC-01, FR-DISC-02 | NFR-PERF-01 | US-01, US-02 |
[...]

## 8. Prioritization Summary

| Category | Count | % of Total | Status |
|----------|-------|------------|--------|
| Must | X | X% | [OK/OVER 60%] |
| Should | X | X% | |
| Could | X | X% | |
| Won't | X | - | |
```

</phase_8_output_srs>

<phase_8_output_stories>
## Phase 8b: Generate USER-STORIES.md (Agile Format)

Write to `.charter/USER-STORIES.md`:

```markdown
# User Stories Backlog

> Generated from: .charter/BUSINESS-CASE.md
> Generated on: [date]
> Methodology: INVEST + MoSCoW + Vertical Slicing

## Overview

### Process Flow (BPMN)

<!-- IMPORTANT: Do NOT write Mermaid here directly. -->
<!-- Insert the diagram generated by /build-diagrams skill (Phase 5.2) -->

```mermaid
[Paste output from /build-diagrams skill here]
```

### Epic Summary

| Epic | Features | Stories | Priority |
|------|----------|---------|----------|
| [Epic 1] | X | Y | Must |
[...]

---

## Epic 1: [Name]

**Source:** BR-01, BR-02, BR-03
**Business Objective:** [From Section 9.1]

### Feature 1.1: [Name]

**Source:** BR-XX

#### US-001: [Story Title]

**Source:** BR-XX (BUSINESS-CASE.md, Section 9.3)

As a [role],
I want [capability],
So that [benefit].

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Priority:** Must | **Size:** [S/M/L] | **INVEST:** ✓

---

[Repeat for all stories]

---

## Deferred Stories (Won't Have This Release)

| Story | Source | Rationale | Revisit |
|-------|--------|-----------|---------|
| [From Section 9.2 Out of Scope] | BR-XX | [why] | [when] |

---

## Traceability

| BR-XX | Epic | Feature | Stories |
|-------|------|---------|---------|
| BR-01 | Epic 1 | Feature 1.1 | US-001, US-002 |
[...]
```

</phase_8_output_stories>

<phase_8c_enhance_acceptance_criteria>
## Phase 8c: Enhance Acceptance Criteria (Sub-Agent)

**When:** Only if User Stories output was selected (Phase 8b completed)

After writing USER-STORIES.md, spawn the AC Brainstormer sub-agent to systematically review and enhance acceptance criteria.

### 8c.1 Spawn Sub-Agent

Use the Task tool to spawn the ac-brainstormer sub-agent:

```
Task tool invocation:
  description: "Enhance acceptance criteria for user stories"
  prompt: "Review and enhance acceptance criteria in .charter/USER-STORIES.md using the ac-brainstorming methodology. Apply the Ten Questions, 6 Categories Framework, and edge case analysis to each story. Add missing criteria while preserving existing ones. Add sign-off summary at the end."
  subagent_type: "ac-brainstormer"
```

### 8c.2 What the Sub-Agent Does

The ac-brainstormer sub-agent:
1. Reads USER-STORIES.md
2. Applies systematic AC methodology (preloaded via skills: field)
3. Reviews each story for category coverage (functional, business rules, UI/UX, errors, NFRs, edge cases)
4. Adds missing acceptance criteria
5. Flags stories with >7 AC as split candidates
6. Edits the file with enhanced AC
7. Adds sign-off summary at the end

### 8c.3 Verify Enhancement

After sub-agent completes, confirm:
- [ ] AC count per story is now 3-7 (or flagged)
- [ ] Edge cases and error handling covered
- [ ] Sign-off summary added to USER-STORIES.md

</phase_8c_enhance_acceptance_criteria>

<phase_9_completion>
## Phase 9: Completion

### 9.1 Confirm Output

Report to user:
```
Requirements generation complete.

**Files written:**
- .charter/REQUIREMENTS.md ([X] functional, [Y] non-functional requirements)
- .charter/USER-STORIES.md ([Z] stories across [N] epics) [if selected]

**Coverage:**
- [X]/[Y] BR-XX requirements transformed
- [N] diagrams generated (Use Case, BPMN)

**Priorities:**
- Must: [count] ([%])
- Should: [count] ([%])
- Could: [count] ([%])

**Traceability:** All requirements link to source BR-XX IDs.
```

### 9.2 Offer Refinement

"Would you like to:
1. Adjust any priorities?
2. Split large stories further?
3. Add requirements I may have missed?
4. Proceed to Skill 3 (`/create-design-doc`)?"

</phase_9_completion>

<success_criteria>
Requirements generation is complete when:
- [ ] BUSINESS-CASE.md parsed (all 9 sections)
- [ ] Stakeholders reused from Section 4 (not re-extracted)
- [ ] Constraints reused from Section 7 (not re-extracted)
- [ ] All BR-XX transformed to FR-XX and/or User Stories
- [ ] NFRs derived from constraints using ISO 25010 taxonomy
- [ ] Use Case diagram generated using **Skill tool → `/build-diagrams`** (NOT inline Mermaid)
- [ ] BPMN process diagram generated using **Skill tool → `/build-diagrams`** (NOT inline Mermaid)
- [ ] Diagrams use hex colors and render correctly on target platform
- [ ] All requirements have BR-XX traceability
- [ ] MoSCoW priorities assigned (inherited from BRD)
- [ ] 60% rule validated
- [ ] Output files written to `.charter/`
- [ ] **AC Brainstormer sub-agent spawned** (if User Stories output selected)
- [ ] **Acceptance criteria enhanced** with methodology coverage
- [ ] **AC sign-off summary** added to USER-STORIES.md
- [ ] User confirmed or adjusted output
</success_criteria>
