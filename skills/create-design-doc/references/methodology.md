<overview>
This reference covers architecture documentation methodologies: Google Design Docs, C4 Model, arc42, and Architecture Decision Records (ADRs). These can be combined into a pragmatic approach for Agile teams.
</overview>

<google_design_docs>

**Purpose:** Decision-focused documents written BEFORE implementation.

**Core Sections:**

| Section | Purpose |
|---------|---------|
| **Context & Scope** | Background, what's being built |
| **Goals & Non-Goals** | What we're solving; what we're NOT |
| **Design Overview** | High-level approach, system context |
| **Detailed Design** | Trade-offs (not implementation details) |
| **Alternatives Considered** | Other designs evaluated, why rejected |
| **Cross-Cutting Concerns** | Security, privacy, monitoring |

**Key Characteristics:**
- 10-20 pages for larger projects; 1-3 for features
- Plain language, not UML-heavy
- Focuses on **trade-offs** over specification
- Living document, updated as design evolves

**Goals & Non-Goals Pattern:**

Goals state what you're building. Non-Goals explicitly state what you're NOT building—this prevents scope creep.

```markdown
## Goals
- Support up to 10,000 records
- Enable filtering by multiple criteria
- Provide export functionality

## Non-Goals (Explicitly Out of Scope)
- Real-time sync (batch updates sufficient)
- Advanced analytics (basic reporting only)
- Multi-tenant architecture (single tenant for MVP)
```

</google_design_docs>

<c4_model>

**Purpose:** Visual architecture communication at 4 zoom levels.

**Levels:**

| Level | Shows | When to Use |
|-------|-------|-------------|
| 1: System Context | How system fits in the world | Always |
| 2: Container | Major technical building blocks | Always |
| 3: Component | What's inside each container | Sometimes |
| 4: Code | Class diagrams | Rarely (code is truth) |

**Level 1 Example (Mermaid):**
```mermaid
graph TB
    User[User] --> System[System Name]
    System --> ExternalAPI[External API]
    System --> DB[(Database)]
```

**Level 2 Example (Mermaid):**
```mermaid
graph TB
    subgraph System["System Boundary"]
        UI[Web UI]
        API[API Server]
        DB[(Database)]
    end
    User --> UI
    UI --> API
    API --> DB
    API --> External[External Service]
```

**Best Practice:** Most projects need only Levels 1-2. Level 3 is optional; Level 4 rarely useful.

</c4_model>

<arc42>

**Purpose:** Structured template with 12 optional sections for comprehensive documentation.

**Sections (pick what you need):**

| # | Section | Include When |
|---|---------|--------------|
| 1 | Introduction & Goals | Always |
| 2 | Constraints | Technical/org limitations exist |
| 3 | Context & Scope | Always |
| 4 | Solution Strategy | Major decisions to capture |
| 5 | Building Block View | Complex decomposition |
| 6 | Runtime View | Complex interactions |
| 7 | Deployment View | Infrastructure matters |
| 8 | Crosscutting Concepts | Patterns across system |
| 9 | Architecture Decisions | Always (use ADRs) |
| 10 | Quality Requirements | NFRs drive architecture |
| 11 | Risks & Technical Debt | Known problems exist |
| 12 | Glossary | Domain terms need defining |

**When arc42 is overkill:** MVPs, small projects, tight deadlines. Use Google Design Doc instead.

</arc42>

<adrs>

**Purpose:** Capture single decisions with rationale. Immutable—new info is appended.

**Michael Nygard Format:**
```markdown
# ADR NNN: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the situation? What forces are at play?]

## Decision
[What is the change being made?]

## Consequences
[What becomes easier? What becomes harder?]
```

**MADR Format (more detailed):**
Adds "Considered Options" and "Pros/Cons" sections.

**Best Practices:**
- One decision per ADR
- Store in repository: `docs/adr/adr-NNN.md`
- Keep to 1-2 pages
- Never delete—mark as superseded

</adrs>

<recommended_approach>

**For most Agile projects, combine:**

1. **Google Design Doc structure** for the narrative
2. **C4 diagrams** (Level 1 + Level 2) for visualization
3. **ADRs** for key decisions

**Directory structure:**
```
docs/
├── DESIGN-DOC.md       # Main document
├── diagrams/
│   ├── context.mmd     # C4 Level 1
│   └── containers.mmd  # C4 Level 2
└── adr/
    ├── 0001-decision.md
    └── 0002-decision.md
```

**Core principle:** Document what you can't get from code—context, decisions, trade-offs.

</recommended_approach>
