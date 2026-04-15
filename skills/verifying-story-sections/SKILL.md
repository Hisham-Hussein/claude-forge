---
name: verifying-story-sections
description: Use when creating story specs with bmad-create-story to catch source document deviations incrementally before they cascade. Also use when auditing an existing story spec against its source documents (PRD, architecture, data model, epics, UX specs).
---

<objective>
Catch source-document deviations incrementally as each story section is written — not after the entire story is complete. A read-only sonnet verifier compares each section against the relevant source documents and project principles, so errors are fixed before downstream sections build on them.

Story specs synthesize facts from multiple source documents (PRD, architecture, data model, epics, UX specs) into a single developer guide. A wrong fact early in the story — a misquoted field name, a missing port interface, a wrong table relationship — propagates through every downstream section. The type design references the wrong field. The task breakdown implements the wrong type. The testing section validates the wrong behavior. By line 400, you have a coherent-looking story that's internally consistent but wrong relative to the sources.

Verifying each section against its sources catches errors at the point of introduction — when fixing costs one edit, not twenty.
</objective>

<quick_start>
Invoke this skill alongside bmad-create-story. After writing each section group, spawn the verifier from `templates/verification-prompt.md` with the section text and source document excerpts inline. Commit the section only after the verifier returns PASS. If deviations are found, fix and re-verify (up to 3 cycles, then escalate to user).
</quick_start>

<scope>
The story creation workflow (bmad-create-story) owns artifact analysis, section content, and template structure. This skill owns only the verification loop — comparing what was written against what the source documents and principles require.

This skill does NOT replace the existing `checklist.md` post-creation validation. That checklist performs holistic review after completion (disaster prevention, LLM optimization, competitive quality). This skill performs incremental fidelity checking during creation (source accuracy, internal consistency). They are complementary — this skill prevents the cascading errors that make post-creation review harder.
</scope>

<section_groups>
Story specs have 5 natural verification checkpoints. Each group depends on the accuracy of previous groups, which is why incremental verification prevents compounding.

| # | Section Group | What Gets Verified | Source Documents |
|---|--------------|-------------------|-----------------|
| 1 | **Story statement + Acceptance Criteria** | Scope, user role, AC completeness | Epics file, PRD (FR references) |
| 2 | **Tasks / Subtasks** | AC coverage, architecture alignment | ACs (internal), architecture doc, data model |
| 3 | **Architecture context** (existing code, patterns, file structure) | Factual accuracy of claims about codebase | Architecture doc, data model spec, previous story, actual codebase |
| 4 | **Data model + interface design** (types, ports, adapters, composition) | Field names, port methods, type shapes, relationships | Data model spec, architecture doc, shared package types |
| 5 | **Guardrails** (testing reqs, dependency rules, naming, what NOT to build) | Constraint completeness, principle alignment | CLAUDE.md, architecture doc, previous story intelligence |
</section_groups>

<source_document_mapping>
Which source excerpts to inline for each section group. **Excerpt selection principle:** prefer broader sections over narrow snippets. When the mapping says "tables and fields this story touches," include the full table definitions from the data model — not just the fields you think are relevant. The verifier needs enough context to catch what you missed, not just confirm what you included.

**Group 1 (Story + ACs):**
- Epics file: the specific story entry — user story statement, acceptance criteria, technical requirements
- PRD: the functional requirements this story traces to (check FR references in the epic entry)

**Group 2 (Tasks / Subtasks):**
- The ACs from Group 1 (already in the story file — internal consistency check)
- Architecture doc: relevant patterns (adapter pattern, port design, composition roots)
- Data model spec: full table definitions for all tables this story touches (not just the fields you referenced — include the complete table so the verifier can catch omissions)

**Group 3 (Architecture context):**
- Architecture doc: tech stack, code structure, file organization, relevant subsystem design
- Data model spec: tables, relationships, state machines relevant to this story
- Previous story file: files created, patterns established, dev notes
- Codebase verification results: before spawning the verifier, run Glob/Grep on all codebase claims in the section (file paths, exports, existing code). Include the results in the verifier prompt as "Codebase Verification Results" so the verifier can compare claims against reality without needing tool access.

**Group 4 (Data model + interface design):**
- Data model spec: exact field names, types, constraints, relationships for affected tables — include full table definitions
- Architecture doc: port interfaces, adapter patterns, type design conventions
- Shared package exports: if prior stories have been implemented, run Grep on the barrel exports and include results

