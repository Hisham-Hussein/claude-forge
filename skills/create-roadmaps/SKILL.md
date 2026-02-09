---
name: create-roadmaps
description: Transform STORY-MAP.md and ARCHITECTURE-DOC.md into a phased project roadmap with vertical slices and wave-based parallelism. Use when user needs release planning, slice ordering, delivery sequencing, or wants to organize stories into an implementable roadmap.
---

<objective>
**Project Roadmap Skill**

Transform story map and architecture documents into a phased delivery roadmap with vertical slices grouped into parallelizable waves.

**Inputs:**

| Input | From Skill | Key Content |
|-------|------------|-------------|
| **STORY-MAP.md** | `/create-story-map` | Release slices, walking skeleton, SM-XXX IDs, BR-XX traceability |
| **ARCHITECTURE-DOC.md** | `/create-design-doc` | Domain model, layer dependencies, external interfaces, constraints |

**Output:** `.charter/ROADMAP.md` (~200-400 lines)

**Methodology:** Vertical Slice Delivery + Wave-Based Parallelism + Architectural Dependency Reconciliation

**What this skill does NOT consume:** USER-STORIES.md. Detailed acceptance criteria, sizing, and US-XXX IDs are consumed downstream by `/plan-phase-tasks`.

**Relationship to adjacent skills:**

| Aspect | /create-roadmap | /plan-phase-tasks |
|--------|----------------|-------------------|
| Question | WHICH stories, WHEN? | WHAT tasks for this slice? |
| Input | STORY-MAP.md + ARCHITECTURE-DOC.md | ROADMAP.md + USER-STORIES.md + ARCHITECTURE-DOC.md |
| Output | ROADMAP.md (~200-400 lines) | PHASE-N-PLAN.md (~150-300 lines per slice) |
| Parallelism | Wave grouping (which slices run simultaneously) | Story/task independence within a slice |
</objective>

<quick_start>
**Usage:**
```
/create-roadmap .charter/STORY-MAP.md .charter/ARCHITECTURE-DOC.md
/create-roadmap
```

If no arguments, defaults to `.charter/STORY-MAP.md` and `.charter/ARCHITECTURE-DOC.md`.

**What happens:**
1. Progressively loads relevant sections from both inputs (not full files)
2. Reads release slices from the story map as baseline
3. Reads architectural dependencies for ordering constraints
4. Breaks each release into vertical slices (deliverable chunks)
5. Orders slices and groups into parallelizable waves
6. Defines release transitions (Produces/Requires/Unlocks)
7. Asks user for Definition of Done per release
8. Generates compact ROADMAP.md

**Output:** `.charter/ROADMAP.md` with:
- Roadmap overview table (quick reference)
- Releases with wave-grouped vertical slices
- SM-XXX story assignments with BR-XX source
- Release transitions (dependency flow)
- Definition of Done per release
- Phase numbering (sequential across all releases)
- Cross-release dependencies
</quick_start>

<essential_principles>

**Vertical Slices, Not Horizontal Layers**

Each slice delivers end-to-end user value across all necessary architectural layers. A slice is NOT "build the database" -- it is "user can search by niche" (touching domain, application, adapter, and UI layers).

- **Good slice:** "User can discover influencers by niche and view basic profiles"
- **Bad slice:** "Set up database schema and API layer"

**Releases Come from the Story Map**

Releases are read from the story map's release slices -- the skill does not invent releases. The story map may define 2 releases or 6; the skill adapts. Within each release, the skill breaks stories into deliverable vertical slices.

**Reconcile Journey with Architecture**

The story map provides a user journey perspective. The architecture doc reveals technical dependencies. These two views may conflict. The skill must:

1. Start with story map release slices as baseline
2. Read architectural dependencies (domain model, layers, external interfaces)
3. Order slices so foundational work precedes dependent work
4. Move stories between slices *within the same release* if dependencies require it
5. Flag cross-release conflicts to the user rather than moving silently
6. Validate business constraints from cross-cutting concerns against wave groupings (e.g., API budget limits concurrent work, external dependencies gate specific slices)

**Ordering principle:** Slices that establish domain foundations come before slices that build on those foundations. External service setup precedes features consuming those services. This does NOT mean "build all domain, then all application" -- each slice touches multiple layers, but ORDERING respects foundations.

**Wave-Based Parallelism**

