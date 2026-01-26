---
name: build-diagrams
description: Use when creating technical diagrams for documentation, architecture, processes, or data models. Supports Mermaid.js with C4, flowcharts, sequence, ER, state, class, Gantt, and mindmap diagrams.
---

<essential_principles>

<principle name="platform-first">
**Target platform determines capabilities.** GitHub has limitations (no click events, ~v10.8.0). VSCode supports all features. Always confirm target before generating.
</principle>

<principle name="type-matches-intent">
**Diagram type follows communication goal:**
- Architecture overview → C4 Context/Container
- Process/algorithm → Flowchart
- Object interactions over time → Sequence
- Database schema → ER Diagram
- Object lifecycle → State Diagram

Don't let user skip type selection - wrong type = useless diagram.
</principle>

<principle name="complexity-kills">
**Keep diagrams simple:**
- ≤15 nodes recommended, >25 requires splitting
- ≤3 edges per node average
- If it doesn't fit on one screen, split it

Complex diagrams become unreadable. Multiple focused diagrams > one "complete" hairball.
</principle>

<principle name="hex-colors-only">
**Always use hex colors, never color names.** `fill:#1976D2` works everywhere. `fill:blue` fails on GitHub.
</principle>

<principle name="syntax-from-context7">
**For Mermaid syntax, query Context7** with library ID `/mermaid-js/mermaid`. Don't guess syntax - verify it.
</principle>

<principle name="design-before-code">
**Make design decisions BEFORE writing Mermaid code:**
1. **Shape language** - Different element types need different shapes (actors=stadium, actions=rectangle)
2. **Label refinement** - 2-3 words max, not verbose sentences
3. **Semantic colors** - ASK what colors should communicate (domain, priority, actor, status)
4. **Visual hierarchy** - Boundaries recede (dashed), content pops (solid stroke)
5. **Legend** - If colors have meaning, document it

Skipping this step produces dull, generic diagrams that require multiple iterations.
</principle>

<principle name="beautiful-defaults">
**Start with beautiful, not just functional.** Use the vibrant Tailwind palette instead of muted MD3 by default. Apply smooth curves (`curve: "basis"`). Style links (`linkStyle default`). Make it look like a world-class designer created it.
</principle>

<principle name="sequence-diagrams-are-different">
**Sequence diagrams have different styling rules.** They don't support `classDef` like flowcharts. Instead:
- Use `box rgb(r, g, b) Label` syntax to group and color participants
- Use `%%{init: {"sequence": {"mirrorActors": false}} }%%` to prevent duplicate actors
- Group by actor type (Human, System, External) rather than domain
- See `references/color-palettes.md` for sequence-specific colors
</principle>

</essential_principles>

<defaults>
**Theme:** dark (user preference)
**Target:** github (most common)
**Layout:** LR for ≤5-step chains, TD for >5-step chains (longest sequential path)
**Spacing:** `nodeSpacing: 30, rankSpacing: 60` for cohesive layout
**Curves:** `curve: "basis"` for smooth, modern arrows
**Max nodes:** 15 (recommended), 25 (hard limit before split)
**Palette:** Vibrant Tailwind colors (not muted MD3) for visual impact
**Links:** Always style with `linkStyle default stroke:#64748B,stroke-width:1px`
</defaults>

<intake>
**Invocation modes:**

1. **Context-aware** (no args): Analyze conversation, auto-select type, confirm
2. **Explicit args**: `/build-diagrams c4-context --theme=light --target=vscode`
3. **Guided**: Ask when context is ambiguous

**If arguments provided**, parse them and proceed to create-diagram workflow.

**If no arguments**, ask:

What would you like to diagram?

1. System architecture (C4 Context/Container/Component)
2. Process or algorithm (Flowchart)
3. Object interactions (Sequence)
4. Database schema (ER Diagram)
5. Object states (State Diagram)
6. Code structure (Class Diagram)
7. Project timeline (Gantt)
8. Something else

**Wait for response before proceeding.**
</intake>

<argument_schema>
Optional CLI-style arguments:

| Argument | Values | Default |
|----------|--------|---------|
| type | c4-context, c4-container, c4-component, flowchart, sequence, er, state, class, gantt, mindmap, timeline | (auto-detect) |
| --theme | dark, light | dark |
| --target | github, vscode | github |
| --title | "string" | (none) |

Examples:
- `/build-diagrams` - guided mode
- `/build-diagrams c4-context` - explicit type
- `/build-diagrams --theme=light` - just override theme
- `/build-diagrams sequence --target=vscode --title="Auth Flow"`
</argument_schema>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "architecture", "c4", "system", "overview" | `workflows/create-diagram.md` (type: c4) |
| 2, "process", "flow", "algorithm", "steps" | `workflows/create-diagram.md` (type: flowchart) |
| 3, "sequence", "interaction", "api", "messages" | `workflows/create-diagram.md` (type: sequence) |
| 4, "database", "schema", "er", "tables" | `workflows/create-diagram.md` (type: er) |
| 5, "state", "lifecycle", "status", "transitions" | `workflows/create-diagram.md` (type: state) |
| 6, "class", "code", "interface", "inheritance" | `workflows/create-diagram.md` (type: class) |
| 7, "timeline", "gantt", "schedule", "project" | `workflows/create-diagram.md` (type: gantt) |
| 8, other | Clarify, then route |
| "fix", "error", "broken", "not rendering" | `workflows/troubleshoot-diagram.md` |
| "change", "modify", "update", "add to" | `workflows/iterate-diagram.md` |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
All domain knowledge in `references/`:

**Selection:** diagram-selection.md (type matrix, decision logic, C4 levels)
**Styling:** color-palettes.md (MD3 light/dark, semantic colors)
**Platform:** platform-compatibility.md (GitHub vs VSCode, safe patterns)
**Accessibility:** accessibility.md (WCAG contrast, color-blind safety)
**Limits:** complexity-guidelines.md (node counts, splitting, labeling)
**Debugging:** troubleshooting.md (common errors, syntax fixes)
**Export:** cli-export.md (mmdc commands, image generation)
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| create-diagram.md | Create new diagram with type selection and styling |
| iterate-diagram.md | Refine or modify existing diagram |
| troubleshoot-diagram.md | Fix rendering or syntax issues |
</workflows_index>

<success_criteria>
A well-created diagram:
- Renders without errors on target platform
- Uses correct diagram type for the communication goal
- Has ≤15 nodes (or justified reason for more)
- Uses hex colors (vibrant Tailwind palette preferred)
- Has clear, concise labels (2-3 words max)
- Uses shape language (different shapes for different element types)
- Has semantic color meaning (by domain, priority, actor, or status)
- Includes a legend if colors encode meaning
- Has subtle boundaries (dashed, receding)
- Has styled links (not default black)
- Uses smooth curves (`curve: "basis"`)
- Looks like a world-class designer created it
</success_criteria>
