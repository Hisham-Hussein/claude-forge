<required_reading>

**Read these reference files before executing updates:**

1. workflows/verify-ux-consistency.md — the 10-check consistency verification (called in Phase 4)
2. references/atomic-design.md — component pattern classification (needed when merges change page types)
3. references/interaction-patterns.md — navigation model patterns (needed when merges alter navigation)

</required_reading>

<inputs>

**Required:**
- Existing UX plan files in `.charter/` (any subset of: `UX-DESIGN-PLAN.md`, `UX-LAYOUTS.md`, `UX-COMPONENTS.md`, `UX-INTERACTIONS.md`, `UX-FLOWS.md`)
- Change specification from the user (page merges, removals, additions, or story-level changes)

**Optional:**
- Story map (`.charter/STORY-MAP.md`) — needed for traceability verification when stories change
- Updated user stories — needed when story-level changes are involved

If no `.charter/UX-*.md` files exist, inform the user that there is no existing plan to update and suggest using the `create-ux-plan` workflow instead.

</inputs>

<process>

<phase name="1-parse-change-set">

## Phase 1: Parse Change Set & Index Existing State

### Step 1: Read & Index Existing UX Plan

Read all `.charter/UX-*.md` files (excluding `UX-COMPLIANCE-REPORT.md`, which is a historical record and never modified by this workflow). Build an internal index of:

- **Pages:** Every PG-XXX with its name, Interface, page type, source stories, and nav level
- **Navigation:** Every cross-Interface button with source page, target page, label, and trigger
- **Components:** Every component pattern with its "Used in: PG-XXX" list
- **Buttons:** Every entry in the button automation table (location, trigger, automation, result)
- **Empty states:** Every entry in the per-page empty states table
- **Traceability:** Every story-to-page mapping in the traceability matrix
- **Flows:** Every PG-XXX reference in user flow prose and Mermaid diagrams
- **Visual hierarchy:** Every PG-XXX reference in scanning patterns, content hierarchy, and status color system
- **Interactions:** Every PG-XXX reference in state machines, filter specs, and inline editing lists

This index is the "before" snapshot. It drives the impact analysis in Step 3.

### Step 2: Parse Change Specification

Accept the user's change set in any format (natural language, structured list, or reference to a decision document). Classify each change as one of four operation types:

**Page merge:**
- Identify the **absorbing page** (keeps its PG-XXX ID) and the **absorbed page** (its ID is retired)
- Note the intended combined page name and type
- Note which content from the absorbed page integrates into the absorbing page

**Page removal:**
- Identify the removed page
- Identify where its stories and functionality are reassigned (other existing pages, or flagged as dropped)

**Page addition:**
- Identify the new page with its proposed name, Interface, page type, and source stories
- Assign the next available PG-XXX ID (find the current max and increment by 1)

**Story-level change:**
- Identify which stories are added, modified, or removed
- Identify which existing pages are affected

### Step 3: Build Impact Map

For each change, enumerate every location in every file that will be affected. Produce a structured impact map:

```
| Change | File | Section | What Changes |
|--------|------|---------|--------------|
```

For page merges, the impact map should cover at minimum:

| File | Sections Affected |
|------|-------------------|
| UX-DESIGN-PLAN.md | Page inventory table, navigation table, entry points table, content hierarchy, scanning pattern lists, page count |
| UX-LAYOUTS.md | Absorbed page wireframe (remove), absorbing page wireframe (integrate content) |
| UX-FLOWS.md | Flow prose (page references), Mermaid diagrams (node labels), traceability matrix (story-to-page mappings), coverage summary (page counts) |
| UX-COMPONENTS.md | "Used in" lists, empty states table, button automation table, navigation buttons table |
| UX-INTERACTIONS.md | State machine references, filter spec page lists, inline editing page lists |

**Present the impact map to the user and wait for confirmation before proceeding.** This is a mandatory gate — do not begin edits without user approval of the scope.

</phase>

<phase name="2-structural-changes">

## Phase 2: Execute Structural Changes

### Step 4: Update Information Architecture (UX-DESIGN-PLAN.md Section 2)

Process each change against the IA:

