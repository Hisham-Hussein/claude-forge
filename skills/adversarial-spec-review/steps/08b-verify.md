<step_8b>
**Step 8b: Verify Fixes**

After all fixes are applied, switch from editor mode to adversarial self-reviewer mode. Your goal is to find problems with your own edits before they waste a reviewer cycle.

Run three verification passes:

**Pass 1: Fix-to-finding validation.**
For each fix, re-read the original reviewer finding and the edit you applied. Ask: "Does this edit actually resolve the concern the reviewer raised, or did I address something adjacent?" If the fix is a partial resolution, note what's still unresolved.

**Pass 2: Consistency scan.**
For each fix that added, removed, or renamed anything:
- **Stale references:** Grep the entire spec for the old name or removed item. Zero matches required. If matches remain, update them.
- **Dropped items:** If you removed something (field, state, row), verify its function is absorbed elsewhere — not silently lost.
- **Incomplete enumerations:** If you added a list, mapping, or table that should be exhaustive, enumerate ALL items from the source of truth and compare against what you wrote. Gaps here are the most common regression.
- **Summary/count consistency:** If totals or counts appear anywhere in the spec (overview sections, headers, relationship tables), verify they still match reality.

**Pass 3: Re-read changed sections.**
Read each changed section of the actual file (not from memory). Verify markdown formatting is clean, tables render correctly, and the new content is consistent with the surrounding text style and conventions.

If any pass finds issues, fix them and re-run the specific pass on the affected fix. Do NOT proceed to commit with known issues.

**Present verification results:**
```
Verification of N fixes:
- X passed all checks
- Y had issues caught and corrected: [brief list]
All fixes verified clean.
```

This step is mandatory — not optional, not "if you have time." Skipping it is the primary driver of review round inflation. Every minute spent here saves 10 minutes of reviewer cycles.
</step_8b>

