<purpose>
Rules for synthesizing reviewer findings into a final issues list. The orchestrator applies these after each round to produce an honest, critically-evaluated assessment.
</purpose>

<cross_challenge_rules>

**Rule 1: Independent convergence is the strongest signal.**
When 2+ reviewers independently flag the same issue (even with different framing), that's a high-confidence finding. Prioritize these.

**Rule 2: Single-reviewer findings require code verification.**
If only one reviewer flagged it, the orchestrator MUST verify it against the actual codebase before including it. Read the relevant source file. Check if the concern is real. If verification is inconclusive (cannot confirm or deny from available evidence), include the finding at one severity level lower than the reviewer assigned, with a note: "Could not verify — flagged for user judgment."

**Rule 3: Discard findings that are implementation details, not design flaws.**
"The spec doesn't specify the exact function name" is an implementation detail. "The spec says to use upsert but upsert can create ghost records" is a design flaw. Only design flaws matter.

**Rule 4: Discard manufactured severity.**
Reviewers sometimes inflate severity to justify their existence. Apply this test: "Would a senior engineer stop the review to fix this before implementation, or would they note it and move on?" Critical = stop everything. Major = fix before implementing. Minor = note for implementer.

**Rule 5: Check if fixes from prior rounds introduced new problems.**
Each round of fixes can create regressions. Explicitly ask: "Did fixing X break Y?" This is the Devil's Advocate's primary job in rounds 2+.

**Rule 6: Judge goal achievement explicitly.**
After collecting findings, the orchestrator must answer: "If a developer implements this spec literally, will the stated objective be achieved?" This is not about individual issues — it's a holistic assessment. A spec can have zero individual Critical findings yet still fail to achieve its goal due to cumulative gaps or a flawed overall approach. If the answer is "no" or "probably not," that is a Critical finding even if no single reviewer flagged it.

**Rule 7: Apply stricter severity calibration in Round 2+.**
In Round 1, a borderline finding may reasonably be kept as Major — it's the first pass, and caution is appropriate. In Round 2+, apply a HIGHER bar: if an issue was in scope during Round 1 but wasn't caught by any reviewer, it is almost certainly Minor (if it were truly Major, at least one of N reviewers would have flagged it). The only findings that can be Major in Round 2+ are: (a) regressions introduced by Round N-1 fixes, or (b) issues that were literally invisible until a Round N-1 fix revealed them. Everything else is Minor by default — the orchestrator must justify upgrading it with specific evidence of why prior rounds couldn't have caught it.

</cross_challenge_rules>

<solo_reviewer_adaptation>

When Mode C (Solo Reviewer) is used, the cross-challenge rules adapt:

**Rule 1 adaptation:** Independent convergence is replaced by cross-lens convergence. If the solo reviewer flags the same issue under multiple lenses, treat it as a convergence signal equivalent to multi-reviewer convergence.

**Rule 2 adaptation:** Becomes the DEFAULT for all findings. Every Critical and Major finding from the solo reviewer requires orchestrator verification against the actual codebase. This is more work for the orchestrator but is essential — a single reviewer has more potential blind spots than a team.

**Rules 3-6:** Apply unchanged.

**Orchestrator spot-check requirement:** After processing the solo reviewer's findings, the orchestrator MUST independently examine the top 3 riskiest areas of the spec (as identified in Step 1 analysis). If the orchestrator finds issues the solo reviewer missed, those are added as orchestrator-originated findings. This compensates for the loss of multi-reviewer diversity.

</solo_reviewer_adaptation>

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

**Mode C note:** For Mode C (Solo Reviewer), convergence requires the solo reviewer to report zero Critical/Major AND the orchestrator's spot-check of the top 3 riskiest areas to find no additional issues. A clean solo pass without the orchestrator's spot-check is NOT convergent.

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
