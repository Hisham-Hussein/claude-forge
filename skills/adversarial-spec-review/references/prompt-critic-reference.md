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

### Anti-Pattern Lists

Research finding: The combination of positive instructions ("write like this") and negative instructions ("never write like that") is more effective than either alone. But negative *examples* (showing bad output) can prime the model to produce what you showed it.

**Review check:** If the prompt has anti-pattern instructions, verify they're phrased as prohibitions ("do NOT return generic descriptions"), not as examples of bad output.

## Common Prompt Spec Issues (From Real Reviews)

1. **"The prompt uses the established format"** — but the spec doesn't show what the actual prompt text says. Verify by reading `assemblePrompt()` output for a concrete input.

2. **Token count ignored.** The spec adds 50 tokens of metadata per item and processes 30 items — that's 1,500 new tokens. At scale, this matters.

3. **Aggregation in the wrong layer.** The spec says "the LLM analyzes the distribution" — but counting is arithmetic, not analysis. Code should count; the LLM should interpret.

4. **Output schema mismatch.** The prompt says "provide 3-5 examples" but the schema has no `.min(3).max(5)` constraint. Or worse: the schema enforces constraints the prompt doesn't mention, confusing the LLM.

5. **Field definitions ambiguous.** Two fields overlap — the spec doesn't say what goes where. The LLM will guess differently each time. Explicit boundary definitions ("this field covers X; that field covers Y; do NOT include Z here") prevent drift.

6. **Version not bumped.** A material prompt change (new fields, restructured instructions, different output format) keeps the old version string. Logs become uninterpretable — you can't tell which prompt version produced which output.
