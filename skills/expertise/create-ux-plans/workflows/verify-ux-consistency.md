<objective>

Lightweight cross-document consistency verification that runs after `create-ux-plan.md` writes its output files. Catches internal inconsistencies between the split UX plan documents — the class of errors where one file says X and another says Y.

This is NOT the full compliance review (`review-ux-compliance.md`). It is a fast, mechanical cross-referencing pass that catches the most common post-creation inconsistencies. It produces a short pass/fail report and auto-fixes what it can.

**When to run:** Automatically after Step 16 of `create-ux-plan.md`, or manually when UX files have been edited.

</objective>

<inputs>

The UX plan files — either a single `UX-DESIGN-PLAN.md` or the split set:

```
.charter/
  UX-DESIGN-PLAN.md    — Sections 1-3
  UX-LAYOUTS.md         — Section 4
  UX-COMPONENTS.md      — Section 5
  UX-INTERACTIONS.md    — Sections 6-8
  UX-FLOWS.md           — Sections 10-11
```

Also read the story map (`.charter/STORY-MAP.md`) for story ID verification.

If any files are missing, report which and skip checks that depend on them.

</inputs>

<process>

Read all UX plan files and the story map. Run all 10 checks below. For each check, collect findings with severity ratings (using the same 1-4 scale as the compliance review). After all checks, report results and auto-fix severity 3+ issues where the correct value can be determined mechanically.

<check name="1-page-name-consistency">

## Check 1: Page Name Consistency

**Cross-reference:** IA inventory page names (UX-DESIGN-PLAN.md Section 2) vs. layout page titles (UX-LAYOUTS.md `PAGE TITLE:` lines).

**Procedure:**
1. Extract every page ID, page name from the IA inventory table
2. Extract every page ID, page title from layout wireframes
3. Compare: do they match?

**Acceptable variations:** Layout title may be a more descriptive display version (e.g., IA "Performance Snapshot" vs. layout "This Week's Performance Snapshot"). Flag only when the names are semantically different (e.g., "Bi-weekly Insights" vs. "Performance Insights").

**Severity:** Semantically different names = 3. Minor variation = 1.

**Auto-fix:** Update the layout title to match the IA name, unless the layout title is clearly a better display name (in which case, update the IA name).

</check>

<check name="2-navigation-table-completeness">

## Check 2: Navigation Table Completeness

**Cross-reference:** Cross-Interface navigation table (UX-DESIGN-PLAN.md Section 2) vs. navigation buttons in layouts (UX-LAYOUTS.md) vs. navigation button specs (UX-COMPONENTS.md).

**Procedure:**
1. Extract every navigation button from all layouts (buttons containing "→" or "Go to" that link to another page)
2. Extract every entry from the cross-Interface navigation table
3. Extract every entry from the navigation buttons table in UX-COMPONENTS.md
4. For each layout button: verify it appears in the navigation table (for cross-Interface links) AND in the components button spec
5. For each navigation table entry: verify the button exists in the corresponding layout

**Severity:** Button in layout but not in nav table or components = 2. Entry in nav table but not in layout = 3 (phantom button).

**Auto-fix:** Add missing entries to the navigation table and/or components button spec, copying label and target from the layout.

</check>

<check name="3-button-label-consistency">

## Check 3: Button Label Consistency

**Cross-reference:** Button labels across all documents.

**Procedure:**
1. For each button that appears in multiple documents (nav table, layouts, components, flows), extract its label from each
2. Compare: are labels identical?
3. Check for systematic patterns (e.g., arrow suffix "→" present in some docs but not others)

**Severity:** Different label for same action = 3. Systematic formatting difference (arrow suffix) = 1.

**Auto-fix:** Standardize to the label used in UX-LAYOUTS.md (the wireframe is the source of truth for button text). Update nav table and components to match.

</check>

<check name="4-button-target-consistency">

## Check 4: Button Target Consistency

**Cross-reference:** Button targets (destination pages) across documents.

**Procedure:**
1. For each navigation button, extract its target page from: nav table, layouts, components, flows
2. Compare: do all documents agree on where the button navigates?

**Severity:** Different target pages = 3 (critical — developer builds wrong navigation).

**Auto-fix:** Use the target specified in UX-COMPONENTS.md button automation spec (most authoritative for behavior). Update nav table to match.

</check>

<check name="5-component-pattern-assignment">

## Check 5: Component Pattern Assignment

**Cross-reference:** IA page inventory (page types) vs. component pattern "Used in" lists (UX-COMPONENTS.md).

**Procedure:**
1. Extract every page and its page type from the IA inventory
2. Extract every component pattern and its "Used in" list from UX-COMPONENTS.md
3. Verify every page is listed in at least one pattern's "Used in"

**Severity:** Page not in any pattern = 3 (no component spec for that page).

**Auto-fix:** Assign unmatched pages to the closest pattern based on page type (List → Review Queue or Data Management variant; Dashboard → Dashboard pattern; etc.). Add to the pattern's "Used in" list.

</check>

<check name="6-status-value-consistency">

## Check 6: Status Value Consistency

**Cross-reference:** Status values in state machines (UX-INTERACTIONS.md) vs. field specifications (UX-LAYOUTS.md) vs. Status Color System (UX-DESIGN-PLAN.md Section 3).

**Procedure:**
1. Extract every state from every state machine diagram in UX-INTERACTIONS.md
2. Extract every status field's allowed values from UX-LAYOUTS.md field specifications
3. Extract every status and color from the Status Color System
4. Cross-compare:
   - Every state machine state should appear in the corresponding field spec
   - Every status value that appears on a page should have a color in the Status Color System
   - Status filter defaults should only reference values that exist in the relevant pipeline

