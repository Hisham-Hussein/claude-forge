<overview>
The Golden Master pattern captures program output as a reference, then compares future runs against this "golden" baseline. It's ideal for characterizing complex behavior you don't fully understand.
</overview>

<when_to_use>
Use Golden Master when:
- Output is complex (large data structures, formatted text)
- Behavior is hard to specify precisely
- You're characterizing legacy code
- The "correct" output is whatever it currently produces

Do NOT use Golden Master when:
- Output is simple (single values, booleans)
- You know exactly what output should be
- Output is non-deterministic (timestamps, random IDs)
</when_to_use>

<implementation>

<basic_pattern>
**Basic Golden Master Test**

```python
import json
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent / "golden"

def test_process_data_golden_master():
    """
    Golden Master: Captures current output as baseline.
    If output changes, test fails - review diff to decide if change is intentional.
    """
    input_data = load_test_input()
    result = process_data(input_data)

    golden_file = GOLDEN_DIR / "process_data_output.json"

    if not golden_file.exists():
        # First run: create the golden master
        golden_file.parent.mkdir(parents=True, exist_ok=True)
        golden_file.write_text(json.dumps(result, indent=2, sort_keys=True))
        pytest.fail("Golden master created. Review and commit if correct.")

    # Subsequent runs: compare against golden master
    expected = json.loads(golden_file.read_text())
    assert result == expected, f"Output changed from golden master"
```
</basic_pattern>

<pytest_snapshot>
**Using pytest-snapshot (recommended)**

```bash
pip install pytest-snapshot
```

```python
def test_process_data(snapshot):
    """Characterization test using snapshot"""
    result = process_data(test_input)
    snapshot.assert_match(result, "process_data_output.json")
```

Update snapshots when behavior intentionally changes:
```bash
pytest --snapshot-update
```
</pytest_snapshot>

<handling_nondeterminism>
**Handling Non-Deterministic Output**

When output contains timestamps, IDs, or random values:

```python
import re

def normalize_output(output):
    """Remove non-deterministic parts for comparison"""
    # Replace timestamps
    output = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', 'TIMESTAMP', output)
    # Replace UUIDs
    output = re.sub(r'[a-f0-9-]{36}', 'UUID', output)
    # Replace auto-increment IDs (if pattern known)
    output = re.sub(r'"id": \d+', '"id": ID', output)
    return output

def test_with_normalization(snapshot):
    result = process_data(test_input)
    normalized = normalize_output(json.dumps(result))
    snapshot.assert_match(normalized, "process_data_normalized.json")
```
</handling_nondeterminism>

</implementation>

<documenting_bugs>

When Golden Master captures buggy behavior:

```python
def test_percentage_calculation_golden_master():
    """
    CHARACTERIZATION TEST - Documents current behavior

    KNOWN BUG: Returns 99 when it should return 100 (off-by-one).
    This test captures the BUG, not the correct behavior.
    DO NOT "fix" this test during refactoring.

    Bug ticket: ISSUE-123
    Fix planned for: After refactoring complete
    """
    result = calculate_percentage(100, 100)

    # This is the ACTUAL output (buggy)
    assert result == 99

    # NOT the correct output:
    # assert result == 100  # <-- DO NOT USE
```

**Why document bugs this way:**
1. Prevents accidental "fixes" during refactoring
2. Creates explicit record of known issues
3. Separates "changing behavior" from "changing structure"
</documenting_bugs>

<multiple_golden_files>

For complex systems, organize golden files by scenario:

```
tests/
└── golden/
    ├── happy_path/
    │   ├── basic_input.json
    │   ├── basic_output.json
    │   └── basic_side_effects.json
    ├── edge_cases/
    │   ├── empty_input.json
    │   ├── empty_output.json
    │   └── unicode_input.json
    └── errors/
        ├── invalid_input.json
        └── error_response.json
```

</multiple_golden_files>

<updating_golden_masters>

**When to update Golden Masters:**

| Scenario | Action |
|----------|--------|
| Refactoring (structure change) | Do NOT update - test should pass |
| Bug fix (intentional behavior change) | Update after verifying new output |
| New feature | Create new golden file |
| Environment difference | Normalize the output |

**Update workflow:**
1. Run test, see failure
2. Review diff carefully
3. If change is intentional: `pytest --snapshot-update`
4. If change is unintentional: investigate and fix code
5. Commit updated golden files with explanation
</updating_golden_masters>

<anti_patterns>

<pitfall name="golden_everything">
**Don't Golden Master everything**

Simple assertions are clearer:
```python
# Bad - overkill for simple output
snapshot.assert_match({"count": 5}, "count.json")

# Good - direct assertion
assert result["count"] == 5
```
</pitfall>

<pitfall name="ignoring_failures">
**Don't blindly update**

If golden master fails, INVESTIGATE:
- Was change intentional?
- Did refactoring change behavior?
- Is characterization incomplete?

Never run `--snapshot-update` without understanding why.
</pitfall>

</anti_patterns>
