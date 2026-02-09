<objective>
Review the "create-architecture-doc" workflow from the create-design-docs skill for critical gaps against software architecture documentation best practices. Use a sub-agent to perform the review, then critically evaluate each finding.
</objective>

<context>
The create-design-docs skill produces three types of documents: Design Doc (lightweight), Architecture Doc (comprehensive), and Hybrid. This review focuses ONLY on the Architecture Document route.

The skill files to review:

**Main workflow:** `skills/create-design-docs/workflows/create-architecture-doc.md`
**Skill entry point:** `skills/create-design-docs/SKILL.md`
**Template:** `skills/create-design-docs/templates/architecture-doc-template.md`
**References:**
- `skills/create-design-docs/references/methodology.md` — Google Design Docs, C4, arc42, ADRs
- `skills/create-design-docs/references/domain-modeling.md` — DDD patterns
- `skills/create-design-docs/references/clean-architecture.md` — Layer definitions, dependency rule
- `skills/create-design-docs/references/data-api-extraction.md` — Extracting from data models and API specs
</context>

<process>

## Step 1: Read All Skill Files

Read every file listed in the context section above. You need the full picture before spawning the review agent.

## Step 2: Spawn Review Sub-Agent

Use the Task tool with `subagent_type: "general-purpose"` to spawn a sub-agent with the following prompt. Include the FULL content of every skill file you read in Step 1 inside the prompt (the sub-agent cannot read files itself — you must embed the content).

The sub-agent prompt should instruct it to:

1. **Review the architecture doc workflow** against established best practices for software architecture documentation, drawing from recognized frameworks and standards including:
   - ISO/IEC 42010 (architecture description standard)
   - arc42 template (12 sections)
   - C4 Model (Simon Brown)
   - SEI/CMU architecture documentation approaches (Views and Beyond)
   - IEEE 1471/42010 stakeholder-viewpoint approach
   - Domain-Driven Design strategic patterns (bounded contexts, context mapping)
   - The "4+1" architectural view model (Kruchten)

2. **Identify ONLY critical or very important gaps** — things that, if missing, would make the architecture document fundamentally incomplete, misleading, or unable to serve its purpose. Skip nice-to-haves, minor improvements, or stylistic preferences.

3. **For each gap found**, the sub-agent must provide:
   - A clear title for the gap
   - What is missing or inadequate
   - Why this is critical (what goes wrong without it)
   - What the best practice recommends
   - Specific evidence from the skill files showing the gap

4. **Explicitly state** if the sub-agent finds NO critical gaps — an empty finding list is a valid and valuable outcome.

## Step 3: Review Each Sub-Agent Finding

After receiving the sub-agent's findings, critically evaluate EACH issue raised:

For every single finding:

1. **State your verdict**: AGREE, DISAGREE, or PARTIALLY AGREE
2. **Provide your reasoning**: Why you agree or disagree, with specific references to:
   - The actual skill file content (quote specific sections)
   - Your own knowledge of architecture documentation best practices
   - Whether the gap would truly cause problems in practice or is more theoretical
3. **If you partially agree**: Explain which part you agree with and which part you don't, and why
4. **Assess severity independently**: Even if you agree a gap exists, you may disagree on whether it's truly "critical" — say so

Be genuinely critical of the sub-agent's analysis. Don't rubber-stamp everything. Some findings may be theoretically correct but practically irrelevant for the skill's scope and target audience (agile teams producing architecture docs from requirements artifacts). Others may seem minor but actually be fundamental. Use your judgment.

## Step 4: Write Summary Report

After reviewing all findings, write a summary report to `./reviews/arch-doc-skill-review.md` with:

1. **Executive Summary**: One paragraph on the overall health of the architecture doc workflow
2. **Sub-Agent Findings with Your Critique**: Each finding followed by your verdict and reasoning
3. **Final Assessment**: Your independent conclusion on whether the skill has critical gaps that need fixing, organized as:
   - Confirmed critical gaps (you agreed with the sub-agent)
   - Disputed findings (you disagreed)
   - Downgraded findings (sub-agent said critical, you say nice-to-have)
   - Any critical gaps YOU noticed that the sub-agent missed

</process>

<constraints>
- Focus ONLY on the architecture document route (Option 2 in the skill's routing), NOT the design doc or hybrid routes
- "Critical gap" means: without addressing this, the produced architecture document would be fundamentally deficient for its stated purpose of guiding implementation
- Do NOT flag the skill for not covering things it explicitly delegates elsewhere (e.g., ADRs are handled by a separate create-adrs skill)
- The skill is designed for AI-assisted generation from requirements artifacts — evaluate it in that context, not as a manual documentation guide for human architects
- Do NOT include nice-to-haves, minor improvements, or subjective preferences in the review
</constraints>

<verification>
Before completing:
- [ ] All skill files were read
- [ ] Sub-agent was spawned with full file content embedded in its prompt
- [ ] Every sub-agent finding received an explicit AGREE/DISAGREE/PARTIALLY AGREE verdict with reasoning
- [ ] Summary report written to `./reviews/arch-doc-skill-review.md`
- [ ] Your own independent assessment is included (gaps the sub-agent may have missed)
</verification>
