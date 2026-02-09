# Architecture Doc Skill Review

**Skill:** `create-design-docs` (Architecture Document route only)
**Date:** 2026-02-09
**Methodology:** Sub-agent review against ISO/IEC 42010, arc42, C4 Model, SEI Views and Beyond, IEEE 1471/42010, DDD strategic patterns, and Kruchten 4+1 — followed by independent critical evaluation of each finding.

---

## Executive Summary

The create-design-docs skill's architecture document workflow is a well-structured, pragmatic tool that produces comprehensive static architecture documentation from requirements artifacts. It covers domain modeling, clean architecture layering, interface definitions, C4 diagrams, quality attributes, constraints, and risks. However, it has one confirmed critical gap (missing deployment view), two important gaps (missing bounded context identification and cross-cutting concerns), and several theoretically valid but practically insignificant observations. The skill's methodology references (arc42, Google Design Docs, C4 Model) provide a strong foundation, but the workflow does not fully implement all the sections those methodologies recommend.

---

## Sub-Agent Findings with Reviewer Critique

### Finding 1: Missing Deployment View / Infrastructure Perspective

**Sub-agent assessment: CRITICAL**

**What is missing:** The workflow and template contain no deployment view, infrastructure topology, or operational perspective. The C4 diagrams stop at Level 2 (Container) and never reach Level 3 (Component in deployment context) or the C4 Deployment Diagram. There is no section for documenting how the system maps to infrastructure — servers, containers, cloud services, networks, or deployment environments.

**Why this is critical (sub-agent reasoning):** Architecture is not just about logical structure — it must also describe how software maps to hardware and infrastructure. Without a deployment view, the document cannot answer fundamental questions: How many instances run? Where does the database live? What are the network boundaries? How is the system scaled? These are not operational details — they are architectural decisions.

**Best practice recommendation:**
- C4 Model includes a Deployment Diagram as a first-class diagram type
- arc42 Section 7 (Deployment View) is mandatory in the standard template
- Kruchten 4+1 includes a Physical View specifically for deployment topology
- SEI Views and Beyond includes an Allocation viewtype for mapping software to hardware
- ISO/IEC 42010 requires viewpoints addressing all stakeholder concerns, and operations/deployment is a core concern

**Evidence from skill files:**
- The workflow (create-architecture-doc.md) Phase 5 generates C4 Level 1 (System Context) and Level 2 (Container) diagrams only
- The template (architecture-doc-template.md) Section 5 has C4 L1 and L2 but no deployment diagram section
- The methodology reference (methodology.md) lists arc42 Section 7 (Deployment View) as "include when infrastructure matters" but the workflow does not implement it
- No workflow phase addresses deployment topology, scaling strategy, or infrastructure mapping

---

**Verdict: AGREE**

**Reasoning:** This is a genuine critical gap. The sub-agent correctly identifies that the workflow produces a comprehensive logical architecture document but completely ignores the physical/deployment dimension. For a skill that targets "new systems, major refactors" (per SKILL.md routing), deployment topology is architecturally significant.

The C4 model — which the skill explicitly uses — includes deployment diagrams as a standard diagram type. The skill implements C4 L1 and L2 but skips the deployment diagram entirely. Similarly, the methodology reference (methodology.md) lists arc42 Section 7 (Deployment View) but the workflow does not implement it.

For the skill's stated audience (developers implementing a new system), not knowing the deployment topology means they cannot make informed decisions about:
- Service boundaries and network communication
- Data storage location and replication
- Scaling approach (horizontal vs. vertical)
- Environment separation (dev/staging/prod)

The deployment view need not specify exact cloud services (that belongs in ADRs) — it should show the logical deployment topology: "stateless web tier behind load balancer, with separate database tier and async worker pool" is architectural; "AWS ECS on Fargate with RDS Aurora" is a technology choice.

**Severity assessment: Confirmed as CRITICAL.** This is the most impactful gap identified.

---

### Finding 2: No Bounded Context Identification / Context Mapping

**Sub-agent assessment: CRITICAL**

**What is missing:** The workflow builds a single unified domain model (Phase 2) without any mechanism to identify bounded contexts or create a context map. The domain-modeling reference (domain-modeling.md) focuses exclusively on tactical DDD patterns (entities, value objects, aggregates) within a single bounded context, with no coverage of strategic DDD patterns (bounded contexts, context maps, anti-corruption layers).

