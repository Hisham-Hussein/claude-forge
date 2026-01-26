<overview>
Domain knowledge for business case and BRD creation. Load this reference during Steps 2-4 of the process when analyzing documents, eliciting gaps, or drafting output. Contains framework details, elicitation techniques, stakeholder analysis, and BRD structure guidance.
</overview>

<document_hierarchy>

The documents form a cascade of increasing specificity:

```
Business Case → BRD → SRS/FRS → Technical Plan
     WHY         WHAT    HOW (system)   HOW (build)
```

- **Business Case** — Justifies the investment. "Should we do this?"
- **BRD** — Defines business-level needs. "What does the business need?"
- **SRS** — System-level functional/non-functional requirements. "What must the system do?"
- **Technical Plan** — Architecture, phases, implementation. "How do we build it?"

This skill produces items 1-2 combined. Downstream skills handle 3-4.

</document_hierarchy>

<frameworks>

<lean_canvas>
**Use for: Lightweight projects** (small teams, short timelines, MVPs, high uncertainty)

9-section model by Ash Maurya, maps to BRD:

| Lean Canvas Section | Maps To |
|---------------------|---------|
| Problem (top 1-3) | Problem Statement |
| Customer Segments | Stakeholders |
| Unique Value Proposition | Value Proposition |
| Solution (top 3 features) | High-level Requirements |
| Channels | Context for requirements |
| Revenue Streams | Success Criteria |
| Cost Structure | Constraints |
| Key Metrics | KPIs / Acceptance Criteria |
| Unfair Advantage | Strategic context |

**Key insight:** Problem-first — starts with pain, not solution. Use as conversational structure, output in BRD format.
</lean_canvas>

<prince2>
**Use for: Heavyweight projects** (large teams, formal approval, significant budget, regulated)

| Section | Purpose |
|---------|---------|
| Executive Summary | Brief overview for senior management |
| Reasons | Why this project exists (problem/opportunity) |
| Business Options | Do nothing / Do minimum / Do something |
| Expected Benefits | Quantified, with tolerances |
| Expected Dis-benefits | Negative consequences even if project succeeds |
| Timescale | Timeline and scheduling |
| Costs | Project + ongoing maintenance costs |
| Investment Appraisal | ROI, NPV, payback period analysis |
| Major Risks | Key risks with impact and responses |

**Key insight:** Always includes "Do Nothing" — forces explicit comparison against inaction.
</prince2>

</frameworks>

<brd_structure>

<essential_sections>
**Always include in Section 9 BRD:**

1. **Business Objectives** — SMART goals from business case
2. **Scope** — In-scope and explicitly out-of-scope
3. **Business Requirements** — ID, description, priority (MoSCoW), acceptance criteria
4. **Assumptions** — What we're assuming true
5. **Dependencies** — External needs
</essential_sections>

<optional_sections>
**Add based on complexity:**

- **Current vs. Future State** — How things work now vs. desired
- **Data Requirements** — What data entities exist, relationships
- **Success Metrics** — Measurable KPIs tied to objectives
- **Cost-Benefit Analysis** — Investment justification
</optional_sections>

<requirement_format>
Each requirement follows:

- **Format:** "The business needs to [verb] [object] so that [benefit]"
- **ID:** BR-01, BR-02, etc.
- **Priority:** Must | Should | Could | Won't (MoSCoW)
- **Acceptance Criteria:** Measurable condition for "done"

**Good:** "The business needs to respond to brand requests within 24 hours so that client satisfaction is maintained"
**Bad:** "Build a REST API with PostgreSQL" (this is implementation, not a requirement)
</requirement_format>

<brd_best_practices>
- "What" not "How": Requirements describe business needs, never implementation
- Prioritize everything: MoSCoW on each requirement during elicitation
- Be specific: "Improve response time" → "Respond to brand requests within 24 hours"
- Acceptance criteria: Each requirement has measurable "done" condition
- Keep accessible: Plain language, no jargon
- Scope explicitly: Document what's OUT as clearly as what's IN
- 81% of successful projects use context-specific BRD formats (BABOK 2024)
</brd_best_practices>

</brd_structure>

<elicitation_techniques>

<selection_matrix>
| Situation | Primary Technique | Secondary |
|-----------|-------------------|-----------|
| Research doc provided | Document Analysis | Structured Interview (for gaps) |
| No docs, new project | Structured Interview | Brainstorming |
| Unclear scope | Brainstorming | Prototyping |
| Validating draft | Prototyping | Structured Interview |
</selection_matrix>