Slices within a release are grouped into waves:
- Slices in the same wave have no mutual dependencies and can execute in parallel
- Later waves depend on earlier waves completing
- Wave 1 = foundational slices (walking skeleton for first release, infrastructure for later releases)
- Label each wave as `parallel` (multiple independent slices) or `sequential` (single slice or dependency chain)

**Progressive Loading of Inputs**

Input documents can total 1,000-1,500+ lines combined. Do NOT read entire files. Use targeted `Grep` to find section headers, then `Read` with `offset` and `limit` to load only needed sections.

| Input | Sections to Read | Sections to Skip |
|-------|-----------------|-----------------|
| **STORY-MAP.md** | Release Overview table, Walking Skeleton, Traceability table, Cross-Cutting Concerns, Gaps and Open Questions | Visual Mermaid diagram, Detailed Map narrative |
| **ARCHITECTURE-DOC.md** | Domain model dependencies, Layer architecture, External interfaces, Deployment view, Cross-cutting concerns, Constraints | C4 diagrams, ADRs, Quality Attributes, full implementation details |

**Phase = Slice**

Each slice in the roadmap becomes one phase for `/plan-phase-tasks`. Phases are numbered sequentially across the entire roadmap (not reset per release). Example: MVP has 4 slices -> PHASE-1 through PHASE-4. R2 has 3 slices -> PHASE-5 through PHASE-7.

**SM-XXX IDs with BR-XX Source**

The roadmap uses SM-XXX IDs (from the story map) with their BR-XX source throughout. No SM-XXX to US-XXX cross-reference. When `/create-requirements` runs with STORY-MAP.md as input, each US-XXX traces to exactly one SM-XXX parent, creating lineage downstream.

</essential_principles>

<intake>

**Arguments:**
- First argument (optional): Path to STORY-MAP.md (default: `.charter/STORY-MAP.md`)
- Second argument (optional): Path to ARCHITECTURE-DOC.md (default: `.charter/ARCHITECTURE-DOC.md`)

**Examples:**
```
/create-roadmap
/create-roadmap .charter/STORY-MAP.md .charter/ARCHITECTURE-DOC.md
/create-roadmap path/to/STORY-MAP.md path/to/ARCHITECTURE-DOC.md
```

**Parsing:**
1. Split `$ARGUMENTS` by spaces
2. First path = story map document (default: `.charter/STORY-MAP.md`)
3. Second path = architecture document (default: `.charter/ARCHITECTURE-DOC.md`)
4. If no arguments provided, check defaults exist

**Validation:**
1. Verify story map file exists and contains release/walking skeleton sections
2. Verify architecture doc file exists and contains domain model or layer sections
3. If story map is missing: "STORY-MAP.md not found. Run `/create-story-map` first."
4. If architecture doc is missing: "ARCHITECTURE-DOC.md not found. Run `/create-design-doc` first."

Proceed to Phase 1.

</intake>

<phase_1_progressive_loading>
**Phase 1: Progressive Loading of Inputs**

Do NOT read entire files. Use targeted section extraction.

**1.1 Scan Story Map Headers**

Use `Grep` to find line numbers of markdown headings in STORY-MAP.md:
```
Grep(pattern="^##", file=[story-map-path], output_mode="content")
```

**1.2 Read Story Map Sections**

Read only these sections using `Read(file, offset, limit)`:
- **Release Overview table** -- Release structure, story counts per release
- **Walking Skeleton** -- Minimal end-to-end stories
- **Traceability table** -- All SM-XXX with BR-XX mappings and release assignments
- **Cross-Cutting Concerns** -- Constraints affecting roadmap decisions
- **Gaps and Open Questions** -- Unresolved decisions or blockers that may affect roadmap structure

**1.3 Scan Architecture Doc Headers**

Use `Grep` to find section headings in ARCHITECTURE-DOC.md.

**1.4 Read Architecture Doc Sections**

Read only:
- **Domain model** -- Entity relationships and dependencies
- **Layer architecture** -- Dependency rules (which layers build on which)
- **External interfaces** -- APIs, services, third-party integrations
- **Deployment View** -- Container-to-infrastructure mapping, scaling approach
- **Cross-Cutting Concerns** -- System-wide patterns (security, error handling, logging, validation)
- **Constraints** -- Technical blockers and limitations

**1.5 Present Parsing Summary**

