---
name: build-llm-app
description: Guide building LLM applications with pattern selection, tool design, context engineering, and safety guardrails. Use when building agents, designing agent tools, adding RAG, creating LLM-powered features, or asking how to structure an AI application.
---

<essential_principles>

**Core insight:** Agents decide WHAT to do; execution scripts DO it. This separation keeps LLM non-determinism contained while business logic remains reliable.

<pattern_selection>
Choose the simplest pattern that solves the problem. See `references/agent-patterns.md` for full decision tree.

| Pattern | Complexity | Best For |
|---------|------------|----------|
| Single Agent | Low | Simple focused tasks |
| Orchestrator-Workers | Medium | Parallel subtasks |
| Subagents as Tools | Medium-High | Hierarchical expertise |
| Multi-Agent Handoffs | High | Domain switching |

Quick check: Simple task? → Single Agent. Parallel subtasks? → Orchestrator. Domain switching? → Handoffs. Otherwise → Subagents as Tools.
</pattern_selection>

<tool_design_checklist>
**Every tool must:**

- [ ] Do one thing well (single responsibility)
- [ ] Have typed, documented parameters
- [ ] Return explicit, consistent output schema
- [ ] Validate inputs before executing (fail fast)
- [ ] Return actionable error messages
- [ ] Be idempotent where possible
</tool_design_checklist>

<anti_patterns>
| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| God tool | Tool does everything | Split into focused tools |
| Cryptic errors | Agent can't recover | Return actionable messages |
| Deep nesting | Debugging nightmare | Max 2 levels of subagents |
| No loop limit | Infinite loops | Set max_iterations |
| No timeouts | Hanging requests | Use timeouts |
| Full history | Token explosion | Sliding window + summary |
</anti_patterns>

</essential_principles>

<intake>
**What are you building?**

Describe your LLM application (e.g., "an agent that researches companies", "RAG for internal docs", "tool-using assistant").

**Wait for response, then route to workflow.**
</intake>

<routing>
After user describes their application:

1. Read `workflows/build-app.md`
2. Follow the workflow exactly, loading references as needed

The workflow guides through: Pattern Selection → Tool Design → Context Engineering → RAG (if needed) → Error Handling → Safety
</routing>

<reference_index>
All domain knowledge in `references/`:

**Patterns:** agent-patterns.md (single agent, orchestrator, subagents, handoffs)
**Tools:** tool-design.md (principles, contracts, idempotency, errors)
**Context:** context-and-rag.md (what to include/exclude, RAG strategies)
**Reliability:** reliability.md (error handling, loop prevention, safety guardrails)
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| build-app.md | Single guided flow through all design decisions |
</workflows_index>

<templates_index>
Output templates in `templates/`:

| Template | Purpose |
|----------|---------|
| agent-design-doc.md | Design document structure for LLM applications |
| tool-contract.py | Python template for tool signatures with validation |
| context-strategy.md | Context window and RAG configuration template |
</templates_index>

<success_criteria>
LLM application design is complete when:

- Agent pattern selected with documented rationale
- Tools designed with typed contracts and error handling
- Context strategy defined (window management + RAG if needed)
- Reliability measures specified (retries, loops, timeouts)
- Safety guardrails added (input/output validation, HITL)
</success_criteria>
