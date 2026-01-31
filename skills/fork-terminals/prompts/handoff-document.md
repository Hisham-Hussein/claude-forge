# Handoff Document Meta-Prompt

This is a meta-prompt template. Fill in the placeholders to create a handoff document for spawning an agent.

<template>
```markdown
<fork_context>
## Task
{{TASK_DESCRIPTION}}

## Background
{{BACKGROUND_CONTEXT}}

## Session Info
- **Fork ID**: {{SESSION_ID}}
- **Parent Session**: {{PARENT_SESSION_ID}}
- **Spawned At**: {{TIMESTAMP}}

## Scope
**Files to modify:**
{{FILES_TO_MODIFY}}

**Files for context (read-only):**
{{CONTEXT_FILES}}

## Constraints
{{CONSTRAINTS}}

## Success Criteria
{{SUCCESS_CRITERIA}}

## Verification Steps
{{VERIFICATION_STEPS}}

## If Blocked
{{BLOCKED_INSTRUCTIONS}}

## Coordination Notes
{{COORDINATION_NOTES}}
</fork_context>
```
</template>

<filling_instructions>
## How to Fill This Template

### TASK_DESCRIPTION
One clear sentence describing what the agent should accomplish.
- Good: "Implement Google OAuth2 authentication provider"
- Bad: "Work on auth stuff"

### BACKGROUND_CONTEXT
2-3 sentences explaining why this task exists. Include:
- What problem it solves
- What led to this task
- Any relevant decisions already made

### SESSION_ID
Generated session ID (e.g., `fork-001`). Used for tracking.

### PARENT_SESSION_ID
The session that spawned this one. Use "root" if this is the original session.

### FILES_TO_MODIFY
Bullet list of specific files the agent should change:
```
- src/auth/providers/google.ts (create)
- src/auth/index.ts (modify)
- src/routes/auth.ts (modify)
```

### CONTEXT_FILES
Files the agent should read but NOT modify:
```
- src/auth/providers/email.ts (existing pattern to follow)
- docs/ARCHITECTURE.md
```

### CONSTRAINTS
What the agent should NOT do:
```
- Do not modify the AuthProvider interface
- Do not add new npm dependencies
- Do not touch files outside src/auth/
```

### SUCCESS_CRITERIA
Checkboxes for completion verification:
```
- [ ] /auth/google/login endpoint returns 302 to Google
- [ ] /auth/google/callback handles OAuth response
- [ ] User session created on successful auth
- [ ] `npm test auth` passes
```

### VERIFICATION_STEPS
Specific commands to run:
```
1. Run: `npm test auth`
2. Manual test: Visit /auth/google/login, verify redirect
3. Check: No TypeScript errors in src/auth/
```

### BLOCKED_INSTRUCTIONS
What to do if the task can't be completed:
```
If missing Google API credentials:
1. Document required env vars in .env.example
2. Add placeholder implementation
3. Note in completion that credentials needed
```

### COORDINATION_NOTES
For parallel tasks, explain boundaries:
```
This is Agent 1 of 3.
- Agent 2 handles API endpoints (will use your auth types)
- Agent 3 handles frontend (will call your auth hooks)
DO NOT modify anything in /api or /components.
```
</filling_instructions>

<minimal_version>
## Minimal Handoff (Quick Tasks)

For simple, isolated tasks:

```markdown
<fork_context>
## Task
{{TASK_DESCRIPTION}}

## Files
{{FILES_TO_MODIFY}}

## Done When
{{SUCCESS_CRITERIA}}
</fork_context>
```
</minimal_version>
