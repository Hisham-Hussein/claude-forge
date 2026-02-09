# Workflow: Agent Team Orchestration

This workflow replaces the standard sequential execution (Phases 1–8) with a coordinated agent team of 3 teammates. The lead agent orchestrates; teammates implement phases in parallel with adversarial quality review.

<prerequisites>
**Prerequisites: Verify Agent Teams Feature**

Before proceeding, check that agent teams are enabled:
- Environment variable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` must be set, OR
- `settings.json` must include `"experimentalAgentTeams": true`

If agent teams are NOT enabled:
1. Warn user: "Agent teams require the experimental agent teams feature. Enable it with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` or in settings.json."
2. Offer fallback: "Would you like to proceed in standard mode instead?"
3. If user accepts fallback, return to SKILL.md and proceed to Phase 1 normally (standard mode).

</prerequisites>

<lead_execution>
**Lead Execution: Phases 1–2**

The lead executes Phases 1 and 2 itself because they require user interaction (validation prompts, format choice, clarification questions).

1. Execute **Phase 1** (Parse Business Case) — extract structured data from all 9 sections
2. Execute **Phase 1b** (Load Reference Documents) — collect and load all references
3. Execute **Phase 1c** (Parse Story Map) — if story-map mode, extract SM-XXX registry
4. Execute **Phase 2** (Targeted Clarification) — ask user only what the business case doesn't answer

**After Phase 2 completes:**

Enter **delegate mode** (Shift+Tab). From this point forward, the lead MUST NOT implement any phases itself. The lead is restricted to:
- Creating and managing the shared task list
- Spawning and monitoring teammates
- Reviewing teammate plans
- Steering teammates if they get stuck
- Assembling final output (Phase 7)

</lead_execution>

<task_list_creation>
**Task List: Create Granular Tasks Before Spawning**

Before spawning teammates, the lead creates all tasks in the shared task list. This gives teammates clear, bounded work items to claim and complete.

**Requirements Analyst tasks (6 tasks):**

1. **RA-1: Transform BR-XX to FR-XX functional requirements**
   Phase 3.1 — Apply transformation pattern, domain prefixes, one-to-many decomposition.

2. **RA-2: Transform constraints to NFR-XX non-functional requirements**
   Phase 3.2 — Map Section 7 constraints to ISO 25010 categories.

3. **RA-3: Derive transition requirements TRANS-XX**
   Phase 3.3 — Data migration, integration, and adoption requirements.

4. **RA-4: Verify requirements against reference documents**
   Phase 3.5 — Data model field verification, filterable field verification, validation rules transfer.

5. **RA-5: Identify implicit requirements**
   Phase 3.6 — Data integrity, operational ordering, stakeholder workflows, system-managed fields.

6. **RA-6: Build traceability matrix**
   Phase 3.4 — Every derived requirement links to BR-XX source.

**Story Writer tasks (5 tasks):**

1. **SW-1: Build Epic/Feature/Story hierarchy from BR-XX or story map**
   Phase 4.1 — Business-case mode: derive from BR-XX groupings. Story-map mode: inherit Activity/Task/SM-XXX structure.

2. **SW-2: Write full story cards with As a/I want/So that**
   Phase 4.2 — Elaborate each story with role, capability, benefit. In story-map mode, expand SM-XXX compact entries.

3. **SW-3: Validate INVEST criteria per story**
   Phase 4.3 — Independent, Negotiable, Valuable, Estimable, Small, Testable. Flag failures, suggest splits.

4. **SW-4: Write acceptance criteria**
   Phase 4.4 — Checklist format for simple stories, Given/When/Then for complex scenarios.

5. **SW-5: Apply vertical slicing to large stories**
   Phase 4.5 — Split vertically (end-to-end thin slices), not horizontally (by layer).

**Quality Reviewer tasks (5 tasks — all depend on RA and SW completing):**

1. **QR-1: Validate prioritization and 60% rule**
   Phase 5 — Inherit priorities from BRD, apply 60% Must-have ceiling, Kano validation.
   *Depends on: RA-1, RA-2, SW-1*

2. **QR-2: Verify each requirement: atomic, testable, traceable, prioritized, unambiguous**
   Phase 6.1 — Individual requirement quality checks with fixes.
   *Depends on: RA-1 through RA-6*

3. **QR-3: Challenge Requirements Analyst — message directly with quality issues**
   Message the Analyst directly with specific issues: "FR-SEARCH-03 is not testable — lacks measurable criteria." Analyst fixes and updates output.
   *Depends on: RA-1 through RA-6*

