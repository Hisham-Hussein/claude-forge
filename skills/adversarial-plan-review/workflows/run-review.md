<process>

Copy this checklist and track progress as you go:

```
Review Progress:
- [ ] Step 1: Read and analyze the plan (scope dimensions, source spec, referenced files)
- [ ] Step 2: Select the review team (announce to user, get acknowledgment)
- [ ] Step 3: Identify files for reviewers (plan + spec + source + types + tests)
- [ ] Step 4: Generate focus areas per reviewer (specific questions, not instructions)
- [ ] Step 5: Ask user for mode (Agent Teams vs Parallel Subagents), then spawn reviewers
- [ ] Step 6: Synthesize with critical judgment (cross-challenge, severity calibration)
- [ ] Step 7: Present to user and get decision
- [ ] Step 8: Apply fixes (if approved) → loop back to Step 5
- [ ] Step 9: Safety valve (if round 5 reached with open Critical/Major)
```

<step_1>
**Step 1: Read and Analyze the Plan**

Read the plan file completely. Then analyze it for scope dimensions:

1. **Extract plan structure** — count tasks, identify phases, note dependencies between tasks
2. **Find the source spec** — the plan should reference its source design document. Read it. If not referenced, ask the user which spec this plan implements.
3. **Identify referenced files** — find all file paths (Create, Modify, Test), module names, function names, interface names mentioned in the plan. These are the files reviewers must read.
4. **Scan for scope signals** — for each archetype in reviewer-archetypes.md, count how many selection signals appear in the plan
5. **Note the plan's complexity** — task count, phase count, number of files touched, number of new vs modified files

Output: a mental map of the plan's scope dimensions and which archetypes match.
</step_1>

<step_2>
**Step 2: Select the Review Team**

**Read `references/reviewer-archetypes.md` now** — it contains the archetype catalog and selection process.

Apply the selection process from reviewer-archetypes.md:
- Select every archetype with 2+ signal matches
- Always include Devil's Advocate
- Do NOT cap at a fixed number — let the plan's complexity determine team size

**Announce the team to the user before proceeding:**
```
Based on the plan's scope, I'm spawning N reviewers:
- {Archetype 1} — {why: which signals matched, which tasks they'll focus on}
- {Archetype 2} — {why}
- ...
- Devil's Advocate — mandatory, end-to-end execution walkthrough
```

Wait for user acknowledgment. The user may want to add or remove reviewers.
</step_2>

<step_3>
**Step 3: Identify Files for Reviewers**

For each reviewer, determine which files they must read:

1. **Always include the plan itself**
2. **Always include the source spec** — the plan is an implementation of a spec. Reviewers need both.
3. **Source files referenced in the plan** — any file path mentioned in Create/Modify/Test lines
4. **Existing source files the plan modifies** — read the current version to verify the plan's assumptions about what exists
5. **Type definitions and interfaces** — if the plan creates or imports types
6. **Test files** — existing tests that the plan extends or that test code the plan modifies
7. **Entry points** — server.ts, main files, where new modules get wired in

Use Glob and Grep to find files by name/pattern if needed. Don't guess paths — verify they exist.

Each reviewer gets the plan + spec + their domain-relevant files.
</step_3>

<step_4>
**Step 4: Generate Focus Areas per Reviewer**

**Read `templates/reviewer-task.md` now** — it contains the prompt template, dynamic fields, and focus area generation guidance.

For each reviewer, generate 3-7 specific QUESTIONS (not instructions) based on:
- The plan's task structure mapped to the reviewer's expertise
- The specific concerns that archetype is designed to catch
- The source files they'll be reading

Questions should be specific to THIS plan, not generic. Reference actual task numbers, file paths, function names from the plan.

**Self-check before proceeding:** For each focus area question, verify: (a) it references a specific task number or file path from the plan, (b) it asks the reviewer to TRACE or VERIFY something concrete, not just "check if X is correct." Rewrite any question that fails this test.
</step_4>

<step_5>
**Step 5: Spawn Reviewers**

**MANDATORY: Ask the user which mode they want BEFORE spawning in Round 1.** Present both options clearly and wait for their choice. For subsequent rounds, confirm briefly: "Continuing with Mode [A/B] — OK, or want to switch?" Example for Round 1:

```
Before I spawn the reviewers, which mode do you want?

**Mode A: Agent Teams** (preferred) — Teammates share a task list, message each other,
and challenge findings in real-time. Requires Agent Teams feature enabled in CLI.

**Mode B: Parallel Subagents** (fallback) — Independent agents that report back to me.
No inter-agent communication. I handle cross-challenge in synthesis.
```

Two modes are available. They are fundamentally different — do NOT confuse them.

### Mode A: Agent Teams (PREFERRED)

**What it is:** Claude Code Agent Teams — a specific experimental feature where teammates are separate Claude Code sessions that share a task list, have a mailbox for inter-agent messaging, and can see each other's work. Teammates can challenge each other's findings in real-time. This is the best mode for adversarial review because cross-challenge happens DURING the review, not just in synthesis.

