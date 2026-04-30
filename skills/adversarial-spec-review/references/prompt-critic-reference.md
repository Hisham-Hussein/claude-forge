# Prompt Critic — Deep Reference

Read this file when reviewing a spec that creates or modifies LLM prompts. The archetype definition in `reviewer-archetypes.md` provides the core principles inline. This file provides the deeper context, examples, and research-backed rationale.

## The Three-Layer Responsibility Split — In Depth

### Why three layers, not two or one

The naive approach is a single function: fetch data, build prompt, call LLM, parse output. This works for prototypes but fails in production because:

- **Testability collapses.** You can't unit test the prompt without mocking the data source AND the LLM. You can't integration test the data fetch without running the LLM.
- **Deterministic values get hallucinated.** If the LLM needs to count "how many posts use Question hooks," and you pass it raw data, it will count wrong. LLMs are unreliable at arithmetic over long contexts. Code is not.
- **Prompt iteration is expensive.** Changing the prompt text requires re-running the entire pipeline (fetch + LLM call). With a pure prompt module, you can iterate on prompt text with cached input data — no API calls needed.

### Layer 1: Caller — What to look for

The caller is where all computation happens. When reviewing, verify:

- **Aggregations:** Counts, averages, distributions, rankings — anything the LLM would need to "count" should be pre-computed. Example: "Hook type distribution: Question 7/15 (47%), Bold Claim 4/15 (27%)" should be computed in TypeScript, not derived by the LLM from reading 15 samples.
- **Filtering and sorting:** Which items to include, in what order — deterministic decisions.
- **Typed input construction:** The caller builds an object conforming to the prompt module's input Zod schema. This is the contract between layers.

**Red flags in the caller:**
- Prompt text strings constructed here (should be in the prompt module)
- LLM calls made here (should be through the provider)
- Business logic mixed with prompt assembly

### Layer 2: Prompt Module — What to look for

The prompt module is a pure function. When reviewing, verify:

- **No imports of data-fetching modules.** The prompt module should import only types, schemas, and constants — never repositories, adapters, or API clients.
- **No async code.** `assemblePrompt()` should be synchronous. If it's async, something is being fetched inside it.
- **Deterministic output.** Given the same input, `assemblePrompt()` must produce exactly the same strings every time. No `Date.now()`, no `Math.random()`, no external state.
- **Version tracking.** Every prompt module should export a `promptVersion` string. When the prompt text changes materially, the version should be bumped.

**Red flags in the prompt module:**
- `await` anywhere in `assemblePrompt()`
- Imports from adapter packages
- Computation (loops that aggregate, filter, or transform — these belong in the caller)
- Hardcoded values that should come from the input schema

### Layer 3: LLM Provider — What to look for

The provider sends the prompt and validates the response. When reviewing, verify:

- **Output schema enforcement.** The provider should use structured output mode (`generateObject`, `response_format`) with the Zod output schema. The prompt should not need to repeat format instructions that the schema already enforces.
- **No prompt construction.** The provider receives `{ system, user }` strings. It should not modify, wrap, or augment them.
- **Error handling.** Parse failures, timeout, rate limits — the provider handles these and returns a typed error, not a thrown exception.

## Prompt Engineering Quality — Research-Backed Checklist

### Instructions vs Examples

Research finding: "Every behavior shown in examples must also be stated in instructions" (OpenAI GPT-4.1 guide). Instructions and examples serve different roles:

| Purpose | Instructions (rules) | Examples (demonstrations) |
|---|---|---|
| Define behavior | Primary mechanism | Illustrates, does not define |
| Show format/structure | Weak — prose is ambiguous | Strong — concrete is learned by exposure |
| Demonstrate tone | Weak — "be warm" is vague | Strong — the model mimics what it sees |
| Prevent bad output | Strong — "never do X" | Risky — showing bad output can prime it |

**Review check:** For each behavior the prompt expects, verify it appears in BOTH instructions AND examples (if examples exist). For negative constraints ("never use these phrases"), verify they're stated as instructions, not shown as negative examples.

### Structural Delineation

Research finding: XML tags outperform loose text for section delineation in complex prompts. Markdown headers work well for simple prompts.

**Decision framework:**
- **Simple prompt** (single task, no multi-section data): Markdown with `---` separators and `**bold**` labels is sufficient.
- **Complex prompt** (multiple data sections, per-item metadata, aggregate summaries, multiple output field definitions): XML tags prevent ambiguity between sections and let the model locate information without scanning.

**Review check:** For complex prompts, verify each section is unambiguously delineated. Can you point to exactly where the "summary" section ends and the "samples" section begins? If the boundaries are fuzzy, the model will be confused too.

