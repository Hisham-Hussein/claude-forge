# Context Strategy Template

## Context Budget

| Component | Token Budget | Notes |
|-----------|--------------|-------|
| System Prompt | ~500 | Fixed, always present |
| Retrieved Context (RAG) | ~2000 | Variable, compress if needed |
| Conversation History | ~1500 | Sliding window + summarization |
| Current Turn | ~500 | User message + recent tool results |
| Response Reserve | ~2000 | Space for model output |
| **Total** | ~6500 | Adjust based on model limits |

## System Prompt

```
You are [role] that [capabilities].

Your tools:
- [tool_name]: [one-line description]

Constraints:
- [constraint 1]
- [constraint 2]

When responding:
- [behavior guideline]
```

## Window Management

**Strategy:** [Sliding window / Semantic filtering / Compression]

**Rules:**
- Keep last [N] messages in full
- Summarize older messages using: [summarization approach]
- Tool results: [include all / filter relevant / compress]

## RAG Configuration (if applicable)

**Retrieval:**
- Strategy: [Semantic / Keyword / Hybrid]
- Top-k: [number]
- Reranking: [yes/no, method]

**Chunking:**
- Chunk size: [tokens/characters]
- Overlap: [tokens/characters]
- Splitting: [paragraph / sentence / semantic]

**Injection Format:**
```
<context>
Source: [document_name]
---
[chunk_content]
</context>

Answer based ONLY on the context above.
```

**Faithfulness Instructions:**
- [ ] "Answer ONLY based on provided context"
- [ ] "Include source references for claims"
- [ ] "If context doesn't contain the answer, say 'I don't know'"

## Exclusions

Never include in context:
- [ ] Credentials/secrets
- [ ] Full conversation history (summarize instead)
- [ ] System internals
- [ ] Irrelevant tool results
