# Session Tracking

How to track and manage spawned terminal sessions.

<manifest_system>
## Session Manifest

All spawned sessions are logged to `.fork-sessions/manifest.json`:

```json
{
  "sessions": [
    {
      "id": "fork-001",
      "agent": "claude",
      "task_summary": "Implement OAuth2 login",
      "status": "running",
      "spawned_at": "2025-01-18T10:30:00Z",
      "working_dir": "/home/user/project",
      "handoff_file": ".fork-sessions/fork-001-handoff.md",
      "mode": "interactive",
      "pid": 12345
    }
  ],
  "last_updated": "2025-01-18T10:30:00Z"
}
```

### Status Values
| Status | Meaning |
|--------|---------|
| `running` | Session active (terminal open) |
| `completed` | Task finished successfully |
| `failed` | Task failed or session crashed |
| `unknown` | Cannot determine status |
</manifest_system>

<session_id_format>
## Session ID Format

Format: `fork-{NNN}` where NNN is zero-padded sequence number.

Examples:
- `fork-001` (first session)
- `fork-042` (42nd session)

The ID is used for:
- Log file names: `.fork-sessions/fork-001.log`
- Handoff files: `.fork-sessions/fork-001-handoff.md`
- Status queries: "Check status of fork-001"
</session_id_format>

<directory_structure>
## Session Directory Structure

```
.fork-sessions/
├── manifest.json           # Master session list
├── fork-001-handoff.md     # Handoff doc for session 1
├── fork-001.log            # Output log for session 1
├── fork-002-handoff.md
├── fork-002.log
└── ...
```

This directory should be in `.gitignore`.
</directory_structure>

<status_checking>
## Checking Session Status

### Quick Status
```bash
# Check if process is running
ps -p $PID > /dev/null && echo "running" || echo "stopped"
```

### Check All Sessions
```bash
# Parse manifest and check each PID
jq -r '.sessions[] | "\(.id) \(.pid) \(.task_summary)"' .fork-sessions/manifest.json
```

### Detailed Status
For each session:
1. Check if PID exists
2. Check for completion markers (files created, tests passing)
3. Check log file for errors
</status_checking>

<completion_detection>
## Detecting Completion

### Method 1: Completion Marker Files
Agent creates a marker when done:
```bash
# In handoff, instruct agent to create:
touch .fork-sessions/fork-001-complete
```

### Method 2: Log Parsing
Look for completion patterns in output:
```bash
# Check for success indicators
grep -q "All tests passed" .fork-sessions/fork-001.log
grep -q "Task completed" .fork-sessions/fork-001.log
```

### Method 3: File Change Detection
Check if expected files were modified:
```bash
# Check if target file was touched recently
find src/auth/ -newer .fork-sessions/fork-001-handoff.md -type f
```
</completion_detection>

<cleanup>
## Session Cleanup

### After Successful Completion
```bash
# Update manifest status
jq '.sessions |= map(if .id == "fork-001" then .status = "completed" else . end)' \
  .fork-sessions/manifest.json > tmp && mv tmp .fork-sessions/manifest.json
```

### Purge Old Sessions
```bash
# Remove sessions older than 7 days
find .fork-sessions -name "fork-*.log" -mtime +7 -delete
find .fork-sessions -name "fork-*-handoff.md" -mtime +7 -delete
```

### Full Reset
```bash
rm -rf .fork-sessions
```
</cleanup>

<coordination>
## Coordinating Multiple Sessions

### Wait for All
```bash
# Simple: wait for all PIDs
for pid in $PIDS; do
  wait $pid
done
```

### First Failure
```bash
# Exit if any session fails
for id in fork-001 fork-002 fork-003; do
  if grep -q "ERROR\|FAILED" .fork-sessions/$id.log; then
    echo "$id failed"
    exit 1
  fi
done
```

### Dependency Chain
If task B depends on task A:
1. Spawn A
2. Wait for A's completion marker
3. Spawn B with A's output as input
</coordination>