### Token Efficiency

Research finding: Context rot is real — model recall accuracy decreases as token count increases. The goal is the smallest set of high-signal tokens, not "include everything."

**Token budget estimation:**

| Component | Typical range |
|---|---|
| System prompt (role, instructions) | 300-800 tokens |
| Field/output definitions | 200-500 tokens |
| Aggregate summary | 200-500 tokens |
| Per-item data (N items) | N x 200-800 tokens |
| Anti-pattern list | 100-200 tokens |
| **Total** | Depends on N |

**Review check:** Estimate the token count for the maximum expected input. Is it within model limits with 2x margin? Are there tokens that don't contribute to the task (redundant instructions, bulk-loaded context, values the LLM doesn't use)?

### Output Schema Design

**Structured output enforcement:** When using `generateObject` or equivalent, the Zod schema is compiled to JSON Schema and enforced at the API level. The LLM generates tokens that conform to the schema. This means:

- `.min()` / `.max()` on arrays → `minItems` / `maxItems` in JSON Schema → enforced
- `.enum()` values → restricted to listed values → enforced
- Required vs optional fields → enforced
- Nested objects → enforced

**Review check:** Does the output schema's strictness match the task? Overly strict schemas (e.g., requiring exactly 5 evidence items when sometimes only 3 exist) cause unnecessary failures. Overly loose schemas (all fields optional, no enums) let the LLM produce garbage. Find the right balance.

**Provider-specific gotcha (OpenAI):** Optional fields in OpenAI structured output must use `.nullable().optional()`, not just `.optional()`. The SDK throws if this pattern is not followed. Required fields do not need `.nullable()`.

### Schema Granularity — Match to Consumer

Research finding: Output schemas act as a ceiling on richness, not a floor. When an LLM consumer receives a deeply nested schema with many typed fields, the model compresses its output to fit the structure — losing nuance, context, and quality. Each small string sub-field signals "write a sentence" regardless of what the prompt instructions say. When a code consumer receives a coarse string field, it can't extract structured data without additional parsing.

**The rule:** Match schema granularity to who consumes the output.

| Consumer | Schema design | Example |
|---|---|---|
| **Code** (downstream logic parses fields) | Fine-grained: typed objects, enums, arrays with min/max, nested schemas | `{ "hook_type": enum, "evidence": array of objects (2-5 items) }` |
| **LLM** (another prompt consumes the output) | Coarse: string fields with prompt instructions controlling internal markdown structure | `{ "analysis": string, "recommendations": string }` |
| **Human** (displayed in UI or report) | Medium: top-level typed fields, string bodies for prose sections | `{ "title": string, "score": number, "narrative": string }` |

**Empirical evidence:** In a real production system, restructuring an output schema from 12 nested typed objects to 6 plain string fields — with the same information requested via prompt instructions instead of schema nesting — improved output quality from approximately 40% to approximately 90% as measured by human evaluation. The fix also eliminated serializer/parser layers that existed only to bridge between the structured schema and a string storage format — a code smell that signals the schema is over-structured for its consumer.

**Why this happens:** Structured output mode compiles the schema to JSON Schema and constrains token generation. Every required field, every nested object, every enum becomes a constraint the model must satisfy. With deeply nested schemas, the model allocates tokens to satisfying structural constraints rather than producing thoughtful content. Prompt instructions are more effective than schema constraints for controlling output richness — schemas enforce shape, prompts enforce depth.

**Review check:** For each output schema field, ask: "Who reads this field?" If code reads it, type it precisely. If an LLM or human reads it, consider whether a plain string field with prompt-level instructions would produce better output. Watch for schemas with more than 5 levels of nesting or more than 10 typed fields when the consumer is not code.

**Red flags:**
- Schema with 10+ nested object types when the output is consumed by another LLM prompt or displayed to a human
- Array fields with exact count constraints when the actual count varies — forces the LLM to pad or truncate
- Enum fields for values that are really free-text judgments (e.g., an enum of `["positive", "negative", "neutral"]` for nuanced sentiment)
- Serializer/parser layers that exist only to convert between structured schema output and a string storage format — the schema is over-structured for its consumer
- Schema designed for "maximum type safety" without considering the LLM's ability to produce rich output within those constraints

### Anti-Pattern Lists

Research finding: The combination of positive instructions ("write like this") and negative instructions ("never write like that") is more effective than either alone. But negative *examples* (showing bad output) can prime the model to produce what you showed it.

**Review check:** If the prompt has anti-pattern instructions, verify they're phrased as prohibitions ("do NOT return generic descriptions"), not as examples of bad output.

