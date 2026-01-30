# Deep Dive: Requirements Engineering Methodology

## Strategic Summary

Requirements engineering is a structured discipline for transforming business intent into formal, traceable system specifications. The key frameworks — BABOK (elicitation and lifecycle), ISO/IEC 25010 (quality classification), and prioritization models (MoSCoW, Kano) — provide complementary lenses that, when combined, enable an AI skill to systematically extract, classify, prioritize, and trace requirements from business documents. The critical insight for our `/create-requirements` skill: **document analysis is the primary elicitation technique** (since the skill reads files, not interviews stakeholders), augmented by interactive clarification questions that mirror the stakeholder elicitation patterns from BABOK.

## Key Questions
- How does BABOK structure the requirements lifecycle from elicitation to validation?
- What requirement types exist and how should they be classified?
- How does ISO/IEC 25010 organize non-functional requirements systematically?
- How should document analysis extract requirements from existing documents?
- What prioritization frameworks best suit an interactive AI skill?
- How should requirements be traced back to their sources?

---

## Overview

Requirements engineering sits at the intersection of business analysis and systems engineering. It's the discipline of discovering, documenting, and managing the requirements of a system. The profession has mature frameworks (BABOK from IIBA, ISO standards, IEEE guidelines) that encode decades of practitioner experience.

