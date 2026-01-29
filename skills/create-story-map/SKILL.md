---
name: create-story-map
description: Transform BUSINESS-CASE.md into a journey-organized story map with release slices. Use when user needs MVP planning, journey visualization, or shared product understanding. Complements /create-requirements (domain-organized backlog).
---

<objective>
**Story Mapping Skill**

Transform business case documents into 2D user story maps organized by user journey with release slices.

**Input:** `.charter/BUSINESS-CASE.md` (9-section format from `/create-business-case`)
**Output:** `.charter/STORY-MAP.md` (journey-organized map with release slices)

**Methodology:** Jeff Patton's User Story Mapping + Walking Skeleton + Vertical Release Slicing

**Relationship to /create-requirements:**
| Aspect | /create-requirements | /create-story-map |
|--------|----------------------|-------------------|
| Organization | Domain (Epic → Feature → Story) | Journey (Activity → Task → Story) |
| Output | Full story cards with AC | Compact map with release slices |
| Best for | Formal documentation, sprint planning | MVP planning, shared understanding |

Both consume BUSINESS-CASE.md. Use together: map for vision, backlog for execution.

**Output philosophy:** The story map is a PLANNING artifact, not a backlog. It shows WHAT stories exist, WHERE they sit in the journey, and WHICH release they belong to — but does NOT duplicate full story cards (As a / I want / So that + acceptance criteria). Full story details belong in USER-STORIES.md from `/create-requirements`.
</objective>

<quick_start>
**Usage:**
```
/create-story-map .charter/BUSINESS-CASE.md
/create-story-map .charter/BUSINESS-CASE.md assets/CLIENT-BRIEF.md
```

**What happens:**
1. Parses BUSINESS-CASE.md for BR-XX requirements, stakeholders, constraints
2. Identifies user personas and their goals
3. Builds Activity → Task backbone (horizontal journey)
4. Places stories vertically by priority under each task
5. Asks user to define release boundaries (MVP, R2, R3)
6. Generates compact STORY-MAP.md

**Output:** `.charter/STORY-MAP.md` with:
- Release overview table (quick reference)
- Mermaid diagram (visual map)
- Detailed map (stories per task with release assignments)
- Walking skeleton (minimal end-to-end journey)
- Traceability table (BR-XX links)
- Cross-cutting concerns and gaps
</quick_start>

<essential_principles>

**Story Mapping is 2D, Not 1D**

Unlike flat backlogs, story maps preserve context through two dimensions:
- **Horizontal (left → right):** User's journey through the product (activities and tasks)
- **Vertical (top → down):** Priority within each task (must-haves at top, nice-to-haves below)

```
ACTIVITIES:  [Discover] ──→ [Search] ──→ [Evaluate] ──→ [Contact] ──→ [Track]
BACKBONE:     Configure     Query        View profile   Select       Monitor
              Run           Filter       Check metrics  Send         Log
              Review        Sort         Compare        Track        Flag
                │             │              │            │            │
STORIES:      ─┼─────────────┼──────────────┼────────────┼────────────┼─ MVP
              ─┼─────────────┼──────────────┼────────────┼────────────┼─ R2
              ─┼─────────────┼──────────────┼────────────┼────────────┼─ Future
```

**The Three Layers**

1. **Activities (Goals):** High-level user goals forming the top row. Answer: "What is the user fundamentally trying to do?" Keep to 3-7 activities.

2. **Backbone (Tasks):** Steps under each activity. Read left-to-right as narrative: "First the user does X, then Y, then Z."

3. **User Stories:** Hang vertically under tasks, ordered by priority. Top = must-have, bottom = nice-to-have.

**Walking Skeleton First**

The walking skeleton is the minimal slice that provides end-to-end functionality. On the map, it's the top row of stories under each backbone task.

**Key insight: Go right before going down.** Build the walking skeleton (horizontal slice) before adding depth to any single feature. This ensures you always have a working product.

**Release Slicing is Horizontal**

