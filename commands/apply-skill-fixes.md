---
description: Apply upstream fixes from an audit report to a skill's source files
argument-hint: <path-to-audit-report> [U-1 U-3 ...]
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Task
  - TodoWrite
  - AskUserQuestion
---

<objective>
Apply the proposed upstream skill fixes from the audit report to the skill's source files in the marketplace directory.

This command reads a report produced by `/audit-skill-output`, parses the structured fix proposals (U-{N} blocks), and applies them to the correct skill source files. Edits go to `~/.claude/plugins/marketplaces/<plugin>/skills/<skill-name>/` — NEVER to `~/.claude/plugins/cache/`.

**Arguments:** `$ARGUMENTS` contains the report path as the first token, followed by optional fix IDs.
- `/apply-skill-fixes reviews/audit-report.md` — interactive mode (asks which fixes to apply)
- `/apply-skill-fixes reviews/audit-report.md U-1 U-3 U-5` — apply only these specific fixes
- `/apply-skill-fixes reviews/audit-report.md all` — apply all fixes without prompting
</objective>

<process>
1. **Parse arguments and read the report**
   - Split `$ARGUMENTS` into tokens. The first token is the report path. Remaining tokens are optional fix selectors (`U-1`, `U-3`, etc.) or the keyword `all`.
   - Read the report file at the parsed path.
   - Extract the **Metadata** table at the top of the report. Parse by matching bold field names in the first column:
     - `Skill identifier` — e.g. `claude-forge:create-business-case`
     - `Plugin` — e.g. `claude-forge`
     - `Skill name` — e.g. `create-business-case`
     - `Skill root` — e.g. `~/.claude/plugins/marketplaces/claude-forge/skills/create-business-case`
   - Verify the skill root directory exists. If not, abort with an error.

2. **Extract all upstream fix blocks** from the report
   - Scan the "Recommendations > Upstream" section (and "Root Cause Analysis" sections if fixes are embedded there)
   - Each fix block follows this contract:
     ```
     #### Fix U-{N}: {Title}
     - **Priority:** Critical | High | Medium | Low
     - **Target file:** `{relative path from skill root}`
     - **Action:** ADD | REPLACE | RESTRUCTURE
     - **Location:** {section name or placement guidance}
     - **Current content:** (for REPLACE only)
     - **Proposed content:**
     - **Rationale:** {why this is generalizable}
     ```
   - Build a list of all fixes with their number, title, priority, target file, action, and content.

3. **Determine which fixes to apply**
   - Always show a numbered table of all extracted fixes: Fix ID, Priority, Target File, Action, Title.
   - Then branch based on the parsed arguments:
     - **Explicit fix IDs provided** (e.g. `U-1 U-3 U-5`): Filter to only those fixes. Confirm with the user: "Applying U-1, U-3, U-5. Proceed?" (Yes / Cancel).
     - **`all` keyword provided**: Apply every fix. Confirm with the user: "Applying all N fixes. Proceed?" (Yes / Cancel).
     - **No fix IDs provided** (interactive mode): Ask the user which fixes to apply using AskUserQuestion:
       - "Apply all fixes" (default)
       - "Select specific fixes to skip"
       - "Cancel — do not apply"
       - If the user selects specific fixes to skip, ask which U-{N} numbers to exclude.
   - If any requested fix IDs don't exist in the report (e.g. `U-99`), warn the user and list valid IDs.

4. **Spawn a sub-agent** (via Task tool) to apply the approved fixes
   - Pass the sub-agent:
     - The full report content (or relevant sections)
     - The skill root path
     - The list of approved fixes (after any exclusions)
     - Clear instructions on the edit protocol:
       a. For each fix, read the target file first
       b. For ADD actions: insert the proposed content at the specified location
       c. For REPLACE actions: find the current content and replace with proposed content
       d. For RESTRUCTURE actions: reorganize the section as described
       e. After each fix, confirm the edit was applied correctly
   - The sub-agent must:
     - Edit files ONLY under the skill root in `~/.claude/plugins/marketplaces/` (never `~/.claude/plugins/cache/`)
     - Apply fixes one at a time as discrete, reviewable changes
     - Track progress using TodoWrite (one todo per fix)
     - Report what was changed, in which file, and why

5. **Summarize results** after the sub-agent completes
   - List each fix applied: file modified, action taken, brief description
   - List any fixes that were skipped (user-excluded or failed)
   - Remind the user to commit changes in the plugin marketplace repo if desired
</process>

<success_criteria>
- Report metadata parsed correctly (plugin, skill name, skill root resolved)
- All U-{N} fix blocks extracted from the report
- User confirmed which fixes to apply before any edits
- Each approved fix applied to the correct file in the marketplace source directory
- No edits made to `~/.claude/plugins/cache/`
- Summary of all changes provided to the user
</success_criteria>

<verification>
After applying fixes, verify:
- Each modified file still has valid markdown structure
- The skill root directory contains the expected files (SKILL.md, templates/, etc.)
- No files were created or modified outside the skill root directory
- Changes are consistent with the fix proposals (no drift from proposed content)
</verification>

<output>
Files modified: Skill source files under `~/.claude/plugins/marketplaces/<plugin>/skills/<skill-name>/`
No new files created by the command itself (fixes may add content to existing files or create new sections within them)
</output>
