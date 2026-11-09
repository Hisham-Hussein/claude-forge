# Update Roadmap — Detailed Steps

## Step 0: Check git history for cross-session work

Run BEFORE analyzing the conversation. This catches work done in other sessions.

```bash
git log --oneline --since="$(date -d '7 days ago' +%Y-%m-%d)"
git log --oneline --merges -10
```

- Compare commits and merged PRs against items in ACTIVE.md and QUEUE.md
- Any completed items still listed as "not started" or "in progress" → mark done
- Any merged PRs that correspond to QUEUE.md items → move out of the queue, as in Step 4

## Step 1: Analyze the conversation

Identify:
- Tasks completed in this session
- New issues, bugs, or improvements discovered
- Progress on items in ACTIVE.md
- Decisions made that should be logged
- Any blockers that prevent continuing scheduled work
- **User-confirmed manual completions**: Scan for messages like "I did it", "done", "I'm done with X", "I finished X". These indicate work the user completed outside the agent's tools (e.g., UI changes, manual steps). Each confirmation must be reflected as a checked-off success criterion.

## Step 2: Update LOG.md

Do this BEFORE trimming ACTIVE.md — decisions must be captured here first.

- Add new entry at the TOP for significant decisions/completions
- Format: `## YYYY-MM-DD: [Title]` followed by **2-3 sentences MAX** (not paragraphs, not bullet lists)
- STRICT: Each entry = heading + one short paragraph. No sub-headings, no bullet lists, no "What was done / Impact / Artifacts" structure. Details live in ACTIVE.md and research docs — the log is a scannable index, not a record of everything.
- Good: "Created custom `/execute-phase` skill (not GSD) because GSD won't enforce our architecture principles. Borrows wave parallelization and deviation rules but adds DOE integration. At `.claude/skills/execute-phase/`."
- Bad: Multi-paragraph entry with "What was done:", "Key decisions:", "Impact:" sections and 15+ lines
- **Queue behavior:** Add entry at TOP. When that makes more than 10 entries, move the entry at the BOTTOM word for word to `roadmap/ARCHIVE.md`, under `## Moved YYYY-MM-DD from LOG.md`. First read it for a decision still in force or open work, and send that to its home as in Step 3.
- Each entry should be self-contained (make sense without reading others)

## Step 3: Update ACTIVE.md

Older history can move out now — this session's decisions are captured in LOG.md.

