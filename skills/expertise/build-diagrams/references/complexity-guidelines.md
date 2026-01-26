<overview>
Diagram complexity directly impacts readability. Complex diagrams become unreadable "hairballs." This reference provides limits and strategies for managing complexity.
</overview>

<limits>
## Complexity Limits

| Metric | Recommended | Warning | Split Required |
|--------|-------------|---------|----------------|
| Nodes per diagram | ≤15 | 15-25 | >25 |
| Edges per node (avg) | ≤3 | 3-5 | >5 |
| Nesting depth | ≤3 | 4 | >4 |

**Platform-specific:**
- GitHub: Max ~30 nodes for reliable rendering
- VSCode: Can handle ~50+ nodes
- Mermaid Live: Can handle larger diagrams but readability suffers
</limits>

<when_to_split>
## When to Split a Diagram

Split when any of these are true:
- Doesn't fit on one screen without scrolling
- Labels overlap or become unreadable
- Relationships form a "hairball" pattern (everything connects to everything)
- Different audiences need different detail levels
- More than 25 nodes
- Average edges per node exceeds 5
</when_to_split>

<splitting_strategies>
## Splitting Strategies

<by_abstraction>
**By abstraction level (C4 style):**
1. Overview diagram: System context (high-level, few nodes)
2. Detail diagrams: Container/component views (focused areas)

Example:
- `system-context.md` - 5-10 nodes showing actors and system
- `auth-container.md` - 10-15 nodes showing auth subsystem
- `payment-container.md` - 10-15 nodes showing payment subsystem
</by_abstraction>

<by_functional_area>
**By functional area:**
- Authentication flow
- Data processing pipeline
- Error handling paths
- User journey

Each area becomes its own focused diagram.
</by_functional_area>

<by_sequence_phase>
**By sequence phase:**
- Setup/initialization
- Main flow (happy path)
- Error handling
- Cleanup/teardown

Especially useful for long sequence diagrams.
</by_sequence_phase>

<by_audience>
**By audience:**
- Executive summary (simple, 5-10 nodes)
- Technical overview (moderate, 15-20 nodes)
- Implementation detail (focused, 10-15 nodes per area)
</by_audience>
</splitting_strategies>

<labeling>
## Labeling Conventions

Good labels make diagrams self-documenting.

<nodes>
**Nodes: Noun phrases, 2-4 words max**
- Good: "User", "Payment Service", "Order Database"
- Bad: "The user who initiated the request", "PaymentProcessingServiceImpl"
</nodes>

<edges>
**Edges/Relationships: Verb phrases**
- Good: "sends to", "authenticates with", "stores in", "reads from"
- Bad: "connection", "link", "data"
</edges>

<subgraphs>
**Subgraphs: Functional area names**
- Good: "Authentication", "Data Layer", "UI Components"
- Bad: "Group 1", "Section A", "Part 2"
</subgraphs>

<general_rules>
**General rules:**
- Be specific but concise
- Use consistent terminology throughout
- Match domain vocabulary (what the team calls things)
- Avoid abbreviations unless universally understood
</general_rules>
</labeling>

<llm_generation>
## LLM Diagram Generation Best Practices

When generating diagrams with Claude:

<do_list>
**Do:**
1. Specify exact diagram type upfront
2. Describe elements and relationships clearly
3. Set constraints ("keep under 15 nodes")
4. Specify theme preference (light/dark)
5. Mention target platform (GitHub/VSCode)
6. Start simple, then iterate to add detail
</do_list>

<dont_list>
**Don't:**
1. Let Claude choose diagram type without guidance
2. Request >25 nodes in one diagram
3. Expect interactive features for GitHub target
4. Mix diagram types in one code block
5. Skip validation step
</dont_list>

<iterative_approach>
**Iterative refinement approach:**
1. Start simple: Basic structure with key elements
2. Add detail: "Now add error handling paths"
3. Apply style: "Apply dark theme colors"
4. Validate: "Ensure this renders in GitHub"
5. Split if needed: "This is too complex, let's split by..."
</iterative_approach>
</llm_generation>

<common_mistakes>
## Common LLM Mistakes to Catch

| Mistake | Example | Fix |
|---------|---------|-----|
| Invalid sequence arrows | `A -> B` | Use `A ->> B` |
| Wrong diagram type | Flowchart for states | Use `stateDiagram-v2` |
| Over-complexity | 50+ nodes | Split into multiple diagrams |
| Using click events | For GitHub target | Remove - not supported |
| Color names | `fill:blue` | Use `fill:#1976D2` |
| Missing type declaration | No first line | Add `flowchart LR` etc. |
</common_mistakes>
