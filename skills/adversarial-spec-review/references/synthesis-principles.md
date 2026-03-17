<purpose>
Rules for synthesizing reviewer findings into a final issues list. The orchestrator applies these after each round to produce an honest, critically-evaluated assessment.
</purpose>

<cross_challenge_rules>

**Rule 1: Independent convergence is the strongest signal.**
When 2+ reviewers independently flag the same issue (even with different framing), that's a high-confidence finding. Prioritize these.

**Rule 2: Single-reviewer findings require code verification.**
If only one reviewer flagged it, the orchestrator MUST verify it against the actual codebase before including it. Read the relevant source file. Check if the concern is real.

**Rule 3: Discard findings that are implementation details, not design flaws.**
"The spec doesn't specify the exact function name" is an implementation detail. "The spec says to use upsert but upsert can create ghost records" is a design flaw. Only design flaws matter.

**Rule 4: Discard manufactured severity.**
Reviewers sometimes inflate severity to justify their existence. Apply this test: "Would a senior engineer stop the review to fix this before implementation, or would they note it and move on?" Critical = stop everything. Major = fix before implementing. Minor = note for implementer.

**Rule 5: Check if fixes from prior rounds introduced new problems.**
Each round of fixes can create regressions. Explicitly ask: "Did fixing X break Y?" This is the Devil's Advocate's primary job in rounds 2+.

</cross_challenge_rules>

<severity_calibration>

**Critical** — The spec as written would produce incorrect behavior, data loss, or security vulnerability if implemented literally. A developer following the spec would build the wrong thing.
Examples: protection mechanism that doesn't actually protect, write path that deletes data, auth bypass.

**Major** — The spec has a real gap that would cause implementation problems, but a competent developer might catch it during implementation. Still should be fixed in the spec.
Examples: missing env vars, unspecified interface changes, contradictions between sections, missing error handling for likely scenarios.

**Minor** — Documentation polish, missing implementation details that are obvious to the implementer, or edge cases that can be handled during implementation.
Examples: formula field not named, section cross-references missing, batch size rationale not documented.

</severity_calibration>

<convergence_criteria>

The review loop STOPS when ALL of these are true:
1. All reviewers report zero Critical and zero Major findings
2. The orchestrator's critical judgment agrees (no reviewer missed anything obvious)
3. No prior-round fixes introduced regressions

The orchestrator declares: "Spec is implementation-ready. N rounds, M total reviewers, all converged on zero Critical/Major."

If after 5 rounds there are still Critical/Major issues, the orchestrator should pause and tell the user: "After 5 rounds we're still finding issues. The spec may need a structural rethink, not just iterative fixes. Here's what's still broken: [list]."

</convergence_criteria>

<presentation_format>

After each round, present to the user:

```
## Round N Review — [Verdict]

### Team: [list reviewers and their focus areas]

### Critical Issues (N)
For each: title, severity, section reference, description, recommended fix, code evidence

### Major Issues (N)
Same format

### Dropped Findings
Brief list of what reviewers flagged but the orchestrator downgraded or dropped, with reasoning

### Verdict
[Either "N Critical, M Major — fixes needed" or "Spec is implementation-ready"]
```

</presentation_format>