**Group 5 (Guardrails):**
- CLAUDE.md: architectural principles, testing requirements, naming conventions
- Architecture doc: testing standards, dependency rules
- Previous story: learnings, anti-patterns discovered, what NOT to repeat
</source_document_mapping>

<procedure>
Repeat for each section group:

```
Section Group N:
- [ ] Write the section from source documents
- [ ] Spawn verifier (see templates/verification-prompt.md)
      Model: sonnet (fast, precise enough for comparison work)
      Mode: read-only — verifier reports findings, never edits the story
- [ ] Verifier returned PASS? -> Commit section to story file -> Next group
- [ ] Verifier returned deviations? -> Fix -> Re-spawn verifier (re-verification mode)
- [ ] Re-verification PASS? -> Commit -> Next group
- [ ] 3 fix cycles exhausted without PASS? -> Escalate to user with remaining issues
```

The verifier receives four inputs:

1. **Section text** (inline) — the full text of the section group just written. Paste it into the prompt so the verifier does not need to read the story file for the current section.

2. **Source document excerpts** (inline) — the specific sections from source documents that this story section draws from. Paste the relevant excerpts with document name and section path for each.

3. **Project principles file** (path) — the path to CLAUDE.md. The verifier reads this for architectural principle compliance.

4. **Story file so far** (path) — the path to the story file containing all previously committed sections. The verifier reads this for internal consistency checking. Empty for Section Group 1.
</procedure>

<verification_areas>
The verifier checks seven things. These are ordered by cascade severity — a source fidelity error causes more downstream damage than an actionability gap.

1. **Source document fidelity** — Does the section accurately reflect its source documents? The verifier must build an explicit **comparison table** mapping every factual claim in the story section to its source text. If the data model spec says field X is a `singleSelect` with specific choices, does the story section say that? If the architecture doc specifies 3 adapter patterns, are all 3 reflected? Every claim not traceable to a source row is flagged as unsupported. Cite the specific source text and the specific story text that diverges.

2. **Completeness** — Are all relevant requirements from source documents captured? A missing constraint is invisible to the developer — they cannot follow guidance that is not there. Check: are all fields from the data model included? All ports from the architecture? All ACs from the epic?

3. **Source coherence** — When multiple source documents are provided, do they agree with each other on the facts the story references? If the PRD says field X is required and the data model spec says it is optional, or the architecture defines an interface that contradicts the data model's table structure, flag this as a SOURCE CONFLICT. The story author cannot resolve source conflicts alone — escalate to the user with both source locations cited. Do not penalize the story for choosing one side of a conflict; flag the conflict itself.

4. **Internal consistency** — Does this section contradict earlier sections in the same story? Does an AC reference a type that the data model section defines differently? Does a task reference a file path that the architecture section placed elsewhere? For Groups 3-5: actively scan every entity (field name, type, file path, interface method) mentioned in this section against all previously committed sections. If this section says field X is type Y, and an earlier section references field X as type Z, that is a cross-group regression.

5. **Actionability** — Is the section specific enough for a developer agent to implement without ambiguity? The developer agent will ONLY have this story file — everything it needs must be present. Apply these concrete tests (fail any = deviation):
   - Every interface/port mentioned: are its method signatures listed?
   - Every file path referenced: is the full path from repo root given?
   - Every type mentioned: is its shape defined or a reference to its definition location?
   - Every "follow pattern X": is the pattern described inline or cited by file:line?
   - Every constraint ("must be", "required", "at most"): is the specific value/threshold stated?

6. **Principle compliance** — Do design decisions in this section honor the project's CLAUDE.md principles? Dependency direction, interface segregation, vendor portability, error handling patterns — check against the principles the project actually states, not theoretical best practices.

7. **Codebase claim verification** (Groups 3-4 only) — When the story claims "the shared package already exports X," "file Y exists at path Z," or "the existing adapter follows pattern W," the verifier must use Glob or Grep to confirm. Do not trust prose claims about codebase state. Stale claims about what exists are a common source of developer confusion.
</verification_areas>

<severity_classification>
Every deviation must be classified by severity. This focuses fix effort on what matters and prevents the fix-verify loop from churning on trivial findings.

- **CRITICAL**: Wrong fact that will propagate and cause downstream errors — wrong field name, wrong type, wrong relationship, missing required constraint, wrong interface method signature. A developer implementing from this story will write incorrect code. Must fix before proceeding.
- **MAJOR**: Missing information that leaves a gap the developer cannot fill — port method not listed, constraint not mentioned, architecture pattern referenced but not described. The developer will have to guess. Should fix before proceeding.
- **MINOR**: Imprecise wording that is unlikely to cause implementation errors but could be clearer — slightly informal description of a well-defined concept, redundant context. Fix if convenient. Does not block section commitment.

