---
name: create-business-case
description: Use when starting a new project, justifying an investment, or when a research document exists but no formal business case. Triggers include "create business case", "write BRD", "business requirements", "justify this project", or when scope is unclear and needs structured exploration.
---

<objective>
Produce a BUSINESS-CASE.md that justifies why a project should exist and defines what the business needs from it. The output combines strategic justification (Sections 1-8) with a structured BRD section (Section 9) containing business requirements with IDs, MoSCoW priorities, and acceptance criteria. This BRD section serves as the input artifact for downstream requirements engineering.
</objective>

<quick_start>
1. Ask if user has a research document or is starting from scratch
2. Detect project complexity (team size, timeline, budget, stakeholders)
3. If doc provided: analyze it, identify gaps, ask targeted questions
4. If no doc: structured interview (problem → stakeholders → constraints → success)
5. Draft BUSINESS-CASE.md using the template at `templates/BUSINESS-CASE.md`
6. Validate with user, iterate if needed, deliver
</quick_start>

<essential_principles>

**Problem-First, Not Solution-First**
Start with pain, not features. "We need a database" is a solution. "We can't find matching influencers fast enough" is a problem. If the user gives a solution, use "5 Whys" to reach the business need.

**Always Include "Do Nothing"**
Explicitly state what happens if you don't build this. Forces honest evaluation and provides a baseline for measuring success. Never skip this — it's the most underrated section.

**"What" Not "How"**
Requirements describe business needs, never implementation. "The business needs to respond to brand requests within 24 hours" not "Build a REST API with PostgreSQL." This is the single most common contamination.

