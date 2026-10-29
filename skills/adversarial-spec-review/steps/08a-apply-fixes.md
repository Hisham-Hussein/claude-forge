<step_8a>
**Step 8a: Apply Fixes with Impact Tracing**

For each approved issue, BEFORE editing:

1. **Trace impact radius.** Search the spec (using Grep) for every reference to the entity being changed — field names, table names, state names, relationship names. List them. These are the locations you must check after editing.
2. **Read the target section** — read the actual file content around the edit point.
3. **Apply the fix** using the Edit tool. First fix the text that caused the problem: correct it, simplify it, or remove it, whichever fixes it. Add new text only if that can't fix it, and keep it short.
4. **Immediately check impact locations** — revisit each reference found in step 1. Update any that are now stale or inconsistent.

The purpose of the impact trace is to make cascading updates part of the fix, not an afterthought discovered in the next review round.
</step_8a>

