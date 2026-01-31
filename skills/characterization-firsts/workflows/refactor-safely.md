# Workflow: Refactor Safely

<required_reading>
None - this workflow is self-contained.
(References from previous workflows should already be loaded)
</required_reading>

<context>
You have:
- Characterization tests covering current behavior
- Verified coverage via mutation testing
- Documented all inputs, outputs, and seams

Now you can refactor. But ONLY with atomic changes and continuous verification.
</context>

<process>

**Step 1: Plan the refactoring**

List specific changes to make:

```markdown
## Refactoring Plan for {target}

1. [ ] Extract helper function for X
2. [ ] Rename variable Y to Z
3. [ ] Simplify conditional at line N
4. [ ] ... (each change is ONE operation)
```

**Step 2: The atomic change loop**

For EACH change in your plan:

```
┌─────────────────────────────────────────┐
│           ATOMIC CHANGE LOOP            │
│                                         │
│   1. Make ONE small change              │
│              ↓                          │
│   2. Run ALL characterization tests     │
│              ↓                          │
│   3. Tests pass?                        │
│      YES → Commit, next change          │
│      NO  → Revert, investigate          │
│                                         │
└─────────────────────────────────────────┘
```

**Step 3: Execute each change**

```bash
# Before each change
git status  # Clean working tree

# Make ONE change (e.g., rename a variable)
# ... edit file ...

# Run characterization tests
pytest tests/characterization/test_{target}_char.py -v

# If pass:
git add -p  # Review changes
git commit -m "refactor({target}): rename foo to bar"

# If fail:
git checkout -- path/to/file  # Revert
# Investigate why
```

**Step 4: Handle unexpected failures**

When a characterization test fails unexpectedly:

1. **STOP** - Do not continue refactoring
2. **Revert** - Return to last known good state
3. **Investigate** - Why did this test fail?

Possible causes:
| Cause | Action |
|-------|--------|
| Refactor changed behavior | Fix the refactor, not the test |
| Incomplete characterization | Add missing test FIRST, then retry refactor |
| Test was wrong | Rare - verify against actual behavior |

```markdown
## Unexpected Failure Log

| Change | Test Failed | Root Cause | Resolution |
|--------|-------------|------------|------------|
| Extracted helper | test_edge_case | Missed closure variable | Added test for closure, then refactored |
```

**Step 5: Maintain green state**

**THE RULE:** Never have more than one failing test.

If you're in a failing state:
- Revert to green
- Make smaller change
- Re-verify

```bash
# Good rhythm
edit → test → commit → edit → test → commit

# Bad rhythm
edit → edit → edit → test → ?!?!
```

**Step 6: Complete refactoring**

When all planned changes are made:

```bash
# Final verification
pytest tests/characterization/test_{target}_char.py -v

# Run mutation testing again (optional but recommended)
mutmut run --paths-to-mutate path/to/target.py

# If all green:
git log --oneline -10  # Review commit history
```

**Step 7: Post-refactoring review**

Check:
- [ ] All characterization tests still pass
- [ ] Code is cleaner/better than before
- [ ] No new behavior introduced (only structural changes)
- [ ] Commit history shows atomic changes

Now you can:
- Fix known bugs (with new tests for correct behavior)
- Add new features (with new tests)
- The characterization tests become regression tests

</process>

<blocking_rule>
**Refactoring discipline violations:**

If you catch yourself:
- Making multiple changes before testing → STOP, revert, do one at a time
- "Fixing" a test instead of the refactor → STOP, the test is right
- Skipping tests because "it's a small change" → STOP, run tests anyway
- Batching commits → STOP, commit after each green

The discipline IS the skill. Breaking it defeats the purpose.
</blocking_rule>

<commit_message_format>
Use conventional commits with context:

```
refactor({target}): {what changed}

Characterization tests verified behavior unchanged.
```

Examples:
- `refactor(validation): extract is_valid_email helper`
- `refactor(parser): rename temp to parsed_data`
- `refactor(api_client): simplify retry logic`
</commit_message_format>

<when_to_stop>
**Stop refactoring when:**
- All planned changes complete
- Code meets refactoring goals
- Further changes would be "nice to have"

**Do not:**
- Keep going because code "could be better"
- Add features during refactoring
- Fix bugs during refactoring (do that separately)
</when_to_stop>

<success_criteria>
This workflow is complete when:
- [ ] All planned refactoring changes applied
- [ ] Each change committed atomically
- [ ] All characterization tests pass
- [ ] No unexpected behavior changes
- [ ] Code review shows clean diff
</success_criteria>

<post_refactoring>
After successful refactoring:

1. **Keep characterization tests** - They're now regression tests
2. **Fix known bugs** - Now you can change behavior (with new tests)
3. **Update documentation** - If code structure changed significantly
4. **Consider**: Can contract tests (Skill 2) formalize the expected behavior?
</post_refactoring>
