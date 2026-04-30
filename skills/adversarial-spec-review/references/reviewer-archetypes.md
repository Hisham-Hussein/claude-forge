<catalog>

The orchestrator selects reviewers by scanning the spec for **domain signals** — keywords, section topics, and structural patterns that indicate which areas of expertise are needed. Each archetype below lists its selection signals.

The orchestrator MUST NOT default to a fixed count. Select as many reviewers as the spec's dimensions demand, plus the mandatory Devil's Advocate. Typical range: 3-5 total.

## Contents
- Data Integrity Guardian — field preservation, corruption, audit trails
- Architecture Critic — module boundaries, package boundaries, interfaces, testability, SOLID, architectural tech debt
- Behavioral Preservation Reviewer — refactoring safety, type widening, default preservation, value tracing
- Performance Analyst — scalability, rate limits, cost modeling
- Integration & Feasibility Detective — env vars, deployment, file mappings, build viability, scope estimation
- Deployment Mechanics Reviewer — Dockerfile, shutdown semantics, lock lifecycle, rollback, persistent state
- Security Auditor — auth, secrets, injection, access control
- UX Advocate — user-facing workflows, error messages, feedback
- Domain Expert — business logic, domain rules, edge cases
- Platform Constraints Reviewer — vendor capabilities, plan limitations, API truth
- State Machine Reviewer — status transitions, race conditions, concurrent state
- Operational Readiness Reviewer — monitoring, alerting, debugging, day-2 ops
- Competitive Coder — regex precision, algorithmic edge cases, parsing correctness
- Test Architect — three-layer test coverage, unit/integration/E2E completeness, CLAUDE.md T1-T8 compliance
- Prompt Critic — prompt-as-code architecture, prompt engineering quality, LLM input/output design
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

**Expertise:** Module boundaries, package boundaries, separation of concerns, code duplication risks, interface contracts, type system design, public API surface management, dependency direction, architectural tech debt detection.

**Selection signals in spec:**
- New functions or modules being created
- Refactoring decisions (extract, merge, split)
- "Separate function vs mode flag" discussions
- Interface or type changes
- Mentions of "reuse", "shared", "common"
- Dependency injection patterns or test setup implications
- Mentions of "mock", "stub", "testable", "injectable"
- Monorepo or package extraction (barrel exports, workspace packages, internal vs public types)
- Adapter or implementation placement decisions (which package owns what)
- Mentions of "export", "barrel", "index.ts", "public API", "internal"
- Platform-specific names or vendor-specific patterns in core/shared packages
- Mentions of "debt", "coupling", "migration", "neutral", "platform"
- Code placed in core packages that names a specific external platform or vendor

**What this reviewer checks:**
- Is the architectural decision (e.g., separate function vs mode flag) justified?
- What code duplication does this introduce? Can shared helpers be extracted?
- Are interface changes backward-compatible or do they break existing callers?
- Is the type system design clean (union types, generics, discriminated unions)?
- Are local/private functions being reused without extraction?
- Can each component be tested in isolation via TDD? Are dependencies injectable or hardwired?
- Does the design force awkward test setups (deep mocking, global state, test-only code paths)?
- Is any mechanism disproportionately complex for the problem it solves? Could the design be significantly simpler while still meeting the stated requirements?
- Does the dependency graph flow correctly (core → ports ← adapters, apps → packages)? Any circular dependencies?
- Is the public API surface (barrel export) correct? Are types classified as "internal" that consumers actually need? Are internal types leaking into the public surface?
- For monorepo specs: can each package be consumed independently? Are adapters placed in the right package (shared vs tenant-specific)?
- Do port interfaces fully cover the abstraction? Are there hidden couplings where a "generic" interface requires tenant-specific knowledge?
- **Architectural tech debt audit:** Search the project for tech debt registries or governance documents (e.g., `docs/tech-debt/`, constraint files, CLAUDE.md principles). If a registry exists, cross-reference the spec against it: does the spec deepen any registered debt? Does it add new debt that should be registered? Does it violate any registry rules (e.g., "use neutral names for new items")? If no registry exists, independently audit for architectural debt patterns: platform-specific names leaking into core/shared packages, vendor lock-in in domain logic, coupling that would resist provider substitution, naming that assumes a single implementation when the architecture intends multiple.

