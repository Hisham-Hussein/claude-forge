# Workflow: Analyze and Dispatch

Main workflow for distributing work across multiple agents.

<required_reading>
**Read these references NOW:**
1. references/context-handoff-patterns.md
2. references/agent-invocations.md
3. prompts/handoff-document.md
</required_reading>

<process>
## Step 1: Understand the Request

Analyze what the user wants to parallelize:
- How many independent tasks?
- What's the scope of each?
- Which agents are best suited?

If unclear, ask:
```
I'll help distribute this work. Can you clarify:
1. What are the independent pieces that can run in parallel?
2. Any dependencies between them?
3. Preferred agents (Claude Code, Gemini, Aider) or should I choose?
```

## Step 2: Decompose into Tasks

Break the work into independent units. Each task should:
- Be completable without waiting for other tasks
- Have clear boundaries (specific files/modules)
- Have testable success criteria

Example decomposition:
```
Original: "Build a user dashboard with analytics"

Tasks:
1. Backend API endpoints (Aider - focused file edits)
2. Data aggregation service (Claude Code - complex logic)
3. Frontend components (Claude Code - multi-file)
4. Documentation (Gemini - research and writing)
```

## Step 3: Initialize Session Tracking

Create the session directory and manifest:
```bash
mkdir -p .fork-sessions
```

If manifest doesn't exist, initialize it:
```bash
cat > .fork-sessions/manifest.json << 'EOF'
{
  "version": "1.0",
  "project": "PROJECT_NAME",
  "sessions": [],
  "last_updated": "TIMESTAMP",
  "settings": {
    "auto_cleanup_days": 7,
    "log_retention": true,
    "completion_markers": true
  }
}
EOF
```

## Step 4: Generate Session IDs

For each task, generate a unique session ID:
```bash
# Get next available ID
next_num=$(($(jq '.sessions | length' .fork-sessions/manifest.json 2>/dev/null || echo 0) + 1))
printf "fork-%03d" $next_num
```

## Step 5: Create Handoff Documents

For each task, create a handoff document using `prompts/handoff-document.md` template.

Fill in:
- Task description (specific and actionable)
- Background context (why this exists)
- Files to modify (explicit list)
- Constraints (what NOT to do)
- Success criteria (testable)
- If blocked instructions

Save to: `.fork-sessions/{session-id}-handoff.md`

## Step 6: Choose Agents

Based on task characteristics:

| Task Type | Best Agent |
|-----------|------------|
| Multi-file refactoring | Claude Code |
| Single-file focused edits | Aider |
| Research/exploration | Gemini CLI |
| Documentation | Gemini CLI or Claude Code |
| Complex logic/architecture | Claude Code |
| Quick scripts | CLI or Aider |

Respect variable settings:
- Check `enable_claude_code`, `enable_gemini_cli`, `enable_aider`
- If preferred agent disabled, suggest alternative

## Step 7: Spawn Sessions

For each task:

### Interactive Mode (default)
```bash
# Spawn new terminal with agent
gnome-terminal --working-directory="$PWD" -- bash -c '
  claude --prompt-file .fork-sessions/fork-001-handoff.md
  exec bash
' &
```

### Headless Mode (if `headless_mode: true`)
```bash
# Run in background, capture output
nohup claude --print --prompt-file .fork-sessions/fork-001-handoff.md \
  > .fork-sessions/fork-001.log 2>&1 &
echo $! > .fork-sessions/fork-001.pid
```

### Record in manifest
After each spawn, update manifest with session entry.

## Step 8: Report to User

Summarize what was spawned:

```
Forked 3 sessions:

| ID | Agent | Task | Mode |
|----|-------|------|------|
| fork-001 | Claude Code | Backend API endpoints | Interactive |
| fork-002 | Claude Code | Frontend components | Interactive |
| fork-003 | Gemini | Documentation | Headless |

To check status: "Check fork status" or view .fork-sessions/manifest.json
Handoff docs in: .fork-sessions/fork-*-handoff.md
```
</process>

<success_criteria>
This workflow is complete when:
- [ ] Tasks decomposed into independent units
- [ ] Session tracking initialized
- [ ] Handoff document created for each task
- [ ] Sessions spawned (terminals opened or background processes started)
- [ ] Manifest updated with all sessions
- [ ] User informed of session IDs and how to check status
</success_criteria>

<error_handling>
## Common Issues

**Terminal spawn fails:**
- Check if terminal emulator is available (gnome-terminal, iTerm2, etc.)
- Fall back to tmux: `tmux new-window -c "$PWD" 'claude ...'`

**Agent not installed:**
- Check if binary exists: `which claude` / `which gemini` / `which aider`
- Suggest installation or alternative agent

**Manifest locked:**
- Another process may be writing
- Retry with backoff or use file locking
</error_handling>