**Requirement:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` must be set in settings.json or environment.

**Reference:** https://code.claude.com/docs/en/agent-teams

**How to use:** Tell Claude (the lead) in natural language to create an agent team. Example:

```
Create an agent team with {N} teammates for adversarial plan review:
- Teammate 1: {archetype_name} — {focus description}
- Teammate 2: {archetype_name} — {focus description}
- ...

Each teammate should:
1. Read the plan at {plan_path}
2. Read the source spec at {spec_path}
3. Read their assigned source files
4. Post findings with severity (Critical/Major/Minor) and task/step citations
5. Challenge other teammates' findings when they disagree

Use Opus for each teammate. Require plan approval before they start reviewing.
```

The lead manages task creation, assignment, and synthesis. Teammates self-coordinate via the shared task list and messaging.

### Mode B: Parallel Subagents (FALLBACK)

**What it is:** Independent Agent tool invocations that run in isolation. Each agent reads files, does its review, and returns results to the orchestrator. Agents CANNOT see each other's work or communicate. Cross-challenge only happens in the orchestrator's synthesis step.

**When to use:** Only when Agent Teams is unavailable (feature not enabled, etc.). **You MUST tell the user** before using this mode: "Agent Teams isn't available in this environment. Falling back to parallel subagents — reviewers won't be able to cross-challenge each other directly. I'll handle cross-challenge in synthesis."

**How to use:**
1. For each reviewer, create a task via TaskCreate with the task description from the template. Note the task ID.
2. Create a synthesis task (blocked by all reviewer tasks via `addBlockedBy`).
3. Spawn all reviewers **in parallel** using the Agent tool.
   - Use `model: opus` for each reviewer
   - Each agent's prompt follows the agent_prompt_template from templates/reviewer-task.md with all dynamic fields filled
4. Wait for all agents to complete.

**CRITICAL:** Do NOT use Mode B's mechanics (Agent tool) while claiming to use Mode A (Agent Teams). They are completely different features. If you find yourself typing `Agent tool` invocations, you are in Mode B.
</step_5>

<step_6>
**Step 6: Synthesize with Critical Judgment**

**Read `references/synthesis-principles.md` now** — it contains cross-challenge rules, severity calibration, and convergence criteria.

After all reviewers complete, apply synthesis-principles.md:

1. **Collect all findings** from task comments/agent results
2. **Cross-challenge:** check for independent convergence (2+ reviewers flagging same issue)
3. **Verify single-reviewer findings** — read the actual spec and code to confirm or refute
4. **Apply severity calibration** — re-rank each finding honestly
5. **Drop noise** — remove style preferences, manufactured severity, implementation details the developer would handle
6. **Check for fix regressions** (round 2+) — did prior fixes create new problems?
7. **Judge spec coverage** — holistically, does this plan fully implement the spec?

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
Plan is execution-ready. N rounds, M total reviewer passes, all converged on zero Critical/Major.
```

Wait for user response:
- "Apply fixes" → proceed to Step 8
- "Stop" or "good enough" → end
- User disagrees with findings → discuss, adjust, re-present
</step_7>

<step_8>
**Step 8: Apply Fixes**

For each approved Critical/Major issue:
1. Read the plan section that needs editing
2. Apply the fix using Edit tool
3. Verify the edit is clean and consistent with surrounding text

After all fixes applied:
4. Summarize what changed (list each fix briefly)
5. **Commit the round's fixes** as a single commit with message format:
   `docs: fix N Critical + M Major issues from adversarial review (round R)`
   Include a body listing each fix for traceability. One commit per round — not per fix — because fixes within a round are semantically coupled and may touch overlapping sections.

**MANDATORY: Do NOT auto-start the next round.** Present the fix summary to the user and ask:
```
Round R fixes applied and committed. Ready to start Round R+1, or do you want to stop here?
```
Wait for explicit user confirmation before proceeding. Only after the user confirms, proceed to Step 5 with updated round context:
- Increment round number
- Set round_context to list all fixes applied
- Set round_specific_instructions to "Don't re-report fixed issues. Focus on what's STILL broken or what the fixes INTRODUCED."
- Re-select reviewers if needed (same team is fine if plan scope hasn't changed)
</step_8>

<step_9>
**Step 9: Safety Valve**

If round number reaches 5 and there are still Critical/Major issues:

Stop the loop and tell the user:
```
After 5 rounds we're still finding Critical/Major issues. The plan may need a structural rethink, not just iterative fixes.

Still open:
- [list remaining issues]

Recommendation: [restructure task ordering / revisit spec interpretation / split plan into phases]
```

</step_9>

</process>

<success_criteria>
This workflow is complete when:
- [ ] Plan analyzed and scope dimensions identified
- [ ] Source spec located and read
- [ ] Review team selected based on plan content (not defaults)
- [ ] All reviewers read the plan, spec, AND real source files
- [ ] Each round synthesized with critical judgment (not rubber-stamped)
- [ ] User approved all fixes before they were applied
- [ ] Final round: all reviewers found zero Critical/Major
- [ ] Orchestrator confirmed the verdict with own judgment
- [ ] User received "execution-ready" declaration
</success_criteria>