**Files to read:** Existing modules being modified, interface definitions, type files, callers of changed interfaces, barrel/index files, package.json files (for workspace and dependency declarations), tech debt registries and governance documents (e.g., `docs/tech-debt/`, CLAUDE.md).

</archetype>

<archetype id="behavioral-preservation-reviewer">

**Behavioral Preservation Reviewer**

**Expertise:** Refactoring safety, type widening risks, default value preservation, value tracing through conversion boundaries, silent regression detection in parameterization and extraction specs.

**Selection signals in spec:**
- Type widening (union types broadened to `string`, specific types relaxed to generic)
- Function signature changes (new parameters, parameter type changes)
- Parameterization of hardcoded values (constants extracted to config, presets, or parameters)
- Claims of "no behavioral change" or "behavioral preservation"
- Default value tables (what happens when a field is omitted)
- Format or encoding conversions at system boundaries (ingress/egress mappings, display name vs code)
- Refactoring specs where existing consumers must continue working unchanged
- Mentions of "preset", "fallback", "default", "backwards-compatible"

**What this reviewer checks:**
- Trace a representative value (e.g., a country name, a niche category, a phone number) through the ENTIRE pipeline — from config ingress through every processing stage to the final output. Verify the value is correct at every boundary. This is the most important check.
- For every parameterized function: does the default value EXACTLY match the current hardcoded behavior? Check each one against source code, not the spec's claims.
- When types widen (e.g., `NicheName` from 26-literal union to `string`): what type safety is lost? Can the existing consumer's strict typing be preserved via presets or generics?
- When conversion boundaries are introduced (e.g., ISO codes internally, display names in storage): enumerate every boundary. For each, verify the conversion is specified, the mapping is complete, and a missing entry fails safely (not silently).
- When a fallback/default changes or becomes configurable: what happens if the configuration fails to load? Does the system fail loudly or silently corrupt data?
- For each "unchanged" claim in the spec: verify it against the actual source code. Read the current implementation and confirm the spec's "before" description is accurate.
- Check that the spec's function signature change table matches actual function names and signatures in the codebase — specs often reference planned names or outdated names instead of what's actually in the code.
- Identify the "preset failure mode": if the tenant preset (e.g., gccPreset) fails to load or is partially spread, which fields fall back to defaults and what's the production impact?

**Files to read:** All files whose function signatures change, type definition files (before and after), domain constants, config/preset files, the transform/output layer, any adapter that does format conversion.

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

<archetype id="integration-feasibility-detective">

**Integration & Feasibility Detective**

**Expertise:** Interface contracts between systems, environment variables, deployment checklists, dependency injection, configuration management, file mapping completeness, import rewiring, build system viability, scope estimation.

**Selection signals in spec:**
- New API endpoints
- New environment variables or secrets
- External service integrations (webhooks, automations)
- Changes to dependency injection interfaces
- Deployment or infrastructure changes
- CI/CD pipeline impacts
- File moves, renames, or restructuring (monorepo extraction, directory reorganization)
- Build system changes (new bundler, workspace configuration, TypeScript path resolution)
- Explicit file mapping tables (source → destination)
- Session or scope estimates ("~3,000 lines", "fits in one session")
- Mentions of "import", "rewire", "workspace", "turbo", "monorepo"

**What this reviewer checks:**
- Are all new env vars listed in every relevant location (spec, README, deployment checklist)?
- Do interface changes (e.g., dependency injection) propagate to all callers?
- Is the deployment sequence specified (what must happen before what)?
- Are external integrations (webhooks, automations) resilient to failures?
- What happens when an external dependency is down?
- **File mapping completeness:** List every source file and test file in the current codebase. Does the spec's mapping account for ALL of them? Which files are missing from the mapping?
- **Import rewiring:** After files move, which imports break? Are there circular dependency risks in the new structure? Do cross-package imports resolve correctly through workspace symlinks?
- **Build system viability:** Will the proposed build configuration actually work? For TypeScript + workspaces: do path aliases resolve? Does the runtime (tsx, node) resolve workspace packages? Are there known gotchas with the chosen tooling?
- **Test mapping:** Do test files map to the correct package? Do test imports match new source locations? Will the test runner discover tests in the new structure?
- **Scope estimation:** Count actual files to move, imports to rewire, configs to create. Is the claimed scope realistic? If a plan claims "~3,000 lines," verify by counting the actual work.
- **Plan boundary verification:** If the spec splits work into phases (Plan A, Plan B), are dependencies clean? Is anything in Plan A that requires Plan B changes, or vice versa?