**Why this is critical (sub-agent reasoning):** For systems with multiple subdomains, a single unified domain model is an anti-pattern. Different subdomains may use the same terms with different meanings (e.g., "Account" in billing vs. authentication). Without bounded context identification, the architecture document may prescribe a single model that conflates distinct concepts, leading to a Big Ball of Mud.

**Best practice recommendation:**
- DDD (Eric Evans) identifies bounded contexts and context maps as the most strategically important patterns
- The C4 model's System Context diagram implicitly identifies system boundaries but does not address internal context boundaries
- arc42 Section 3 (Context and Scope) addresses system boundary but arc42 does not prescribe internal context mapping

**Evidence from skill files:**
- The workflow (create-architecture-doc.md) Phase 2 creates a single domain model with no bounded context assessment
- The domain-modeling reference (domain-modeling.md) covers entities, value objects, aggregates, and repositories but not bounded contexts or context maps
- The methodology reference (methodology.md) does not mention bounded contexts or context mapping

---

**Verdict: PARTIALLY AGREE**

**Reasoning:** The sub-agent is correct that DDD strategic patterns are completely absent from the workflow. The domain-modeling reference covers only tactical patterns (entities, value objects, aggregates), and the workflow builds a single unified domain model with no assessment of whether multiple bounded contexts exist.

However, the severity is overstated. This is especially problematic when the system has multiple distinct subdomains — and the workflow provides no guidance to even recognize when this is the case. The skill could extract bounded context signals (it already identifies some) but never synthesizes them into an explicit context map.

**Severity assessment: Downgrade from CRITICAL to IMPORTANT.** It is a real gap that should be addressed, but for most projects where this skill would be used (single team, single system), it is unlikely to make the document "fundamentally deficient." For larger systems, it would become critical.

---

### Finding 3: No Runtime/Behavioral View (Only Static Structure)

**Sub-agent assessment: CRITICAL**

**What is missing:** The workflow focuses almost entirely on static structure (domain model, layers, interfaces). The only behavioral element is the data flow sequence diagram in the template (Section 6), but the workflow itself has no phase dedicated to documenting runtime behavior, interaction patterns, or dynamic views.

**Why this is critical (sub-agent reasoning):** Architecture is not just structure — it is also behavior. Without runtime views, the document cannot show how the system behaves during key scenarios: error handling flows, asynchronous processing, event propagation, state transitions, or complex multi-step interactions.

**Best practice recommendation:**
- Kruchten 4+1 includes a Process View for concurrency, synchronization, and runtime behavior
- arc42 Section 6 (Runtime View) documents important runtime scenarios
- SEI Views and Beyond includes a Component-and-Connector (C&C) viewtype specifically for runtime behavior
- ISO/IEC 42010 requires viewpoints that address all stakeholder concerns, and runtime behavior is a core concern

**Evidence from skill files:**
- The workflow (create-architecture-doc.md) has no phase for documenting runtime scenarios, event flows, or behavioral patterns
- The template (architecture-doc-template.md) has Section 6 "Data Flow" with a sequence diagram for one primary use case — this is a single example, not systematic runtime documentation
- The methodology reference (methodology.md) lists arc42 Section 6 (Runtime View) with "include when complex interactions exist" but the workflow does not implement this

---

**Verdict: PARTIALLY AGREE**

**Reasoning:** The sub-agent is correct that the workflow is structurally biased — the overwhelming emphasis is on static decomposition (domain model, layers, interfaces) with minimal attention to runtime behavior.

However:

1. **The template does include a behavioral element.** Section 6 of the template contains a "Data Flow" section with a sequence diagram showing request/response flow through Controller -> UseCase -> Repository -> Database. This is not nothing — it is a basic runtime view.

2. **The workflow's Phase 4 (Document Key Interfaces) implicitly captures behavioral contracts.** Use case input/output definitions describe what happens at runtime, even if they do not show the full interaction sequence.

3. **For the skill's target use case (AI-generated docs from requirements), the static-first approach is pragmatic.** Requirements artifacts (user stories, SRS) are primarily structured around functional capabilities and quality attributes. Detailed runtime scenarios typically emerge during detailed design, not at the architecture level.

