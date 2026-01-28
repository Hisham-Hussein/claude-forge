<overview>
Diagram type selection is communication-driven. The right diagram type makes the message clear; the wrong type obscures it. This reference provides decision logic for selecting the optimal diagram type.
</overview>

<quick_reference>
| Communication Goal | Diagram Type | Mermaid Keyword |
|-------------------|--------------|-----------------|
| System overview (who uses what) | C4 Context | `C4Context` |
| Services & databases | C4 Container | `C4Container` |
| Internal modules | C4 Component | `C4Component` |
| Step-by-step process | Flowchart | `flowchart LR/TB` |
| Object interactions over time | Sequence | `sequenceDiagram` |
| Class/interface structure | Class | `classDiagram` |
| Object lifecycle states | State | `stateDiagram-v2` |
| Database schema | ER | `erDiagram` |
| Project timeline | Gantt | `gantt` |
| Brainstorming/hierarchy | Mindmap | `mindmap` |
| Historical events | Timeline | `timeline` |
| 2D grid / matrix (rows × cols) | Block Beta | `block-beta` |
| 2x2 matrix analysis | Quadrant | `quadrantChart` |
</quick_reference>

<decision_tree>
**What are you communicating?**

```
"How the system fits in the bigger picture"
  → C4 Context (actors + system as black box)

"What services/apps make up the system"
  → C4 Container (apps, databases, services)

"How objects interact over time"
  → Sequence Diagram (messages between participants)

"Step-by-step process or algorithm"
  → Flowchart (decisions, branches, flows)

"Object states and transitions"
  → State Diagram (lifecycle, status changes)

"Database structure"
  → ER Diagram (entities, relationships)

"Code structure (classes/interfaces)"
  → Class Diagram (inheritance, composition)

"2D grid — data with rows AND columns"
  → Block Beta (story maps, priority matrices, feature planners)

"Project timeline"
  → Gantt Chart (tasks, dependencies, dates)
```
</decision_tree>

<c4_model>
## C4 Model Zoom Levels

The C4 model provides four levels of abstraction. Most teams only need levels 1-2.

| Level | Name | Audience | Shows | When to Use |
|-------|------|----------|-------|-------------|
| 1 | Context | Everyone | System as black box + external actors | Starting point, stakeholder presentations |
| 2 | Container | Technical staff | Applications, databases, services | Architecture discussions, team onboarding |
| 3 | Component | Developers | Internal modules within a container | Deep dives, specific implementation |
| 4 | Code | Developers | Classes, interfaces | Usually skip - auto-generate from code |

**Key insight:** Start with Context. Only zoom in when the audience needs more detail.

**C4 in Mermaid:**
- `C4Context` - Level 1
- `C4Container` - Level 2
- `C4Component` - Level 3
- C4 is now stable in Mermaid (not experimental)
</c4_model>

<flowchart_direction>
## Flowchart Direction

| Direction | Code | Best For |
|-----------|------|----------|
| Left to Right | `flowchart LR` | Process flows, timelines, horizontal space |
| Top to Bottom | `flowchart TB` | Hierarchies, decision trees, vertical space |
| Right to Left | `flowchart RL` | Reverse flows (rare) |
| Bottom to Top | `flowchart BT` | Bottom-up processes (rare) |

**Default recommendation:** `flowchart LR` for most process diagrams
</flowchart_direction>

<sequence_vs_flowchart>
## Sequence vs Flowchart

**Use Sequence when:**
- Time/order matters (message 1 before message 2)
- Multiple actors/systems exchange messages
- Request/response patterns
- API interactions

**Use Flowchart when:**
- Decisions branch the flow
- Single actor follows steps
- Algorithm or procedure
- No inter-system communication
</sequence_vs_flowchart>

<block_beta_grids>
## Block Beta Grid Diagrams

**Use `block-beta` when data has two dimensions** — anything that would be a spreadsheet or matrix, NOT a process flow.

| Use Case | Columns | Rows | Example |
|----------|---------|------|---------|
| User story map | Activities (journey steps) | Release slices (MVP, R2, R3...) | Features at each intersection |
| Priority matrix | Feature areas | MoSCoW priority | Items per area/priority |
| Team × feature | Teams | Features | Ownership mapping |
| Release planner | Sprints | Epics | Stories per sprint/epic |

**Why NOT flowchart:** Flowcharts add arrows between nodes, implying process flow. Grids have no flow — just intersections.
**Why NOT journey:** Mermaid `journey` is a 1D backbone. It cannot show vertical stacking (release slices) — only a single horizontal journey.

**Key syntax:**
```mermaid
block-beta
    columns 7
    space:1 H1["Col Header"]:1 H2["Col Header"]:1
    ROW["Row Label"]:1 CELL["Content\nLine 2"]:1 space:1
```

**Rules:**
- `columns N` defines width. 4-7 columns works well for typical screens.
- Every row must total exactly N blocks (use `space:1` for empties).
- `\n` creates line breaks in labels (NOT `<br/>`).
- Use `·` separator to fit two items on one line: `"Item A · Item B"`.
- No `classDef` support — use per-node `style` statements.
- No arrows/edges — pure grid layout.
- Color rows by semantic meaning (e.g., release → color) for scanability.
</block_beta_grids>

<anti_patterns>
## Wrong Type Choices

| Scenario | Wrong Choice | Right Choice |
|----------|--------------|--------------|
| API call sequence | Flowchart | Sequence |
| User login process (single system) | Sequence | Flowchart |
| Database tables | Class diagram | ER diagram |
| Object inheritance | ER diagram | Class diagram |
| System overview | Component diagram | Context diagram |
| Internal modules | Context diagram | Component diagram |
| Story map / release planner | Flowchart or Journey | Block Beta |
| Feature × team matrix | Flowchart | Block Beta |
</anti_patterns>