For our purpose — building an AI skill that reads business documents and produces formal requirements — we need to encode three capabilities: (1) **extraction** (pulling requirements from unstructured text using document analysis techniques), (2) **classification** (organizing into the right taxonomy — functional, non-functional, by stakeholder), and (3) **prioritization** (helping the user decide what's MVP vs. future). The traceability layer ties it all together, ensuring every requirement traces back to a business need.

The BABOK Guide v3 (Business Analysis Body of Knowledge) is the most comprehensive reference, defining six knowledge areas with 30+ techniques. ISO/IEC 25010:2023 provides the definitive taxonomy for quality (non-functional) requirements. MoSCoW and Kano provide complementary prioritization lenses — MoSCoW for binary scope decisions, Kano for understanding satisfaction dynamics.

---

## How It Works

### BABOK Requirements Classification Schema

BABOK defines four requirement types in a hierarchy:

```
Business Requirements (WHY — enterprise-level goals)
    └── Stakeholder Requirements (WHAT — what users need)
        └── Solution Requirements (HOW — system behavior)
            ├── Functional Requirements (what the system does)
            └── Non-Functional Requirements (how well it does it)
    └── Transition Requirements (temporary migration needs)
```

**Business Requirements** define the "why" — the enterprise-level objectives. Example: "Agency needs to find matching influencers within 24 hours of a brand request."

**Stakeholder Requirements** bridge business and solution — what specific actors need. Example: "Account managers need to filter influencers by niche and location."

**Solution Requirements** define system behavior:
- **Functional**: "System shall display influencer profiles with engagement metrics."
- **Non-Functional**: "Search results shall load within 2 seconds for up to 10,000 records."

**Transition Requirements** are temporary: "Existing CSV data shall be importable into the new system."

### BABOK Six Knowledge Areas

1. **Business Analysis Planning & Monitoring** — How to plan BA activities
2. **Elicitation & Collaboration** — Gathering requirements (5 tasks)
3. **Requirements Life Cycle Management** — Trace, maintain, prioritize, approve
4. **Strategy Analysis** — Current/future state, risk assessment
5. **Requirements Analysis & Design Definition** — Model, verify, validate, architect
6. **Solution Evaluation** — Assess solution performance

### Elicitation Techniques (Chapter 4)

BABOK defines multiple elicitation techniques. For an AI skill reading documents:

| Technique | Applicability to AI Skill |
|-----------|--------------------------|
| **Document Analysis** | PRIMARY — reading existing docs |
| **Interviews** | Simulated via interactive questions |
| **Brainstorming** | Not applicable (single user) |
| **Workshops** | Not applicable |
| **Prototyping** | Not applicable |
| **Surveys/Questionnaires** | Simulated via structured questions |
| **Observation** | Not applicable |

### Requirements Analysis & Design Definition (Chapter 7)

Six tasks for analyzing requirements:

1. **Specify and Model Requirements** — Describe requirements using text, diagrams, matrices
2. **Verify Requirements** — Ensure they are correct, complete, consistent
3. **Validate Requirements** — Ensure they deliver business value
4. **Define Requirements Architecture** — Structure requirements for cohesion
5. **Define Design Options** — Propose solution approaches
6. **Analyze Potential Value** — Recommend solution

Key techniques for specification:
- Data Modeling (entities, attributes, relationships)
- Process Modeling (workflows, activities, decisions)
- Use Cases & Scenarios (actor-system interactions)
- User Stories (As a... I want... So that...)
- Business Rules Analysis (constraints, conditions)
- Non-Functional Requirements Analysis (quality attributes)

### Requirements Lifecycle Management (Chapter 5)

Five tasks for managing requirements over time:

1. **Trace Requirements** — Link requirements to sources and deliverables
2. **Maintain Requirements** — Keep accurate and current
3. **Prioritize Requirements** — Rank by importance and urgency
4. **Assess Requirements Changes** — Evaluate proposed modifications
5. **Approve Requirements** — Get stakeholder sign-off

---

## ISO/IEC 25010:2023 — Quality Requirements Classification

### Product Quality Model (9 Characteristics)

The 2023 update defines nine quality characteristics (up from eight in 2011):

| # | Characteristic | Sub-characteristics | Relevance |
|---|---|---|---|
| 1 | **Functional Suitability** | Completeness, Correctness, Appropriateness | Core functional |
| 2 | **Performance Efficiency** | Time behavior, Resource utilization, Capacity | Load/speed NFRs |
| 3 | **Compatibility** | Co-existence, Interoperability | Integration NFRs |
| 4 | **Interaction Capability** | Recognizability, Learnability, Operability, User Error Protection, User Engagement, Self-descriptiveness, Inclusivity, Accessibility | UX NFRs |
| 5 | **Reliability** | Faultlessness, Availability, Fault Tolerance, Recoverability | Uptime NFRs |
| 6 | **Security** | Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity, Resistance | Security NFRs |
| 7 | **Maintainability** | Modularity, Reusability, Analysability, Modifiability, Testability | Code quality NFRs |
| 8 | **Flexibility** | Adaptability, Scalability, Installability, Replaceability | Deployment NFRs |
| 9 | **Safety** | Operational Constraint, Risk Identification, Fail Safe, Hazard Warning, Safe Integration | Safety-critical NFRs |

### Quality in Use Model (5 Characteristics)

| # | Characteristic | Description |
|---|---|---|
| 1 | **Effectiveness** | Accuracy and completeness of goal achievement |
| 2 | **Efficiency** | Resources expended in relation to results |
| 3 | **Satisfaction** | Usefulness, Trust, Pleasure, Comfort |
| 4 | **Freedom from Risk** | Economic, health/safety, environmental risk mitigation |
| 5 | **Context Coverage** | Completeness, Flexibility across contexts |

### Key Changes from 2011 to 2023

- "Usability" → "Interaction Capability" (broader scope, includes inclusivity)
- "Portability" → "Flexibility" (includes scalability)
- New: "Safety" characteristic added
- "User Interface Aesthetics" → "User Engagement"
- New sub-characteristics: Self-descriptiveness, Inclusivity, Resistance, Scalability

### Application to Requirements Classification

The ISO 25010 model serves as a **checklist** for non-functional requirements. For each characteristic, ask: "Does this system have requirements in this area?" This prevents missing entire categories of quality requirements.

For the Boom influencer system, the most relevant characteristics are:
- **Performance Efficiency** (search speed, API response times)
- **Interaction Capability** (dashboard usability, learnability)
- **Reliability** (data accuracy, system availability)
- **Security** (API key protection, data privacy)
- **Maintainability** (clean architecture, testability)
- **Flexibility** (scalability to more platforms, adaptability)

---

## Document Analysis as Elicitation

### The Technique

Document analysis is the systematic review of existing documentation to extract requirements. BABOK lists it as a primary elicitation technique (10.14). It's particularly valuable when:
- Subject matter experts are unavailable
- The domain has existing documentation
- Cross-checking requirements from other sources
- Preparing for stakeholder interviews

### Process for AI-Driven Document Analysis

For our skill, document analysis maps to a structured extraction pipeline:

```
1. RECEIVE document (business case, research, brief)
2. IDENTIFY document type and structure
3. EXTRACT entities (nouns → domain objects)
4. EXTRACT actions (verbs → functional requirements)
5. EXTRACT constraints (adjectives, conditions → NFRs, business rules)
6. EXTRACT actors (people, roles → stakeholders)
7. EXTRACT workflows (sequences → use cases)
8. MAP relationships (entity-to-entity, actor-to-workflow)
9. CLASSIFY into requirement types (business, stakeholder, solution)
10. IDENTIFY gaps (what's implied but not stated)
```

### What to Extract from Different Document Types

| Document Type | Extract | Maps To |
|---|---|---|
| Business Case | Goals, KPIs, constraints | Business Requirements |
| Research Report | Domain entities, workflows, market rules | Stakeholder + Solution Reqs |
| Client Brief | Features, user needs, timeline | Stakeholder Requirements |
| Technical Spec | System behaviors, integrations | Solution Requirements |
| Meeting Notes | Decisions, preferences, priorities | Priority metadata |

### Linguistic Patterns for Extraction

- **"The system shall..."** → Explicit functional requirement
- **"Users need to..."** → Stakeholder requirement
- **"Within X seconds/minutes"** → Performance NFR
- **"Must handle N concurrent..."** → Capacity NFR
- **"Securely store/transmit"** → Security NFR
- **"Available 24/7"** → Reliability NFR
- **"Easy to use/intuitive"** → Interaction Capability NFR
- **"Currently they do X, which causes Y"** → Problem → implied requirement
- **"Ideally/nice to have/eventually"** → Low priority / v2 candidate

---

## Prioritization Frameworks

### MoSCoW Method

Origin: Dai Clegg at Oracle, adopted by DSDM (Dynamic Systems Development Method).

| Category | Meaning | Criteria | Budget Rule |
|---|---|---|---|
| **Must** | Critical for delivery | Project fails without it | ≤60% of effort |
| **Should** | Important but not critical | High priority, not time-sensitive | ~20% of effort |
| **Could** | Desirable if resources allow | Nice-to-have, no failure impact | ~20% of effort |
| **Won't** | Not this time | Agreed out-of-scope for now | 0% |

**Strengths for our skill:**
- Simple, universally understood
- Clear binary: in-scope (M+S+C) vs. out-of-scope (W)
- DSDM's 60% rule prevents scope creep
- Maps directly to MVP (Must) vs. v2 (Should+Could)

**Limitations:**
- No ranking within categories
- No objective criteria for which category
- Won't ≠ Never (ambiguity about future)

**How to use in the skill:**
- Present extracted requirements to user grouped by inferred priority
- Ask user to confirm/adjust MoSCoW categories
- Apply 60% rule: if Must-haves exceed 60% of scope, flag for reduction

### Kano Model

Origin: Professor Noriaki Kano, 1984. Maps features to customer satisfaction dynamics.

| Category | If Present | If Absent | Lifecycle |
|---|---|---|---|
| **Must-Be** (Basic) | No extra satisfaction | High dissatisfaction | Stable baseline |
| **Performance** (One-Dimensional) | Proportional satisfaction | Proportional dissatisfaction | Competitive differentiator |
| **Attractive** (Delighters) | Disproportionate delight | No dissatisfaction | Becomes Must-Be over time |
| **Indifferent** | No impact | No impact | Skip or deprioritize |
| **Reverse** | Dissatisfaction | Satisfaction | Remove if present |

**Strengths for our skill:**
- Captures satisfaction dynamics MoSCoW misses
- Identifies delighters (competitive advantage)
- Reveals requirements that seem important but are actually indifferent
- The "becomes Must-Be over time" insight informs v2 planning

**Mapping Kano to MoSCoW:**
- Must-Be → Must Have (table stakes)
- Performance → Should Have (competitive features)
- Attractive → Could Have (differentiators)
- Indifferent → Won't Have (don't build)
- Reverse → Explicitly avoid

