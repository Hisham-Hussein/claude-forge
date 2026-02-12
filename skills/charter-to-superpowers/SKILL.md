---
name: charter-to-superpowers
description: Use when starting or continuing execution of a .charter/ phase with superpowers skills. Invoke with a phase number.
---

<objective>
State-machine bridge from `.charter/` planning artifacts to the superpowers execution pipeline. Given a phase number, detects pipeline progress and outputs the exact prompt to run next.

**Invocation:** `/charter-to-superpower {N}` — single required argument: phase number (integer, 1-based).
</objective>

<quick_start>
```
/charter-to-superpower 1
```

Checks pipeline state in order (State 0→6), stops at the first incomplete step, and outputs the exact superpowers prompt to run.

States 2-4 cycle per execution group. A phase with 3 groups cycles: plan G1 → execute G1 → plan G2 → execute G2 → plan G3 → execute G3 → finish.
</quick_start>

<process>

**Check states in order. Stop at the first incomplete step and output its prompt.**

**Why plan per group (not all at once):** writing-plans produces complete code in plans. Group 2 stories depend on Group 1's code existing (e.g., US-004 creates HookGrid.tsx, then US-003 imports it). Planning per group after prior groups are implemented gives writing-plans real code to reference.

<state_0 title="No phase plan">
**Check:** `.charter/PHASE-{N}-PLAN.md` does not exist.

**Output:**
```
Phase {N} plan not found. Run plan-phase-tasks first:

/plan-phase-task {N}           # without UI stories
/plan-phase-task {N} --has-ui  # with UI stories
```
</state_0>

<state_1 title="Phase plan exists, no worktree">
**Check:** `.charter/PHASE-{N}-PLAN.md` exists AND no worktree for this phase (see `<detection_logic>`).

**Pre-check — .charter/ must be committed.** Run `git status .charter/ --short`. If any files show `??` (untracked), block and output:
```
.charter/ files are untracked. Commit them before creating the worktree,
otherwise the worktree won't have access to your planning artifacts:

git add .charter/
git commit -m "Add .charter/ planning artifacts for Phase {N}"
git push

Then re-run: /charter-to-superpower {N}
```

**Extract from phase plan:**
- Phase name from `# Phase {N} Plan: {name}` heading
- Slugify name: "Walking Skeleton -- End-to-End Hook Browsing" → "walking-skeleton" (lowercase, hyphens, drop everything after " -- ")

**Output:**
```
Next step: Create an isolated worktree.

/superpowers:using-git-worktrees

Feature: Phase {N} {phase-name}
Branch: feat/phase-{N}-{slugified-phase-name}
```
</state_1>

<state_2 title="Worktree exists, current group needs planning">
**Check:** Worktree exists. Current execution group (see `<detection_logic>`) has no matching plan file in the worktree's `docs/plans/`.

**Extract from phase plan:**
- Current group number and its stories (from Parallelism Analysis section)
- `UX Inputs Loaded` field from Metadata section

**Detect tech stack file:** Check for a tech stack document in `.charter/` by testing these filenames in order (first match wins):
- `.charter/TECH-DECISIONS.md`
- `.charter/TECH-STACK.md`
- `.charter/tech-decisions.md`

If found, set `{TECH_STACK_LINE}` to `Tech Stack: .charter/{matched-filename}`. If none found, set `{TECH_STACK_LINE}` to empty (omit entirely).

**Ask the user:** Which prompt version to use?
- **V1 (original)** — presents the phase plan's FDD tasks as the spec
- **V2 (transform)** — presents the phase plan as context to transform

<prompt_v1>
**Output (V1 — original):**
```
Next step: Create TDD implementation plan for Execution Group {G}.

/superpowers:writing-plans

Spec: .charter/PHASE-{N}-PLAN.md
Architecture: .charter/ARCHITECTURE-DOC.md
{UI_REFERENCE_LINE}
{TECH_STACK_LINE}

Plan Execution Group {G} stories only: {story-list}.
The phase plan has the full FDD task decomposition with I/O/Test
per task and Design OS section references for UI tasks.
Focus on these stories: {story-ids with names}.
Include the story ID prefix in each commit message
(e.g., "feat(US-001): add HeroBanner component").
```
</prompt_v1>

