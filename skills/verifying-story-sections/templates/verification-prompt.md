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

    ## Codebase Verification Results (Groups 3-4 only)

    {codebase_verification_results}

    If this section makes claims about existing files, exports, or code patterns,
    the author has pre-verified them with Glob/Grep. The results are above.
    Compare the story's claims against these results. If no codebase claims
    exist in this section, this block will be empty — skip it.

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
    - Chosen one side of a source conflict without flagging it

    Independently compare every factual claim in the section against the source excerpts.

    ## What to Check

    1. Source document fidelity
    Build an explicit comparison table for every factual claim:

    | Source Claim | Source Location | Story Claim | Story Location | Match? |
    |---|---|---|---|---|
    | Field: status (singleSelect) | data-model:§Posts | Field: status (singleSelect) | story:§4.2 | YES |
    | Field: personaId (required link) | data-model:§Posts | Field: personaId (optional link) | story:§4.2 | NO — required vs optional |

    Every factual claim in the story section MUST appear in this table.
    Any claim NOT traceable to a source row is flagged as UNSUPPORTED.
    Include the completed table in your report.

    2. Completeness
    For each source excerpt, check whether all relevant details made it
    into the story section. If the data model defines 8 fields for a table,
    are all 8 mentioned (or explicitly scoped out with justification)?
    If the architecture defines 3 patterns for adapters, are all 3 reflected?
    A missing constraint is invisible to the developer — flag it.

    3. Source coherence
    When multiple source documents are provided, check whether they agree
    with each other on the facts the story references. If source A says
    field X is required and source B says it is optional, or the architecture
    defines an interface that contradicts the data model's table structure,
    flag this as a SOURCE CONFLICT. Cite both source locations. Do not
    penalize the story for choosing one side — flag the conflict itself
    so the user can resolve it.

    4. Internal consistency
    Check the story section against the previously written sections in
    the story file (if any). For Groups 3-5: actively scan every entity
    (field name, type, file path, interface method) mentioned in this
    section against ALL previously committed sections. If this section
    says field X is type Y, and an earlier section references field X
    as type Z, that is a cross-group regression — report it.

    5. Actionability
    Is the section specific enough for a developer agent to implement
    without guessing? The developer will ONLY have this story file.
    Apply these concrete tests — fail any = deviation:
    - Every interface/port mentioned: are its method signatures listed?
    - Every file path referenced: is the full path from repo root given?
    - Every type mentioned: is its shape defined or referenced by location?
    - Every "follow pattern X": is the pattern described or cited by file:line?
    - Every constraint ("must be", "required", "at most"): is the value stated?

    6. Principle compliance
    Read the project principles file. Check design decisions in this
    section against each relevant principle: dependency direction,
    interface segregation, vendor portability, error classification,
    clean boundaries, credential handling. Only flag violations of
    principles the project actually states — not theoretical best practices.

    7. Codebase claim verification (Groups 3-4 only)
    If codebase verification results are provided above, compare each
    claim in the story section against those results. Flag any claim
    where the Glob/Grep results contradict what the story states
    (file does not exist, export not found, pattern not present).

    ## Intentional Deviations

    The story section may contain annotations like:
    <!-- INTENTIONAL DEVIATION: [reason] -->

    These mark places where the author knowingly departs from a source
    document. Acknowledge these in a separate "Acknowledged Deviations"
    section of your report. Do NOT count them as findings. However, if
    the reason is missing, vague, or unconvincing, flag the annotation
    itself as a MAJOR deviation — an unjustified intentional deviation
    is worse than an accidental one.

    ## Severity Classification

    Every deviation MUST be classified:

    - CRITICAL: Wrong fact that will propagate — wrong field name, wrong
      type, wrong relationship, missing required constraint, wrong interface
      method signature. A developer implementing from this story will write
      incorrect code.
    - MAJOR: Missing information that leaves a gap — port method not listed,
      constraint not mentioned, architecture pattern referenced but not
      described. The developer will have to guess.
    - MINOR: Imprecise wording unlikely to cause implementation errors but
      could be clearer. Does not block section commitment.

    ## Reporting

    If all 7 checks pass (no CRITICAL or MAJOR findings):

    PASS — Section Group {group_number} ({group_name}) is source-faithful.
    [1-2 sentence summary of what was verified]
    MINOR findings (if any): [list]

    If CRITICAL or MAJOR deviations found:

    DEVIATIONS FOUND — Section Group {group_number} ({group_name})

    Comparison table:
    [the full comparison table from check 1]

    D{n}: {brief title}
    Severity: CRITICAL / MAJOR / MINOR
    Area: {which of the 7 checks}
    Source says: {quote or paraphrase the source document}
    Story says: {what the story section actually states}
    Fix: {specific suggested fix}

    Source conflicts (if any):
    SC{n}: {source A location} says X, {source B location} says Y.
    Escalate to user.

    Acknowledged intentional deviations (if any):
    [list with reasons]

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

    ## Codebase Verification Results (Groups 3-4 only)

    {codebase_verification_results}

    ## Previous Deviations That Were Fixed

    {previous_deviations}

    ## Files to Read

    - {principles_file_path} — project architectural principles.
    - {story_file_path} — the story file written so far (prior section groups).

    ## What to Check

    Perform all 7 standard checks (source fidelity with comparison table,
    completeness, source coherence, internal consistency, actionability,
    principle compliance, codebase claim verification) — same as a
    first-pass verification.

    Additionally, check two things specific to re-verification:

    8. Fix resolution
    For each previous deviation listed above, verify the fix actually
    resolves it. A fix that addresses something adjacent to the deviation
    but not the deviation itself is not a resolution.

    9. Fix regression
    Did any fix introduce new inconsistencies with the rest of the story?
    Check: field names changed but not updated in other references,
    constraints added that contradict an earlier AC, port methods renamed
    but tasks still reference the old name.

    ## Intentional Deviations

    Same handling as first-pass: acknowledge annotated deviations, flag
    those with weak or missing reasons.

    ## Severity Classification

    Same as first-pass: CRITICAL / MAJOR / MINOR.

    ## Reporting

    Same format as first-pass. Report PASS or DEVIATIONS FOUND.
    Include the full comparison table.
    For re-verification, also report fix resolution status:

    Fix resolution:
    - D1 ({title}): RESOLVED / NOT RESOLVED / PARTIALLY RESOLVED
    - D2 ({title}): RESOLVED / NOT RESOLVED / PARTIALLY RESOLVED

    Regressions introduced: {none / list}

    Source conflicts (if any): [list]
    Acknowledged intentional deviations (if any): [list]
```

</re_verification>
