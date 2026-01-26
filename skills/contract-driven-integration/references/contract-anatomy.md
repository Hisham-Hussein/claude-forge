# Contract Anatomy

What makes a contract between a directive and its implementing scripts.

## Definition

A **contract** is the set of promises a directive makes that scripts must fulfill. It's the implicit agreement between specification (directive) and implementation (script).

## Contract Components

### 1. Preconditions
What must be true before the script runs.

- Required inputs and their formats
- Environment setup (env vars, credentials)
- File dependencies (templates, configs)
- System state (no concurrent runs, etc.)

### 2. Postconditions
What must be true after the script runs successfully.

- Output format and required fields
- Side effects (files created, APIs called)
- State changes (database writes, cache updates)

### 3. Invariants
What remains true throughout execution.

- Idempotency guarantees
- Data integrity constraints
- Resource limits respected

### 4. Error Contracts
What happens when things fail.

- Which errors are expected/handled
- Error output formats
- Cleanup/compensation actions
- Retry behavior

## Contract Strength

| Level | Description | Verification |
|-------|-------------|--------------|
| **Implicit** | Understood but not written | Manual review only |
| **Documented** | Written in directive | Human-readable |
| **Tested** | Has contract tests | Automated verification |
| **Enforced** | CI blocks violations | Prevents drift |

Goal: Move all contracts from implicit → enforced.

## Contract vs. Implementation Detail

**Contract** (include in directive):
- Function accepts email parameter
- Returns JSON with success field
- Sends notification on completion

**Implementation detail** (don't include):
- Uses `re.match()` for email validation
- JSON serialization via `json.dumps()`
- Notification uses `requests.post()` internally

Rule: If changing it would break callers, it's a contract. If changing it is invisible to callers, it's implementation detail.

## Contract Violations

### Type 1: Directive Drift
Directive says X, script doesn't do X.

**Example**: Directive says "sends Slack notification on failure" but script doesn't.

**Fix**: Either update script to match directive, or update directive to match reality.

### Type 2: Script Drift
Script does Y, directive doesn't mention Y.

**Example**: Script writes audit log to database, directive doesn't mention database.

**Fix**: Either document the behavior, or remove it if unintentional.

### Type 3: Contradiction
Directive says X, script does opposite of X.

**Example**: Directive says "retries 3 times", script retries 5 times.

**Fix**: Determine correct behavior, update both to match.

## Writing Testable Contracts

**Vague** (hard to test):
> "Handles errors appropriately"

**Specific** (testable):
> "Returns {error: string, code: number} when email is invalid"

**Vague** (hard to test):
> "Processes the data quickly"

**Specific** (testable):
> "Completes within 30 seconds for inputs under 1MB"

## Contract Checklist

When reviewing a directive, check:

- [ ] All inputs documented with types and requirements
- [ ] All outputs documented with structure
- [ ] All side effects documented
- [ ] All error conditions documented
- [ ] All dependencies documented
- [ ] Success criteria is testable
- [ ] Edge cases are specific