That said, the gap is real in one important respect: the workflow provides no guidance on documenting asynchronous patterns, event-driven flows, or complex multi-step interactions that are common in modern systems.

**Severity assessment: Downgrade from CRITICAL to NICE-TO-HAVE for the template's stated scope.** The template already has a data flow section with a sequence diagram. For most projects this skill targets, this is adequate. For event-driven or heavily asynchronous systems, this would become important.

---

### Finding 4: No Explicit Stakeholder-Viewpoint Mapping

**Sub-agent assessment: CRITICAL**

**What is missing:** The workflow does not establish a formal mapping between stakeholders and their architectural concerns/viewpoints. While the template has a stakeholder table in Section 1, there is no workflow phase that uses stakeholder concerns to drive which architectural views are included or emphasized.

**Best practice recommendation:**
- ISO/IEC 42010 requires explicit identification of stakeholders, their concerns, and the viewpoints that address those concerns
- IEEE 1471 defines the architecture description as a collection of views, each governed by a viewpoint that frames stakeholder concerns
- SEI Views and Beyond recommends a stakeholder-view mapping table as the starting point

---

**Verdict: DISAGREE**

**Reasoning:** While technically correct per ISO/IEC 42010 and IEEE 1471, formal stakeholder-viewpoint mapping is an enterprise architecture practice inappropriate for this skill's agile, project-level context:

1. **The skill produces a fixed, well-chosen set of views.** The template covers: system context, domain model, architecture layers, key interfaces, data flow, quality attributes, constraints, architecture decisions, risks, and glossary. This is a pragmatically complete set for the target audience.

2. **Formal stakeholder-viewpoint mapping adds ceremony** that conflicts with the skill's pragmatic philosophy.

3. **The template already captures stakeholders** in Section 1 with Role and Concern columns. The fixed view set addresses concerns of developers, architects, project managers, and operations.

**Severity assessment: NOT A CRITICAL GAP.** Theoretical concern from formal standards that does not apply to the skill's context.

---

### Finding 5: Clean Architecture Prescribed Without Fit Assessment

**Sub-agent assessment: CRITICAL**

**What is missing:** The workflow mandates Clean Architecture (Phase 3: "Use Clean Architecture pattern") without any guidance on assessing whether Clean Architecture is appropriate. The clean-architecture reference includes a "When Clean Architecture Fits" section listing scenarios where it is overkill, but the workflow ignores this.

**Evidence from skill files:**
- The workflow Phase 3 states "Use Clean Architecture pattern:" with no conditional
- The clean-architecture reference has a "When Clean Architecture Fits" table showing scenarios where it should be skipped
- The success criteria require "Architecture layers clearly defined with dependency rule" — making Clean Architecture mandatory

---

**Verdict: PARTIALLY AGREE**

**Reasoning:** The observation is valid — the workflow unconditionally prescribes Clean Architecture, and the skill's own reference material acknowledges it is not always appropriate. However:

1. **The skill is routed to the Architecture Document path only when the user selects "comprehensive" documentation.** The SKILL.md routing states this option is "Best for: new systems, major refactors." These are exactly the scenarios where Clean Architecture is most appropriate.

2. **The routing context provides implicit fit assessment.** By the time a user reaches this workflow, they have self-selected into "comprehensive" — a reasonable proxy for sufficient complexity.

3. **That said, the sub-agent is right that there is no escape hatch.** Some systems within the "comprehensive" path may benefit from a different architectural pattern (event-driven, microservices, pipe-and-filter).

**Severity assessment: Downgrade from CRITICAL to NICE-TO-HAVE.** The routing mechanism provides implicit fit assessment. A brief conditional check would be good but its absence does not make the document fundamentally deficient.

---

### Finding 6: No Cross-Cutting Concerns Section

**Sub-agent assessment: CRITICAL**

**What is missing:** The workflow and template lack a dedicated section for cross-cutting concerns — patterns that span multiple components or layers. Examples: error handling strategy, logging/observability, authentication/authorization patterns, transaction management, configuration management.

**Best practice recommendation:**
- arc42 Section 8 (Crosscutting Concepts) is dedicated to patterns spanning multiple building blocks
- Google Design Docs include "Cross-Cutting Concerns" as a core section
- The methodology reference lists both but neither is implemented in the workflow

