<prompt_description>
Meta-prompt for spawning sub-agents to execute work units in parallel.

Use this when work units are independent and can benefit from fresh context.
</prompt_description>

<prompt_template>
<objective>
Execute Work Unit {N}: {Name}

You are a sub-agent spawned to implement a specific work unit with fresh context.
Your job: implement, test, verify, and commit. Then report results.
</objective>

<context>
**Project:** Boom Influencer Database System
**Architecture:** Clean Architecture + DOE (Directive-Orchestration-Execution)

**Required reading (before implementation):**
- `CLAUDE.md` - Operating instructions and conventions
- `.planning/PLAN.md` section for Phase {N} - Specifications
- `directives/strategic/architecture_principles.md` (Quick Reference at end)
- `directives/strategic/testing_methodology.md`

{If relevant directive exists:}
- `directives/{category}/{directive}.md` - SOP for this work
</context>

<work_unit_specification>
**Work Unit:** {N} - {Name}
**Phase:** {Phase number and name}
**Dependencies:** {What must exist / what this builds on}

**Files to create:**
{List exact file paths}

**Implementation requirements:**
{Specific features, interfaces, or behavior}

**Test requirements:**
- Layer: {domain/adapter/integration}
- Location: `tests/{unit|contracts|integration}/`
- Coverage: {What must be tested}

**Constraints:**
- {Constraint 1 - e.g., no external dependencies beyond X}
- {Constraint 2 - e.g., follow existing patterns in Y}
- Do not modify files outside your scope
</work_unit_specification>

<architecture_principles>
**Check Quick Reference in `architecture_principles.md` and apply:**

Key principles for this work unit:
- {Principle 1} - {Why it applies}
- {Principle 2} - {Why it applies}

Pre-built utilities available in `execution/utils/`:
- `validation.py` - Fail Fast input validation
- `retry.py` - Retry with backoff
- `logging.py` - Event sourcing
- See `directives/reference/utilities_api.md` for full API
</architecture_principles>

<testing_requirements>
Follow TDD:
1. **RED**: Write failing test first
2. **GREEN**: Minimal code to pass
3. **REFACTOR**: Clean up

Test type based on layer:
- Domain (entities, value objects) → Unit tests
- Adapters (API clients, storage) → Contract tests
- Integration (cross-layer) → E2E tests
</testing_requirements>

<deviation_handling>
If you discover work not in the plan:

- **Bug (broken behavior):** Fix immediately, note in output
- **Missing critical (security, validation):** Add immediately, note in output
- **Blocker (can't proceed):** Fix immediately, note in output
- **Architectural (new table, schema change):** STOP, report in output, do not implement

Track all deviations for the orchestrator.
</deviation_handling>

<commit_format>
Stage files individually (NEVER `git add .`):
```bash
git add path/to/file.py
git add tests/unit/test_file.py
```

Commit format: `{type}({phase}-{unit}): {description}`

Types: feat, fix, test, refactor, docs, chore
</commit_format>

<output_format>
When complete, report:

```markdown
## Work Unit {N} Complete

**Status:** {Success / Blocked}
**Commit:** {hash}

**Files created:**
- {path/to/file.py}
- {tests/unit/test_file.py}

**Tests:**
- {N} tests written
- All passing: {yes/no}

**Deviations:**
- {[Rule N] description} OR None

**Decisions made:**
- {Any implementation decisions}

**Notes for orchestrator:**
- {Anything the next work unit needs to know}
```

If blocked (Rule 4 deviation):
```markdown
## Work Unit {N} Blocked

**Status:** Blocked - Architectural decision needed
**Progress:** {What was completed before block}

**Decision needed:**
{Description of architectural change discovered}

**Options:**
1. {Option A} - {pros/cons}
2. {Option B} - {pros/cons}

**Recommendation:** {Your recommendation}
```
</output_format>

<success_criteria>
Work unit complete when:
- [ ] All specified files created
- [ ] Tests written (layer-appropriate)
- [ ] Tests pass
- [ ] Architecture principles followed
- [ ] Atomic commit made with proper format
- [ ] Output format returned to orchestrator
</success_criteria>
</prompt_template>

<usage>
**To spawn a sub-agent:**

```
Task(
  description="Execute work unit {N}: {brief name}",
  prompt="[Fill in template above with specific values]",
  subagent_type="general-purpose"
)
```

**For parallel execution (same wave):**

Send multiple Task calls in a single message:
```
Task(...work unit 1...)
Task(...work unit 2...)
Task(...work unit 3...)
```

All run in parallel. Task tool blocks until all complete.
</usage>