**Files to read:** Server/entry point code, config files, existing interface definitions, deployment configs, .env templates, package.json files, tsconfig.json files, build configs (turbo.json, vite.config.ts), Dockerfile, full directory listing of source and test files.

</archetype>

<archetype id="deployment-mechanics-reviewer">

**Deployment Mechanics Reviewer**

**Expertise:** Container builds, graceful shutdown semantics, lock/mutex lifecycle across process boundaries, rollback safety with persistent state, deployment pipeline correctness, process signal handling.

**Selection signals in spec:**
- Dockerfile changes or new container configurations
- Graceful shutdown patterns (SIGTERM, drain, AbortSignal)
- Mutex, lock, or semaphore patterns that span process lifecycle
- Rollback strategies ("revert the merge commit", "redeploy previous version")
- Persistent state that survives deployments (volumes, caches, databases)
- Health check changes or service readiness patterns
- Mentions of "shutdown", "drain", "SIGTERM", "lock", "mutex", "rollback", "volume"
- Process signal handling or lifecycle hooks
- Decorator or wrapper patterns around process-critical operations

**What this reviewer checks:**
- **Container build correctness:** Will the Dockerfile build with the new structure? Are all required files copied? Does `npm ci` resolve workspace dependencies? Are production vs dev dependencies handled correctly?
- **Graceful shutdown preservation:** Does the new shutdown pattern preserve the current drain semantics? Trace the signal path: SIGTERM → abort signal → drain current work → exit. Check for timing issues (can the shutdown handler race with initialization?).
- **Lock lifecycle safety:** For every lock/mutex acquisition, verify there is a guaranteed release path. Check: what if the operation between acquire and release throws? What if the release call itself throws? Is there a `finally` block? Can the lock get stuck permanently?
- **Rollback with persistent state:** If the deployment is reverted, what happens to data written by the new version? Cache format changes? Database migrations? Volume data compatibility? Will the old version choke on new-format data?
- **Health check validity:** Does the health check accurately reflect service readiness? During shutdown, does the health check signal "draining" or does it keep reporting healthy (causing the load balancer to route new requests to a dying instance)?
- **HTTP server lifecycle:** On shutdown, is the HTTP server closed before or after draining background work? Can new requests arrive during the drain window?
- **Environment/path resolution:** After file moves, do `process.cwd()`, `__dirname`, and env file resolution still work in all contexts (local dev, Docker, CI, production platform)?
- **Deployment platform constraints:** Does the deployment platform (Railway, Vercel, AWS, etc.) have build timeouts, memory limits, or other constraints that the new structure might hit?

**Files to read:** Dockerfile, server entry points, shutdown/signal handling code, mutex/lock implementation, health check endpoints, deployment platform configuration, volume mount configuration.

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

<archetype id="competitive-coder">

**Competitive Coder**

**Expertise:** Regex precision, algorithmic edge cases, off-by-one errors, parsing correctness, input boundary conditions, greedy vs lazy matching, character class completeness, catastrophic backtracking.

**Selection signals in spec:**
- Regular expressions (new or modified)
- String parsing or extraction logic
- Input normalization or sanitization
- Character set handling (Unicode, special characters, mixed scripts)
- Digit/number formatting or validation
- Pattern matching with multiple branches or fallbacks
- Edge case lists in test specifications
- Mentions of "first match wins", "greedy", "contiguous", "separator"

