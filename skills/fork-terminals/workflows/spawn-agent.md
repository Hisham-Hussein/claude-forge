# Workflow: Spawn Agent

Direct agent dispatch with explicit control over agent type and configuration.

<required_reading>
**Read these references NOW:**
1. references/agent-invocations.md
2. references/context-handoff-patterns.md
3. prompts/handoff-document.md
</required_reading>

<process>
## Step 1: Identify Agent

If not specified, ask:
```
Which agent should I spawn?

1. **Claude Code** - Best for multi-file changes, complex refactoring
2. **Gemini CLI** - Best for research, exploration, documentation
3. **Aider** - Best for focused single-file edits, quick iterations
```

Check variable toggles:
- `enable_claude_code`: If false and Claude requested, suggest alternative
- `enable_gemini_cli`: If false and Gemini requested, suggest alternative
- `enable_aider`: If false and Aider requested, suggest alternative

## Step 2: Get Task Description

If not provided:
```
What task should this agent work on?
```

Task should be:
- Specific (not "work on the code")
- Scoped (mention specific files/modules)
- Actionable (clear deliverable)

## Step 3: Determine Mode

Check `headless_mode` variable or ask:
```
How should this agent run?

1. **Interactive** (Recommended) - Opens terminal, you take over
2. **Headless** - Runs autonomously, logs output
```

## Step 4: Create Handoff Document

Use the handoff template from `prompts/handoff-document.md`.

At minimum, include:
- Task description
- Files to focus on
- Success criteria

Save to: `.fork-sessions/{session-id}-handoff.md`

## Step 5: Generate Spawn Command

### Claude Code
```bash
# Interactive
gnome-terminal --working-directory="$PWD" -- bash -c '
  claude --prompt-file .fork-sessions/SESSION_ID-handoff.md
  exec bash
' &

# Headless
nohup claude --print --prompt-file .fork-sessions/SESSION_ID-handoff.md \
  > .fork-sessions/SESSION_ID.log 2>&1 &
```

### Gemini CLI
```bash
# Interactive
gnome-terminal --working-directory="$PWD" -- bash -c '
  gemini --prompt "$(cat .fork-sessions/SESSION_ID-handoff.md)"
  exec bash
' &

# Headless
nohup gemini --no-interactive --prompt "$(cat .fork-sessions/SESSION_ID-handoff.md)" \
  > .fork-sessions/SESSION_ID.log 2>&1 &
```

### Aider
```bash
# Get files from handoff
FILES=$(grep -A100 "Files to modify" .fork-sessions/SESSION_ID-handoff.md | grep "^- " | sed 's/^- //' | tr '\n' ' ')

# Interactive
gnome-terminal --working-directory="$PWD" -- bash -c '
  aider --message "$(cat .fork-sessions/SESSION_ID-handoff.md)" $FILES
  exec bash
' &

# Headless
nohup aider --yes --message "$(cat .fork-sessions/SESSION_ID-handoff.md)" $FILES \
  > .fork-sessions/SESSION_ID.log 2>&1 &
```

## Step 6: Execute Spawn

Run the appropriate command for the chosen agent and mode.

Capture PID for tracking:
```bash
PID=$!
```

## Step 7: Update Manifest

```bash
jq --arg id "$SESSION_ID" \
   --arg agent "AGENT" \
   --arg task "TASK_SUMMARY" \
   --arg mode "MODE" \
   --arg pid "$PID" \
   --arg handoff ".fork-sessions/$SESSION_ID-handoff.md" \
   '.sessions += [{
     id: $id,
     agent: $agent,
     mode: $mode,
     task_summary: $task,
     status: "running",
     spawned_at: (now | todate),
     working_dir: "'"$PWD"'",
     handoff_file: $handoff,
     log_file: ".fork-sessions/'"$SESSION_ID"'.log",
     pid: ($pid | tonumber),
     parent_session: "root"
   }] | .last_updated = (now | todate)' \
   .fork-sessions/manifest.json > tmp && mv tmp .fork-sessions/manifest.json
```

## Step 8: Report

```
Spawned AGENT session.

Session ID: SESSION_ID
Agent: AGENT
Mode: MODE
Task: TASK_SUMMARY

Handoff: .fork-sessions/SESSION_ID-handoff.md
Log: .fork-sessions/SESSION_ID.log

To check status: "Check fork status"
```
</process>

<success_criteria>
- [ ] Agent selected and available
- [ ] Handoff document created
- [ ] Terminal spawned with agent
- [ ] Session recorded in manifest
- [ ] User informed of session details
</success_criteria>

<agent_comparison>
## Quick Agent Selection Guide

| Need | Agent | Why |
|------|-------|-----|
| Explore unfamiliar codebase | Gemini | Strong at research |
| Refactor across many files | Claude Code | Coordinates complex changes |
| Quick fix in one file | Aider | Fast, focused |
| Write documentation | Gemini or Claude | Both excel here |
| Implement new feature | Claude Code | Best planning |
| Debug tricky issue | Claude Code | Strong reasoning |
</agent_comparison>
