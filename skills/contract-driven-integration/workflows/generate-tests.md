# Generate Tests Workflow

Create contract test file from extracted assertions.

## Input

- **directive_path**: Path to the directive
- **extracted_contract**: Output from extract-contract workflow
- **script_mapping**: Output from map-to-scripts workflow

## Process

### Step 1: Create test file path

```
tests/contract/test_{directive_stem}_contract.py
```

Example: `directives/workflows/onboard_client.md` → `tests/contract/test_onboard_client_contract.py`

### Step 2: Generate test class structure

```python
"""
Contract tests for {directive_name}

Verifies alignment between:
- Directive: {directive_path}
- Scripts: {script_paths}

Generated: {date}
"""

import pytest
from pathlib import Path


class TestDirectiveContract:
    """Contract assertions for {directive_name}"""

    # === Input Contracts ===

    # === Output Contracts ===

    # === Process Contracts ===

    # === Edge Case Contracts ===
```

### Step 3: Generate input tests

For each input assertion:

```python
def test_accepts_{input_name}(self):
    """Script accepts {input_name} input as specified in directive"""
    # Import the primary script's main function or entry point
    # Verify it accepts the parameter without error
    # Note: May need to mock external calls
    pass  # TODO: Implement
```

For required inputs:
```python
def test_requires_{input_name}(self):
    """Script requires {input_name} - fails without it"""
    # Call without required input
    # Assert appropriate error
    pass  # TODO: Implement
```

### Step 4: Generate output tests

For each output assertion:

```python
def test_output_contains_{field}(self):
    """Output includes {field} as specified in directive"""
    # Call with valid inputs
    # Assert output has expected field
    pass  # TODO: Implement
```

For output format:
```python
def test_output_format_{format}(self):
    """Output is {format} as specified in directive"""
    # Call with valid inputs
    # Assert output matches expected format
    pass  # TODO: Implement
```

### Step 5: Generate process tests

For step ordering:
```python
def test_{step_a}_before_{step_b}(self):
    """Script performs {step_a} before {step_b} per directive"""
    # Use mocks or logs to verify step ordering
    pass  # TODO: Implement
```

For step presence:
```python
def test_includes_{step}(self):
    """Script includes step: {step_description}"""
    # Verify step occurs during execution
    pass  # TODO: Implement
```

### Step 6: Generate edge case tests

```python
def test_handles_{edge_case}(self):
    """Script handles {edge_case} as specified in directive"""
    # Trigger edge case condition
    # Verify expected behavior
    pass  # TODO: Implement
```

### Step 7: Add file verification tests

These tests verify the directive-script relationship exists:

```python
class TestContractStructure:
    """Verify contract structure is intact"""

    def test_directive_exists(self):
        """Directive file exists"""
        assert Path("{directive_path}").exists()

    def test_primary_script_exists(self):
        """Primary script exists"""
        assert Path("{primary_script}").exists()

    def test_directive_references_script(self):
        """Directive mentions the implementing script"""
        directive = Path("{directive_path}").read_text()
        assert "{script_name}" in directive
```

### Step 8: Add markers and skip decorators

For tests that need external resources:
```python
@pytest.mark.integration
def test_sends_email(self):
    """Requires Gmail API - integration test"""
```

For tests awaiting implementation:
```python
@pytest.mark.skip(reason="Contract assertion - implementation needed")
def test_placeholder(self):
    pass
```

### Step 9: Write test file

Create the complete test file at `tests/contract/test_{name}_contract.py`.

### Step 10: Run tests

Execute the generated tests:
```bash
pytest tests/contract/test_{name}_contract.py -v
```

Report:
- How many tests pass (structure tests)
- How many tests skip (need implementation)
- How many tests fail (potential contract violations)

## Output

Return:
1. Path to generated test file
2. Test counts by status
3. Next steps

Format:

```markdown
# Generated Contract Tests: {directive_name}

**Test file**: tests/contract/test_{name}_contract.py
**Generated**: {date}

## Test Counts

| Category | Count |
|----------|-------|
| Total | {n} |
| Passing | {n} |
| Skipped | {n} |
| Failing | {n} |

## Tests Generated

### Input Tests
- test_accepts_email
- test_requires_email
- test_accepts_name_optional

### Output Tests
- test_output_format_json
- test_output_contains_success
- test_output_contains_correlation_id

### Process Tests
- test_validates_before_processing
- test_checks_idempotency

### Edge Case Tests
- test_handles_invalid_email
- test_handles_duplicate

## Next Steps

1. Review generated tests
2. Implement `# TODO: Implement` test bodies
3. Run `pytest tests/contract/ -v` to verify contracts
4. Address any failing tests (contract violations)
```

## Notes

- Generated tests start as placeholders with `pass` or `skip`
- Structure tests (file existence) run immediately
- Behavioral tests need implementation based on script internals
- Tests should not require external services (mock them)
