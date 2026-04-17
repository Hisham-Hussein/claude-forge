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
