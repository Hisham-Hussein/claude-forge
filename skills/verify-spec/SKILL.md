---
name: verify-spec
description: Use when verifying a spec or design document for structural completeness, or when the user asks to "verify spec", "check spec completeness", "find spec gaps", or "run verification checklist". Also triggers when a spec has been written and needs mechanical validation before adversarial review.
---

<objective>
Mechanically verify specs and design documents for structural completeness by producing a five-section verification checklist. This catches missing states, contradictions, data flow gaps, and unverified assumptions that adversarial review (heuristic, sampling-based) is likely to miss.

This is NOT a replacement for adversarial review. It catches a different class of defects — structural gaps that can be found by exhaustive enumeration over a defined space. Adversarial review catches creative issues (feasibility, scaling, architectural fit) that don't fit in a matrix.

**Workflow position:** Spec writing → **Verification Checklist** → Adversarial Review → Writing Plans
</objective>

<quick_start>
Given a spec document, produce a filled verification checklist with five sections:

1. **Entity-State Matrix** — every entity × every state = defined behavior
2. **Contradiction Scan** — every requirement pair touching same entity/field
3. **Data Flow Trace** — every output field traced back to its source
4. **External Assumptions Register** — every external system assumption verified
5. **Requirement Traceability** — every requirement has a test signature

Read the template: [templates/verification-checklist.md](templates/verification-checklist.md)
</quick_start>

<process>
**Step 1: Read the spec**

Read the spec document provided by the user (path or content). Identify:
- All entities mentioned (profiles, runs, configs, records, etc.)
- All requirements (explicit and implicit)
- All external systems referenced
- All output fields or data transformations

**Step 2: Enumerate entities and states**

For each entity, list ALL possible states — not just states from this spec, but states from the existing system. Check existing code, prior specs, and CLAUDE.md for states the spec may have inherited.

Fill the Entity-State Matrix. For every cell, determine:
- **Defined** — the spec says what happens
- **GAP** — the spec is silent
- **N/A** — not applicable (with reasoning)

**Step 3: Scan for contradictions**

For each pair of requirements that touch the same entity, field, or state, check compatibility. Include requirements from existing system behavior, not just this spec.

Mark each pair: Compatible, Tension, or Conflict.

**Step 4: Trace data flow**

For each output field in the spec's deliverable, trace backward:
- Which step/component produces it?
- Which steps pass it through?
- What is the original source?

Flag: fields with no producer, steps that need data the prior step doesn't emit, fields produced but never consumed.

**Step 5: Register external assumptions**

List every assumption about external systems (APIs, services, platforms). For each:
- What does the spec assume?
- Is it verified by spike, production data, or official docs?
- If unverified, flag as GAP.

**Step 6: Map requirements to tests**

For each requirement, write a test signature (`test('...')`). If you can't write a meaningful test signature, the requirement is ambiguous — flag it and suggest a rewrite.

**Step 7: Resolve gaps**

For every GAP found in steps 2-6:
- If the gap can be resolved by adding behavior to the spec, propose the fix.
- If the gap requires user input (design decision), flag it with a clear question.
- Present all gaps to the user with proposed resolutions.

**Step 8: Produce the checklist**

Append the completed checklist to the spec document as an appendix, or produce it as a separate document if the user prefers. Fill in the summary table with counts.
</process>

<anti_patterns>
<pitfall name="inventing-behavior">
When filling the Entity-State Matrix, do NOT invent behavior the spec doesn't define. If the spec is silent on a combination, mark it GAP — don't fill in what you think the behavior should be. The point is to surface the gap, not to silently resolve it.
</pitfall>

<pitfall name="only-this-spec-states">
Do NOT limit states to what this spec defines. Check existing code and prior specs for states the system already has. The most dangerous gaps are interactions between new spec behavior and existing system states.
</pitfall>

<pitfall name="happy-path-assumptions">
When checking external assumptions, "I've seen this API work" is not verification. Cite specific evidence: spike results, production data analysis, or official documentation with dates.
</pitfall>

<pitfall name="vague-test-signatures">
`test('it works correctly')` is not a valid test signature. Each test must verify a specific, observable behavior with a clear expected outcome implied by the name.
</pitfall>
</anti_patterns>

<success_criteria>
The verification checklist is complete when:

- Every cell in the Entity-State Matrix is filled (no empty cells)
- Every GAP is either resolved or flagged with a clear question for the user
- Every requirement pair touching the same entity has been checked for contradictions
- Every output field has been traced back to its source
- Every external assumption has a verification status
- Every requirement has at least one test signature
- The summary table shows zero unresolved GAPs (or all remaining GAPs are flagged as user decisions)
</success_criteria>
