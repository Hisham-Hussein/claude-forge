# Workflow: Check Status

Review and manage spawned sessions.

<required_reading>
**Read if needed:**
- references/session-tracking.md
</required_reading>

<process>
## Step 1: Load Manifest

Read the session manifest:
```bash
cat .fork-sessions/manifest.json
```

If manifest doesn't exist:
```
No active fork sessions found.
Run "fork work to agents" to spawn new sessions.
```

## Step 2: Check Process Status

For each session with status "running", verify the process is alive:

```bash
for session in $(jq -r '.sessions[] | select(.status == "running") | "\(.id):\(.pid)"' .fork-sessions/manifest.json); do
  id=$(echo $session | cut -d: -f1)
  pid=$(echo $session | cut -d: -f2)
  
  if ps -p $pid > /dev/null 2>&1; then
    echo "$id: running (PID $pid)"
  else
    echo "$id: stopped (PID $pid no longer exists)"
  fi
done
```

## Step 3: Check Completion Markers

Look for completion indicators:
```bash
for id in $(jq -r '.sessions[].id' .fork-sessions/manifest.json); do
  # Check for explicit completion marker
  if [ -f ".fork-sessions/$id-complete" ]; then
    echo "$id: completed (marker found)"
  fi
  
  # Check log for success indicators
  if grep -q "Task completed\|All tests passed\|Done" ".fork-sessions/$id.log" 2>/dev/null; then
    echo "$id: likely completed (success pattern in log)"
  fi
done
```

## Step 4: Update Manifest

Update status for sessions that have stopped:
```bash
# Mark stopped processes as completed or unknown
jq '
  .sessions |= map(
    if .status == "running" then
      # Would need actual PID check here
      .
    else
      .
    end
  )
' .fork-sessions/manifest.json > tmp && mv tmp .fork-sessions/manifest.json
```

## Step 5: Generate Report

Display summary to user:

```
## Fork Session Status

| ID | Agent | Task | Status | Duration |
|----|-------|------|--------|----------|
| fork-001 | Claude Code | Implement OAuth | ✅ completed | 45m |
| fork-002 | Gemini | Generate docs | 🔄 running | 12m |
| fork-003 | Aider | Fix login bug | ❌ failed | 8m |

### Details

**fork-001** (completed)
- Files modified: src/auth/google.ts, src/auth/index.ts
- Notes: All tests passing

**fork-002** (running)
- PID: 12456
- Log tail: [last 5 lines]

**fork-003** (failed)
- Exit code: 1
- Error: [from log]
```

## Step 6: Offer Actions

Based on status, offer relevant actions:

```
What would you like to do?

1. View full log for a session
2. Resume/retry a failed session
3. Kill a running session
4. Clean up completed sessions
```
</process>

<success_criteria>
- [ ] Manifest loaded
- [ ] Process status checked for running sessions
- [ ] Status report displayed
- [ ] Actions offered if relevant
</success_criteria>

<status_icons>
## Status Display

| Status | Icon | Meaning |
|--------|------|---------|
| running | 🔄 | Process active |
| completed | ✅ | Task finished successfully |
| failed | ❌ | Task failed |
| unknown | ❓ | Cannot determine status |
</status_icons>

<log_inspection>
## Log Inspection Commands

**View full log:**
```bash
cat .fork-sessions/fork-001.log
```

**View last 20 lines:**
```bash
tail -20 .fork-sessions/fork-001.log
```

**Watch live output:**
```bash
tail -f .fork-sessions/fork-001.log
```

**Search for errors:**
```bash
grep -i "error\|fail\|exception" .fork-sessions/fork-001.log
```
</log_inspection>

<session_actions>
## Session Management Actions

### Kill Running Session
```bash
kill $(cat .fork-sessions/fork-001.pid)
# Or
kill $PID
```

### Clean Up Completed Sessions
```bash
# Remove sessions older than 7 days
jq '.sessions |= map(select(.status != "completed" or (.completed_at | fromdateiso8601) > (now - 604800)))' \
  .fork-sessions/manifest.json > tmp && mv tmp .fork-sessions/manifest.json
```

### Retry Failed Session
```bash
# Re-run with same handoff
claude --prompt-file .fork-sessions/fork-001-handoff.md
```
</session_actions>