**How to use in the skill:**
- After MoSCoW classification, apply Kano lens to validate
- Ask: "If this feature were missing, would users be dissatisfied?" (Must-Be test)
- Ask: "Would this feature surprise and delight users?" (Attractive test)

### Value vs. Effort Matrix

A 2x2 prioritization tool:

```
         High Value
             │
   Quick     │    Big Bets
   Wins      │    (strategic)
─────────────┼──────────────
   Fill-Ins  │    Money Pit
   (if time) │    (avoid)
             │
         Low Value
    Low Effort ──── High Effort
```

**Strengths for our skill:**
- Practical for sprint planning
- Identifies quick wins (high value, low effort)
- Warns about money pits (low value, high effort)

**How to use in the skill:**
- After requirements are classified and prioritized, optionally ask user to estimate effort
- Plot on matrix to identify implementation order
- Quick wins first, then big bets, then fill-ins, avoid money pits

### Weighted Scoring

For more complex decisions, assign weights to criteria and score each requirement:

```
Score = Σ (Weight_i × Score_i) for each criterion

Example criteria:
- Business value (weight: 5)
- User impact (weight: 4)
- Technical risk (weight: 3)
- Implementation effort (weight: -2)  ← negative = penalizes high effort
```

**When to use:** Large requirement sets (50+) where simple MoSCoW doesn't provide enough differentiation.

