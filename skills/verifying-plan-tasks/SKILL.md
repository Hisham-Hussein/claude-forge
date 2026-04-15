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
- [ ] Verifier returned CRITICAL or MAJOR deviations? → Fix → Re-spawn verifier (re-verification mode)
      (MINOR findings are logged but do not block — commit the task with MINORs noted)
- [ ] Re-verification PASS? → Commit → Next task
- [ ] 3 fix cycles exhausted without PASS? → Escalate to user
```

After all tasks pass per-task verification:

```
Final holistic verification:
- [ ] Spawn final holistic verifier (see templates/final-verification-prompt.md)
      Inputs: complete plan file, complete spec, CLAUDE.md
- [ ] Score verifier's raw findings using the confidence rubric (see <final_verification>)
- [ ] Verdict APPROVED (zero Critical, zero Major)? → Plan is ready for user review
- [ ] Verdict REVISE? → Fix findings → Re-run final verification
- [ ] 2 fix cycles exhausted? → Escalate to user with remaining findings
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

The verifier checks six things. These are ordered by cascade severity — a spec fidelity error causes more downstream damage than an actionability gap.

1. **Spec behavioral fidelity** — Does the task's code implement exactly what the spec prescribes for this area? The verifier must build an explicit **comparison table** mapping every behavioral prescription in the spec section to the corresponding task code. If the spec says "flat 30s wait for 429," does the code do that? If the spec defines an interface with 5 methods, does the task's interface have 5 methods? Every prescription not traceable to task code is flagged as missing. Every task code not traceable to a spec prescription is flagged as UNSUPPORTED (scope creep). Cite the specific spec text and the specific task code that diverges.

2. **Test behavioral specificity** — Beyond checking that tests exist, verify that each test would actually distinguish correct from incorrect implementation. Apply these concrete checks:
   - Each test asserts on the *specific value/behavior* the spec prescribes, not just "doesn't throw"
   - Each test would *fail* if the implementation were wrong (a test that passes for any return value is not a test)
   - Edge cases from the spec have corresponding test cases
   - Test descriptions match the spec's behavioral language
   - If the spec lists 5 test scenarios, all 5 are present with specific assertions

3. **Actionability** — Is the task specific enough for a developer agent to implement without reading the spec? The developer agent will ONLY have this plan file — everything it needs must be present. Apply these concrete tests (fail any = deviation):
   - Every interface/port mentioned: are method signatures with parameter types listed?
   - Every constant/threshold: is the specific value stated (not "per spec" or "as specified")?
   - Every error handling path: is the error type and response specified?
   - Every "follow pattern X": is the pattern described inline or cited by file:line?
   - Every type mentioned: is its shape defined or referenced by definition location?

4. **Principle compliance** — Do the code snippets honor the project's architectural principles? Dependency direction, credential sanitization at boundaries, interface segregation, error classification — whatever the project's CLAUDE.md prescribes. Only flag violations of principles the project actually states — not theoretical best practices.

