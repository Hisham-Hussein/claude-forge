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

**Rule 4: Score each finding before classifying severity.**
For every finding that survives Rules 1-3, the orchestrator MUST assign a confidence score (0-100) before classifying it as Critical, Major, or Minor. This is mandatory — do not skip this step.

Score each finding by completing this sentence: "I am __% confident this finding is real AND would cause problems in practice." Use the confidence scoring rubric in `<confidence_scoring>` to calibrate. Then apply the thresholds:
- Score < 60: Drop (not reported to user)
- Score 60-79: Minor — note for implementer, fix if easy
- Score 80+: Major — fix before execution
- Critical: Identified by nature (execution failure, incorrect results, missed spec requirements), not by confidence score. Critical findings bypass scoring.

The score must be written down for each finding. If you cannot write "I am 80% confident this would cause problems in practice," it is not Major.

**Rule 5: Check if fixes from prior rounds introduced new problems.**
Each round of fixes can create regressions — a reordered task may break a dependency, a split task may duplicate setup code. Explicitly ask: "Did fixing X break Y?" This is the Devil's Advocate's primary job in rounds 2+.

**Rule 6: Judge spec coverage explicitly.**
After collecting findings, the orchestrator must answer: "If a developer executes this plan task by task, will the spec's requirements be fully implemented?" This is not about individual issues — it's a holistic assessment. A plan can have zero individual Critical findings yet still fail to cover the spec due to cumulative gaps. If the answer is "no" or "probably not," that is a Critical finding even if no single reviewer flagged it.

</cross_challenge_rules>

<solo_reviewer_adaptation>

When Mode C (Solo Reviewer) is used, the cross-challenge rules adapt:

**Rule 1 adaptation:** Independent convergence is replaced by cross-lens convergence. If the solo reviewer flags the same issue under multiple lenses, treat it as a convergence signal equivalent to multi-reviewer convergence.

**Rule 2 adaptation:** Becomes the DEFAULT for all findings. Every Critical and Major finding from the solo reviewer requires orchestrator verification against the actual spec and codebase. This is more work for the orchestrator but is essential — a single reviewer has more potential blind spots than a team.

**Rules 3-6:** Apply unchanged.

**Orchestrator spot-check requirement:** After processing the solo reviewer's findings, the orchestrator MUST independently examine the top 3 riskiest areas of the plan (as identified in Step 1 analysis). If the orchestrator finds issues the solo reviewer missed, those are added as orchestrator-originated findings. This compensates for the loss of multi-reviewer diversity.

</solo_reviewer_adaptation>

<severity_calibration>

**Critical** — (bypasses confidence scoring) The plan as written would fail to execute, produce incorrect results, or miss a spec requirement entirely. A developer following the plan would build the wrong thing or get stuck.
Examples: missing task that creates a type other tasks import, dependency ordering that makes a task impossible, test that asserts the wrong behavior, spec requirement with zero task coverage.

**Major** — (confidence score 80+) The plan has a real gap that would cause execution problems AND the implementer would not catch it without the plan mentioning it. Verified real, will be hit in practice.
Examples: vague step that needs more specificity, test that only covers happy path for complex logic, task that partially covers a spec requirement but misses edge cases, file path that looks wrong.

**Minor** — (confidence score 60-79) Real gap, but likely caught by a competent implementer. Note for implementer, fix if easy. Findings scoring below 60 are dropped entirely.
Examples: commit message could be more descriptive, test variable names are generic, step could mention an existing utility function, defense-in-depth improvements where primary coverage already exists.

</severity_calibration>

<confidence_scoring>

Score each non-Critical finding on a 0-100 confidence scale. The question is:
"How confident am I that this is a REAL issue that would cause PROBLEMS IN PRACTICE?"

0:  Not confident. False positive that doesn't survive light scrutiny, or a
    pre-existing issue the plan didn't introduce.