**For page merges:**
1. Remove the absorbed page's row from its Interface's page inventory table
2. Update the absorbing page's row:
   - Merge Source Stories (union of both pages' stories, deduplicated)
   - Update Page Name if the combined page has a new name
   - Update Page Type if the merge changes the page's primary type
3. Update the opening page count (e.g., "6 Interfaces containing N pages")
4. Update the cross-Interface navigation table:
   - Any button targeting the absorbed page → redirect to the absorbing page
   - Any button sourced from the absorbed page → move to the absorbing page
   - Remove buttons that navigated between the two now-merged pages (they become in-page sections)
5. Update entry points table if either page was a workflow entry point
6. **Do NOT renumber remaining pages.** Gaps in PG-XXX numbering are intentional.

**For page removals:**
1. Remove the page's row from its Interface's page inventory table
2. Reassign its Source Stories to the pages specified in the change set
3. Update page count
4. Remove or redirect navigation entries that targeted the removed page
5. Update entry points table if affected

**For page additions:**
1. Add a new row to the appropriate Interface's page inventory table
2. Use the next available PG-XXX ID
3. Add navigation entries as specified in the change set
4. Update page count

### Step 5: Update Content Hierarchy & Visual Hierarchy (UX-DESIGN-PLAN.md Sections 2-3)

1. Update per-Interface content priority descriptions to reflect merged/removed/added pages
2. Update scanning pattern page lists — the parenthetical PG-XXX lists after each pattern type (Dashboard, List, Form, Record Review, Calendar, Gallery)
3. If a merge changes a page's effective type (e.g., dashboard absorbs a list), update the page's scanning pattern assignment
4. Update the status color system "Used In" column if affected

### Step 6: Update Page Layouts (UX-LAYOUTS.md)

**For page merges:**
1. Remove the absorbed page's entire wireframe section (heading + wireframe + content priority + field specs)
2. Integrate the absorbed page's content into the absorbing page's wireframe:
   - If both pages are the same type (e.g., two forms): merge field sections under the absorbing page's structure
   - If different types (e.g., dashboard absorbs a list): add the absorbed content as a new section within the absorbing page's wireframe, positioned by content priority
3. Update the absorbing page's title if the name changed
4. Update the absorbing page's content priority description to cover the merged content
5. **The merged wireframe must read as if it were designed as one page from the start** — do not simply concatenate

**For page removals:**
1. Remove the page's entire wireframe section
2. If the page's content is redistributed to other pages, update those receiving pages' wireframes to include the relevant content

**For page additions:**
1. Create a new wireframe section following the conventions for that page type
2. Use existing pages of the same type as structural models

### Step 7: Update Interaction Patterns (UX-INTERACTIONS.md)

1. Update page references in state machine descriptions (e.g., "Expert imports on PG-001")
2. Update filter interaction specs — which pages have which filters (persona, status, time range, category)
3. Update inline editing page lists
4. If a merge combines functionality that had separate interaction descriptions, consolidate the descriptions
5. If a removal eliminates the only page hosting an interaction, move the interaction to its new host page
6. Update the feedback model page list if form pages are affected (explicit save vs. optimistic)

</phase>

<phase name="3-cross-references">

## Phase 3: Update Cross-References

### Step 8: Update Component Specifications (UX-COMPONENTS.md)

Update in this order:

1. **"Used in" lists on every component pattern:** For each pattern (Dashboard, List-Review Queue, List-Data Management, Form, Record Review, Calendar, Gallery):
   - Merges: replace absorbed PG-XXX with absorbing PG-XXX (avoid duplicates if absorbing page is already listed)
   - Removals: remove the PG-XXX entirely
   - Additions: add new PG-XXX to the appropriate pattern

2. **Per-page empty states table:** Remove entries for absorbed/removed pages. Add entries for new pages. Update entries for absorbing pages if their empty state message should change due to merged content.

3. **Button automation table:** Update the Location column for any button that was on a removed/absorbed page. Remove buttons that no longer exist. Add buttons for new pages.

4. **Navigation buttons table:** Update From and To page references. Remove entries where the navigation was between two now-merged pages. Add entries for new cross-page navigation.

### Step 9: Update User Flows & Traceability (UX-FLOWS.md)

1. **User flow prose (per-flow sections):** For each flow, update:
   - Page references in step descriptions (e.g., "Expert opens PG-011 (Strategy Recommendations)" → "Expert scrolls to the Strategy Recommendations section on PG-010")
   - Navigation steps between merged pages become in-page transitions (scrolling, section switching)
   - Entry and exit point declarations
   - Error path references

2. **Mermaid diagrams:** Update node labels, remove nodes for absorbed pages, redirect connections to absorbing pages. Simplify edges where two-page navigation becomes in-page navigation.

3. **Story-to-page traceability matrix:**
   - Coverage by Activity table: update UX Pages column, update page counts per activity
   - Per-Story Traceability table: update UX Page(s) column for every story that referenced changed pages
   - Update element descriptions if they referenced the absorbed page by name

4. **Coverage summary:** Update total page count and any derived statistics

5. **Orphan UX elements note:** Update if any cross-cutting pages were affected

### Step 10: Global PG-XXX Reference Sweep

After completing Steps 4-9, perform a mechanical sweep of ALL `.charter/UX-*.md` files (excluding `UX-COMPLIANCE-REPORT.md`) for any remaining references to absorbed or removed page IDs:

1. Search for every PG-XXX that was absorbed or removed
2. If any references remain, fix them:
   - Absorbed page IDs → replace with absorbing page ID
   - Removed page IDs → remove the reference or redirect per the change specification
3. Report any references that could not be automatically resolved (ambiguous context)

This step is the safety net. Steps 4-9 should catch everything, but this sweep ensures nothing was missed.

</phase>

<phase name="4-validate">

## Phase 4: Validate & Reconcile

### Step 11: Apply Hierarchy Rule for Conflicts

When documents disagree after updates, resolve using this precedence:

- **UX-COMPONENTS.md** (behavior) > **UX-LAYOUTS.md** (wireframes) > **UX-DESIGN-PLAN.md** (tables)
- **Traceability matrix** > **IA inventory** for story-to-page mappings

In practice:
- If a component pattern's "Used in" list says a page exists but the IA doesn't list it → trust the IA, fix the component
- If the traceability matrix and IA disagree on which stories map to a page → trust the traceability matrix, fix the IA
- If a wireframe shows content for a page that the IA says was removed → trust the IA, remove the wireframe content

### Step 12: Run verify-ux-consistency.md

Execute the full 10-check consistency verification from `workflows/verify-ux-consistency.md`:

1. Page name consistency (IA vs. layouts)
2. Navigation table completeness
3. Button label consistency
4. Button target consistency
5. Component pattern assignment
6. Status value consistency
7. Empty state coverage
8. Story ID consistency
9. Cross-reference validity
10. Flow diagram coverage

Auto-fix severity 3+ issues per the verification workflow's rules. Report the verification summary.

If any severity 3+ issues cannot be auto-fixed, flag them for the user before proceeding.

</phase>

<phase name="5-report">

## Phase 5: Report & Note Compliance Impact

### Step 13: Write Updated Files & Report

Save all modified files. Do NOT write files that had zero changes.

Report to the user:

- **Files modified** and approximate number of changes per file
- **Pages merged/removed/added** with before and after counts
- **Final page count** across all Interfaces
- **Cross-references updated** (count of PG-XXX substitutions)
- **Verification summary** from Step 12 (pass/fail per check, issues found and fixed)
- **Manual review items** — any changes that altered the meaning of existing UX decisions (flag for human review)

### Step 14: Note Compliance Report Impact

Do NOT modify `UX-COMPLIANCE-REPORT.md`. Instead, report to the user:

> "The existing UX Compliance Report was generated before these changes. Consider re-running the compliance review workflow to validate the updated plan."

List specific compliance areas likely affected:
- If pages were merged: traceability coverage numbers are outdated, page-specific findings may reference retired page IDs
- If pages were removed: findings referencing removed pages are now invalid
- If pages were added: new pages have not been audited
- If story mappings changed: traceability verification should be re-run

</phase>

</process>

<anti_patterns>

- **Regenerating unchanged content**: The update workflow edits surgically. Rewriting an entire wireframe because one section was added defeats the purpose. Preserve existing text verbatim for unchanged portions.

- **Renumbering pages**: When pages are removed or merged, remaining pages keep their IDs. Gaps in PG numbering (e.g., PG-001, PG-002, PG-005) are acceptable and intentional. Renumbering breaks external references in decision logs, compliance reports, and user communications.

- **Updating UX-COMPLIANCE-REPORT.md**: This is a historical audit record. The update workflow notes that a re-audit may be warranted but never modifies the report itself.

- **Skipping the impact map confirmation**: Proceeding directly to edits without showing the user what will change risks unwanted modifications. Always present the impact map and wait for confirmation.

- **Partial reference updates**: Updating IA but forgetting to update flows, or updating component "Used in" lists but forgetting button automation targets. The global sweep in Step 10 is the safety net, but each targeted step should be thorough.

- **Merging by concatenation**: When absorbing a page, the absorbed content must be integrated into the absorbing page's structure naturally. The result should read as if it were designed as one page from the start — not two wireframes stacked.

- **Inventing new UX during updates**: The update workflow applies specified changes. It does not add new features, pages, or components beyond what the change set specifies. If a change reveals a gap, flag it for the user rather than filling it.

- **Trusting a single document as complete**: Cross-references span 5 files. A change is not complete until all files are consistent. The verify-ux-consistency check catches most issues, but each targeted step should aim for zero findings.

</anti_patterns>

<success_criteria>

The update is complete when:

- [ ] Every change in the change set has been applied
- [ ] No references to absorbed/removed page IDs remain in any file (global sweep confirms)
- [ ] Page numbering gaps are preserved (no renumbering occurred)
- [ ] Unchanged content is preserved verbatim
- [ ] verify-ux-consistency.md passes (all 10 checks, or all severity 3+ auto-fixed)
- [ ] UX-COMPLIANCE-REPORT.md is untouched, with a note about re-audit reported to user
- [ ] Impact map was presented to and confirmed by user before edits began
- [ ] Updated file report delivered to user with change summary
- [ ] All "Used in" lists on component patterns reflect the current page set
- [ ] Traceability matrix reflects current story-to-page mappings with no orphaned references
- [ ] All Mermaid diagrams reference only existing pages
- [ ] Cross-Interface navigation table references only existing pages with correct names and targets

</success_criteria>
