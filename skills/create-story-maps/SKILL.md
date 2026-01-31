---
name: create-story-maps
description: Use when user needs story mapping, MVP planning, journey visualization, release slicing, or walking skeleton planning from a business case. Transforms BUSINESS-CASE.md into a journey-organized story map with release slices. Complements /create-requirements (domain-organized backlog).
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
7. Offers to resolve identified gaps interactively or leave as documentation

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

After validation, read and follow `workflows/create-map.md` exactly.

</intake>

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
- [ ] Gaps offered for interactive resolution (user chose to resolve or defer)
- [ ] If resolved: answers incorporated into STORY-MAP.md and affected sections updated
- [ ] User confirmed or adjusted output
</success_criteria>