The fix-reverify loop is required only for CRITICAL and MAJOR deviations. MINOR findings are logged in the verifier report but do not block commitment of the section.
</severity_classification>

<intentional_deviations>
Sometimes the story legitimately departs from a source document — the source is stale, the user made a decision that overrides it, or a refinement emerged during story creation. Without a mechanism to mark these, the verifier will re-flag them every cycle, wasting fix-verify iterations.

When the story author knows a deviation from a source is intentional:
1. Annotate the deviation inline in the story section with: `<!-- INTENTIONAL DEVIATION: [reason] -->`
2. The verifier acknowledges annotated deviations in its report but does not count them as findings.
3. Unannotated deviations are always flagged — the annotation is opt-in and requires a reason.

The verifier must still report intentional deviations in a separate "Acknowledged Deviations" section so the user can audit them if desired. If the reason is weak or missing, the verifier should flag it as a MAJOR deviation (an unjustified intentional deviation is worse than an accidental one).
</intentional_deviations>

<fix_reverify_loop>
When the verifier finds CRITICAL or MAJOR deviations:

1. The story author fixes the section.
2. The verifier is re-spawned in **re-verification mode**. In addition to the 7 standard checks, re-verification also checks:
   - Did each fix actually resolve the reported deviation?
   - Did any fix introduce new inconsistencies with the rest of the story?
3. If re-verification passes, commit and move on.
4. If re-verification finds more issues, fix and re-verify again.
5. **Cap: 3 fix-verify cycles.** If the section still has deviations after 3 cycles, escalate to the user. Something may need human judgment — perhaps the source documents themselves are inconsistent, or the story needs to intentionally deviate from a source for good reasons.
</fix_reverify_loop>

<standalone_audit>
To audit an existing story spec (not during creation):

1. Read the complete story file.
2. Identify which source documents it references (check the References section).
3. For each section group, spawn the verifier with the section text + source excerpts.
4. Collect all deviations across all groups.
5. Present a consolidated report: which sections have issues, what the sources actually say, and suggested fixes.

This mode is useful when source documents have been updated after a story was written, or when reviewing a story created by a different agent.
</standalone_audit>

<anti_patterns>
<pitfall name="verifying-without-sources">
Do not spawn the verifier with only the section text and no source excerpts. The verifier cannot check fidelity if it has nothing to compare against. Always inline the relevant source document sections.
</pitfall>

<pitfall name="trusting-codebase-claims">
When the story section claims "the shared package already exports X" or "file Y exists at path Z," do not take this at face value during verification. Use Glob or Grep to confirm. Stale claims about codebase state are a common source of developer confusion.
</pitfall>

<pitfall name="over-verifying-boilerplate">
The Dev Agent Record section (agent model, debug log, completion notes, file list) is a template placeholder. Do not waste a verification cycle on it.
</pitfall>
</anti_patterns>

<verification_audit_trail>
After each section group completes verification, append a verification log entry to the story file as an HTML comment. This enables process improvement and post-hoc auditing.

```
<!-- Verification Log
Group 1: PASS (1 cycle)
Group 2: PASS after fixes (2 cycles) — D1 [CRITICAL]: wrong field type personaId, D2 [MAJOR]: missing FR7 constraint
Group 3: PASS (1 cycle) — 1 MINOR logged (imprecise adapter description)
Group 4: PASS after fixes (3 cycles) — D1 [CRITICAL]: port method signature wrong, escalated D2: SOURCE CONFLICT PRD vs data-model on field optionality (user resolved: required)
Group 5: PASS (1 cycle)
Intentional deviations: 1 (Group 4 — field renamed per user decision 2026-04-10, source doc stale)
-->
```
</verification_audit_trail>

<success_criteria>
The skill is working when:

- Each story section group is verified against its source documents before the next group is written
- Deviations are caught and fixed at the section where they originate, not discovered downstream
- The fix-verify loop converges within 3 cycles (if it consistently hits the cap, the source document mapping or excerpt selection needs improvement)
- The final story spec, after all sections pass verification, has zero source-document contradictions
- Source conflicts between documents are surfaced and escalated, not silently resolved by the author
- The verification audit trail shows a clear record of what was checked and what was fixed
</success_criteria>

<reference_index>
Verifier prompt templates: `templates/verification-prompt.md`
</reference_index>
