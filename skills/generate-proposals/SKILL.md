---
name: generate-proposals
description: Use when creating AI agency consulting proposals, writing client proposals, or when a client brief needs to be converted into a proposal document. Triggers include "create proposal", "generate proposal", "write proposal for client", "proposal from brief", or when iSemantics/AI agency proposal work is mentioned.
---

<objective>
Generate professional B2B consulting proposals for AI/automation agencies. Transforms client briefs into structured proposals with business value focus, tiered pricing, risk mitigation, and clear ROI frameworks. Outputs markdown proposals ready for delivery or conversion to PDF/HTML.

The skill embeds methodology from consulting proposal best practices: lead with business outcomes, use tiered pricing (3 options), include competitive positioning, and disclose ongoing costs transparently.
</objective>

<essential_principles>

**Business Value Over Technical Depth**
80% of decision-makers read only the executive summary. Lead with outcomes, not features. "Reduce cost-per-meeting by 40%" beats "AI-powered lead qualification system." The executive summary must include: problem, solution, key outcome with number, investment range, and CTA.

**Tiered Pricing (3 Options)**
Proposals with tiered pricing see 32% more conversions. Structure:
- **Essential**: Core solution, entry point for budget-conscious
- **Recommended** (mark this): Full solution, best value (majority choose this)
- **Premium**: Everything + ongoing support for committed clients

Always mark the recommended option. Wide price range increases "bulls-eye" match.

**Risk Mitigation Upfront**
SMB/startup clients fear project failure. Include:
- Phased payments tied to milestones (reduces client risk)
- Pilot/POC option for larger engagements
- Post-launch support period in base price
- Clear scope boundaries with change protocol

**Competitive Positioning Required**
Every proposal needs a Price vs Value chart showing where you sit relative to:
- Basic SaaS ($50-200/mo, no customization)
- Mid-market specialist ($2,500-$5,000, limited integrations)
- Large agency ($5,000-$15,000+, overkill for most)
Position as "full solution at specialist pricing."

**Ongoing Costs Disclosure**
Never hide post-launch costs. Transparently disclose:
- API fees (WhatsApp, OpenAI, etc.)
- Optional maintenance retainer
- Hosting costs if applicable
This builds trust and prevents objections later.

**"What" Not "How" in Solution Section**
Describe what the solution does and why it matters. Show workflow, not architecture. Include one demo/sample interaction. Reference "detailed technical spec available on request" for technical buyers.

</essential_principles>

<quick_start>
1. Ask: "Do you have a client brief ready, or should I help you structure one?"
2. If brief provided: Extract client name, industry, problem, solution type, budget, timeline
3. If missing info: Use AskUserQuestion to fill gaps (required fields only)
4. Ask optional preferences: Include future roadmap? Personify the solution with a name?
5. Generate proposal using templates/PROPOSAL.md structure
6. Validate with user, iterate if needed
</quick_start>

<intake>
What would you like to do?

1. **Generate proposal from client brief** — I have a brief ready (file path or paste)
2. **Create client brief first** — Help me structure the intake information
3. **Review/improve existing proposal** — I have a draft that needs refinement
4. **Generate competitive matrix SVG** — Create a visual positioning chart

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Next Action | Workflow |
|----------|-------------|----------|
| 1, "brief", "generate", "create proposal" | Ask for brief path/content | workflows/generate-from-brief.md |
| 2, "structure", "help me", "create brief" | Structured interview | workflows/create-brief.md |
| 3, "review", "improve", "existing" | Ask for proposal path | workflows/improve-proposal.md |
| 4, "matrix", "competitive", "chart", "graph", "svg" | Collect axis/competitor info | workflows/generate-competitive-matrix.md |

**Intent-based routing (if user provides clear context without selecting):**
- User provides file path or pastes brief → workflows/generate-from-brief.md
- "Here's the client info..." → workflows/generate-from-brief.md
- "I need to write a proposal for [client]" → workflows/generate-from-brief.md
- "Can you help structure client information?" → workflows/create-brief.md
- "Generate competitive matrix" / "create comparison chart" / "make positioning SVG" → workflows/generate-competitive-matrix.md
</routing>

<client_brief_schema>
**Required Fields** (ask if missing):
- Client name
- Industry (SaaS, marketing agency, influencer marketing, real estate, or other)
- Problem statement / pain points
- Solution type (what are we proposing?)
- Budget range (or "TBD" if unknown)
- Timeline expectations

**Optional Fields** (use defaults if missing):
- Decision-maker names
- Specific integrations needed
- Competitive context
- Existing technical plan (if prepared separately)
</client_brief_schema>

<industry_templates>
**Specialized templates available for:**
1. **SaaS** — Focus: MRR/ARR impact, churn reduction, user activation
2. **Marketing Agencies** — Focus: Client acquisition, campaign ROI, team efficiency
3. **Influencer Marketing** — Focus: Creator management, brand partnerships, campaign metrics
4. **Real Estate** — Focus: Lead-to-close time, deal volume, commission impact

**Universal template** used for other industries with dynamic context injection (industry terminology, relevant KPIs, typical pain points).
</industry_templates>

<slide_count_guidance>
**Target range:** 14-22 slides (flexible based on deal complexity)
- Minimum: 12 slides (below this is too thin)
- Maximum: 30 slides (above this loses attention)

| Section | Slides |
|---------|--------|
| Title & Context | 1 |
| Executive Summary | 1-2 |
| Problem & Opportunity | 2-3 |
| The Solution | 3-4 |
| Proof & Credibility | 1-2 |
| What's Delivered | 1-2 |
| Timeline | 1 |
| Investment Options | 2-3 |
| ROI Framework | 1-2 |
| Terms & Next Steps | 1-2 |
| Future Roadmap (optional) | 1-2 |
</slide_count_guidance>

<reference_index>
**Domain knowledge** in `references/`:
- `case-studies.md` — Case study library schema and selection logic
- `pricing-structures.md` — Tiered pricing guidance and ROI calculations
- `competitive-positioning.md` — Price vs value charts and comparison tables
- `isemantics-brand-elements-2.md` — iSemantics brand guidelines (colors, typography, logo usage)

**Templates** in `templates/`:
- `PROPOSAL.md` — Full proposal structure template
- `competitive-matrix.svg.template` — Glassmorphic 2x2 competitive positioning SVG (variable placeholders)
</reference_index>

<anti_patterns>
- Leading with technical features instead of business outcomes
- Single price point (no tiers)
- Hiding ongoing costs until after signing
- Using jargon without explanation
- No "Do Nothing" option in alternatives
- All requirements marked as "Must" priority
- Missing competitive positioning
- Over 30 slides (loses attention)
- Under 12 slides (appears lightweight)
- Skipping the executive summary or burying it
</anti_patterns>

<success_criteria>
Proposal generation is complete when:

- [ ] Executive summary includes: problem, solution, key outcome with number, investment, CTA
- [ ] Three pricing tiers with Recommended marked
- [ ] Competitive positioning chart included
- [ ] Ongoing costs disclosed transparently
- [ ] ROI/payback calculation present
- [ ] Clear scope (included vs not included)
- [ ] Timeline with phases
- [ ] Risk mitigation elements (phased payments, support period)
- [ ] Case study or proof points included
- [ ] Next steps with clear CTA
- [ ] 14-22 slides/sections (appropriate for deal size)
- [ ] User has validated the draft
</success_criteria>
