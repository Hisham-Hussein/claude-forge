<required_reading>

Read the stage file for each stage as you reach it (progressive loading):

| Stage | File | References Loaded |
|-------|------|-------------------|
| 0 | stages/stage-0-context-detection.md | (none — reads PRD directly) |
| 1 | stages/stage-1-design-plan.md | visual-hierarchy, interaction-patterns |
| 2 | stages/stage-2-flows.md | nielsen-heuristics |
| 3 | stages/stage-3-layouts.md | responsive-patterns |
| 4 | stages/stage-4-components.md | atomic-design, data-states |
| 5 | stages/stage-5-interactions.md | interaction-patterns, responsive-patterns, data-states |
| 6 | stages/stage-6-accessibility.md | accessibility-wcag |

Also read the output template when generating documents: `templates/ux-design-plan-template.md`

**Do NOT load all references upfront.** Load only what each stage needs.

</required_reading>

<inputs>

**Required:** Story Map (`.charter/STORY-MAP.md` or path provided by user)
**Optional:** User Stories with AC (`.charter/USER-STORIES.md` or path provided by user)

If no story map path is provided, check `.charter/STORY-MAP.md` first. If neither exists, ask the user.

If user stories exist but weren't specified, ask: "I found `.charter/USER-STORIES.md` — should I use it to enrich the plan with acceptance criteria detail?"

</inputs>

<resume_check>

## Resume Detection

Before starting, check for `.charter/UX-GENERATION-STATUS.md`:

**If exists:**
1. Read the manifest
2. Identify the last incomplete document (first with status != `verified` / `user-approved` / `skipped`)
3. Re-read all prior verified documents from disk
4. Re-read the constraint manifest from disk
5. Continue the pipeline from that stage

**If not exists:** Start from Phase 0.

**On context reset mid-verification:** The manifest records which `verification_loop` iteration was active, so the verification picks up where it left off.

Tell the user: "Resuming pipeline from **[document name]** (Stage [N]). Prior documents: [list verified docs]."

</resume_check>

<process>

<phase name="0-context-detection">

## Phase 0: Context Detection

Read and follow `stages/stage-0-context-detection.md`.

This produces:
- `.charter/UX-CONSTRAINTS.md` (platform constraint manifest)
- `.charter/UX-GENERATION-STATUS.md` (pipeline state)
- Confirmed scope (MVP or specific slice)

**Do not proceed to Stage 1 until Phase 0 is complete.**

</phase>

<pipeline_cycle>

## Pipeline: Stages 1-6

Execute each stage in order. For each stage:

### Step A: Load the Stage

Read the stage file from `stages/stage-N-*.md`. Load ONLY the references listed in that stage file.

### Step B: Re-Read All Inputs From Disk

**This is mandatory every stage — do not rely on conversation context.**

1. Re-read the **story map** from disk
2. Re-read the **constraint manifest** from disk
3. Re-read ALL **previously verified documents** from disk

Why: Fresh reads prevent context attention decay. The documents on disk are the source of truth.

### Step C: Query Context7 (if constrained platform)

Run the stage-specific Context7 query from the stage file. Append findings to the constraint manifest.

### Step D: Generate the Document

Follow the generation instructions in the stage file. Write the output to `.charter/`.

Update the generation status manifest: set document status to `generating`.

### Step E: Verification (Fresh Subagent)

Dispatch a **fresh subagent** using the Agent tool:

```
Agent tool parameters:
  description: "Verify [document name]"
  prompt: |
    You are a UX document verification agent. Read ALL files from disk — do not trust any content from conversation context.

    ## Files to Read
    - Generated document: .charter/[document].md
    - Previously verified documents: [list paths]
    - Constraint manifest: .charter/UX-CONSTRAINTS.md
    - Story map: [path]
    - Verification workflow: [skill path]/workflows/verify-ux-consistency.md (for check procedures)

    ## Run These 4 Verification Dimensions

    ### 1. Input Fidelity
    - Does the document faithfully reflect the story map?
    - Are all in-scope activities accounted for?
    - Were any requirements invented (not traceable to SM-XXX)?

    ### 2. Internal Consistency
    - Are terms consistent within the document?
    - Do cross-references resolve?
    - Are there contradictions?

    ### 3. Cross-Document Consistency
    Run the named checks from verify-ux-consistency.md that apply to this document:
    - Stage 1: `story-id-consistency`
    - Stage 2: `story-id-consistency`, `flow-diagram-coverage`
    - Stage 3: `page-name-consistency`, `navigation-table-completeness`, `button-label-consistency`
    - Stage 4: `button-target-consistency`, `component-pattern-assignment`, `status-value-consistency`, `empty-state-coverage`
    - Stage 5: `status-value-consistency`, `cross-reference-validity`
    - Stage 6: (none — final sweep covers all checks)

    For each check: follow the exact procedure in verify-ux-consistency.md, report findings with severity ratings (1-4).

    ### 4. Platform Feasibility
    [If constrained platform] Query Context7 for anything that looks potentially infeasible. Report specific concerns.

    ## Output Format
    Report as:
    - PASS: All dimensions clean
    - FAIL: List each finding with severity, location, and suggested fix
```

