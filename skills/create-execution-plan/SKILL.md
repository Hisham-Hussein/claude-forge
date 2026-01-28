---
name: create-execution-plan
description: Use when you have architecture documents and user stories ready and need to plan implementation phases. Invoke after design docs are complete, before coding begins, or when asked to create an execution plan, project roadmap, or phase breakdown.
---

<essential_principles>

**This skill produces project-level roadmaps, NOT implementation-level plans.**

| Level | Skill | Output |
|-------|-------|--------|
| **Project (this skill)** | /create-execution-plan | Phases → Stories → Tasks (what to build) |
| **Implementation** | superpowers:writing-plans | Task → Steps (how to build each task) |
| **Execution** | superpowers:executing-plans | Steps → Code |

**Methodology: Clean Architecture + Vertical Slices + FDD**

1. **Clean Architecture layers**: Domain → Application → Infrastructure (dependency flows inward)
2. **Vertical Slices**: Each phase delivers working end-to-end functionality
3. **FDD-style tasks**: Atomic tasks with explicit Input/Output/Test

**Task Structure (CRITICAL):**

Every task MUST have:

```text
Task X.Y: [Description]
├── Input: What this task needs to start
├── Output: What this task produces
├── Test: How to verify correctness
└── Commit: Conventional commit message
```

This structure minimizes AI coding errors by making requirements explicit.

</essential_principles>

<objective>
Transform architecture documents and user stories into phased execution plans with atomic, TDD-ready tasks. Output enables AI-assisted development with clear work units that fit within context windows and have verifiable success criteria.
</objective>

<quick_start>
**Required inputs:**

- USER-STORIES.md (with acceptance criteria)
- ARCHITECTURE-DOC.md or Design Doc (from /create-design-doc)

**Optional inputs:**

- BUSINESS-CASE.md (constraints, success criteria)
- Tech stack research, API docs, data templates

**Output:**

- EXECUTION-PLAN.md (phases, stories, tasks with I/O/Test)
- jira-import.csv (optional JIRA bulk import)

**Run:** `/create-execution-plan path/to/USER-STORIES.md path/to/ARCHITECTURE-DOC.md`
</quick_start>

<intake>
**Confirm inputs:**

1. Where are the required documents?
   - USER-STORIES.md: [path]
   - ARCHITECTURE-DOC.md: [path]

2. Any optional documents?
   - BUSINESS-CASE.md: [path or skip]
   - Tech stack research: [path or skip]
   - Other (API docs, data templates): [paths or skip]

3. Where should output go?
   - Default: same directory as USER-STORIES.md
   - Custom: [path]

4. Generate JIRA export?
   - Yes / No

**After confirming, read `workflows/generate-plan.md` and follow it exactly.**
</intake>

<routing>

| Intent | Workflow |
|--------|----------|
| Generate new plan | `workflows/generate-plan.md` |
| Direct invocation with args | `workflows/generate-plan.md` (parse paths from args) |

**If arguments provided:** Parse document paths from ARGUMENTS and proceed directly to workflow.
</routing>

<reference_index>
All in `references/`:

- **Methodology:** methodology.md (Clean Architecture + VSA + FDD integration)
- **Task decomposition:** task-decomposition.md (FDD-style atomic tasks)
</reference_index>

<templates_index>
All in `templates/`:

- **Plan structure:** execution-plan.md (EXECUTION-PLAN.md template)
- **JIRA export:** jira-import.csv (CSV format for bulk import)
</templates_index>

<success_criteria>
Execution plan is complete when:

- [ ] All user stories assigned to phases
- [ ] Must-have stories in early phases
- [ ] Each phase delivers working vertical slice
- [ ] Every task has Input/Output/Test
- [ ] Phase transitions documented (output → input)
- [ ] Definition of Done per phase
- [ ] JIRA export generated (if requested)
</success_criteria>
