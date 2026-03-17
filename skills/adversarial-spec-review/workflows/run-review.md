<required_reading>
**Read these reference files NOW before proceeding:**
1. references/reviewer-archetypes.md — reviewer catalog and selection process
2. references/synthesis-principles.md — cross-challenge rules and convergence criteria
3. templates/reviewer-task.md — dynamic template for spawning reviewers
</required_reading>

<process>

<step_1>
**Step 1: Read and Analyze the Spec**

Read the spec file completely. Then analyze it for domain dimensions:

1. **Extract section structure** — list all ## headings and their topics
2. **Identify referenced files** — find all file paths, module names, function names, interface names mentioned in the spec. These are the files reviewers must read.
3. **Scan for domain signals** — for each archetype in reviewer-archetypes.md, count how many selection signals appear in the spec
4. **Note the spec's scope** — is it a narrow change (1-2 sections of concern) or a broad design (5+ interacting systems)?

Output: a mental map of the spec's domain dimensions and which archetypes match.
</step_1>

<step_2>
**Step 2: Select the Review Team**

Apply the selection process from reviewer-archetypes.md:
- Select every archetype with 2+ signal matches
- Always include Devil's Advocate
- Do NOT cap at a fixed number — let the spec's complexity determine team size

**Announce the team to the user before proceeding:**
```
Based on the spec's domain dimensions, I'm spawning N reviewers:
- {Archetype 1} — {why: which signals matched, which sections they'll focus on}
- {Archetype 2} — {why}
- ...
- Devil's Advocate — mandatory, end-to-end flow tracing
```

Wait for user acknowledgment. The user may want to add or remove reviewers.
</step_2>

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

Each reviewer gets the spec + their domain-relevant files.
</step_3>

<step_4>
**Step 4: Generate Focus Areas per Reviewer**

For each reviewer, generate 3-7 specific QUESTIONS (not instructions) based on:
- The spec's section structure mapped to the reviewer's expertise
- The specific concerns that archetype is designed to catch
- The source files they'll be reading

Questions should be specific to THIS spec, not generic. Reference actual section numbers, field names, function names from the spec.

See templates/reviewer-task.md `<focus_area_generation>` for examples.
</step_4>

<step_5>
**Step 5: Create Shared Tasks and Spawn Agent Team**

**IMPORTANT: Use Claude Code Agent Teams (shared task list + inter-agent communication), NOT isolated subagents.** Agent Teams teammates share tasks, can claim work, and see each other's output — this is critical for cross-challenge. Reference: https://code.claude.com/docs/en/agent-teams

Setup:
1. For each reviewer, create a task via TaskCreate with the task description from the template. Note the task ID.
2. Create a synthesis task (blocked by all reviewer tasks via `addBlockedBy`).
3. Spawn all reviewers **in parallel** using the Agent tool — each as a teammate that claims their task from the shared task list.
   - Use `model: opus` for each reviewer
   - Each agent's prompt includes "You are a teammate on an agent team. Claim task #{task_id} from the shared task list and execute it."
   - Each agent's prompt follows the agent_prompt_template from templates/reviewer-task.md with all dynamic fields filled
4. Wait for all agents to complete.

The shared task list is the coordination mechanism — reviewers post findings as task updates, the synthesis task is unblocked when all reviews complete, and the orchestrator (lead) synthesizes.
</step_5>

<step_6>
**Step 6: Synthesize with Critical Judgment**

After all reviewers complete, apply synthesis-principles.md:

1. **Collect all findings** from task comments/agent results
2. **Cross-challenge:** check for independent convergence (2+ reviewers flagging same issue)
3. **Verify single-reviewer findings** — read the actual code to confirm or refute
4. **Apply severity calibration** — re-rank each finding honestly
5. **Drop noise** — remove implementation details, manufactured severity, nitpicks
6. **Check for fix regressions** (round 2+) — did prior fixes create new problems?

Produce the final issues list using the presentation format from synthesis-principles.md.
</step_6>

<step_7>
**Step 7: Present to User and Get Decision**

Present the round results to the user. End with one of:

**If Critical/Major issues found:**
```
Round N found X Critical, Y Major issues. Want me to apply fixes?
```

**If zero Critical/Major:**
```
Spec is implementation-ready. N rounds, M total reviewer passes, all converged on zero Critical/Major.
```

Wait for user response:
- "Apply fixes" → proceed to Step 8
- "Stop" or "good enough" → end
- User disagrees with findings → discuss, adjust, re-present
</step_7>

<step_8>
**Step 8: Apply Fixes**

For each approved Critical/Major issue:
1. Read the spec section that needs editing
2. Apply the fix using Edit tool
3. Verify the edit is clean and consistent with surrounding text

After all fixes applied, summarize what changed.

Then **automatically proceed to the next round** (back to Step 5) with updated round context:
- Increment round number
- Set round_context to list all fixes applied
- Set round_specific_instructions to "Don't re-report fixed issues. Focus on what's STILL broken or what the fixes INTRODUCED."
- Re-select reviewers if needed (same team is fine if spec scope hasn't changed)
</step_8>

<step_9>
**Step 9: Safety Valve**

If round number reaches 5 and there are still Critical/Major issues:

Stop the loop and tell the user:
```
After 5 rounds we're still finding Critical/Major issues. The spec may need a structural rethink, not just iterative fixes.

Still open:
- [list remaining issues]

Recommendation: [restructure section X / reconsider approach Y / split spec into Z]
```

</step_9>

</process>

<success_criteria>
This workflow is complete when:
- [ ] Spec analyzed and domain dimensions identified
- [ ] Review team selected based on spec content (not defaults)
- [ ] All reviewers read real source files, not just the spec
- [ ] Each round synthesized with critical judgment (not rubber-stamped)
- [ ] User approved all fixes before they were applied
- [ ] Final round: all reviewers found zero Critical/Major
- [ ] Orchestrator confirmed the verdict with own judgment
- [ ] User received "implementation-ready" declaration
</success_criteria>