**What this reviewer checks:**
- Trace every regex character by character — does each group capture exactly what's intended, nothing more, nothing less?
- Test regex against adversarial inputs: empty strings, max-length strings, inputs that almost-match, inputs with unexpected separators
- Check for catastrophic backtracking (nested quantifiers on overlapping character classes)
- Verify greedy vs lazy quantifiers produce correct results at boundaries
- Check character class completeness — are all valid separators included? Are invalid ones excluded?
- Verify anchoring: can the regex match in an unintended position (mid-word, inside a URL, inside another number)?
- Check normalization ordering: does the order of strip → match → normalize steps produce correct results for ALL input variants, not just the examples?
- Verify digit count constraints match real-world formats — off-by-one in `{8}` vs `{9}` silently drops valid inputs
- Check for false positives: inputs that shouldn't match but do (e.g., a sequence of digits inside a URL or ID that looks like a phone number)
- Check for false negatives: valid inputs the spec claims to support but the regex would reject (e.g., less common but valid separators like `/` or `(`)
- When test cases are specified, verify they are exhaustive: do they cover every regex branch? Every normalization path? Every boundary between "match" and "no match"?

**Files to read:** Source files containing regex/parsing logic, test files with edge cases, any referenced format specifications or standards.

</archetype>

<archetype id="test-architect">

**Test Architect**

**Expertise:** Three-layer test coverage completeness (unit, integration, E2E), test strategy soundness, CLAUDE.md testing discipline principles T1–T8 compliance, boundary-to-test traceability, pipeline-to-E2E traceability, zero-gap test coverage verification.

**Selection signals in spec:**
- New adapter methods or external service integrations (Airtable, OpenAI, Apify, LinkedIn)
- Pipeline or orchestrator creation (multi-step workflows wiring adapters and engine logic)
- Behavioral logic (matching, filtering, scoring, classification, validation, state transitions)
- State machine definitions with status transitions
- New port or interface definitions at external boundaries
- Data transformation or enrichment stages
- Mentions of "test", "coverage", "verification", "validation"
- User-facing workflows that a user or operator would trigger

**What this reviewer checks:**

This reviewer enforces the project's three-layer testing methodology as defined in CLAUDE.md principles T1–T8. The core mandate: **nothing the spec adds should escape testing. Zero holes. Zero scenarios without coverage.**

1. **Three-layer coverage matrix.** For every behavioral component the spec introduces, produce a coverage assessment across all three layers:

| Component | Unit Test Required? | Integration Test Required? | E2E Test Required? | Spec Coverage |
|---|---|---|---|---|
| Matching engine (6 filters) | Yes — per filter logic | No — pure domain logic | Yes — part of campaign pipeline | Missing E2E |
| Airtable adapter (listInfluencers) | Yes — mapper/transform | Yes — real Airtable call (T7) | Yes — part of campaign pipeline | Missing integration |
| Voice extraction pipeline | Yes — prompt construction | Yes — real LLM call | Yes — user-facing workflow (T8) | Full |

Coverage levels:
- **Full** = spec explicitly addresses testing at all applicable layers
- **Partial** = spec addresses some layers but misses others → Major finding
- **None** = spec has no test strategy for this component → Critical finding

2. **Unit test completeness (T1, T2).** For every behavioral function or module the spec introduces, verify: (a) does the spec prescribe or imply unit tests? (b) do the described tests exercise **behavior, not just signatures** (T2)? A spec that says "test the matching engine" without specifying what behaviors to test (filter logic, sort order, exclusion rules, edge cases) is insufficient. (c) are edge cases addressed — empty inputs, boundary values, error paths, partial data? A matching engine with 6 filter criteria needs tests for each criterion independently AND in combination. A single "it matches" test is a T2 violation.

3. **Integration test boundary audit (T7 — MANDATORY).** Enumerate every adapter method the spec introduces that communicates with a real external system. For EACH one, verify the spec includes an integration test requirement against the real system — not mocks. This is a **blocking requirement per T7**: an adapter method is not complete until its integration test passes against the real system. Unit tests verify logic; integration tests verify the external system behaves as assumed. Mocked clients hide contract mismatches. Produce an explicit boundary-to-test traceability list:

| Adapter Method | External System | Integration Test Specified? | Verdict |
|---|---|---|---|
| listInfluencers() | Airtable | Yes — spec Section 7 | Pass |
| fetchPosts() | Apify/LinkedIn | No | **FAIL — T7 violation** |
| generateContent() | OpenAI | No | **FAIL — T7 violation** |

