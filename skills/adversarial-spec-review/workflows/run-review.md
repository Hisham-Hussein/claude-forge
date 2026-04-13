<process>

Copy this checklist and track progress as you go:

```
Review Progress:
- [ ] Step 1: Read and analyze the spec (domain dimensions, referenced files)
- [ ] Step 2: Select the review team (announce to user, get acknowledgment)
- [ ] Step 3: Identify files for reviewers (spec + source + config + types + tests)
- [ ] Step 4: Generate focus areas per reviewer (specific questions, not instructions)
- [ ] Step 5: Ask user for mode (Agent Teams vs Parallel Subagents vs Solo Reviewer), then spawn reviewers
- [ ] Step 6: Synthesize with critical judgment (cross-challenge, severity calibration)
- [ ] Step 7: Present to user and get decision
- [ ] Step 8a: Apply fixes with impact tracing
- [ ] Step 8b: Verify fixes (self-review gate — catch regressions before next round)
- [ ] Step 8c: Commit and ask about next round → loop back to Step 5
- [ ] Step 9: Safety valve (if round 5 reached with open Critical/Major)
```

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

**Read `references/reviewer-archetypes.md` now** — it contains the archetype catalog and selection process.

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

**Mode C adaptation:** If the user chooses Mode C (Solo Reviewer) in Step 5, adapt the announcement: instead of "spawning N reviewers," say "the solo reviewer will cover N lenses" and list the same archetypes as combined lenses. The user can still add or remove lenses.
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

**Read `templates/reviewer-task.md` now** — it contains the prompt template, dynamic fields, and focus area generation guidance.

For each reviewer, generate 3-7 specific QUESTIONS (not instructions) based on:
- The spec's section structure mapped to the reviewer's expertise
- The specific concerns that archetype is designed to catch
- The source files they'll be reading

Questions should be specific to THIS spec, not generic. Reference actual section numbers, field names, function names from the spec.

See templates/reviewer-task.md `<focus_area_generation>` for examples.

**Self-check before proceeding:** For each focus area question, verify: (a) it references a specific section number or field name from the spec, (b) it asks the reviewer to TRACE or VERIFY something concrete, not just "check if X is correct." Rewrite any question that fails this test.

**Round 2+ focus area rules:** In subsequent rounds, focus areas MUST narrow, not deepen. Generate questions ONLY from these three categories:
1. **Fix verification** — "Did the fix for [prior finding] resolve the concern? Did it introduce any inconsistency with [related section]?"
2. **Regression check** — "Is [section that was clean in Round N-1] still consistent after the fixes?"
3. **Fix-adjacent gaps** — "Did fixing [X] reveal a gap in [Y] that was hidden by the original error?"

Do NOT generate "go deeper" questions, "find what Round N missed" questions, or questions that expand scope beyond Round 1's coverage. Round 2+ is convergence, not discovery. If the spec was clean in an area during Round 1, it's still clean — don't re-investigate it with deeper scrutiny.
</step_4>

<step_5>
**Step 5: Spawn Reviewers**

**MANDATORY: Ask the user which mode they want BEFORE spawning in Round 1.** Present all options clearly and wait for their choice. For subsequent rounds, confirm briefly: "Continuing with Mode [A/B/C] — OK, or want to switch?" Example for Round 1:

```
Before I spawn the reviewers, which mode do you want?

**Mode A: Agent Teams** (preferred) — Teammates share a task list, message each other,
and challenge findings in real-time. Requires Agent Teams feature enabled in CLI.

**Mode B: Parallel Subagents** (fallback) — Independent agents that report back to me.
No inter-agent communication. I handle cross-challenge in synthesis.

**Mode C: Solo Reviewer** (lightweight) — One agent reviews through all lenses in a single
comprehensive pass. Best for small-medium specs, quick validation, or budget-conscious
reviews. Same rigor, single agent.
```

Three modes are available. They are fundamentally different — do NOT confuse them.

### Mode A: Agent Teams (PREFERRED)

**What it is:** Claude Code Agent Teams — a specific experimental feature where teammates are separate Claude Code sessions that share a task list, have a mailbox for inter-agent messaging, and can see each other's work. Teammates can challenge each other's findings in real-time. This is the best mode for adversarial review because cross-challenge happens DURING the review, not just in synthesis.

**Requirement:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` must be set in settings.json or environment.

**Reference:** https://code.claude.com/docs/en/agent-teams

**How to use:** Tell Claude (the lead) in natural language to create an agent team. Example:

```
Create an agent team with {N} teammates for adversarial spec review:
- Teammate 1: {archetype_name} — {focus description}
- Teammate 2: {archetype_name} — {focus description}
- ...

Each teammate should:
1. Read the spec at {spec_path}
2. Read their assigned source files
3. Post findings with severity (Critical/Major/Minor) and section citations
4. Challenge other teammates' findings when they disagree

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

### Mode C: Solo Reviewer (LIGHTWEIGHT)

**What it is:** A single Agent tool invocation that reviews through ALL selected archetype lenses in one pass. The solo agent receives a combined prompt with all focus areas organized by lens. This mode uses fewer tokens and API calls than Mode A or B while maintaining the same severity calibration and engineering standards.

**When to use:**
- Small-to-medium specs (under ~5 major sections)
- Quick validation passes (e.g., verifying fixes from a prior Mode A/B round)
- Budget-conscious reviews where spawning 3-5 agents is not justified
- When the user explicitly requests it

