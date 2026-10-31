---
name: reviewing-specs-adversarially
description: Runs adversarial multi-round review of design specs, architecture docs, and technical specifications for correctness and implementation-readiness. Triggers on "review spec", "review this design", "adversarial review", "spec review", or after creating a design document. Spawns a dynamic team of domain-relevant reviewers that loop until convergence.
allowed-tools: Read, Glob, Grep, Agent, TaskCreate, TaskUpdate, TaskList, TaskGet, AskUserQuestion, Edit, Write, Bash
---

<objective>
Run adversarial multi-round review of a design specification using dynamically-selected agent teams. The orchestrator analyzes the spec's domain dimensions, spawns the right reviewers (not a fixed set), loops rounds of review with cross-challenge synthesis, and converges when zero Critical/Major issues remain. The spec is declared implementation-ready only when nothing Critical or Major remains after synthesis.
</objective>

<essential_principles>

**Principle 1: The orchestrator determines the team, not a template.**
Never default to a fixed number or type of reviewers. Read the spec. Identify its domain dimensions (what areas of concern does it touch?). Select reviewers from the archetype catalog whose expertise matches those dimensions. A database migration spec gets different reviewers than a UI workflow spec. The number of reviewers is determined by the spec's complexity, not by convention.

**Principle 2: Every reviewer must read real files, not just the spec.**
Reviewers that only read the spec produce shallow findings. The best findings come from comparing what the spec says against what the code, configs, and referenced documents actually contain. Every reviewer MUST read the source files, config files, and any other files referenced by or relevant to the spec.

**Principle 3: The lead never rubber-stamps.**
After each round's synthesis, the orchestrator critically evaluates every finding against the actual codebase. Re-rank severity based on evidence. Downgrade theoretical issues. Upgrade issues verified in code. The user gets the orchestrator's honest assessment, not a raw dump of reviewer findings.

**Principle 4: Convergence means zero Critical/Major, not zero findings.**
Minor issues and documentation polish are not blockers. The loop stops when no Critical or Major issues remain after synthesis. Do not manufacture issues to justify another round. If the spec is clean, say so.

**Principle 4a: Finding issues is not a goal. Readiness is the goal.**
The purpose of the review is to determine whether the spec is implementation-ready — not to produce a list of findings. Reporting zero issues is a valid outcome when the spec is genuinely clean. The orchestrator must downgrade findings where the reviewer is reaching — where the concern is theoretical, the spec already addresses it, or a competent implementer would handle it without spec guidance. BE ACCURATE. You do not get points for inflating issues that are minor or cosmetic into Major, and you do not get points for deflating genuine issues to avoid reporting them. The only measure of a good review is accuracy — did you correctly identify what is and is not a problem? When dismissing a concern as "an implementer would handle this," verify: would the implementer KNOW this concern exists without the spec mentioning it? If not, flag it.

**Principle 5: Always pause for user approval before editing.**
Spec edits are high-stakes. Never auto-apply fixes. Present findings with your critical assessment, get user approval, then apply fixes. Then re-review.

**Principle 6: For software specs, judge against engineering fundamentals.**
When the spec describes a software system, the orchestrator judges every finding through this lens in synthesis:
- **Goal achievement** — Will the design, if implemented literally, actually achieve the spec's stated objectives? Trace the logic end-to-end.
- **Logical correctness** — Are there logical gaps, race conditions, or contradictions in the specified behavior?
- **Maintainability and ease of change** — Does the design support long-term evolution? Are responsibilities cleanly separated (SOLID principles)? Will future developers understand and modify this confidently?
- **Testability and TDD readiness** — Can each component be tested in isolation? Are dependencies injectable? Does the design make test-driven implementation natural, or does it force awkward test setups?
- **Deployability** — Can changes be deployed independently and safely? Are there hidden deployment coupling or ordering constraints?
- **Performance under realistic load** — Are hot paths identified? Are there latent scaling problems at 10x growth?
- **Observability** — Can the system be debugged in production? Are there logging/monitoring hooks at key decision points? Will operators know when something is wrong and where to look?

These are not separate review items — they are the lens through which all findings are evaluated.

</essential_principles>

<prerequisites>

Three execution modes exist (Agent Teams, Parallel Subagents, Solo Reviewer) and, for Modes B and C, three reviewer engines (Claude, Codex, Mixed) — see `steps/05-spawn.md` for details and the critical distinctions between them. The Codex engine needs the `codex` plugin.

</prerequisites>

<quick_start>
From the Claude Code CLI:
```
/review-spec docs/path/to/spec.md
```

The skill handles everything: reads the spec, selects the right reviewer team, runs adversarial review rounds, applies critical judgment, and loops until convergence.
</quick_start>

<routing>
Run these steps in order. At each step, READ ITS FILE NOW (not earlier, not from memory), then do every instruction in it. If a read comes back truncated, read the rest before acting.

Gate files go in `.review-state/` in the session's working directory (`N` = current round). Hooks block the next action until the gate file exists; they do not check quality, so do the step, then write its file. Before the team OK, use Read/Grep/Glob or a read-only helper agent (`Explore`, `Plan`, `claude-code-guide`) only; any other agent spawn, and any Codex job (`codex-companion.mjs`), counts as a reviewer and is gated. Write gate files and `active.json` with the Write tool.

0.  `steps/00-checklist.md` — post the checklist. Create `.review-state/active.json` = `{"spec": "<absolute spec path>", "round": 1}`, append `.review-state/` to the file `git rev-parse --git-path info/exclude` prints (works in worktrees), write `.review-state/round-1/0-checklist.md` (the checklist as posted).
1.  `steps/01-analyze.md`
2.  `steps/02-team.md` — announce the team and WAIT for the user's OK. Then write `round-N/2-team-ok.md` (quote the user's words).
3.  `steps/03-files.md`
4.  `steps/04-focus.md`
5.  `steps/05-spawn.md`
6.  `steps/06-synthesize.md`
7.  `steps/07-present.md` — WAIT for the user's decision. Then write `round-N/7-approved.md` (quote the user's words and list the approved findings).
8a. `steps/08a-apply-fixes.md` — write `round-N/8a-impact-trace.md` (per finding: references found, sections to re-check) BEFORE any spec edit.
8b. `steps/08b-verify.md` — write `round-N/8b-verification.md` with headings `## Pass 1`, `## Pass 2`, `## Pass 3` and what each found.
8c. `steps/08c-commit-loop.md` — commit; ask before the next round. For a new round: set `round` in `active.json` to N+1 and write `round-<N+1>/0-checklist.md` and `round-<N+1>/2-team-ok.md` after the user confirms.
9.  `steps/09-safety-valve.md` (if round 5 has open Critical/Major)
10. `steps/10-finish.md` — when the review ends (converged, stopped, or user says stop), delete `.review-state/active.json`.
</routing>

<reference_index>
All domain knowledge in `references/`:

**Reviewer Selection:** reviewer-archetypes.md
**Synthesis:** synthesis-principles.md
</reference_index>

<success_criteria>
Review is complete when:
- Zero Critical/Major issues remain after a round's synthesis
- The orchestrator's critical judgment confirms the verdict
- The user sees the "implementation-ready" verdict
- `.review-state/active.json` is deleted (the review is over; otherwise the gates keep blocking in later sessions)
</success_criteria>