### Recommended Approach for the Skill

Layer the techniques:

1. **First pass: MoSCoW** — Binary scope decisions (in/out for this release)
2. **Second pass: Kano validation** — Verify Must-Be vs. Attractive classification
3. **Optional: Value vs. Effort** — Implementation ordering within "in-scope" requirements
4. **For large sets: Weighted scoring** — Only if >50 requirements need ranking

---

## Traceability Patterns

### Requirements Traceability Matrix (RTM)

A traceability matrix maps requirements across lifecycle stages:

```
Source (Business Need) → Requirement ID → Design → Implementation → Test
```

### Four Types of Traceability

1. **Forward Traceability** — Source → Requirement → Implementation → Test
   - Ensures nothing is missed in implementation
   - "Every requirement gets built and tested"

2. **Backward Traceability** — Test → Implementation → Requirement → Source
   - Ensures nothing extra is built
   - "Every feature traces back to a real need"

3. **Bidirectional Traceability** — Both directions simultaneously
   - Complete coverage verification
   - "Nothing missing AND nothing extra"

4. **Horizontal Traceability** — Across teams/systems at the same level
   - Cross-functional alignment
   - "Frontend and backend requirements align"

### Traceability for the Skill

The skill should produce requirements with explicit source tracing:

```markdown
- [ ] **DISC-01**: Discover influencers by hashtag search
  - Source: research/influencer-marketing-ops.md (Section: Discovery Workflow)
  - Stakeholder: Account Manager
  - Validates: BIZ-01 (Find matching influencers within 24 hours)
```

This pattern enables:
- **Backward trace**: Why does this requirement exist? → Source document, section
- **Forward trace**: What implements this? → (filled in during planning/execution)
- **Stakeholder trace**: Who needs this? → Actor identification

### Minimal Traceability for AI-Generated Requirements

For our skill, each requirement should carry:
1. **Source reference** — Which document/section it came from
2. **Stakeholder** — Who benefits from this requirement
3. **Parent requirement** — Which business requirement it supports (hierarchy)
4. **Priority rationale** — Why it's Must/Should/Could

---

## Patterns & Best Practices

### 1. The Requirements Pyramid
Structure requirements hierarchically: Business → Stakeholder → Solution (Functional + Non-Functional) → Transition. Fewer at the top (3-5 business requirements), more at the bottom (potentially hundreds of solution requirements).

