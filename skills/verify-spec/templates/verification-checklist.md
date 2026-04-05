## Appendix: Verification Checklist

> Mechanical completeness check — run BEFORE adversarial review.
> Every cell must be filled. Resolve all gaps before approval.

### 1. Entity-State Matrix

Every entity this spec touches × every possible state (including states from existing system behavior).

| State / Entity | [Entity A] | [Entity B] | [Entity C] |
|----------------|------------|------------|------------|
| [state 1]      |            |            |            |
| [state 2]      |            |            |            |
| [state 3]      |            |            |            |

**Legend:**
- **Defined** — Spec defines behavior for this combination
- **GAP** — Spec is silent (must resolve before approval)
- **N/A** — Not applicable (state reasoning)

**Rules:**
- States come from the SYSTEM, not just this spec. Include states from prior work and existing code.
- If two entities interact, add rows for meaningful combinations.
- Every GAP must be resolved: either add behavior to the spec, or convert to N/A with reasoning.

---

### 2. Contradiction Scan

For each pair of requirements that touch the same entity, field, or state:

| Req A | Req B | Verdict | Reasoning |
|-------|-------|---------|-----------|
|       |       |         |           |

**Verdicts:**
- **Compatible** — No conflict
- **Tension** — Works today but could conflict under scale or new features. Note the trigger condition.
- **Conflict** — Direct contradiction. Must resolve before approval.

**Rules:**
- Only pairs touching the same entity/field/state need checking.
- Include requirements from EXISTING system behavior, not just this spec.
- Every Conflict must be resolved before approval.

---

### 3. Data Flow Trace

For each output field in the final result, trace backward through the pipeline:

| Output Field | Produced By | Passed Through | Source |
|--------------|-------------|----------------|--------|
|              |             |                |        |

**Gap types to check:**
- Field with no producer (where does this value come from?)
- Step that needs data the prior step doesn't emit
- Field produced but never consumed (dead data)
- Field transformed but original lost when downstream needs it

---

### 4. External Assumptions Register

Every assumption about an external system, with verification status:

| Assumption | System | Verified By | Status |
|------------|--------|-------------|--------|
|            |        |             |        |

**Status values:**
- **Verified** — confirmed by spike, production data, or official docs
- **Unverified** — assumed but not checked (GAP)
- **Contradicted** — evidence against this assumption (BLOCKER)

**Rules:**
- Include API behavior, rate limits, data formats, field availability.
- "I've used this API before" is not verification — cite the specific evidence.
- Every Unverified assumption is a GAP. Either verify it or flag it as a risk.

---

### 5. Requirement Traceability

Every requirement maps to at least one acceptance test. If you can't write the test signature, the requirement is ambiguous.

| # | Requirement (from spec) | Test Signature | Verifies What? |
|---|-------------------------|----------------|----------------|
|   |                         | `test('...')`  |                |

**Rules:**
- One requirement may have multiple tests (different scenarios, boundary conditions).
- If a test covers multiple requirements, list it under each.
- A requirement with no test signature = ambiguous requirement. Rewrite it.
- These test signatures feed directly into the writing-plans phase.

---

### Checklist Summary

| Section | Total Items | Gaps | Resolved |
|---------|-------------|------|----------|
| Entity-State Matrix | | | |
| Contradiction Scan | | | |
| Data Flow Trace | | | |
| External Assumptions | | | |
| Requirement Traceability | | | |
| **Total** | | | |

**Verdict:** All gaps resolved? YES / NO (if NO, spec is not ready for approval)
