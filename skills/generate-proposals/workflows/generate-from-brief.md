<required_reading>
Before generating, read:
- `templates/PROPOSAL.md` — Output structure template
- `references/pricing-structures.md` — For tiered pricing guidance
- `references/case-studies.md` — For case study selection
- `references/competitive-positioning.md` — For positioning charts
</required_reading>

<process>

**Step 1: Parse Client Brief**

Read the provided brief (file path or pasted content). Extract and validate:

| Field | Required? | If Missing |
|-------|-----------|------------|
| Client name | YES | Ask immediately |
| Industry | YES | Ask with options (SaaS, marketing agency, influencer marketing, real estate, other) |
| Problem statement | YES | Ask: "What problem is the client trying to solve?" |
| Solution type | YES | Ask: "What are we proposing to build?" |
| Budget range | YES | Ask or accept "TBD" |
| Timeline | YES | Ask: "When do they want to start/launch?" |
| Decision-maker | NO | Skip if not provided |
| Integrations | NO | Use defaults for solution type |

**Step 2: Ask Optional Preferences**

Use AskUserQuestion for:

1. **Technical plan exists?** "Is there a technical plan/proposal already prepared for this project?"
   - If YES → Get path, extract solution details for Section 4
   - If NO → Generate Section 4 from brief alone

2. **Future roadmap?** "Include future phases / Phase 2 roadmap?"
   - If YES → Add 1-2 slides showing expansion possibilities
   - If NO → Skip section, keep focused on current scope

3. **Solution personification?** "Would you like to give the solution a memorable name (like 'Noura')?"
   - If YES → Ask for name or suggest based on solution type
   - If NO → Use generic references ("The Solution", "The System")

**Step 3: Gather Ongoing Costs**

Ask about ongoing costs for this specific project:

1. "Which API costs will the client incur monthly?" (WhatsApp, OpenAI, etc.)
2. "Will you offer a maintenance retainer? Monthly/annual fee?"
3. "Does this solution require client-paid hosting?"

Store answers for Investment section.

**Step 4: Gather Pricing**

Default pricing ranges by solution type:
- WhatsApp AI Agent: $1,500-$3,500
- Lead Generation System: $2,000-$5,000
- Content Automation: $1,500-$4,000
- CRM Integration: $1,000-$3,000

Ask: "Confirm or adjust the pricing tiers:
- Essential: $[default_low]
- Recommended: $[default_mid]
- Premium: $[default_high]"

**Step 5: Select Case Study**

Read `references/case-studies.md` for selection logic.

Match based on:
1. Industry match (exact > related > any)
2. Solution type match (exact > similar)
3. Metric relevance (prioritize metrics client cares about)

If no good match, use industry statistics and benchmarks instead.

**Step 6: Generate Proposal**

Read `templates/PROPOSAL.md` and fill each section:

1. **Title & Context**
   - Project name with tagline
   - Client name + iSemantics branding

2. **Executive Summary** (CRITICAL - 80% only read this)
   - Client's problem in their language
   - Solution in one paragraph
   - Key business outcome WITH NUMBER
   - Investment range and timeline
   - Single clear CTA

3. **The Problem & Opportunity**
   - Market context with data (industry-specific)
   - Client's current situation (from brief)
   - Cost of inaction (quantified)
   - Why now

4. **The Solution**
   - Overview with personified name if chosen
   - Capabilities as WORKFLOW, not feature list
   - How it addresses each problem
   - Sample interaction (brief)
   - High-level technical approach

5. **Proof & Credibility**
   - Selected case study with metrics
   - Industry statistics supporting ROI
   - Social proof if available

6. **What's Delivered**
   - Clear scope bullets
   - Included vs not included
   - Integration points
   - Future phases (if roadmap included)

7. **Timeline**
   - Phase breakdown with milestones
   - Client responsibilities
   - Go-live expectations

8. **Investment Options**
   - Three tiers with clear differentiation
   - Mark Recommended option
   - ROI calculation for each
   - "Best for whom" guidance

9. **Competitive Positioning**
   - Price vs Value chart (read `references/competitive-positioning.md`)
   - Comparison table vs alternatives

10. **Ongoing Costs**
    - API fees (from Step 3)
    - Maintenance options
    - Hosting if applicable
    - What's included in initial investment vs ongoing

11. **ROI Framework**
    - Time savings calculation
    - Revenue impact calculation
    - Payback period
    - Comparison to alternatives

12. **Terms & Next Steps**
    - Payment schedule (milestone-based)
    - Scope boundaries
    - Next steps with clear CTA
    - Timeline to start if signed by X date

13. **Future Roadmap** (if included)
    - Phase 2 possibilities
    - How current solution enables expansion

**Step 7: Validate with User**

Present summary:
"Based on the brief:
- Client: [name], Industry: [industry]
- Problem: [1-sentence summary]
- Solution: [solution type]
- Pricing: Essential $X / Recommended $Y / Premium $Z
- Case study: [selected or "industry benchmarks"]

Does this capture the project correctly? Anything to adjust before I generate the full proposal?"

**Step 8: Deliver**

Write proposal to suggested path (or user-specified):
- Default: `.proposals/[client-name]-proposal.md`
- Or client-specified location

Summarize: "Proposal generated with [N] sections, [X] slides. Pricing: $[low]-$[high]. Ready for review."

</process>

<output_format>
The proposal is generated as a single markdown file following `templates/PROPOSAL.md` structure. Each major section maps to 1-4 slides when converted to presentation format.

For markdown-to-PDF conversion, recommend tools like Marp, Slidev, or Pandoc. This conversion is Phase 2 functionality (not yet implemented).
</output_format>

<success_criteria>
Workflow is complete when:

- [ ] All required fields extracted or gathered
- [ ] Optional preferences collected (tech plan, roadmap, personification)
- [ ] Ongoing costs documented
- [ ] Pricing confirmed for all three tiers
- [ ] Case study selected or benchmarks identified
- [ ] Full proposal generated using template
- [ ] User validated the summary
- [ ] Proposal written to file
</success_criteria>
