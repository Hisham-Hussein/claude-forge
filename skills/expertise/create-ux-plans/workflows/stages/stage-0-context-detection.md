<stage name="0-context-detection">

## Stage 0: Context Detection & UX Brief

Runs before any document generation. Looks through the project first, then interviews the user about what it could not settle, and writes the **UX brief** that every later stage reads.

Why look before asking: the project often already answers "is there a data model?" or "is there a design system?". Asking what the files already say wastes the user's time and invites a wrong answer from memory. Asking about what the files cannot settle (depth, primary device) is where the user's judgment matters.

### Step 0.1: Discover Story Map

1. Check `.charter/STORY-MAP.md`
2. If not found, ask the user for the path
3. **Hard stop** if no story map is available — cannot proceed without one

Also check for user stories: `.charter/USER-STORIES.md`. If found but not mentioned by user, ask: "I found `.charter/USER-STORIES.md` — should I use it to enrich the plan with acceptance criteria detail?"

### Step 0.2: Look Before Asking

Search the project for the six things below. Skip dependency and build folders (`node_modules`, `dist`, `.git`) and archive folders. For each, stop at the first convincing source, note its path, and note what it says. A finding is a candidate answer for the interview, not a decision.

| Look for | Where it usually is |
|----------|---------------------|
| **Platform** | A PRD (`**/prd*.md`, `**/PRD*.md`), an architecture doc, a business case (`.charter/BUSINESS-CASE.md`), the README, or the front end's dependencies (`package.json`) |
| **Design system** | A design-rules document (`DESIGN.md`, `design-system*.md`, `docs/design*`), a component-library config (`components.json` for shadcn/ui), theme or token files, a Storybook |
| **Data model** | Database schema files (`schema.prisma`, Drizzle `schema.ts`, SQL migrations), an API schema (`openapi*.json`, `openapi*.yaml`, `*.graphql`) |
| **Languages** | The story map and business case (languages, right-to-left, localization), locale or translation files |
| **Primary device** | The story map's personas and context (desk work vs. on the move), analytics notes, the business case |
| **Competitor research** | Research or design folders and files that name competitors (`**/*competitor*`, `.charter/COMPETITOR-FUNCTIONALITY.md`), a competitor section in the business case or market research |

Classify the platform:

| Category | Examples | Implication |
|----------|----------|-------------|
| **Constrained** | Airtable Interface Designer, Notion, Retool, Bubble | Hard limits shape every UX decision — Context7 required |
| **Custom UI** | React, Next.js, Vue, Angular, Svelte | Full freedom — Context7 optional but useful |
| **Hybrid** | Custom UI with constrained data layer (e.g., React + Airtable backend) | UI is unconstrained but data model may limit states/fields |

### Step 0.3: Interview

Ask one question per message, in the order below, and wait for the answer before the next. Use a multiple-choice question tool when one is available. Each question:
- offers what Step 0.2 found as the first, recommended option, with the path it came from;
- says in one line why the answer changes the plan;
- accepts "none" or a correction.

Skip a question (other than Platform, question 8, which is asked only when nothing was found) only when the story map or business case states the answer outright (for example, "every screen in Arabic or English"). List skipped answers in the brief summary (Step 0.5) so the user still confirms them.

1. **Scope.** "The story map has **[N]** release slices. Should the UX plan target **MVP only**, or a specific slice?" Default to MVP.

