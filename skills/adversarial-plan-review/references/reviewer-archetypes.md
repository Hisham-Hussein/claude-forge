<catalog>

The orchestrator selects reviewers by scanning the plan for **scope signals** — task count, subsystem breadth, technology mix, dependency complexity, and structural patterns that indicate which areas of expertise are needed. Each archetype below lists its selection signals.

The orchestrator MUST NOT default to a fixed count. Select as many reviewers as the plan's dimensions demand, plus the mandatory Devil's Advocate. Typical range: 3-7 total.

## Contents
- Dependency Analyst — task ordering, parallelism validity, prerequisite chains
- Spec Fidelity Reviewer — coverage gaps, scope creep, requirement traceability
- Task Decomposition Critic — granularity, atomicity, step completeness, file paths
- TDD Discipline Reviewer — test quality, red-green-commit cycle, assertion specificity
- Integration Sequencing Reviewer — build order, working system at each boundary, merge safety
- Risk & Blocker Detector — external dependencies, unknowns, assumptions, environmental prerequisites
- Codebase Alignment Reviewer — existing patterns, interface compatibility, naming conventions
- Competitive Coder — regex precision, algorithmic edge cases, parsing correctness
- Devil's Advocate (mandatory) — end-to-end walkthrough, contradictions, blind spots
- Software Architecture Reviewer — dependency direction fidelity, boundary implementation, vendor isolation, SOLID compliance in code
- Performance & Scalability Reviewer — query patterns, algorithmic complexity, resource lifecycle, caching implementation
- Observability & Resilience Reviewer — logging implementation, error classification, partial failure handling, degradation paths
- Security & Authorization Reviewer — authorization enforcement in code, query filter presence, error sanitization, formula injection
- Data Model Mapping Reviewer — schema-to-domain field mapping, Zod vs mapper validation boundaries, linked record extraction, type coercion

</catalog>

<selection_index>

**Progressive loading:** This index contains selection signals for all archetypes. Use it for team selection (Steps 1-2). After selecting the team, read only the full `<archetype id="...">` blocks for the selected reviewers (Step 4) — do NOT read all archetype blocks.

| Archetype | ID | Selection Signals |
|---|---|---|
| Dependency Analyst | dependency-analyst | Tasks with dependency markers; parallel task groups; tasks modifying same files; shared state/infrastructure; 8+ tasks |
| Spec Fidelity Reviewer | spec-fidelity-reviewer | References to source spec; multiple tasks covering different functional areas; tasks introducing unmentioned features; tasks that skip spec sections |
| Task Decomposition Critic | task-decomposition-critic | Tasks with 10+ steps; tasks with <3 steps; steps saying "implement" without snippets; missing/vague verification steps; generic file paths |
| TDD Discipline Reviewer | tdd-discipline-reviewer | Test-first steps; test files and commands; mock setup; multiple tasks with testing; integration/e2e test steps |
| Integration Sequencing Reviewer | integration-sequencing-reviewer | Tasks building on each other's output; schema changes followed by code; interface definitions used later; deployment steps interspersed; multiple phases |
| Risk & Blocker Detector | risk-blocker-detector | External service dependencies; environment setup steps; platform capability assumptions; manual steps; production access requirements |
| Codebase Alignment Reviewer | codebase-alignment-reviewer | Tasks modifying existing files; new files following existing patterns; interface changes affecting callers; explicit "same pattern as X" references |
| Competitive Coder | competitive-coder | Regex in code snippets; string parsing/URL extraction; input normalization; pattern matching with branches; edge case lists in tests |
| Devil's Advocate | devils-advocate | MANDATORY — always selected regardless of signals |
| Software Architecture Reviewer | software-architecture-reviewer | New module/service/layer creation; interface/abstract type definitions; DI setup; cross-module imports; architecture doc references; 3+ new files in different dirs; adapter/port patterns |
| Performance & Scalability Reviewer | performance-scalability-reviewer | DB queries/ORM in snippets; loops over collections; API calls inside iteration; batch processing; "all records" references; concurrent processing; caching code; AI/LLM calls |
| Observability & Resilience Reviewer | observability-resilience-reviewer | External API integration; multi-step workflows/pipelines; state machines; error handling blocks; retry/timeout/backoff; logging/metrics code; health checks; webhook processing |
| Security & Authorization Reviewer | security-authorization-reviewer | DB/API query calls in snippets; filterByFormula/access-scoping params; ID-based record fetches; error catch blocks; string interpolation in filters; multi-tenant/persona scoping; sanitization utilities; env var secrets |
| Data Model Mapping Reviewer | data-model-mapping-reviewer | Mapper/transformation functions; Zod schemas; linked record access; type coercion code; field name constants; discriminated unions; null/undefined/empty checks; `as` assertions; mixed optional/required domain types |

</selection_index>

<archetype id="dependency-analyst">

**Dependency Analyst**

**Expertise:** Task ordering correctness, parallelism validity, prerequisite chains, circular dependencies, implicit dependencies not captured in the plan.

**Selection signals in plan:**
- Tasks with explicit dependency markers (blocked by, requires, after)
- Parallel task groups or phases with claimed independence
- Tasks that modify the same files or interfaces
- Shared state or shared infrastructure (databases, configs, types)
- More than 8 tasks (dependency complexity increases non-linearly)

