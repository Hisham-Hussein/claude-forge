<overview>
Mutation testing verifies test quality by introducing small bugs (mutants) and checking if tests catch them. Surviving mutants reveal gaps in characterization.
</overview>

<why_mutation_testing>

**Line coverage lies:**
```python
def calculate_discount(price, is_member):
    if is_member:
        return price * 0.9  # 10% discount
    return price

# This test has 100% line coverage but misses behavior
def test_discount():
    result = calculate_discount(100, True)
    assert result is not None  # Weak assertion!
```

**Mutation testing exposes the gap:**
- Mutant: Change `0.9` to `0.8`
- Test still passes (only checks `is not None`)
- **Mutant survives** → characterization incomplete

</why_mutation_testing>

<mutmut_basics>

**Installation:**
```bash
pip install mutmut
```

**Configuration (setup.cfg):**
```ini
[mutmut]
paths_to_mutate=path/to/target.py
tests_dir=tests/characterization/
runner=pytest -x tests/characterization/test_target_char.py
```

**Run mutation testing:**
```bash
mutmut run
```

**View results:**
```bash
mutmut results      # Summary
mutmut show <id>    # Specific mutant
mutmut html         # HTML report
```

</mutmut_basics>

<mutation_types>

mutmut applies these mutations:

| Mutation | Example | What it tests |
|----------|---------|---------------|
| **Arithmetic** | `+` → `-` | Calculation correctness |
| **Comparison** | `>` → `>=` | Boundary conditions |
| **Boolean** | `True` → `False` | Conditional logic |
| **Constant** | `10` → `11` | Magic numbers |
| **Return** | `return x` → `return None` | Return value usage |
| **String** | `"foo"` → `"XXfooXX"` | String handling |

</mutation_types>

<interpreting_results>

**Mutation score = killed / total**

| Score | Interpretation |
|-------|----------------|
| 90-100% | Excellent - characterization is thorough |
| 70-89% | Good - review survivors for gaps |
| 50-69% | Fair - significant gaps in characterization |
| <50% | Poor - major rework needed |

**For each survivor:**

```bash
mutmut show 42
```

```
--- original
+++ mutant
@@ -10,7 +10,7 @@
 def calculate_total(items):
     total = 0
     for item in items:
-        total += item.price
+        total -= item.price  # <-- Mutant survived!
     return total
```

</interpreting_results>

<triaging_survivors>

<classification name="missing_test">
**Missing Test** - Write a test to kill it

The mutant changes behavior that tests don't verify.

```python
# Survivor: Changed + to -
# Fix: Add test that verifies sum is positive/increasing
def test_total_adds_prices():
    items = [Item(10), Item(20)]
    result = calculate_total(items)
    assert result == 30  # Will fail if + becomes -
```
</classification>

<classification name="equivalent">
**Equivalent Mutant** - Accept it

The mutation doesn't change observable behavior.

```python
# Survivor: Changed x = 1 to x = +1
# These are equivalent - no test can distinguish them
```

Document and accept:
```python
# Accepted equivalent mutant #42: x = 1 vs x = +1
```
</classification>

<classification name="dead_code">
**Dead Code** - Consider removal

The mutated code is never executed.

```python
def process(data):
    if never_true_condition:
        return mutated_code  # Never reached
    return normal_path
```

Flag for removal during refactoring.
</classification>

<classification name="weak_oracle">
**Weak Oracle** - Strengthen assertion

Test runs the code but doesn't verify result properly.

```python
# Weak oracle - mutant survives
def test_process():
    result = process(data)
    assert result  # Only checks truthiness

# Strong oracle - kills mutant
def test_process():
    result = process(data)
    assert result == {"status": "success", "count": 5}
```
</classification>

</triaging_survivors>

<practical_workflow>

**Step 1: Initial run**
```bash
mutmut run --paths-to-mutate path/to/target.py
```

**Step 2: Quick triage**
```bash
mutmut results
# Shows: X killed, Y survived, Z timeout
```

**Step 3: Investigate survivors**
```bash
for id in $(mutmut results | grep "survived" | cut -d' ' -f1); do
    mutmut show $id
done
```

**Step 4: Kill or accept**

For each survivor:
1. Is it equivalent? → Accept and document
2. Missing test? → Write test
3. Dead code? → Flag for removal
4. Weak oracle? → Strengthen assertion

**Step 5: Iterate**
```bash
mutmut run  # Re-run after adding tests
```

Repeat until satisfied with mutation score.

</practical_workflow>

<time_optimization>

Mutation testing is slow. Optimize with:

**Use quick mode for initial assessment:**
```bash
mutmut run --quick  # Fewer mutation operators, much faster
```

**Scope to lines you'll actually refactor:**
```bash
# Only mutate lines 50-100 (what you're changing)
mutmut run --paths-to-mutate path/to/target.py:50-100
```

**Run on specific file:**
```bash
mutmut run --paths-to-mutate path/to/target.py
```

**Run subset of mutations:**
```bash
mutmut run --mutations-from 1 --mutations-to 50
```

**Use faster test runner:**
```ini
[mutmut]
runner=pytest -x --tb=no -q  # Fast fail, minimal output
```

**Set a time budget, not a coverage target:**
For large files (300+ lines), aim for "15 minutes of mutation testing" rather than "100% mutation coverage." Accept survivors after the budget expires and document them.

**Cache results:**
mutmut caches results in `.mutmut-cache`. Delete only when source changes significantly.

</time_optimization>

<when_mutmut_unavailable>

If mutmut can't be installed:

**Manual mutation review:**

1. Read each conditional in target code
2. Ask: "If I changed this condition, would tests catch it?"
3. For each operation, ask: "If I changed +/-/*/÷, would tests catch it?"
4. Document gaps and write tests

Less thorough but maintains discipline.

</when_mutmut_unavailable>