### 2. Verification vs. Validation
- **Verify**: "Are we building the thing right?" (correct, complete, consistent, unambiguous)
- **Validate**: "Are we building the right thing?" (delivers business value)
The skill should verify (quality check) before outputting, and ask the user to validate (confirm business relevance).

### 3. SMART Requirements
Each requirement should be: **S**pecific, **M**easurable, **A**chievable, **R**elevant, **T**ime-bound (where applicable). Non-functional requirements especially need measurable criteria.

### 4. Requirement Quality Checklist
- Atomic (one requirement per statement)
- Complete (contains all necessary information)
- Consistent (no contradictions with other requirements)
- Feasible (technically achievable)
- Necessary (traces back to a business need)
- Prioritized (has a MoSCoW or equivalent ranking)
- Testable (can be verified when implemented)
- Unambiguous (only one interpretation)

### 5. ID Naming Convention
Use category prefixes with sequential numbering:
- `BIZ-01`, `BIZ-02` — Business requirements
- `FOUND-01`, `DISC-01`, `ENRICH-01` — Domain-specific categories
- `NFR-PERF-01`, `NFR-SEC-01` — Non-functional by ISO characteristic
- `TRANS-01` — Transition requirements

### 6. Grouping Strategy
Group requirements by business capability or workflow phase, not by technical layer. This keeps them understandable to stakeholders who think in terms of "what the system does" not "how it's built."

### 7. Source Document Completeness Verification

After generating requirements from business requirements, verify completeness
against all source documents:

**The Completeness Triangle:**
```
BR-XX (top-down: what the business says it needs)
    +
Data Model (bottom-up: what fields the system must store)
    +
Stakeholder Needs (lateral: what each actor needs to do)
    =
Complete requirement set
```

