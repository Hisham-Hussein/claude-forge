---
name: create-design-docs
description: Transform requirements into software architecture documentation. Use when user has requirements specs, user stories, or business cases and needs design documents, architecture documentation, or ADRs. Use when user mentions "design doc", "architecture doc", "system design", or "technical design".
argument-hint: [user-stories.md] [requirements.md] [additional-files...]
---

<objective>
**Software Architect Skill**

Transform requirements specifications into technology-agnostic software architecture documentation.

**Inputs (any combination):**
- **User Stories** — Epic/Feature/Story hierarchy with acceptance criteria
- **SRS Document** (optional) — Functional requirements (FR-XX), Non-functional requirements (NFR-XX)
- **Business Case** (optional) — Stakeholders, constraints, business requirements
- **Additional reference files** (optional) — Data models, API specs, integration docs

**Outputs (user selects one):**
1. **Design Document** (lightweight) — Goals/Non-Goals, Alternatives Considered, Key Decisions (~10-20 pages)
2. **Architecture Document** (comprehensive) — Domain Model, Layers, Interfaces, Quality Attributes (~20-40 pages)
3. **Hybrid Document** (both) — Single document with all sections (Recommended)

**Methodology:** Google Design Docs + C4 Model + Architecture Decision Records (ADRs)

**Core principle:** Architecture documentation captures what you CAN'T get from the code — context, decisions, trade-offs, and the "why" behind the "what." Technology choices belong in ADRs, not the architecture document itself.
</objective>

<quick_start>
**Usage:**
```
/create-design-doc [path-to-user-stories] [path-to-requirements] [additional-files...]
```

**Examples:**
```
/create-design-doc docs/USER-STORIES.md
/create-design-doc docs/USER-STORIES.md docs/REQUIREMENTS.md
/create-design-doc .charter/USER-STORIES.md .charter/BUSINESS-CASE.md assets/data-model.md
```

**What happens:**
1. Reads provided input files (prompts for paths if none provided)
2. Asks: "What type of document do you need?"
3. Extracts domain model from requirements
4. Maps to architecture layers (Clean Architecture)
5. Documents interfaces and quality attributes
6. Creates C4 diagrams (Context, Container)
7. Writes output to same directory as primary input file

**Output location:** Same directory as primary input file (e.g., `docs/DESIGN-DOC.md`)
</quick_start>

<essential_principles>

**Expected Input Formats:**

This skill works best with structured requirements artifacts:
- **User Stories** — Epic/Feature/Story hierarchy (format from `/create-requirements` or similar)
- **SRS/REQUIREMENTS.md** — Functional requirements (FR-XX), Non-functional requirements (NFR-XX)
- **BUSINESS-CASE.md** — Business context, stakeholders, constraints
- **Data Models** (optional) — SQL DDL, Prisma/Drizzle schemas, ORM definitions, ER diagrams
- **API Specifications** (optional) — OpenAPI/Swagger, GraphQL schemas, gRPC protobuf, tRPC routers

**Technology-Agnostic Architecture:**

The architecture document describes WHAT the system does and HOW it's structured, NOT which specific technologies implement it.

| In Architecture Doc | In ADRs (Separate) |
|--------------------|--------------------|
| "Repository interface for persistence" | "ADR-001: Use PostgreSQL for relational data" |
| "Web interface for user interactions" | "ADR-002: Use React for frontend" |
| "External API adapter for platform data" | "ADR-003: Use RapidAPI for TikTok access" |

**Document What Code Can't Show:**

| Document | Skip |
|----------|------|
| Context (who uses it, what it integrates with) | Implementation details |
| Decisions (why this approach, what alternatives) | Code that's self-documenting |
| Trade-offs (what we sacrificed for what) | Standard patterns Claude knows |
| Boundaries (in-scope vs out-of-scope) | Line-by-line explanation |

**Domain Model Extraction:**