**MoSCoW During Elicitation, Not After**
Apply prioritization (Must/Should/Could/Won't) as requirements are discovered. Users present everything as critical — explicit prioritization forces trade-off thinking early.

**Acceptance Criteria Make Requirements Testable**
A requirement without acceptance criteria is a wish. Each business requirement must have a measurable condition for "done."

**Adaptive Depth Over One-Size-Fits-All**
Scale output to match project complexity. A solo developer building an MVP doesn't need a 40-page PRINCE2 business case. Detect complexity signals and adjust.

**No Technical Contamination**
NEVER read technical plans, architecture docs, or implementation files during generation. The business case must be derived purely from business context — problems, stakeholders, constraints, and goals.

**Reference Forward, Don't Duplicate**
Input documents (client briefs, research docs) often contain detailed specifications — data models, field lists, API details, pricing tables — that are too granular for the BRD but essential for downstream stages (SRS, architecture). Do NOT duplicate these details in the BRD. Instead, add a "Reference Documents" section (9.6) that points to these specifications with brief descriptions of what they contain. This keeps the BRD at the right abstraction level while ensuring downstream stages know exactly where to find implementation-level details.

</essential_principles>

<complexity_detection>

Detect project complexity to determine output depth:

| Signal | Lightweight | Heavyweight |
|--------|-------------|-------------|
| Team size | 1-5 people | 5+ people |
| Timeline | Less than 3 months | More than 3 months |
| Budget | Under $50K or internal | Over $50K or external client |
| Stakeholders | 1-3 decision makers | 4+ with competing interests |
| Uncertainty | High (exploring) | Low (defined problem) |
| Regulatory | None | Compliance requirements |

**Lightweight** (Lean Canvas-inspired): Sections 1, 2, 3, 6, 7, 9. Shorter, focused on speed.

**Heavyweight** (PMI/PRINCE2-inspired): All 9 sections, expanded. Include dis-benefits, investment appraisal considerations, RACI for stakeholders.

**Default**: Start lean, add formality where the project demands it.

</complexity_detection>

<reference_index>

**Domain knowledge** in `references/`:
- `methodology.md` — Business case frameworks (Lean Canvas, PRINCE2), BRD structure, elicitation techniques, stakeholder analysis, edge cases, and patterns

</reference_index>

<process>

**Before Step 2, read:** `references/methodology.md` for detailed framework guidance, elicitation techniques, and BRD structure rules.

**Step 1: Intake**

Ask the user:
- "Do you have an existing research document, brief, or business document I should analyze?" (If yes, get path)
- "How many people will use/work on this? What's your timeline? Budget range?"

These answers determine complexity level and whether to use Document Analysis or Structured Interview as primary technique.

**Step 2: Document Analysis (if doc provided)**

Read the provided document. Extract and map to template sections:
- Problems mentioned → Section 2 (Problem Statement)
- People/roles mentioned → Section 4 (Stakeholders)
- Constraints mentioned → Section 7 (Constraints)
- Goals/metrics mentioned → Section 6 (Success Criteria)
- Implied requirements → Section 9 (BRD)

Identify gaps — sections with no coverage from the document.

**Also identify detailed specifications for downstream reference:**
- Data models / field lists / schema definitions
- API specifications or integration details
- Pricing structures or rate cards
- Regulatory/compliance checklists
- Reference data (categories, regions, currencies)

These are too granular for the BRD but valuable for SRS/architecture stages. Note their location (file path + section) for Section 9.6 Reference Documents.

**Step 3: Elicit Gaps**

Only ask about what's missing. Use this priority:
1. Problem-level: "What problem are you trying to solve?" (if not clear from doc)
2. Stakeholder-level: "Who experiences this problem? Who decides?" (if not identified)
3. Constraint-level: "What are your limits? (time, budget, team, tech)" (if not stated)
4. Solution-level: "What would success look like?" (if metrics unclear)
5. Scope-level: "What is explicitly OUT of scope?" (almost always missing)

For each requirement discovered, immediately ask:
- "Is this a Must, Should, Could, or Won't for the first version?"
- "How would you know this requirement is satisfied?"

Ask at most 3-5 focused questions per round. Don't interrogate.

**Step 4: Draft**

Read `templates/BUSINESS-CASE.md` for the output structure.

Generate the full BUSINESS-CASE.md:
- Fill all sections appropriate to the complexity level
- Section 3 MUST include a "Do Nothing" option with consequences
- Section 9 (BRD) uses the table format: ID | Requirement | Priority | Acceptance Criteria
- Requirements use format: "The business needs to [verb] [object] so that [benefit]"
- IDs follow pattern: BR-01, BR-02, etc.
- If input documents contained detailed specifications (identified in Step 2), add Section 9.6 Reference Documents with file paths and brief descriptions of what each contains. This ensures downstream stages (SRS, architecture) know where to find implementation-level details without the BRD duplicating them.

**Step 5: Validate**

Present the draft to the user. Reflect back key points:
"Based on our conversation:
- The core problem is [X]
- Primary stakeholders are [Y]
- Success looks like [Z]
- I identified [N] business requirements ([M] must-haves, [K] should-haves)

Does this capture your intent? Anything to add, remove, or reprioritize?"

Iterate if user provides corrections.

**Step 6: Deliver**

Write BUSINESS-CASE.md to `.charter/BUSINESS-CASE.md` (create the `.charter/` folder if it doesn't exist). User can override with a different path.

Summarize: "[N] business requirements identified — [M] Must, [S] Should, [C] Could. Ready for requirements engineering."

</process>

<elicitation_techniques>

**When doc is provided**: Document Analysis (primary) + Structured Interview (for gaps)

**When no doc exists**: Structured Interview (primary) + Brainstorming (for unclear scope)

**When validating draft**: Prototyping — show the draft, let user react, iterate

**Brainstorming technique**: When requirements are unclear, propose possibilities: "Would the system need X, Y, or Z?" Let user react rather than answer open-ended questions.

**5 Whys technique**: When user gives solution instead of problem, keep asking "why" until you reach the business need. "We need a database" → "Why?" → "To store influencer data" → "Why?" → "To find matches faster" → Problem: "Finding matching influencers is too slow."

</elicitation_techniques>

<stakeholder_template>

For each stakeholder in Section 4, capture:

- **Role**: [Who — e.g., Marketing Manager, Brand Partner, Influencer]
- **Type**: Sponsor | Decision-maker | User | Affected party | Technical
- **Power/Interest**: High-High | High-Low | Low-High | Low-Low
- **Needs**: [What they need from the project]
- **Engagement**: Manage Closely | Keep Satisfied | Keep Informed | Monitor

For heavyweight projects, also capture RACI roles (Responsible, Accountable, Consulted, Informed).

</stakeholder_template>

<anti_patterns>

- Reading PLAN.md, architecture docs, or technical files during generation
- Writing "how" in the BRD section (implementation details masquerading as requirements)
- Skipping the "Do Nothing" option in Section 3
- Marking all requirements as "Must" priority
- Writing acceptance criteria that can't be objectively measured
- Asking more than 5 questions in a single round
- Producing heavyweight output for a solo developer's side project
- Producing lightweight output for a multi-team enterprise initiative

</anti_patterns>

<success_criteria>
Skill is complete when:

- BUSINESS-CASE.md written with all appropriate sections for complexity level
- Section 3 includes "Do Nothing" option with consequences
- Section 9 has requirements with IDs (BR-XX), MoSCoW priorities, and acceptance criteria
- All requirements describe business needs, never implementation
- Section 9.6 references any detailed specifications from input documents (if present)
- User has validated the draft and confirmed it captures their intent
- Output is ready to feed into requirements engineering
</success_criteria>