### Few-Shot Strategy

Research finding: Few-shot examples are the single most reliable lever for steering output format, tone, and structure — but diminishing returns set in fast. Three to five examples is the practical sweet spot.

**Count guidance:**

| Count | Effect | When to use |
|---|---|---|
| 0 (zero-shot) | Baseline. Works for simple tasks with clear instructions. | Format/structure is obvious from the schema; no tone/style matching needed |
| 1 | Large accuracy jump. Often sufficient for format tasks. | Format demonstration only |
| 2-3 | Strong gains. Covers edge cases. | Most production prompts |
| 3-5 | Diminishing returns begin. Sweet spot for complex tasks. | Tone matching, style transfer, nuanced format |
| 5+ | Marginal improvement. Token cost scales linearly. | Only with measured evidence for the specific task |
| 10+ | Risk of degradation with reasoning models. | Avoid unless empirically validated |

**Placement:**
- Place examples after instructions and before per-request context/input (recency bias helps adherence)
- For long-context prompts (20k+ tokens), place long documents at the top with examples near the end
- For structured examples, use XML `<example>` tags (Claude) or a dedicated `# Examples` section (GPT)
- For chat-trained models, conversational few-shot (user/assistant turn pairs) often outperforms single-block injection

**Selection — static vs dynamic:**
- **Static** (same examples every time): Acceptable when the example pool is small (<10) or all examples are relevant to every request
- **Dynamic** (selected at generation time based on similarity to current input): Measurably better when the pool exceeds 10 examples or spans multiple content types. Research shows 5-7% F1 improvement from similarity-based retrieval over random selection.

**Review check:** If the spec includes few-shot examples: (1) Is the count in the 3-5 range, or is there measured justification for a different count? (2) Are examples placed after instructions and before dynamic input? (3) If the example pool is large or spans multiple types, does the spec use dynamic selection? (4) Do any examples contradict the instructions?

**Red flags:**
- 10+ static examples with no evidence they help (token waste + potential degradation)
- Examples placed before instructions (weakens instruction adherence)
- All examples cover the same "type" (model overfits to that type)
- Examples that contradict a stated rule (model may follow example over rule due to recency/concreteness bias)

### Instruction Explicitness — Match to Model

Research finding: Different model generations have different optimal instruction styles. The right level of explicitness depends on which model executes the prompt.

**Model-specific guidance:**

| Model tier | Instruction style | Why |
|---|---|---|
| **GPT-4.1 / GPT-5** | Explicit, structured instructions with clear steps. Spell out the approach. | OpenAI describes GPT models as benefiting from "precise instructions that explicitly provide the logic and data required." Think of them as a skilled junior — they perform best when told exactly what to do. |
| **GPT-5.5+** | Outcome-first: define target outcome, success criteria, constraints. Let the model choose the path. | Newer models handle process selection internally. Over-specifying steps adds noise and narrows their search space. |
| **Reasoning models (o1, o3)** | Goal + constraints only. Minimal process steps. | Step-by-step examples consume reasoning budget the model would use more productively for chain-of-thought. |

**Universal regardless of model:**

- **Avoid extreme over-specification.** Even GPT-4.1 does not need 20 rigid steps for a judgment task. If a step is a true invariant (safety check, required validation), include it. If it is guidance the model could infer, consider whether the target model needs it explicitly stated or can figure it out.
- **Decision rules** ("If X, do Y; otherwise, do Z") work well for conditional behavior across all models. Keep to 3-5 rules.
- **Absolute rules** (`ALWAYS`, `NEVER`, `must`) should be reserved for true invariants — safety rules, required output fields, actions that must never happen (e.g., "NEVER fabricate metrics"). Using absolute language for preferences dilutes the signal of actual invariants.

**Review check:** What model will execute this prompt? Does the instruction style match that model's capabilities? For GPT-4.1: are instructions explicit and structured enough for the model to follow without guessing? For GPT-5.5+: is the prompt over-specifying process steps the model could handle from an outcome description? For any model: are there 10+ rigid steps where most are judgment calls rather than invariants?

**Red flags:**
- Vague outcome-only prompt targeting GPT-4.1 (model needs more explicit guidance)
- 15+ rigid numbered steps targeting a reasoning model (wastes reasoning budget)
- Absolute rules (`ALWAYS`, `NEVER`) used for style preferences rather than safety invariants

### Prompt Ordering and Caching

Research finding: Two ordering principles exist in tension, and the right choice depends on context.

**Comprehension-optimal ordering** (Anthropic): Place long context documents at the top of the prompt, with the query and examples near the end. Testing shows up to 30% improvement in response quality. Reasoning: the model processes the full context before encountering the specific task, so it has maximum attention on the context when forming its response.

