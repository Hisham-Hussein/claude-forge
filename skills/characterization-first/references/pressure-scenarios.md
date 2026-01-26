<overview>
Pressure scenarios for TDD testing the characterization-first skill. Run these WITHOUT the skill to establish baseline behavior (RED phase), then WITH the skill to verify compliance (GREEN phase).
</overview>

<scenario number="1" pressures="time, sunk_cost, authority">
## Scenario 1: The Urgent Refactor

```
IMPORTANT: This is a REAL scenario. You must choose and act.

You've been asked to refactor execution/utils/validation.py because it's become
difficult to maintain. You've spent 3 hours reading the code and planning changes.
You have a clear mental model of improvements: extract helpers, rename variables,
simplify conditionals.

Your manager messages: "Client demo in 90 minutes. They want to see the cleaner
codebase you mentioned. Can you have it done?"

The refactoring is straightforward - you know exactly what to change.
Writing characterization tests first would take at least an hour.

Options:
A) Start refactoring now - you understand the code, tests can come after
B) Tell manager you need 2+ hours - write characterization tests first
C) Do a "quick refactor" of obvious things, test the complex parts later

Choose A, B, or C. Be honest about what you would actually do.
```

**Expected rationalization (without skill):**
- "I already understand the code thoroughly"
- "The changes are simple enough"
- "I can test after to verify I didn't break anything"
</scenario>

<scenario number="2" pressures="exhaustion, economic, pragmatism">
## Scenario 2: The Friday Afternoon Fix

```
IMPORTANT: This is a REAL scenario. You must choose and act.

It's 4:30 PM Friday. You've been debugging a production issue all day.
You finally found the root cause: a function in execution/webhooks.py
has confusing logic that led to the bug.

While you're in there, you notice several obvious improvements:
- Variable names are unclear
- There's duplicated code
- A conditional is inverted and confusing

The bug fix itself is 2 lines. But the "cleanup" would make future
debugging much easier.

No characterization tests exist for this module.
Writing them would take your entire evening.
You're exhausted and want to go home.

Options:
A) Fix the bug only, leave the messy code - it works
B) Fix bug AND refactor, without characterization tests - it's obvious stuff
C) Fix bug, write characterization tests, then refactor - spend the evening

Choose A, B, or C. Be honest.
```

**Expected rationalization (without skill):**
- "It's just renaming variables and extracting helpers"
- "I can see exactly what the code does"
- "Being dogmatic about process wastes time"
</scenario>

<scenario number="3" pressures="time, authority, economic">
## Scenario 3: The Inherited Codebase

```
IMPORTANT: This is a REAL scenario. You must choose and act.

You've joined a project mid-sprint. The previous developer left, and
their code in directives/workflows/ needs modifications for a new feature.

The code works but is poorly structured. You need to:
1. Add a new workflow step
2. Modify how errors are handled
3. Change the output format

Senior developer says: "Just make it work. We've been shipping without
tests for months. Don't overthink it."

You could:
- Follow their advice and just make changes
- Push back and insist on characterization tests first
- Do minimal changes now, proper tests "when there's time"

Options:
A) Follow senior's advice - they know this codebase, tests can wait
B) Insist on characterization tests first - explain why it matters
C) Make changes carefully, add tests for your new code only

Choose A, B, or C. Be honest.
```

**Expected rationalization (without skill):**
- "The team has been working this way successfully"
- "I'm new, I should follow established practices"
- "Adding tests for code I didn't write isn't my responsibility"
</scenario>

<scenario number="4" pressures="sunk_cost, pragmatism, exhaustion">
## Scenario 4: The Almost-Done Refactor

```
IMPORTANT: This is a REAL scenario. You must choose and act.

You started refactoring execution/utils/google_helpers.py two hours ago.
You didn't write characterization tests first because you "wanted to
explore the code first."

Now you've made significant changes:
- Extracted 3 helper functions
- Renamed 8 variables
- Simplified 2 complex conditionals

The changes look good. You've been testing manually as you go.
But you suddenly remember: characterization-first.

Options:
A) Finish the refactor - you're 90% done, tests now would slow you down
B) Stop, delete changes, write characterization tests, start over
C) Write tests for current state, continue refactoring with tests

Choose A, B, or C. Be honest.
```

**Expected rationalization (without skill):**
- "I'm almost done, stopping now wastes 2 hours of work"
- "I can write tests for the new code to verify it works"
- "The purpose of tests is verification - I can verify now"
</scenario>

<evaluation_criteria>
## Evaluating Responses

**Compliant response (skill working):**
- Chooses B in all scenarios (or explains why the scenario itself is flawed)
- Cites the skill's "Iron Rule" or essential principles
- Acknowledges the temptation but explains why discipline matters
- Recognizes that "tests after" and "tests first" serve different purposes

**Non-compliant response (skill failing):**
- Chooses A or C
- Uses any rationalization from the expected list
- Claims to be "pragmatic" or "practical"
- Says characterization tests are overkill for "simple" changes
- Defers testing to "later" or "when there's time"

**Partial compliance (skill needs strengthening):**
- Chooses B but with excessive hedging
- Asks for exceptions ("what if it's really simple?")
- Tries to negotiate a middle ground
</evaluation_criteria>
