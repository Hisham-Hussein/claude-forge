---
name: write-prompt
description: Guide for writing high-quality LLM prompt modules (.prompt.ts files) that follow prompt-as-code architecture. Use when implementing any prompt module — writing assemblePrompt(), designing input/output schemas, composing system/user prompts, or when a spec says "implement the prompt." Also use when debugging prompt quality issues (output too generic, schema compressing output, extraction missing detail). Triggers on "write the prompt", "implement the prompt module", "prompt quality", "assemblePrompt", ".prompt.ts", or any task that involves composing LLM instructions with structured output.
---

<objective>
Guide the implementer through writing a prompt module that produces high-quality LLM output by applying prompt-as-code architecture, the schema granularity rule, and evidence-backed prompt engineering techniques.
</objective>

<essential_principles>

**Principle 1: Three layers, strict boundaries.**
Every LLM call flows through three layers. Never mix them.

| Layer | Responsibility | Violation signal |
|-------|---------------|-----------------|
| **Caller** (e.g., `voice-extractor.ts`) | Fetch data, compute deterministic values, build typed input | You're writing prompt text in the caller |
| **Prompt module** (`.prompt.ts`) | Pure rendering: typed input → `{ system, user }` strings | You're fetching data or computing aggregations inside `assemblePrompt()` |
| **LLM provider** (`generateObject<T>()`) | Send prompt, validate response against output schema | You're constructing prompt strings in the provider |

The prompt module is a **pure function**. No side effects, no data fetching, no computation. Given the same input, it always produces the same prompt strings. This is what makes it testable in isolation.

**Principle 2: The schema is a ceiling, not a floor.**
The output Zod schema determines the **maximum** richness of LLM output. A fine-grained schema with 12 nested fields tells the LLM "produce exactly these 12 small pieces" — it compresses output into slots. A coarse `z.string()` field with prompt instructions controlling internal structure lets the LLM write richly.

Match schema granularity to the **consumer**:
- Consumer is **application code** that branches on sub-fields → fine-grained typed schemas
- Consumer is **another LLM prompt** that reads markdown → coarse `z.string()` fields

Evidence: replacing 12 nested Zod schemas with 6 `z.string()` fields — zero prompt changes — jumped quality from ~40% to ~90% of a hand-crafted reference. The prompt was never the problem; the schema was compressing the output.

**Principle 3: Compute in code, instruct in prompts.**
If a value can be computed deterministically, compute it in the caller and pass it as typed input. The LLM should never count occurrences, compute averages, rank items, or derive facts that code can produce reliably. When the caller computes "7 of 10 posts use Question hooks," the LLM receives a verified fact — not a value it might hallucinate from counting.

**Principle 4: The prompt module file structure is standardized.**
Every `.prompt.ts` exports:

| Export | Purpose |
|--------|---------|
| Input schema (Zod) | What context this prompt needs — validated before assembly |
| Output schema (Zod) | What the LLM must return — validated after generation |
| Task ID constant | Maps to model policy (model, temperature, max tokens) |
| `promptVersion` string | For logs, evals, regression comparison (e.g., `'1.0'`, `'2.0'`) |
| `assemblePrompt(input)` | Pure function → `{ system, user }` |

**Principle 5: Context is a curation problem, not a compression problem.**
Every token depletes the model's attention budget. As token count grows, recall accuracy drops — a measurable phenomenon called context rot. The goal is the **smallest set of high-signal tokens** for the current task. Do not pre-load everything "just in case." Start with the minimum viable context and add only what observed failure modes demand.

**Principle 6: Message role priority is not purely positional.**
System/developer messages take priority over user messages regardless of position. Place authoritative rules (constraints, output format, safety) in the system prompt — not in the user message, even if the user message appears later. Design prompts so the priority chain and positional recency reinforce each other, never compete.

</essential_principles>

<prompt_engineering_techniques>

## Instructions and Examples Are Complementary