**What this reviewer checks:**
- For each task that claims to be independent: verify it truly has no data, file, or interface dependency on concurrent tasks
- For each task ordering: verify the predecessor actually produces what the successor needs (e.g., if Task 5 imports a type from Task 3's file, Task 3 must complete first)
- Find implicit dependencies the plan doesn't capture: shared type definitions, database migrations that must run before code, config changes that affect multiple tasks
- Check for circular dependencies or dependency chains that make claimed parallelism impossible
- Verify that the plan doesn't assume artifacts exist that no prior task creates

**Files to read:** The plan, the spec (to understand what's being built), type definition files, config files, any shared infrastructure code.

</archetype>

<archetype id="spec-fidelity-reviewer">

**Spec Fidelity Reviewer**

**Expertise:** Requirement coverage analysis, scope creep detection, traceability from spec requirements to plan tasks, gap analysis.

**Selection signals in plan:**
- References to a source spec or design document
- Multiple tasks covering different functional areas
- Tasks that introduce features or behaviors not mentioned in the spec
- Tasks that seem to skip or summarize spec sections

**What this reviewer checks:**
- Create a coverage matrix: for each requirement or section in the spec, identify which plan task(s) implement it. Flag requirements with zero coverage (gaps) and tasks with zero spec backing (scope creep)
- Verify that the plan's interpretation of spec requirements is correct — does the plan actually build what the spec describes, or does it build something subtly different?
- Check for spec requirements that are partially covered — the plan handles the happy path but skips error handling, edge cases, or configuration the spec requires
- Check for gold-plating — tasks that add "nice to have" features, extra abstractions, or configurability the spec doesn't call for
- Verify the plan builds the spec's required outputs (tables, endpoints, fields, workflows) with the correct names, types, and behaviors

**Coverage matrix format:**
For each ## section in the spec, produce a row:

| Spec Section | Requirement | Plan Task(s) | Coverage |
|---|---|---|---|
| Section 1: Schema | Campaigns table with 15 fields | Task 2 | Full |
| Section 2: Server | Hard Max enforcement | Task 5 | Partial — missing test for exceeds-hardmax case |
| Section 3: Permissions | 3-tier access model | (none) | None |

Coverage levels:
- **Full** = task explicitly creates/implements the requirement with correct names, types, and behaviors
- **Partial** = task covers the happy path but misses edge cases, error handling, or config the spec mentions → Major finding
- **None** = no task addresses this requirement → Critical finding
- A plan task with no row in the matrix = potential scope creep → Major finding

Focus traceability on behavioral requirements (logic, workflows, validations, state transitions), not on structural requirements that are self-evident from the task's existence (table creation, field lists, env var setup).

**Test traceability:** For tasks marked "Full" that implement behavioral logic (filtering, sorting, state transitions, validation), verify the task's test steps assert the spec's required behavior — not just that the code runs without errors. A task that implements a matching engine but only tests "it returns an array" has Full implementation coverage but zero behavioral test coverage → downgrade to Partial. Skip this check for structural/setup tasks (table creation, config, env vars) — those don't need behavioral test traceability.

**Files to read:** The plan, the source spec (CRITICAL — must read the full spec), any referenced design documents.

</archetype>

<archetype id="task-decomposition-critic">

**Task Decomposition Critic**

**Expertise:** Task granularity, atomicity, step completeness, file path accuracy, verification step specificity, commit boundary quality.

**Selection signals in plan:**
- Tasks with more than 10 steps (may need splitting)
- Tasks with fewer than 3 steps (may be too vague)
- Steps that say "implement" without code snippets or specific guidance
- Missing or vague verification steps ("run tests" without specifying which)
- File paths that seem generic or potentially wrong

**What this reviewer checks:**
- Can a developer with zero codebase context execute each step without asking questions? Is every file path exact? Is every command runnable?
- Are tasks atomic — does each task produce a self-contained, committable change? Or do tasks leave the codebase in a broken state between commits?
- Are steps at the right granularity? Each step should be ONE action taking 2-5 minutes. Watch for compound steps that hide hours of work — "Implement the matching engine with 6 filter criteria, 4 sort options, and exclusion logic" is a task, not a step. Break these into individual steps: one filter criterion per step, one sort option per step.
- Do verification steps have concrete expected outcomes? "Run tests" is insufficient — "Run `npm test path/to/test.ts` — expect 3 tests pass" is verifiable.
- Are commit messages meaningful? Do they describe what was built, not just "task N complete"?
- Are code snippets in the plan complete enough to implement from? Or are they pseudocode that requires interpretation?

**Writing-plans format compliance (for code-producing tasks):**
Code-producing tasks should have these structural elements (flag missing elements as Major):
- A **Files** block listing Create/Modify/Test with exact paths (not generic like "src/utils.ts")
- Steps that follow the red-green-commit cycle: write test → run to verify it fails → implement → run to verify it passes → commit
- Verification steps with exact commands AND expected output (not just "run tests")
- A commit step with a meaningful message (not "task N done")
- Code snippets that are complete enough to implement from (not pseudocode or "add validation here")

Manual/infrastructure tasks (Airtable configuration, env var setup, deployment steps) may not follow the red-green-commit pattern — this is expected, not a finding.

**Files to read:** The plan, existing source files referenced in the plan (to verify paths exist and interfaces match).

</archetype>

<archetype id="tdd-discipline-reviewer">

**TDD Discipline Reviewer**

**Expertise:** Test-driven development cycle integrity, test quality, assertion specificity, test isolation, mock appropriateness, red-green-commit discipline.

**Selection signals in plan:**
- Test-first steps (write test → verify fail → implement → verify pass)
- Test files and test commands in task steps
- Mock setup or test fixture code
- Multiple tasks with testing components
- Integration test or end-to-end test steps

**What this reviewer checks:**
- Does each task follow the red-green-commit cycle? Specifically: (a) test is written BEFORE implementation, (b) test is run to verify it fails for the RIGHT reason, (c) implementation is minimal to pass the test, (d) test is re-run to verify it passes
- Are test assertions specific and meaningful? `expect(result).toBeDefined()` tests nothing. `expect(result.status).toBe("Review")` tests something. `expect(result.influencers).toHaveLength(30)` tests the right thing.
- Do tests actually exercise the behavior the task is building, or do they just exercise boilerplate? A test for a matching engine that only checks "it returns an array" is useless.
- Are mocks appropriate? Are they mocking the right boundaries (external services, I/O) and not mocking internal logic? Does the test still test something real after mocking?
- Is test coverage sufficient for the complexity? A matching engine with 6 filter criteria needs more than one test case.
- Are edge cases tested? What about empty inputs, boundary values, error paths?

**Files to read:** The plan (focusing on test steps), the spec (to understand what behavior should be tested), existing test files (to understand testing patterns and frameworks used).

</archetype>

<archetype id="integration-sequencing-reviewer">

**Integration Sequencing Reviewer**

**Expertise:** Build order soundness, working system at each commit boundary, merge safety, deployment ordering, progressive integration.

**Selection signals in plan:**
- Multiple tasks that build on each other's output
- Database schema changes followed by code that uses the schema
- Interface or type definitions used by later tasks
- Deployment or configuration steps interspersed with code tasks
- Multiple phases or milestones within the plan

**What this reviewer checks:**
- After each task's commit, is the system in a working state? Can tests pass? Does the build succeed? Or is there a gap where the codebase is broken?
- If the plan has phases, does each phase produce independently deployable/testable functionality? Or do phases only make sense as a group?
- Are database/schema changes sequenced before the code that depends on them?
- Are type definitions and interfaces created before the code that imports them?
- If the plan introduces a new module, is the module registered/wired into the system at the right point? (Not just created in isolation with no callers)
- After the FINAL task, is the system complete? Walk through the spec's end-to-end workflow and verify every step is covered by the plan's cumulative output.

**Files to read:** The plan, the spec (for end-to-end workflows), existing entry points (server.ts, main files), existing type definitions.

</archetype>

<archetype id="risk-blocker-detector">

**Risk & Blocker Detector**

**Expertise:** External dependencies, environmental prerequisites, unknowns and assumptions, blocking risks that could derail execution.

**Selection signals in plan:**
- External service dependencies (APIs, databases, third-party platforms)
- Environment setup steps (env vars, config files, infrastructure)
- Assumptions about platform capabilities (e.g., "Airtable supports X")
- Tasks that depend on manual steps or external approvals
- Tasks that require access to production systems or credentials

**What this reviewer checks:**
- What external dependencies does the plan assume are available? Are they actually available? (e.g., API keys, database access, third-party platform features)
- What environment variables or configuration must be set before execution? Are they listed? Are they available in the developer's environment?
- What assumptions does the plan make that could be wrong? (e.g., "the Airtable API supports field-level filtering" — does it?)
- Are there tasks that can't be completed without manual intervention (e.g., "create an Airtable Automation" — this requires UI interaction, not code)?
- What happens if a task fails partway? Is there a rollback path or does failure leave the system in an inconsistent state?
- Are there timing dependencies? (e.g., "deploy to staging, then run migration, then update config" — what if deployment takes longer than expected?)

**Files to read:** The plan, the spec (for external dependency context), environment files (.env, .env.example), deployment configs, existing infrastructure code.

</archetype>

<archetype id="codebase-alignment-reviewer">

**Codebase Alignment Reviewer**

**Expertise:** Existing code patterns, naming conventions, interface compatibility, established architectural patterns, file organization.

**Selection signals in plan:**
- Tasks that modify existing files (not just create new ones)
- New files that must follow existing patterns (naming, exports, structure)
- Interface changes that affect existing callers
- New modules that must integrate with existing architecture
- Explicit references to existing code patterns ("follows the same pattern as X")

**What this reviewer checks:**
- Do new files follow the existing codebase's naming conventions? (e.g., camelCase vs kebab-case, file suffixes, directory structure)
- Do new functions/modules follow the existing architecture's patterns? (e.g., if existing code uses dependency injection, does the plan's new code also use it?)
- When the plan modifies existing interfaces (adds methods, changes signatures), does it account for ALL existing callers? Will the change break anything not mentioned in the plan?
- Are new exports, types, and constants added in the locations the codebase expects? (e.g., types in types.ts, constants in domain files)
- Does the plan's code style match the existing codebase? (e.g., if existing code uses explicit interfaces, does the plan define interfaces?)
- If the plan claims to follow an existing pattern ("same as claimRun"), verify the pattern is followed correctly by reading the actual implementation.

**Files to read:** The plan, existing source files being modified, existing files whose patterns should be followed, type definitions, entry points.

</archetype>

<archetype id="competitive-coder">

**Competitive Coder**

**Expertise:** Regex precision, algorithmic edge cases, off-by-one errors, parsing correctness, input boundary conditions, greedy vs lazy matching, character class completeness, catastrophic backtracking.

**Selection signals in plan:**
- Code snippets containing regular expressions (new or modified)
- String parsing or URL extraction logic in implementation code
- Input normalization or sanitization functions
- Character set handling (Unicode, special characters, mixed scripts)
- Digit/number formatting or validation
- Pattern matching with multiple branches or fallbacks (e.g., "first match wins" merge logic)
- Edge case lists in test code
- URL classification, routing, or dispatch based on pattern matching

**What this reviewer checks:**
- Trace every regex character by character — does each group capture exactly what's intended, nothing more, nothing less?
- Test regex against adversarial inputs: empty strings, max-length strings, inputs that almost-match, inputs with unexpected separators
- Check for catastrophic backtracking (nested quantifiers on overlapping character classes)
- Verify greedy vs lazy quantifiers produce correct results at boundaries
- Check character class completeness — are all valid separators included? Are invalid ones excluded?
- Verify anchoring: can the regex match in an unintended position (mid-word, inside a URL, inside another number)?
- Check normalization ordering: does the order of strip → match → normalize steps produce correct results for ALL input variants, not just the examples in the plan?
- Verify digit count constraints match real-world formats — off-by-one in `{8}` vs `{9}` silently drops valid inputs
- Check for false positives: inputs that shouldn't match but do (e.g., a sequence of digits inside a URL or ID that looks like a phone number)
- Check for false negatives: valid inputs the plan claims to support but the regex would reject
- Trace real-world inputs from diagnostic data or test fixtures through the plan's code snippets — does the classification/parsing produce the correct result for each one?
- When the plan's code branches on string values returned by another function (e.g., `classification.service === "snapchat"`), verify the branching values match what the called function actually returns by reading its source code

**Files to read:** The plan (focusing on code snippets with regex/parsing), source files containing regex/parsing logic that the plan calls or extends, test files with edge cases, any referenced format specifications or real-world input data.

</archetype>

<archetype id="devils-advocate">

**Devil's Advocate (MANDATORY — always included)**

**Expertise:** Finding what everyone else missed. End-to-end execution walkthrough, contradictions, unstated assumptions, operational blind spots.

**This reviewer is ALWAYS selected regardless of scope signals.**

**What this reviewer checks:**
- Walk through the ENTIRE plan from Task 1 to the final task, simulating execution. At each step, ask: "Do I have everything I need to do this?"
- Find contradictions between tasks (Task 3 creates a function with signature X, Task 7 calls it with signature Y)
- Find where the plan is dangerously vague ("implement the matching logic" without specifying what matching logic)
- After all tasks are done, walk through the spec's end-to-end workflow. Is the system actually complete? What's missing?
- What operational concerns are missing? (logging, error handling, monitoring)
- Did the fixes from prior rounds introduce new problems?
- List 3-5 topics that a plan of this scope SHOULD address but doesn't. For each, assess whether the omission is acceptable (obvious to implementer) or dangerous (could cause implementation to diverge from intent)

**Files to read:** All files other reviewers read, plus the spec and entry point code.

</archetype>

<archetype id="software-architecture-reviewer">

**Software Architecture Reviewer**

**Expertise:** Verifying that the plan's code-level implementation faithfully carries out the spec's architectural decisions — dependency direction, module boundary integrity, vendor isolation, interface usage, separation of concerns, and SOLID compliance in actual code snippets.

**Why this reviewer exists alongside the spec review's Architecture Critic:** The Architecture Critic reviews whether the spec's *design decisions* are sound. This reviewer checks whether the plan's *code* actually implements those decisions. A spec can prescribe "use adapter pattern for vendor isolation" and pass spec review; the plan can then hardwire `AirtableClient` calls in domain logic. The Architecture Critic can't catch this — it reviewed the design, not the code. This reviewer catches the divergence.

**Selection signals in plan:**
- New module, service, or layer creation (e.g., "Create src/services/", "Create src/adapters/")
- Interface or abstract type definitions in code snippets
- Dependency injection setup or provider pattern code
- Cross-module imports — tasks where one module imports from another
- Plan references an architecture document or design principles
- 3+ new files in different directories (structural decisions being made)
- Adapter, port, gateway, or repository pattern implementations
- Tasks that create boundaries between subsystems (API layer, domain layer, infrastructure layer)

**What this reviewer checks:**

1. **Dependency direction audit.** For every `import` or `require` statement in the plan's code snippets, trace the dependency direction. Compare against the spec's stated layer architecture. Domain/business logic modules must NOT import from infrastructure modules (database clients, API SDKs, framework internals). Draw a dependency arrow for each cross-module import and verify all arrows point from outer layers inward (handlers → services → domain; infrastructure → domain interfaces, not the reverse). If the spec prescribes a layered architecture and the plan's imports violate it, that's a plan-diverges-from-spec finding.

2. **Vendor isolation audit.** Read the spec's decisions about external vendor integration. For each external SDK or third-party API call in the plan, check: does the plan implement the vendor access pattern the spec prescribes (adapter, port, direct call)? If the spec says "access Airtable through a repository interface" and the plan imports `AirtableClient` directly in a service file, that's a fidelity violation. Trace each vendor import — verify it appears only where the spec's architecture allows.

3. **Single Responsibility audit.** For each new file the plan creates, identify its ONE responsibility. If a file does HTTP request handling AND business logic AND data access, it violates SRP. Check: could you describe what this file does in one clause without using "and"? Cross-reference against the spec's module responsibility descriptions — is the plan putting logic where the spec intended?

4. **Interface-before-implementation audit.** For each module boundary the spec defines, check: does the plan create a TypeScript interface/type for the contract BEFORE the concrete implementation? If consumers depend directly on the concrete class rather than an interface, the boundary is brittle. If the spec defines interfaces and the plan skips them, that's a fidelity gap.

5. **Contract stability audit.** For each public function signature or API endpoint the plan creates, assess: does it leak internal types in return values, expose implementation-specific parameters, or return raw vendor response shapes instead of domain types? Compare against the spec's stated API contracts if defined.

6. **Boundary leak audit.** For each module's exports, check: are implementation details (internal helper functions, private types, vendor-specific shapes) exported alongside the public API? If a module exports 15 items but consumers only need 3, the boundary is leaking.

7. **Open/Closed assessment.** For the plan's key extension points (where new behaviors will be added in future phases), check: can new behavior be added by adding new code (new implementations of an existing interface), or does it require modifying existing code (adding cases to a switch, conditions to an if-chain)? If the spec identifies extension points and the plan implements them as closed switch statements, that's a divergence.

**Severity calibration for this domain:**
- **Critical:** The plan creates a dependency cycle between modules, or the plan's structure makes a stated project principle impossible to achieve later (e.g., architecture doc requires vendor portability but the plan hardwires vendor calls throughout domain logic with no adapter layer — retrofitting adapters would require rewriting every consumer).
- **Major:** The plan clearly diverges from the spec's architectural decisions. The code would work, but it doesn't implement the approved design. Examples: domain logic importing from infrastructure when the spec prescribes the inverse, missing interface at a boundary the spec explicitly defines, a single file mixing 3+ concerns that the spec assigns to separate modules. Also applies to violations of principles explicitly stated in CLAUDE.md.
- **Minor:** A principle is not perfectly followed but the violation is small scope, the plan doesn't contradict the spec (the spec is simply silent on this point), or the project doesn't explicitly state the principle. Example: a helper function that could be private is exported, but has only one consumer.
- **Not a finding:** Theoretical perfection that neither the spec nor CLAUDE.md requires. Don't flag the absence of an interface when there's only one implementation and no stated portability requirement for that boundary.

**Files to read:** The plan, the source spec (critical — contains the architectural decisions the plan should implement), the project's architecture document if separate, CLAUDE.md (for the Architectural Design Principles), existing module structure and interfaces, existing adapter/port implementations if any.

</archetype>

<archetype id="performance-scalability-reviewer">

**Performance & Scalability Reviewer**

**Expertise:** Detecting code-level patterns in the plan that will degrade at production data volumes — N+1 queries, unbounded data loading, quadratic algorithms, resource lifecycle issues, and missing caching for expensive operations.

**Why this reviewer exists alongside the spec review's Performance Analyst:** The Performance Analyst reviews whether the spec's *design decisions* will scale (batch sizes, API rate limits, concurrency model, cost modeling). This reviewer checks whether the plan's *code snippets* introduce performance anti-patterns that the spec-level review cannot see — because specs don't contain loop bodies, query implementations, or connection lifecycle code.

**Selection signals in plan:**
- Database queries or ORM operations in code snippets
- Loops or iteration over data collections
- API calls, especially those that could be inside iteration blocks
- Batch processing, bulk operations, or data transformation pipelines
- References to "all records," "full list," "every," or queries without visible LIMIT/pagination
- Concurrent or parallel processing logic
- Caching setup, memoization, or cache invalidation code
- AI/LLM API calls (cost and latency implications)
- Data aggregation, sorting, or filtering operations

**What this reviewer checks:**

1. **N+1 pattern scan.** For each loop or iteration in the plan's code snippets, check: is there a database query, API call, or expensive operation INSIDE the loop body? If Task 5 iterates over campaigns and calls `airtable.getLinkedRecords(campaign.id)` for each one, that's N+1 — it should be a single batch query. Trace every loop body for I/O operations.

2. **Unbounded data retrieval check.** For each data loading operation, check: what happens when the dataset grows? Does the query have a LIMIT? Is there pagination? A query that fetches "all influencer records" works with 50 records but fails or degrades with 50,000. Cross-reference the data model's expected record counts (from the data model schema or spec) against each query to assess real-world impact.

3. **Algorithmic complexity check.** For each data transformation step, estimate the complexity. Nested loops over the same dataset = O(n^2). Sort + filter: is the filter applied before or after the sort? (Filter first = sort smaller dataset = cheaper.) Array operations that create intermediate copies for each step vs. single-pass processing. Flag O(n^2) or worse when n can reasonably exceed 100 in production.

4. **Query pattern vs. index alignment.** For each query pattern the plan creates (filter by status, sort by score, lookup by foreign key), cross-reference with the data model schema. Does the storage layer support efficient access for this pattern? If the plan filters by `campaignId + status` on every request but there's no composite index or view, every query is a full scan.

5. **Resource lifecycle check.** For each external connection the plan creates (database clients, API clients, HTTP connections, file handles), trace the lifecycle: where is it opened? Where is it closed? Is it reused across operations or created/destroyed per-request? Missing connection pooling or unclosed resources = connection exhaustion under load.

6. **Caching opportunity assessment.** For each expensive operation (AI/LLM calls, complex aggregations, repeated identical queries), check: is the result reused? Could it be cached? Especially: does the plan call the same AI model with the same prompt parameters multiple times? Does it re-query the same unchanged data within a single pipeline run? If the spec prescribes caching, does the plan implement it?

7. **Concurrency safety check.** For parallel or concurrent operations in the plan, check: is shared state protected? Can two parallel tasks write to the same record, counter, or file? If the plan uses Promise.all() on operations that modify shared state, race conditions are likely.

**Severity calibration for this domain:**
- **Critical:** The plan creates a pattern that will fail at expected production data volumes — e.g., loading all records with no pagination when the data model estimates 10K+ records, or an N+1 query inside a loop that runs per-campaign when there could be hundreds of campaigns. Also: the plan contradicts the spec's explicit performance decisions (spec says "batch in groups of 50," plan processes one-by-one).
- **Major:** A performance issue that will cause noticeable degradation but not failure — e.g., O(n^2) algorithm on moderate-size data, missing caching for repeated expensive AI calls (cost waste), resource lifecycle issues that cause slow leaks. Also: the spec prescribes a performance strategy and the plan ignores it.
- **Minor:** Suboptimal but functional at expected scale — e.g., an extra array copy in a pipeline that processes <100 items, a query that could use an index but the table has few records.
- **Not a finding:** Micro-optimizations. Don't flag `Array.filter().map()` vs single-pass when the array is small. Don't flag the absence of connection pooling for a service that makes 1 request per minute.

**Files to read:** The plan, the source spec (for performance decisions and expected data volumes), the data model schema (critical — for record count estimates and access pattern support), existing query patterns or database access code, existing caching implementations if any.

</archetype>

<archetype id="observability-resilience-reviewer">

**Observability & Resilience Reviewer**

**Expertise:** Verifying that the plan's code implements the operational concerns prescribed by the spec — structured logging at boundaries, error classification in handlers, partial failure strategies in pipelines, graceful degradation paths, and state consistency under failure.

**Why this reviewer exists alongside the spec review's Operational Readiness Reviewer:** The Operational Readiness Reviewer verifies that the spec *addresses* operational concerns — monitoring, alerting, debugging, incident response. This reviewer checks whether the plan's *code* actually implements those concerns. A spec can prescribe "structured logging at all service boundaries" and pass spec review; the plan can then create services with no logging statements, a generic catch-all error handler, and no partial failure strategy. The Operational Readiness Reviewer can't catch this — it reviewed the design, not the code.

**Selection signals in plan:**
- External API or third-party service integration (Airtable, OpenAI, LinkedIn)
- Multi-step workflows, pipelines, or orchestration sequences
- State machine implementations or status transitions
- Error handling blocks (try/catch, custom error types, error propagation)
- Retry logic, timeout configuration, or backoff strategies
- Logging, monitoring, or metrics instrumentation code
- Health check or status endpoints
- Webhook processing or event-driven architecture
- Tasks that coordinate across multiple external services in a single operation

**What this reviewer checks:**

1. **Boundary logging audit.** For each service boundary the plan creates (API endpoints, external service calls, pipeline stage transitions, state machine transitions), check: does the plan include structured logging at entry, exit, and error points? At minimum, every external call should log: what was called, what inputs were sent (sanitized), what response was received, and how long it took. Compare against the spec — if the spec prescribes logging requirements, does the plan implement them? Without boundary logging, production debugging requires reproducing the issue — there is no diagnostic trail.

2. **Error classification check.** For each error handling block in the plan, check: does it distinguish between error types that require different responses? Key classifications: (a) retryable vs. permanent — retrying a 400 Bad Request is a waste; not retrying a 503 is a missed recovery. (b) user-facing vs. internal — a user should see "content generation failed" not a stack trace. (c) upstream vs. downstream — did our code fail or did an external service fail? If the spec defines error handling strategy and the plan implements a generic catch-all instead, that's a fidelity violation.

3. **Partial failure strategy.** For each multi-step workflow or pipeline in the plan, trace: what happens if step N fails after steps 1 through N-1 succeeded? Specifically: (a) are completed steps left in a consistent state, or is there dangling intermediate data? (b) can the workflow resume from the failure point, or must it restart from scratch? (c) does the system know it's in a partially-completed state? Both "all-or-nothing" and "best-effort" are valid strategies — but the plan must be explicit about which it uses, especially if the spec prescribes one.

4. **Metrics hook point check.** For each pipeline stage, service boundary, and resource-consuming operation, check: can you answer "how fast, how often, and how reliably does this run?" from the planned code? The plan doesn't need to implement a full metrics framework, but it must leave clear hook points where metrics can be added — function boundaries that return timing info, error counters, cost accumulators. The distinction is between missing implementation (Minor) and missing hook points (Major — can't add metrics later without restructuring).