25: Somewhat confident. Might be real, but could be a false positive. Unable to
    verify against the actual codebase. If the concern is theoretical ("what if
    a future API change..."), it belongs here unless there is concrete evidence.

50: Moderately confident. Verified real against the codebase, but unlikely to be
    hit in practice, or a nitpick that a competent developer would handle without
    guidance. Not important relative to the rest of the plan.

60-79: Confident. Double-checked and verified as real. A competent implementer
    would LIKELY catch it, but it's a genuine gap worth noting. Defense-in-depth
    improvements (a second safety layer where the primary coverage already works),
    documentation that prevents confusion, and ambiguities that could lead to
    divergent implementations belong here.
    → Classified as **Minor** (note for implementer, fix if easy).

80-100: High confidence. Verified real, will be hit in practice, and the existing
    approach is insufficient. The implementer would NOT catch this without the
    plan mentioning it. Directly impacts correctness or functionality. Or:
    directly violates a stated project principle (CLAUDE.md / architecture doc).
    → Classified as **Major** (fix before execution).

IMPORTANT: "The fix is easy" is not a severity input. A trivially fixable gap
can still be Minor (score 60-79) if a developer would catch it. Ease of fix
determines whether a Minor is "fix if easy" vs "note for implementer" — it does
NOT upgrade Minor to Major.

IMPORTANT: "Pattern-setting story" is not an automatic severity amplifier. A
finding in a pattern-setting story is Major only if it scores 80+ on its own
merits. If the concern is that the pattern will propagate, verify: would the
propagation actually cause problems, or would developers in future stories also
catch and handle it?

</confidence_scoring>

<principle_violation_calibration>

Some archetypes (Software Architecture, Performance & Scalability, Observability & Resilience) review the plan's code against the approved spec's design decisions and the project's stated principles. Their findings follow a different evidence chain than functional-coverage archetypes: plan code → spec/principle divergence, not plan task → spec requirement gap.

When evaluating these findings:

1. **Spec divergence outranks general principles.** If the approved spec explicitly prescribes an architectural decision (e.g., "use adapter pattern for Airtable") and the plan's code violates it, that's at minimum Major — the plan doesn't implement the approved design. The spec was already reviewed and approved; the plan should follow it.

2. **CLAUDE.md principles are project-level requirements.** If CLAUDE.md states a principle (e.g., "vendor portability," "depend on abstractions") and the plan violates it, treat it like a stated requirement — Major if the violation is structural and affects the codebase broadly. If CLAUDE.md doesn't state the principle, downgrade to Minor.

3. **Check scope of impact.** A violation in a utility function used once is Minor. The same violation in a core service used by every pipeline stage is Major — fixing it later touches everything.

4. **Check if the plan is phase-appropriate.** If this is a Phase 1/MVP plan and the spec or architecture doc explicitly defers certain concerns to later phases, a violation of a deferred concern is Minor at most. But if the plan creates a structure that PREVENTS the deferred concern from being addressed later (e.g., hardwiring vendor calls so deeply that adding adapters later requires rewriting every consumer), that's Major regardless of phase.

5. **The "would they know?" test still applies.** If a principle violation is something a competent developer would recognize and fix during implementation without the plan mentioning it, it's Minor. If the violation is structural (wrong module boundary, missing adapter layer, generic catch-all where classification is needed) and the developer would follow the plan's structure faithfully, it's Major — they wouldn't know to deviate from the plan.

</principle_violation_calibration>

<convergence_criteria>

The review loop STOPS when ALL of these are true:
1. All reviewers report zero Critical and zero Major findings
2. The orchestrator's critical judgment agrees (no reviewer missed anything obvious)
3. No prior-round fixes introduced regressions

The orchestrator declares: "Plan is execution-ready. N rounds, M total reviewers, all converged on zero Critical/Major."

If after 5 rounds there are still Critical/Major issues, the orchestrator should pause and tell the user: "After 5 rounds we're still finding issues. The plan may need a structural rethink, not just iterative fixes. Here's what's still broken: [list]."

**Mode C note:** For Mode C (Solo Reviewer), convergence requires the solo reviewer to report zero Critical/Major AND the orchestrator's spot-check of the top 3 riskiest areas to find no additional issues. A clean solo pass without the orchestrator's spot-check is NOT convergent.

</convergence_criteria>

<presentation_format>

After each round, present to the user:

```
## Round N Review — [Verdict]

### Team: [list reviewers and their focus areas]

### Critical Issues (N)
For each: title, severity, section/task reference, description, recommended fix, evidence from spec/code

### Major Issues (N) — confidence 80+
For each: title, confidence score, section/task reference, description, recommended fix, evidence from spec/code

### Minor Issues (N) — confidence 60-79
For each: title, confidence score, section/task reference, brief description, recommendation (note for implementer / fix if easy)

### Dropped Findings
Brief list of what reviewers flagged but the orchestrator scored below 60 or downgraded, with the score and reasoning

### Verdict
[Either "N Critical, M Major — fixes needed" or "Plan is execution-ready"]
```

</presentation_format>