<document_analysis>
**When doc provided:**
- Read document thoroughly
- Extract: problems, stakeholders, constraints, implied requirements
- Map findings to template sections
- Cross-reference against template to find gaps
- Identify what needs conversational elicitation
</document_analysis>

<structured_interview>
**Question hierarchy (follow this order):**

1. Problem-level: "What problem are you trying to solve?"
2. Stakeholder-level: "Who experiences this problem? Who decides?"
3. Constraint-level: "What are your limits? (time, budget, team, tech)"
4. Solution-level: "What would success look like?"
5. Validation-level: "If I summarize this as [X], does that match your intent?"

Open-ended first, then probe for specifics. Validate by reflecting back.
</structured_interview>

<brainstorming>
When requirements are unclear:
- Propose multiple possibilities
- Present options: "Would the system need X, Y, or Z?"
- Let user react rather than generate from scratch
- Use divergent thinking to surface unarticulated needs
</brainstorming>

<prototyping>
For validation:
- Draft a requirement, ask "Is this what you mean?"
- Show sample output format before generating full document
- Use "straw man" proposals user can react to
</prototyping>

<five_whys>
When user gives solution instead of problem:
- "We need a database" → Why?
- "To store influencer data" → Why?
- "To find matches faster" → Why?
- "We can't respond to brand requests quickly enough"
- **Problem found:** Response speed to brand requests

Keep asking until you reach the business need behind the technical request.
</five_whys>

</elicitation_techniques>

<stakeholder_analysis>

<power_interest_grid>
```
           HIGH INTEREST          LOW INTEREST
HIGH    ┌─────────────────┬─────────────────┐
POWER   │  Manage Closely │  Keep Satisfied │
        │  (Key Players)  │  (Context Only) │
        ├─────────────────┼─────────────────┤
LOW     │  Keep Informed  │  Monitor        │
POWER   │  (Show Progress)│  (Minimal)      │
        └─────────────────┴─────────────────┘
```

- **Manage Closely** (High Power, High Interest) → Include in requirements validation
- **Keep Satisfied** (High Power, Low Interest) → Their constraints matter but won't read details
- **Keep Informed** (Low Power, High Interest) → End users, affected parties
- **Monitor** (Low Power, Low Interest) → Peripheral stakeholders
</power_interest_grid>

<raci_matrix>
For heavyweight projects, assign per activity:

- **R**esponsible — Does the work
- **A**ccountable — Makes final decisions (only ONE per item)
- **C**onsulted — Provides input before action
- **I**nformed — Told about results after action

Apply to: defining requirements, approving business case, using final system, maintaining system.
</raci_matrix>

</stakeholder_analysis>

<edge_cases>

| Edge Case | How to Handle |
|-----------|---------------|
| User has no research doc, just an idea | Pure conversational elicitation; ask more questions |
| Multiple competing stakeholders | Capture all perspectives, flag conflicts, don't resolve |
| Project is already partially built | Document current state, focus BRD on gaps/next phase |
| Requirements are purely technical | Push back — find the business need behind the tech request |
| User gives solution instead of problem | "5 Whys" — keep asking why until business need surfaces |
| Everything marked as "Must" priority | Challenge: "What happens if we don't include this in v1?" |
| Contradictory stakeholder needs | Document both, flag as requiring decision, don't choose |

</edge_cases>

<limitations>

| Limitation | Mitigation |
|-----------|------------|
| AI can't interview real stakeholders | Ask user to represent stakeholder perspectives |
| Document analysis misses implicit context | Follow up with targeted questions about gaps |
| User may not distinguish want vs. need | Probe with "what happens if we don't include this?" |
| Solo user may lack full organizational view | Ask about other affected parties, approval processes |
| BRD can become too detailed too early | Enforce "what not how" rule; defer technical details |

</limitations>

<patterns>

1. **Problem-First**: Start with pain. Lean Canvas and BRD best practice both enforce this.
2. **"Do Nothing" Baseline**: PRINCE2's greatest contribution — explicit comparison against inaction.
3. **Requirements Are Negotiable, Constraints Are Not**: Distinguish wants (requirements) from boundaries (constraints).
4. **Adaptive Depth**: 72% of mid-sized companies use hybrid approaches. Scale output to match project complexity.
5. **Validate by Reflection**: Before final output, reflect key points back — catches misunderstandings early.
6. **Separate "Must" from "Nice to Have" Early**: MoSCoW during elicitation forces trade-off thinking.
7. **Acceptance Criteria for Each Requirement**: Without them, a requirement is a wish.

</patterns>
