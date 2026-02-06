---
name: plan-phase-tasks
description: Use when breaking a roadmap phase into implementable tasks with FDD decomposition. Use when user says "plan phase", "decompose phase", "break down phase", "plan phase tasks", or needs task-level planning from ROADMAP.md phases.
---

<objective>
**Phase Task Decomposition Skill**

Transform one roadmap phase into an implementable PHASE-N-PLAN.md using Feature-Driven Development (FDD) task decomposition with explicit Input/Output/Test per task, ordered Domain → Application → Adapters.

**Invocation:** Once per phase. Each invocation is self-contained — reads shared upstream artifacts and produces one `.charter/PHASE-N-PLAN.md`. Phases within the same wave can be planned in parallel.

**Inputs:**

| Input | Condition | Key Content |
|-------|-----------|-------------|
| **ROADMAP.md** | Always | Phase block, wave header, release transitions, Definition of Done |
| **USER-STORIES.md** | Always (via trace script) | US-XXX stories with acceptance criteria for this phase |
| **ARCHITECTURE-DOC.md** | Always | Domain model, layers, interfaces, constraints |
| **Design OS export** | `--has-ui` AND export exists | Section paths referenced in task descriptions (preferred) |
| **UX docs + DESIGN-TOKENS.md** | `--has-ui` AND no export | UX specs filtered via traceability matrix (fallback) |

**Output:** `.charter/PHASE-N-PLAN.md` (~150-400 lines; walking skeleton phases with many stories trend upper bound)

**Template:** `templates/phase-plan-template.md`

**Downstream consumer:** `superpowers:writing-plans` transforms each story's task tree into TDD implementation steps (RED-GREEN-REFACTOR). `superpowers:executing-plans` then executes with `superpowers:test-driven-development` enforcing non-negotiable TDD.

**Pipeline position:**
```
/create-roadmap → ROADMAP.md
/create-requirements → USER-STORIES.md
/create-design-doc → ARCHITECTURE-DOC.md
                          ↓ (all three)
              /plan-phase-tasks N [--has-ui]
                          ↓
              .charter/PHASE-N-PLAN.md
                          ↓
              superpowers:writing-plans
```
</objective>

<quick_start>
**Usage:**
```
/plan-phase-tasks 1
/plan-phase-tasks 3 --has-ui
```

- First argument (required): Phase number (1-based, sequential across all releases)
- `--has-ui` flag (optional): Load UX inputs for phases with UI stories

**What happens:**
1. Runs `trace-phase-stories.py` to get this phase's user stories from ROADMAP.md → USER-STORIES.md
2. Progressively loads relevant sections from ROADMAP.md and ARCHITECTURE-DOC.md
3. If `--has-ui`: loads Design OS export sections (preferred) or UX docs (fallback)
4. Decomposes each user story into FDD tasks (Domain → Application → Adapters)
5. Analyzes story independence for parallel execution
6. Writes `.charter/PHASE-N-PLAN.md` using the template
</quick_start>

<essential_principles>

**FDD Task Decomposition Pattern**

Each story decomposes into tasks following Clean Architecture layer order. Not every story touches all three layers — the structure is a maximum, not a mandate:

```
Story US-XXX: [Story Name]
├── Layer: Domain
│   └── Task 1: Create [Entity/Value Object]
│       ├── Input: Requirements from acceptance criteria
│       ├── Output: Tested domain object
│       └── Test: Unit tests for validation rules
├── Layer: Application
│   └── Task 2: Create [Use Case/Handler]
│       ├── Input: Domain objects, interface contracts
│       ├── Output: Working use case
│       └── Test: Unit tests with mocked dependencies
└── Layer: Adapters
    └── Task 3: Create [Adapter Implementation]
        ├── Input: Interface contract from domain
        ├── Output: Working adapter
        ├── Test: Integration tests
        └── Reference: design-os-export/sections/[section-name]/
```

- UI-only stories may have only Adapters tasks
- Data pipeline stories may skip Application
- `Reference:` field only for UI tasks when Design OS export exists
- When `--has-ui` but no export: embed UX specs in task `Input:` field instead

