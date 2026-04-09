<required_reading>

**Read these reference files NOW before running the review:**

1. references/nielsen-heuristics.md — 50-question quality gate and severity scale
2. references/atomic-design.md — state applicability matrix (which states each component type requires)
3. references/accessibility-wcag.md — per-component accessibility validation checklist
4. references/responsive-patterns.md — breakpoint validation checklist
5. references/data-states.md — loading/empty/error/success patterns + microcopy requirements
6. references/interaction-patterns.md — filter specification checklist, feedback model rules
7. references/visual-hierarchy.md — type role taxonomy, emphasis model validation

Also read the output template: templates/ux-compliance-report-template.md

</required_reading>

<objective>

Audit UX plan documents for completeness, consistency, and quality — then optionally audit implementation against the plan. Produces a structured compliance report with severity-rated findings and specific remediation recommendations.

**Two review modes:**

| Mode | When to Use | Inputs | Audits |
|------|-------------|--------|--------|
| **Plan Quality Review** | UX plan exists, no implementation yet | UX plan files + story map | Plan completeness, traceability, consistency, Nielsen's heuristics, state coverage, microcopy specificity |
| **Implementation Compliance Review** | Implementation exists | UX plan files + story map + implementation (code, screenshots, or live app) | Everything in Plan Quality + per-page implementation match, missing states, behavioral deviations |

</objective>

<inputs>

**Required:**
- UX plan files (`.charter/UX-DESIGN-PLAN.md` and any split files: `UX-LAYOUTS.md`, `UX-COMPONENTS.md`, `UX-INTERACTIONS.md`, `UX-FLOWS.md`, `UX-ACCESSIBILITY.md`)
- Story map (`.charter/STORY-MAP.md` or path provided by user)

**Optional:**
- User Stories with AC (`.charter/USER-STORIES.md` or path provided by user)
- PRD (for FR-level traceability)
- Implementation artifacts (code files, screenshots, live URL) — triggers Implementation Compliance mode

If UX plan files are not found at default paths, ask the user for locations.

If no implementation artifacts are provided, run in **Plan Quality Review** mode.

</inputs>

<process>

<phase name="1-gather-and-index">

## Phase 1: Gather & Index

### Step 1: Locate UX Plan Files

Search for UX plan files. Catalog what exists:

```
.charter/
  UX-DESIGN-PLAN.md    — Sections 1-3 (overview, IA, hierarchy)
  UX-LAYOUTS.md         — Section 4 (page layouts)
  UX-COMPONENTS.md      — Section 5 (component specs)
  UX-INTERACTIONS.md    — Sections 6-8 (interactions, responsive, data states)
  UX-ACCESSIBILITY.md   — Section 9 (accessibility)
  UX-FLOWS.md           — Sections 10-11 (user flows, traceability)
```

If a single `UX-DESIGN-PLAN.md` contains all sections, use that. If split, read all files.

Flag any missing files immediately — a missing file is a severity-4 finding.

### Step 2: Read Story Map

Read the story map. Extract:
- All backbone activities
- All MVP stories (SM-XXX IDs and descriptions)
- Release slice boundaries
- Personas

This becomes the **source of truth** for traceability verification.

### Step 3: Read PRD (if available)

If a PRD exists, extract functional requirements (FR-XXX) for deeper traceability verification (SM-XXX → FR-XXX → UX element chain).

### Step 4: Determine Review Mode

- **If implementation artifacts provided:** Run full review (Plan Quality + Implementation Compliance)
- **If no implementation:** Run Plan Quality Review only
- **Ask the user** if unclear: "Should I review the UX plan documents for quality, or also audit an implementation against the plan?"

### Step 5: Build Audit Index

Create an internal index of everything to audit:

| Item | Count | Source |
|------|-------|--------|
| Pages in IA | [N] | UX-DESIGN-PLAN.md Section 2 |
| Page layouts | [N] | UX-LAYOUTS.md |
| Component patterns | [N] | UX-COMPONENTS.md |
| Interaction patterns | [N] | UX-INTERACTIONS.md |
| Data state specs | [N] | UX-INTERACTIONS.md Section 8 |
| User flows | [N] | UX-FLOWS.md Section 10 |
| Traceability entries | [N] | UX-FLOWS.md Section 11 |
| Story map stories in scope | [N] | STORY-MAP.md |

