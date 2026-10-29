<step_8c>
**Step 8c: Commit and Loop**

After verification passes:

1. Summarize what changed (list each fix briefly)
2. **Commit the round's fixes** as a single commit with message format:
   `docs: fix N Critical + M Major + K Minor findings from adversarial review round R`
   Include a body listing each fix for traceability. One commit per round — not per fix — because fixes within a round are semantically coupled and may touch overlapping sections.

**MANDATORY: Do NOT auto-start the next round.** Present the fix summary to the user and ask:
```
Round R fixes applied, verified, and committed. Ready to start Round R+1, or do you want to stop here?
```
Wait for explicit user confirmation before proceeding. Only after the user confirms, proceed to Step 4 with updated round context:
- Increment round number
- Set round_context to list all fixes applied
- Set round_specific_instructions — use the convergence-mode text from templates/reviewer-task.md (NOT the Round 1 text)
- Re-select reviewers if needed (same team is fine if spec scope hasn't changed)

**CRITICAL — Anti-escalation rule for Round N+1 prompts:**
- NEVER tell reviewers to "go deeper", "find what was missed", "expand scope", or "look harder"
- Round N+1 focus areas must be NARROWER than Round N — fix verification and regression checks only (see Step 4 Round 2+ rules)
- Consider switching to Mode C (Solo Reviewer) for Round 2+ — convergence rounds don't need the diversity of 5 parallel agents; a single focused pass verifying fixes is more cost-effective and less prone to scope creep
- The orchestrator's Round N+1 prompt must include the Round 2+ `{round_specific_instructions}` text from templates/reviewer-task.md.
</step_8c>

