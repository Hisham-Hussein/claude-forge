---
name: update-roadmap
description: Updates roadmap folder (ACTIVE.md, QUEUE.md, LOG.md) based on conversation progress and git history. Maintains continuity across sessions by synchronizing roadmap/ with actual work done.
disable-model-invocation: true
---

# Update Roadmap

Synchronize `roadmap/` with actual work done — conversation progress, git history, and manual completions.

## Before starting

**Read [steps.md](steps.md) now.** It contains the complete 10-step process. Do not proceed from memory — load the steps from disk every time.

## Files to update

- `roadmap/ACTIVE.md` — progress, checked items, "How to Continue"
- `roadmap/QUEUE.md` — new discoveries, completed removals, prioritization
- `roadmap/LOG.md` — decision entries (max 10, push front / shift back)

## Checklist

Copy this and track progress:

```
Roadmap Update Progress:
- [ ] Step 0: Check git history for cross-session work
- [ ] Step 1: Analyze conversation for completions, discoveries, decisions
- [ ] Step 2: Update LOG.md (BEFORE trimming ACTIVE.md)
- [ ] Step 3: Update ACTIVE.md (check off criteria, update progress, How to Continue)
- [ ] Step 4: Update QUEUE.md (remove completed, add discoveries, fresh-agent check)
- [ ] Step 5: Check artifacts index (if artifacts/ exists)
- [ ] Step 6: Ensure handoff clarity
- [ ] Step 7: Verify ACTIVE.md section alignment (re-read from disk)
- [ ] Step 8: Memory sync check
- [ ] Step 9: Present summary to user
```

## Context

Active work:
@roadmap/ACTIVE.md

Queue and backlog:
@roadmap/QUEUE.md

Decision log:
@roadmap/LOG.md