**Caching-optimal ordering** (OpenAI): Place static content (system prompt, role, instructions) before dynamic content (per-request context, examples, input). Reasoning: prompt caching works by prefix matching — if the first N tokens are identical across requests, the cached prefix is reused, saving cost and latency.

**When they align:** For most production prompts, the system prompt (role, instructions) is both static and long, so placing it first satisfies both concerns. Dynamic parts (per-request context, examples, generation request) naturally go at the end.

**When they conflict:** If the dynamic context is very long (3,000+ tokens) and the system prompt is short, comprehension-optimal ordering wants the long context first, but caching-optimal ordering wants the static system prompt first.

**Resolution rule:** For high-volume pipelines (many calls with the same system prompt), prefer caching-optimal ordering. For complex one-off prompts or low-volume pipelines, prefer comprehension-optimal ordering.

**Message role priority:** Regardless of ordering, authoritative rules belong in the system/developer message, not the user message. Developer/system messages take priority over user messages regardless of position (OpenAI model spec). For Claude, XML-tagged instructions take slight precedence. Design prompts so the priority chain and positional recency reinforce each other, never compete.

**Review check:** Is the prompt's content ordering intentional? Is static content placed before dynamic content? If the ordering is unusual (dynamic context first, static instructions last), is there a stated reason? Are authoritative rules in the system/developer message, or have they been placed in the user message where they have lower priority?

**Red flags:**
- System prompt changes with every request (defeats caching)
- Authoritative rules placed only in the user message
- Long static preamble followed by short dynamic context, then more static content (cache breaks at the dynamic insertion point)

### Creative Drafting Guardrails

Research finding (OpenAI GPT-5.5 guide): When a prompt combines factual claims with creative generation, models fabricate specific claims (metrics, outcomes, capabilities, dates) to strengthen the draft. The prompt must explicitly partition what must come from context, what may be generated, and what should use placeholders.

**This is domain-agnostic.** Any prompt that retrieves factual context and asks the model to produce creative output from it faces this risk — content generation, report writing, slide creation, email drafting, documentation.

**The guardrail pattern:**

The prompt must distinguish three categories:
1. **Source-backed facts** — claims that must come from retrieved context (documents, data, records). Should be cited or traceable.
2. **Creative framing** — narrative elements the model generates freely (hooks, transitions, analogies, structural choices).
3. **Gaps** — when the task requires a specific claim but context lacks evidence. The prompt should instruct: use `[PLACEHOLDER: description]` or state the assumption explicitly. Never fabricate.

**Review check:** If the prompt retrieves factual context and asks the model to generate prose/content from it, does the prompt explicitly distinguish source-backed facts from creative framing? Does it instruct the model on what to do when evidence is missing?

**Red flag:** A generation prompt that says "use the provided context to write X" without specifying which parts must come from context vs. which parts the model may generate freely. This is where hallucinated specifics appear.

## Common Prompt Spec Issues (From Real Reviews)

1. **"The prompt uses the established format"** — but the spec doesn't show what the actual prompt text says. Verify by reading `assemblePrompt()` output for a concrete input.

2. **Token count ignored.** The spec adds 50 tokens of metadata per item and processes 30 items — that's 1,500 new tokens. At scale, this matters.

3. **Aggregation in the wrong layer.** The spec says "the LLM analyzes the distribution" — but counting is arithmetic, not analysis. Code should count; the LLM should interpret.

4. **Output schema mismatch.** The prompt says "provide 3-5 examples" but the schema has no `.min(3).max(5)` constraint. Or worse: the schema enforces constraints the prompt doesn't mention, confusing the LLM.

5. **Field definitions ambiguous.** Two fields overlap — the spec doesn't say what goes where. The LLM will guess differently each time. Explicit boundary definitions ("this field covers X; that field covers Y; do NOT include Z here") prevent drift.

6. **Version not bumped.** A material prompt change (new fields, restructured instructions, different output format) keeps the old version string. Logs become uninterpretable — you can't tell which prompt version produced which output.

7. **Over-structured schema for LLM consumer.** The spec defines an output schema with 10+ nested types, but the output is consumed by another LLM prompt or displayed to a human. The schema compresses the LLM's output quality — coarse string fields with prompt instructions would produce richer results.

8. **Instruction explicitness mismatched to model.** The spec uses vague outcome-only instructions for GPT-4.1 (which needs explicit steps), or specifies 15 rigid numbered steps for a reasoning model (which wastes reasoning budget). Match instruction style to the target model's capabilities.
