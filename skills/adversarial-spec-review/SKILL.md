---
name: adversarial-spec-review
description: Use when reviewing a design spec, design document, architecture doc, or technical specification for correctness and implementation-readiness. Use when user says "review spec", "review this design", "adversarial review", "spec review", or after creating a design document. Spawns a dynamic team of domain-relevant reviewers that loop until convergence.
allowed-tools: Read, Glob, Grep, Agent, TaskCreate, TaskUpdate, TaskList, TaskGet, AskUserQuestion, Edit
---

<objective>
Run adversarial multi-round review of a design specification using dynamically-selected agent teams. The orchestrator analyzes the spec's domain dimensions, spawns the right reviewers (not a fixed set), loops rounds of review with cross-challenge synthesis, and converges when zero Critical/Major issues remain. The spec is declared implementation-ready only when all reviewers independently find nothing Critical or Major.
</objective>

<essential_principles>

**Principle 1: The orchestrator determines the team, not a template.**
Never default to a fixed number or type of reviewers. Read the spec. Identify its domain dimensions (what areas of concern does it touch?). Select reviewers from the archetype catalog whose expertise matches those dimensions. A database migration spec gets different reviewers than a UI workflow spec. The number of reviewers is determined by the spec's complexity, not by convention.

**Principle 2: Every reviewer must read real files, not just the spec.**
Reviewers that only read the spec produce shallow findings. The best findings come from comparing what the spec says against what the code, configs, and referenced documents actually contain. Every reviewer MUST read the source files, config files, and any other files referenced by or relevant to the spec.

**Principle 3: The lead never rubber-stamps.**
After each round's synthesis, the orchestrator critically evaluates every finding against the actual codebase. Re-rank severity based on evidence. Downgrade theoretical issues. Upgrade issues verified in code. The user gets the orchestrator's honest assessment, not a raw dump of reviewer findings.

**Principle 4: Convergence means zero Critical/Major, not zero findings.**
Minor issues and documentation polish are not blockers. The loop stops when reviewers find no Critical or Major issues. Do not manufacture issues to justify another round. If the spec is clean, say so.

**Principle 5: Always pause for user approval before editing.**
Spec edits are high-stakes. Never auto-apply fixes. Present findings with your critical assessment, get user approval, then apply fixes. Then re-review.

</essential_principles>

<prerequisites>

**Agent Teams is required.** This skill uses Claude Code Agent Teams (shared task list, inter-agent communication). The `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable is already configured in settings.

**CLI only.** Agent Teams does not work from the VS Code extension. If you are in VS Code, tell the user:
> "This skill requires Agent Teams, which only works in the Claude Code CLI. Open a new `claude` session from your terminal and run `/review-spec` there."

Check the environment before proceeding. If you detect you're in VS Code (no Agent Teams capability), stop and show the message above instead of attempting the review.

</prerequisites>

<quick_start>
From the Claude Code CLI:
```
/review-spec docs/path/to/spec.md
```

The skill handles everything: reads the spec, selects the right reviewer team, runs adversarial review rounds, applies critical judgment, and loops until convergence.
</quick_start>

<routing>
This skill has one workflow. Proceed directly to `workflows/run-review.md`.
</routing>

<reference_index>
All domain knowledge in `references/`:

**Reviewer Selection:** reviewer-archetypes.md
**Synthesis:** synthesis-principles.md
</reference_index>

<success_criteria>
Review is complete when:
- All reviewers independently find zero Critical/Major issues in a round
- The orchestrator's critical judgment confirms the finding
- The user sees the "implementation-ready" verdict
</success_criteria>
