# Workflow: Create Hybrid Document (Design + Architecture)

<required_reading>
**Read these reference files NOW:**
1. references/methodology.md — Google Design Docs + C4 + ADRs
2. references/domain-modeling.md — Entity extraction, aggregates
3. references/clean-architecture.md — Layer definitions, dependency rule
4. templates/hybrid-template.md — Output template to fill
</required_reading>

<context>
A Hybrid Document combines the **decision focus** of a Design Document with the **structural depth** of an Architecture Document. This is the **recommended format** for most projects because it provides:
- Context and rationale (why)
- Structure and interfaces (what)
- Decision records (how we got here)

It is a single document that tells the complete architectural story.
</context>

<process>

## Phase 1: Analyze Input Files

Follow the same analysis as both workflows:

1. Read all provided input files thoroughly
2. Extract:
   - **Actors** — From "As a [role]" patterns in user stories
   - **Capabilities** — From "I want to" patterns and functional requirements
   - **Constraints** — From non-functional requirements and business case
   - **Entities** — Nouns that have identity and lifecycle
   - **Quality Attributes** — Performance, security, scalability requirements

Create a structured extraction document before proceeding.

## Phase 2: Goals and Non-Goals (Design Doc Section)

**The most important section for decision context.**

1. Draft 3-7 **Goals**:
   - Concrete, verifiable capabilities
   - Active voice: "Support X", "Enable Y"
   - Derived from requirements and user stories

2. Draft 3-5 **Non-Goals**:
   - Explicit exclusions with rationale
   - Prevents scope creep
   - Sets expectations clearly

## Phase 3: Context and Overview

### 3.1 System Context (C4 Level 1)

Create a diagram showing:
- The system being built
- Users/actors
- External systems

### 3.2 Background Narrative

Write 2-3 paragraphs:
- What is this system?
- What problem does it solve?
- Who are the key stakeholders?

## Phase 4: Domain Model (Architecture Section)

### 4.1 Entities

| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| [Entity] | [Purpose] | [Attributes] |

### 4.2 Value Objects

Immutable domain concepts with validation.

### 4.3 Aggregates

Entity clusters with consistency boundaries. Identify:
- Aggregate roots
- Nested entities
- Embedded value objects

### 4.4 Domain Services

Operations spanning multiple aggregates.

## Phase 5: Architecture Layers (Architecture Section)

### 5.1 Layer Diagram (C4 Level 2)

Create a Container diagram showing:
- Domain Layer (innermost)
- Application Layer (use cases)
- Adapters Layer (infrastructure)

### 5.2 Layer Definitions

For each layer, document:
- What it contains
- What it depends on
- Key responsibilities

### 5.3 Dependency Rule

Diagram showing dependencies point INWARD only.

## Phase 6: Key Interfaces (Architecture Section)

### 6.1 Repository Interfaces

For each aggregate root:
```python
class EntityRepository(Protocol):
    def find_by_id(self, id: UUID) -> Entity | None: ...
    def save(self, entity: Entity) -> None: ...
```

### 6.2 Use Case Interfaces

For major operations:
```python
@dataclass
class UseCaseInput: ...

@dataclass
class UseCaseOutput: ...
```

## Phase 7: Alternatives Considered (Design Doc Section)

For 2-3 key architectural decisions:

1. What decision was made
2. What alternatives were considered
3. Why the chosen approach won

This becomes the seed for formal ADRs.

## Phase 8: Quality Attributes (Architecture Section)

| Attribute | Requirement | Architecture Decision |
|-----------|-------------|----------------------|
| Testability | [Target] | [How achieved] |
| Performance | [Target] | [How achieved] |
| Modifiability | [Target] | [How achieved] |

## Phase 9: Cross-Cutting Concerns (Design Doc Section)

Address briefly:
- Security
- Error handling
- Logging/monitoring
- Data validation

## Phase 10: Constraints and Risks

**Constraints:**
- Technical (platform, language, APIs)
- Organizational (team, timeline, budget)
- External (regulations, third-party limits)

**Risks:**
- Architectural risks with mitigation strategies
- Technical debt acknowledgment

## Phase 11: Architecture Decision Records

Create ADR stubs for key decisions:

```markdown
| ADR | Decision | Status |
|-----|----------|--------|
| 001 | [Major decision 1] | Proposed |
| 002 | [Major decision 2] | Proposed |
```

ADRs can be expanded into separate files later.

## Phase 12: Write Output

1. Read `templates/hybrid-template.md`
2. Fill in all sections from phases 2-11
3. Write to output location (same directory as primary input)
4. Filename: `DESIGN-DOC.md`

</process>

<success_criteria>
Hybrid Document is complete when:
- [ ] Goals and Non-Goals clearly defined
- [ ] System Context diagram shows environment
- [ ] Domain model has entities, value objects, aggregates
- [ ] Architecture layers defined with dependency rule
- [ ] Container diagram shows technical structure
- [ ] Repository interfaces documented
- [ ] Use case interfaces documented
- [ ] At least 2 alternatives considered documented
- [ ] Quality attributes mapped to decisions
- [ ] Constraints and risks acknowledged
- [ ] ADR stubs created for key decisions
- [ ] Document is comprehensive but focused (20-40 pages)
- [ ] Written to output location
</success_criteria>
