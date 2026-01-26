---
name: execute-phase
description: Use when executing phases from PLAN.md, running implementation work units, or resuming work from a previous session. Enforces architecture principles, layer-specific testing, and DOE integration.
---

<essential_principles>

<principle name="doe_integration">
**DOE (Directive-Orchestration-Execution) Integration**

Before executing any work unit:
1. Check `directives/` for relevant SOPs
2. Use existing `execution/` scripts when available
3. After completion, self-anneal: update directives with learnings

You are the orchestration layer. Push complexity into deterministic scripts.
</principle>

<principle name="architecture_enforcement">
**Architecture Principles Enforcement**

@agent-os/standards/architecture.md

Read the Quick Reference before each work unit.

Key principles that MUST be applied:
- **Fail Fast**: Validate inputs before API calls
- **Single Responsibility**: One work unit = one coherent change
- **Ports & Adapters**: Separate interface from implementation
- **KISS/YAGNI**: Only add complexity when needed
- **Event Sourcing**: Log all operations

The 17 principles are NOT optional. Check the Quick Reference "Apply When" column.
</principle>

<principle name="layer_specific_testing">
**Layer-Specific Testing**

Tests are required. The type depends on what you're building:

| Layer | Test Type | Location |
|-------|-----------|----------|
| Domain (entities, value objects) | Unit tests | `tests/unit/` |
| Adapters (API clients, storage) | Contract tests | `tests/contracts/` |
| Integration (cross-layer flows) | E2E tests | `tests/integration/` |
| Principles (Fail Fast, etc.) | Principle tests | `tests/unit/test_<principle>.py` |

Follow TDD when creating new code:
1. **RED**: Write failing test first
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Clean up if needed

@agent-os/standards/testing.md
</principle>

<principle name="session_continuity">
**Session Continuity**

Monitor context window. At ~70% capacity:
1. STOP starting new work units
2. Complete current micro-task
3. Commit current state
4. Update `roadmap/ACTIVE.md` with:
   - Current state
   - Next work unit
   - In-progress items
   - Watch-out-for notes
5. Report to user: "Context at 70%. Roadmap updated. Ready for fresh session."

A fresh session reads `roadmap/ACTIVE.md` and continues seamlessly.
</principle>

<principle name="atomic_commits">
**Atomic Commits**

One commit per work unit. Format: `{type}({phase}-{unit}): {description}`

Types: `feat`, `fix`, `test`, `refactor`, `docs`, `chore`

Example: `feat(1-02): add Influencer entity with validation`

Never use `git add .` or `git add -A`. Stage files individually.
</principle>

</essential_principles>

<objective>
Execute phases from `.planning/PLAN.md` using work unit decomposition that ensures high-quality implementation while staying within context window constraints.

This skill:
- Decomposes phases into manageable work units
- Spawns sub-agents for parallel work when appropriate
- Enforces architecture principles and testing methodology
- Maintains perfect session continuity via roadmap updates
- Integrates with DOE (checks directives, updates with learnings)
</objective>

<quick_start>
**To execute a phase:**

1. Invoke `/execute-phase 1` (where 1 is the phase number)
2. Skill reads PLAN.md and ACTIVE.md
3. Presents work unit decomposition for approval
4. Executes work units sequentially (spawning sub-agents where beneficial)
5. Updates roadmap after each work unit
6. Stops at 70% context or phase completion
</quick_start>

<intake>
**What would you like to do?**

1. Execute a phase (start or continue)
2. Resume from previous session

**Wait for response before proceeding.**

If user invoked with argument (e.g., `/execute-phase 1`), skip intake and route directly.
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "execute", phase number | `workflows/execute.md` |
| 2, "resume", "continue" | `workflows/execute.md` (reads ACTIVE.md for state) |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
All domain knowledge in `references/`:

**Execution:** deviation-rules.md (auto-fix vs ask user)
</reference_index>

<prompts_index>
Sub-agent prompts in `prompts/`:

| Prompt | Purpose |
|--------|---------|
| work-unit-executor.md | Fresh context handoff for parallel work units |
</prompts_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| execute.md | Main phase execution workflow |
</workflows_index>

<success_criteria>
Phase execution succeeds when:
- [ ] All work units produce working, tested code
- [ ] Architecture principles enforced (Quick Reference checked)
- [ ] Tests written per layer (domain/adapter/integration)
- [ ] Roadmap files updated after EVERY work unit
- [ ] Atomic commits with proper format
- [ ] Session can be interrupted and resumed cleanly
</success_criteria>
