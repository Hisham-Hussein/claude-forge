<overview>
When diagrams don't render, systematic debugging finds the issue fast. This reference covers common errors, their causes, and fixes.
</overview>

<common_errors>
## Common Syntax Errors

| Error Message | Likely Cause | Fix |
|---------------|--------------|-----|
| "Parse error" | Invalid syntax | Check diagram type declaration |
| "Expecting..." | Missing element | Check for missing arrows, brackets |
| Blank/no render | Missing preamble | First line must be diagram type |
| Partial render | Syntax error mid-diagram | Find and fix the breaking line |
| "Unknown diagram type" | Typo or unsupported | Check spelling: `flowchart`, `sequenceDiagram` |
| Layout broken | Too complex | Reduce nodes, split diagram |
</common_errors>

<debugging_checklist>
## Debugging Checklist

1. **Check first line** - Must be diagram type declaration
   - `flowchart LR` not just `flowchart`
   - `sequenceDiagram` not `sequence`
   - `stateDiagram-v2` not `stateDiagram`

2. **Check brackets** - All must be closed
   - `{` needs `}`
   - `[` needs `]`
   - `(` needs `)`
   - `"` needs closing `"`

3. **Check arrow syntax** - Must match diagram type
   - Flowchart: `-->`, `---`, `-.->`, `==>`
   - Sequence: `->>`, `-->>`, `-x`, `--x`
   - Class: `<|--`, `*--`, `o--`
   - ER: `||--o{`, `}|..|{`

4. **Test in Mermaid Live Editor** - https://mermaid.live
   - Paste code, see if it renders
   - Editor shows error location

5. **Binary search** - If error unclear
   - Comment out half the diagram with `%%`
   - Does it render now?
   - Narrow down to problematic section
</debugging_checklist>

<diagram_specific>
## Diagram-Specific Issues

<flowchart_issues>
**Flowchart:**
- `A -> B` is invalid, use `A --> B`
- Subgraph needs `end` keyword
- Node IDs can't start with numbers
- Special chars in labels need quotes: `A["Label (with parens)"]`
</flowchart_issues>

<sequence_issues>
**Sequence:**
- `A -> B` is invalid, use `A ->> B` (sync) or `A -->> B` (async)
- Participant names with spaces need quotes: `participant "User Service"`
- Notes use `Note right of A: text` or `Note over A,B: text`
- Activation: `activate A` / `deactivate A`
</sequence_issues>

<class_issues>
**Class:**
- Methods need parentheses: `+getName()` not `+getName`
- Visibility: `+` public, `-` private, `#` protected
- Relationships: `<|--` inheritance, `*--` composition, `o--` aggregation
</class_issues>

<er_issues>
**ER:**
- Relationship labels must be in quotes: `||--o{ : "has"`
- Entity names can't have spaces
- Cardinality: `||` one, `o|` zero or one, `}|` one or more, `}o` zero or more
</er_issues>

<state_issues>
**State:**
- Use `stateDiagram-v2` not `stateDiagram`
- Transitions: `State1 --> State2 : event`
- Initial state: `[*] --> FirstState`
- Final state: `LastState --> [*]`
</state_issues>

<c4_issues>
**C4:**
- Requires Mermaid 10.4+
- Keywords: `C4Context`, `C4Container`, `C4Component`
- Person: `Person(alias, "Name", "Description")`
- System: `System(alias, "Name", "Description")`
- Container: `Container(alias, "Name", "Tech", "Description")`
- Relationships: `Rel(from, to, "description")`
</c4_issues>
</diagram_specific>

<escaping>
## Escaping Special Characters

| Character | Problem | Solution |
|-----------|---------|----------|
| Parentheses | Breaks node definition | `A["Text (with parens)"]` |
| Quotes | Breaks label | `A["Text #quot;quoted#quot;"]` |
| Brackets | Breaks structure | `A["Text [bracketed]"]` |
| Ampersand | May cause issues | `A["A #amp; B"]` |
| Line breaks | Need explicit break | `A["Line 1<br/>Line 2"]` |

**General rule:** Wrap labels with special characters in `["..."]`
</escaping>

<platform_issues>
## Platform-Specific Issues

**GitHub-specific:**
- Click events silently fail (security restriction)
- Custom fonts ignored
- Large diagrams (>50 nodes) may timeout
- Some newer diagram types may not render

**VSCode-specific:**
- Need Markdown Preview Mermaid extension
- Click events require `securityLevel: loose` in settings
- Theme may not match editor theme

**Cross-platform:**
- Only hex colors work: `#1976D2` not `blue`
- Test in both environments if sharing
</platform_issues>

<quick_fixes>
## Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| Diagram won't render | Add diagram type as first line |
| Colors not working | Replace color names with hex |
| GitHub shows nothing | Remove click events |
| Syntax error somewhere | Use Mermaid Live to locate |
| Too complex | Split into multiple diagrams |
| Labels overlap | Shorten labels or reduce nodes |
</quick_fixes>

<mermaid_gotchas>
## Mermaid Gotchas

- Only hex colors, never color names
- GitHub renders differently than VSCode
- Large diagrams (>50 nodes) cause performance issues
- Comments use `%%` not `//` or `#`
- Whitespace sensitivity varies by diagram type
- Some keywords are reserved (e.g., `end`, `graph`)
</mermaid_gotchas>
