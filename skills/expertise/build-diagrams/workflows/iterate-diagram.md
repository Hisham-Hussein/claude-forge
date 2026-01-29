# Workflow: Iterate Diagram

<required_reading>
**Read based on requested change:**
- Adding detail → references/complexity-guidelines.md
- Changing theme → references/color-palettes.md
- Splitting diagram → references/diagram-selection.md
</required_reading>

<process>

<step name="1-identify-change">
## Step 1: Identify Change Type

What does the user want to change?

| Request | Action |
|---------|--------|
| "Add more detail" | Add nodes/edges, check complexity |
| "Change theme" | Swap color palette |
| "Split this" | Create multiple focused diagrams |
| "Change layout" | Adjust direction (LR↔TB) or structure |
| "Fix labels" | Update text for clarity |
| "Add styling" | Apply semantic colors |
| "Make it simpler" | Remove nodes, increase abstraction |
| "Make labels clearer" (block-beta) | Iterate cell label content |
| "Too tall / too compact" (block-beta) | Adjust row height via label compression |

If unclear, ask: "What specifically would you like to change?"
</step>

<step name="2-assess-impact">
## Step 2: Assess Impact

**For adding detail:**
- Current node count + new nodes
- If total >15: warn user
- If total >25: require split discussion

**For theme change:**
- Just swap palette values (dark ↔ light)
- No structural changes needed

**For splitting:**
- Identify natural boundaries (subsystems, phases, layers)
- Each resulting diagram should have clear focus
- Plan linking strategy (naming convention, cross-references)
</step>

<step name="3-apply-change">
## Step 3: Apply Change

**Adding nodes:**
1. Add new elements with consistent naming
2. Connect to existing structure
3. Apply same styling classes
4. Re-validate complexity

**Changing theme:**
1. Replace all hex color values
2. Dark → Light or Light → Dark from palettes
3. Ensure contrast still works

**Splitting diagram:**
1. Create overview diagram (high-level)
2. Create detail diagrams (focused areas)
3. Use consistent naming across diagrams
4. Add comments linking them: `%% See: detailed-auth-flow.md`

**Changing layout:**
- `flowchart LR` ↔ `flowchart TB`
- Reorder elements if needed for readability

**Iterating block-beta grids:**

Block-beta iteration is about **label content, not structure**. The grid (columns, rows, space:1 padding) stays fixed — what changes is the text inside each cell.

1. **Label clarity** — iterate from terse to descriptive:
   - Round 1: Short nouns (`"Niche\nSize"`)
   - Round 2: Add context (`"Primary niche\nFollower bucket"`)
   - Round 3: Add specifics (`"Primary niche (25+)\nNano→Mega bucket"`)
   - Grids scale well with descriptive text (3-4 words per line) — don't fear longer labels

2. **Row height control** — row height is set by the **tallest cell**:
   - Identify the tallest cell in the row
   - Compress that cell first (combine items, shorten phrases)
   - Other cells in the row automatically shrink with it
   - Use `·` separator only for obvious noun pairs: `"Status · Priority"` (not for phrases)

3. **What NOT to change:**
   - Column count (viewport-dependent, set once)
   - `space:1` padding (maintains grid alignment)
   - Per-node `style` statements (colors are semantic, not aesthetic)
</step>

<step name="4-validate">
## Step 4: Validate

Re-check after changes:
- [ ] Still renders without errors
- [ ] Complexity within limits
- [ ] Theme colors consistent
- [ ] Labels still clear
- [ ] Platform compatibility maintained
</step>

<step name="5-present">
## Step 5: Present Updated Diagram

Show the updated diagram and summarize changes:
"Updated the diagram: [summary of changes]. Node count is now X."

Offer further iterations or confirm done.
</step>

</process>

<splitting_strategies>
## When to Split and How

**By abstraction level (C4 style):**
- Overview: System context (who uses what)
- Detail: Container view (what's inside)
- Deep: Component view (internal structure)

**By functional area:**
- Authentication flow
- Data processing
- Error handling
- Each as separate diagram

**By sequence phase:**
- Setup/initialization
- Main flow
- Cleanup/teardown

**By audience:**
- Executive summary (simple)
- Technical detail (comprehensive)
</splitting_strategies>

<anti_patterns>
Avoid:
- Adding detail without checking complexity limits
- Partial theme changes (mixing light/dark colors)
- Splitting without clear boundaries
- Losing context when splitting (no cross-references)
</anti_patterns>

<success_criteria>
Iteration is complete when:
- [ ] Requested change applied correctly
- [ ] Diagram still renders
- [ ] Complexity within acceptable limits
- [ ] User confirms the update meets their need
</success_criteria>
