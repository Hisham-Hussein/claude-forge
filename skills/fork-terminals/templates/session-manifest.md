# Session Manifest Template

Copy this structure to initialize `.fork-sessions/manifest.json`.

<initial_manifest>
```json
{
  "version": "1.0",
  "project": "{{PROJECT_NAME}}",
  "sessions": [],
  "last_updated": "{{TIMESTAMP}}",
  "settings": {
    "auto_cleanup_days": 7,
    "log_retention": true,
    "completion_markers": true
  }
}
```
</initial_manifest>

<session_entry>
## Session Entry Structure

Each session in the `sessions` array:

```json
{
  "id": "fork-001",
  "agent": "claude",
  "mode": "interactive",
  "task_summary": "Brief description of the task",
  "status": "running",
  "spawned_at": "2025-01-18T10:30:00Z",
  "completed_at": null,
  "working_dir": "/absolute/path/to/project",
  "handoff_file": ".fork-sessions/fork-001-handoff.md",
  "log_file": ".fork-sessions/fork-001.log",
  "pid": 12345,
  "exit_code": null,
  "parent_session": "root",
  "related_sessions": [],
  "files_modified": [],
  "notes": ""
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique session ID (fork-NNN) |
| `agent` | string | "claude", "gemini", "aider", or "cli" |
| `mode` | string | "interactive" or "headless" |
| `task_summary` | string | Human-readable task description |
| `status` | string | "running", "completed", "failed", "unknown" |
| `spawned_at` | ISO8601 | When session was created |
| `completed_at` | ISO8601 | When session finished (null if running) |
| `working_dir` | string | Absolute path to working directory |
| `handoff_file` | string | Path to handoff document |
| `log_file` | string | Path to output log |
| `pid` | number | Process ID (for status checking) |
| `exit_code` | number | Exit code (null if running) |
| `parent_session` | string | ID of spawning session or "root" |
| `related_sessions` | array | IDs of parallel/related sessions |
| `files_modified` | array | List of files changed (populated on completion) |
| `notes` | string | Free-form notes about the session |
</session_entry>

<example_manifest>
## Example: Active Manifest

```json
{
  "version": "1.0",
  "project": "my-webapp",
  "sessions": [
    {
      "id": "fork-001",
      "agent": "claude",
      "mode": "interactive",
      "task_summary": "Implement Google OAuth provider",
      "status": "completed",
      "spawned_at": "2025-01-18T10:30:00Z",
      "completed_at": "2025-01-18T11:15:00Z",
      "working_dir": "/home/user/my-webapp",
      "handoff_file": ".fork-sessions/fork-001-handoff.md",
      "log_file": ".fork-sessions/fork-001.log",
      "pid": 12345,
      "exit_code": 0,
      "parent_session": "root",
      "related_sessions": ["fork-002", "fork-003"],
      "files_modified": [
        "src/auth/providers/google.ts",
        "src/auth/index.ts"
      ],
      "notes": "Completed successfully. Tests passing."
    },
    {
      "id": "fork-002",
      "agent": "gemini",
      "mode": "headless",
      "task_summary": "Generate API documentation",
      "status": "running",
      "spawned_at": "2025-01-18T10:35:00Z",
      "completed_at": null,
      "working_dir": "/home/user/my-webapp",
      "handoff_file": ".fork-sessions/fork-002-handoff.md",
      "log_file": ".fork-sessions/fork-002.log",
      "pid": 12456,
      "exit_code": null,
      "parent_session": "root",
      "related_sessions": ["fork-001", "fork-003"],
      "files_modified": [],
      "notes": ""
    }
  ],
  "last_updated": "2025-01-18T10:35:00Z",
  "settings": {
    "auto_cleanup_days": 7,
    "log_retention": true,
    "completion_markers": true
  }
}
```
</example_manifest>

<bash_helpers>
## Bash Helpers

### Initialize Manifest
```bash
mkdir -p .fork-sessions
cat > .fork-sessions/manifest.json << 'EOF'
{
  "version": "1.0",
  "project": "$(basename $(pwd))",
  "sessions": [],
  "last_updated": "$(date -Iseconds)",
  "settings": {
    "auto_cleanup_days": 7,
    "log_retention": true,
    "completion_markers": true
  }
}
EOF
```

### Get Next Session ID
```bash
next_id=$(jq -r '
  .sessions | map(.id | ltrimstr("fork-") | tonumber) | max // 0 | . + 1 |
  "fork-" + (. | tostring | if length < 3 then "0" * (3 - length) + . else . end)
' .fork-sessions/manifest.json)
echo $next_id
```

### Add Session Entry
```bash
jq --arg id "$SESSION_ID" \
   --arg agent "$AGENT" \
   --arg task "$TASK" \
   --arg dir "$PWD" \
   --arg pid "$PID" \
   '.sessions += [{
     id: $id,
     agent: $agent,
     task_summary: $task,
     status: "running",
     spawned_at: (now | todate),
     working_dir: $dir,
     pid: ($pid | tonumber)
   }] | .last_updated = (now | todate)' \
   .fork-sessions/manifest.json > tmp && mv tmp .fork-sessions/manifest.json
```

### Update Session Status
```bash
jq --arg id "fork-001" \
   --arg status "completed" \
   '.sessions |= map(if .id == $id then .status = $status | .completed_at = (now | todate) else . end)' \
   .fork-sessions/manifest.json > tmp && mv tmp .fork-sessions/manifest.json
```
</bash_helpers>