Flag count mismatches early: if IA lists 30 pages but layouts only cover 25, that's already a finding.

</phase>

<phase name="2-structural-completeness">

## Phase 2: Structural Completeness Audit

### Step 6: Section Presence Check

Verify all required sections exist. Use this checklist:

| # | Section | Expected In | Required Content |
|---|---------|-------------|------------------|
| 1 | Overview & Design Principles | UX-DESIGN-PLAN.md | Product summary + 3-5 guiding principles |
| 2 | Information Architecture | UX-DESIGN-PLAN.md | Page inventory table + navigation model + content hierarchy |
| 3 | Visual Hierarchy Map | UX-DESIGN-PLAN.md | Hierarchy table with role + emphasis per element + scanning pattern per page type |
| 4 | Page Layouts | UX-LAYOUTS.md | Text wireframe per page + content priority |
| 5 | Component Specifications | UX-COMPONENTS.md | Component patterns with state tables |
| 6 | Interaction Patterns | UX-INTERACTIONS.md | State machines, filter specs, button specs |
| 7 | Responsive Behavior | UX-INTERACTIONS.md | Per-tier behavior for relevant components |
| 8 | Data States | UX-INTERACTIONS.md | Loading/empty/error/success per dynamic component |
| 9 | Accessibility | UX-FLOWS.md or UX-ACCESSIBILITY.md | Global requirements + per-component notes |
| 10 | User Flows | UX-FLOWS.md | Step-by-step flows with decision branches and error recovery |
| 11 | Traceability Matrix | UX-FLOWS.md | Story → UX element mapping + coverage summary + Nielsen's validation |

**Severity:** Missing section = severity 4 (catastrophic). Section present but incomplete = severity 2-3 depending on what's missing.

### Step 7: Placeholder Detection

Scan every section for:
- Template placeholder text: `[bracketed placeholders]`, `TODO`, `TBD`, `...`, `etc.`
- Generic descriptions that don't specify behavior: "standard behavior", "appropriate feedback", "show an error", "handle gracefully"
- Empty tables or table rows with placeholder values

**The meta-test (from nielsen-heuristics reference):** For every interaction and state, ask: "If a developer reads ONLY this spec, would they know exactly what to build?" If the answer is "they'd have to guess about X," that's a finding.

**Severity:** Placeholder in critical path (primary interaction, error state) = severity 3. Placeholder in secondary element = severity 2. Placeholder in metadata/reference = severity 1.

### Step 8: Page Coverage Audit

Cross-reference three lists:

| Source | What to Check |
|--------|--------------|
| IA page inventory (Section 2) | Every page listed → has a layout in Section 4 |
| Layouts (Section 4) | Every layout → maps to a page in the IA inventory |
| Components (Section 5) | Every component pattern → used by at least one page |

