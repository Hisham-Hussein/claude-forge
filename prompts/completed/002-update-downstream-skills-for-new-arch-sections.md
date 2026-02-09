<objective>
Update two downstream skills (create-roadmaps, plan-phase-tasks) to read the two new ARCHITECTURE-DOC.md sections: Deployment View and Cross-Cutting Concerns.
</objective>

<context>
We added two new sections to the architecture doc template and workflow:
- **Section 7: Deployment View** — deployment diagram + environment mapping table (Container | Environment | Scaling | Notes)
- **Section 9: Cross-Cutting Concerns** — strategy table (Concern | Approach | Applies To) covering Security, Error Handling, Logging & Monitoring, Data Validation

These sections are generated but no downstream skill reads them yet. Two skills need updating:
1. `skills/create-roadmaps/SKILL.md`
2. `skills/plan-phase-tasks/SKILL.md`

**NOT in scope:** `skills/create-execution-plans/` (stale skill, no longer maintained)
</context>

<changes>

## Skill 1: create-roadmaps/SKILL.md

### Change 1.1: Progressive Loading Table (line 104)

Current:
```
| **ARCHITECTURE-DOC.md** | Domain model dependencies, Layer architecture, External interfaces, Constraints | C4 diagrams, ADRs, full implementation details |
```

Change to:
```
| **ARCHITECTURE-DOC.md** | Domain model dependencies, Layer architecture, External interfaces, Deployment view, Cross-cutting concerns, Constraints | C4 diagrams, ADRs, Quality Attributes, full implementation details |
```

Note: "Quality Attributes" was already implicitly skipped but wasn't listed in the Skip column. Add it explicitly for clarity since it's now between two sections that ARE read.

### Change 1.2: Read Architecture Doc Sections (lines 170-176)

Current:
```
**1.4 Read Architecture Doc Sections**

Read only:
- **Domain model** -- Entity relationships and dependencies
- **Layer architecture** -- Dependency rules (which layers build on which)
- **External interfaces** -- APIs, services, third-party integrations
- **Constraints** -- Technical blockers and limitations
```

Change to:
```
**1.4 Read Architecture Doc Sections**

Read only:
- **Domain model** -- Entity relationships and dependencies
- **Layer architecture** -- Dependency rules (which layers build on which)
- **External interfaces** -- APIs, services, third-party integrations
- **Deployment View** -- Container-to-infrastructure mapping, scaling approach
- **Cross-Cutting Concerns** -- System-wide patterns (security, error handling, logging, validation)
- **Constraints** -- Technical blockers and limitations
```

### Change 1.3: Parsing Summary (lines 189-193)

Current:
```
**Architecture:**
- Domain entities: [count]
- Key dependencies: [list critical ones]
- External interfaces: [count]
- Constraints: [count]
```

Change to:
```
**Architecture:**
- Domain entities: [count]
- Key dependencies: [list critical ones]
- External interfaces: [count]
- Deployment nodes: [count]
- Cross-cutting concerns: [count]
- Constraints: [count]
```

### Change 1.4: Dependency Analysis (lines 259-264)

The slice ordering logic at line 261-264 currently checks three dependency types. Add two more:

Current:
```
For each pair of slices within a release, determine if one depends on the other:
- Does Slice B require domain entities established in Slice A?
- Does Slice B consume an external service set up in Slice A?
- Does Slice B's application layer depend on Slice A's infrastructure?
```

Change to:
```
For each pair of slices within a release, determine if one depends on the other:
- Does Slice B require domain entities established in Slice A?
- Does Slice B consume an external service set up in Slice A?
- Does Slice B's application layer depend on Slice A's infrastructure?
- Does Slice B require deployment infrastructure (nodes, scaling) provisioned in Slice A?
- Does Slice B depend on a cross-cutting concern (auth, logging) that Slice A establishes?
```

### Change 1.5: Wave Validation (lines 291-296)

The constraint validation at line 293 already references "cross-cutting concerns (loaded in Phase 1)". Since we're now loading cross-cutting concerns from ARCHITECTURE-DOC.md (architectural strategies) in addition to STORY-MAP.md (business constraints), update the validation guidance:

Current:
```
Check cross-cutting concerns (loaded in Phase 1) against proposed wave groupings:
- Do any parallel slices share rate-limited resources (API budgets, external service quotas)?
- Do any business constraints gate specific slices (regulatory approvals, external dependency timelines)?
- If constraints conflict with proposed parallelism, downgrade from parallel to sequential or flag to user.
```

