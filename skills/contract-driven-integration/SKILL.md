---
name: contract-driven-integration
description: Use when verifying alignment between directives and their implementations (scripts OR plans). Detects when specifications drift from implementations. Triggers include "check contract", "verify directive matches script", "verify plan against principles", "generate contract tests", "find misalignments", or when modifying scripts/plans that implement directives.
---

<objective>
Formalize the implicit contract between directives (specifications) and execution scripts (implementations). Generate tests that verify alignment. Detect drift in both directions.
</objective>

<essential_principles>

<contract_definition>
A directive is a specification. A script is an implementation. The contract is the set of promises the directive makes that the script must fulfill:

| Directive Section | Contract Assertion |
|-------------------|-------------------|
| **Trigger** | Script is callable under stated conditions |
| **Inputs** | Script accepts all declared inputs |
| **Tools/Scripts** | Script uses specified tools/dependencies |
| **Process** | Script follows stated workflow steps |
| **Outputs** | Script produces declared outputs |
| **Edge Cases** | Script handles stated edge cases |
</contract_definition>

<contract_types>
The skill handles two types of contracts:

| Contract Type | Specification | Implementation | Output |
|---------------|---------------|----------------|--------|
| **Directive → Script** | Workflow directive (e.g., `onboard_client.md`) | Python script (e.g., `onboard_client.py`) | Python contract tests |
| **Strategic → Plan** | Strategic directive (e.g., `architecture_principles.md`) | Project plan (e.g., `PLAN.md`) | Markdown alignment report |

**When to use which:**
- **Directive → Script**: Verifying executable code implements an SOP
- **Strategic → Plan**: Verifying a project plan addresses all principles from a strategic document

Strategic contracts check *coverage* (does the plan mention each principle?), not *behavior* (does code execute correctly?).
</contract_types>

<bidirectional_checking>
Contracts break in two ways:

1. **Directive Drift**: Directive promises something the script doesn't do
   - Example: Directive says "sends Slack notification" but script doesn't

2. **Script Drift**: Script does something the directive doesn't document
   - Example: Script writes to database but directive doesn't mention it

Both are contract violations. This skill catches both.
</bidirectional_checking>

<flexible_parsing>
Not all directives follow the same format. Parse what exists:
- Look for common section headers (Trigger, Inputs, Process, Outputs, etc.)
- Extract implicit contracts from prose descriptions
- Document gaps rather than enforcing strict format
- Strategic directives differ from workflow directives
</flexible_parsing>

<test_organization>
Each directive gets its own contract test file:
- `tests/contract/test_{directive_name}_contract.py`
- Tests are assertions about the directive-script relationship
- Easy to maintain and trace failures to specific contracts
</test_organization>

</essential_principles>

<intake>
What would you like to do?

1. **Extract contract** - Parse a directive to identify its contract assertions
2. **Map to scripts** - Identify which scripts implement a directive
3. **Generate tests** - Create contract tests for a directive
4. **Detect drift** - Check if directives and scripts are aligned
5. **Full audit** - Run all workflows on a directive
6. **Verify plan alignment** - Check if a project plan addresses all principles from a strategic directive

**Provide the directive path with your selection.**

For option 6, also provide the plan path (e.g., `.planning/PLAN.md`).
</intake>

<routing>
| Response | Workflow | Purpose |
|----------|----------|---------|
| 1, "extract", "parse" | workflows/extract-contract.md | Parse directive → assertions |
| 2, "map", "scripts", "mapping" | workflows/map-to-scripts.md | Create directive→script mapping |
| 3, "generate", "tests", "create tests" | workflows/generate-tests.md | Produce contract test file |
| 4, "detect", "drift", "check", "verify" | workflows/detect-drift.md | Find misalignments (directive→script) |
| 5, "full", "audit", "all" | Run all workflows in sequence | Complete contract verification |
| 6, "plan", "principles", "strategic" | workflows/verify-plan-alignment.md | Check plan covers strategic principles |

**After selecting a workflow, read it and follow exactly.**
</routing>

<quick_reference>

<test_structure>
**Contract Test Structure:**

```python
# tests/contract/test_{directive}_contract.py

class TestDirectiveContract:
    """Contract tests for {directive_name}"""

    # Input contracts
    def test_accepts_required_inputs(self):
        """Script accepts inputs declared in directive"""

    # Output contracts
    def test_produces_declared_outputs(self):
        """Script produces outputs promised in directive"""

    # Process contracts
    def test_follows_stated_workflow(self):
        """Script follows process steps in directive"""

    # Edge case contracts
    def test_handles_declared_edge_cases(self):
        """Script handles edge cases documented in directive"""
```
</test_structure>

<mapping_format>
**Mapping File Format:**

```json
{
  "directives/workflows/onboard_client.md": {
    "scripts": ["execution/onboard_client.py"],
    "last_verified": "2026-01-19",
    "contract_status": "aligned"
  }
}
```
</mapping_format>

</quick_reference>

<success_criteria>
Contract verification complete when:
- [ ] Directive parsed into testable assertions
- [ ] Script(s) identified for directive
- [ ] Contract tests generated and passing
- [ ] No unaddressed drift detected (or drift documented in backlog)
- [ ] Mapping file updated
</success_criteria>
