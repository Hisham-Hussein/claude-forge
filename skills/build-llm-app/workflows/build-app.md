# Workflow: Build LLM Application

<required_reading>
Load references progressively as you reach each phase:

- **Phase 1 (Pattern):** `references/agent-patterns.md`
- **Phase 2 (Tools):** `references/tool-design.md`
- **Phase 3 (Context):** `references/context-and-rag.md`
- **Phase 4 (Reliability):** `references/reliability.md`
</required_reading>

<process>

<phase name="1" title="Understand the Application">

**Ask clarifying questions:**

1. What is the core task? (research, process data, answer questions, take actions)
2. What inputs will it receive? (user queries, documents, API data)
3. What outputs should it produce? (answers, reports, actions, files)
4. What external services/APIs will it need?

**Capture answers before proceeding.**
</phase>

<phase name="2" title="Select Agent Pattern">

**Read:** `references/agent-patterns.md`

**Apply the decision tree:**

```
Simple + focused task? → Single Agent
Parallelizable subtasks? → Orchestrator-Workers
Different domains? → Multi-Agent Handoffs
Hierarchical expertise? → Subagents as Tools
```

**Confirm pattern with user:**
"Based on [reasoning], I recommend [pattern]. Does this fit your needs?"

**Document the choice and rationale.**
</phase>

<phase name="3" title="Design Tools">

**Read:** `references/tool-design.md`

**For each capability the agent needs:**

1. Define the tool's single responsibility
2. Specify input parameters (typed, documented)
3. Specify output schema (explicit, consistent)
4. Add input validation (fail fast)
5. Design error responses (actionable)
6. Consider idempotency

**Output:** List of tools with signatures:
```python
def tool_name(param1: type, param2: type) -> ReturnType:
    """One-line description.

    Args:
        param1: Description
        param2: Description

    Returns:
        {field1: type, field2: type}

    Errors:
        {error: message, suggestion: how_to_fix}
    """
```

**Review checklist with user before proceeding.**
</phase>

<phase name="4" title="Design Context Strategy">

**Read:** `references/context-and-rag.md`

**Determine what context the agent needs:**

| Include | Exclude |
|---------|---------|
| System prompt (role, capabilities) | Full conversation history |
| Current task | Irrelevant tool results |
| Relevant tool results | System internals |
| Retrieved docs (if RAG) | Credentials/secrets |

**If RAG is needed:**

1. Choose retrieval strategy (semantic, keyword, hybrid)
2. Define chunking approach
3. Plan context injection format
4. Add faithfulness instructions

**Output:** Context management plan.
</phase>

<phase name="5" title="Add Reliability">

**Read:** `references/reliability.md`

**Error handling checklist:**

- [ ] Tool failures → Retry with backoff
- [ ] Invalid tool calls → Reprompt agent
- [ ] Agent loops → Max iterations limit
- [ ] Context overflow → Summarize/truncate
- [ ] Rate limits → Wait or fallback

**Safety checklist:**

- [ ] Input validation (prompt injection, PII)
- [ ] Output filtering (harmful content, leaked prompts)
- [ ] Scope limiting (least privilege tools)
- [ ] Human-in-the-loop for destructive actions

**Output:** Reliability and safety plan.
</phase>

<phase name="6" title="Produce Deliverables">

**Ask user what they want:**

1. **Design document only** - Summary of all decisions
2. **Starter templates** - Code scaffolds to build from
3. **Both**

**If design document:**
Produce markdown summarizing: pattern, tools, context strategy, reliability plan.

**If starter templates:**
Produce Python scaffolds for: agent loop, tool definitions, context manager.

**Review output with user.**
</phase>

</process>

<success_criteria>
This workflow is complete when:

- [ ] Application requirements understood
- [ ] Agent pattern selected with rationale
- [ ] Tools designed with signatures and error handling
- [ ] Context strategy defined (including RAG if needed)
- [ ] Reliability and safety measures specified
- [ ] Deliverables produced and reviewed with user
</success_criteria>