Draw horizontal lines to create release slices. Each release delivers end-to-end value—a user can complete their journey with that release, just with fewer options.

**Good slice:** "Release 1 lets users search by niche, country, and platform—simple but complete"
**Bad slice:** "Release 1 builds the database schema" (no user value)

**Transformation, Not Re-extraction**

Like /create-requirements, this skill TRANSFORMS BR-XX requirements. It doesn't re-extract stakeholders or constraints—pull them directly from the business case.

| Section | How it Maps |
|---------|-------------|
| Section 4 (Stakeholders) | → Personas for story map |
| Section 7 (Constraints) | → Cross-cutting concerns |
| Section 9.3 (BR-XX) | → Stories placed on map |
| Section 6 (Success Criteria) | → Release slice criteria |

</essential_principles>

<intake>

**Arguments:**
- First argument (required): Path to BUSINESS-CASE.md
- Additional arguments (optional): Reference documents for detailed specifications

**Examples:**
```
/create-story-map .charter/BUSINESS-CASE.md
/create-story-map .charter/BUSINESS-CASE.md assets/CLIENT-BRIEF.md
```

**Parsing:**
1. Split `$ARGUMENTS` by spaces
2. First path = business case document
3. Remaining paths = explicit reference documents
4. If no arguments provided, check if `.charter/BUSINESS-CASE.md` exists

**Validation:**
1. Read the business case document
2. Verify it has the 9-section structure (look for "## 9. Business Requirements")
3. If not a BUSINESS-CASE.md format, warn: "This document doesn't match the expected format. Run `/create-business-case` first, or confirm you want generic extraction."

Proceed to Phase 1.

</intake>

<phase_1_parse_and_identify_personas>
**Phase 1: Parse Business Case and Identify Personas**

**1.1 Extract Stakeholders as Personas**

From Section 4 (Stakeholders), identify user personas for the story map:
- Filter to stakeholders with Type = "User" or direct system interaction
- Each persona may have a different journey through the product

```
Persona: [Role from Section 4]
Goals: [Derived from stakeholder Needs column]
Key Activities: [Inferred from their role]
```

**1.2 Load Reference Documents**

Collect references from two sources:

1. **From Section 9.6 (automatic):** If Section 9.6 (Reference Documents) exists, collect all document paths listed in the reference table.
2. **From command arguments (explicit):** If reference documents were passed as arguments in the intake phase, add them to the collection.
3. **Merge and deduplicate:** Combine both sources. Load once if duplicated.
4. **Load all collected references:** Extract detailed specifications (data types, validation rules, thresholds, enumerations) that inform story granularity and scope decisions.

**If no references from either source:** Proceed without additional context. Stories may lack implementation-level precision.

**1.3 Extract BR-XX Requirements**

From Section 9.3, parse the requirements table:
- ID (BR-01, BR-02, ...)
- Requirement text
- Priority (Must/Should/Could)
- Acceptance Criteria

**1.4 Extract Constraints**

From Section 7, note cross-cutting concerns that apply across the map:
- Timeline constraints → Affect release slicing
- Technical constraints → May limit certain activities
- Regulatory constraints → Add compliance requirements

**1.5 Present Parsing Summary**

```
## Business Case Parsing Summary

**Personas identified:** [count] ([list roles])
**Business Requirements (BR-XX):** [count] (Must: X, Should: X, Could: X)
**Constraints:** [count] cross-cutting concerns

Ready to build story map.
```

Proceed to Phase 2.
</phase_1_parse_and_identify_personas>

<phase_2_build_backbone>
**Phase 2: Build the Backbone**

**2.1 Identify Activities (User Goals)**

Group BR-XX requirements by the user goal they serve. Ask:
- "What is the user fundamentally trying to accomplish?"
- "What major activity areas does this product support?"

Typical activity patterns:
- **Discover/Create** — Adding new data to the system
- **Search/Find** — Locating existing data
- **Evaluate/Analyze** — Assessing or comparing items
- **Act/Execute** — Taking action on items
- **Track/Monitor** — Following progress over time

