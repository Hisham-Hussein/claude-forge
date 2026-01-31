---
description: Fix contract drifts between directives and scripts
argument-hint: [directive_path]
allowed-tools: Skill(fix-drifts), Skill(contract-driven-integration), Read, Edit, Grep, Glob, AskUserQuestion, TodoWrite
---

Invoke the fix-drifts skill to detect and correct contract drifts for: $ARGUMENTS

If no directive path provided, ask user which directive to check.
