# Workflow: Spawn CLI Command

Simple workflow for running a raw CLI command in a new terminal.

<required_reading>
**Read this reference if spawning in a new terminal:**
- references/agent-invocations.md (terminal spawning section)
</required_reading>

<process>
## Step 1: Get the Command

If user hasn't specified the command, ask:
```
What command should I run in the new terminal?
```

## Step 2: Determine Mode

Ask or infer:
- **Foreground**: User watches output, terminal stays open
- **Background**: Command runs detached, output logged

Default to foreground unless user says "background" or "in the background".

## Step 3: Prepare Session Tracking

Generate session ID and create minimal manifest entry:

```bash
mkdir -p .fork-sessions
SESSION_ID="fork-$(printf '%03d' $(($(jq '.sessions | length' .fork-sessions/manifest.json 2>/dev/null || echo 0) + 1)))"
```

## Step 4: Spawn Terminal

### Foreground (Interactive)
```bash
# Linux (GNOME)
gnome-terminal --working-directory="$PWD" -- bash -c '
  echo "Running: COMMAND"
  COMMAND
  echo ""
  echo "Command completed. Press Enter to close."
  read
' &

# Linux (tmux)
tmux new-window -c "$PWD" -n "$SESSION_ID" 'COMMAND; read -p "Done. Press Enter."'

# macOS (Terminal.app)
osascript -e 'tell application "Terminal" to do script "cd \"$PWD\" && COMMAND"'
```

### Background (Detached)
```bash
nohup bash -c 'COMMAND' > .fork-sessions/$SESSION_ID.log 2>&1 &
echo $! > .fork-sessions/$SESSION_ID.pid
```

## Step 5: Update Manifest

Add session entry:
```bash
jq --arg id "$SESSION_ID" \
   --arg cmd "COMMAND" \
   --arg pid "PID" \
   '.sessions += [{
     id: $id,
     agent: "cli",
     task_summary: $cmd,
     status: "running",
     spawned_at: (now | todate),
     working_dir: "'"$PWD"'",
     pid: ($pid | tonumber)
   }] | .last_updated = (now | todate)' \
   .fork-sessions/manifest.json > tmp && mv tmp .fork-sessions/manifest.json
```

## Step 6: Report

```
Spawned CLI command in new terminal.

Session: SESSION_ID
Command: COMMAND
Mode: foreground/background
Log: .fork-sessions/SESSION_ID.log (if background)

To check status: "Check fork status"
```
</process>

<success_criteria>
- [ ] Command identified
- [ ] Terminal spawned with command
- [ ] Session recorded in manifest
- [ ] User informed of session ID
</success_criteria>

<quick_commands>
## Quick Reference: Terminal Commands

| Platform | Command |
|----------|---------|
| Linux (GNOME) | `gnome-terminal -- bash -c 'CMD'` |
| Linux (tmux) | `tmux new-window 'CMD'` |
| macOS | `osascript -e 'tell application "Terminal" to do script "CMD"'` |
| WSL | `cmd.exe /c start wt.exe -- wsl bash -c 'CMD'` |
</quick_commands>