4. **QR-4: Challenge Story Writer — message directly with INVEST failures or weak AC**
   Message the Writer directly with specific issues: "US-007 fails INVEST — not independent from US-006." Writer fixes and updates output.
   *Depends on: SW-1 through SW-5*

5. **QR-5: Document-level verification: count accuracy, cross-reference integrity**
   Phase 6.2 — Count FR/NFR/TRANS totals, verify priority percentages, check traceability completeness, cross-reference integrity, no orphan requirements.
   *Depends on: QR-2, QR-3, QR-4*

**Task dependencies:**
- RA tasks have no dependencies — start immediately
- SW tasks have no dependencies — start immediately (parallel with RA)
- QR-1 depends on RA-1, RA-2, SW-1
- QR-2, QR-3 depend on all RA tasks completing
- QR-4 depends on all SW tasks completing
- QR-5 depends on QR-2, QR-3, QR-4 (runs after fixes are applied)

</task_list_creation>

<team_spawn>
**Team Spawn: Create Agent Team with 3 Teammates**

Each teammate receives full context so they can work autonomously. Do NOT give vague instructions like "do Phase 3" — include the actual phase content.

**Teammate 1: Requirements Analyst**

| Setting | Value |
|---------|-------|
| Model | Sonnet |
| Plan Approval | Yes — lead reviews plan before implementation |

Spawn prompt must include:
- Full parsed business case summary (Phase 1 output: stakeholders, constraints, BR-XX table, scope, success criteria)
- Reference document content (Phase 1b output: data model, field specs, validation rules)
- Story map data if applicable (Phase 1c output: SM-XXX registry, hierarchy)
- User's format choice (SRS, User Stories, or Both)
- **Complete Phase 3, 3.5, and 3.6 instructions** from SKILL.md (the actual transformation patterns, domain prefix table, ISO 25010 mapping, reference verification steps, implicit requirement checks)
- Instruction to read `references/srs-methodology.md` before starting
- Output path: write all work to `.charter/.tmp/requirements-draft.md`

**Teammate 2: Story Writer**

| Setting | Value |
|---------|-------|
| Model | Sonnet |
| Plan Approval | Yes — lead reviews plan before implementation |

Spawn prompt must include:
- Full parsed business case summary (Phase 1 output)
- Reference document content (Phase 1b output)
- Story map data if applicable (Phase 1c output — critical for hierarchy inheritance)
- User's format choice
- **Complete Phase 4 instructions** from SKILL.md (hierarchy building, story format for both modes, INVEST validation, AC formats, vertical slicing)
- Instruction to read `references/user-story-methodology.md` THEN `references/acceptance-criteria-methodology.md` before starting
- Output path: write all work to `.charter/.tmp/stories-draft.md`

**Teammate 3: Quality Reviewer**

| Setting | Value |
|---------|-------|
| Model | Sonnet |
| Plan Approval | No — starts after others finish, adversarial by nature |

Spawn prompt must include:
- Full parsed business case summary (Phase 1 output)
- Reference document content (Phase 1b output)
- User's format choice
- **Complete Phase 5 and Phase 6 instructions** from SKILL.md (prioritization rules, 60% rule, Kano validation, quality verification checks, document-level verification)
- Instruction to read the Analyst's output at `.charter/.tmp/requirements-draft.md` and Writer's output at `.charter/.tmp/stories-draft.md` once their tasks are complete
- Instruction to **message teammates directly** when issues are found (not just document them)
- Output path: write review notes to `.charter/.tmp/quality-review.md`

</team_spawn>

<coordination_rules>
**Coordination: Lead Monitors and Steers**

While teammates work, the lead:

