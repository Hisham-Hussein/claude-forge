---
description: Update roadmap folder (ACTIVE.md, QUEUE.md, LOG.md) based on conversation progress
---

<objective>
Review the current conversation and update the roadmap folder to reflect:
- Progress on the active work
- New discoveries or issues found
- Decisions made that should be logged

This maintains continuity across sessions by keeping `roadmap/` synchronized with actual work done.
</objective>

<context>
Active work:
@roadmap/ACTIVE.md

Queue and backlog:
@roadmap/QUEUE.md

Decision log:
@roadmap/LOG.md
</context>

<process>
1. **Analyze the conversation** to identify:
   - Tasks completed in this session
   - New issues, bugs, or improvements discovered
   - Progress on items in ACTIVE.md
   - Decisions made that should be logged
   - Any blockers that prevent continuing scheduled work

2. **Update LOG.md** (do this BEFORE trimming ACTIVE.md — decisions must be captured here first):
   - Add new entry at the TOP for significant decisions/completions
   - Format: `## YYYY-MM-DD: [Title]` followed by **2-3 sentences MAX** (not paragraphs, not bullet lists)
   - STRICT: Each entry = heading + one short paragraph. No sub-headings, no bullet lists, no "What was done / Impact / Artifacts" structure. Details live in ACTIVE.md and research docs — the log is a scannable index, not a record of everything.
   - Good: "Created custom `/execute-phase` skill (not GSD) because GSD won't enforce our architecture principles. Borrows wave parallelization and deviation rules but adds DOE integration. At `.claude/skills/execute-phase/`."
   - Bad: Multi-paragraph entry with "What was done:", "Key decisions:", "Impact:" sections and 15+ lines
   - **Queue behavior:** When adding a new entry, ALSO delete the oldest entry (last `## YYYY-MM-DD` section + its paragraph). One in, one out — every time.
   - Each entry should be self-contained (make sense without reading others)

3. **Update ACTIVE.md** (safe to trim now — decisions are captured in LOG.md):
   - Check off completed success criteria with `[x]`
   - Update progress section with THIS session's completions
   - Add any new sub-tasks discovered
   - Update "How to Continue" if next steps changed
   - **CONSISTENCY CHECK:** Scan supplementary content (specs, plans, designs embedded below the core sections) for staleness. If research or work completed this session produced updated designs that supersede embedded specs, update the specs to match or replace with a reference to the authoritative artifact. A fresh agent must never see conflicting instructions between "How to Continue" and the specs below.
   - **SIZE CONTROL:** ACTIVE.md should stay under ~200 lines. It's a Kanban board, not a history file. If preserving unique context pushes past 200 lines, that's OK — the preservation rule is absolute, the line limit is a guideline.
     - Keep only the LAST session's completed items (for handoff context). Older completions → delete them (they're now in LOG.md or research docs).
     - Large specs/plans that exist elsewhere → reference by file path instead of embedding.
     - **NEVER remove context that doesn't exist anywhere else.** If specs, decisions, or context are ONLY in ACTIVE.md, they MUST stay — the next session has no other way to recover them. When in doubt, keep it.
     - "How to Continue" = actionable next steps + key context a fresh agent needs.
     - Core sections only: Current Focus, Success Criteria, Progress (last session + not started), Blockers, How to Continue. Supplementary specs are OK when they're the only copy.

4. **Update QUEUE.md**:
   - Add new discoveries under the appropriate section (Next Up, topic-specific groups, or Backlog)
   - Promote items to "Next Up" if they become urgent
   - Remove items that were completed
   - Keep "Next Up" to roughly 5 items
   - **CRITICAL:** If clearing ACTIVE.md, ensure "Next Up" has at least one item (check project directives, strategic docs, or conversation context for logical next steps)

5. **Check artifacts index** (if `artifacts/` exists):
   - Scan `artifacts/` for all `.md` files (excluding ARTIFACTS-INDEX.md itself)
   - Compare against files listed in `artifacts/ARTIFACTS-INDEX.md`
   - If new files found that aren't in the index:
     - List the unindexed files to the user
     - Ask: "Should I add these to ARTIFACTS-INDEX.md?"
     - If yes, add entries with appropriate category (guides vs research) and brief description
   - This ensures new research and guides are discoverable

6. **Ensure handoff clarity** (critical for session transitions):
   - If work is in-progress, note specific files modified in this session
   - Note current state: tests passing/failing, build status, any errors
   - "How to Continue" first step must be immediately actionable (not "continue working on X")
   - Include any context a fresh agent would need to pick up seamlessly

7. **Verify ACTIVE.md core section alignment** (final consistency check):
   - After all updates, re-read ACTIVE.md and check that core sections tell the same story:
     - **Current Focus** = what we're working on right now
     - **Status** (in Progress section) = where we are in that work
     - **Success Criteria** = includes unchecked items for the current focus
     - **How to Continue** = next steps toward completing the current focus
   - If any section contradicts another (e.g., "Current Focus" says X but "How to Continue" says build Y instead), fix before finishing
   - Common inconsistency: updating "How to Continue" but forgetting to update "Current Focus" or "Status"

8. **Present summary** to user:
   - What was updated
   - Items checked off
   - New queue items added
   - Active blockers if any
</process>

<output>
Files modified:
- `roadmap/ACTIVE.md` - Progress updates, checked items
- `roadmap/QUEUE.md` - New discoveries, prioritization changes
- `roadmap/LOG.md` - New decision entries (if applicable)
</output>

<success_criteria>
- All completed work from conversation is reflected in roadmap
- New discoveries are captured in QUEUE.md with proper context
- ACTIVE.md accurately shows current state
- Significant decisions logged in LOG.md
- User receives clear summary of what changed
</success_criteria>
