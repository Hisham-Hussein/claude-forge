---
description: Run adversarial multi-round spec review with dynamic agent teams until convergence
argument-hint: <path/to/spec.md>
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - Edit
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - AskUserQuestion
  - Skill(adversarial-spec-review)
---

Invoke the adversarial-spec-review skill for: $ARGUMENTS
