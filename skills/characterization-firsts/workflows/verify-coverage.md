# Workflow: Verify Coverage

<required_reading>
**Read now:** `references/mutation-testing.md`
</required_reading>

<scripts_to_use>
**Scripts for this workflow:**

1. `scripts/run_mutation.sh` - Executes mutation testing
2. `scripts/check_coverage.py` - Parses results and assesses confidence

```bash
# Run mutation testing
~/.claude/skills/characterization-first/scripts/run_mutation.sh \
    path/to/target.py \
    tests/characterization/test_target_char.py

# Check coverage and get structured report
python ~/.claude/skills/characterization-first/scripts/check_coverage.py \
    --threshold 80
```

The scripts handle:

- mutmut configuration
- Running tests before mutations (fail-fast if tests broken)
- Parsing results into actionable format
- Exit codes based on coverage confidence
</scripts_to_use>

<context>
Line coverage lies. 100% line coverage can still miss behavior changes.

Mutation testing answers: "If I change the code, will tests catch it?"

A surviving mutant = a behavior change that tests wouldn't catch = incomplete characterization.
</context>

<process>

**Step 1: Run mutation testing script**

Use the provided script which handles installation, configuration, and execution:

```bash
~/.claude/skills/characterization-first/scripts/run_mutation.sh \
    path/to/target.py \
    tests/characterization/test_target_char.py
```

The script will:

1. Verify mutmut is installed (install if needed)
2. Verify tests pass before mutating
3. Run mutation testing
4. Output results summary

**Manual alternative (if script unavailable):**

```bash
pip install mutmut
mutmut run --paths-to-mutate path/to/target.py
```

**Step 2: Analyze results with coverage script**

```bash
python ~/.claude/skills/characterization-first/scripts/check_coverage.py --threshold 80
```

This outputs a structured report with:

- Total mutants, killed, survived counts
- Confidence level (HIGH/MEDIUM/LOW)
- List of surviving mutants needing attention

**Manual inspection of survivors:**

```bash
mutmut results
mutmut show <mutant_id>
```

**Step 5: Triage survivors**

For each surviving mutant, classify it:

| Classification | Action | Example |
|----------------|--------|---------|
| **Missing test** | Write test to kill it | Changed `>` to `>=`, tests passed |
| **Equivalent mutant** | Accept (doesn't change behavior) | Changed `x = 1` to `x = +1` |
| **Dead code** | Consider removing in refactor | Mutated unreachable branch |

Document decisions:

```markdown
## Mutation Testing Results

| Mutant ID | Change | Classification | Action |
|-----------|--------|----------------|--------|
| 1 | line 45: > to >= | Missing test | Added test_boundary_condition |
| 2 | line 67: + to - | Missing test | Added test_calculation_sign |
| 3 | line 89: True to False | Equivalent | Accepted - logging only |
```

**Step 6: Kill missing mutants**

For each "Missing test" mutant:
1. Understand what behavior change the mutant represents
2. Write a characterization test that would catch it
3. Run `mutmut run` again to verify

```python
# Example: Mutant changed > to >=
def test_boundary_exclusive(self):
    """
    Characterization: boundary is exclusive (>), not inclusive (>=)
    Added to kill mutant #1
    """
    result = target_function(boundary_value)
    assert result == expected_exclusive_behavior
```

**Step 7: Iterate until satisfied**

Target: 0 surviving mutants (except accepted equivalents)

```bash
mutmut run
mutmut results
# Repeat until clean
```

**Step 8: Document final state**

```markdown
## Characterization Complete

- Total mutants generated: X
- Killed: Y
- Survived (accepted equivalents): Z
- Coverage confidence: HIGH/MEDIUM/LOW

Accepted survivors:
- Mutant #N: [reason]
```

**Step 9: Checkpoint**

Before proceeding to refactor-safely.md:
- [ ] Mutation testing completed
- [ ] All surviving mutants triaged
- [ ] Missing tests added to kill relevant mutants
- [ ] Only equivalent mutants survive
- [ ] Documentation updated

</process>

<blocking_rule>
**DO NOT proceed to refactor until:**
1. Mutation testing has run (or time budget expired)
2. All non-equivalent surviving mutants are killed OR explicitly accepted
3. User accepts the coverage level

**If mutation testing is slow (large files):**
1. First try `--quick` mode for faster assessment
2. Scope to specific line ranges you'll refactor: `--paths-to-mutate file.py:50-100`
3. Set a time budget (15 min) and accept survivors after budget expires
4. Document accepted survivors and proceed

If user says "mutation testing takes too long", offer pragmatic options:
"We can: (1) Run in quick mode, (2) Scope to just the lines you'll change, or (3) Set a 15-minute budget and accept the coverage we get. Which approach works for you?"

If mutmut is unavailable:
"Falling back to manual verification. For each function, I'll describe what would happen if each conditional/operation changed. This is less thorough but maintains discipline."
</blocking_rule>

<coverage_thresholds>
| Mutation Score | Confidence | Recommendation |
|----------------|------------|----------------|
| 90-100% killed | HIGH | Safe to refactor |
| 70-89% killed | MEDIUM | Review survivors, may proceed with caution |
| <70% killed | LOW | More characterization needed |

For critical code (payments, auth, data integrity): require HIGH confidence
For non-critical code: MEDIUM may be acceptable with user approval
</coverage_thresholds>

<success_criteria>
This workflow is complete when:
- [ ] Mutation testing executed
- [ ] All survivors triaged and documented
- [ ] Missing tests added
- [ ] Coverage confidence is acceptable
- [ ] User approves proceeding to refactor
</success_criteria>