**Severity:** State machine state missing from field spec = 3. Status value with no color = 2. Filter references non-existent status = 3.

**Auto-fix:** Add missing values to field specs. Add missing colors to the Status Color System (using reasonable defaults: new processing states = Blue, new completion states = Green, new error states = Red).

</check>

<check name="7-empty-state-coverage">

## Check 7: Empty State Coverage

**Cross-reference:** Pages that display dynamic data vs. per-page empty state table (UX-COMPONENTS.md).

**Procedure:**
1. Identify every page that displays dynamic data (List pages, Dashboard pages, Calendar, Gallery)
2. Check if each has an entry in the per-page empty states table
3. Verify each entry has: headline, body copy, and CTA (or explicit "(No CTA — [reason])")

**Severity:** List/dashboard page with no empty state = 2. Missing headline or body = 2. Missing CTA without explanation = 1.

**Auto-fix:** Generate empty state microcopy for missing pages following the established pattern: "[No items] yet" / "[Explanation of what populates this page]" / "[CTA to the source action]".

</check>

<check name="8-story-id-consistency">

## Check 8: Story ID Consistency

**Cross-reference:** Story IDs in IA inventory "Source Stories" column (UX-DESIGN-PLAN.md) vs. traceability matrix (UX-FLOWS.md) vs. story map (STORY-MAP.md).

**Procedure:**
1. For each page in the IA, extract its Source Stories
2. For each story in the traceability matrix, extract its mapped page(s)
3. Cross-compare: does the IA agree with the traceability matrix about which stories map to which pages?
4. Verify every referenced SM-XXX exists in the story map

**Severity:** IA and traceability disagree on story-to-page mapping = 3. Story ID doesn't exist in story map = 3.

**Auto-fix:** Use the traceability matrix as source of truth (it was built with more detail). Update IA Source Stories to match.

</check>

<check name="9-cross-reference-validity">

## Check 9: Cross-Reference Validity

**Cross-reference:** Every PG-XXX reference across all documents.

**Procedure:**
1. Extract every PG-XXX reference from all documents
2. Verify each references a page that exists in the IA inventory
3. Check button automation "Result" columns — do they reference valid pages?
4. Check flow steps — do they reference valid pages?

**Severity:** Reference to non-existent page = 3. Reference to page with wrong name = 2.

**Auto-fix:** Correct page references. If a page ID doesn't exist, flag for manual review.

</check>

<check name="10-flow-diagram-coverage">

## Check 10: Flow Diagram Coverage

**Cross-reference:** User flows in UX-FLOWS.md.

**Procedure:**
1. For each user flow, assess complexity: count steps, decision points, and pages visited
2. Flows with 3+ decision points or 4+ pages SHOULD have a Mermaid diagram
3. Verify flows that have diagrams: do diagram steps match the prose steps?

**Severity:** Complex flow without diagram = 2. Diagram contradicts prose = 3.

**Auto-fix:** Cannot auto-generate diagrams, but flag which flows need them.

</check>

</process>

<output>

After running all 10 checks, produce a summary:

```
## UX Consistency Verification

| # | Check | Result | Findings |
|---|-------|--------|----------|
| 1 | Page name consistency | [PASS/FAIL] | [count] issues |
| 2 | Navigation table completeness | [PASS/FAIL] | [count] issues |
| 3 | Button label consistency | [PASS/FAIL] | [count] issues |
| 4 | Button target consistency | [PASS/FAIL] | [count] issues |
| 5 | Component pattern assignment | [PASS/FAIL] | [count] issues |
| 6 | Status value consistency | [PASS/FAIL] | [count] issues |
| 7 | Empty state coverage | [PASS/FAIL] | [count] issues |
| 8 | Story ID consistency | [PASS/FAIL] | [count] issues |
| 9 | Cross-reference validity | [PASS/FAIL] | [count] issues |
| 10 | Flow diagram coverage | [PASS/FAIL] | [count] issues |

**Overall: [N]/10 checks passed**
**Auto-fixed: [N] issues**
**Remaining: [N] issues requiring manual review**
```

If severity 3+ issues remain after auto-fix, list each with its location and what needs manual attention.

If all checks pass (or all issues were auto-fixed), report: "UX plan is internally consistent. Ready for implementation or full compliance review."

</output>

<anti_patterns>

- **Skipping checks because "it looks fine"** — run every check mechanically. Visual scanning misses cross-document inconsistencies.
- **Auto-fixing without understanding context** — when two documents disagree, the fix depends on which is authoritative. The hierarchy is: UX-COMPONENTS.md (behavior) > UX-LAYOUTS.md (wireframes) > UX-DESIGN-PLAN.md (tables). Traceability matrix > IA inventory for story mappings.
- **Treating this as a full compliance review** — this is a fast consistency pass, not a quality audit. It doesn't evaluate UX design quality, Nielsen's heuristics, or platform feasibility. Those belong in `review-ux-compliance.md`.
- **Running this INSTEAD of the compliance review** — this catches ~70% of common issues. The compliance review catches the remaining 30% (design quality, platform feasibility, heuristic gaps). Both have value; they serve different purposes.

</anti_patterns>

<success_criteria>

The verification is complete when:

- [ ] All 10 checks have been run
- [ ] Every finding has a severity rating
- [ ] All severity 3+ issues with mechanical fixes have been auto-corrected
- [ ] Remaining issues are clearly listed with locations
- [ ] Summary table is reported to the user
- [ ] Modified files are saved

</success_criteria>