<prompt_v2>
**Output (V2 — transform):**
```
Next step: Create TDD implementation plan for Execution Group {G}.

/superpowers:writing-plans

Spec: .charter/PHASE-{N}-PLAN.md
Architecture: .charter/ARCHITECTURE-DOC.md
{UI_REFERENCE_LINE}
{TECH_STACK_LINE}

Plan Execution Group {G} stories only: {story-list}.
The phase plan has FDD context per task (I/O/Test, file paths, layers,
Design OS refs). Use it as reference, not as a task list — transform
the decomposition into your own plan per your skill instructions.
Focus on these stories: {story-ids with names}.
Include the story ID prefix in each commit message
(e.g., "feat(US-001): add HeroBanner component").
```
</prompt_v2>

**UI Reference line rule:** Only include `UI Reference: .charter/design-os-export/` when `UX Inputs Loaded` contains "Design OS export" (i.e., `.charter/design-os-export/` exists). For all other values — fallback UX path, "No", or "N/A" — omit the line entirely. In the fallback case, plan-phase-tasks already embedded UX specs inline in task Input fields.

**Tech Stack line rule:** Check `.charter/` for a tech stack file (`TECH-DECISIONS.md`, `TECH-STACK.md`, or `tech-decisions.md` — first match wins). Only include `Tech Stack: .charter/{filename}` when a matching file exists. If no match, omit the line entirely. This gives `writing-plans` concrete technology choices (frameworks, libraries, database) to use when translating design references into implementation code.
</state_2>

<state_3 title="Current group planned, needs execution">
**Check:** Plan file exists in worktree's `docs/plans/` for current group (see `<detection_logic>`). Stories not yet complete.

**Extract:** Stories in current group. Whether group has 1 story or 2+.

<single_story>
**If current group has 1 story:**

```
Next step: Execute the plan for {story-id}: {story-name}.

/superpowers:subagent-driven-development

Plan: docs/plans/{plan-filename}
Execute tasks for {story-id}: {story-name}
{NOT_LAST_GROUP_WARNING}
```
</single_story>

<multi_story>
**If current group has 2+ stories:**

```
Next step: Execute {count} stories in Execution Group {G}. Two options:

OPTION A — Sequential (safe, one session):
Run subagent-driven-development ONCE with the full group plan.
All tasks across all {count} stories execute sequentially in a single session.

IMPORTANT: Do NOT invoke subagent-driven-development multiple times
(once per story) with the same plan. TodoWrite progress tracking is
per-session — re-invoking loses state and causes duplicate work.

/superpowers:subagent-driven-development

Plan: docs/plans/{plan-filename}
{NOT_LAST_GROUP_WARNING}

OPTION B — Parallel (faster, multiple sessions):
Prerequisite: commit the group plan so sub-worktrees can access it:

git add docs/plans/{plan-filename}
git commit -m "Add Execution Group {G} implementation plan"

Then create a separate worktree per story:

{for each story: git worktree add .worktrees/{story-slug} -b feat/{story-slug}}

In each worktree session, run executing-plans scoped to ONE story:

/superpowers:executing-plans

Plan: docs/plans/{plan-filename}
Execute ONLY the tasks for {story-id}: {story-name}.
Skip all other stories in this plan.

{NOT_LAST_GROUP_WARNING}

After ALL story branches complete, merge them into the phase branch:

cd {phase-worktree-path}
{for each story: git merge feat/{story-slug}}

If merge conflicts occur, resolve before merging the next branch.
Then clean up sub-worktrees:

{for each story: git worktree remove .worktrees/{story-slug}}

Stories in this group:
{list of stories with IDs and names}
```
</multi_story>

<not_last_group_warning>
**{NOT_LAST_GROUP_WARNING}** — Include this text if the current group is NOT the last execution group. Omit entirely for the last group.

```
WARNING: [skill-name] will invoke finishing-a-development-branch
when done. It will detect "main" as the base branch (not the phase
branch). Choose Option 3 "Keep the branch as-is" — do NOT merge
or create a PR. More execution groups remain after this one.
```

Replace `[skill-name]` with `subagent-driven-development` (Option A / single story) or `executing-plans` (Option B).
</not_last_group_warning>

</state_3>

<state_4 title="Current group done, more groups remain">
**Check:** All stories in current group have commits. More groups exist in the phase plan.

