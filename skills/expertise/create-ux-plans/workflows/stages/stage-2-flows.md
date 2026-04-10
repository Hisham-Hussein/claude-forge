<stage name="2-flows">

## Stage 2: UX-FLOWS.md

### Output
`.charter/UX-FLOWS.md` — Sections 10-11 of the output template (User Flows + Traceability Matrix)

### Dependencies
Stage 1 verified and approved (UX-DESIGN-PLAN.md with IA available)

### Inputs (re-read from disk)
- Story map
- Constraint manifest
- **UX-DESIGN-PLAN.md** (verified — the IA is the foundation for flows)
- User stories (if available — acceptance criteria enrich flow detail)

### References to Load
- `references/nielsen-heuristics.md`

### Context7 Query (if constrained platform)
Query for: flow complexity limits (max steps, branching support), automation/trigger capabilities, form submission patterns.

Append findings to constraint manifest under `## Stage-Specific Constraints > ### Stage 2 Constraints`.

### Why Flows Before Layouts

Flows stress-test the IA before committing to wireframes. When tracing real user journeys through the page inventory, you discover:
- Missing pages (journey has no destination for a required step)
- Broken navigation paths (no way to get from A to B)
- Pages that should be merged (two pages visited in the same breath)
- Wrong page groupings (activities that should be separate)

Fix IA issues discovered here by editing UX-DESIGN-PLAN.md (update page inventory, navigation model). The verification subagent will catch any cross-document inconsistencies this creates.

### Generation Instructions

#### Section 10: User Flows

For each major user task from the story map, create a step-by-step flow:

- **Entry point:** How does the user start this task?
- **Steps:** What does the user do at each point? Reference pages from the IA by PG-XXX.
- **Decision points:** What if the user does X instead of Y?
- **Error recovery paths:** What happens when something fails mid-flow?
- **Exit point:** Where does the flow end?

Use bulleted sequences for simple flows. Add **Mermaid diagrams** for flows with 3+ decision points or 4+ pages (the verification will flag missing diagrams).

Trace each flow to its source: SM-XXX.

**Platform constraint check:** If constrained platform, verify flow complexity is feasible. Simplify branches that exceed platform capabilities.

#### Section 11: Traceability Matrix

Build the traceability table linking every UX decision to its source:

| UX Element | Plan Section | Source ID | Source Description |
|------------|-------------|-----------|-------------------|
| [element] | [section ref] | SM-XXX / US-XXX | [activity/story name] |

**Coverage check:** Every story map activity in scope must have at least one UX element. Flag gaps.

**Orphan check:** Every UX element must trace to a source. Flag elements without traceability — they are either invented requirements (remove) or story map gaps (flag for user).

#### Nielsen's Heuristic Validation Summary

Using the nielsen-heuristics reference, run a two-pass validation across the plan so far (DESIGN-PLAN + FLOWS):

1. **First pass:** Read for overall impressions. Note which heuristics seem well-addressed vs. absent.
2. **Second pass:** Go heuristic-by-heuristic (H1-H10). Record gaps with severity ratings (0-4).

Include the summary table in Section 11 of the output (per template format). Fix severity 3+ gaps in the existing documents before proceeding.

### Verification Checks
- `story-id-consistency` (Check 8)
- `flow-diagram-coverage` (Check 10)

</stage>
