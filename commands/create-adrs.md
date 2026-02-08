---
description: Expand ADR stubs from the architecture document into formal Architecture Decision Records using tech stack research
argument-hint: [arch-doc-path] [tech-stack-path]
---

<objective>
Expand Architecture Decision Record (ADR) stubs from the architecture document into formal, standalone ADR records by cross-referencing with tech stack research documentation.

This bridges the gap between the tech-agnostic architecture document (which contains only ADR stubs) and the tech stack research (which contains detailed rationale, alternatives, and trade-offs). The result is a concise, scannable ADR document that any future session can read in seconds to understand what technology decisions were made and why.

Position in charter pipeline: runs after `/create-design-doc` and before `/create-roadmap`.
</objective>

<context>
Architecture document: @$1
Tech stack research: @$2

If no arguments provided, use these defaults:
- Architecture doc: `.charter/ARCHITECTURE-DOC.md`
- Tech stack research: look for tech stack research in `artifacts/research/` (e.g., `stack-recommendations.md`, `tech-stack.md`, or similar)

If the tech stack research file cannot be found, ask the user for its location.
</context>

<process>
1. **Load inputs**
   - Read the architecture document and locate the "Architecture Decisions" section (typically Section 9)
   - Extract all ADR stubs from the decisions table (ADR number, decision title, status)
   - Read the tech stack research document for detailed rationale

2. **Cross-reference and expand**
   - For each ADR stub, find the corresponding section in the tech stack research that provides:
     - The context (what problem or requirement drove this decision)
     - The decision made (specific technology or approach chosen)
     - Alternatives that were considered (with brief reasons for rejection)
     - Consequences (trade-offs, limitations, fallback plans)
   - If an ADR stub has no corresponding detail in the tech research (e.g., an architectural pattern decision), derive the rationale from the architecture document itself

3. **Generate ADRs document**
   - Write each ADR in this exact format:
     ```
     ## ADR-NNN: [Decision Title]
     **Status:** Accepted | Proposed | Superseded
     **Context:** 1-2 sentences on the problem or requirement
     **Decision:** 1 sentence stating the choice
     **Alternatives:** Bullet list of alternatives considered (1 line each)
     **Consequences:** Bullet list of trade-offs and implications (1 line each)
     ```
   - Keep each ADR to 5-10 lines maximum -- this is a reference document, not a research paper
   - Include a summary table at the top listing all ADRs with their status

4. **Write output**
   - Save to `.charter/ADRs.md` (same directory as the architecture document)
</process>

<output>
Files created:
- `.charter/ADRs.md` -- Formal Architecture Decision Records expanded from stubs
</output>

<verification>
Before completing, verify:
- Every ADR stub from the architecture document has a corresponding full ADR
- Each ADR has all five fields: Status, Context, Decision, Alternatives, Consequences
- No ADR exceeds 10 lines
- The summary table at the top matches the individual ADR entries
- Cross-reference accuracy: decisions match what the tech stack research recommends
</verification>

<success_criteria>
- All ADR stubs from the architecture document are expanded into formal records
- Each record is concise (5-10 lines) and self-contained
- Tech stack decisions are traceable to research rationale
- The document is scannable -- a new session can understand all tech decisions in under 60 seconds
- Output written to `.charter/ADRs.md`
</success_criteria>
