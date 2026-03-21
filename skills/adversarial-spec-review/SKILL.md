---
name: reviewing-specs-adversarially
description: Runs adversarial multi-round review of design specs, architecture docs, and technical specifications for correctness and implementation-readiness. Triggers on "review spec", "review this design", "adversarial review", "spec review", or after creating a design document. Spawns a dynamic team of domain-relevant reviewers that loop until convergence.
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

**Principle 4a: Finding issues is not a goal. Readiness is the goal.**
The purpose of the review is to determine whether the spec is implementation-ready — not to produce a list of findings. Reporting zero issues is a valid outcome when the spec is genuinely clean. The orchestrator must downgrade findings where the reviewer is reaching — where the concern is theoretical, the spec already addresses it, or a competent implementer would handle it without spec guidance. BE ACCURATE. You do not get points for inflating issues that are minor or cosmetic into Major, and you do not get points for deflating genuine issues to avoid reporting them. The only measure of a good review is accuracy — did you correctly identify what is and is not a problem?

**Principle 5: Always pause for user approval before editing.**
Spec edits are high-stakes. Never auto-apply fixes. Present findings with your critical assessment, get user approval, then apply fixes. Then re-review.

**Principle 6: For software specs, judge against engineering fundamentals.**
When the spec describes a software system, every reviewer must evaluate through this lens in addition to their domain expertise:
- **Goal achievement** — Will the design, if implemented literally, actually achieve the spec's stated objectives? Trace the logic end-to-end.
- **Logical correctness** — Are there logical gaps, race conditions, or contradictions in the specified behavior?
- **Maintainability and ease of change** — Does the design support long-term evolution? Are responsibilities cleanly separated (SOLID principles)? Will future developers understand and modify this confidently?
- **Testability and TDD readiness** — Can each component be tested in isolation? Are dependencies injectable? Does the design make test-driven implementation natural, or does it force awkward test setups?
- **Deployability** — Can changes be deployed independently and safely? Are there hidden deployment coupling or ordering constraints?
- **Performance under realistic load** — Are hot paths identified? Are there latent scaling problems at 10x growth?
- **Observability** — Can the system be debugged in production? Are there logging/monitoring hooks at key decision points? Will operators know when something is wrong and where to look?

These are not separate review items — they are the lens through which all findings are evaluated. A design that works but is untestable, or that's correct but unmaintainable, has Major issues.

</essential_principles>

<prerequisites>

Two execution modes exist (Agent Teams vs Parallel Subagents) — see Step 5 of the workflow for details and the critical distinction between them.

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
