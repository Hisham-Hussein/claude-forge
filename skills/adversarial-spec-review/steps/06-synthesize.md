<step_6>
**Step 6: Synthesize with Critical Judgment**

**Read `references/synthesis-principles.md` now** — it contains cross-challenge rules, severity calibration, and convergence criteria.

After all reviewers complete, apply synthesis-principles.md:

1. **Collect all findings** from task comments (Mode A), agent results (Modes B/C) or Codex `{slug}-review.md` files (Codex engine). With the Mixed engine, a finding raised by both a Claude and a Codex reviewer counts as independent convergence
2. **Cross-challenge:** check for independent convergence (2+ reviewers flagging same issue)
3. **Verify single-reviewer findings** — read the actual code to confirm or refute
4. **Adversarial weighing (Rule 4 — MANDATORY)** — For every Critical or Major candidate, write the FOR/AGAINST/verdict weighing visibly before scoring. Apply hard disqualifiers. This is the primary defense against severity inflation — do not skip it.
5. **Confidence-score each surviving finding** — For every finding that survived Rules 1-3 (and Rule 4 for Critical/Major candidates), assign a confidence score (0-100) using the rubric in `<confidence_scoring>`. Write the score next to each finding. Apply thresholds: <60 = drop, 60-79 = Minor, 80+ = Major.
6. **Drop noise** — remove implementation details and nitpicks that survived scoring
7. **Check for fix regressions** (round 2+) — did prior fixes create new problems?

Produce the final issues list using the presentation format from synthesis-principles.md.

**Mode C adaptation:** When the round used Mode C (Solo Reviewer), synthesis changes:
- Skip the cross-challenge step (there is only one reviewer) — instead, examine the reviewer's "Cross-Lens Observations" section for convergence signals (same issue surfacing under multiple lenses)
- Every Critical and Major finding requires orchestrator verification against the actual codebase (this is Rule 2 applied universally, since all findings are single-reviewer findings)
- The orchestrator MUST spot-check the top 3 riskiest areas identified in Step 1 (Round 2+: the areas the fixes touched) to verify the solo reviewer didn't miss anything — if the orchestrator finds Critical/Major issues the solo reviewer missed, those become orchestrator-originated findings and the round is NOT converged
- All other synthesis rules (severity calibration, noise dropping, fix regression checking, holistic goal achievement judgment) apply unchanged
</step_6>

