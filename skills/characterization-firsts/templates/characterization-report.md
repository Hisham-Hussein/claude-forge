# Characterization Report: {TARGET_NAME}

**Generated:** {DATE}
**Target:** {FILE_PATH}
**Status:** {PHASE} (SELECT | CAPTURE | VERIFY | REFACTOR | COMPLETE)

---

## Target Analysis

### Inputs

| Input | Type | Source | Example Value | Notes |
|-------|------|--------|---------------|-------|
| {param1} | {type} | {explicit/implicit} | {example} | {notes} |

### Outputs

| Output | Type | Destination | Description |
|--------|------|-------------|-------------|
| {output1} | {type} | {where} | {description} |

### Seams Identified

| Location | Type | What it enables |
|----------|------|-----------------|
| {line X} | {object/link/config} | {mocking capability} |

### Edge Cases

- [ ] Empty inputs
- [ ] Null/None values
- [ ] Boundary conditions
- [ ] Error conditions
- [ ] {additional edge cases}

---

## Characterization Tests

**Test file:** `tests/characterization/test_{target}_char.py`

### Test Coverage

| Test Name | Type | Status | Notes |
|-----------|------|--------|-------|
| test_basic_usage | Happy path | PASS | |
| test_empty_input | Edge case | PASS | |
| {test_name} | {type} | {status} | {notes} |

### Known Bugs Documented

| Bug | Test | Actual Behavior | Expected Behavior | Ticket |
|-----|------|-----------------|-------------------|--------|
| {bug_name} | {test} | {actual} | {expected} | {ticket} |

---

## Mutation Testing Results

**Tool:** mutmut
**Run date:** {DATE}

### Summary

| Metric | Value |
|--------|-------|
| Total mutants | {N} |
| Killed | {N} |
| Survived | {N} |
| Timeout | {N} |
| **Mutation score** | {X}% |

### Survivor Triage

| Mutant ID | Change | Classification | Action Taken |
|-----------|--------|----------------|--------------|
| {id} | {description} | Missing test / Equivalent / Dead code | {action} |

### Coverage Confidence

- [ ] HIGH (90%+) - Safe to refactor
- [ ] MEDIUM (70-89%) - Proceed with caution
- [ ] LOW (<70%) - More characterization needed

---

## Refactoring Log

### Planned Changes

1. [ ] {change 1}
2. [ ] {change 2}
3. [ ] {change 3}

### Executed Changes

| Change | Commit | Tests Passed | Notes |
|--------|--------|--------------|-------|
| {change} | {hash} | YES/NO | {notes} |

### Unexpected Failures

| Change | Test Failed | Root Cause | Resolution |
|--------|-------------|------------|------------|
| {change} | {test} | {cause} | {resolution} |

---

## Post-Refactoring Checklist

- [ ] All characterization tests pass
- [ ] No unexpected behavior changes
- [ ] Commit history shows atomic changes
- [ ] Ready for bug fixes (if any documented)
- [ ] Documentation updated (if needed)

---

## Learnings

**What we discovered:**
- {learning 1}
- {learning 2}

**Recommended follow-up:**
- {recommendation 1}
- {recommendation 2}