Every "FAIL" is a Critical finding. T7 is non-negotiable.

4. **E2E pipeline audit (T8 — MANDATORY).** Identify every user-facing pipeline the spec creates, modifies, or completes — an orchestrated flow that wires multiple adapters and engine logic into an end-to-end workflow. For EACH pipeline, verify the spec includes an E2E test requirement that exercises the full pipeline with zero mocks — real external services, real data, real write-back. This is a **blocking requirement per T8**: if the spec adds a pipeline, the spec is not complete without an E2E test for that pipeline. Produce an explicit pipeline-to-E2E traceability list:

| Pipeline | Components Wired | E2E Test Specified? | Verdict |
|---|---|---|---|
| Enrichment pipeline | LLM + Airtable → fields written | Yes — spec Section 9 | Pass |
| Social import pipeline | Apify + Airtable → Writing Samples | No | **FAIL — T8 violation** |

Every "FAIL" is a Critical finding. T8 is non-negotiable.

5. **Test data realism check (T3).** For every test scenario the spec describes, verify: does it use realistic, imperfect inputs? Partial data, nulls, missing fields, edge-case shapes? All-happy-path fixtures hide wiring problems. If the spec's test examples are all clean/perfect data, flag it as Major — T3 requires realistic test data.

6. **Test isolation check (T6).** If the spec describes test suites or test setup patterns, verify: do tests depend on each other's state, execution order, or side effects? Shared mutable state between tests is a T6 violation. Each test must set up its own preconditions. Exception: integration/E2E tests may share expensive resources (API clients, Airtable records) in `beforeAll`, but must not depend on test execution order.

7. **Error suppression prohibition check (T4).** If the spec's test strategy mentions or implies any form of error suppression to make tests pass (`dangerouslyIgnoreUnhandledErrors`, blanket `try/catch`, `@ts-ignore`, `--no-verify`), flag it as Critical. T4 is absolute: error suppression is never acceptable — not as a first resort, not as a last resort, not under any circumstance.

8. **Gated test visibility check (T5).** If the spec introduces tests gated behind opt-in flags (environment variables, feature flags, cost-bearing test suites), verify the spec makes the gating explicit and documents what coverage is skipped when the gate is closed. Silent skipping of gated tests violates T5.

**Severity calibration for this domain:**
- **Critical:** A spec introduces an adapter method with no integration test requirement (T7 violation). A spec introduces a user-facing pipeline with no E2E test requirement (T8 violation). A spec proposes error suppression to make tests pass (T4 violation). A behavioral component has zero test coverage at any layer.
- **Major:** A spec addresses some test layers but misses others (partial coverage). Tests exercise signatures but not behavior (T2 violation). Test data is all-happy-path with no edge cases (T3 violation). Tests share mutable state or depend on execution order (T6 violation). Gated tests skip silently without documentation (T5 violation).
- **Minor:** Test descriptions could be more specific but cover the right behaviors. Test data is realistic but doesn't cover every edge case. Cosmetic test organization issues.
- **Not a finding:** The absence of a testing framework choice when the project already has one. Don't flag missing test infrastructure that already exists in the codebase. Don't flag test count — coverage completeness matters, not test quantity.

**Files to read:** The spec (every section — test gaps hide in sections that seem non-testable), the project's CLAUDE.md (critical — contains T1–T8 principles that this reviewer enforces verbatim), existing test files (to understand current testing patterns and frameworks), data model schema (to identify external boundaries), architecture document (to identify pipeline/adapter boundaries).

</archetype>

<archetype id="prompt-critic">

**Prompt Critic**

**Expertise:** LLM prompt architecture, prompt engineering quality, input/output schema design, prompt text effectiveness, few-shot strategy, separation of concerns between computation and LLM reasoning, structured output validation, token efficiency, prompt ordering and caching.

