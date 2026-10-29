<step_3>
**Step 3: Identify Files for Reviewers**

For each reviewer, determine which files they must read:

1. **Always include the spec itself**
2. **Source files referenced in the spec** — any file path mentioned (e.g., `src/airtableWriter.ts`)
3. **Source files implied by the spec** — if the spec mentions changing an interface, include the file that defines it. If it mentions a function, include the file containing it.
4. **Config and deployment files** — if the spec has operational implications
5. **Type definitions** — if the spec introduces or changes types
6. **Test files** — if the spec changes behavior that has existing tests

Use Glob and Grep to find files by name/pattern if needed. Don't guess paths — verify they exist.

Each reviewer gets the spec + their domain-relevant files. Prompt Critic also gets this skill's `references/prompt-critic-reference.md` (absolute path).
</step_3>

