---
name: reviewing-plans-adversarially
description: Runs adversarial multi-round review of implementation plans for executability, task decomposition quality, dependency correctness, spec fidelity, and TDD readiness. Triggers on "review plan", "review this plan", "adversarial plan review", "plan review", "check plan quality", "validate plan", "plan ready for execution", or after creating an implementation plan. Spawns a dynamic team of domain-relevant reviewers that loop until convergence.
allowed-tools: Read, Glob, Grep, Agent, TaskCreate, TaskUpdate, TaskList, TaskGet, AskUserQuestion, Edit
---

<objective>
Run adversarial multi-round review of an implementation plan using dynamically-selected agent teams. The orchestrator analyzes the plan's scope, spawns the right reviewers (not a fixed set), loops rounds of review with cross-challenge synthesis, and converges when zero Critical/Major issues remain. The plan is declared execution-ready only when all reviewers independently find nothing Critical or Major.
</objective>

<essential_principles>

**Principle 1: The orchestrator determines the team, not a template.**
Never default to a fixed number or type of reviewers. Read the plan. Identify its scope dimensions (what subsystems does it touch? how many tasks? what complexity?). Select reviewers from the archetype catalog whose expertise matches those dimensions. A 5-task data migration plan gets different reviewers than a 30-task full-stack feature plan. The number of reviewers is determined by the plan's complexity, not by convention.

**Principle 2: Every reviewer must read the spec AND the codebase, not just the plan.**
Reviewers that only read the plan produce shallow findings. The best findings come from comparing: (a) what the plan says to build against (b) what the spec actually requires, and (c) what the codebase already contains. Every reviewer MUST read the source spec, the plan, and relevant source files.

**Principle 3: The lead never rubber-stamps.**
After each round's synthesis, the orchestrator critically evaluates every finding against the actual spec and codebase. Re-rank severity based on evidence. Downgrade theoretical issues. Upgrade issues verified against the spec or code. The user gets the orchestrator's honest assessment, not a raw dump of reviewer findings.

**Principle 4: Convergence means zero Critical/Major, not zero findings.**
Minor issues and polish suggestions are not blockers. The loop stops when reviewers find no Critical or Major issues. Do not manufacture issues to justify another round. If the plan is clean, say so.

**Principle 4a: Finding issues is not a goal. Readiness is the goal.**
The purpose of the review is to determine whether the plan is execution-ready — not to produce a list of findings. Reporting zero issues is a valid outcome when the plan is genuinely clean. The orchestrator must downgrade findings where the reviewer is reaching — where the concern is theoretical, the plan already addresses it, or a competent implementer would handle it on the fly. BE ACCURATE. You do not get points for inflating issues that are minor or cosmetic into Major, and you do not get points for deflating genuine issues to avoid reporting them. The only measure of a good review is accuracy — did you correctly identify what is and is not a problem? When dismissing a concern as "an implementer would handle this," verify: would the implementer KNOW this concern exists without the plan mentioning it? If not, flag it.

**Principle 5: Always pause for user approval before editing.**
Plan edits are high-stakes — they change what gets built. Never auto-apply fixes. Present findings with your critical assessment, get user approval, then apply fixes. Then re-review.

**Principle 6: Judge against executability fundamentals.**
Every reviewer must evaluate through this lens in addition to their domain expertise:
- **Spec fidelity** — Does the plan build everything the spec requires? Does it build anything the spec doesn't require? Trace every spec requirement to a plan task.
- **Task executability** — Can a developer pick up each task and implement it without ambiguity? Are file paths exact? Are code snippets complete? Are verification steps concrete?
- **Dependency correctness** — Are task orderings correct? Can tasks marked as parallel actually run independently? Does each task have access to what prior tasks produced?
- **TDD discipline** — Does each task follow the red-green-commit cycle? Are test assertions specific and meaningful? Would the tests catch real bugs, or just exercise happy paths?
- **Build order soundness** — Does the sequence produce a working, testable system at each commit boundary? Or are there gaps where the code is broken between tasks?
- **Scope control** — Does the plan stay within the spec's boundaries? Is there scope creep (tasks that add features not in the spec) or scope leak (spec requirements not covered)?

These are not separate review items — they are the lens through which all findings are evaluated. A plan that covers all requirements but has impossible dependency orderings, or that follows TDD form but writes meaningless tests, has Major issues.

</essential_principles>

<prerequisites>

Three execution modes exist (Agent Teams, Parallel Subagents, Solo Reviewer) — see Step 5 of the workflow for details and the critical distinctions between them.

The plan being reviewed should follow the writing-plans skill output format: tasks with steps, file paths, TDD cycle (write test → verify fail → implement → verify pass → commit), and verification criteria. The skill adapts to other plan formats but is optimized for this structure.

</prerequisites>

<quick_start>
From the Claude Code CLI:
```
/review-plan docs/superpowers/plans/YYYY-MM-DD-feature-name.md
```

The skill handles everything: reads the plan (and its source spec), selects the right reviewer team, runs adversarial review rounds, applies critical judgment, and loops until convergence.
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
- The user sees the "execution-ready" verdict
</success_criteria>
