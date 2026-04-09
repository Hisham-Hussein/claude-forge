# UX Compliance Report — [Product Name]

> **Reviewed:** [UX plan file paths]
> **Against:** [Story map path] | [PRD path or "not provided"]
> **Review mode:** [Plan Quality Review / Implementation Compliance Review]
> **Date:** [Review date]

---

## Verdict: [PASS / PASS WITH NOTES / FAIL — REVISE]

[1-2 sentence summary of the overall assessment]

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total findings** | [N] |
| Severity 4 (catastrophic) | [N] |
| Severity 3 (major — must fix) | [N] |
| Severity 2 (minor — fix if in scope) | [N] |
| Severity 1 (cosmetic — note) | [N] |
| **Traceability coverage** | [N]% of stories have UX elements |
| **Reverse traceability** | [N]% of UX elements trace to a story |
| **State completeness** | [N]% of applicable states documented |
| **Microcopy specificity** | [N]% of data states have exact text |
| **Nielsen's heuristics** | [N]/10 pass, [N] warn, [N] fail |
| **Pages audited** | [N] in IA, [N] with layouts |
| **Components audited** | [N] patterns, [N] with full state tables |
| **Flows audited** | [N] flows, [N] with error recovery paths |

---

## Critical Findings (Severity 3-4)

These must be resolved before the UX plan is considered implementation-ready.

### [F-XXX] [Finding Title]

