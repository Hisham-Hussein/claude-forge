<stage name="0-context-detection">

## Stage 0: Context Detection & Platform Constraints

Runs before any document generation. Discovers inputs, detects platform, writes manifests.

### Step 0.1: Discover Story Map

1. Check `.charter/STORY-MAP.md`
2. If not found, ask the user for the path
3. **Hard stop** if no story map is available — cannot proceed without one

Also check for user stories: `.charter/USER-STORIES.md`. If found but not mentioned by user, ask: "I found `.charter/USER-STORIES.md` — should I use it to enrich the plan with acceptance criteria detail?"

### Step 0.2: Detect Platform Stack

Parse the PRD (`_bmad-output/planning-artifacts/prd.md` or user-specified path) for technology choices. If no PRD exists, check architecture doc. **Find the answer and stop — do not scan both.**

Classify the platform:

| Category | Examples | Implication |
|----------|----------|-------------|
| **Constrained** | Airtable Interface Designer, Notion, Retool, Bubble | Hard limits shape every UX decision — Context7 required |
| **Custom UI** | React, Next.js, Vue, Angular, Svelte | Full freedom — Context7 optional but useful |
| **Hybrid** | Custom UI with constrained data layer (e.g., React + Airtable backend) | UI is unconstrained but data model may limit states/fields |

### Step 0.3: Gate on Constrained Platforms

If constrained platform detected AND Context7 MCP (`mcp__plugin_context7_context7__resolve-library-id` tool) is unavailable:

**REFUSE to proceed.** Tell the user:

> "Platform **[X]** has hard limits (page count, component types, layout grid, navigation model) that must shape the UX design from the start. Please set up Context7 MCP before continuing. Without it, the generated UX plan will likely specify patterns the platform cannot implement."

If Context7 IS available, resolve the library ID now:
- Use `mcp__plugin_context7_context7__resolve-library-id` with the platform name
- Store the resolved ID for use in subsequent stages

### Step 0.4: Write Constraint Manifest

Write `.charter/UX-CONSTRAINTS.md` using the template from `templates/ux-constraints-template.md`.

Populate:
- Platform name and category (constrained/custom/hybrid)
- Context7 availability
- Source file where platform was detected
- Known constraints extracted from PRD (page limits, nav models, component types, etc.)
- Leave Stage-Specific Constraints subsections empty (enriched incrementally)

### Step 0.5: Write Generation Status Manifest

Write `.charter/UX-GENERATION-STATUS.md` using the template from `templates/ux-generation-status-template.md`.

Populate:
- Pipeline run date
- Platform name and constrained flag
- Story map path
- All 6 documents initialized as `pending`
- If platform handles accessibility (e.g., Airtable), set UX-ACCESSIBILITY status to `skipped` with reason `"platform handles a11y"`

### Step 0.6: Confirm Scope

Ask the user: "The story map has **[N]** release slices. Should the UX plan target **MVP only**, or a specific slice?"

Default to MVP if the user doesn't specify. Record the scope in the generation status manifest.

</stage>