```
## Input Parsing Summary

**Story Map:**
- Releases defined: [count] ([list names])
- Total stories: [count] (MVP: X, R2: Y, ...)
- Walking skeleton: [count] stories
- Cross-cutting concerns: [count]

**Architecture:**
- Domain entities: [count]
- Key dependencies: [list critical ones]
- External interfaces: [count]
- Deployment nodes: [count]
- Cross-cutting concerns: [count]
- Constraints: [count]

Ready to build roadmap.
```

Proceed to Phase 2.
</phase_1_progressive_loading>

<phase_2_build_slices>
**Phase 2: Build Vertical Slices**

**2.1 For Each Release**

Starting with the story map's release boundaries, group stories into vertical slices within each release.

**Slice criteria:**
- Each slice delivers end-to-end user value
- A user should be able to USE the result of a slice
- Slices are days-to-weeks of work, not months
- Slices should roughly align with story map activity groupings where natural

**2.2 Walking Skeleton as First Slice**

For the first release (usually MVP), the first slice is always the walking skeleton:
- Take the walking skeleton stories from the story map
- This slice establishes the minimal end-to-end journey
- It touches all necessary architectural layers

**2.3 Remaining Slices**

Group remaining stories within each release into slices based on:
- Journey coherence (don't split related stories across slices)
- Architectural proximity (stories needing the same domain entities)
- Activity groupings (stories under the same activity often form natural slices)

**2.4 Present Proposed Slices**

```
## Proposed Vertical Slices

### [Release Name] ([count] slices)

**Slice 1: [Name -- Walking Skeleton]**
Stories: SM-XXX, SM-XXX, SM-XXX
Delivers: [End-to-end capability]

**Slice 2: [Name]**
Stories: SM-XXX, SM-XXX
Delivers: [Capability]

**Slice 3: [Name]**
Stories: SM-XXX, SM-XXX
Delivers: [Capability]

### [Release 2 Name] ([count] slices)
...

Does this slice grouping make sense? Any stories to move between slices?
```

Wait for user confirmation before proceeding.
</phase_2_build_slices>

<phase_3_order_and_wave>
**Phase 3: Order Slices and Group into Waves**

**3.1 Analyze Dependencies**

For each pair of slices within a release, determine if one depends on the other:
- Does Slice B require domain entities established in Slice A?
- Does Slice B consume an external service set up in Slice A?
- Does Slice B's application layer depend on Slice A's infrastructure?
- Does Slice B require deployment infrastructure (nodes, scaling) provisioned in Slice A?
- Does Slice B depend on a cross-cutting concern (auth, logging) that Slice A establishes?

**3.2 Order Slices**

Within each release, order slices so that:
- Foundational slices (domain setup, service connections) come first
- Feature slices build on the foundation
- Integration/validation slices come last

Architectural ordering specifics (from the architecture doc's layer dependencies):
- Slices that establish domain foundations come before slices that build features on those foundations
- The walking skeleton slice includes minimal representatives from all necessary layers
- External service setup (API connections, third-party integrations) is placed before features that consume those services

Note: This does NOT mean "build all domain, then all application" — that would be horizontal slicing. Each vertical slice touches multiple layers, but the *ordering* of slices respects which foundations must exist first.

**3.3 Group into Waves**

Within each release:
1. Wave 1: Slices with no intra-release dependencies (typically the walking skeleton or foundation)
2. Wave 2: Slices that depend only on Wave 1 outputs AND are independent of each other
3. Wave 3+: Continue until all slices are assigned

Label each wave:
- `sequential` -- single slice or slices that must run in order
- `parallel` -- multiple independent slices that can run simultaneously

**3.4 Validate Business Constraints Against Waves**

Check cross-cutting concerns from both STORY-MAP.md (business constraints) and ARCHITECTURE-DOC.md (architectural strategies) against proposed wave groupings:
- Do any parallel slices share rate-limited resources (API budgets, external service quotas)?
- Do any business constraints gate specific slices (regulatory approvals, external dependency timelines)?
- Do any slices depend on shared infrastructure (deployment nodes) or cross-cutting patterns (auth middleware, logging framework) that must be established first?
- If constraints conflict with proposed parallelism, downgrade from parallel to sequential or flag to user.

**3.5 Reconciliation Conflicts**

If architectural dependencies conflict with story map groupings:
- Move stories between slices *within the same release*
- If cross-release movement is needed, flag to user:
  "Story SM-XXX depends on infrastructure from SM-YYY (currently in [Release]). Recommend moving or reordering."

**3.6 Present Wave Structure**

```
## Wave Structure

### [Release Name]

Wave 1 (sequential -- foundation):
  Slice 1: [Name]

Wave 2 (parallel -- independent):
  Slice 2: [Name]
  Slice 3: [Name]

Wave 3 (sequential -- integration):
  Slice 4: [Name]

### [Release 2 Name]
...

Any adjustments needed?
```

Wait for confirmation before proceeding.
</phase_3_order_and_wave>

<phase_4_transitions_and_dod>
**Phase 4: Define Release Transitions and Definition of Done**

**4.1 Release Transitions**

For each release, define:
- **Produces:** What this release delivers that downstream work depends on
- **Requires:** What must exist from prior releases (none for first release)
- **Unlocks:** What becomes possible after this release

**4.2 Definition of Done**

Ask user for DoD criteria per release using AskUserQuestion. Suggest categories:

```
"What should the Definition of Done include for [Release Name]?"

Options:
1. Standard (functional completeness + basic tests + manual verification)
2. Thorough (functional + unit/integration tests + CI green + deployed to staging)
3. Let me specify custom criteria
```

**4.3 Assign Phase Numbers**

Number phases sequentially across all releases:
- Phase 1 = first slice of first release
- Phase N = last slice of last release
- Phases are never reset per release

**4.4 Present Transitions and DoD**

```
## Release Transitions

### [Release 1]
Produces: [Core entities, primary adapter, basic UI]
Requires: Nothing (first release)
Unlocks: [What R2 can build on]

DoD:
- [ ] [Criteria 1]
- [ ] [Criteria 2]

### [Release 2]
Produces: [What R2 delivers]
Requires: [What from R1]
Unlocks: [What R3 can build on]

DoD:
- [ ] [Criteria 1]
- [ ] [Criteria 2]

Confirm transitions and DoD?
```

Wait for user confirmation.
</phase_4_transitions_and_dod>

<phase_5_generate_output>
**Phase 5: Generate ROADMAP.md**

**Read template:** `templates/roadmap-template.md`

Generate the roadmap output following the template structure.

**Key output sections:**

1. **Quick Reference** -- Roadmap overview table, release summary
2. **Release sections** -- Each release with transitions, waves, slices, story tables
3. **Phase Numbering** -- Sequential mapping across all releases
4. **Cross-Release Dependencies** -- What connects releases
5. **Complementary Artifacts** -- Links to adjacent skills

**Output rules:**
- Use SM-XXX IDs with BR-XX source throughout (no US-XXX references)
- Keep output within ~200-400 lines
- Each slice has a brief description + story table (no full story cards)
- Wave labels include `sequential` or `parallel` designation

Write output to `.charter/ROADMAP.md`.
</phase_5_generate_output>

<phase_6_completion>
**Phase 6: Completion**

**6.1 Confirm Output**

```
Roadmap generation complete.

**File written:** .charter/ROADMAP.md

**Structure:**
- Releases: [count]
- Total slices: [count]
- Total phases: [count]
- Stories assigned: [count]

**Wave structure:**
- [Release 1]: [X] waves ([Y] parallel opportunities)
- [Release 2]: [X] waves ([Y] parallel opportunities)

**Coverage:**
- [X]/[Y] SM-XXX stories assigned to slices
- All slices deliver end-to-end value
```

**6.2 Offer Next Steps**

"Would you like to:
1. Adjust slice boundaries or wave groupings?
2. Modify release transitions or DoD criteria?
3. Run `/plan-phase-tasks` to break a phase into tasks (requires USER-STORIES.md)?
4. Update `/create-requirements` to add SM-XXX lineage?"
</phase_6_completion>

<success_criteria>
Roadmap generation is complete when:

- [ ] Both inputs progressively loaded (not full files read into context)
- [ ] All releases from story map represented in roadmap
- [ ] Each release broken into vertical slices (end-to-end value each)
- [ ] Walking skeleton is first slice of first release
- [ ] Slices ordered by architectural dependencies
- [ ] Slices grouped into waves (parallel/sequential labeled)
- [ ] Release transitions defined (Produces/Requires/Unlocks)
- [ ] Definition of Done per release confirmed by user
- [ ] Phases numbered sequentially across all releases
- [ ] All SM-XXX stories assigned to slices with BR-XX source
- [ ] No architectural conflicts left unresolved
- [ ] Output written to `.charter/ROADMAP.md` (~200-400 lines)
- [ ] User confirmed output
</success_criteria>
