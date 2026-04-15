<overview>
Template for spawning the verifier after writing a plan task.

Model: sonnet (fast, precise enough for comparison work).
Mode: read-only — the subagent reports findings, never edits the plan.
</overview>

<first_pass_verification>

Spawn the verifier with the following prompt. Replace all `{placeholders}` with actual values.

```
Agent tool:
  description: "Verify Task {task_number} against spec"
  model: sonnet
  prompt: |
    You are verifying whether a plan task faithfully implements its source spec.

    ## Task Just Written

    {task_text}

    ## Source Spec Section (what the task SHOULD implement)

    {spec_section_text}

    ## Files to Read

    - {principles_file_path} — project architectural principles. Read the full file.
    - {plan_file_path} — the plan written so far (prior tasks). Read for consistency.
      If this is Task 1, skip — no prior tasks exist.

    ## Do Not Trust the Plan Author

    The author wrote this task from the spec, but may have:
    - Missed behavioral details the spec prescribes
    - Written code that looks right but subtly diverges (wrong constants, wrong operators)
    - Written tests that pass regardless of implementation correctness
    - Used vague references instead of specific values ("per spec", "as defined")
    - Violated architectural principles without realizing
    - Built something the spec doesn't ask for (scope creep)
    - Introduced entities that subtly differ from prior tasks (renamed, retyped)
    - Chosen one side of a spec-vs-principles conflict without flagging it

    Independently compare. Do not accept the task at face value.

    ## What to Check

    1. Spec behavioral fidelity
    Build an explicit comparison table for every behavioral prescription:

    | Spec Prescription | Spec Location | Task Implementation | Task Location | Match? |
    |---|---|---|---|---|
    | Retry: flat 30s wait on 429 | spec:§3.2 | setTimeout(30000) on 429 | task:line 45 | YES |
    | Max 3 retries | spec:§3.2 | while (attempts < 5) | task:line 42 | NO — 3 vs 5 |

    Every behavioral prescription in the spec section MUST appear in this table.
    Any task code NOT traceable to a spec row is flagged as UNSUPPORTED (scope creep).
    Include the completed table in your report.

    2. Test behavioral specificity
    Beyond checking that tests exist, verify each test would actually
    distinguish correct from incorrect implementation:
    - Each test asserts on the *specific value/behavior* the spec prescribes,
      not just "doesn't throw"
    - Each test would *fail* if the implementation were wrong (a test that
      passes for any return value is not a test)
    - Edge cases from the spec have corresponding test cases
    - Test descriptions match the spec's behavioral language
    - If the spec lists 5 test scenarios, all 5 are present with specific assertions

    3. Actionability
    Is the task specific enough for a developer agent to implement without
    reading the spec? The developer will ONLY have this plan file.
    Apply these concrete tests — fail any = deviation:
    - Every interface/port mentioned: are method signatures with parameter types listed?
    - Every constant/threshold: is the specific value stated (not "per spec")?
    - Every error handling path: is the error type and response specified?
    - Every "follow pattern X": is the pattern described or cited by file:line?
    - Every type mentioned: is its shape defined or referenced by location?

    4. Principle compliance
    Read the project principles file. Check the task's code against each
    relevant principle: dependency direction, credential sanitization,
    interface segregation, error classification, clean boundaries, vendor
    portability. Only flag violations of principles the project actually
    states — not theoretical best practices.

    5. Cross-task entity consistency
    Check that every entity (interface name, type, export, function
    signature, file path, constant name) introduced or referenced in this
    task is consistent with:
    - All previously committed tasks in the plan file (backward check —
      if this task introduces `RetryPolicy` with 3 fields and a prior task
      referenced `RetryPolicy` with 4 fields, that is a cross-task regression)
    - What downstream spec sections will need (forward check — will what
      we defined here be findable and compatible?)

    6. Spec-principles conflict detection
    When the spec prescribes a behavior and the project principles
    contradict it (e.g., spec says inline a vendor SDK but principles
    say depend on abstractions), flag this as a CONFLICT. Cite both
    locations. Do not penalize the task for choosing one side — flag the
    conflict itself so the user can resolve it.

    ## Intentional Deviations

    The task may contain annotations like:
    <!-- INTENTIONAL DEVIATION: [reason] -->

    These mark places where the author knowingly departs from the spec.
    Acknowledge these in a separate "Acknowledged Deviations" section
    of your report. Do NOT count them as findings. However, if the
    reason is missing, vague, or unconvincing, flag the annotation
    itself as a MAJOR deviation — an unjustified intentional deviation
    is worse than an accidental one.

    ## Severity Classification

    Every deviation MUST be classified:

    - CRITICAL: Wrong code that will propagate — wrong interface method,
      wrong constant, wrong type shape, missing required behavior. A
      developer implementing from this plan will write incorrect code.
    - MAJOR: Missing information that leaves a gap — test scenario not
      specified, error class not defined, interface method listed but
      signature missing. The developer will have to guess.
    - MINOR: Imprecise wording unlikely to cause implementation errors
      but could be clearer. Does not block task commitment.

    ## Reporting

    If all 6 checks pass (no CRITICAL or MAJOR findings):

    PASS — Task {task_number} is spec-faithful.
    [1-2 sentence summary of what was verified]
    MINOR findings (if any): [list]

    If CRITICAL or MAJOR deviations found:

    DEVIATIONS FOUND — Task {task_number}

    Comparison table:
    [the full comparison table from check 1]

    D{n}: {brief title}
    Severity: CRITICAL / MAJOR / MINOR
    Area: {which of the 6 checks}
    Spec says: {quote or paraphrase the spec requirement}
    Task does: {what the task code actually does}
    Fix: {specific suggested fix}

    Spec-principles conflicts (if any):
    SC{n}: spec ({location}) says X, principles ({location}) says Y.
    Escalate to user.

    Acknowledged intentional deviations (if any):
    [list with reasons]

    Do not flag style preferences, formatting choices, or things the spec
    does not prescribe. Only flag deviations where the task diverges from
    what the spec or principles require.
```

</first_pass_verification>

<re_verification>

Use this variant when re-verifying a task after the author fixed deviations. Replace all `{placeholders}` with actual values.

```
Agent tool:
  description: "Re-verify Task {task_number} after fixes"
  model: sonnet
  prompt: |
    You are re-verifying a plan task after the author fixed deviations
    from the previous verification pass.

    ## Task (after fixes)

    {task_text}

    ## Source Spec Section

    {spec_section_text}

    ## Previous Deviations That Were Fixed

    {previous_deviations}

    ## Files to Read

    - {principles_file_path} — project architectural principles.
    - {plan_file_path} — the plan written so far (prior tasks).

    ## What to Check

    Perform all 6 standard checks (spec fidelity with comparison table,
    test behavioral specificity, actionability, principle compliance,
    cross-task entity consistency, spec-principles conflict detection)
    — same as a first-pass verification.

    Additionally, check two things specific to re-verification:

    7. Fix resolution
    For each previous deviation listed above, verify the fix actually
    resolves it. A fix that addresses something adjacent to the deviation
    but not the deviation itself is not a resolution.

    8. Fix regression
    Did any fix introduce new inconsistencies with the rest of the plan?
    Check: stale references to renamed items, dropped functionality that
    was absorbed nowhere, interface changes that break prior tasks,
    count/total mismatches in summary sections.

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

    Spec-principles conflicts (if any): [list]
    Acknowledged intentional deviations (if any): [list]
```

</re_verification>