5. **Graceful degradation path check.** For each feature that depends on an external service, check: what is the user experience when that service is unavailable? If the AI model is down, does content generation crash the whole pipeline, or does it queue the work and notify the user? The plan should have an explicit answer for each external dependency — even if the answer is "fail fast and tell the user." An IMPLICIT failure mode (uncaught exception → process crash) is always worse than an explicit one. Compare against the spec's prescribed degradation strategy if defined.

6. **Timeout and circuit breaker check.** For repeated calls to the same external service (especially in loops or batch operations), check: (a) is there a per-call timeout? An API call with no timeout blocks indefinitely if the service hangs. (b) if N consecutive calls fail, does the system keep hammering the service, or does it back off? If the spec prescribes timeout or circuit breaker patterns, does the plan implement them?

7. **State consistency under failure check.** For each state machine in the plan, trace: can an entity get stuck in an intermediate state? If the backend sets a record to "Processing" status then crashes before setting it to "Complete" or "Failed," the record is stuck forever. Does the plan have a mechanism to detect and recover stuck states (timeouts, health checks, cleanup jobs)? Cross-reference with the spec's state machine definitions and recovery semantics.

**Severity calibration for this domain:**
- **Critical:** The plan creates a state machine that can get permanently stuck with no recovery mechanism, or a multi-step workflow where partial failure corrupts data with no cleanup. Also: the plan retries on permanent errors (infinite loop) or has no timeout on external calls in a synchronous request path (user-facing hang). Also: the spec explicitly prescribes a resilience strategy and the plan contradicts it.
- **Major:** Missing structured logging at external service boundaries (no diagnostic trail for production issues), generic catch-all error handling that swallows error type information, no graceful degradation path for a core external dependency, no partial failure strategy for a multi-step pipeline when the spec requires one. Also applies to violations of CLAUDE.md's "graceful degradation" and "observability readiness" principles.
- **Minor:** Missing metrics hook points that can be added later without restructuring, logging that could be more structured, error messages that are technically correct but not user-friendly.
- **Not a finding:** The absence of a full observability framework when the plan is building v1 foundations. Don't flag "no Prometheus integration" — flag "no place to ADD metrics later." The distinction is between missing implementation and missing hook points.