**When NOT to use (warn the user):**
- Large, complex specs where blind spots from a single pass are likely
- Specs touching 5+ distinct subsystems (reviewer fatigue degrades quality)
- When the user has previously done Mode A/B and wants comparable depth

**How to use:**
1. Combine all selected archetypes' focus areas into a single prompt following the `solo_agent_prompt_template` from templates/reviewer-task.md. Keep focus areas to the top 3-4 questions per lens (not the full 3-7) to manage total prompt length.
2. Create one task via TaskCreate: "R{round}: Solo Comprehensive Review"
3. Spawn ONE agent using the Agent tool with `model: opus`.
4. The agent reviews through all lenses sequentially, performs a cross-lens pass, and returns consolidated findings.

**Key difference from Mode B:** Mode B spawns N independent agents in parallel — diversity of perspective catches blind spots through independent convergence. Mode C spawns 1 agent with N lenses combined — the solo reviewer sees connections across lenses that independent agents cannot, but may have blind spots that diversity would catch. The orchestrator compensates via mandatory spot-checking (see Step 6).
</step_5>

<step_6>
**Step 6: Synthesize with Critical Judgment**

**Read `references/synthesis-principles.md` now** — it contains cross-challenge rules, severity calibration, and convergence criteria.

After all reviewers complete, apply synthesis-principles.md:

1. **Collect all findings** from task comments/agent results
2. **Cross-challenge:** check for independent convergence (2+ reviewers flagging same issue)
3. **Verify single-reviewer findings** — read the actual code to confirm or refute
4. **Apply severity calibration** — re-rank each finding honestly
5. **Drop noise** — remove implementation details, manufactured severity, nitpicks
6. **Check for fix regressions** (round 2+) — did prior fixes create new problems?

Produce the final issues list using the presentation format from synthesis-principles.md.

**Mode C adaptation:** When the round used Mode C (Solo Reviewer), synthesis changes:
- Skip the cross-challenge step (there is only one reviewer) — instead, examine the reviewer's "Cross-Lens Observations" section for convergence signals (same issue surfacing under multiple lenses)
- Every Critical and Major finding requires orchestrator verification against the actual codebase (this is Rule 2 applied universally, since all findings are single-reviewer findings)
- The orchestrator MUST spot-check the top 3 riskiest areas identified in Step 1 to verify the solo reviewer didn't miss anything — if the orchestrator finds issues the solo reviewer missed, those become orchestrator-originated findings and the round is NOT converged
- All other synthesis rules (severity calibration, noise dropping, fix regression checking, holistic goal achievement judgment) apply unchanged
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
- "Apply fixes" → proceed to Step 8a
- "Stop" or "good enough" → end
- User disagrees with findings → discuss, adjust, re-present
</step_7>

<step_8a>
**Step 8a: Apply Fixes with Impact Tracing**

For each approved Critical/Major issue, BEFORE editing:

1. **Trace impact radius.** Search the spec (using Grep) for every reference to the entity being changed — field names, table names, state names, relationship names. List them. These are the locations you must check after editing.
2. **Read the target section** — read the actual file content around the edit point.
3. **Apply the fix** using the Edit tool.
4. **Immediately check impact locations** — revisit each reference found in step 1. Update any that are now stale or inconsistent.

The purpose of the impact trace is to make cascading updates part of the fix, not an afterthought discovered in the next review round.
</step_8a>

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

<step_8c>
**Step 8c: Commit and Loop**

After verification passes:

1. Summarize what changed (list each fix briefly)
2. **Commit the round's fixes** as a single commit with message format:
   `docs: fix N Critical + M Major findings from adversarial review round R`
   Include a body listing each fix for traceability. One commit per round — not per fix — because fixes within a round are semantically coupled and may touch overlapping sections.

**MANDATORY: Do NOT auto-start the next round.** Present the fix summary to the user and ask:
```
Round R fixes applied, verified, and committed. Ready to start Round R+1, or do you want to stop here?
```
Wait for explicit user confirmation before proceeding. Only after the user confirms, proceed to Step 5 with updated round context:
- Increment round number
- Set round_context to list all fixes applied
- Set round_specific_instructions — use the convergence-mode text from templates/reviewer-task.md (NOT the Round 1 text)
- Re-select reviewers if needed (same team is fine if spec scope hasn't changed)

**CRITICAL — Anti-escalation rule for Round N+1 prompts:**
- NEVER tell reviewers to "go deeper", "find what was missed", "expand scope", or "look harder"
- Round N+1 focus areas must be NARROWER than Round N — fix verification and regression checks only (see Step 4 Round 2+ rules)
- Consider switching to Mode C (Solo Reviewer) for Round 2+ — convergence rounds don't need the diversity of 5 parallel agents; a single focused pass verifying fixes is more cost-effective and less prone to scope creep
- The orchestrator's Round N+1 prompt must include: "This is a convergence round. Your job is to verify fixes are clean and confirm readiness. Zero findings is the expected outcome if the fixes are correct. Do NOT expand scope."
</step_8c>

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
- [ ] All fixes verified by orchestrator before committing (fix-to-finding, consistency scan, re-read)
- [ ] Final round: all reviewers found zero Critical/Major
- [ ] Orchestrator confirmed the verdict with own judgment
- [ ] User received "implementation-ready" declaration
</success_criteria>
