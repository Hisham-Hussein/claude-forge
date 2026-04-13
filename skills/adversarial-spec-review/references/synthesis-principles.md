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

**Rule 4: Score each finding before classifying severity.**
For every finding that survives Rules 1-3, the orchestrator MUST assign a confidence score (0-100) before classifying it as Critical, Major, or Minor. This is mandatory — do not skip this step.

Score each finding by completing this sentence: "I am __% confident this finding is real AND would cause problems in practice." Use the confidence scoring rubric in `<confidence_scoring>` to calibrate. Then apply the thresholds:
- Score < 60: Drop (not reported to user)
- Score 60-79: Minor — note for implementer, fix if easy
- Score 80+: Major — fix before implementation
- Critical: Identified by nature (incorrect behavior, data loss, security), not by confidence score. Critical findings bypass scoring.

The score must be written down for each finding. If you cannot write "I am 80% confident this would cause problems in practice," it is not Major.

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

**Critical** — (bypasses confidence scoring) The spec as written would produce incorrect behavior, data loss, or security vulnerability if implemented literally. A developer following the spec would build the wrong thing.
Examples: protection mechanism that doesn't actually protect, write path that deletes data, auth bypass.

**Major** — (confidence score 80+) The spec has a real gap that would cause implementation problems AND the implementer would not catch it without the spec mentioning it. Verified real, will be hit in practice.
Examples: missing env vars, unspecified interface changes, contradictions between sections, missing error handling for likely scenarios.

**Minor** — (confidence score 60-79) Real gap, but likely caught by a competent implementer. Note for implementer, fix if easy. Findings scoring below 60 are dropped entirely.
Examples: formula field not named, section cross-references missing, batch size rationale not documented, defense-in-depth improvements where primary protection already exists.

</severity_calibration>

<confidence_scoring>

Score each non-Critical finding on a 0-100 confidence scale. The question is:
"How confident am I that this is a REAL issue that would cause PROBLEMS IN PRACTICE?"

0:  Not confident. False positive that doesn't survive light scrutiny, or a
    pre-existing issue the spec didn't introduce.

25: Somewhat confident. Might be real, but could be a false positive. Unable to
    verify against the actual codebase. If the concern is theoretical ("what if
    a future API change..."), it belongs here unless there is concrete evidence.

50: Moderately confident. Verified real against the codebase, but unlikely to be
    hit in practice, or a nitpick that a competent developer would handle without
    guidance. Not important relative to the rest of the spec.

60-79: Confident. Double-checked and verified as real. A competent implementer
    would LIKELY catch it, but it's a genuine gap worth noting. Defense-in-depth
    improvements (a second safety layer where the primary protection already works),
    documentation that prevents confusion, and ambiguities that could lead to
    divergent implementations belong here.
    → Classified as **Minor** (note for implementer, fix if easy).

80-100: High confidence. Verified real, will be hit in practice, and the existing
    approach is insufficient. The implementer would NOT catch this without the
    spec mentioning it. Directly impacts correctness or functionality. Or:
    directly violates a stated project principle (CLAUDE.md / architecture doc).
    → Classified as **Major** (fix before implementation).

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

### Major Issues (N) — confidence 80+
For each: title, confidence score, section reference, description, recommended fix, code evidence

### Minor Issues (N) — confidence 60-79
For each: title, confidence score, section reference, brief description, recommendation (note for implementer / fix if easy)

### Dropped Findings
Brief list of what reviewers flagged but the orchestrator scored below 60 or downgraded, with the score and reasoning

### Verdict
[Either "N Critical, M Major — fixes needed" or "Spec is implementation-ready"]
```

</presentation_format>