**Atomic Tasks for AI Execution**

Each task must be small enough for one agent to complete in one session:
- One task = one file or one function
- Explicit I/O = clear success criteria
- Test-first = verifiable correctness (TDD via superpowers downstream)
- Atomic commits = rollback points

**Scripts Handle Deterministic Tracing**

Two companion scripts handle text-matching operations. The LLM never searches USER-STORIES.md or UX-FLOWS.md directly.

| Script | Purpose | When Run |
|--------|---------|----------|
| `trace-phase-stories.py` | ROADMAP.md phase → filtered user stories | Every invocation |
| `generate-section-manifest.py` | Design OS sections → US-XXX story IDs | Auto if manifest.json missing |

Scripts are co-located at: `~/.claude/plugins/marketplaces/claude-forge/skills/plan-phase-tasks/scripts/`

**Progressive Loading**

Input documents can total 2,400+ lines combined. Never read entire files. Use targeted `Grep` for headers, then `Read` with `offset`/`limit` for specific sections.

</essential_principles>

<intake>

**Argument Parsing:**
1. Split `$ARGUMENTS` by spaces
2. First token = phase number (required, integer)
3. If `--has-ui` present anywhere in arguments = load UX inputs
4. If phase number is missing or non-numeric: error with usage example

**Validation:**
1. Verify `.charter/ROADMAP.md` exists — if missing: "ROADMAP.md not found. Run `/create-roadmap` first."
2. Verify `.charter/USER-STORIES.md` exists — if missing: "USER-STORIES.md not found. Run `/create-requirements` first."
3. Verify `.charter/ARCHITECTURE-DOC.md` exists — if missing: "ARCHITECTURE-DOC.md not found. Run `/create-design-doc` first."
4. If `--has-ui` set, verify at least one UX source exists:
   - `.charter/design-os-export/` directory (preferred)
   - OR `.charter/UX-DESIGN-PLAN.md` (fallback)
   - If neither: warn user and continue without UX inputs

Proceed to Phase 1.

</intake>

<phase_1_trace_stories>
**Phase 1: Trace Phase Stories**

Run the companion script to extract this phase's user stories:

```bash
python3 ~/.claude/plugins/marketplaces/claude-forge/skills/plan-phase-tasks/scripts/trace-phase-stories.py {phase-number} .charter/ROADMAP.md .charter/USER-STORIES.md
```

**Parse the output:**
- Read `**SM-XXX IDs in this phase:**` line for source story map IDs
- Read `**US-XXX IDs in this phase:**` line for derived user story IDs (regex: `\*\*US-XXX IDs in this phase:\*\* (.*)`, split by whitespace)
- Read full story blocks with acceptance criteria
- Check warnings for missing SM-XXX → US-XXX mappings

If the script reports missing SM-XXX IDs (no matching US-XXX stories), warn the user: some story map items have no corresponding user stories. They may need to run `/create-requirements` to generate them.

Save the script output — it becomes the user stories context for task decomposition.

</phase_1_trace_stories>

<phase_2_progressive_loading>
**Phase 2: Load Upstream Context**

**2.1 ROADMAP.md — Phase Block + Wave Header**

Use `Grep` to find `#### PHASE-{N}:` heading, then `Read` with offset/limit to load:
- The target phase's `#### PHASE-N:` block (stories assigned, scope description)
- Its containing `### Wave` header (wave number, parallel/sequential label)
- The parent release's Transitions and Definition of Done sections
- The Quick Reference table at the top of the file
- The `## Cross-Release Dependencies` table (phase-to-phase dependency chains across releases)

Skip: Other releases, sibling phases in other waves.

**Extract wave metadata** from the `### Wave` header using regex:
- Wave: `^### Wave (\d+) \(([^)]+)\)` → captures wave number and label
- Phase: `^#### PHASE-(\d+):` → captures phase number

**2.2 ARCHITECTURE-DOC.md — Targeted Sections**

Use `Grep` for `^##` headers, then `Read` only:
- **Domain Model** — entity relationships, dependencies
- **Architecture Layers** — layer separation rules
- **External Interfaces** — the `###` subsection under System Context
- **Key Interfaces** — contracts between layers
- **Constraints** — technical limits