**Output:**
```
Execution Group {G} complete ({completed-stories}).
Next group: Execution Group {G+1} ({next-stories}).

Re-invoke to plan the next group:

/charter-to-superpower {N}
```

This loops back to State 2 for the next execution group.
</state_4>

<state_5 title="All execution groups complete">
**Check:** All stories from all groups in the phase plan have been implemented.

**Output:**
```
All {total} stories implemented across {group-count} execution groups.
Finish the branch:

/superpowers:finishing-a-development-branch
```
</state_5>

<state_6 title="Branch finished">
**Check:** Branch merged or PR created (see `<detection_logic>`).

**Output:**
```
Phase {N} complete. Next phase:

/charter-to-superpower {N+1}
```
</state_6>

</process>

<detection_logic>

**Worktree detection:**
```bash
# Check both conventional locations
ls -d .worktrees/feat/phase-{N}-* 2>/dev/null
ls -d worktrees/feat/phase-{N}-* 2>/dev/null
# Also check git worktree list
git worktree list | grep "phase-{N}"
```

**Execution group parsing:**
Parse the phase plan's `## Parallelism Analysis` section. Match heading patterns:
```
### Execution Group N (description)     # standard format
### Parallel Group N (description)      # deprecated, backward compat
```
Regex: `### (?:Execution Group|Parallel Group) (\d+)`. Story list is bullet items below each heading.

If no Parallelism Analysis section or only 1 group: treat entire phase as a single execution group. Skip group cycling — go straight from plan → execute → finish.

**Plan file detection — content-based, NOT filename:**
writing-plans saves as `docs/plans/YYYY-MM-DD-<slug>.md` where slug is derived internally. Grep each plan file for ALL story IDs in the current group:
```bash
WORKTREE=$(git worktree list | grep "phase-{N}" | awk '{print $1}')
for plan in "$WORKTREE"/docs/plans/*.md; do
  # Check if plan contains ALL story IDs for this group
  if grep -q "US-001" "$plan" && grep -q "US-004" "$plan" && \
     grep -q "US-006" "$plan" && grep -q "US-013" "$plan"; then
    echo "Group plan: $plan"
  fi
done
```
Fallback: ask user which file in `docs/plans/` is the plan for the group.

**Group completion — git log:**
```bash
git -C "$WORKTREE" log --oneline | grep -c "US-{XXX}"
```
A group is complete when ALL its story IDs appear in commit messages. First incomplete group = current group.

Fallback: ask user `Has Execution Group {G} been completed? ({story-list})`

**Branch completion:**
```bash
gh pr list --head "feat/phase-{N}-*" --state all 2>/dev/null
git branch --merged main | grep "phase-{N}"
```
</detection_logic>

<edge_cases>
1. **Missing upstream artifacts:** Warn, don't block. The phase plan is self-contained for writing-plans.
2. **Wrong branch worktree:** Warn user, suggest switching or creating new worktree.
3. **Partially complete groups:** Find the first incomplete group (first where not all story IDs appear in git log).
4. **No Parallelism Analysis / single group:** Treat entire phase as one execution group. Skip cycling.
5. **Re-invoke after completing group:** State 4 triggers — advance to next group, output loops back to State 2.
6. **Option B merge needed:** After parallel execution, story branches must merge into the phase branch before next group can be planned.
7. **Deleted plan file:** Re-detect as State 2. writing-plans regenerates.
8. **Mid-execution re-invoke:** Cannot detect partial task completion. Ask: "Are you resuming execution or starting fresh?"
</edge_cases>

<anti_patterns>
- **Never suggest parallel subagents in same session.** subagent-driven-development prohibits this — it processes plans sequentially with per-session TodoWrite tracking.
- **Never match plan files by filename pattern.** Always use content-based detection (grep for story IDs).
- **Never plan all groups upfront.** Each group must be planned AFTER prior groups are implemented so writing-plans can reference real code.
</anti_patterns>

<success_criteria>
- Correct state detected for the given phase number
- Output contains the exact superpowers skill invocation with correct arguments
- Phase plan parsed correctly (name, groups, stories, UX inputs)
- Worktree path resolved correctly
- Plan file matched by content (story IDs), not filename
- WARNING included when current group is not the last
- Edge cases handled gracefully (ask user when detection is ambiguous)
</success_criteria>