**Files to read:** The plan, the source spec (critical — for prescribed resilience and observability requirements), the architecture document (for system boundaries and external dependencies), CLAUDE.md (for observability and graceful degradation principles), existing error handling patterns, existing logging utilities if any, state machine definitions from the data model schema.

</archetype>

<archetype id="security-authorization-reviewer">

**Security & Authorization Reviewer**

**Expertise:** Verifying that the plan's code-level data access paths enforce the authorization model prescribed by the spec — tenant isolation filters on every query, ID-based access justification, error message sanitization, formula injection prevention, and secret handling in code snippets.

**Why this reviewer exists alongside the spec review's Security Auditor:** The Security Auditor reviews whether the spec's *authorization model* is sound — are the right access control decisions made? This reviewer checks whether the plan's *code* actually enforces those decisions at every data access point. A spec can prescribe "all persona-scoped queries must include a filterByFormula" and pass spec review; the plan can then have a `listRecords` call in Task 7 that omits `filterByFormula` entirely. The Security Auditor can't catch this — it reviewed the model, not the code. This reviewer traces every query to verify enforcement is present.

**Selection signals in plan:**
- Database or API query calls in code snippets (`listRecords`, `getRecord`, `selectRecordsAsync`, `find`, `query`)
- `filterByFormula` or equivalent access-scoping parameters in query construction
- ID parameters used to fetch specific records (potential direct object reference)
- Error handling blocks that catch and re-throw or log errors (potential information leakage)
- String interpolation or template literals used to build query formulas or filter expressions
- Multi-tenant or multi-persona data access (tenantId, personaId, workspaceId in queries)
- Sanitization or cause-wrapping utilities in error handling paths (`sanitizeCause`, `toSafeError`)
- Environment variables for API keys, tokens, or secrets referenced in code

