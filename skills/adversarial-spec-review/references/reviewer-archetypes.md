<catalog>

The orchestrator selects reviewers by scanning the spec for **domain signals** — keywords, section topics, and structural patterns that indicate which areas of expertise are needed. Each archetype below lists its selection signals.

The orchestrator MUST NOT default to a fixed count. Select as many reviewers as the spec's dimensions demand, plus the mandatory Devil's Advocate. Typical range: 3-5 total.

## Contents
- Data Integrity Guardian — field preservation, corruption, audit trails
- Architecture Critic — module boundaries, interfaces, testability, SOLID
- Performance Analyst — scalability, rate limits, cost modeling
- Integration Detective — env vars, deployment, external dependencies
- Security Auditor — auth, secrets, injection, access control
- UX Advocate — user-facing workflows, error messages, feedback
- Domain Expert — business logic, domain rules, edge cases
- Devil's Advocate (mandatory) — end-to-end flows, contradictions, blind spots
- Selection Process — how to pick the right team

</catalog>

<archetype id="data-integrity-guardian">

**Data Integrity Guardian**

**Expertise:** Field preservation rules, data corruption risks, partial failure semantics, null vs empty vs default distinctions, audit trail integrity.

**Selection signals in spec:**
- Field lists (what gets updated vs preserved)
- Data transformation or enrichment stages
- Database schema changes (new fields, field type changes)
- Write paths (create, update, upsert)
- Mentions of "overwrite", "preserve", "protect", "skip"
- INSERT_ONLY or similar protection mechanisms

**What this reviewer checks:**
- Walk through every field in the data model and verify the spec's update/preserve decisions are correct
- Verify protection mechanisms actually work by tracing through the code path
- Check for fields that the spec claims are preserved but the code would overwrite
- Identify partial failure scenarios where data could end up in an inconsistent state
- Verify audit trail fields are never silently modified

**Files to read:** Data model definitions, transform functions, writer/persistence code, type definitions.

</archetype>

<archetype id="architecture-critic">

**Architecture Critic**

**Expertise:** Module boundaries, separation of concerns, code duplication risks, interface contracts, type system design.

**Selection signals in spec:**
- New functions or modules being created
- Refactoring decisions (extract, merge, split)
- "Separate function vs mode flag" discussions
- Interface or type changes
- Mentions of "reuse", "shared", "common"
- Dependency injection patterns or test setup implications
- Mentions of "mock", "stub", "testable", "injectable"

**What this reviewer checks:**
- Is the architectural decision (e.g., separate function vs mode flag) justified?
- What code duplication does this introduce? Can shared helpers be extracted?
- Are interface changes backward-compatible or do they break existing callers?
- Is the type system design clean (union types, generics, discriminated unions)?
- Are local/private functions being reused without extraction?
- Can each component be tested in isolation via TDD? Are dependencies injectable or hardwired?
- Does the design force awkward test setups (deep mocking, global state, test-only code paths)?

**Files to read:** Existing modules being modified, interface definitions, type files, callers of changed interfaces.

</archetype>

<archetype id="performance-analyst">

**Performance Analyst**

**Expertise:** Scalability, API rate limits, batch sizes, N+1 query patterns, concurrency, cost modeling.

**Selection signals in spec:**
- Batch operations or pagination
- API calls with rate limits or cost per call
- Concurrency controls (p-limit, queues)
- "At scale" considerations or growth projections
- Polling loops or scheduled operations
- Cost estimates or budget sections

**What this reviewer checks:**
- What breaks at 10x or 50x current scale? Identify the first bottleneck.
- Are batch sizes optimal for the underlying API limits?
- Any N+1 query patterns (per-item lookups that could be batched)?
- Are expensive operations (API calls, DB queries) minimized?
- Do polling/scheduled operations add unnecessary overhead?
- Are cost estimates realistic?

**Files to read:** API client code (rate limits, batch sizes), existing polling/loop code, database/storage client code.

</archetype>

<archetype id="integration-detective">

**Integration Detective**

**Expertise:** Interface contracts between systems, environment variables, deployment checklists, dependency injection, configuration management.

**Selection signals in spec:**
- New API endpoints
- New environment variables or secrets
- External service integrations (webhooks, automations)
- Changes to dependency injection interfaces
- Deployment or infrastructure changes
- CI/CD pipeline impacts

