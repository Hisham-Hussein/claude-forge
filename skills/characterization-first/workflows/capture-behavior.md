# Workflow: Capture Behavior

<required_reading>
**Read now:** `references/golden-master-pattern.md`
</required_reading>

<scripts_to_use>
**Primary script:** `scripts/scaffold_char_tests.py`

Generate test skeleton from the target file:

```bash
python ~/.claude/skills/characterization-first/scripts/scaffold_char_tests.py \
    path/to/target.py \
    --output tests/characterization/
```

The script creates:

- Test file with proper structure and imports
- Test stubs for each function found
- Mock fixtures for identified seams
- Parametrized test templates
- Known bugs section (to fill in during testing)

**After scaffolding:** Fill in the actual assertions by running the code and capturing outputs.
</scripts_to_use>

<context>
Characterization tests capture what code DOES, not what it SHOULD do. If the code has bugs, the test captures the buggy behavior. We fix bugs AFTER refactoring, not during.
</context>

<process>

**Step 1: Generate test scaffold**

Run the scaffolding script on the target file:

```bash
python ~/.claude/skills/characterization-first/scripts/scaffold_char_tests.py \
    path/to/target.py \
    --output tests/characterization/
```

This creates a structured test file. If running manually, use this template:

```python
# tests/characterization/test_{target_name}_char.py
"""
Characterization tests for {target_name}

These tests capture CURRENT behavior, including known bugs.
DO NOT "fix" failing tests - they document actual behavior.

Generated: {date}
Target: {file_path}
"""

import pytest
from {module} import {function_or_class}
```

**Step 2: Write happy path tests**

Start with the most common usage patterns:

```python
class TestCharacterization{TargetName}:
    """Characterization tests - capture current behavior"""

    def test_basic_usage(self):
        """Capture: Basic invocation with typical inputs"""
        # Setup
        input_data = {...}  # From select-target analysis

        # Execute
        result = target_function(input_data)

        # Characterize (not assert correctness)
        assert result == {...}  # Actual output, even if "wrong"
```

**Step 3: Write edge case tests**

For each edge case identified in select-target:

```python
    def test_empty_input(self):
        """Capture: Behavior with empty input"""
        result = target_function({})
        assert result == {...}  # What it actually does

    def test_none_value(self):
        """Capture: Behavior with None"""
        result = target_function(None)
        # If it raises, capture that:
        # with pytest.raises(TypeError):
        #     target_function(None)
```

**Step 4: Capture side effects**

If code has side effects (file writes, API calls), capture them:

```python
    def test_side_effects(self, tmp_path, mocker):
        """Capture: File write behavior"""
        mock_write = mocker.patch('builtins.open', mocker.mock_open())

        target_function(data)

        # Capture what was written
        mock_write.assert_called_once_with(...)
        handle = mock_write()
        handle.write.assert_called_with(...)
```

**Step 5: Document bugs as "expected"**

When you discover buggy behavior, document it:

```python
    def test_known_bug_off_by_one(self):
        """
        CHARACTERIZATION: Current behavior (bug)

        The function returns 99 when it should return 100.
        This is a known bug that will be fixed AFTER refactoring.
        DO NOT change this assertion during refactoring.
        """
        result = calculate_percentage(100, 100)
        assert result == 99  # Bug: off-by-one error
```

**Step 6: Run tests**

```bash
pytest tests/characterization/test_{target}_char.py -v
```

All tests MUST pass before proceeding. If a test fails:
- The test is wrong (you misunderstood the behavior)
- Fix the test to match actual behavior
- Do NOT fix the code

**Step 7: Add parametrized tests for coverage**

Expand coverage with parametrized tests:

```python
    @pytest.mark.parametrize("input_val,expected", [
        ("valid", {"status": "ok"}),
        ("empty", {}),
        ("unicode", {"name": "caf\u00e9"}),
        ("special", {"chars": "a&b<c>d"}),
    ])
    def test_input_variations(self, input_val, expected):
        """Capture: Various input handling"""
        result = target_function(input_val)
        assert result == expected
```

**Step 8: Checkpoint**

Before proceeding to verify-coverage.md:
- [ ] All happy path tests written and passing
- [ ] All edge case tests written and passing
- [ ] Side effects captured with mocks
- [ ] Bugs documented as "expected behavior"
- [ ] Test file runs green

</process>

<blocking_rule>
**DO NOT proceed to verify-coverage until:**
1. All characterization tests pass
2. No tests are "expected failures" (xfail) - they must assert actual behavior

If user says "these tests are good enough", respond:
"We need to verify coverage with mutation testing. Incomplete characterization means refactoring could break things we didn't test."
</blocking_rule>

<anti_patterns>
<pitfall name="fixing_bugs_in_tests">
**WRONG:** "This test says result is 99 but it should be 100, let me fix the code"
**RIGHT:** "This test captures that result is currently 99. We document this as a bug and fix it AFTER refactoring."
</pitfall>

<pitfall name="asserting_correctness">
**WRONG:** `assert is_valid(result)  # Check if valid`
**RIGHT:** `assert result == {"status": "invalid", "error": "..."}`  # Capture actual output
</pitfall>

<pitfall name="skipping_edge_cases">
**WRONG:** "Edge cases are obvious, I'll skip them"
**RIGHT:** Test every edge case - they're where refactoring breaks
</pitfall>
</anti_patterns>

<success_criteria>
This workflow is complete when:
- [ ] Test file created with proper structure
- [ ] Happy path tests written and passing
- [ ] Edge case tests written and passing
- [ ] Side effects captured with mocks
- [ ] Bugs documented (not fixed)
- [ ] All tests run green
- [ ] Ready for mutation testing
</success_criteria>
