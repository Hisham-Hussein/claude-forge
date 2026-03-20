---
description: Run adversarial multi-round plan review with dynamic agent teams until convergence
argument-hint: <path/to/plan.md>
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
  - Skill(reviewing-plans-adversarially)
---

Invoke the reviewing-plans-adversarially skill for: $ARGUMENTS
