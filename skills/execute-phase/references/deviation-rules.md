<overview>
During execution, you WILL discover work not in the plan. This is normal. These rules define when to fix automatically vs when to ask the user.

**Rule priority:** If Rule 4 applies → STOP. If Rules 1-3 apply → fix automatically. If unsure → Rule 4.
</overview>

<rule_1 name="auto_fix_bugs">
**RULE 1: Auto-fix bugs**

**Trigger:** Code doesn't work as intended (broken behavior, incorrect output, errors)

**Action:** Fix immediately, track for roadmap LOG.md

**Examples:**
- Wrong logic returning incorrect results
- Type errors, null pointer exceptions
- Broken validation (accepts invalid, rejects valid)
- Security vulnerabilities (SQL injection, XSS)
- Race conditions, infinite loops
- Memory/resource leaks

**Process:**
1. Fix the bug inline
2. Add/update tests to prevent regression
3. Verify fix works
4. Continue task
5. Track in LOG.md: `[Rule 1 - Bug] {description}`

**No user permission needed.** Bugs must be fixed for correct operation.
</rule_1>

<rule_2 name="auto_add_critical">
**RULE 2: Auto-add missing critical functionality**

**Trigger:** Code is missing essential features for correctness, security, or basic operation

**Action:** Add immediately, track for roadmap LOG.md

**Examples:**
- Missing error handling (no try/catch)
- No input validation (accepts malicious data)
- Missing null/undefined checks
- No authentication on protected routes
- Missing authorization checks
- No CSRF protection, missing CORS
- No rate limiting on public APIs
- Missing required database indexes
- No logging for errors

**Process:**
1. Add the missing functionality
2. Add tests for it
3. Verify it works
4. Continue task
5. Track in LOG.md: `[Rule 2 - Missing Critical] {description}`

**Critical = required for correct/secure operation**
**No user permission needed.** These aren't features—they're requirements for basic correctness.
</rule_2>

<rule_3 name="auto_fix_blockers">
**RULE 3: Auto-fix blocking issues**

**Trigger:** Something prevents completing the current task

**Action:** Fix immediately to unblock, track for roadmap LOG.md

**Examples:**
- Missing dependency (package not installed)
- Wrong types blocking compilation
- Broken import paths
- Missing environment variable
- Database connection config error
- Build configuration error
- Missing file referenced in code
- Circular dependency

**Process:**
1. Fix the blocking issue
2. Verify task can now proceed
3. Continue task
4. Track in LOG.md: `[Rule 3 - Blocking] {description}`

**No user permission needed.** Can't complete task without fixing blocker.
</rule_3>

<rule_4 name="ask_about_architectural">
**RULE 4: Ask about architectural changes**

**Trigger:** Fix/addition requires significant structural modification

**Action:** STOP, present to user, wait for decision

**Examples:**
- Adding new database table (not just column)
- Major schema changes (changing primary key)
- Introducing new service layer or pattern
- Switching libraries/frameworks
- Changing authentication approach
- Adding new infrastructure (queue, cache)
- Changing API contracts (breaking changes)
- Adding new deployment environment

**Process:**
1. STOP current task
2. Present to user:
   - What you found
   - Proposed change
   - Why needed
   - Impact
   - Alternatives
3. Wait for user decision
4. Implement decision
5. Continue

**User decision required.** These changes affect system design.
</rule_4>

<priority_order>
**When multiple rules could apply:**

1. **If Rule 4 applies** → STOP and ask user (architectural decision)
2. **If Rules 1-3 apply** → Fix automatically, track for LOG.md
3. **If genuinely unsure** → Apply Rule 4 (ask user)

**Edge case guidance:**
- "This validation is missing" → Rule 2 (critical for security)
- "This crashes on null" → Rule 1 (bug)
- "Need to add table" → Rule 4 (architectural)
- "Need to add column" → Rule 1 or 2 (depends: fixing bug or adding critical field)

**Ask yourself:** "Does this affect correctness, security, or ability to complete task?"
- YES → Rules 1-3 (fix automatically)
- MAYBE → Rule 4 (ask user)
</priority_order>

<logging_format>
**Track all deviations in roadmap/LOG.md:**

```markdown
### [DATE] - Work Unit [N]: [Name]
...
**Deviations:**
- [Rule 1 - Bug] Fixed null check in Influencer.validate()
- [Rule 2 - Missing Critical] Added input sanitization for username
- [Rule 3 - Blocking] Installed missing pytest-asyncio
```

Or if none: `**Deviations:** None - executed as planned.`
</logging_format>