- Check off completed success criteria with `[x]`
- Update progress section with THIS session's completions
- Add any new sub-tasks discovered
- Update "How to Continue" if next steps changed
- **CONSISTENCY CHECK:** Scan supplementary content (specs, plans, designs embedded below the core sections) for staleness. If research or work completed this session produced updated designs that supersede embedded specs, update the specs to match or replace with a reference to the authoritative artifact. A fresh agent must never see conflicting instructions between "How to Continue" and the specs below.
- **SIZE CONTROL:** ACTIVE.md is a Kanban board, not a history file: at most 200 lines and 40 KB. The KB limit matters because a few very long lines can dodge a line count. Step 9 enforces both.
  - **Nothing is deleted; it moves.** History leaves ACTIVE.md so each session starts light, and it stays findable in `roadmap/ARCHIVE.md`. The archive is a record to search when someone needs the history: never load it at the start of a session or add it to this skill's Context.
  - **What may leave ACTIVE.md:** only Progress entries older than the most recent day that has entries, Success Criteria items ticked `[x]` before this session (with their heading once none are left under it; a ticked item with an unticked item under it stays), and embedded specs that exist elsewhere (below). That whole day stays, because parallel sessions each need their last entry for handoff; if the file is still over a limit, that day's oldest entries move too, but never the entry this session wrote. Current Focus, unticked Success Criteria, Blockers and How to Continue stay.
  - **Before moving an entry or item, read it for anything still live.** Open work goes to QUEUE.md. A decision still in force goes to `roadmap/decisions/` or the spec it belongs to; LOG.md is no home for it, because it holds only 10 entries. Then move the whole entry word for word to the top of ARCHIVE.md, under `## Moved YYYY-MM-DD from ACTIVE.md`.
  - Large specs/plans that exist elsewhere → reference by file path instead of embedding, with the embedded text moved to ARCHIVE.md.
  - "How to Continue" = actionable next steps + key context a fresh agent needs.
  - Core sections only: Current Focus, Success Criteria (open items and this session's), Progress (most recent day + not started), Blockers, How to Continue. Supplementary specs are OK when they're the only copy.

## Step 4: Update QUEUE.md

- Add new discoveries under the appropriate section (Next Up, topic-specific groups, or Backlog)
- Promote items to "Next Up" if they become urgent
- **Move completed items to ARCHIVE.md, word for word, under `## Moved YYYY-MM-DD from QUEUE.md`** — do NOT leave struck-through items in Next Up. A completed item cluttering #1 misleads fresh agents about what to work on next.
- If an item was promoted from Backlog to Next Up, replace the Backlog entry with a pointer (e.g., "Promoted to Next Up #1") or remove it, moving any text that isn't in Next Up to ARCHIVE.md. Never have the same item described in both sections.
- **SIZE CONTROL:** QUEUE.md holds at most 200 lines and 60 KB (Step 9). Only finished or duplicated items may leave. Open work stays: to shorten an item, first confirm a spec holds its full detail, then point to that spec and move the long wording to ARCHIVE.md.
- Keep "Next Up" to roughly 5 items
- **LABELS:** Every QUEUE item starts with one bold work-area label, e.g. `**[BACK END]**`. The project's allowed labels are listed once in a `Labels:` line near the top of QUEUE.md (create it on first use from the labels already in the file, merging near-duplicates; keep the list short, about six). Use only listed labels; add a new one only when the work truly fits none. Label new items, relabel items whose label is missing or not on the list, and use the same labels on ACTIVE.md's Current Focus items, Success Criteria headings and How to Continue steps.
- **CRITICAL:** If clearing ACTIVE.md, ensure "Next Up" has at least one item (check project directives, strategic docs, or conversation context for logical next steps)
- **FRESH-AGENT CHECK (mandatory):** After all QUEUE.md edits, re-read Next Up #1 and ask: "If a fresh agent reads this right now with zero context, will it know exactly what to work on?" If #1 is a completed item, a vague reference, or points to something that doesn't match ACTIVE.md's Current Focus — fix it before proceeding.

## Step 5: Check artifacts index

Only if `artifacts/` exists:

- Scan `artifacts/` for all `.md` files (excluding ARTIFACTS-INDEX.md itself)
- Compare against files listed in `artifacts/ARTIFACTS-INDEX.md`
- If new files found that aren't in the index:
  - List the unindexed files to the user
  - Ask: "Should I add these to ARTIFACTS-INDEX.md?"
  - If yes, add entries with appropriate category (guides vs research) and brief description
- This ensures new research and guides are discoverable

## Step 6: Ensure handoff clarity

Critical for session transitions:

- If work is in-progress, note specific files modified in this session
- Note current state: tests passing/failing, build status, any errors
- "How to Continue" first step must be immediately actionable (not "continue working on X")
- Include any context a fresh agent would need to pick up seamlessly

## Step 7: Verify ACTIVE.md core section alignment

Final consistency check:

- **Re-read ACTIVE.md from disk** after all edits — do not rely on your memory of what you wrote
- Check that core sections tell the same story:
  - **Current Focus** = what we're working on right now
  - **Status** (in Progress section) = where we are in that work
  - **Success Criteria** = includes unchecked items for the current focus
  - **How to Continue** = next steps toward completing the current focus
- **Cross-check Success Criteria vs How to Continue**: For every `[x]` checked item in Success Criteria, verify it does NOT still appear in "How to Continue" or "Not Started". Checked-off items must be removed from future action lists.
- **Cross-check Success Criteria vs Not Started**: Any item in "Not Started" that has been checked `[x]` must be removed from "Not Started".
- If any section contradicts another (e.g., "Current Focus" says X but "How to Continue" says build Y instead), fix before finishing
- Common inconsistency: updating "How to Continue" but forgetting to update "Current Focus" or "Status"

## Step 8: Memory sync check

- If any project-level facts changed (deployment status, table IDs, architecture decisions, feature completions), check if memory files need updating
- Common triggers: PRs merged, new tables/fields created, infrastructure changes, key decisions made
- Update or create memory files as needed to keep future sessions informed

## Step 9: Run the roadmap check

Run this before committing, because it compares the roadmap with the last commit; if roadmap/ was already committed outside this skill this session, add `--base <the commit before that>`. `<skill directory>` is the base directory shown when this skill loaded.

```bash
node <skill directory>/scripts/check-roadmap.cjs
```

It must pass before the update is finished.

- **`LOST` line:** the line left the roadmap and exists nowhere else. Restore it, or move it to ARCHIVE.md word for word if it really is finished or replaced.
- **Over a limit:** move whatever Steps 3 and 4 allow. If nothing more may move, stop and tell the user which sections take the space. The user decides what happens to open work; the limit is never passed by deleting it, or by raising the limit in the script.
- **Exit code 2:** the check did not run, which is not a pass. Run it from the project root, or pass the root as the first argument. A `SKIP` line means that file had no earlier version to compare, so tell the user unless the file is new.

After any move made here, redo Step 7. The check can't see open work moved to the archive, or an item that lost up to about 30% of its words, so Steps 3 and 4 are what protect those.

## Step 10: Present summary to user

Summarize in ONE line only (e.g. "Roadmap updated."). No per-file breakdown, no lists. If the check could not pass, say so and name what is blocking it.