2. **Depth.** Offer:
   - **Lean (3 documents):** UX-DESIGN-PLAN (IA, navigation, hierarchy), UX-FLOWS (flows and traceability), UX-LAYOUTS (a wireframe per page with its loading, empty and error states and exact microcopy). Enough for design concepts, mockups, prototypes and early front-end work, especially when a design system already defines component states.
   - **Full (6 documents):** Lean plus UX-COMPONENTS (every component's states), UX-INTERACTIONS (interaction, responsive and component data-state specs) and UX-ACCESSIBILITY. Use when there is no design system, or when a team will build every component from the plan.

   Recommend Lean when Step 0.2 found a design system, Full when it did not. Tell the user a lean plan can be extended to full later without redoing it.

3. **Primary device.** Desktop, mobile, or both equally. The primary device becomes the **base tier**: it is specified in full, and the other tiers state only what changes. Recommend from what Step 0.2 found and give the reason (dense data work done at a desk → desktop; consumer or on-the-move use → mobile). For "both equally", use mobile as the base tier, since adding space is easier to describe than taking it away.

4. **Languages and direction.** Which languages the interface ships in and which of them are right-to-left. With more than one language, every piece of microcopy is written in each, and right-to-left layouts get mirroring notes.

5. **Design system.** "I found **[path]**. Should the plan use it?" If used, later stages map elements to its existing components and cite its rules instead of re-specifying states, type roles, motion and accessibility basics. If none, the plan specifies them itself.

6. **Data model.** "I found **[paths]**. Should field specs come from it?" If used, layouts take field names, types and allowed values from it and flag any field the model lacks. If none, fields come from the story map.

7. **Competitors.** "I found research on **[names]** in **[paths]**. Should the plan draw on it, and for which 1-3 competitors?" If nothing was found, or the user names a competitor the existing research does not cover, offer: name 1-3 competitors for a short sourced research step (public help docs and feature pages, every finding cited), or skip. Offer the short step only if web search and page-reading tools are both available; otherwise say so and offer skip. Why it matters: users arrive with habits from the tools they know, and the plan should decide on purpose which conventions to keep. The plan takes functionality only, never a competitor's look, and the user decides each pattern in Stage 1.

8. **Platform** — ask only if Step 0.2 found no source: "What will the interface be built with?"

### Step 0.4: Gate on Constrained Platforms

Look for a Context7 server among the available tools: its tools end in `resolve-library-id` and `query-docs` (older versions: `get-library-docs`), whatever prefix the install gives them (`mcp__context7__…`, `mcp__plugin_context7_context7__…`, `mcp__claude_ai_Context7__…`). Record the exact tool names in the constraint manifest; later stages use those names.

If the platform is constrained and no Context7 tools are available:

**REFUSE to proceed.** Tell the user:

> "Platform **[X]** has hard limits (page count, component types, layout grid, navigation model) that must shape the UX design from the start. Please set up Context7 MCP before continuing. Without it, the generated UX plan will likely specify patterns the platform cannot implement."

If Context7 is available, resolve the platform's library ID now with the recorded `resolve-library-id` tool and store the ID for later stages.

### Step 0.5: Confirm the Brief

Show the UX Brief (every answer and its source, including any taken from the story map without asking) in one message, and ask the user to confirm or correct it. Write the files in Steps 0.6-0.7 only after confirmation, so a correction never leaves stale statuses behind.

### Step 0.6: Write Constraint Manifest and UX Brief

Write `.charter/UX-CONSTRAINTS.md` using `templates/ux-constraints-template.md`.

Populate:
- The **UX Brief** table: every interview answer with its source (file path, "user", or "story map"). If the user chose the short competitor research step, write that row as "[existing research paths, if any]; research pending for [names]"; Step 0.8 replaces it with the final file paths.
- Platform name and category (constrained/custom/hybrid), and the Context7 tool names or "not available"
- Source file where the platform was detected
- Known constraints extracted from that source (page limits, nav models, component types, etc.)
- Leave Stage-Specific Constraints subsections empty (enriched incrementally)

### Step 0.7: Write Generation Status Manifest

Write `.charter/UX-GENERATION-STATUS.md` using `templates/ux-generation-status-template.md`.

Populate:
- Pipeline run date, platform and constrained flag, story map path, scope, depth
- All 6 documents initialized as `pending`
- If depth is lean, set UX-COMPONENTS, UX-INTERACTIONS and UX-ACCESSIBILITY to `skipped` with reason `"lean depth"`
- If the platform handles accessibility (e.g., Airtable), set UX-ACCESSIBILITY to `skipped` with reason `"platform handles a11y"`

### Step 0.8: Short Competitor Research (only if chosen)

Run this when the brief's Competitor research row says "research pending": the user named competitors that existing research does not cover. Run the short sourced step in `references/competitor-research.md` for those competitors only. Write the findings to `.charter/COMPETITOR-FUNCTIONALITY.md`; if that file already exists, add a section for each new competitor and update its header, and never overwrite what is there. Then replace "research pending" in the brief with the file paths (existing research plus this file). If the step is skipped (the user declines, or no web tools are available), set the row to the existing research paths, or "none".

</stage>