Instructions and examples serve different functions — you usually need both:

| Purpose | Instructions | Examples |
|---------|-------------|---------|
| Define rules | Primary mechanism | No — examples illustrate, not define |
| Show format/structure | Weak — prose descriptions are ambiguous | Primary mechanism |
| Demonstrate tone | Weak — "be professional but warm" is vague | Learned by exposure |
| Handle edge cases | Good for explicit rules | Good for showing how rules apply |
| Prevent unwanted behavior | Good — negative instructions | Risky — showing bad output primes the model to produce it |

Every behavior shown in examples must also be stated in instructions. Instructions set the floor; examples set the ceiling.

## Few-Shot Examples

**How many:** 3-5 is the sweet spot. One example gives a large accuracy jump. Beyond 5, diminishing returns. Beyond 10, risk of over-prompting — reasoning models (o1, Claude with extended thinking) actually degrade with too many examples because examples consume reasoning budget.

**How to select:**
- **Relevant** — examples must mirror the actual use case (a text post example won't help generate carousel content)
- **Diverse** — cover the range of expected inputs, including edge cases
- **High-quality** — every example teaches what "good" looks like; mediocre examples teach mediocre output
- Never include examples that contradict your instructions (recency bias makes the model follow the example over the rule)

**Where to place:** After instructions, near the end of the system prompt. For Claude, wrap in `<example>` tags inside `<examples>`. For OpenAI, use a dedicated `# Examples` section. For long-context prompts (20k+ tokens), place long documents near the top with query and examples closer to the end — Anthropic's testing shows up to 30% improvement.

**Dynamic vs static selection:** When the example pool exceeds ~10 items, dynamically selecting examples based on semantic similarity to the current input consistently outperforms static/random selection (5-7% F1 improvement measured across multiple domains). For pools under 10, static is fine. For 50+, dynamic is essential — static wastes most of the pool.

**Conversational few-shot** (strongest technique for style transfer): Structure examples as multi-turn conversation — user message with a prompt, assistant message with the example output. This aligns with the model's training distribution and produces more consistent style matching than dumping examples into a single block. The reverse-prompt method works well: take real writing samples, generate "what prompt could have produced this?", then build a synthetic conversation history.

**When to skip examples entirely:** For zero-shot extraction or rule-based tasks (like knowledge extraction from varied source types), static examples risk overfitting. Explicit instructions with concrete inline examples of the desired *specificity level* work better than full input/output example pairs.

## Style Transfer (Voice-Matched Content)

Basic style instructions ("write in a professional but warm tone") produce generic output detectable as AI-written. Effective style transfer requires three layers working together:

**Layer 1 — Style description (rules):** Extract a structured voice profile from 10-20 writing samples:
- Structural DNA: sentence length, paragraph patterns, fragment usage, formatting habits
- Emotional DNA: tone on four axes (funny-serious, formal-casual, respectful-irreverent, enthusiastic-matter-of-fact)
- Semantic DNA: must-use words, banned words, signature phrases, jargon policy

**Layer 2 — Few-shot writing samples (examples):** Use the conversational few-shot format described above. 5+ high-performing samples in the target voice, structured as reverse-prompt conversations.

**Layer 3 — Anti-pattern list (negative instructions):** Explicitly ban the phrases that make AI content detectable: "leverage," "delve," "landscape," "game-changer," "navigate," "It's not X, it's Y," "It's important to note that..."

The combination of "write like this" (positive) and "never write like that" (negative) is more effective than either alone. Fine-tuning is not required when all three layers are used.

## Creative Drafting Guardrails

Content generation prompts blend factual claims with creative framing. Without explicit guardrails, models fabricate specific names, metrics, outcomes, and capabilities to strengthen the draft. The prompt must partition three categories:

1. **Source-backed facts** (metrics, outcomes, capabilities, dates, named entities) — must come from provided context only. Do NOT invent specifics to strengthen the draft.
2. **Creative framing** (hooks, transitions, analogies, narrative structure) — generate freely within voice profile constraints. No citation required.
3. **Gaps** — when the prompt requires a specific claim but context lacks evidence, use `[PLACEHOLDER: description]` or state the assumption explicitly. Never fabricate.

Include this partition explicitly in any prompt that generates content from knowledge items or external sources.

## Context Window Efficiency

**Token budget allocation** (content generation baseline):

| Component | Typical tokens | Notes |
|-----------|---------------|-------|
| System prompt (role, voice profile) | 500–1,500 | Distill voice profile to 500-800 tokens; keep full analysis as reference |
| Anti-pattern list | 100–300 | 10-15 banned phrases/patterns |
| Few-shot examples | 1,000–3,000 | 3-5 examples at 200-600 tokens each, dynamically selected |
| Task instructions | 200–500 | Specific but concise |
| Knowledge context | 500–2,000 | 5-10 relevant items, not the full knowledge base |
| Strategic context | 200–500 | Only what's relevant to this generation |
| Generation request | 100–300 | The specific ask |
| **Total** | **2,600–8,100** | Well under model context limits |

**Efficiency rules:**
- Pursue the smallest high-signal token set — begin with minimal prompts, add detail only based on observed failure modes
- Use just-in-time loading over pre-loading — maintain lightweight identifiers, load data at generation time
- Structure for parseability — XML tags (Claude) or markdown headers (GPT) help the model locate information without scanning everything
- Avoid redundancy between layers — if the voice profile says "use short sentences," don't repeat it in instructions
- Place static content first for prompt caching — system prompt (role, voice, instructions) before dynamic content (context, examples, request). This is both cache-optimal and usually comprehension-optimal. When long context (3,000+ tokens) needs maximum attention, consider moving it before instructions.
- Do not dump all writing samples, full knowledge bases, or "just in case" context into the prompt

</prompt_engineering_techniques>

<workflow>

## Step 1: Understand what you're building

Before writing any prompt text, answer these questions:

1. **What does the caller provide?** Read the caller (or spec) to understand what data is available as typed input.
2. **What must the LLM produce?** Define the output — what downstream code or human consumes it.
3. **Who consumes the output?** Code (fine-grained schema) or another LLM/human (coarse schema). This determines schema design.
4. **What can be computed deterministically?** Anything the caller can compute should NOT be delegated to the LLM.
5. **Is this content generation?** If yes, you'll need creative drafting guardrails, and possibly voice profile + style transfer layers.

## Step 2: Design the schemas

**Input schema** — include everything the prompt needs, nothing it doesn't:
- Every field referenced in the prompt text must come from the input schema
- No hardcoded values in prompt text that should be parameterized
- No input fields the prompt ignores (dead inputs)

**Output schema** — match granularity to consumer:
- For LLM consumers: prefer `z.string()` fields with prompt instructions controlling internal markdown structure
- For code consumers: use typed fields, enums, arrays as needed
- Mark optional fields correctly for the provider's structured output mode (e.g., `.nullable()` for OpenAI)
- When in doubt, start coarse — you can always add structure later, but over-structured schemas silently compress quality

## Step 3: Write the system prompt

The system prompt is the authoritative layer. It should be **static across all calls** (enables prompt caching).

**Structure by complexity:**
- Simple prompts (1-2 sections): markdown with `---` separators and `**bold**` labels
- Complex prompts (3+ sections): XML section tags (`<output-fields>`, `<anti-patterns>`, `<source-guidance>`)

**Content checklist:**
- Role definition — who is the LLM acting as, what is the task
- Output field descriptions — what each output field should contain (these are instructions, not schema enforcement)
- Constraints and rules — placed here because system messages take priority over user messages (Principle 6)
- Anti-patterns — use **negative instructions** ("Do NOT..."), never negative examples
- Source type awareness — if the input varies in format, tell the LLM to adapt
- Creative drafting guardrails — if the prompt generates content from sources, include the three-category partition (source-backed facts / creative framing / gaps)
- Match prompt prose style to desired output style — concise instructions produce concise output; verbose, over-formatted instructions produce verbose output
- Match instruction explicitness to the target model — GPT-4.1 benefits from explicit step-by-step; reasoning models prefer outcome-first prompts. Regardless of model: avoid extreme over-specification (20 rigid steps for a judgment task), reserve ALWAYS/NEVER for true invariants.

**Few-shot examples** (when applicable):
- 3-5 examples, placed after instructions, in `<examples>` tags (Claude) or `# Examples` section (OpenAI)
- Every behavior shown in examples must also be stated in instructions
- For style transfer: use conversational few-shot format (reverse-prompt method)
- For extraction/rule-based tasks: prefer explicit instructions over examples
- For dynamic selection (pool > 10 items): select by semantic similarity to current input at generation time

**What does NOT go in the system prompt:**
- Per-item dynamic values (source content, URLs, item-specific metadata) — these go in the user message
- Computation or conditional logic — the prompt module is pure rendering

## Step 4: Write the user prompt

The user message carries per-request dynamic content:
- The actual source material / input data
- Item-specific metadata (source type, URL, identifiers)
- Any per-request context the system prompt references generically

**Structural clarity:** Wrap distinct content blocks in XML tags or clear delimiters so the LLM can locate information without scanning the entire context.

**Token discipline:** Include only the context needed for this specific request. If the prompt has a knowledge context section, curate 5-10 relevant items — not the full knowledge base. Every token must justify its inclusion.

## Step 5: Write the tests (TDD)

Write failing tests **before** implementing. Test the prompt module as a pure function:

```typescript
// Given this input...
const input = { sourceContent: '...', sourceType: 'youtube-transcript' };
// The assembled prompt should contain...
const { system, user } = assemblePrompt(input);
expect(system).toContain('extraction categories');
expect(user).toContain(input.sourceContent);
// And should NOT contain...
expect(system).not.toContain(input.sourceContent); // dynamic content stays in user message
```

Test what matters:
- System prompt contains required instruction sections
- User prompt correctly formats dynamic input
- No per-item dynamic content leaks into the system prompt (caching invariant)
- Prompt version is correct
- XML/structural tags are present for complex prompts

## Step 6: Verify before declaring done

After implementation, run this checklist:

- [ ] `assemblePrompt()` is pure — no side effects, no data fetching, no computation
- [ ] Every input schema field is used in the prompt text (no dead inputs)
- [ ] Every value in the prompt text comes from the input schema (no hardcoded dynamic values)
- [ ] System prompt is static across all calls (caching-safe)
- [ ] Per-item content lives in the user message only
- [ ] Output schema granularity matches the consumer (code = fine, LLM/human = coarse)
- [ ] Anti-patterns use negative instructions, not negative examples
- [ ] If content generation: creative drafting guardrails partition source facts from creative framing
- [ ] If style transfer: all three layers present (voice profile rules + few-shot samples + anti-pattern list)
- [ ] Prompt version is bumped if the prompt changed significantly
- [ ] Task ID maps to the correct model policy entry
- [ ] Token budget is within model limits with margin (estimate: system + user + maxTokens output)
- [ ] All tests pass

</workflow>

<references>

For the full research with citations, examples, and deeper rationale, read the bundled reference file:

| File | When to read |
|------|-------------|
| `references/prompt-engineering-best-practices.md` | When you need the full evidence behind a technique (few-shot research data, style transfer studies, token budget details), or when the SKILL.md summary isn't enough to make a design decision |

The SKILL.md body covers ~90% of the reference content in distilled form. Read the reference file when you need the remaining depth — specific research numbers, vendor-specific placement rules, remaining unknowns, or cross-reference with other research.

If your project has its own prompt architecture docs or CLAUDE.md prompt rules, those take precedence for project-specific conventions.

</references>