A common failure mode: generating requirements only from BR-XX text and missing
fields/behaviors that are in the source data model but not explicitly stated in
any BR. This happens because BRs are intentionally abstract ("collect profile
data") while data models are intentionally specific ("43 fields with types and
validation rules").

**Verification procedure:**
1. Map every data model field to an FR (storage, collection, or derivation)
2. Map every stakeholder need to at least one FR or UI requirement
3. Identify implied requirements from system behavior (deduplication, ordering,
   timestamps, defaults)

---

## Limitations & Edge Cases

### Document Analysis Limitations
- **Only captures as-is**: Documents describe current state; future needs require inference
- **Implicit requirements**: Many requirements are "obvious" to domain experts but unstated
- **Conflicting sources**: Different documents may contradict each other
- **Stale information**: Documents may be outdated
- **Mitigation**: Always ask clarifying questions; never assume completeness from documents alone

### Prioritization Limitations
- **MoSCoW ambiguity**: No objective criteria for Must vs. Should boundary
- **Kano requires users**: True Kano analysis needs questionnaire responses
- **Stakeholder bias**: Different stakeholders prioritize differently
- **Mitigation**: Use multiple frameworks as cross-checks; make priority rationale explicit

### Classification Limitations
- **Functional/Non-Functional boundary**: Some requirements blur the line (e.g., "search shall be fast" — is "search" functional and "fast" non-functional?)
- **Granularity mismatch**: Too fine-grained = noise; too coarse = ambiguous
- **ISO 25010 overkill**: For small projects, checking all 9 characteristics may be excessive
- **Mitigation**: For small/medium projects, focus on Performance, Reliability, Security, Maintainability; expand for larger projects

### Traceability Overhead
- **Cost vs. value**: Full bidirectional traceability is expensive to maintain
- **Staleness risk**: Traces become incorrect as requirements evolve
- **Mitigation**: For our skill, embed source references in requirement text rather than maintaining a separate matrix

---

## Current State & Trends

### Industry Trends (2024-2026)
- **AI-assisted requirements engineering**: LLMs being explored for requirement extraction, but hallucination risk means human validation is essential
- **Continuous requirements**: Agile/DevOps blurs the line between requirements and backlog items
- **Living documentation**: Requirements as code (e.g., Gherkin/BDD), version-controlled alongside implementation
- **Shift from documents to models**: Domain-driven design and event storming replacing traditional requirement docs
- **ISO 25010:2023 adoption**: New Safety and Interaction Capability characteristics gaining traction

### Relevance to Our Skill
- The skill should produce **living documents** (Markdown with checkboxes, suitable for version control)
- Requirements should be **atomic and testable** (ready for implementation)
- The classification should use **ISO 25010 as a checklist** (not an exhaustive taxonomy)
- Prioritization should be **interactive** (the AI suggests, the human decides)

---

## Key Takeaways

1. **BABOK's requirement pyramid (Business → Stakeholder → Solution) is the right structure** for the skill's output. Start with business objectives, derive stakeholder needs, then specify solution requirements.

2. **Document analysis + interactive clarification is the right elicitation model** for an AI skill. Extract what's in the document, then ask targeted questions about gaps (scope, priority, constraints).

3. **ISO 25010:2023's nine characteristics serve as a non-functional requirements checklist**, not a rigid taxonomy. For each characteristic, the skill should ask: "Does this system have requirements here?" and only elaborate where relevant.

4. **Layer prioritization: MoSCoW first (scope), Kano second (validation), Value vs. Effort third (ordering)**. This gives the user clear scope decisions, validates against satisfaction dynamics, then sequences implementation.

5. **Minimal traceability embedded in requirement text** (source reference, stakeholder, parent requirement) is more maintainable than a separate matrix for our use case.

6. **Quality attributes for each requirement**: Atomic, Testable, Traceable, Prioritized. The skill should verify these before outputting.

---

## Remaining Unknowns

- [ ] How much interactive questioning is ideal? (Too many questions = friction; too few = assumptions)
- [ ] Should the skill attempt Kano classification automatically from document language, or always ask?
- [ ] How to handle conflicting information across multiple input documents?
- [ ] Optimal granularity: how many requirements per page of source document is typical?
- [ ] Should transition requirements be generated, or are they always project-specific?

---

## Implementation Context

<claude_context>
<application>
- when_to_use: When transforming business documents (research, business cases, briefs) into formal requirements specifications
- when_not_to_use: When requirements already exist and need editing, or when doing pure technical planning (use /create-technical-plan instead)
- prerequisites: At least one input document describing business intent (research doc, business case, or client brief)
</application>
<technical>
- methodology: BABOK v3 (elicitation, lifecycle, analysis) + ISO 25010:2023 (quality classification) + MoSCoW/Kano (prioritization)
- extraction_pipeline: Read → Identify entities/actions/constraints/actors/workflows → Classify → Prioritize → Trace
- output_format: Markdown with checkbox format, categorized IDs, v1/v2 sections, source traceability
- quality_checks: Atomic, Testable, Traceable, Prioritized, Unambiguous
</technical>
<integration>
- works_with: /create-business-case (produces input), /create-technical-plan (consumes output), /execute-phase (implements requirements)
- conflicts_with: Requirements generated without source documents (hallucination risk)
- alternatives: Traditional BA workshops (not AI-compatible), Gherkin/BDD specs (too technical for business stakeholders)
</integration>
</claude_context>

---

## Methodology Encoding Guide (for Skill Implementation)

### The Skill's Core Algorithm

```
PHASE 1: INTAKE
  1. Read input document(s)
  2. Identify document type (business case, research, brief, mixed)
  3. Extract document structure (sections, headings, key themes)

PHASE 2: DOMAIN EXTRACTION
  4. Extract entities (nouns → domain objects)
  5. Extract actions (verbs → functional behaviors)
  6. Extract constraints (conditions, limits → business rules + NFRs)
  7. Extract actors (roles, people → stakeholders)
  8. Extract workflows (sequences, processes → use cases)

PHASE 3: INTERACTIVE CLARIFICATION
  9. Present extracted domain model to user
  10. Ask scope questions: "Which workflows are in scope?"
  11. Ask priority questions: "What's MVP vs. v2?"
  12. Ask constraint questions: "Budget, timeline, team size?"
  13. Ask NFR questions (ISO 25010 checklist): "Any performance/security/reliability targets?"

PHASE 4: REQUIREMENT CLASSIFICATION
  14. Derive business requirements from goals/KPIs
  15. Derive stakeholder requirements from actor-workflow pairs
  16. Derive functional requirements from in-scope workflows
  17. Derive non-functional requirements from ISO 25010 checklist + constraints
  18. Identify transition requirements (migration, training)

PHASE 5: PRIORITIZATION
  19. Apply MoSCoW based on user's scope answers
  20. Validate with Kano lens (Must-Be vs. Attractive)
  21. Flag if Must-haves exceed 60% of scope

PHASE 6: QUALITY & OUTPUT
  22. Verify each requirement: Atomic? Testable? Traceable? Unambiguous?
  23. Assign IDs with category prefixes
  24. Add source references (document + section)
  25. Generate REQUIREMENTS.md with v1 and v2 sections
```

### Interactive Question Templates

**Scope clarification:**
- "I've identified these workflows in the document: [list]. Which are in scope for this system?"
- "These actors appear: [list]. Who are the primary users?"

**Priority clarification:**
- "Here are the core capabilities I extracted. Which are absolutely essential for launch?"
- "These features seem like nice-to-haves. Should any move to MVP?"

**NFR clarification (ISO 25010 checklist):**
- "Any performance targets? (e.g., response time, concurrent users)"
- "Any security requirements beyond standard best practices?"
- "Availability expectations? (e.g., 99.9% uptime, or internal-tool-grade)"
- "Scale expectations? (e.g., 100 records, 10,000, or 1M+)"

---

## Sources
- [BABOK v3: Requirements Life Cycle Management](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/5-requirements-life-cycle-management/)
- [BABOK v3: Elicitation and Collaboration](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/4-elicitation-and-collaboration/)
- [BABOK v3: Requirements Analysis and Design Definition](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/7-requirements-analysis-and-design-definition/)
- [BABOK v3: Requirements Classification Schema](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/2-business-analysis-key-concepts/2-3-requirements-classification-schema/)
- [BABOK v3: Non-Functional Requirements Analysis](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/10-techniques/10-30-non-functional-requirements-analysis/)
- [ISO/IEC 25010:2023 - Product Quality Model](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)
- [ISO/IEC 25010:2023 Update - arc42](https://quality.arc42.org/articles/iso-25010-update-2023)
- [What Is ISO 25010? - Perforce](https://www.perforce.com/blog/qac/what-is-iso-25010)
- [MoSCoW Method - Wikipedia](https://en.wikipedia.org/wiki/MoSCoW_method)
- [MoSCoW Prioritization - DSDM/Agile Business Consortium](https://www.agilebusiness.org/dsdm-project-framework/moscow-prioririsation.html)
- [Kano Model - Wikipedia](https://en.wikipedia.org/wiki/Kano_model)
- [Understanding the Kano Model: Complete 2026 Guide - Edstellar](https://www.edstellar.com/blog/kano-model)
- [The Complete Guide to the Kano Model - Folding Burritos](https://foldingburritos.com/blog/kano-model/)
- [Value vs. Effort Matrix - Highberg](https://highberg.com/insights/value-vs-effort-matrix-lean-approach)
- [Requirements Traceability Matrix - Perforce](https://www.perforce.com/resources/alm/requirements-traceability-matrix)
- [Four Types of Requirements Traceability - Security Compass](https://www.securitycompass.com/blog/four-types-of-requirements-traceability/)
- [Document Analysis - Modern Analyst](https://www.modernanalyst.com/Careers/InterviewQuestions/tabid/128/ID/1610/What-is-Document-Analysis.aspx)
- [Elicitation Techniques for Business Analysts - Bridging the Gap](https://www.bridging-the-gap.com/elicitation-techniques-business-analysts/)
- [A Guide to Non-Functional Requirements for Software Architects](https://www.workingsoftware.dev/the-ultimate-guide-to-write-non-functional-requirements/)
- [Weighted Scoring Prioritization - SixSigma.us](https://www.6sigma.us/six-sigma-in-focus/weighted-scoring-prioritization/)
