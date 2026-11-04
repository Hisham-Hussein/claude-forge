<overview>
Competitor research gives the UX plan the conventions users already expect from tools they know, so the plan is not designed in a void. It informs; it never decides. The story map stays the source of every UX element, and the user decides which patterns to take.

Two rules hold throughout:
- **Functionality, never identity.** Take flows, features and conventions (what users expect to find and do). Never take a competitor's colours, type, brand motifs or copy voice.
- **Nothing from memory.** A product's flows as remembered by a model are often outdated or wrong. Every pattern cites a source file or URL; anything without one is marked unverified and is never presented as fact.
</overview>

<research_file_format>

## Shared research file format

Used by the short sourced step below, and by any dedicated competitor-research skill, so either can read or deepen the other's file. Default path: `.charter/COMPETITOR-FUNCTIONALITY.md`.

```markdown
# Competitor Functionality — [Product]

> **Competitors:** [1-3 names] | **Researched:** [YYYY-MM-DD] | **Method:** [existing research / public docs / logged-in walkthrough]

## [Competitor name]

| Flow or feature | What the user does (steps) | Source (URL or file + section) | Seen on | Evidence |
|-----------------|----------------------------|--------------------------------|---------|----------|
| [e.g., Save a creator to a list] | [1. … 2. … 3. …] | [URL] | [YYYY-MM-DD] | [verified / unverified] |
```

**verified** = the step sequence was read in the cited source. **unverified** = inferred or incomplete; say what is missing.

Research the project already has in another format is read as it is: cite its file and section; do not rewrite it into this format.

</research_file_format>

<short_sourced_step>

## Short sourced research (only for named competitors that existing research does not cover)

Bounded: 1-3 competitors, and only flows that match the in-scope stories (for each in-scope story map activity, look for how the competitor does the same job).

1. **Check for tools first.** It needs web search and page reading. If either is missing, say so and offer to skip. Never fall back to memory.
2. **Read the pages that show how the product works:** help centre and documentation articles (they describe real flows step by step), feature pages, product tours or demo videos. Marketing home pages show curated screenshots; use them only for conventions visible in a product shot, and say so.
3. **Record each flow** in the shared format above, with its URL and the date. Write the file before using it, so the plan cites the file and a later run can reuse it.
4. **Tell the user** where the file is, how many flows were verified vs. unverified, and that a dedicated competitor-research skill (logged-in walkthroughs, screenshots) goes deeper.

</short_sourced_step>

<competitor_patterns_table>

## Competitor patterns table (Stage 1)

Turn the research into decisions the user makes. One row per pattern seen in at least one competitor that serves an in-scope story (patterns that serve none go under Story-map gaps):

| ID | Pattern | Seen in | Source | Serves | Recommendation | Decision |
|----|---------|---------|--------|--------|----------------|----------|
| CP-01 | [e.g., Save to list from the results row] | [competitors] | [file/URL] | [SM-XXX] | [Adopt / Adapt / Skip — one line why] | [user's decision] |

How to recommend:
- **Adopt** — a convention most competitors share, so leaving it out costs users familiarity.
- **Adapt** — the idea serves a story, but the users, languages or context call for a change; say what changes.
- **Skip** — it does not serve an in-scope story, conflicts with the product's principles, or is a competitor's signature rather than a convention.

Patterns that serve no in-scope story are never added to the plan. List them under **Story-map gaps** (pattern, seen in, source, why no story fits, Decision) for the user to accept or reject. An accepted gap is not added during this run: the user adds the story to the story map, then runs the update workflow to bring it into the plan.

Later stages use only rows the user decided as Adopt or Adapt, and cite the CP-ID next to the element they shape. Traceability still runs to SM-XXX.

</competitor_patterns_table>
