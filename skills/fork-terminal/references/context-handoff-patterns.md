# Context Handoff Patterns

Best practices for structuring handoff documents that transfer context between agent sessions.

<principles>
## Core Principles

### 1. Be Explicit About Task Boundaries
The receiving agent has no context from your session. State clearly:
- What to do (task)
- What NOT to do (constraints)
- What files matter (scope)
- What success looks like (criteria)

### 2. Compress, Don't Dump
Don't paste entire conversations. Distill to:
- Key decisions made
- Relevant code snippets
- Critical constraints discovered

### 3. Provide Verification Steps
Include how the receiving agent should verify their work:
- Tests to run
- Behaviors to check
- Edge cases to consider

### 4. Include Recovery Context
If this task is part of a larger workflow:
- What step is this?
- What depends on this completing?
- What to do if blocked?
</principles>

<handoff_structure>
## Recommended Handoff Structure

```markdown
<fork_context>
## Task
[One sentence: what the agent should accomplish]

## Background
[2-3 sentences: why this task exists, what led to it]

## Scope
**Files to modify:**
- path/to/file1.py
- path/to/file2.py

**Files for context (read-only):**
- docs/ARCHITECTURE.md
- src/types.ts

## Constraints
- [Constraint 1]
- [Constraint 2]
- [Things explicitly NOT to do]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests pass: `npm test`

## If Blocked
[What to do if the task can't be completed]
</fork_context>
```
</handoff_structure>

<examples>
## Examples

### Good Handoff
```markdown
<fork_context>
## Task
Implement OAuth2 login flow for Google authentication.

## Background
User auth currently uses email/password only. We're adding Google OAuth as the first SSO provider. The auth service already has the infrastructure for multiple providers.

## Scope
**Files to modify:**
- src/auth/providers/google.ts (create)
- src/auth/index.ts (add provider registration)
- src/routes/auth.ts (add /auth/google/* routes)

**Files for context:**
- src/auth/providers/email.ts (existing provider pattern)
- docs/AUTH_ARCHITECTURE.md

## Constraints
- Use existing AuthProvider interface (don't modify it)
- Store tokens in existing session store
- No new dependencies without checking package.json first

## Success Criteria
- [ ] /auth/google/login redirects to Google
- [ ] /auth/google/callback handles the response
- [ ] User is created/found and session established
- [ ] `npm test auth` passes

## If Blocked
If the Google API requires config we don't have, document what's needed in .env.example and complete the implementation with placeholder values.
</fork_context>
```

### Bad Handoff (Too Vague)
```markdown
Add Google login to the app. Look at how email login works.
```
Problems: No specific files, no constraints, no success criteria, no recovery path.

### Bad Handoff (Too Much)
```markdown
[500 lines of conversation history]
[Full file dumps]
[Every decision ever made]
```
Problems: Overwhelms context window, buries the actual task.
</examples>

<parallel_handoffs>
## Parallel Task Handoffs

When spawning multiple agents for related tasks, each handoff should:

### 1. Define Clear Boundaries
```markdown
## Your Scope (Agent 1 of 3)
You handle: Authentication module
Agent 2 handles: API endpoints
Agent 3 handles: Frontend components

DO NOT modify anything in /api or /components.
```

### 2. Specify Coordination Points
```markdown
## Coordination
When you're done, your changes will be merged with:
- Agent 2's API changes (uses your auth types)
- Agent 3's UI (calls your auth hooks)

Export interfaces in src/auth/types.ts - other agents depend on them.
```

### 3. Define Completion Signal
```markdown
## When Done
Create file: .fork-complete/agent-1-auth
Contents: List of files modified and any notes for integration
```
</parallel_handoffs>

<anti_patterns>
## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| "Just figure it out" | Agent makes wrong assumptions | Be explicit about approach |
| Dumping full files | Wastes context window | Reference files, include snippets |
| No success criteria | Agent doesn't know when done | Add testable criteria |
| No constraints | Agent over-engineers | List what NOT to do |
| No scope | Agent touches wrong files | List specific files |
| Assuming context | Agent lacks necessary info | Include background |
</anti_patterns>
