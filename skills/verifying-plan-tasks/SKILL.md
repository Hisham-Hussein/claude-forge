---
name: verifying-plan-tasks
description: Incrementally verifies each plan task against its source spec and project architectural principles as the plan is written. Companions plan-writing workflows (e.g., superpowers:writing-plans) by spawning a verifier after each task, catching spec deviations before they cascade to downstream tasks. Use when writing implementation plans, or when the user asks for incremental verification, task-by-task verification, or spec-checked plan writing.
---

<objective>
Catch spec deviations incrementally as each plan task is written — not after the entire plan is complete. A verifier compares each task's code and tests against the source spec section and project principles, so errors are fixed before downstream tasks depend on them.
</objective>

<quick_start>
Invoke this skill alongside a plan-writing skill (e.g., superpowers:writing-plans). After writing each task, spawn the verifier from `templates/verification-prompt.md` with the task text + spec section inline. Commit the task only after the verifier returns PASS. If deviations are found, fix and re-verify (up to 3 cycles, then escalate to user).
</quick_start>

<why>
Plans written from specs accumulate deviations. A wrong interface in Task 3 propagates through Tasks 5, 6, and 7. Catching it after writing 1800 lines means fixing it everywhere. Catching it after writing 200 lines means fixing it once. The cost of verifying early is low; the cost of discovering late is high.
</why>

<invocation>
This skill companions a plan-writing skill (typically superpowers:writing-plans). The authoring skill owns plan structure, TDD format, and task decomposition. This skill owns fidelity to the source spec.

Tell the plan-writing agent: "Use verifying-plan-tasks after writing each task to verify it against the spec before moving on."
</invocation>

<procedure>

Copy this checklist and repeat for each task:

```
Task N:
- [ ] Write the task from the relevant spec section
- [ ] Spawn verifier (see templates/verification-prompt.md)
- [ ] Verifier returned PASS? → Commit task to plan file → Move to next task
- [ ] Verifier returned deviations? → Fix → Re-spawn verifier (re-verification mode)
- [ ] Re-verification PASS? → Commit → Next task
- [ ] 3 fix cycles exhausted without PASS? → Escalate to user
```

</procedure>

<inputs>

The verifier receives four inputs:

1. **Task text** (inline) — the full text of the task just written, pasted into the prompt. The verifier should not read the plan file for the current task.

2. **Spec section** (inline) — the relevant section(s) of the source spec that this task implements, pasted into the prompt.

3. **Project principles file** (path) — the path to CLAUDE.md or equivalent. The verifier reads this to check architectural principle compliance.

4. **Plan file so far** (path) — the path to the plan file containing all previously committed tasks. The verifier reads this for consistency checking against what's already been written. Empty for Task 1.

</inputs>

<verification_areas>

The verifier checks four things:

1. **Spec behavioral fidelity** — Does the task's code implement exactly what the spec prescribes for this area? Line-by-line comparison. If the spec says "flat 30s wait for 429," does the code do that? If the spec defines an interface with 5 methods, does the task's interface have 5 methods?

2. **Test completeness** — Does the task's test code verify the behaviors the spec requires? If the spec lists 5 test scenarios for this area, are all 5 present? Are assertions specific enough to distinguish correct from incorrect behavior?

3. **Principle compliance** — Do the code snippets honor the project's architectural principles? Dependency direction, credential sanitization at boundaries, interface segregation, error classification — whatever the project's CLAUDE.md prescribes.

4. **Forward consistency** — Do interfaces, signatures, types, and exports established in this task align with what downstream spec sections will need? This requires the verifier to skim ahead in the spec, not just the current section.

</verification_areas>

<fix_reverify_loop>

When the verifier finds deviations:

1. The plan author fixes the task.
2. The verifier is re-spawned in **re-verification mode**. In addition to the 4 standard checks, re-verification also checks:
   - Did each fix actually resolve the reported deviation?
   - Did any fix introduce new inconsistencies with the rest of the plan?
3. If re-verification passes → commit and move on.
4. If re-verification finds more issues → fix and re-verify again.
5. **Cap: 3 fix-verify cycles.** If the task still has deviations after 3 cycles, escalate to the user with the remaining issues. Something structural may need human judgment.

</fix_reverify_loop>

<commit_discipline>

After each task passes verification, commit it to the plan file before writing the next task. This creates a clean history where each commit is a verified plan task. If something goes wrong later, `git log` shows exactly when a deviation was introduced.

Commit message format: `docs: add Task N — [brief description] to [plan name]`

</commit_discipline>

<scope>

The authoring skill (e.g., superpowers:writing-plans) owns plan structure, TDD format, task decomposition, and file organization. This skill owns only the verification loop — comparing what was written against what the spec and principles require.

</scope>

<reference_index>
Verifier prompt template: `templates/verification-prompt.md`
</reference_index>