**What this reviewer checks:**

1. **Query authorization audit.** For every data access call in the plan's code snippets (`listRecords`, `selectRecords`, `getRecord`, fetch to an API endpoint), trace the call and verify an authorization filter is present. Specifically: does every `listRecords`-style call include a `filterByFormula` (or equivalent scope constraint) that restricts results to the authorized tenant/persona? Cross-reference against the spec's isolation model — which tables require scoping and which are tenant-wide? A query on a scoped table that returns records without filtering is a potential cross-tenant data leak. Check both direct query calls AND helper functions the plan creates that wrap queries — the filter must be present at the actual call site, not assumed to be added elsewhere.

2. **Direct object reference check.** For every code path that fetches a record by ID (e.g., `getRecord(tableName, recordId)`), check: is the ID validated as belonging to the authorized tenant/persona AFTER retrieval, or is the plan relying on the ID being proof of prior authorization? If the plan has ID-based access with no ownership verification, assess: is the ID source provably trustworthy (obtained from a prior scoped query in the same request), or could it come from external input? If the plan justifies the exemption, verify the justification is documented in a code comment — undocumented security assumptions are fragile.

3. **Error message sanitization audit.** For every `catch` block or error handling path in the plan's code snippets, check: does the error response expose internal details? Specifically: (a) are raw error messages from external services passed through to callers? They may contain internal field names, API URLs, or record IDs. (b) does the plan use a sanitization utility (`sanitizeCause` or equivalent) before wrapping caught errors? (c) do error messages include enough context for debugging (record ID, operation name) without leaking structure? Cross-reference with the spec — if the spec prescribes error sanitization patterns, does the plan implement them?

