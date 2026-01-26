---
name: fork-terminal
description: Use when distributing independent tasks across multiple AI coding assistants in parallel. Triggers include "fork this work", "spawn agents", "run in parallel", "distribute tasks", or when multiple independent tasks would benefit from concurrent execution.
---

<variables>
enable_claude_code: true
enable_gemini_cli: true
enable_aider: true
default_agent: claude
session_tracking: true
headless_mode: false
</variables>

<essential_principles>

## How Fork-Terminal Works

This skill spawns independent terminal sessions with structured context handoffs. Each spawned session receives a handoff document containing task, context, and constraints.

### 1. Handoff Documents Are Critical

Never spawn a terminal without a proper handoff document. Raw commands work for CLI tools, but agentic tools need structured context:

- What task to complete
- What files/code to focus on
- What constraints apply
- What success looks like

### 2. Track What You Spawn

Every spawned session gets logged to a manifest file. This enables:

- Status checks across all spawned work
- Resumption if sessions fail
- Coordination between parallel tasks

### 3. Match Tool to Task

| Task Type | Best Tool |
|-----------|-----------|
| Code generation, refactoring | Claude Code, Aider |
| Research, exploration | Gemini CLI |
| Quick scripts, one-liners | Raw CLI |
| Complex multi-file changes | Claude Code |

### 4. Interactive vs Headless

- **Interactive**: User takes over the terminal (default for complex tasks)
- **Headless**: Agent runs autonomously, output captured (for batch work)

Set `headless_mode: true` in variables for autonomous execution.
</essential_principles>

<intake>
What would you like to do?

1. **Fork work to agents** - Distribute tasks across Claude Code, Gemini, or Aider
2. **Run CLI command** - Spawn a raw terminal command
3. **Check status** - See status of spawned sessions
4. **Custom dispatch** - Specify exactly what to spawn and how

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow | Notes |
|----------|----------|-------|
| 1, "fork", "spawn agents", "distribute", "parallelize" | `workflows/analyze-and-dispatch.md` | Main workflow - analyzes task, creates handoffs |
| 2, "CLI", "command", "terminal", "run" | `workflows/spawn-cli-command.md` | Simple command dispatch |
| 3, "status", "check", "progress", "sessions" | `workflows/check-status.md` | Review spawned work |
| 4, "custom", "specific" | `workflows/spawn-agent.md` | Direct agent dispatch |

**Variable-based routing:**

- If user requests Claude Code AND `enable_claude_code` is false → Suggest alternative
- If user requests Gemini AND `enable_gemini_cli` is false → Suggest alternative
- If user requests Aider AND `enable_aider` is false → Suggest alternative

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>

## Domain Knowledge

All in `references/`:

**Agent Patterns:** agent-invocations.md (how to invoke each tool)
**Handoff Design:** context-handoff-patterns.md (structuring handoffs)
**Session Management:** session-tracking.md (tracking spawned work)
</reference_index>

<workflows_index>

## Workflows

| Workflow | Purpose |
|----------|---------|
| analyze-and-dispatch.md | Main flow: analyze task → create handoffs → spawn agents |
| spawn-cli-command.md | Dispatch raw CLI commands |
| spawn-agent.md | Direct agent dispatch with full control |
| check-status.md | Review and manage spawned sessions |
</workflows_index>

<prompts_index>

## Meta-Prompts

| Prompt | Purpose |
|--------|---------|
| handoff-document.md | Structured context for agent-to-agent handoff |
</prompts_index>

<templates_index>

## Templates

| Template | Purpose |
|----------|---------|
| session-manifest.md | Track all spawned sessions |
</templates_index>

<quick_start>

## Quick Start

**Fork work to Claude Code:**

```
User: "Fork this to Claude Code - implement the login form in src/components/"
```

**Parallel dispatch:**

```
User: "Spawn 3 agents - one for frontend, one for API, one for tests"
```

**Check progress:**

```
User: "Check status of spawned sessions"
```

</quick_start>

<success_criteria>
A successful fork-terminal invocation:

- Creates structured handoff document for each spawned agent
- Logs session to manifest for tracking
- Launches appropriate tool (CLI or agent) in new terminal
- Returns confirmation with session ID and how to check status
</success_criteria>
