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
- Platform Constraints Reviewer — vendor capabilities, plan limitations, API truth
- State Machine Reviewer — status transitions, race conditions, concurrent state
- Operational Readiness Reviewer — monitoring, alerting, debugging, day-2 ops
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
- Is any mechanism disproportionately complex for the problem it solves? Could the design be significantly simpler while still meeting the stated requirements?

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

<archetype id="platform-constraints-reviewer">

**Platform Constraints Reviewer**

**Expertise:** Vendor platform capabilities and limitations, plan tier feature gates, platform API truth vs spec assumptions, undocumented platform behaviors, vendor-specific gotchas.

**Selection signals in spec:**
- Specific platform or vendor names (Airtable, Shopify, Salesforce, Stripe, AWS, Firebase, Supabase)
- Claims about platform-specific features (automations, webhooks, shared views, permissions models, Interface-only access)
- Vendor API limitations or plan tier dependencies
- Assumptions about what a platform "can" or "cannot" do
- Design workarounds for platform limitations (e.g., "Airtable doesn't support dynamic field visibility, so we control it via data")

**What this reviewer checks:**
- Verify every claim about what the platform can and cannot do — treat each as a hypothesis, not a fact
- Check plan tier requirements: does the design depend on features only available on higher tiers?
- Identify undocumented platform limitations that could break the design (rate limits, record caps, automation trigger reliability, shared link restrictions)
- Verify platform API behaviors match spec assumptions (e.g., does a webhook actually fire on a specific status change? Can a shared Interface actually filter by linked record?)
- Check whether platform behavior differs between API access and UI access (some platforms behave differently via API vs their native UI)
- Check for platform-specific race conditions (e.g., automation trigger timing, webhook delivery guarantees, eventual consistency)
- Verify platform migration paths exist — if the design requires upgrading tiers mid-project, what's the rollback plan?
- Identify vendor lock-in risks: what happens if the platform changes a feature or deprecates an API?
- When a platform claim cannot be verified from code or documentation alone, flag it as "Assumption Requiring Manual Verification" with severity Major — present these separately in synthesis rather than silently accepting the spec's claim

**Files to read:** Platform integration code, API client wrappers, configuration files, any platform-specific documentation referenced in the spec.

</archetype>

<archetype id="state-machine-reviewer">

**State Machine Reviewer**

**Expertise:** Status lifecycle correctness, state transition completeness, race conditions between concurrent state changes, re-entry flows, recovery semantics, guard conditions.

**Selection signals in spec:**
- Status fields with defined transitions (e.g., Queued → Running → Completed/Failed)
- Re-entry or looping flows (e.g., Review → Queued for top-ups)
- Concurrent operations on shared state (multiple users, multiple webhooks, polling + webhooks)
- Recovery mechanisms for stuck states (polling for stale records, timeout-based retries)
- Mentions of "race condition", "concurrent", "at the same time", "meanwhile"
- Webhook + polling overlap (both mechanisms can trigger the same operation)
- Guard conditions ("if status = X then do Y")

**What this reviewer checks:**
- Enumerate ALL valid state transitions explicitly — draw the state machine and find missing edges
- Identify impossible or unspecified transitions: what happens if a record is in state X and event Y occurs? (e.g., AM clicks "Request More" while server is already populating)
- Find race conditions: two concurrent triggers operating on the same record (webhook fires + polling loop detects same stuck record)
- Verify recovery mechanisms don't conflict with normal operation (e.g., polling recovery re-processes a campaign the webhook is already handling)
- Check for states with no exit (dead states) — can a record get stuck permanently?
- Verify re-entry flows: after looping back, does the system behave identically to the first pass? Are counters/accumulators reset correctly?
- Verify state transitions are idempotent — what happens if the same transition fires twice? (e.g., two webhooks for the same event)
- Check whether status values are validated on write — can a bug set an invalid status string?
- Check guard condition completeness: every status branch should handle "else" — what if the status is something unexpected?

**Files to read:** Orchestration code, status constants/enums, existing state management code (e.g., run managers, polling loops), webhook handlers.

</archetype>

<archetype id="operational-readiness-reviewer">

**Operational Readiness Reviewer**

**Expertise:** Day-2 operations: monitoring, alerting, debugging workflows, observability, incident response, graceful degradation, operator experience.

**Selection signals in spec:**
- Long-running background processes or stateful endpoints
- Polling loops or scheduled operations without described monitoring
- Multi-user systems where failures affect specific users
- Production systems where failure detection is unspecified
- Mentions (or conspicuous absence) of "monitoring", "alerting", "logging", "observability"
- Failure recovery mechanisms (implies failures happen — but how will operators know?)

**What this reviewer checks:**
- For each failure mode described (or implied) in the spec: how does an operator KNOW it happened? Is there an alert, a log, a dashboard, or nothing?
- What is the mean-time-to-detect (MTTD) for each failure mode? Is it acceptable?
- Can an operator debug a specific failure? (e.g., "Campaign matched only 18 of 30 — why?" Is the reasoning logged?)
- Is there a health check or heartbeat for new endpoints/processes?
- What does graceful degradation look like? Does the system fail loudly or silently?
- Are there any "silent success" paths where the system does nothing but doesn't report why? (e.g., "open slots = 0, exits" — does anyone know this happened?)
- Are there operational escape hatches? Can an operator manually force a state transition, retry a failed operation, or skip a stuck step?
- What operational procedures does this feature require that are currently unspecified?
- Are log messages actionable? (Not just "error occurred" but enough context to diagnose)

**Files to read:** Server entry points, existing logging patterns, existing health checks, monitoring/alerting configuration, error handling code.

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
- List 3-5 topics that a spec of this type SHOULD address but doesn't. For each, assess whether the omission is acceptable (obvious to implementer) or dangerous (could cause implementation to diverge from intent)
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
6. If 7+ archetypes match, the spec is broad — prioritize the 4-5 with the strongest signal density (most signals matched, most relevant to the spec's riskiest sections) and fold the remaining archetypes' top concerns into the Devil's Advocate's focus areas. Announce which archetypes were folded and why.

The orchestrator announces the selected team to the user before spawning, e.g.:
"Based on the spec's domain dimensions, I'm spawning 4 reviewers: Data Integrity Guardian (field preservation rules in Sections 3, 5.4), Performance Analyst (batch operations, API costs in Sections 5, 9), Integration Detective (new endpoint, env vars in Sections 6, 11), and Devil's Advocate."

</selection_process>