- **Severity:** [3 or 4]
- **Phase:** [Which audit phase]
- **Category:** [Completeness / Traceability / Consistency / Heuristic / State / Flow / Platform / Implementation]
- **Location:** [File → Section → Element]
- **Description:** [What's wrong — specific]
- **Evidence:** [What the spec says vs. what's expected]
- **Remediation:** [Exact fix — specific enough to execute]

[Repeat for each severity 3-4 finding]

---

## Minor Findings (Severity 2)

Fix if in scope. These won't block implementation but will cause friction.

| ID | Category | Location | Description | Remediation |
|----|----------|----------|-------------|-------------|
| F-XXX | [cat] | [location] | [what's wrong] | [fix] |

---

## Cosmetic Notes (Severity 1)

Note for future refinement. Not actionable now.

| ID | Category | Location | Description |
|----|----------|----------|-------------|
| F-XXX | [cat] | [location] | [note] |

---

## Phase-by-Phase Results

### Phase 2: Structural Completeness

| Section | Status | Notes |
|---------|--------|-------|
| 1. Overview & Principles | [Present/Missing/Incomplete] | [detail] |
| 2. Information Architecture | [Present/Missing/Incomplete] | [detail] |
| 3. Visual Hierarchy | [Present/Missing/Incomplete] | [detail] |
| 4. Page Layouts | [Present/Missing/Incomplete] | [detail] |
| 5. Component Specs | [Present/Missing/Incomplete] | [detail] |
| 6. Interaction Patterns | [Present/Missing/Incomplete] | [detail] |
| 7. Responsive Behavior | [Present/Missing/Incomplete] | [detail] |
| 8. Data States | [Present/Missing/Incomplete] | [detail] |
| 9. Accessibility | [Present/Missing/Incomplete] | [detail] |
| 10. User Flows | [Present/Missing/Incomplete] | [detail] |
| 11. Traceability | [Present/Missing/Incomplete] | [detail] |

**Placeholder count:** [N] placeholders found | [N] in critical paths | [N] in secondary elements

### Phase 3: Traceability

**Forward (Stories → UX):**
- Stories in scope: [N]
- Stories with UX coverage: [N] ([%])
- Uncovered stories: [list SM-XXX IDs or "none"]

**Backward (UX → Stories):**
- UX elements audited: [N]
- Elements with story source: [N] ([%])
- Orphan elements: [list or "none"]

**Cross-references verified:** [N] checked, [N] valid, [N] broken

### Phase 4: Consistency

| Check | Status | Findings |
|-------|--------|----------|
| Status name consistency | [Pass/Fail] | [details] |
| Page name consistency | [Pass/Fail] | [details] |
| Button label consistency | [Pass/Fail] | [details] |
| Field name consistency | [Pass/Fail] | [details] |
| Persona terminology | [Pass/Fail] | [details] |
| Navigation integrity | [Pass/Fail] | [details] |
| State pipeline completeness | [Pass/Fail] | [details] |

### Phase 5: Nielsen's Heuristics

| Heuristic | Status | Severity | Key Findings |
|-----------|--------|----------|-------------|
| H1: Visibility of system status | [Pass/Warn/Fail] | [max severity] | [summary] |
| H2: Match system and real world | [Pass/Warn/Fail] | [max severity] | [summary] |
| H3: User control and freedom | [Pass/Warn/Fail] | [max severity] | [summary] |
| H4: Consistency and standards | [Pass/Warn/Fail] | [max severity] | [summary] |
| H5: Error prevention | [Pass/Warn/Fail] | [max severity] | [summary] |
| H6: Recognition rather than recall | [Pass/Warn/Fail] | [max severity] | [summary] |
| H7: Flexibility and efficiency | [Pass/Warn/Fail] | [max severity] | [summary] |
| H8: Aesthetic and minimalist design | [Pass/Warn/Fail] | [max severity] | [summary] |
| H9: Error recovery | [Pass/Warn/Fail] | [max severity] | [summary] |
| H10: Help and documentation | [Pass/Warn/Fail] | [max severity] | [summary] |

**Cross-heuristic checks:**

| Check | Status | Finding |
|-------|--------|---------|
| H1 + H9: Error states have both status AND message | [Pass/Fail] | [detail] |
| H3 + H6: Escape hatches are visually discoverable | [Pass/Fail] | [detail] |
| H4 + H2: Consistent terminology is domain-appropriate | [Pass/Fail] | [detail] |
| H5 + H9: Prevention and recovery cover same errors | [Pass/Fail] | [detail] |
| H1 + H7: Status visible without extra interaction | [Pass/Fail] | [detail] |
| H6 + H10: Recognition aids align with help text | [Pass/Fail] | [detail] |

### Phase 6: State & Microcopy Completeness

**Component state coverage:**

| Component Pattern | Applicable States | Documented States | Coverage | Missing |
|-------------------|-------------------|-------------------|----------|---------|
| [pattern name] | [N] | [N] | [%] | [list missing states] |

**Microcopy audit:**

| Category | Total Required | With Exact Text | Specificity |
|----------|---------------|-----------------|-------------|
| Empty states (first-use) | [N] | [N] | [%] |
| Empty states (no-results) | [N] | [N] | [%] |
| Error messages | [N] | [N] | [%] |
| Success feedback | [N] | [N] | [%] |
| Button labels | [N] | [N] | [%] |

**Button automation audit:**

| Buttons Total | With Trigger | With Automation | With Result | With Error Handling | Complete |
|---------------|-------------|-----------------|-------------|--------------------|----|
| [N] | [N] | [N] | [N] | [N] | [%] |

### Phase 7: Interaction & Flow Completeness

**State machines:**

| State Machine | States | Transitions | Dead-ends | Orphans | Complete |
|---------------|--------|-------------|-----------|---------|----------|
| [name] | [N] | [N] | [N] | [N] | [Yes/No] |

**User flows:**

| Flow | Steps | Decision Points | Error Paths | Has Diagram | Complete |
|------|-------|-----------------|-------------|-------------|----------|
| [name] | [N] | [N] | [N] | [Yes/No] | [Yes/No] |

**Filter specifications:**

| Filter | Placement | Method | Multi-select | Logic | Clear | No-results | Default | Persistence | Complete |
|--------|-----------|--------|-------------|-------|-------|------------|---------|-------------|----------|
| [name] | [✓/✗] | [✓/✗] | [✓/✗] | [✓/✗] | [✓/✗] | [✓/✗] | [✓/✗] | [✓/✗] | [%] |

### Phase 8: Platform Compliance

| Check | Status | Notes |
|-------|--------|-------|
| Platform identified | [Yes/No] | [platform name] |
| Interactions feasible | [Pass/Warn/Fail] | [details] |
| Page types match platform | [Pass/Warn/Fail] | [details] |
| Responsive handling | [Native/Custom/Hybrid] | [details] |
| Accessibility handling | [Native/Custom/Hybrid] | [details] |

### Phase 9: Implementation Compliance

[Include only if implementation was reviewed]

| Page | Exists | Title Match | Navigation | Elements | States | Overall |
|------|--------|-------------|------------|----------|--------|---------|
| PG-XXX | [Y/N] | [Y/N] | [Y/N] | [%] | [%] | [Pass/Warn/Fail] |

---

## Remediation Priority

Recommended fix order (highest impact first):

1. **[F-XXX]** — [one-line description] — [why fix first]
2. **[F-XXX]** — [one-line description] — [why fix second]
3. **[F-XXX]** — [one-line description] — [why fix third]
[Continue for all severity 3+ findings]