Skip: C4 diagrams, ADRs, Quality Attributes, full implementation details.

</phase_2_progressive_loading>

<phase_3_ux_inputs>
**Phase 3: Load UX Inputs (only when `--has-ui` is set)**

Skip this entire phase if `--has-ui` was not provided. Set metadata: `UX Inputs Loaded: N/A — --has-ui not set`.

**3.1 Check for Design OS Export (Preferred Path)**

Check if `.charter/design-os-export/` directory exists.

**If export exists:**

1. Check for `manifest.json` in the export directory
2. If `manifest.json` is missing, auto-generate it:
   ```bash
   python3 ~/.claude/plugins/marketplaces/claude-forge/skills/plan-phase-tasks/scripts/generate-section-manifest.py \
       --export-dir .charter/design-os-export \
       --ux-flows .charter/UX-FLOWS.md \
       --output .charter/design-os-export/manifest.json
   ```
   If generation fails (e.g., missing `OPENAI_API_KEY`): emit error "Design OS export found but manifest.json generation failed. Ensure OPENAI_API_KEY is exported in your shell environment, then retry." **Stop execution — do not proceed to Phase 4.**
3. Read `manifest.json` and look up which sections contain US-XXX IDs from the trace script output
4. For each matched section, note the section directory path (e.g., `design-os-export/sections/hook-catalog/`)
5. Do NOT load any Design OS content at planning time — only reference section paths
6. Set metadata: `UX Inputs Loaded: Yes — Design OS export (sections: {matched-section-names})`
7. UX docs and DESIGN-TOKENS.md are skipped — the export supersedes them

**3.2 UX Docs Fallback (When Export Does Not Exist)**

If `.charter/design-os-export/` does not exist, fall back to loading UX docs:

1. **Lookup:** Load UX-FLOWS.md Section 11 (traceability matrix) to find which UX elements map to this phase's US-XXX story IDs
2. **Identify:** Use those mappings to determine which pages, components, interactions, and flows are affected
3. **Load filtered content:** Read only the identified sections from:
   - UX-DESIGN-PLAN.md — page layout wireframes for affected pages
   - UX-COMPONENTS.md — component specs referenced by affected stories
   - UX-INTERACTIONS.md — interaction patterns and responsive specs for affected components
   - UX-FLOWS.md — accessibility specs for affected components
   - DESIGN-TOKENS.md — load entire file (manually provided input with spacing, typography, color tokens)
4. **Discard lookup:** Section 11 traceability matrix is not included in final planning context
5. Set metadata: `UX Inputs Loaded: Yes — UX-DESIGN-PLAN.md, UX-COMPONENTS.md, UX-INTERACTIONS.md, UX-FLOWS.md, DESIGN-TOKENS.md (filtered via traceability matrix); Design OS export not available`

**3.3 Traceability Fallback**

If `--has-ui` is set, no export exists, and the traceability matrix yields NO matching UX sections for this phase's story IDs: skip UX docs entirely.
Set metadata: `UX Inputs Loaded: No — traceability matrix has no entries for this phase's stories; UX patterns deferred to superpowers:writing-plans`

</phase_3_ux_inputs>

<phase_4_task_decomposition>
**Phase 4: FDD Task Decomposition**

For each user story from the trace script output:

**4.1 Analyze Story Scope**

Read the story's acceptance criteria carefully. Determine which architecture layers this story touches:
- **Domain** — new entities, value objects, validation rules, business logic
- **Application** — use cases, handlers, orchestration, interface definitions
- **Adapters** — UI components, API routes, data fetching, external service integrations

Not every story needs all three layers. Assign only the layers that are genuinely needed.

**4.2 Decompose into Tasks**

For each layer the story touches, create one or more tasks following the FDD pattern:

- **Task name:** Specific action — "Create Hook entity", "Implement GitHub API adapter", not "Set up backend"
- **Input:** What the task needs to start — AC requirements, domain objects, interface contracts, upstream task outputs
- **Output:** What the task produces — tested object, working adapter, rendered component
- **Test:** What to verify — unit tests, integration tests, specific assertions
- **Reference:** (UI tasks only, when Design OS export exists) Path to the relevant section directory

