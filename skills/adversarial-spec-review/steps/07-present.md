<step_7>
**Step 7: Present to User and Get Decision**

Present the round results to the user. End with one of:

**If Critical/Major issues found:**
```
Round N found X Critical, Y Major issues. Want me to apply fixes, and the K Minors shown?
```

**If zero Critical/Major:**
```
Spec is implementation-ready. N rounds, M total reviewer passes, all converged on zero Critical/Major. Want me to apply the K Minors shown?
```

Wait for user response:
- "Apply fixes" → proceed to Step 8a
- "Stop" or "good enough" → end
- User disagrees with findings → discuss, adjust, re-present
</step_7>