Update the generation status manifest: set document status to `verifying`, increment `verification_loop`.

### Step F: Handle Verification Result

**If PASS:** Proceed to Step G.

**If FAIL:** Enter fix-and-recheck loop:

1. Review subagent findings
2. Edit the document to fix severity 3+ issues
3. Re-dispatch verification subagent (fresh — reads from disk again)
4. **Maximum 3 loops.** Track loop count in generation status manifest.

**After 3 loops with remaining issues:**
- Present remaining findings to the user alongside the document
- User decides: **accept as-is**, **request specific edits**, or **regenerate from scratch**
- If user requests edits → edit → re-verify (loop counter resets)
- If user requests regeneration → re-run the stage from Step D

### Step G: User Gate or Auto-Advance

**Stages 1-3 (DESIGN-PLAN, FLOWS, LAYOUTS) — User approval required:**
- Present the document to the user
- Wait for approval
- If user requests edits → edit the document → re-run verification (Step E) → present again
- Pipeline advances ONLY on user approval

**Stages 4-6 (COMPONENTS, INTERACTIONS, ACCESSIBILITY) — Auto-advance:**
- Verification passed → proceed to next stage
- After all three complete (or Stage 5 if accessibility is skipped), present documents 4-6 together for user review

### Step H: Update Status Manifest

Update `.charter/UX-GENERATION-STATUS.md`:
- Set document status to `verified` (or `user-approved` for stages 1-3)
- Record `checks_passed` and `checks_total`
- For stages 1-3, record `user_approved: true`

</pipeline_cycle>

<final_sweep>

## Final Cross-Document Sweep

After all stages complete:

1. Dispatch a **fresh subagent** to run ALL 10 checks from `workflows/verify-ux-consistency.md` across all documents
2. The subagent reads everything from disk
3. Auto-fix severity 3+ issues where the correct value can be determined mechanically
4. Report the verification summary

Present documents 4-6 (if not already presented) and any remaining findings to the user.

**Report to user:**
- Files written and their locations
- Number of components specified
- Number of pages/views in IA
- Traceability coverage (% of story map activities with UX elements)
- Verification summary per document
- Any remaining issues requiring manual attention

</final_sweep>

</process>

<anti_patterns>

- **Template-filling without analysis**: Mechanically filling sections without adapting to the project's needs. Every section must derive from the story map.
- **Over-specification**: Prescribing CSS classes, framework-specific patterns, or implementation details. The plan is technology-agnostic (unless constrained platform dictates specific patterns).
- **Under-specification**: Leaving states undefined, saying "standard behavior" without defining it. If a developer would have to guess, specify it.
- **Design system leakage**: Including colors, fonts, or pixel values. Use role-based names and emphasis levels only.
- **Missing traceability**: UX elements that don't trace to any SM-XXX or US-XXX requirement.
- **Desktop-first bias**: Specifying desktop layout in detail, leaving mobile as "it stacks." Mobile is the base tier.
- **Accessibility as appendix**: Treating accessibility as a separate section rather than per-component inline specs (in UX-COMPONENTS.md). UX-ACCESSIBILITY.md deepens but does not replace inline specs.
- **Invented requirements**: Adding UX elements not backed by any story map activity. If the element is needed, flag the story map gap.
- **Default-only components**: Specifying only the happy/loaded state. Every interactive component needs all applicable states.
- **Happy-path-only flows**: User flows that only cover the success path. Error recovery and decision branches are required.
- **Skipping disk re-reads**: Relying on conversation context instead of fresh disk reads. Context decays; disk is truth.
- **Self-verifying**: Running verification in the same context that generated the document. Always use a fresh subagent.

</anti_patterns>

<success_criteria>

The pipeline is complete when:

- [ ] Phase 0 produced constraint manifest and generation status manifest
- [ ] All 6 documents (or 5 if accessibility skipped) are generated and verified
- [ ] Each document passed verification (4 dimensions) with no severity 3+ issues remaining
- [ ] Documents 1-3 received user approval
- [ ] Documents 4-6 were presented to user for review
- [ ] Final cross-document sweep (all 10 checks) passed
- [ ] Every component has all applicable states documented
- [ ] Visual hierarchy uses role-based + semantic naming (no pixel values, no colors)
- [ ] Every UX decision traces to SM-XXX or US-XXX
- [ ] Responsive behavior is explicit for all tiers
- [ ] Accessibility requirements are inline with each component spec
- [ ] Data states defined with exact microcopy for all dynamic components
- [ ] Generation status manifest shows all documents as verified/approved
- [ ] A coding agent reading the output + a design system can implement without guesswork

</success_criteria>