1. **Stays in delegate mode** — does NOT implement any phases
2. **Monitors the shared task list** — periodically checks task progress
3. **Reviews teammate plans** — Analyst and Writer submit plans before implementing; lead approves or redirects
4. **Checks in on progress** — if a teammate hasn't updated tasks in a while, ask for a status update
5. **Handles stuck teammates** — if a teammate is blocked (e.g., can't find a reference document, ambiguous requirement), the lead provides clarification or escalates to the user
6. **Does NOT rush teammates** — let the Quality Reviewer complete the full adversarial cycle

**Wait for all teammates to finish** before proceeding to assembly. Do NOT start Phase 7 while any teammate has incomplete tasks.

</coordination_rules>

<adversarial_protocol>
**Adversarial Quality Review Protocol**

The Quality Reviewer's role is to challenge and improve — not just validate. This is the key advantage of agent teams over standard mode.

**Protocol:**

1. **Wait** for Requirements Analyst and Story Writer to complete all their tasks (task dependencies enforce this)

2. **Read** their output files:
   - `.charter/.tmp/requirements-draft.md` (Analyst's work)
   - `.charter/.tmp/stories-draft.md` (Writer's work)

3. **Challenge the Requirements Analyst directly** — message with specific, actionable issues:
   - "FR-SEARCH-03 is not testable — it says 'fast search' but lacks measurable criteria. Suggest: 'returns results within 2 seconds for up to 10,000 records.'"
   - "NFR-PERF-01 has no source traceability — which constraint from Section 7 does it derive from?"
   - "Missing implicit requirement: BR-03 implies deduplication when collecting from multiple platforms, but no FR covers conflict resolution."

4. **Challenge the Story Writer directly** — message with specific issues:
   - "US-007 fails INVEST: it depends on US-006 completing first (not Independent). Suggest splitting the shared state into a separate setup story."
   - "US-012 acceptance criteria are not testable — 'system works well' is not verifiable. Rewrite with specific measurable outcomes."
   - "Epic 3 has 12 stories but only 2 have acceptance criteria with edge cases. Add negative/boundary test scenarios."

5. **Analyst and Writer fix issues** — they update their draft files based on the Reviewer's feedback

6. **Re-check** — Quality Reviewer reads updated drafts and verifies fixes. Repeat until satisfied.

7. **Document-level verification** (QR-5) — final pass checking counts, cross-references, and traceability integrity

The adversarial cycle may iterate 2–3 times. This is expected and produces higher-quality output than a single review pass.

</adversarial_protocol>

<file_conflict_avoidance>
**File Conflict Avoidance: Isolated Scratch Files**

Each teammate writes to isolated files to prevent conflicts:

| Teammate | Scratch File | Content |
|----------|-------------|---------|
| Requirements Analyst | `.charter/.tmp/requirements-draft.md` | FR-XX, NFR-XX, TRANS-XX, traceability matrix |
| Story Writer | `.charter/.tmp/stories-draft.md` | Epic/Feature/Story hierarchy, full story cards, AC |
| Quality Reviewer | `.charter/.tmp/quality-review.md` | Review notes, issues found, fix verification log |

**Rules:**
- Each teammate ONLY writes to their own scratch file
- Teammates READ each other's files (Quality Reviewer reads both drafts)
- The lead reads all three files during assembly (Phase 7)
- The `.charter/.tmp/` directory is created at the start and deleted after assembly

</file_conflict_avoidance>

<quality_gates>
**Quality Gates with Hooks (Recommended)**

For maximum rigor, recommend the user configure these hooks before running agent-team mode:

**TaskCompleted hook:**
```json
{
  "event": "TaskCompleted",
  "command": "check-traceability.sh",
  "exitBehavior": {
    "2": "Ask teammate to add missing traceability before marking complete"
  }
}
```
Exit code 2 if a task is marked complete but any requirement/story lacks BR-XX traceability.

**TeammateIdle hook:**
```json
{
  "event": "TeammateIdle",
  "command": "check-tasks-remaining.sh",
  "exitBehavior": {
    "2": "Teammate still has incomplete tasks — resume work"
  }
}
```
Exit code 2 with feedback if a teammate goes idle before all their assigned tasks are done.

These hooks are optional but strongly recommended for production-quality output.

</quality_gates>

<assembly_and_cleanup>
**Assembly and Cleanup: Lead Produces Final Output**

After ALL teammates complete ALL tasks (including the adversarial review cycle):

**1. Collect draft files:**
- Read `.charter/.tmp/requirements-draft.md` (Analyst's verified output)
- Read `.charter/.tmp/stories-draft.md` (Writer's verified output)
- Read `.charter/.tmp/quality-review.md` (Reviewer's verification log)

**2. Assemble final output using templates (Phase 7):**
- Read `templates/srs-template.md` and/or `templates/user-stories-template.md`
- Merge Analyst's requirements and Writer's stories into the template structure
- Set `> Production method: agent-team` in document metadata
- Write to the agent-team output paths:
  - `.charter/REQUIREMENTS-agent-team.md` (if SRS selected)
  - `.charter/USER-STORIES-agent-team.md` (if User Stories selected)

**3. Run Phase 8 completion report:**
- Include standard completion metrics (counts, coverage, priorities)
- Add agent-team specific metadata:
  - Production method: agent-team
  - Team size: 3 teammates
  - Quality review: Adversarial (inter-agent messaging)
- Include summary from Quality Reviewer's verification log

**4. Clean up the team:**
- Shut down all 3 teammates first
- Then clean up any remaining team resources

**5. Delete scratch files:**
- Remove `.charter/.tmp/` directory and all contents
- Scratch files are intermediate artifacts — only the final assembled documents matter

</assembly_and_cleanup>