User stories describe BEHAVIOR. Domain model describes STRUCTURE. Extract:
- **Entities** — Nouns that have identity and lifecycle (e.g., Influencer, Campaign)
- **Value Objects** — Immutable concepts (e.g., FollowerCount, EngagementRate)
- **Aggregates** — Entity clusters with consistency boundaries
- **Domain Services** — Operations spanning multiple entities

**C4 Model Levels:**

Most projects need only Levels 1-2:
```
Level 1: System Context  — How does the system fit in the world?
Level 2: Container       — What are the major technical building blocks?
Level 3: Component       — What's inside each container? (Optional)
Level 4: Code            — Class diagrams (Rarely needed — code is the truth)
```

</essential_principles>

<intake>

**Parse Arguments:**
1. If arguments provided, use them as paths to input files
2. If no arguments, use AskUserQuestion to prompt for input paths:
   - "Please provide paths to your requirements files (user stories, SRS, business case)"
3. Validate all provided files exist before proceeding

**After loading inputs, ask document type:**

Use AskUserQuestion:
```
"What type of architecture document do you need?"

Options:
1. Design Document (lightweight) — Focus on decisions, alternatives, goals/non-goals. Best for: features, spikes, technical proposals. (~10-20 pages)
2. Architecture Document (comprehensive) — Full domain model, layers, interfaces, quality attributes. Best for: new systems, major refactors. (~20-40 pages)
3. Hybrid (both) — Design decisions + Architecture structure in one document. Best for: most projects. (Recommended)
```

Route based on selection:
- Option 1 → `workflows/create-design-doc.md`
- Option 2 → `workflows/create-architecture-doc.md`
- Option 3 → `workflows/create-hybrid-doc.md`

</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "design", "lightweight", "decisions" | `workflows/create-design-doc.md` |
| 2, "architecture", "comprehensive", "full" | `workflows/create-architecture-doc.md` |
| 3, "hybrid", "both", "recommended" | `workflows/create-hybrid-doc.md` |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
**Domain Knowledge (read as needed):**

| Reference | When to Read | Content |
|-----------|--------------|---------|
| `references/methodology.md` | Phase 1 | Google Design Docs, arc42, C4 Model, ADRs overview |
| `references/domain-modeling.md` | Phase 3 | Entity extraction, aggregate boundaries, DDD patterns |
| `references/clean-architecture.md` | Phase 4 | Layer definitions, dependency rule, interface design |
| `references/data-api-extraction.md` | Phase 1 (when data models or API specs provided) | Extracting from SQL/ORM schemas, OpenAPI/GraphQL/gRPC specs, reconciliation |

**Output Templates:**

| Template | When to Read | Content |
|----------|--------------|---------|
| `templates/design-doc-template.md` | Workflow 1 output | Google Design Doc structure |
| `templates/architecture-doc-template.md` | Workflow 2 output | Full architecture document structure |
| `templates/hybrid-template.md` | Workflow 3 output | Combined design + architecture structure |

**Loading pattern:** Read references BEFORE corresponding phases. Read templates WHEN generating output files.
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| create-design-doc.md | Lightweight decision-focused document (Goals, Non-Goals, Alternatives, Decisions) |
| create-architecture-doc.md | Comprehensive architecture document (Domain Model, Layers, Interfaces, Quality) |
| create-hybrid-doc.md | Combined document with both decision context and architecture structure |
</workflows_index>

<success_criteria>
Architecture documentation is complete when:
- [ ] All input files loaded and validated
- [ ] Document type selected by user
- [ ] Domain model extracted (entities, value objects, aggregates)
- [ ] Architecture layers defined (Clean Architecture pattern)
- [ ] Key interfaces documented (repository, use case boundaries)
- [ ] C4 diagrams created (at minimum: Context + Container)
- [ ] Goals and Non-Goals explicitly stated
- [ ] Quality attributes mapped to architecture decisions
- [ ] Traceability maintained (requirements → architecture elements)
- [ ] Output file written to appropriate location
- [ ] User asked if they want to proceed to execution planning
</success_criteria>
