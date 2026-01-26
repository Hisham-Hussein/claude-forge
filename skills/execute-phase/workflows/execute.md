<required_reading>
**Read these files NOW before proceeding:**
1. `.planning/PLAN.md` - Phase details, success criteria, domain model
2. `roadmap/ACTIVE.md` - Current progress and state

**Standards (via Agent OS):**
@agent-os/standards/architecture.md
@agent-os/standards/testing.md
</required_reading>

<process>

<step name="load_state" priority="first">
**Load Project State**

Read `roadmap/ACTIVE.md` to determine:
- Which phase is current
- What success criteria are already complete
- Any in-progress work from previous session
- "How to Continue" section for context

**If argument provided** (e.g., phase number): Verify it matches ACTIVE.md state.

**If no ACTIVE.md exists:** Error - project not initialized. Run setup first.
</step>

<step name="analyze_phase">
**Analyze Phase**

From `.planning/PLAN.md`, extract for the current phase:
- Phase name and goal
- Success criteria (these become acceptance tests)
- Deliverables listed
- Dependencies on previous phases

Cross-reference with `roadmap/ACTIVE.md`:
- Which success criteria are already checked?
- Any partial work to continue?
</step>

<step name="check_directives">
**Check for Relevant Directives**

Before decomposing work:

```bash
ls directives/
```

Identify any SOPs that apply to this phase's work:
- Discovery SOPs for API integrations
- Enrichment SOPs for data processing
- Reference docs for utilities

Note relevant directives for work unit execution.
</step>

<step name="decompose_work_units">
**Decompose into Work Units**

Break the phase into work units using these heuristics:

**Size heuristics (fit in ~70% context):**
- 1 domain entity + its tests = ~1 work unit
- 1 adapter implementation + its tests = ~1 work unit
- 1 CLI command or feature = ~1 work unit
- Complex integration = 1 work unit

**Vertical slices preferred:**
- GOOD: "Influencer entity + storage adapter + CLI import"
- BAD: "All 8 domain entities" (too broad, no feedback loop)

**Dependency mapping:**
```
Work Unit 1: Domain entities [no deps]
  └── Parallel opportunity: separate entity per sub-agent
Work Unit 2: Storage adapter [depends: Unit 1]
Work Unit 3: CLI commands [depends: Unit 2]
```

**Output to user:**
```
## Phase [N]: [Name]
## Status: [X/Y] success criteria complete

### Work Units
1. [Name] - [Pending/Complete] - Sub-agents: [yes/no]
   Files: [list]
   Deps: [none/unit N]
2. [Name] - [Pending/Complete] - Sub-agents: [yes/no]
   ...

### Next: Work Unit [N]
[Brief description of what will be done]

Proceed? (yes/no)
```

**Wait for user approval before execution.**
</step>

<step name="execute_work_unit">
**Execute Work Unit**

For each work unit:

**1. Pre-execution checks:**
- Read relevant directive from `directives/` (if any)
- Read Quick Reference in `@agent-os/standards/architecture.md`
- Identify which principles apply (check "Apply When" column)
- Determine test type based on layer:
  - Domain → unit tests in `tests/unit/`
  - Adapter → contract tests in `tests/contracts/`
  - Integration → E2E tests in `tests/integration/`

**2. Sub-agent decision:**

Use sub-agents when:
- Tasks are independent (no shared state)
- Work can parallelize (separate files)
- Fresh context helps (complex implementation)

Do NOT use sub-agents when:
- Tasks have sequential dependencies
- Code references other in-flight code
- Integration logic spans components

**If using sub-agents:**
- Read `prompts/work-unit-executor.md` for handoff template
- Spawn with Task tool, type `general-purpose`
- Wait for completion
- Integrate and verify combined result

**If doing directly:**
- Use TodoWrite to track micro-tasks
- Follow TDD: RED (failing test) → GREEN (pass) → REFACTOR
- Verify each micro-success criterion

**3. During execution - Deviation handling:**

