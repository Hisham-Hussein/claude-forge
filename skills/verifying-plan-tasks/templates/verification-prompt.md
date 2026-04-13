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
    - Written code that looks right but subtly diverges
    - Omitted test cases the spec requires
    - Violated architectural principles without realizing
    - Built something the spec doesn't ask for

    Independently compare. Do not accept the task at face value.

    ## What to Check

    1. Spec behavioral fidelity
    Read the spec section line by line. For each behavioral prescription
    (retry logic, error handling, validation rules, interface methods,
    parameter types, specific constants), find the corresponding code in
    the task. Flag any prescription that is missing, different, or only
    partially implemented. Cite the specific spec text and the specific
    task code that diverges.

    2. Test completeness
    The spec section may list required test scenarios or testing requirements.
    For each, verify a corresponding test exists in the task with assertions
    specific enough to catch the behavior. A test that only checks "it doesn't
    throw" when the spec requires verifying a specific return value is a gap.

    3. Principle compliance
    Read the project principles file. Check the task's code against each
    relevant principle: dependency direction, credential sanitization,
    interface segregation, error classification, clean boundaries, vendor
    portability. Only flag violations of principles the project actually
    states — not theoretical best practices.

    4. Forward consistency
    Check that interfaces, type signatures, export names, and function
    signatures in this task are consistent with:
    - Prior tasks in the plan file (if any)
    - What downstream spec sections will need (skim ahead in the spec
      section for references to things this task creates)

    ## Reporting

    If all 4 checks pass:

    PASS — Task {task_number} is spec-faithful.
    [1-2 sentence summary of what was verified]

    If deviations found:

    DEVIATIONS FOUND — Task {task_number}

    D{n}: {brief title}
    Area: {which of the 4 checks}
    Spec says: {quote or paraphrase the spec requirement}
    Task does: {what the task code actually does}
    Fix: {specific suggested fix}

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

    Perform all 4 standard checks (spec fidelity, test completeness,
    principle compliance, forward consistency) — same as a first-pass
    verification.

    Additionally, check two things specific to re-verification:

    5. Fix resolution
    For each previous deviation listed above, verify the fix actually
    resolves it. A fix that addresses something adjacent to the deviation
    but not the deviation itself is not a resolution.

    6. Fix regression
    Did any fix introduce new inconsistencies with the rest of the plan?
    Check: stale references to renamed items, dropped functionality that
    was absorbed nowhere, interface changes that break prior tasks,
    count/total mismatches in summary sections.

    ## Reporting

    Same format as first-pass. Report PASS or DEVIATIONS FOUND.
    For re-verification, also report fix resolution status:

    Fix resolution:
    - D1 ({title}): RESOLVED / NOT RESOLVED / PARTIALLY RESOLVED
    - D2 ({title}): RESOLVED / NOT RESOLVED / PARTIALLY RESOLVED

    Regressions introduced: {none / list}
```

</re_verification>
