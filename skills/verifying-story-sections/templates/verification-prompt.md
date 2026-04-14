<overview>
Template for spawning the verifier after writing a story section group.

Model: sonnet (fast, precise enough for comparison work).
Mode: read-only — the subagent reports findings, never edits the story.
</overview>

<first_pass_verification>

Spawn the verifier with the following prompt. Replace all `{placeholders}` with actual values.

```
Agent tool:
  description: "Verify story section group {group_number} against sources"
  model: sonnet
  prompt: |
    You are verifying whether a story spec section accurately reflects its source documents.

    ## Section Group {group_number}: {group_name}

    {section_text}

    ## Source Document Excerpts (what the section SHOULD reflect)

    {source_excerpts}

    For each excerpt above, the document name and section path are provided.
    These are the ground truth. The story section must be faithful to them.

    ## Files to Read

    - {principles_file_path} — project architectural principles. Read the full file.
    - {story_file_path} — the story file written so far (prior section groups). Read for internal consistency.
      If this is Section Group 1, skip — no prior sections exist.

    ## Do Not Trust the Story Author

    The author synthesized this section from multiple source documents, but may have:
    - Misquoted a field name, type, or constraint from the data model
    - Omitted a port method or interface the architecture defines
    - Stated a file exists at a path where it does not
    - Written an AC that subtly differs from the epic's AC
    - Included requirements the sources do not prescribe (scope creep)
    - Made claims about existing code that are stale or wrong

    Independently compare every factual claim in the section against the source excerpts.

    ## What to Check

    1. Source document fidelity
    Read each source excerpt line by line. For each factual claim in the
    story section (field names, types, constraints, interface methods,
    file paths, table relationships, status values, API patterns), find
    the corresponding source text. Flag any claim that is missing from
    the sources, different from the sources, or only partially captured.
    Cite the specific source text and the specific story text that diverges.

    2. Completeness
    For each source excerpt, check whether all relevant details made it
    into the story section. If the data model defines 8 fields for a table,
    are all 8 mentioned (or explicitly scoped out with justification)?
    If the architecture defines 3 patterns for adapters, are all 3 reflected?
    A missing constraint is invisible to the developer — flag it.

    3. Internal consistency
    Check the story section against the previously written sections in
    the story file (if any). Look for contradictions: a field name
    spelled differently, a file path that changed, an AC that references
    something the data model section defines differently.

    4. Actionability
    Is the section specific enough for a developer agent to implement
    without guessing? The developer will ONLY have this story file.
    Flag vague directives like "follow the architecture" without citing
    which specific patterns, or "use the existing interface" without
    listing its methods. Every detail the developer needs must be present.

    5. Principle compliance
    Read the project principles file. Check design decisions in this
    section against each relevant principle: dependency direction,
    interface segregation, vendor portability, error classification,
    clean boundaries, credential handling. Only flag violations of
    principles the project actually states — not theoretical best practices.

    ## Reporting

    If all 5 checks pass:

    PASS — Section Group {group_number} ({group_name}) is source-faithful.
    [1-2 sentence summary of what was verified]

    If deviations found:

    DEVIATIONS FOUND — Section Group {group_number} ({group_name})

    D{n}: {brief title}
    Area: {which of the 5 checks}
    Source says: {quote or paraphrase the source document}
    Story says: {what the story section actually states}
    Fix: {specific suggested fix}

    Do not flag style preferences, formatting choices, or things the
    source documents do not prescribe. Only flag deviations where the
    story section diverges from what the sources or principles require.
```

</first_pass_verification>

<re_verification>

Use this variant when re-verifying a section after the author fixed deviations. Replace all `{placeholders}` with actual values.

```
Agent tool:
  description: "Re-verify story section group {group_number} after fixes"
  model: sonnet
  prompt: |
    You are re-verifying a story spec section after the author fixed
    deviations from the previous verification pass.

    ## Section Group {group_number}: {group_name} (after fixes)

    {section_text}

    ## Source Document Excerpts

    {source_excerpts}

    ## Previous Deviations That Were Fixed

    {previous_deviations}

    ## Files to Read

    - {principles_file_path} — project architectural principles.
    - {story_file_path} — the story file written so far (prior section groups).

    ## What to Check

    Perform all 5 standard checks (source fidelity, completeness,
    internal consistency, actionability, principle compliance) — same
    as a first-pass verification.

    Additionally, check two things specific to re-verification:

    6. Fix resolution
    For each previous deviation listed above, verify the fix actually
    resolves it. A fix that addresses something adjacent to the deviation
    but not the deviation itself is not a resolution.

    7. Fix regression
    Did any fix introduce new inconsistencies with the rest of the story?
    Check: field names changed but not updated in other references,
    constraints added that contradict an earlier AC, port methods renamed
    but tasks still reference the old name.

    ## Reporting

    Same format as first-pass. Report PASS or DEVIATIONS FOUND.
    For re-verification, also report fix resolution status:

    Fix resolution:
    - D1 ({title}): RESOLVED / NOT RESOLVED / PARTIALLY RESOLVED
    - D2 ({title}): RESOLVED / NOT RESOLVED / PARTIALLY RESOLVED

    Regressions introduced: {none / list}
```

</re_verification>