**2.2 Define Tasks Under Each Activity**

For each activity, list the sequential steps a user takes:
- Tasks should read as a narrative left-to-right
- Each task is a verb phrase: "Enter query", "Apply filters", "View results"

**2.3 Validate Backbone**

Use the "tell the story" test:
- Can you walk the backbone left-to-right and tell a coherent user story?
- If stuck or confused, there's a gap—add missing tasks.

**2.4 Present Backbone for Confirmation**

```
## Proposed Backbone

Activity 1: [Name] — [Goal]
  Tasks: [Task A] → [Task B] → [Task C]

Activity 2: [Name] — [Goal]
  Tasks: [Task A] → [Task B] → [Task C]

[...]

Does this capture the user's journey? Any activities or tasks to add/remove?
```

Wait for user confirmation before proceeding.
</phase_2_build_backbone>

<phase_3_place_stories>
**Phase 3: Place Stories on the Map**

**3.1 Map BR-XX to Tasks**

For each BR-XX requirement:
1. Identify which activity it belongs to
2. Identify which task it supports
3. Create one or more user stories

**Story format (internal working format — NOT written to output):**

For each story, define internally:
- Title: short descriptive name
- Persona: from Phase 1
- Capability: from BR-XX
- Benefit: from BR-XX or Section 5
- BR-XX source

The output file uses ONLY story ID + title + BR-XX source in the Detailed Map tables. Full "As a / I want / So that" story cards are NOT included in the story map output — they belong in USER-STORIES.md from `/create-requirements`.

**3.2 Vertical Priority**

Place stories under their task in priority order (top = highest):
- Must-have (from BRD) → Top (walking skeleton candidates)
- Should-have → Middle
- Could-have → Bottom

**3.3 One BR May Spawn Multiple Stories**

If BR-XX contains multiple capabilities, create atomic stories:
```
BR-06: "searchable interface for niche, country, platform, size"
    ↓
Task: Apply filters
  - Filter by niche (Must)
  - Filter by country (Must)
  - Filter by platform (Must)
  - Filter by size bucket (Must)
  - Combined AND/OR logic (Should)
```

**3.4 Assign Story IDs**

Use format: `SM-[Activity#].[Task#]-[Seq]`
- SM-1.2-01 = Activity 1, Task 2, Story 1
- Or use simple sequential: SM-001, SM-002, ...

**3.5 Track Traceability**

Every story MUST link back to BR-XX:
```
SM-001: Filter by niche
  Source: BR-06 (BUSINESS-CASE.md, Section 9.3)
```

</phase_3_place_stories>

<phase_4_define_releases>
**Phase 4: Define Release Slices**

**4.1 Identify Walking Skeleton**

The walking skeleton is the minimal end-to-end journey. For each task:
- What is the ONE story that enables basic functionality?
- Mark these as MVP candidates

**4.2 Ask User for Release Boundaries**

Use AskUserQuestion:
```
"How many release slices do you want to define?"

Options:
- 2 releases (MVP + Future) — Simplest
- 3 releases (MVP + R2 + Future) — Recommended
- 4 releases (MVP + R2 + R3 + Future) — Detailed planning
```

**4.3 Slice Criteria**

For each release, define what "done" means:
- MVP: User can complete the core journey (walking skeleton)
- R2: Adds depth to high-value areas
- R3: Polish and differentiation
- Future: Backlog for later

**4.4 Validate Each Slice**

Each slice should:
- Deliver end-to-end user value
- Be independently deployable
- Have clear success criteria (from Section 6)

**4.5 Present Release Plan**

```
## Release Slices

**MVP (Walking Skeleton):**
[X] stories across all activities
User can: [describe end-to-end capability]

**Release 2:**
[Y] additional stories
User gains: [describe added capabilities]

**Future:**
[Z] stories deferred
Rationale: [why deferred]
```