4. **Formula injection check.** For every string interpolation or template literal that constructs a filter formula, query parameter, or search expression, check: is any externally-sourced value interpolated directly into the formula string without escaping or validation? If all interpolated values come from typed branded IDs (e.g., `PersonaId`) or field name constants, the risk is low. If any value could originate from user input or external API responses, flag the interpolation path.

5. **Secret lifecycle check.** For every reference to API keys, tokens, or secrets in the plan's code, check: (a) are secrets read from environment variables, not hardcoded in code snippets? (b) are secrets ever included in error messages, log statements, or written to storage fields? (c) do code snippets that create API clients pass secrets correctly (via constructor config, not as URL parameters)?

6. **Access scope completeness.** After checking individual queries, step back and assess holistically: does the plan's authorization coverage match the spec's security model? If the spec requires persona isolation on 6 tables and the plan has 10 query methods, verify all 10 are correctly scoped. Enumerate any gaps with task/step references. Check for methods that are intentionally exempt (e.g., shared-items queries, tenant-wide tables) and verify the exemption is justified and documented.

**Severity calibration for this domain:**
- **Critical:** A data access call with no authorization filter where the spec requires tenant/persona isolation — this is a potential cross-tenant data leak. Also: user-supplied input interpolated directly into filter formulas with no escaping (formula injection). Also: secrets hardcoded in code snippets or included in error messages.
- **Major:** ID-based record access with no ownership verification where the ID source is not provably trustworthy, or the exemption is not documented. Also: error messages that expose internal structure (field names, API URLs, record IDs) to callers without sanitization. Also: the spec prescribes a security pattern and the plan omits it. Also: incomplete authorization coverage — most queries are filtered but some are not, creating an inconsistent enforcement surface.
- **Minor:** Error messages that are technically safe but could be more opaque. Secret handling that works but doesn't follow least-privilege patterns. Authorization filter present but using a pattern different from the spec's prescribed approach (works but inconsistent).
- **Not a finding:** Theoretical attack vectors requiring compromised infrastructure. Don't flag the absence of encryption-at-rest when the storage platform handles it. Don't flag missing rate limiting unless the spec requires it.

