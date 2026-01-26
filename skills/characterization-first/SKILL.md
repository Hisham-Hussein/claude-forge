---
name: characterization-first
description: Use when refactoring existing code, modifying legacy code, or about to change code behavior. Use when terms like "characterization test", "golden master", "capture behavior", or "safe refactoring" are mentioned. Enforces discipline of capturing current behavior before any code changes.
---

<essential_principles>

**The Iron Rule:** No refactor without characterization. Period.

Before touching ANY code:
1. **Capture** what it currently does (including bugs)
2. **Verify** your characterization is complete
3. **Only then** make changes

This skill enforces strict discipline. It will block progress until characterization tests exist.

**Why this matters:** 90% accuracy per step = 59% success over 5 steps. Characterization tests catch unintended behavior changes before they compound into failures.

**What characterization tests are NOT:**
- They are NOT assertions about correct behavior
- They are NOT contract tests
- They document ACTUAL behavior, bugs and all

</essential_principles>

<rationalization_table>
**Common Excuses - NEVER Fall For These**

| Excuse | Reality |
|--------|---------|
| "I understand the code thoroughly" | Understanding doesn't prevent mistakes. Characterize anyway. |
| "The changes are simple/obvious" | Simple changes break things. Every experienced dev has learned this. |
| "I can test after to verify" | Tests-after verify what you built. Tests-first verify what it did. Different goals. |
| "I'm almost done, stopping wastes work" | Sunk cost fallacy. Stop. Delete. Characterize. Start over. |
| "I'll test the complex parts only" | You don't know which parts are complex until you characterize. |
| "I've been testing manually" | Manual testing isn't reproducible. Write the test. |
| "Being dogmatic wastes time" | Following process IS pragmatic. It prevents bugs. |
| "The team doesn't do this" | Be the change. Broken processes stay broken. |
| "This is different because..." | Every violation feels different. None are. |

**Red Flags - STOP Immediately**

If you're thinking any of these, you're rationalizing:
- "Just this once..."
- "I'll do it properly next time..."
- "The spirit matters more than the letter..."
- "It's just renaming/extracting/simplifying..."

**All of these mean: You're about to violate. Don't.**
</rationalization_table>

<objective>
Enforce the discipline of capturing current code behavior as tests before any modification. Produces pytest-based characterization tests that document what code DOES (not what it should do), verifies coverage completeness via mutation testing with mutmut, and only then permits atomic refactoring changes.
</objective>

<quick_start>

**Starting a characterization:**
1. Tell me what code you want to refactor
2. I'll guide you through SELECT → CAPTURE → VERIFY → REFACTOR phases
3. You cannot skip phases - each gate must pass

**Example:**
```
User: I want to refactor execution/utils/validation.py
Skill: Let's characterize it first. Reading the file to identify seams...
```

</quick_start>

<intake>
What would you like to do?

1. **Start new characterization** - Begin characterizing code before refactoring
2. **Resume characterization** - Continue an in-progress characterization
3. **Verify coverage** - Run mutation testing on existing characterization tests
4. **Proceed to refactor** - I have characterization tests and want to make changes

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "start", "new", "characterize", "begin" | `workflows/select-target.md` |
| 2, "resume", "continue" | Ask for target file, then `workflows/capture-behavior.md` |
| 3, "verify", "coverage", "mutation" | `workflows/verify-coverage.md` |
| 4, "refactor", "proceed", "ready" | `workflows/refactor-safely.md` |

**After reading the workflow, follow it exactly.**
</routing>

<workflow_sequence>
```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ SELECT  │ →  │ CAPTURE │ →  │ VERIFY  │ →  │REFACTOR │
│ target  │    │ behavior│    │ coverage│    │ safely  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
  Identify      Write tests     Mutation      Atomic
  seams and     that capture    testing to    changes with
  I/O points    current I/O     find gaps     test after each
```

**Gate Requirements:**
- SELECT → CAPTURE: Target identified, seams documented
- CAPTURE → VERIFY: Characterization tests written and passing
- VERIFY → REFACTOR: Mutation testing shows adequate coverage
- REFACTOR complete: All tests still pass, changes committed
</workflow_sequence>

<reference_index>
All domain knowledge in `references/`:

**Seams:** seam-identification.md - Finding testable boundaries
**Testing:** golden-master-pattern.md - Recording bugs as expected
**Coverage:** mutation-testing.md - Verifying characterization completeness
**TDD Testing:** pressure-scenarios.md - Pressure test scenarios for skill validation
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| select-target.md | Identify code to characterize, find seams |
| capture-behavior.md | Write characterization tests |
| verify-coverage.md | Run mutation testing |
| refactor-safely.md | Make atomic changes with verification |
</workflows_index>

<scripts_index>
Deterministic scripts in `scripts/` - use these for reliable execution:

| Script | Purpose | When to Use |
|--------|---------|-------------|
| analyze_target.py | AST-based analysis of Python file | SELECT phase: identify seams, inputs/outputs automatically |
| scaffold_char_tests.py | Generate test file skeleton from analysis | CAPTURE phase: create structured test template |
| run_mutation.sh | Run mutmut with proper configuration | VERIFY phase: execute mutation testing |
| check_coverage.py | Parse mutation results into structured report | VERIFY phase: assess coverage confidence |

**Usage pattern:**
```bash
# SELECT: Analyze target (text report to stdout, or JSON with --json)
python scripts/analyze_target.py path/to/target.py
python scripts/analyze_target.py path/to/target.py --json > .tmp/analysis.json

# CAPTURE: Scaffold tests from target file
python scripts/scaffold_char_tests.py path/to/target.py

# VERIFY: Run mutation testing
./scripts/run_mutation.sh path/to/target.py tests/characterization/test_target_char.py

# VERIFY: Check coverage
python scripts/check_coverage.py --threshold 80
```
</scripts_index>

<success_criteria>
Characterization is complete when:
- [ ] Target code identified with all inputs/outputs documented
- [ ] Characterization tests written and passing
- [ ] Mutation testing shows no surviving mutants (or survivors explicitly accepted)
- [ ] Refactoring changes are atomic (one change, run tests, commit)
- [ ] All characterization tests still pass after refactoring
</success_criteria>
