<catalog>

The orchestrator selects reviewers by scanning the plan for **scope signals** — task count, subsystem breadth, technology mix, dependency complexity, and structural patterns that indicate which areas of expertise are needed. Each archetype below lists its selection signals.

The orchestrator MUST NOT default to a fixed count. Select as many reviewers as the plan's dimensions demand, plus the mandatory Devil's Advocate. Typical range: 3-5 total.

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

</catalog>

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
