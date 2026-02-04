<overview>
**Status:** Planned (not yet implemented)

This workflow will guide users through structured intake to create a client brief when they don't have one ready.
</overview>

<process>
For now, use generate-from-brief.md and provide information interactively. The skill will ask for missing fields.

**Future implementation will include:**
1. Structured interview questions
2. Brief template generation
3. Discovery call note extraction
4. Export to standard brief format
</process>

<workaround>
To create a brief manually, use this structure:

```markdown
# Client Brief: [Client Name]

## Client Info
- **Company:** [Name]
- **Industry:** [e.g., SaaS, Real Estate, Marketing Agency]
- **Website:** [URL]

## The Problem
[2-3 sentences describing their pain point]

## What They Want
- **Solution Type:** [e.g., WhatsApp AI Agent, Lead Generation System]
- **Key Outcomes:** [What success looks like]
- **Integrations Needed:** [CRM, Calendar, etc.]

## Budget & Timeline
- **Budget Range:** [e.g., $1,500-$3,000]
- **Timeline:** [When do they want to start/launch?]

## Additional Context
[Any other relevant info]
```

Then use `/generate-proposals` with option 1 (Generate from brief).
</workaround>