**Finding types:**
- Page in IA but no layout = severity 3 (can't build it)
- Layout exists but not in IA = severity 2 (orphan layout — remove or add to IA)
- Component pattern not used by any page = severity 1 (dead spec — remove)

</phase>

<phase name="3-traceability-verification">

## Phase 3: Traceability Verification

### Step 9: Forward Traceability (Stories → UX)

For every story in the story map's MVP scope:

1. Look up SM-XXX in the traceability matrix
2. Verify it maps to at least one UX element
3. Verify the referenced UX element actually exists in the plan

**Finding types:**
- Story has no UX element = severity 3 (feature with no UI — either missing from plan or intentionally backend-only; verify)
- Story references a UX element that doesn't exist = severity 3 (broken reference)
- Story references a page that's not in the IA = severity 4 (structural inconsistency)

### Step 10: Backward Traceability (UX → Stories)

For every UX element in the plan:

1. Verify it traces to at least one SM-XXX or US-XXX
2. Verify the referenced story actually exists in the story map

**Finding types:**
- UX element with no story source = severity 2 (invented requirement — either remove or flag story map gap)
- UX element references non-existent story = severity 2 (broken reference)

### Step 11: Cross-Document Reference Integrity

Verify all cross-references between documents are valid:

- Every "Go to PG-XXX →" button references a real page
- Every "links to PG-XXX" note references a real page
- Every component pattern referenced in layouts exists in UX-COMPONENTS
- Every interaction referenced in flows exists in UX-INTERACTIONS
- Navigation model entry/exit points reference real pages

**Severity:** Broken cross-reference = severity 2 (confusing but not blocking). Broken navigation flow = severity 3 (workflow gap).

</phase>

<phase name="4-consistency-audit">

## Phase 4: Consistency Audit

### Step 12: Terminology Consistency

Scan all documents for terminology drift — the same concept referred to by different names:

**Check these categories:**

| Category | Common Drift | How to Verify |
|----------|-------------|---------------|
| Status names | "Draft" vs "Drafted" vs "New" | Extract all status values, verify identical across all documents |
| Page names | "Draft Review Queue" vs "Review Queue" vs "Draft Queue" | Compare IA inventory names to layout titles to flow references |
| Button labels | "Approve" vs "Mark as Approved" vs "Submit Approval" | Extract all button specs, verify consistent per action type |
| Field names | "Voice Check" vs "Voice Check Status" vs "Voice DNA Check" | Verify same field named identically everywhere it appears |
| Persona references | "Domain Expert" vs "Expert" vs "User" vs "Tenant Admin" | Verify consistent persona terminology |
| Component names | Pattern names used consistently in layouts, interactions, flows | Cross-reference all pattern references |

**Severity:** Inconsistent status names = severity 3 (developers will implement different values). Inconsistent page names = severity 2 (confusing but resolvable). Minor wording variation = severity 1.

### Step 13: Status Pipeline Consistency

If the plan defines a status pipeline (e.g., content status, recommendation status):

1. Extract every status value and its definition
2. Verify the state machine covers all transitions (no dead-end states, no orphan states)
3. Verify every page that displays status uses the same values
4. Verify every button that changes status targets a valid status value
5. Verify color assignments are consistent across all documents

**Severity:** Dead-end state in pipeline = severity 3. Missing transition = severity 3. Inconsistent color = severity 2.

### Step 14: Navigation Consistency

1. Extract all navigation buttons and their targets
2. Verify bidirectional navigation: if Page A links to Page B, can the user get back?
3. Verify entry points in user flows match the navigation model
4. Check for navigation dead-ends: pages with no exit navigation
5. Verify "workflow continuation" links form complete chains (e.g., Planning → Production → Engagement)

**Severity:** Navigation dead-end = severity 3. One-way navigation where bidirectional expected = severity 2.

</phase>

<phase name="5-nielsen-heuristic-gate">

## Phase 5: Nielsen's Heuristic Quality Gate

### Step 15: First Pass — Overall Impressions

Read the entire UX plan end-to-end. Note:
- Which heuristics seem well-addressed
- Which heuristics seem absent or weak
- Overall impression of spec completeness
- Areas where a developer would have to guess

### Step 16: Second Pass — 50-Question Checklist

Run the full 50-question checklist from `references/nielsen-heuristics.md`.

For each question, record:
- **Question number** (H1.1 through H10.50)
- **Status**: Pass / Fail / Partial / N/A
- **Evidence**: Specific section reference where the heuristic is addressed (or should be)
- **Severity** (if Fail/Partial): 1-4 per severity scale
- **Remediation**: Specific fix recommendation

**Minimum pass threshold:** No severity 3+ findings. Severity 1-2 findings are reported but don't block.

### Step 17: Cross-Heuristic Consistency Checks

Run these mandatory cross-checks:

| Check | What to Verify | Typical Gap |
|-------|---------------|-------------|
| H1 + H9 | Every error state includes BOTH a status indication AND an error message with recovery action | Status badge exists but no error text, or vice versa |
| H3 + H6 | Every escape/undo/reset mechanism is visually discoverable (has a button/link), not just functionally available | Filter reset is mentioned in interaction spec but no visible button in layout |
| H4 + H2 | Consistent terminology is also domain-appropriate (not internal jargon) | Consistent use of "context assembly" which is engine-internal, not user-facing |
| H5 + H9 | Prevention and recovery cover the SAME error types | Form validation prevents empty submission (H5) but no error message spec if validation fails (H9) |
| H1 + H7 | System status is visible without extra interaction | Status visible but only after clicking into a detail view |
| H6 + H10 | Recognition aids (visible labels, states) align with help/documentation guidance | Help text references features user can't see on current page |

**Severity:** Cross-heuristic gap = severity 3 (systematic issue affecting multiple interactions).

</phase>

<phase name="6-state-completeness">

## Phase 6: Component & State Completeness Audit

### Step 18: Component State Coverage

For each component pattern in the plan, apply the state applicability matrix from `references/atomic-design.md`:

**For every component, verify these states are documented where applicable:**

| State | Applicable When | Check |
|-------|----------------|-------|
| Default/Loaded | Always | Is the normal appearance and behavior described? |
| Empty — first use | Component displays data | Is first-use empty state specified with headline + body + CTA? |
| Empty — no results | Component is filterable | Is no-results state specified? |
| Empty — no data in range | Component has time filter | Is no-data-in-range specified? |
| Loading | Component fetches data | Is loading indicator specified (skeleton/spinner/none per duration)? |
| Error | Component can fail | Is error state specified with what + why + recovery action? |
| Success | Component completes actions | Is success feedback specified and proportional to action significance? |
| Partial | Component has multiple data sources | Is partial failure strategy specified (degrade vs. error)? |
| Disabled | Component can be conditionally unavailable | Is disabled state + reason specified? |

**How to count:** For each component, count applicable states and documented states. Report as ratio.

**Severity:** Primary interaction missing a state (e.g., draft review queue with no error state) = severity 3. Secondary component missing a state = severity 2. Metadata component missing a state = severity 1.

### Step 19: Microcopy Specificity Audit

For every data state that requires user-facing text, verify:

1. **Headline** is exact text (not "show appropriate headline")
2. **Body** is exact text (not "explain the error")
3. **CTA label** is exact text (not "provide an action button")
4. **Error messages** follow the three-part formula: what happened + why + what to do
5. **Empty states** use correct type: first-use vs. no-data vs. no-results vs. user-cleared
6. **Success feedback** is scaled appropriately: routine=none, standard=toast, important=banner

**The test:** Could a developer copy this microcopy directly into the implementation? If they'd have to write their own copy, it's a finding.

**Severity:** Missing microcopy on error state = severity 3 (developers write terrible error messages). Missing microcopy on empty state = severity 2. Missing microcopy on success state = severity 1.

### Step 20: Button Automation Completeness

For every button in the plan:

1. **Trigger** specified (what user action activates it)
2. **Automation** specified (what the system does)
3. **Result** specified (what changes in the UI)
4. **Error handling** specified (what happens if the automation fails)
5. **Confirmation** specified where needed (destructive actions guarded)

**Severity:** Button with no automation spec = severity 3 (developer doesn't know what it does). Button with automation but no error handling = severity 2.

</phase>

<phase name="7-interaction-flow-audit">

## Phase 7: Interaction & Flow Audit

### Step 21: State Machine Completeness

For every state machine diagram in the plan:

1. Verify every state has at least one outgoing transition (no dead-ends except terminal states)
2. Verify every state has at least one incoming transition (no orphan states except initial state)
3. Verify transition triggers are specific (not "user acts" but "user clicks Approve button")
4. Verify error/failure transitions exist alongside happy-path transitions
5. Verify the initial and terminal states are clearly marked

**Severity:** Dead-end non-terminal state = severity 3. Missing error transition = severity 2.

### Step 22: User Flow Completeness

For every user flow:

1. **Entry point** specified
2. **Steps** are specific actions (not "user does the thing")
3. **Decision points** have all branches documented (not just the happy path)
4. **Error recovery paths** exist for every step that can fail
5. **Exit point** specified
6. **Flow diagram** exists for complex branching flows (Mermaid or equivalent)

**The test:** Could someone unfamiliar with the product execute this flow by reading the spec? If they'd get stuck at any point, it's a finding.

**Severity:** Flow with no error recovery = severity 3. Flow with no decision branches = severity 2. Flow without diagram when complex = severity 1.

### Step 23: Filter Specification Completeness

For every filter interaction in the plan, verify against the filter specification checklist from `references/interaction-patterns.md`:

1. [ ] Placement specified (sidebar, top bar, chips, dropdown)
2. [ ] Application method specified (interactive, batch, hybrid)
3. [ ] Multi-select behavior specified (single vs. multi per facet)
4. [ ] Boolean logic specified (AND between facets, OR within)
5. [ ] Clear/reset mechanism specified (per-filter + global)
6. [ ] No-results handling specified with exact microcopy
7. [ ] Default value specified
8. [ ] Cross-page persistence behavior specified

**Severity:** Missing filter spec items = severity 2 per item. No-results handling missing = severity 3.

</phase>

<phase name="8-platform-compliance">

## Phase 8: Platform Compliance Audit

### Step 24: Platform Feasibility Check

If the plan specifies a target platform (e.g., Airtable Interfaces, specific framework, design system):

1. Verify each specified interaction is feasible on the platform
2. Flag interactions that require workarounds or may not be possible
3. Verify page types match platform capabilities
4. Check that assumed capabilities (conditional visibility, linked records, automation triggers) are real

**This phase requires platform knowledge.** If the reviewer doesn't have platform expertise, flag this phase as "not reviewed" rather than guessing.

**Severity:** Infeasible interaction spec'd as standard = severity 3. Feasible but requires non-obvious workaround = severity 2.

### Step 25: Responsive & Accessibility Platform Assessment

1. If platform handles responsive natively: verify the plan acknowledges this and specifies any exceptions
2. If platform handles accessibility natively: verify the plan acknowledges this and specifies any custom considerations
3. If platform does NOT handle these natively: verify full responsive and accessibility specs exist per reference file requirements

**Severity:** Custom frontend with no responsive specs = severity 4. Platform-native responsive with no exception notes = severity 1.

</phase>

<phase name="9-implementation-compliance">

## Phase 9: Implementation Compliance Audit

**Skip this phase if running in Plan Quality Review mode (no implementation provided).**

### Step 26: Page Existence Check

For every page in the IA:
1. Does the page exist in the implementation?
2. Does the page title match the spec?
3. Is the page reachable via the specified navigation model?

### Step 27: Component Implementation Check

For every component pattern:
1. Do the specified elements exist on the page?
2. Are they in the specified order/position?
3. Are the specified fields/columns present?

### Step 28: State Implementation Check

For every specified state per component:
1. Can the state be triggered?
2. Does the visual treatment match the spec?
3. Does the behavior match the spec?
4. Is the microcopy exact?

### Step 29: Interaction Implementation Check

For every button/interaction:
1. Does the button exist with the specified label?
2. Does clicking it trigger the specified automation?
3. Does the result match the spec?
4. Are error cases handled as specified?

### Step 30: Data State Implementation Check

For every data-dependent component:
1. Is loading state implemented?
2. Is empty state implemented with correct microcopy?
3. Is error state implemented with three-part message?
4. Is success feedback implemented at correct intensity?

**Severity for all implementation findings:** Deviation from spec in primary interaction = severity 3. Deviation in secondary element = severity 2. Minor visual difference = severity 1.

</phase>

<phase name="10-generate-report">

## Phase 10: Generate Compliance Report

### Step 31: Compile Findings

Aggregate all findings from Phases 2-9. For each finding:

| Field | Content |
|-------|---------|
| Finding ID | Sequential (F-001, F-002, ...) |
| Phase | Which audit phase caught it |
| Severity | 1-4 per severity scale |
| Category | Completeness / Traceability / Consistency / Heuristic / State / Flow / Platform / Implementation |
| Location | Specific file, section, and element |
| Description | What's wrong (specific, not vague) |
| Evidence | What the spec says vs. what's expected/found |
| Remediation | Specific fix (not "fix this") |

### Step 32: Calculate Summary Statistics

| Metric | Value |
|--------|-------|
| Total findings | [N] |
| Severity 4 (catastrophic) | [N] — **blocks approval** |
| Severity 3 (major) | [N] — **must fix** |
| Severity 2 (minor) | [N] — fix if in scope |
| Severity 1 (cosmetic) | [N] — note for future |
| Traceability coverage | [N]% stories with UX elements |
| State completeness ratio | [N]% applicable states documented |
| Microcopy specificity | [N]% data states with exact text |
| Nielsen's heuristics | [N]/10 pass, [N] warn, [N] fail |

### Step 33: Determine Verdict

| Verdict | Criteria |
|---------|----------|
| **PASS** | Zero severity 3+ findings. Traceability >= 95%. State completeness >= 90%. |
| **PASS WITH NOTES** | Zero severity 4. Severity 3 count <= 3 and all have clear remediation. Traceability >= 90%. |
| **FAIL — REVISE** | Any severity 4, OR severity 3 count > 3, OR traceability < 90%, OR Nielsen's heuristic with severity 4 gap |

### Step 34: Write Report

Write the compliance report to the project directory. Use the template from `templates/ux-compliance-report-template.md`.

**Default output location:** `.charter/UX-COMPLIANCE-REPORT.md`

If a previous report exists, ask the user: "A previous compliance report exists. Should I overwrite it or create a dated version (e.g., `UX-COMPLIANCE-REPORT-2026-04-09.md`)?"

Report to user:
- Verdict (PASS / PASS WITH NOTES / FAIL)
- Finding count by severity
- Top 3 most critical findings with remediation
- Summary statistics
- Link to full report

</phase>

</process>

<anti_patterns>

- **Rubber-stamp review**: Scanning quickly and declaring "looks good" without running the checklists. Every phase exists for a reason — run them all.
- **Severity inflation**: Rating every minor wording inconsistency as severity 3. Use the severity scale precisely: severity 3 means a developer would build the wrong thing, not that a word could be better.
- **Severity deflation**: Rating missing error states as severity 1 to make the report look clean. Missing error states are severity 3 — developers don't write good error handling without specs.
- **Missing remediation**: Findings without specific fixes are useless. "Fix the empty state" is not remediation. "Add first-use empty state to PG-015: Headline 'No drafts to review' / Body 'Content drafts appear here after you generate a weekly plan.' / CTA 'Go to Planning Hub →'" is remediation.
- **Ignoring platform context**: Flagging "no responsive spec for mobile" when the platform handles it natively. Understand the platform before auditing.
- **Auditing style, not substance**: Criticizing sentence structure in microcopy instead of checking whether the microcopy exists at all and covers the right states.
- **Happy-path-only review**: Only checking that the happy path is specified. The value of this review is catching missing error paths, edge cases, and failure states.
- **Single-pass shortcuts**: Skipping the Nielsen two-pass validation. The first pass catches big-picture gaps; the second pass catches specific omissions. Both are required.
- **Overlooking cross-document drift**: Checking each document in isolation without cross-referencing. The most insidious bugs come from documents that individually look correct but contradict each other.

</anti_patterns>

<success_criteria>

The compliance review is complete when:

- [ ] All 10 phases executed (Phase 9 skipped if no implementation)
- [ ] Every page in the IA has been audited for layout presence
- [ ] Every component pattern has been audited for state completeness
- [ ] Full traceability verification run (forward AND backward)
- [ ] All cross-document references verified
- [ ] Terminology consistency checked across ALL documents
- [ ] Nielsen's 50-question checklist completed with severity ratings
- [ ] Cross-heuristic consistency checks run
- [ ] Every finding has a severity, evidence, and specific remediation
- [ ] Summary statistics calculated
- [ ] Verdict determined per criteria
- [ ] Report written to `.charter/UX-COMPLIANCE-REPORT.md`
- [ ] Top findings communicated to user

</success_criteria>
