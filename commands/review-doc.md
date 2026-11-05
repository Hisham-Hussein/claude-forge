---
description: Run an independent reviewer loop on any document until it is ready for its next reader
argument-hint: <path/to/document.md>
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
  - Skill(reviewing-documents)
---

Invoke the reviewing-documents skill for: $ARGUMENTS