Change to:
```
Check cross-cutting concerns from both STORY-MAP.md (business constraints) and ARCHITECTURE-DOC.md (architectural strategies) against proposed wave groupings:
- Do any parallel slices share rate-limited resources (API budgets, external service quotas)?
- Do any business constraints gate specific slices (regulatory approvals, external dependency timelines)?
- Do any slices depend on shared infrastructure (deployment nodes) or cross-cutting patterns (auth middleware, logging framework) that must be established first?
- If constraints conflict with proposed parallelism, downgrade from parallel to sequential or flag to user.
```

---

## Skill 2: plan-phase-tasks/SKILL.md

### Change 2.1: Targeted Sections (lines 185-194)

Current:
```
**2.2 ARCHITECTURE-DOC.md — Targeted Sections**

Use `Grep` for `^##` headers, then `Read` only:
- **Domain Model** — entity relationships, dependencies
- **Architecture Layers** — layer separation rules
- **External Interfaces** — the `###` subsection under System Context
- **Key Interfaces** — contracts between layers
- **Constraints** — technical limits

Skip: C4 diagrams, ADRs, Quality Attributes, full implementation details.
```

Change to:
```
**2.2 ARCHITECTURE-DOC.md — Targeted Sections**

Use `Grep` for `^##` headers, then `Read` only:
- **Domain Model** — entity relationships, dependencies
- **Architecture Layers** — layer separation rules
- **External Interfaces** — the `###` subsection under System Context
- **Key Interfaces** — contracts between layers
- **Deployment View** — container-to-infrastructure mapping, scaling approach
- **Cross-Cutting Concerns** — system-wide patterns (security, error handling, logging, validation)
- **Constraints** — technical limits

Skip: C4 diagrams, ADRs, Quality Attributes, Data Flow, full implementation details.
```

Note: Added "Data Flow" to the explicit Skip list for clarity since it's now between two sections that ARE read.

### Change 2.2: Story Scope Analysis (lines 260-267)

The layer analysis currently only checks Domain, Application, Adapters. Add awareness of deployment and cross-cutting concerns:

Current:
```
Read the story's acceptance criteria carefully. Determine which architecture layers this story touches:
- **Domain** — new entities, value objects, validation rules, business logic
- **Application** — use cases, handlers, orchestration, interface definitions
- **Adapters** — UI components, API routes, data fetching, external service integrations

Not every story needs all three layers. Assign only the layers that are genuinely needed.
```

Change to:
```
Read the story's acceptance criteria carefully. Determine which architecture layers this story touches:
- **Domain** — new entities, value objects, validation rules, business logic
- **Application** — use cases, handlers, orchestration, interface definitions
- **Adapters** — UI components, API routes, data fetching, external service integrations
- **Infrastructure** — deployment configuration, scaling setup (from Deployment View)
- **Cross-Cutting** — auth middleware, error handling, logging setup (from Cross-Cutting Concerns)

Not every story needs all three core layers. Infrastructure and cross-cutting tasks typically appear in foundational phases (walking skeleton, early slices) rather than feature phases.
```

### Change 2.3: Layer Ordering (lines 279-284)

Current:
```
Within each story, tasks follow dependency order: Domain → Application → Adapters. This respects Clean Architecture dependency rules:
- Domain has no dependencies
- Application depends on Domain
- Adapters depend on Application and Domain
```

Change to:
```
Within each story, tasks follow dependency order: Domain → Application → Adapters → Infrastructure/Cross-Cutting. This respects Clean Architecture dependency rules:
- Domain has no dependencies
- Application depends on Domain
- Adapters depend on Application and Domain
- Infrastructure tasks (deployment config) come after adapters that define what gets deployed
- Cross-cutting tasks (auth, logging setup) come when the pattern spans multiple layers in this story
```

</changes>

<verification>
After implementing:
1. Read the final create-roadmaps/SKILL.md — confirm "Deployment View" and "Cross-Cutting Concerns" appear in the progressive loading table, the read sections list, the parsing summary, the dependency analysis, and the wave validation
2. Read the final plan-phase-tasks/SKILL.md — confirm "Deployment View" and "Cross-Cutting Concerns" appear in the targeted sections list, the story scope analysis, and the layer ordering
3. Verify no other sections were accidentally removed or modified
4. Stage only the two modified files and commit with: `feat(skills): update create-roadmaps and plan-phase-tasks to read new arch doc sections`
</verification>
