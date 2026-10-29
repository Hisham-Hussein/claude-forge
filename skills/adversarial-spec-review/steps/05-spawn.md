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
3. Post findings with severity (Critical/Major/Minor), per the SEVERITY CALIBRATION block from templates/reviewer-task.md, pasted into each teammate's prompt, and section citations
4. Challenge other teammates' findings when they disagree

Use Opus for each teammate. Require plan approval before they start reviewing.
```

The lead manages task creation, assignment, and synthesis. Teammates self-coordinate via the shared task list and messaging.

### Mode B: Parallel Subagents (FALLBACK)

**What it is:** Independent Agent tool invocations that run in isolation. Each agent reads files, does its review, and returns results to the orchestrator. Agents CANNOT see each other's work or communicate. Cross-challenge only happens in the orchestrator's synthesis step.

**When to use:** Only when Agent Teams is unavailable (feature not enabled, etc.). **You MUST tell the user** before using this mode: "Agent Teams isn't available in this environment. Falling back to parallel subagents — reviewers won't be able to cross-challenge each other directly. I'll handle cross-challenge in synthesis."

**How to use:**
1. Spawn all reviewers **in parallel** using the Agent tool.
   - Use `model: opus` for each reviewer
   - Each agent's prompt follows the agent_prompt_template from templates/reviewer-task.md with all dynamic fields filled
2. Wait for all agents to complete.

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
2. Spawn ONE agent using the Agent tool with `model: opus`.
3. The agent reviews through all lenses sequentially, performs a cross-lens pass, and returns consolidated findings.

**Key difference from Mode B:** Mode B spawns N independent agents in parallel — diversity of perspective catches blind spots through independent convergence. Mode C spawns 1 agent with N lenses combined — the solo reviewer sees connections across lenses that independent agents cannot, but may have blind spots that diversity would catch. The orchestrator compensates via mandatory spot-checking (see Step 6).
</step_5>