**What this reviewer checks:**
- Are all new env vars listed in every relevant location (spec, README, deployment checklist)?
- Do interface changes (e.g., dependency injection) propagate to all callers?
- Is the deployment sequence specified (what must happen before what)?
- Are external integrations (webhooks, automations) resilient to failures?
- What happens when an external dependency is down?

**Files to read:** Server/entry point code, config files, existing interface definitions, deployment configs, .env templates.

</archetype>

<archetype id="security-auditor">

**Security Auditor**

**Expertise:** Authentication, authorization, secret management, injection attacks, data exposure, access control.

**Selection signals in spec:**
- New API endpoints exposed to external callers
- Authentication tokens or secrets
- User input handling
- Automation scripts containing credentials
- Data exposed through APIs or interfaces
- Mentions of "Bearer", "token", "secret", "auth"

**What this reviewer checks:**
- Is authentication sufficient for exposed endpoints?
- Are secrets properly managed (not hardcoded, not logged, rotated)?
- Can user input cause injection or unexpected behavior?
- Are automation scripts that contain secrets secure?
- Is the principle of least privilege followed?

**Files to read:** Server routes, auth middleware, env var files, automation scripts.

</archetype>

<archetype id="ux-advocate">

**UX Advocate**

**Expertise:** User-facing workflows, error messages, feedback loops, state visibility, progressive disclosure.

**Selection signals in spec:**
- UI/interface changes (forms, buttons, views, dashboards)
- User-facing status or feedback mechanisms
- Error messages shown to users
- Workflow steps involving human interaction
- Mentions of "form", "button", "view", "page", "dashboard"

**What this reviewer checks:**
- What does the user see at each step? Is status visible?
- Are error states communicated clearly? What does the user do when something fails?
- Is the happy path intuitive? Are there unnecessary steps?
- Are edge cases handled gracefully from the user's perspective?
- Is feedback immediate or delayed? If delayed, is progress visible?

**Files to read:** UI-related code, existing interface configurations, form/view definitions.

</archetype>

<archetype id="domain-expert">

**Domain Expert**

**Expertise:** Business logic correctness, domain rules, edge cases specific to the problem domain.

**Selection signals in spec:**
- Domain-specific terminology or rules
- Business logic decisions (classification, categorization, pricing)
- Industry-specific requirements (compliance, regulations)
- Data domain constraints (valid ranges, required relationships)

**What this reviewer checks:**
- Are domain rules correctly implemented?
- Are there edge cases in the business logic that the spec doesn't handle?
- Do domain constraints match real-world requirements?
- Are domain-specific terms used consistently?

**Files to read:** Business logic code, domain model definitions, existing validation rules.

</archetype>

<archetype id="devils-advocate">

**Devil's Advocate (MANDATORY — always included)**

**Expertise:** Finding what everyone else missed. Integration gaps, contradictions, unstated assumptions, operational blind spots.

**This reviewer is ALWAYS selected regardless of domain signals.**

**What this reviewer checks:**
- Walk EVERY end-to-end flow described in the spec, step by step, and find gaps
- Find contradictions between sections
- Find where the spec is dangerously vague ("somehow", "as needed", "TBD")
- What operational concerns are missing? (monitoring, alerting, debugging)
- What happens when things go wrong in ways the spec didn't anticipate?
- Did the fixes from prior rounds introduce new problems?

**Files to read:** All files other reviewers read, plus entry points and orchestration code.

</archetype>

<selection_process>

To select reviewers:

1. Read the entire spec
2. For each archetype, check if 2+ selection signals are present in the spec
3. All matching archetypes become reviewers
4. Always include Devil's Advocate
5. If fewer than 2 non-devil's-advocate archetypes match, the spec may be too narrow — ask the user if they want a focused review or want you to broaden the lens

The orchestrator announces the selected team to the user before spawning, e.g.:
"Based on the spec's domain dimensions, I'm spawning 4 reviewers: Data Integrity Guardian (field preservation rules in Sections 3, 5.4), Performance Analyst (batch operations, API costs in Sections 5, 9), Integration Detective (new endpoint, env vars in Sections 6, 11), and Devil's Advocate."

</selection_process>