**Evidence from skill files:**
- The workflow has no phase for cross-cutting concerns
- The template has no "Cross-Cutting Concerns" section
- Quality attributes (Phase 6) partially address this by mapping NFRs to architecture decisions, but this is not the same as documenting cross-cutting implementation patterns

---

**Verdict: AGREE**

**Reasoning:** This is a genuine and important gap. The distinction between cross-cutting concerns and quality attributes is key:

- **Quality attributes** (Phase 6) answer: "What are our performance/security/scalability targets and which architectural decisions achieve them?"
- **Cross-cutting concerns** answer: "What consistent patterns do we use across the system for error handling, logging, authentication, validation, etc.?"

These are different things. For the skill's stated audience (developers implementing a new system), cross-cutting concerns are arguably more practically valuable than the quality attribute table, because they directly prescribe implementation patterns that must be consistent.

Note: The skill states "Technology choices belong in ADRs." Some cross-cutting concerns straddle the line between architecture pattern and technology choice. The skill would need to document patterns at the architectural level while deferring technology specifics to ADRs.

**Severity assessment: Confirmed as IMPORTANT (slightly below CRITICAL).** The absence won't make the document fundamentally unable to guide implementation, but it will leave a significant gap that developers will fill inconsistently.

---

## Additional Gap Identified by Reviewer

### Finding 7: No Guidance on Document Evolution / Living Document Strategy

The workflow produces a point-in-time architecture document but provides no guidance on how the document should be maintained as the system evolves. The Google Design Docs methodology (referenced in methodology.md) explicitly states docs are "Living document, updated as design evolves." The template has a Version field and Status field (Draft | Approved), but the workflow has no phase or guidance addressing when or how to update the document.

**Severity assessment: NICE-TO-HAVE.** The skill's purpose is to *generate* the initial architecture document, not to define a maintenance process. A separate skill or a brief note in the output document would address this adequately.

---

## Final Assessment

### Confirmed Critical Gaps

| # | Gap | Fix Approach |
|---|-----|-------------|
| 1 | **Missing Deployment View / Infrastructure Perspective** | Add Phase 5.5 or expand Phase 5 to include C4 Deployment Diagram. Add corresponding template section. Keep technology-agnostic. |

### Confirmed Important Gaps (Should Be Fixed)

| # | Gap | Fix Approach |
|---|-----|-------------|
| 2 | **Missing Bounded Context Identification** | Add lightweight bounded context assessment step ("Does this system have multiple distinct subdomains?") and optional context map section. |
| 6 | **No Cross-Cutting Concerns Section** | Add a section between Quality Attributes and Constraints in the template, with a corresponding workflow phase. |

### Downgraded Findings (Sub-Agent Said Critical, Reviewer Says Nice-to-Have)

| # | Gap | Reason for Downgrade |
|---|-----|---------------------|
| 3 | No Runtime/Behavioral View | Template already includes Data Flow section with sequence diagram. Adequate for most target projects. |
| 5 | Clean Architecture Without Fit Assessment | Routing mechanism provides implicit fit assessment. Clean Architecture is appropriate for the vast majority of systems reaching this workflow path. |

### Disputed Findings

| # | Gap | Reason for Dispute |
|---|-----|-------------------|
| 4 | No Stakeholder-Viewpoint Mapping | Formal ISO/IEC 42010 governance is an enterprise practice, inappropriate for agile project-level context. The fixed view set is well-chosen and comprehensive. |

### Reviewer-Identified Gaps (Not Flagged by Sub-Agent)

| # | Gap | Severity |
|---|-----|----------|
| 7 | No Document Evolution / Living Document Strategy | Nice-to-have (skill purpose is generation, not maintenance) |

---

## Verification Checklist

- [x] All skill files were read (7 files: workflow, SKILL.md, template, methodology, domain-modeling, clean-architecture, data-api-extraction)
- [x] Sub-agent review conducted against ISO/IEC 42010, arc42, C4 Model, SEI Views and Beyond, IEEE 1471/42010, DDD strategic patterns, and Kruchten 4+1
- [x] Every sub-agent finding received an explicit AGREE/DISAGREE/PARTIALLY AGREE verdict with reasoning
- [x] Summary report written to `./reviews/arch-doc-skill-review.md`
- [x] Independent assessment included (document evolution gap identified as additional finding)