Read `references/deviation-rules.md` and apply:
- **Rule 1**: Auto-fix bugs (broken behavior)
- **Rule 2**: Auto-add critical (security, validation)
- **Rule 3**: Auto-fix blockers (missing deps)
- **Rule 4**: Ask user about architectural changes (new tables, schema)

Track all deviations for roadmap update.

**4. Post-execution:**
- Run all tests for this work unit
- Verify success criteria
- Stage files individually: `git add path/to/file.py`
- Commit: `{type}({phase}-{unit}): {description}`
</step>

<step name="update_roadmap">
**Update Roadmap (CRITICAL - NEVER SKIP)**

After EVERY work unit completion:

**roadmap/ACTIVE.md:**
```markdown
## Progress

**Completed:**
- [x] Previous items...
- [x] [Just completed work unit]

**In progress:**
- [ ] [Next work unit or empty]

## How to Continue

**Current state:** [What's built, what's tested]
**Next work unit:** [Exact next step]
**In-progress items:** [If any tasks partially done]
**Watch out for:** [Gotchas or context to remember]
```

**roadmap/LOG.md:**
```markdown
### [DATE] - Work Unit [N]: [Name]
**Completed:** [Brief description]
**Files:** [List of files created/modified]
**Decisions:** [Any architectural decisions made]
**Deviations:** [If any, from deviation rules]
**Commit:** [hash]
**Next:** [What comes next]
```

**roadmap/QUEUE.md:**
- Remove completed items
- Add newly discovered tasks
</step>

<step name="context_checkpoint">
**Context Checkpoint**

After updating roadmap, assess:

**Check 1: Context usage**
If you estimate ~70% context capacity:
1. STOP - do not start next work unit
2. Ensure roadmap is fully updated
3. Report: "Context at 70%. [X/Y] success criteria complete. Roadmap updated. Ready for fresh session."
4. END workflow

**Check 2: Phase completion**
If all phase success criteria met:
1. Mark phase complete in ACTIVE.md
2. Report: "Phase [N] complete. All success criteria verified."
3. Offer: `/execute-phase [N+1]` for next phase
4. END workflow

**Otherwise:** Continue to next work unit (loop back to execute_work_unit step)
</step>

</process>

<wave_based_parallelization>
**When to use waves (borrowed from GSD):**

If work units have dependency structure that allows parallelism:

```
Wave 1: [Unit 1, Unit 2] - no deps, can parallel
Wave 2: [Unit 3] - depends on Wave 1
Wave 3: [Unit 4, Unit 5] - depends on Wave 2
```

For each wave:
1. Spawn all units in wave simultaneously (single message, multiple Task calls)
2. Wait for all to complete (Task tool blocks)
3. Verify outputs, resolve conflicts
4. Update roadmap
5. Proceed to next wave

**Example parallel spawn:**
```
Task(prompt="[work unit 1 prompt]", subagent_type="general-purpose")
Task(prompt="[work unit 2 prompt]", subagent_type="general-purpose")
```

Both run in parallel. Task tool blocks until all complete.
</wave_based_parallelization>

<quality_gates>
**Before marking any work unit complete:**

1. **Code quality:**
   - All new code has tests (layer-appropriate)
   - Tests pass
   - No obvious security issues
   - Follows architecture principles (checked Quick Reference)

2. **DOE compliance:**
   - Used existing execution scripts where available
   - Checked directives before implementing
   - Will update directives with learnings (if any)

3. **Integration:**
   - New code works with existing code
   - No broken imports
   - System still runs (if applicable)

4. **Commit hygiene:**
   - Atomic commit (one logical change)
   - Clear message with proper format
   - Files staged individually (not `git add .`)
</quality_gates>

<success_criteria>
This workflow completes when:
- [ ] All work units for phase executed (or stopped at 70% context)
- [ ] Each work unit has tests (layer-appropriate)
- [ ] Architecture principles enforced (Quick Reference checked)
- [ ] Roadmap updated after EVERY work unit
- [ ] Atomic commits with proper format
- [ ] Phase success criteria systematically verified
- [ ] Session state captured for clean resume
</success_criteria>
