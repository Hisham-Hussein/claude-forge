<purpose>
Rules for synthesizing reviewer findings into a final issues list. The orchestrator applies these after each round to produce an honest, critically-evaluated assessment.
</purpose>

<cross_challenge_rules>

**Rule 1: Independent convergence is the strongest signal.**
When 2+ reviewers independently flag the same issue (even with different framing), that's a high-confidence finding. Prioritize these.

**Rule 2: Single-reviewer findings require verification.**
If only one reviewer flagged it, the orchestrator MUST verify it against the actual spec and codebase before including it. Read the relevant source file or spec section. Check if the concern is real. If verification is inconclusive (cannot confirm or deny from available evidence), include the finding at one severity level lower than the reviewer assigned, with a note: "Could not verify — flagged for user judgment."

**Rule 3: Discard findings that are style preferences, not executability flaws.**
"The task should use a more descriptive variable name" is a style preference. "The task creates a function with 3 parameters but the caller in Task 7 passes 4 arguments" is an executability flaw. Only executability flaws matter.

**Rule 4: Discard manufactured severity.**
Reviewers sometimes inflate severity to justify their existence. Apply this test: "Would this issue actually block or derail execution, or is it something a competent developer would handle on the fly?" Critical = execution is impossible or produces wrong results. Major = execution succeeds but misses requirements or creates problems. Minor = developer can handle it.

**Rule 5: Check if fixes from prior rounds introduced new problems.**
Each round of fixes can create regressions — a reordered task may break a dependency, a split task may duplicate setup code. Explicitly ask: "Did fixing X break Y?" This is the Devil's Advocate's primary job in rounds 2+.

**Rule 6: Judge spec coverage explicitly.**
After collecting findings, the orchestrator must answer: "If a developer executes this plan task by task, will the spec's requirements be fully implemented?" This is not about individual issues — it's a holistic assessment. A plan can have zero individual Critical findings yet still fail to cover the spec due to cumulative gaps. If the answer is "no" or "probably not," that is a Critical finding even if no single reviewer flagged it.

</cross_challenge_rules>

<severity_calibration>

**Critical** — The plan as written would fail to execute, produce incorrect results, or miss a spec requirement entirely. A developer following the plan would build the wrong thing or get stuck.
Examples: missing task that creates a type other tasks import, dependency ordering that makes a task impossible, test that asserts the wrong behavior, spec requirement with zero task coverage.

**Major** — The plan has a real gap that would cause implementation problems, but a competent developer might catch and fix it during execution. Still should be fixed in the plan.
Examples: vague step that needs more specificity, test that only covers happy path for complex logic, task that partially covers a spec requirement but misses edge cases, file path that looks wrong.

**Minor** — Polish, style, or implementation details that are obvious to the implementer and wouldn't cause execution problems.
Examples: commit message could be more descriptive, test variable names are generic, step could mention an existing utility function.

</severity_calibration>

<convergence_criteria>

The review loop STOPS when ALL of these are true:
1. All reviewers report zero Critical and zero Major findings
2. The orchestrator's critical judgment agrees (no reviewer missed anything obvious)
3. No prior-round fixes introduced regressions

The orchestrator declares: "Plan is execution-ready. N rounds, M total reviewers, all converged on zero Critical/Major."

If after 5 rounds there are still Critical/Major issues, the orchestrator should pause and tell the user: "After 5 rounds we're still finding issues. The plan may need a structural rethink, not just iterative fixes. Here's what's still broken: [list]."

</convergence_criteria>

<presentation_format>

After each round, present to the user:

```
## Round N Review — [Verdict]

### Team: [list reviewers and their focus areas]

### Critical Issues (N)
For each: title, severity, section/task reference, description, recommended fix, evidence from spec/code

### Major Issues (N)
Same format

### Dropped Findings
Brief list of what reviewers flagged but the orchestrator downgraded or dropped, with reasoning

### Verdict
[Either "N Critical, M Major — fixes needed" or "Plan is execution-ready"]
```

</presentation_format>
