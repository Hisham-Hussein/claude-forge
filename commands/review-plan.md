---
description: Run adversarial multi-round plan review with dynamic agent teams until convergence
argument-hint: <path/to/plan.md>
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - Edit
  - Write
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - AskUserQuestion
  - Bash
  - Skill(reviewing-plans-adversarially)
  - Skill(reviewing-documents)
---

Invoke the reviewing-plans-adversarially skill for: $ARGUMENTS