**4.3 Layer Ordering**

Within each story, tasks follow dependency order: Domain → Application → Adapters. This respects Clean Architecture dependency rules:
- Domain has no dependencies
- Application depends on Domain
- Adapters depend on Application and Domain

**4.4 Task Sizing**

Each task should be completable by one agent in one session. If a task feels too large, split it. Signals of too-large tasks:
- Touches more than 2-3 files
- Has multiple independent test scenarios
- Combines unrelated concerns (e.g., "Create entity AND build API route")

</phase_4_task_decomposition>

<phase_5_parallelism_analysis>
**Phase 5: Parallelism Analysis**

**5.1 Confirm Story Independence**

Stories should be INVEST-independent per upstream `/create-requirements`. Verify by checking:
- Do any stories modify the same files?
- Do any stories depend on another story's output entity or interface?
- Are there shared infrastructure concerns (e.g., database schema, shared types)?

**5.2 Group Stories**

- **Parallel groups:** Stories with no mutual dependencies → can run simultaneously via `superpowers:dispatching-parallel-agents`
- **Sequential dependencies:** Story A must complete before Story B because B uses A's output

**5.3 Recommend Execution Order**

Present the recommended dispatch order:
1. First parallel group — dispatch to parallel agents
2. Sequential dependencies — after relevant group completes
3. Next parallel group — dispatch to parallel agents

Within each story, tasks are always sequential (Domain → Application → Adapters) executed by one agent.

</phase_5_parallelism_analysis>

<phase_6_output_generation>
**Phase 6: Generate PHASE-N-PLAN.md**

**6.1 Read Template**

Read `~/.claude/plugins/marketplaces/claude-forge/skills/plan-phase-tasks/templates/phase-plan-template.md`.

**6.2 Fill Template**

Populate all template sections with the data gathered in Phases 1-5:
- **Metadata:** Phase number, release, wave (from ROADMAP.md progressive load), source/derived story IDs, date, layers touched, UX inputs status
- **Story Summary:** Table of stories with layer coverage and task counts
- **Task Decomposition:** FDD task trees for each story
- **Parallelism Analysis:** Groups, dependencies, recommended execution order

**6.3 Write Output**

Write the completed plan to `.charter/PHASE-N-PLAN.md`.

**6.4 Present Summary**

Show the user:
- Phase number and name
- Number of stories and total tasks
- Architecture layers touched
- Parallelism summary (how many groups, any sequential dependencies)
- UX inputs status
- Output file path

</phase_6_output_generation>

<success_criteria>
Phase plan is complete when:

- `.charter/PHASE-N-PLAN.md` exists and follows the template structure
- All Metadata fields are populated (no placeholders)
- Every US-XXX from the trace script appears in the Task Decomposition
- Every task has Input, Output, and Test fields
- Tasks follow layer order (Domain → Application → Adapters) within each story
- UI tasks have `Reference:` fields (when Design OS export exists) or embedded UX specs in `Input:` (when fallback)
- Parallelism Analysis identifies independent story groups
- Recommended Execution Order is provided
- No extraneous content — the plan is the input to `superpowers:writing-plans`, not a narrative document
</success_criteria>

<format_contracts>
**Upstream Format Dependencies**

This skill depends on specific output formats from upstream skills:

| Upstream | Format Contract |
|----------|----------------|
| **ROADMAP.md** (`/create-roadmap`) | Wave headers: `### Wave N (type -- description)` / Phase headers: `#### PHASE-N: Slice Name` |
| **USER-STORIES.md** (`/create-requirements`) | Story traceability: `**Parent:** SM-XXX` format per story |
| **Design OS manifest.json** | Section mapping: `{ "sections": { "section-name": ["US-XXX", ...] } }` |

**Downstream Format Contract**

`superpowers:writing-plans` accepts any markdown spec as input. The FDD task tree maps directly:
- `Input:` → dependencies and context for writing the test
- `Output:` → deliverable the implementation must produce
- `Test:` → becomes the RED step (write the failing test first)
</format_contracts>