**Selection signals in spec:**
- LLM prompt creation or modification (`.prompt.ts` files, `assemblePrompt()`, system/user prompts)
- Zod schemas for LLM input or output
- `generateObject<T>()` or structured output calls
- Prompt text with instructions, examples, or field definitions
- Mentions of "prompt", "LLM", "extraction", "generation", "system prompt", "user prompt"
- XML or markdown structuring of prompt content
- Few-shot examples or anti-pattern lists
- Token budget or context window considerations
- Aggregation or pre-computation of data fed to an LLM
- Prompt ordering decisions (static vs dynamic content, caching considerations)

**Core principles (apply universally — no project-specific docs needed):**

*Three-layer responsibility split:* Every well-engineered LLM call separates three concerns with strict boundaries:

| Layer | Responsibility | Violation examples |
|---|---|---|
| **Caller** (business logic) | Fetches data, computes deterministic values (counts, averages, rankings, filtering, sorting), builds typed input | Computing inside the prompt module; fetching data inside the prompt module |
| **Prompt module** (pure rendering) | Transforms typed input into prompt strings. No computation, no side effects, no data fetching. Exports typed input/output schemas and a pure assembly function | Aggregation logic inside assemblePrompt(); API calls inside the prompt; hardcoded data that should come from the caller |
| **LLM provider** (execution + validation) | Sends prompt, validates response against typed output schema, returns typed result | Prompt construction inside the provider; business logic in the validation layer |

*Why this matters:* When the caller computes deterministic values (e.g., "7 of 10 posts use Question hooks"), the LLM receives verified facts — not values it might hallucinate from counting. When the prompt module is pure, it is testable in isolation. When the provider enforces the output schema, the caller gets typed data it can trust.

*Prompt engineering quality:* Inside the prompt module, the assembly function is where prompt engineering craft applies. Effective prompts share these traits:
- **Structural delineation:** Sections are clearly separated (XML tags, markdown headers, or delimiters) so the LLM can locate information without scanning the entire context
- **Instructions + examples are complementary:** Instructions define rules, examples demonstrate application. Every behavior shown in examples must also be stated in instructions. Instructions set the floor; examples set the ceiling.
- **Negative instructions over negative examples:** "Never use the word 'leverage'" works better than showing bad output (which primes the model to produce it)
- **Output format enforced by schema, not by prompt:** When using structured output (`generateObject`, `response_format`), the typed schema enforces structure — the prompt should describe *what* to produce, not *how* to format it
- **Token efficiency:** Every token must justify its inclusion. Deterministic values computed by code, not by the LLM. Context curated for the current step, not bulk-loaded "just in case"
- **Match instruction explicitness to model capability:** GPT models (GPT-4.1, GPT-5) benefit from explicit, structured instructions. Newer models (GPT-5.5+) and reasoning models work best with outcome-first prompts. Regardless of model, avoid extreme over-specification (20 rigid steps for a judgment task) and reserve absolute rules for true invariants. The reviewer should check whether the spec's instruction style matches the target model.
- **Message role priority:** Authoritative rules belong in the system/developer message, not the user message. Developer/system messages take priority over user messages regardless of position. Design prompts so the priority chain and positional recency reinforce each other, never compete.
- **Match prompt style to output style:** The formatting and tone of prompt text influence the formatting and tone of output. Concise prose prompt → concise prose output. Verbose, over-formatted prompt → verbose, over-formatted output.

**What this reviewer checks:**

1. **Layer boundary violations.** Trace every piece of data from its source to its appearance in the prompt. For each, verify: is it computed in the caller (correct) or inside the prompt module (violation)? Is there computation that could be done deterministically in code but is delegated to the LLM (e.g., counting occurrences, computing averages, ranking items)?

2. **Prompt module purity.** Read the `assemblePrompt()` function (or equivalent). Does it have side effects? Does it fetch data? Does it compute values? It should be a pure function: typed input in, strings out. Testable by asserting "given this input, the assembled prompt contains these strings."

3. **Input schema completeness.** Does the typed input schema contain everything the prompt needs? Are there values hardcoded in the prompt text that should be parameterized through the input schema? Are there input fields that the prompt ignores (dead inputs)?