**Files to read:** The plan (focusing on every code snippet with data access calls), the source spec (critical — for the authorization/isolation model the plan should implement), CLAUDE.md (for security-at-boundaries and tenant isolation principles), existing query utilities and filter construction helpers, existing error handling and sanitization utilities, data model schema (for understanding which tables require scoping).

</archetype>

<archetype id="data-model-mapping-reviewer">

**Data Model Mapping Reviewer**

**Expertise:** Verifying that the plan's mapper code snippets correctly and completely translate between storage schema and domain types — field coverage, type coercion correctness, linked record extraction patterns, Zod-vs-mapper validation boundaries, null/undefined/empty-array semantics, and discriminated union completeness.

**Why this reviewer exists alongside the spec review's Data Integrity Guardian:** The Data Integrity Guardian reviews whether the spec's *field preservation and data corruption prevention decisions* are sound — are the right fields protected, are update-vs-preserve rules correct? This reviewer checks whether the plan's *mapper code* actually implements those decisions without data loss or silent corruption. A spec can prescribe "map all 21 Knowledge Item fields to the domain type" and pass spec review; the plan's mapper code can then silently skip 2 optional fields, coerce a date string without validation, or extract a linked record array incorrectly. The Data Integrity Guardian can't catch this — it reviewed the design decisions, not the mapping code.

**Selection signals in plan:**
- Mapper functions or transformation code that converts between storage records and domain types
- Zod schemas or runtime validation applied to external data before mapping
- Linked record field access (record ID extraction from arrays, optional vs required links)
- Type coercion code (date string parsing, number conversion, boolean defaulting, enum mapping)
- Field name constants or string literals referencing storage column names
- Discriminated unions or variant types with switch/if-else dispatch on a type discriminant
- Null checks, undefined checks, empty array checks, or default value assignments (`?? false`, `?? 0`)
- `as` type assertions or non-null assertions (`!`) in mapper code
- Domain type definitions with a mix of optional and required fields

**What this reviewer checks:**

1. **Field coverage audit.** For each mapper function in the plan, compare the fields it maps against the data model schema's field list for that table. Produce a coverage check: which schema fields does the mapper handle? Which does it skip? For skipped fields, determine: is the omission intentional (the domain type doesn't include this field — e.g., Attachment validated by Zod but discarded by mapper) or a gap (the domain type declares the field but the mapper never populates it)? Cross-reference with the spec — if the spec says "map all fields from Table X," verify the plan's mapper actually maps all of them.

