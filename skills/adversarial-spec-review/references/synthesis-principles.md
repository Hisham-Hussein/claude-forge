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

**Rule 4: Adversarial weighing before scoring — MANDATORY for every Critical and Major candidate.**
For every finding that survives Rules 1-3, the orchestrator MUST complete a forced adversarial weighing before assigning a confidence score. This is the most important rule in synthesis — skipping it is the primary cause of severity inflation.

**For every finding a reviewer rates Critical or Major, the orchestrator MUST write — visibly in the synthesis, not internally — three things:**

1. **Case FOR this severity:** In 1-2 sentences, the strongest argument that this finding is real, would be hit in practice, and the implementer would not catch it without the spec mentioning it.
2. **Case AGAINST this severity:** In 1-2 sentences, the strongest argument that this finding is not real, would not be hit in practice, or a competent implementer doing TDD would catch it naturally.
3. **Verdict:** Which argument wins, and the resulting confidence score.

The orchestrator must genuinely try to defeat each finding. If the AGAINST argument is stronger or even comparable to the FOR argument, the finding is NOT Major (and NOT Critical). A finding that survives adversarial weighing should feel obviously correct — the FOR argument should clearly dominate.

**Then** assign a confidence score (0-100) using the rubric in `<confidence_scoring>`:
- Score < 60: Drop (not reported to user)
- Score 60-79: Minor — note for implementer, fix if easy
- Score 80+: Major — fix before implementation
- Critical: Must survive adversarial weighing AND be about incorrect behavior, data loss, or security. A finding where the AGAINST argument holds any weight is not Critical.

The adversarial weighing and score must be written down for each finding. If you cannot write a FOR argument that clearly dominates the AGAINST argument, it is not Major.

**Hard disqualifiers — these findings are automatically Minor-or-below regardless of reviewer framing:**
- The spec shows correct code/example but surrounding prose is imprecise → Minor max
- A missing test scenario that TDD would discover naturally during implementation → Drop
- A scaling concern beyond 10x current realistic load → Drop
- The spec says the right thing but doesn't say it prominently enough → Minor max
- The existing codebase pattern already handles the concern without spec guidance → Drop

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

**Critical** — (bypasses confidence scoring but NOT adversarial weighing) The spec as written would produce incorrect behavior, data loss, or security vulnerability if implemented literally. A developer following the spec would build the wrong thing. The Rule 4 AGAINST argument must have no weight — if there is any reasonable counter-argument, it is Major at most, not Critical.
Examples: protection mechanism that doesn't actually protect, write path that deletes data, auth bypass.

**Major** — (confidence score 80+) The spec has a real gap that would cause implementation problems AND the implementer would not catch it without the spec mentioning it. Verified real, will be hit in practice.
Examples: missing env vars, unspecified interface changes, contradictions between sections, missing error handling for likely scenarios.

**Minor** — (confidence score 60-79) Real gap, but likely caught by a competent implementer. Note for implementer, fix if easy. Findings scoring below 60 are dropped entirely.
Examples: formula field not named, section cross-references missing, batch size rationale not documented, defense-in-depth improvements where primary protection already exists.

</severity_calibration>

<confidence_scoring>

PREREQUISITE: Every Critical and Major candidate MUST have completed Rule 4 adversarial weighing before reaching this rubric. If the FOR/AGAINST weighing was not written down, go back and do it. Scoring without adversarial weighing is the primary cause of severity inflation.

Score each finding (including Critical candidates that survived adversarial weighing) on a 0-100 confidence scale. Critical findings bypass the score-to-severity thresholds below (they are classified by nature, not score), but the score still serves as a sanity check — a Critical candidate scoring below 80 should be re-examined. The question is:
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
Include Rule 4 adversarial weighing: FOR argument, AGAINST argument, verdict

### Major Issues (N) — confidence 80+
For each: title, confidence score, section reference, description, recommended fix, code evidence
Include Rule 4 adversarial weighing: FOR argument, AGAINST argument, verdict

### Minor Issues (N) — confidence 60-79
For each: title, confidence score, section reference, brief description, recommendation (note for implementer / fix if easy)

### Dropped Findings
Brief list of what reviewers flagged but the orchestrator downgraded or dropped, with:
- Findings that failed adversarial weighing (AGAINST argument won) — show the FOR/AGAINST/verdict
- Findings that scored below 60 — show the score and reasoning
- Findings caught by hard disqualifiers — name the disqualifier

### Verdict
[Either "N Critical, M Major — fixes needed" or "Spec is implementation-ready"]
```

</presentation_format>
