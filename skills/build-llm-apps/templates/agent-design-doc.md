# LLM Application Design Document

## Overview

**Application Name:** [Name]
**Pattern:** [Single Agent / Orchestrator-Workers / Subagents as Tools / Multi-Agent Handoffs]
**Pattern Rationale:** [Why this pattern fits the use case]

## Requirements

**Core Task:** [What the application does]
**Inputs:** [What it receives]
**Outputs:** [What it produces]
**External Services:** [APIs, databases, etc.]

## Agent Architecture

```
[Diagram or description of agent flow]
```

## Tools

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| [tool_name] | [description] | [params] | [return type] |

## Context Strategy

**System Prompt:** [Role, capabilities, constraints]

**Context Window Management:**
- [Sliding window / Summarization strategy]
- [RAG if applicable]

**RAG Strategy (if applicable):**
- Retrieval: [Semantic / Keyword / Hybrid]
- Chunking: [Strategy]
- Injection: [Format]

## Reliability

**Error Handling:**
- [ ] Tool retry with backoff
- [ ] Invalid call reprompting
- [ ] Max iteration limits
- [ ] Context overflow handling

**Safety Guardrails:**
- [ ] Input validation
- [ ] Output filtering
- [ ] Scope limiting
- [ ] Human-in-the-loop for: [list actions]

## Implementation Notes

[Any additional notes, constraints, or considerations]
