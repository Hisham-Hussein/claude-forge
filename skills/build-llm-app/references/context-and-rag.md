<overview>
Context engineering manages what the agent "knows" at each step. Too little context = wrong decisions. Too much = confused and expensive. RAG extends context with retrieved documents.
</overview>

<context_management>
<what_to_include>
| Context Type | When to Include | Example |
|--------------|-----------------|---------|
| System prompt | Always | Role, capabilities, constraints |
| Current task | Always | User's request |
| Tool results | After tool calls | API responses, search results |
| Conversation history | For multi-turn | Previous messages |
| Retrieved docs | For RAG | Relevant document chunks |
</what_to_include>

<what_to_exclude>
| Context Type | Why Exclude | Alternative |
|--------------|-------------|-------------|
| Full conversation history | Token waste | Summarize older messages |
| Irrelevant tool results | Noise | Filter before injecting |
| System internals | Confusion | Keep in execution layer |
| Credentials/secrets | Security | Use environment variables |
</what_to_exclude>

<window_management>
```
┌─────────────────────────────────────────────┐
│ System Prompt (fixed, ~500 tokens)          │
├─────────────────────────────────────────────┤
│ Retrieved Context / RAG (variable)          │  ← Compress if needed
├─────────────────────────────────────────────┤
│ Conversation History (sliding window)       │  ← Summarize old messages
├─────────────────────────────────────────────┤
│ Current Turn (user message + tool results)  │
├─────────────────────────────────────────────┤
│ Reserved for response (~2000 tokens)        │
└─────────────────────────────────────────────┘
```

**Strategies:**

- **Sliding window:** Keep last N messages, summarize older ones
- **Semantic filtering:** Only include messages relevant to current task
- **Compression:** Use smaller model to summarize verbose tool outputs
</window_management>
</context_management>

<rag_integration>
<when_to_use_rag>
| Use RAG When | Use Pure Agent When |
|--------------|---------------------|
| Answer requires specific facts from docs | Task is action-oriented |
| Knowledge changes frequently | Knowledge is stable/trained |
| Accuracy and citations matter | Creativity/reasoning matters |
| Domain is specialized | Domain is general |
</when_to_use_rag>

<retrieval_strategies>
| Strategy | How It Works | Best For |
|----------|--------------|----------|
| Semantic | Embed query, find similar chunks | Conceptual questions |
| Keyword | BM25/TF-IDF matching | Specific terms, names |
| Hybrid | Combine semantic + keyword | General purpose |
| Reranking | Retrieve many, rerank top-k | High precision needs |
</retrieval_strategies>

<context_injection_pattern>
```
┌─────────────────────────────────────────────┐
│ User Query: "What is our refund policy?"    │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Retriever: Find relevant chunks             │
│ → chunk_1: "Refunds are processed..."       │
│ → chunk_2: "30-day return window..."        │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Prompt to LLM:                              │
│                                             │
│ Context:                                    │
│ [chunk_1]                                   │
│ [chunk_2]                                   │
│                                             │
│ Question: What is our refund policy?        │
│                                             │
│ Answer based ONLY on the context above.     │
└─────────────────────────────────────────────┘
```
</context_injection_pattern>

<faithfulness>
The agent should answer based on retrieved context, not hallucinate.

**Techniques:**

- **Explicit instruction:** "Answer ONLY based on the provided context"
- **Citation requirement:** "Include source references for claims"
- **Abstain option:** "If context doesn't contain the answer, say 'I don't know'"
</faithfulness>
</rag_integration>

<structured_output>
Use XML or JSON for reliable parsing of agent responses.

<xml_format>
```xml
<!-- XML format (Claude excels at this) -->
<thinking>
I need to search for the user's account first.
</thinking>
<action>
<tool>get_user</tool>
<input>{"email": "user@example.com"}</input>
</action>
```
</xml_format>

<json_format>
```json
{
  "thinking": "I need to search for the user's account first.",
  "action": {
    "tool": "get_user",
    "input": {"email": "user@example.com"}
  }
}
```
</json_format>
</structured_output>