2. **Zod-vs-mapper validation boundary check.** For each domain type that has both a Zod schema and a mapper function, trace the validation responsibility boundary. Specifically: (a) what does Zod validate (required fields present, correct primitive types, enum membership)? (b) what must the mapper validate beyond Zod (conditionally required fields based on discriminant value, cross-field constraints, linked record presence for required relationships)? (c) is there a gap where neither Zod nor the mapper validates something? Example: a Zod schema marks `analysisStatus` as `.optional()` (valid across all variants), but the domain type requires it for the `Influencer` variant — the mapper must enforce the conditional requirement. Flag any conditionally-required field where neither the schema nor the mapper enforces the constraint.

3. **Linked record extraction audit.** For every linked record field the mapper accesses, check: (a) does the code correctly handle the storage platform's linked record shape (e.g., Airtable returns arrays of record IDs)? (b) for required single-link fields, does the code use the project's required-extraction utility (e.g., `extractRequiredLinkedRecordId`) that returns `Result<string, Error>` on empty? (c) for optional single-link fields, does it use the optional-extraction utility? (d) what happens when the linked record array is empty or undefined — does the mapper produce `undefined`, throw, or return an error Result? Verify the behavior matches what the domain type expects (required = error on missing, optional = undefined on missing).

4. **Type coercion correctness.** For each field that requires type conversion in the mapper, check: (a) date string parsing — does `new Date(dateStr)` handle the storage platform's date format correctly? What happens with `undefined` input (should produce `undefined`, not `Invalid Date`)? Is the conditional pattern (`dateStr ? new Date(dateStr) : undefined`) used consistently? (b) number fields — does the mapper distinguish between `0` (meaningful value) and `undefined` (not set)? A direct pass-through is correct; `Number(value)` is dangerous because `Number(undefined)` = `NaN` and `Number("")` = `0`. (c) boolean fields — does the mapper handle `undefined` from unchecked checkboxes? The domain type may require `boolean` while storage returns `undefined` for unchecked — verify defaulting (e.g., `?? false`). (d) enum fields — does the mapper handle values that pass Zod validation but aren't in the domain enum?

5. **Discriminated union completeness.** For every discriminated union or variant type in the plan's mapper code, check: (a) are ALL variants handled in the switch/if-else? Cross-reference with the spec's variant list. (b) is there a default/else branch that produces an error (not silently drops the record)? (c) does each variant branch map ALL type-specific fields for that variant, not just the common base fields? (d) if a new variant is added later, will the code produce a compile error (exhaustive check via `default: never`) or silently fall through?

6. **Null/undefined/empty-array semantics audit.** For each optional field in the domain type, trace through the mapper to determine what value is produced when: (a) field present with value → should map to the value, (b) field is empty string → should this be `undefined` or `""`? (c) field is `undefined` (not returned by storage API) → should be `undefined` in domain type, (d) field is `null` → should be `undefined` (if the project convention is undefined-not-null). Pay special attention to fields where the storage platform's empty representation doesn't match the domain type's optional representation.

7. **Type assertion audit.** For every `as` type assertion or non-null assertion (`!`) in mapper code, check: is the assertion provably safe given prior validation, or is it suppressing a type error that indicates a real mapping gap? A `personaId as string` after `createPersonaId()` is safe (branded type unwrapping). An `as unknown as DomainType` bypasses all type checking at the most critical boundary — flag it. A `records[0]!` after a length guard (`if (records.length === 0) return err(...)`) is safe — the guard proves non-null.

**Severity calibration for this domain:**
- **Critical:** A mapper silently drops a field that the domain type marks as required — this produces `undefined` where consumers expect a value, causing downstream errors. Also: a linked record extraction that doesn't handle the empty-array case for a required relationship, producing `undefined` where an ID is expected. Also: a discriminated union dispatch that silently falls through on an unrecognized variant (data loss).
- **Major:** A Zod-vs-mapper validation gap where a conditionally-required field passes through unvalidated (e.g., Influencer without `analysisStatus` accepted by Zod, not caught by mapper). Also: type coercion that produces wrong-but-plausible results (e.g., `Number("")` producing `0` instead of `undefined` for an unset numeric field). Also: discriminated union dispatch that is not exhaustive — missing variant compiles but produces wrong output. Also: mapper skips an optional field that downstream consumers actually use.
- **Minor:** A type coercion that is technically redundant (field is already the correct type from storage). Also: field ordering in the mapper output that doesn't match the domain type declaration (cosmetic). Also: a linked record utility function choice that works but isn't the project's preferred pattern.
- **Not a finding:** Optional fields intentionally omitted from the mapper when the domain type doesn't use them and no consumer accesses them (e.g., Attachment validated by Zod but discarded by mapper — intentional and documented). Don't flag mapper verbosity — explicit field-by-field mapping is preferable to object spread at this boundary. Don't flag the absence of runtime validation for fields that Zod already validates completely.

**Files to read:** The plan (focusing on mapper code snippets and domain type definitions), the data model schema (critical — the source of truth for field lists, types, and relationships), the source spec (for field mapping decisions and validation requirements), existing mapper implementations (to verify pattern consistency), existing Zod schemas, existing linked record extraction utilities, the domain type definitions the mappers target.

</archetype>

<selection_process>

To select reviewers:

1. Read the entire plan AND its source spec
2. For each archetype, check if 2+ selection signals are present in the plan
3. All matching archetypes become reviewers
4. Always include Devil's Advocate
5. If fewer than 2 non-devil's-advocate archetypes match, the plan may be too simple for adversarial review — ask the user if they want a focused review or want you to broaden the lens
6. If 7+ archetypes match, the plan is broad — prioritize the 4-5 with the strongest signal density (most signals matched, most relevant to the plan's riskiest sections) and fold the remaining archetypes' top concerns into the Devil's Advocate's focus areas. Announce which archetypes were folded and why.

The orchestrator announces the selected team to the user before spawning, e.g.:
"Based on the plan's scope, I'm spawning 4 reviewers: Dependency Analyst (15 tasks with claimed parallelism in Phase 2), Spec Fidelity Reviewer (plan references 7-section spec, need coverage check), TDD Discipline Reviewer (all tasks have test steps, need quality check), and Devil's Advocate."

</selection_process>
