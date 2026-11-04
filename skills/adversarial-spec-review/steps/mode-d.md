<mode_d>
**Mode D: Independent Reviewer Loop**

One fresh independent reviewer per round reviews the spec's decisions. The orchestrator judges every finding, fixes what is worth fixing without asking, and starts the next round. The loop stops at the first round where the orchestrator judges nothing Critical or Major; that round's worthwhile Minors are fixed and no further round runs.

**When to use:** a spec that holds decisions only and leaves the wiring to the implementation plan (for example a superpowers:brainstorming "Written Design"), when the user wants the review run to the end without approving each round.

**The user's choice of Mode D is the approval for every round's fixes and every new round of this review.** It replaces the asks in Steps 2, 5 (rounds 2+), 7 and 8c. It does not carry over to another review.

Mode D replaces Steps 2–9, except Steps 8a and 8b, which it runs in D5. Steps 0, 1 and 10 still apply. Post this checklist in Step 0 (or re-post it when the user picks Mode D at Step 5) and re-post it ticked as you go:

```
Review Progress (Mode D):
- [ ] D1: Read and analyze the spec (Step 1)
- [ ] D2: Mechanical checks before round 1
- [ ] D3: Spawn a fresh reviewer for round N
- [ ] D4: Judge every finding against the evidence (spike where nothing settles it)
- [ ] D5: Fix with Steps 8a and 8b (spike first where a fix depends on outside behaviour)
- [ ] D6: Re-run the mechanical checks, commit, report the round
- [ ] D7: Stop rule: next round, or the final Minor pass and Step 10
```

**D2: Mechanical checks before round 1.** Check what a script can check, so the reviewer's rounds go to decisions:
- If the project requires a checklist appendix in specs (for example a Verification Checklist), it is filled and has no gaps.
- Write a check script for this spec in the scratchpad, or reuse the project's if it keeps one. It checks: cross-references point at sections that exist; numbered lists run in order; cited files and `file:line` exist; every named setting, error code, route, table and email or template is declared once and used consistently; every requirement ID traces to a goal and a test; every list that must be complete matches its source. The script reads the spec path from `.review-state/active.json` and never writes the spec: the gate treats a `python` or `node` command that names the spec as a spec edit.
- If the spec has uncommitted changes, ask the user whether to commit them before round 1; D6 commits the spec each round.
- If the checks need spec edits, do them as round 0: set `round` to 0 in `active.json`, write `round-0/7-approved.md` (the user's Mode D quote and the check findings), then D5 and D6 for them, then set `round` to 1.

**D3: Spawn a fresh reviewer for round N.**
- Gate files: `round-N/0-checklist.md` (the checklist as posted) and `round-N/2-team-ok.md` (quote the user's words choosing Mode D; the same quote stands for every round).
- Prompt: `<mode_d_prompt_template>` in `templates/reviewer-task.md`, every field filled. Round 2+ also reviews the whole spec fresh; Step 4's narrowing rule does not apply in Mode D.
- Engine: Claude (one Agent call, `model: opus`) or Codex (one Codex job with slug `solo`, per "Reviewer engine" in `steps/05-spawn.md`). Ask once in round 1 unless the user named it.
- A new reviewer every round. Never continue a previous round's reviewer.

**D4: Judge every finding against the evidence.** Before any verdict:
- Open the cited spec lines and the cited evidence for each finding; confirm or refute it there. Never accept a finding, its severity or its suggested fix at face value. When a finding's truth depends on outside behaviour no evidence settles, spike it (D5) before the verdict, instead of Rule 2's downgrade-and-flag. A finding about the project's own code is settled by reading the code; one that stays inconclusive goes in the round report as unverified.
- Apply Rules 2–6 of `references/synthesis-principles.md`. Rule 7 does not apply: each Mode D round is a fresh review, so a Major found late is still Major.
- Re-rank on evidence: upgrade (a Minor can become Major), downgrade, or drop with a one-line reason. Wiring, items the spec leaves to the builder, and risks the spec accepts are not findings unless the acceptance is unreasonable.
- Every Critical or Major candidate gets the Rule 4 FOR/AGAINST weighing, written down.
- Spot-check the areas the last round's fixes touched (round 1: the 3 riskiest areas from Step 1). A Critical or Major issue you find there is a finding of this round.
- Decide the fix for every finding worth fixing, whatever its severity. The reviewer's suggested fix is an input, not the decision.
- Write `round-N/7-approved.md`: the user's Mode D quote, then per finding: fix or drop, judged severity, one-line reason.

**D5: Fix with Steps 8a and 8b.**
- **Spike before fix:** when a finding or a fix depends on how an outside system behaves (a library, API, browser or provider) and no existing evidence (a spike result, a cited source line, the vendor's docs) proves it, prove it first with a spike, record the result where the project keeps spike findings (its own commit, apart from the spec's), and cite it in the spec. Never write such behaviour into the spec from memory. Run spikes before the round's first spec edit: the gate blocks every `git commit` while the spec has unverified edits.
- Read `steps/08a-apply-fixes.md` and `steps/08b-verify.md` now and do both for every fix of the round. Write `round-N/8a-impact-trace.md` before the first spec edit and `round-N/8b-verification.md` (headings `## Pass 1`, `## Pass 2`, `## Pass 3`) before the commit. No fix goes in without them.

**D6: Re-run the checks, commit, report.**
- A round with nothing judged worth fixing skips D5 and the commit; report it and go to D7.
- Re-run the D2 script. Fix what it finds the same way (D5).
- Commit the round as one commit: `docs: fix N Critical + M Major + K Minor findings from adversarial review round R`, with a body listing each fix.
- Report the round to the user in a few lines: judged counts, what was fixed, what was dropped and why. Do not wait for an answer.

**D7: Stop rule**, decided by the round's D4 verdicts.
- **The round had a finding judged Critical or Major:** set `round` to N+1 in `active.json` and go to D3. Step 9's five-round stop does not apply; the loop ends by this rule or when the user says stop.
- **Nothing judged Critical or Major** (reviewer findings and your spot-check): this round's D5 and D6 fixed its worthwhile Minors, and that was the final pass. Run no further round. Do Step 10, and end with:
  ```
  Spec is implementation-ready (Mode D). N rounds. Critical/Major by round: R1 a, R2 b, ...
  Final Minors fixed: K. Dropped: [finding: reason]. Last commit: <sha>.
  ```
</mode_d>