Wait for user confirmation before generating output.
</phase_4_define_releases>

<phase_5_generate_output>
**Phase 5: Generate STORY-MAP.md**

**Read template:** `templates/story-map-template.md`

Generate a compact output file. The story map is a PLANNING artifact — it shows story placement and release slicing, NOT full story details. Full story cards with acceptance criteria belong in USER-STORIES.md (from `/create-requirements`).

**5.1 Quick Reference (Release Overview Table)**

Shows what's in each release at a glance—one row per activity/task combo.

**5.2 Visual Map (Mermaid Diagram)**

```mermaid
journey
    title [Primary Persona] Journey
    section [Activity 1]
      [Task 1]: 5: [Persona]
      [Task 2]: 4: [Persona]
    section [Activity 2]
      ...
```

**5.3 Detailed Map (Nested Sections)**

Story IDs, titles, and BR-XX sources per task. Brief task descriptions. NO full story cards — no "As a / I want / So that", no acceptance criteria checkboxes.

```markdown
## Activity 1: [Name]

**Goal:** [User goal]
**Persona:** [Primary persona]
**Source:** BR-XX, BR-XX

### Task 1.1: [Name]

[Brief description of what happens in this task]

| Release | Stories |
|---------|---------|
| **MVP** | • SM-001: [Story title] (BR-XX) |
| **R2**  | • SM-005: [Story title] (BR-XX) |
```

**5.4 Walking Skeleton Table**

Minimal MVP story per task showing end-to-end capability.

**5.5 Traceability Table**

Single compact cross-reference. Do NOT produce multiple traceability views (e.g., separate "BR-XX Coverage" table). One table is sufficient:

| Story ID | Title | BR-XX | Release |
|----------|-------|-------|---------|

After the table, add a one-line coverage summary: `**Coverage:** X/Y BR-XX requirements mapped`

**5.6 Cross-Cutting Concerns and Gaps**

From Section 7 constraints and any unresolved questions.

**What NOT to include:**
- **No Story Details section** — Full "As a / I want / So that" + acceptance criteria belong in USER-STORIES.md, not the story map
- **No Tool Export section** — TextUSM/MarkdownUSM format is a niche concern; omit from default output
- **No duplicate traceability** — One cross-reference table, not multiple orientations of the same data

Write output to `.charter/STORY-MAP.md`.

</phase_5_generate_output>

<phase_6_completion>
**Phase 6: Completion**

**6.1 Confirm Output**

```
Story map generation complete.

**File written:** .charter/STORY-MAP.md

**Map Structure:**
- Activities: [count]
- Tasks: [count]
- Stories: [count] (MVP: X, R2: Y, Future: Z)

**Coverage:**
- [X]/[Y] BR-XX requirements mapped
- All stories traceable to source

**Walking Skeleton:** [count] stories provide end-to-end journey
```

**6.2 Offer Next Steps**

"Would you like to:
1. Adjust release boundaries?
2. Add missing activities or tasks?
3. Generate `/create-requirements` output as well (complementary backlog)?
4. Proceed to `/create-design-doc`?"

</phase_6_completion>

<success_criteria>
Story map generation is complete when:
- [ ] BUSINESS-CASE.md parsed (personas, BR-XX, constraints)
- [ ] Personas identified from Section 4 stakeholders
- [ ] Activities identified (3-7 high-level user goals)
- [ ] Backbone built (tasks under each activity)
- [ ] User confirmed backbone captures the journey
- [ ] All BR-XX mapped to stories under tasks
- [ ] Stories prioritized vertically (must-have at top)
- [ ] Release slices defined (MVP + R2 + Future minimum)
- [ ] Walking skeleton identified (top story per task)
- [ ] Each release delivers end-to-end value
- [ ] All stories have BR-XX traceability
- [ ] Compact output written to `.charter/STORY-MAP.md` (no full story cards, no duplicate traceability)
- [ ] User confirmed or adjusted output
</success_criteria>