5. **Cross-task entity consistency** — Actively scan every entity (interface name, type, export, function signature, file path, constant name) introduced or referenced in this task against:
   - All previously committed tasks (backward check — did we contradict something already established? If this task introduces `RetryPolicy` with 3 fields and a prior task referenced `RetryPolicy` with 4 fields, that's a cross-task regression)
   - What the current spec section says about downstream dependencies (forward check — if the spec section references things downstream tasks will consume, will what we defined here be findable and compatible?)

6. **Spec-principles conflict detection** — When the spec prescribes a behavior and the project principles contradict it (e.g., spec says inline a vendor SDK but principles say depend on abstractions), flag this as a CONFLICT. The plan author cannot resolve spec-vs-principles conflicts alone — escalate to the user with both locations cited. Do not penalize the task for choosing one side; flag the conflict itself.

</verification_areas>

<severity_classification>
Every deviation must be classified by severity. This focuses fix effort on what matters and prevents the fix-verify loop from churning on trivial findings.

- **CRITICAL**: Wrong code that will propagate — wrong interface method, wrong retry constant, wrong type shape, missing required behavior. A developer implementing from this plan will write incorrect code. Must fix before proceeding.
- **MAJOR**: Missing information that leaves a gap the developer cannot fill — test scenario not specified, error class not defined, interface method listed but signature missing. The developer will have to guess. Should fix before proceeding.
- **MINOR**: Imprecise wording that is unlikely to cause implementation errors but could be clearer. Fix if convenient. Does not block task commitment.

The fix-reverify loop is required only for CRITICAL and MAJOR deviations. MINOR findings are logged in the verifier report but do not block commitment of the task.
</severity_classification>

<intentional_deviations>
Sometimes the plan task legitimately departs from the spec — the spec is stale, the user made a decision that overrides it, or a refinement emerged during plan writing. Without a mechanism to mark these, the verifier will re-flag them every cycle, wasting fix-verify iterations.

When the plan author knows a deviation from the spec is intentional:
1. Annotate the deviation inline in the task with: `<!-- INTENTIONAL DEVIATION: [reason] -->`
2. The verifier acknowledges annotated deviations in its report but does not count them as findings.
3. Unannotated deviations are always flagged — the annotation is opt-in and requires a reason.

The verifier must still report intentional deviations in a separate "Acknowledged Deviations" section so the user can audit them if desired. If the reason is weak or missing, the verifier should flag it as a MAJOR deviation (an unjustified intentional deviation is worse than an accidental one).
</intentional_deviations>

<fix_reverify_loop>

When the verifier finds CRITICAL or MAJOR deviations:

1. The plan author fixes the task.
2. The verifier is re-spawned in **re-verification mode**. In addition to the 6 standard checks, re-verification also checks:
   - Did each fix actually resolve the reported deviation?
   - Did any fix introduce new inconsistencies with the rest of the plan?
3. If re-verification passes → commit and move on.
4. If re-verification finds more issues → fix and re-verify again.
5. **Cap: 3 fix-verify cycles.** If the task still has deviations after 3 cycles, escalate to the user with the remaining issues. Something structural may need human judgment — perhaps the spec and principles are inconsistent, or the task needs to intentionally deviate from the spec for good reasons.

</fix_reverify_loop>

<commit_discipline>

After each task passes verification, commit it to the plan file before writing the next task. This creates a clean history where each commit is a verified plan task. If something goes wrong later, `git log` shows exactly when a deviation was introduced.

Commit message format: `docs: add Task N — [brief description] to [plan name]`

</commit_discipline>

<scope>

The authoring skill (e.g., superpowers:writing-plans) owns plan structure, TDD format, task decomposition, and file organization. This skill owns only the verification loop — comparing what was written against what the spec and principles require.

</scope>

<verification_audit_trail>
After each task completes verification, append a verification log entry to the plan file as an HTML comment. This enables process improvement and post-hoc auditing.

```
<!-- Verification Log
Task 1: PASS (1 cycle)
Task 2: PASS after fixes (2 cycles) — D1 [CRITICAL]: wrong retry constant, D2 [MAJOR]: missing error class
Task 3: PASS (1 cycle) — 1 MINOR logged (imprecise timeout description)
Task 4: PASS after fixes (3 cycles) — D1 [CRITICAL]: interface signature wrong, escalated D2: CONFLICT spec vs principles on dependency direction (user resolved: use abstraction)
Task 5: PASS (1 cycle)
Intentional deviations: 1 (Task 4 — interface simplified per user decision, spec stale)
-->
```
</verification_audit_trail>

<final_verification>
After all tasks pass per-task verification, spawn a **final holistic verifier** on the complete plan. This catches emergent issues invisible to per-task verification — cumulative spec coverage gaps, entity drift across distant tasks, principle violations that span multiple tasks, and missing integration points.

**When to invoke:** After the last task passes per-task verification and before presenting the plan to the user.

**Inputs:**
1. **Complete plan file** (path) — the full plan with all verified tasks
2. **Complete spec** (path or inline) — the full source spec, not just individual sections
3. **Project principles file** (path) — CLAUDE.md

**Two-layer architecture (find vs judge):**

The final verification separates finding from scoring — the agent that looks for problems should not also decide how serious they are.

1. **Sonnet verifier agent** (spawned via `templates/final-verification-prompt.md`) — runs all 5 holistic checks. Produces raw findings with evidence and spec/principles citations. Does NOT score or classify severity. Its job is to be thorough — surface everything, let the orchestrator judge.

2. **Plan author / orchestrator** (the caller) — receives the verifier's raw findings and applies the confidence scoring rubric below. Scores each finding 0-100, classifies severity, drops low-confidence findings, produces the calibrated report, and renders the APPROVED/REVISE verdict.

**What the final verifier checks (5 holistic areas):**

1. **Cumulative spec coverage** — Walk every requirement, constraint, and behavioral prescription in the full spec. For each, verify at least one task addresses it. Flag any spec requirement with zero task coverage. This is the check that per-task verification structurally cannot do — each task verifier sees only its spec section, so gaps between sections are invisible.

2. **Cross-task entity integrity** — Build a full entity registry: every interface, type, export, function, constant, and file path mentioned across all tasks. For each entity, verify consistent naming, typing, and signatures everywhere it appears. Per-task verification catches adjacent-task drift; this catches drift across tasks 2 and 9 that never see each other.

3. **Dependency graph correctness** — Verify that every entity a task consumes is produced by a prior task (or exists in the codebase). Check for circular dependencies, missing producers, and ordering issues. Per-task forward checks are scoped to the current spec section; this verifies the full dependency graph.

4. **Holistic principle compliance** — Read CLAUDE.md principles. Check the plan as a whole — not individual tasks in isolation. Does the combined dependency graph honor DIP? Does the full set of interfaces honor ISP? Does the overall architecture honor clean boundaries? A principle violation that emerges from the interaction of 3 tasks won't be caught by verifying each task alone.

5. **Integration completeness** — For every interface/port defined in one task and consumed in another, verify the consumer's usage matches the producer's definition. Check: are all defined exports actually imported somewhere? Are there tasks that produce artifacts no other task consumes (dead code in the plan)?

**Orchestrator severity calibration — confidence-scored rubric:**

After receiving the verifier's raw findings, the orchestrator scores each finding (0-100) before classifying. This prevents severity inflation.

| Score | Classification | Action |
|-------|---------------|--------|
| Below 60 | DROP — not reported | Theoretical concern, cosmetic, or competent developer would handle without guidance |
| 60-79 | MINOR | Note for implementer. Fix if easy. Does not block plan approval. |
| 80-100 | MAJOR | Real gap the implementer would NOT catch without the plan mentioning it. Should fix before approval. |
| N/A (by nature) | CRITICAL | Plan as written would produce incorrect results, miss a spec requirement entirely, or create a dependency that cannot be resolved. Must fix. |

**Anti-inflation rules:**
- "Ease of fix" is NOT a severity input. Easy to fix does not make it Major.
- Defense-in-depth improvements (second safety layer where primary exists) are capped at MINOR.
- "Pattern-setting" is not an automatic severity amplifier. A finding is Major only if it scores 80+ on its own merits.
- If you cannot write "I am 80% confident this would cause problems in practice," it is not Major.
- Accuracy is the only measure of quality. Zero Critical / zero Major is a valid and successful outcome — not a failure of the review.

**Orchestrator scoring steps:**
1. Read each raw finding from the verifier
2. Apply the confidence scoring rubric (0-100)
3. Drop findings below 60
4. Classify remaining: MINOR (60-79), MAJOR (80-100), CRITICAL (by nature)
5. Apply anti-inflation rules — demote any finding that fails the rules
6. Produce the calibrated report
7. Render verdict: APPROVED (zero Critical, zero Major) or REVISE (list specific fixes)

**Calibrated report format:**

```
FINAL VERIFICATION — [plan name]

Spec coverage: {N}/{M} requirements covered ({percentage}%)
  Uncovered: [list with spec locations, if any]

Entity registry: {N} entities tracked across {M} tasks
  Inconsistencies: [list, if any]

Dependency graph: {valid / issues found}
  Issues: [list, if any]

Principle compliance: {pass / issues found}
  Issues: [list, if any]

Integration completeness: {pass / issues found}
  Issues: [list, if any]

Findings:
F{n}: {title}
Confidence: {score}/100
Severity: CRITICAL / MAJOR / MINOR
Area: {which of the 5 holistic checks}
Evidence: {what the plan says vs what the spec/principles require}
Fix: {specific suggested fix}

Verdict: APPROVED / REVISE
(APPROVED = zero Critical, zero Major)
(REVISE = list specific fixes needed)
```

**Fix loop:** If REVISE, the plan author fixes the findings and re-runs the final holistic verifier. Cap: 2 cycles. If still not APPROVED after 2 cycles, escalate to the user with remaining findings.
</final_verification>

<success_criteria>
The skill is working when:

- Each plan task is verified against its spec section before the next task is written
- Deviations are caught and fixed at the task where they originate, not discovered downstream
- The fix-verify loop converges within 3 cycles (if it consistently hits the cap, the spec excerpts or task boundaries need improvement)
- The final plan, after all tasks pass verification, has zero spec contradictions
- Spec-principles conflicts are surfaced and escalated, not silently resolved by the author
- The verification audit trail shows a clear record of what was checked and what was fixed
- MINOR findings are logged but do not churn the fix-verify loop
- The final holistic verification passes (APPROVED) before the plan is presented to the user
- Spec coverage is explicitly measured and reported (not assumed from per-task passes)
</success_criteria>

<reference_index>
Per-task verifier prompt: `templates/verification-prompt.md`
Final holistic verifier prompt: `templates/final-verification-prompt.md`
</reference_index>