4. **Output schema precision.** Does the output schema enforce what the spec requires? Are constraints (min/max array lengths, enums, required vs optional) appropriate for the LLM's capability? Are optional fields marked correctly for the LLM provider's structured output mode (e.g., `.nullable()` for OpenAI)? Does the schema granularity match the consumer? Code consumers need fine-grained typed schemas; LLM consumers need coarse string fields with prompt instructions controlling internal structure — over-structured schemas compress LLM output quality.

5. **Prompt text quality.** Read the actual prompt text (system + user) as if you were the LLM receiving it. Is each section's purpose clear? Are field definitions unambiguous — could two reasonable interpretations exist? Are there instructions that contradict each other? Is the role definition appropriate? Are anti-pattern instructions phrased as negative instructions (not negative examples)? If few-shot examples are used, are there 3-5 (the diminishing-returns sweet spot), or is there measured justification for a different count? Are examples placed after instructions and near the end of the prompt? If the prompt retrieves factual context for creative generation, does it partition source-backed facts from creative framing and instruct the model on what to do when evidence is missing? Does the prompt's prose style match the desired output style (concise prompt → concise output)?

6. **Structural clarity.** Are prompt sections delineated so the LLM can parse them unambiguously? For complex prompts (multiple sections, metadata blocks, per-item data): is there structural markup (XML tags, clear delimiters) that separates sections? For simple prompts: is the structure clean enough without markup?

7. **Token efficiency.** Estimate the token count for a realistic input. Is it within model limits with margin? Are there redundancies between prompt sections (the same rule stated differently in instructions and examples)? Is context curated for the task or bulk-loaded? Are deterministic values computed by code or delegated to the LLM? Is static content (system prompt, instructions) placed before dynamic content (per-request context, examples, input) to enable prompt caching? Where caching-optimal and comprehension-optimal ordering conflict, does the choice match the pipeline's call volume?

8. **Prompt version and observability.** Does the prompt module export a version string? A task ID? Can outputs be traced back to the exact prompt version that produced them? If the spec changes the prompt significantly, is the version bumped?

**Severity calibration for this domain:**
- **Critical:** Computation inside the prompt module (layer violation). The prompt module has side effects or fetches data (purity violation). Output schema missing or not enforced by structured output. Prompt text contains contradictory instructions. Over-structured output schema for an LLM consumer (e.g., 10+ nested schemas for a field the LLM should produce as prose — proven to compress quality).
- **Major:** Deterministic values delegated to LLM instead of computed in code. Input schema missing fields the prompt needs. Output schema constraints incompatible with the LLM provider. Prompt sections ambiguous or poorly delineated. Token budget exceeds model limits for realistic input. Few-shot examples contradict instructions. Authoritative rules placed in user message instead of system/developer message. Instruction explicitness mismatched to target model (e.g., vague outcome-only prompt for GPT-4.1, or 15+ rigid steps for a reasoning model).
- **Minor:** Prompt text could be more concise. Structural markup style inconsistent with project conventions. Version not bumped for minor changes. Token budget suboptimal but within limits. Static/dynamic content ordering suboptimal for caching but within token limits. Few-shot count outside 3-5 range without measured justification. Prompt prose style mismatches desired output style.
- **Not a finding:** Choice of XML vs markdown vs delimiters for prompt structuring (this is a project convention, not a quality issue). Specific LLM provider choice. Model selection (fast vs quality tier).

**Project-specific enhancement:** If the project has a prompt architecture section in its architecture document (search for "Prompt Architecture", "prompt-as-code", or `.prompt.ts` patterns), read it — it may define project-specific conventions for prompt module structure, naming, file organization, and text formatting. If the project has prompt engineering research (search `artifacts/research/` for "prompt engineering" or "best practices"), read it for project-specific evidence-backed techniques. These project-specific docs enhance the review but are not required — the core principles above are sufficient for any project.

**Deep reference:** Read `references/prompt-critic-reference.md` for research-backed rationale, detailed examples, and common prompt spec issues. The core principles above are sufficient for triage; the reference file provides depth for thorough reviews.

**Files to read:** All `.prompt.ts` files being created or modified, the caller that builds the prompt input, the LLM provider integration code, the output schema and how it's consumed, architecture documents (for project-specific prompt conventions), any referenced prompt engineering research.

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
