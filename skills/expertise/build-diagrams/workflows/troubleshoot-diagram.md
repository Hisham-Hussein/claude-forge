# Workflow: Troubleshoot Diagram

<required_reading>
**Read these reference files NOW:**
1. references/troubleshooting.md (error patterns and fixes)
2. references/platform-compatibility.md (platform-specific issues)
</required_reading>

<process>

<step name="1-get-context">
## Step 1: Get Error Context

Ask user (if not provided):
1. What error message appears? (exact text)
2. Where is it failing? (GitHub, VSCode, Mermaid Live)
3. Can you share the diagram code?

**Common error patterns:**

| Error Text | Likely Cause |
|------------|--------------|
| "Parse error" | Invalid syntax, wrong diagram type |
| "Expecting..." | Missing arrow, bracket, or keyword |
| No render (blank) | Missing diagram type declaration |
| Partial render | Syntax error mid-diagram |
| "Unknown diagram type" | Typo in type name or unsupported type |
</step>

<step name="2-diagnose">
## Step 2: Diagnose

**Syntax check (most common):**
1. First line must be diagram type (`flowchart LR`, `sequenceDiagram`, etc.)
2. All brackets closed: `{`, `[`, `(`, `"`
3. Arrow syntax correct for diagram type:
   - Flowchart: `-->`, `---`, `-.->`, `==>`
   - Sequence: `->>`, `-->>`, `-x`, `--x`
   - Class: `<|--`, `*--`, `o--`

**Platform check:**
- GitHub: No click events, no custom fonts, limited diagram types
- Check if using features not supported on target platform

**Complexity check:**
- >50 nodes can cause performance issues
- Deeply nested subgraphs may break layout

**Character check:**
- Special characters in labels need escaping
- Use `["text"]` for labels with special chars
</step>

<step name="3-isolate">
## Step 3: Isolate the Problem

If error location unclear:
1. Remove half the diagram
2. Does it render now?
3. Binary search to find problematic section

**Quick isolation technique:**
```
%% Comment out sections to isolate
%% Uncomment one section at a time
```
</step>

<step name="4-fix">
## Step 4: Apply Fix

**Common fixes:**

| Issue | Fix |
|-------|-----|
| Missing declaration | Add `flowchart LR` (or appropriate type) as first line |
| Unclosed bracket | Find and close the bracket |
| Wrong arrow | Check diagram-specific arrow syntax |
| Color name used | Replace with hex: `blue` → `#1976D2` |
| Click event on GitHub | Remove `click` statements |
| Special char in label | Wrap in quotes: `A["Label (with parens)"]` |
| Quote in label | Escape: `A["Text #quot;quoted#quot;"]` |
| Line break needed | Use `<br/>` in label |

**After fix, validate:**
1. Test in [Mermaid Live Editor](https://mermaid.live) first
2. Then test on target platform
</step>

<step name="5-prevent">
## Step 5: Prevent Recurrence

Explain what went wrong and how to avoid it:

"The issue was [X]. To prevent this:
- [Specific prevention tip]
- [Platform-specific note if relevant]"

Offer to regenerate the diagram cleanly if fixes are extensive.
</step>

</process>

<common_issues>
## Quick Reference: Common Issues

**Flowchart:**
- `A -> B` invalid, use `A --> B`
- Subgraph needs `end` keyword

**Sequence:**
- `A -> B` invalid, use `A ->> B` or `A -->> B`
- Participant names can't have spaces without quotes

**Class:**
- Methods need `()`: `+getName()` not `+getName`
- Relationships: `<|--` (inheritance), `*--` (composition)

**ER:**
- Relationship labels in quotes: `||--o{ : "has"`
- Entity names can't have spaces

**State:**
- Use `stateDiagram-v2` not `stateDiagram`
- Transitions: `State1 --> State2 : event`

**C4:**
- Requires Mermaid 10.4+
- Use `C4Context`, `C4Container`, `C4Component`
- GitHub may not support all C4 features

**All types:**
- Only hex colors work: `#1976D2` not `blue`
- Comments use `%%`
- Max ~50 nodes for performance
</common_issues>

<anti_patterns>
Avoid:
- Guessing at fixes without diagnosing
- Making multiple changes at once (hard to isolate)
- Not testing fix before returning to user
- Ignoring platform-specific limitations
</anti_patterns>

<success_criteria>
Troubleshooting is complete when:
- [ ] Root cause identified
- [ ] Fix applied and tested
- [ ] Diagram renders on target platform
- [ ] User understands what went wrong
- [ ] Prevention tip provided
</success_criteria>
