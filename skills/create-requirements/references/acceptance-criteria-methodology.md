# Deep Dive: Acceptance Criteria Methodology

## Strategic Summary

Acceptance criteria (AC) are the conditions that define when a user story is "done" — they transform vague requirements into testable, verifiable specifications. While the existing user-story-methodology.md covers AC formats (Given/When/Then vs Checklist), this research fills critical gaps: **how to systematically brainstorm comprehensive AC**, **how to evaluate AC quality**, **how to identify edge cases and negative scenarios**, and **how to avoid common anti-patterns**. For our create-requirements skill, this methodology enables a specialized sub-agent to generate thorough, high-quality acceptance criteria that reduce rework and prevent missed requirements.

## Key Questions

- How do you systematically brainstorm acceptance criteria to ensure comprehensive coverage?
- What quality frameworks exist to evaluate if AC is well-written?
- How do you identify edge cases, boundary conditions, and negative scenarios?
- What are the common anti-patterns to avoid when writing AC?
- How do you verify AC completeness — when do you have "enough"?
- What categories of AC should be considered for each user story?

---

## Overview

Acceptance criteria serve as the "Confirmation" in the 3 C's of user stories (Card, Conversation, Confirmation). They're not just nice-to-have documentation — they're the contract between product owner and development team that defines success. Well-written AC reduces development cycles by 25-30% by eliminating ambiguity and rework.

The challenge isn't knowing that AC is important — it's knowing **how to generate comprehensive AC systematically**. Most teams write AC ad-hoc, missing edge cases that become bugs in production. This research provides frameworks, heuristics, and questions that transform AC creation from an art into a repeatable process.

For an AI-powered requirements skill, these techniques enable a sub-agent to brainstorm AC methodically, ensuring coverage across functional behavior, business rules, error handling, and edge cases.

---

## How It Works

### The AC Generation Process

```
User Story → Brainstorm Questions → Generate AC → Validate Quality → Verify Completeness
                    ↓                    ↓              ↓                  ↓
              Starbursting          Categories      SMART/3C           5W1H Review
              10 Questions          Coverage        Validation         Stakeholder Check
```

### Step 1: Understand the Story Context

Before generating AC, fully understand:
- **Who** is the user? (role, permissions, context)
- **What** are they trying to accomplish? (goal)
- **Why** does this matter? (business value)
- **Where** does this happen? (context, platform, entry points)

### Step 2: Apply Systematic Brainstorming

Use structured techniques (detailed below) to generate candidate AC across all relevant categories.

### Step 3: Format Appropriately

Choose format based on complexity:
- **Checklist format**: Simple features, NFRs, CRUD operations
- **Given/When/Then**: Complex scenarios, user interactions, test automation

### Step 4: Validate and Refine

Apply quality frameworks (SMART, 3C) to each criterion. Remove or rewrite those that fail.

### Step 5: Verify Completeness

Use the 5W1H review method and stakeholder consensus to confirm coverage.

---

## Brainstorming Techniques

### Technique 1: The Ten Powerful Questions

Use these questions to systematically discover AC for any user story:

| # | Question | Purpose |
|---|----------|---------|
| 1 | "If I deliver this user story, what things should I account for?" | Surfaces obvious requirements |
| 2 | "If this story has already been implemented, what would I try out?" | Shifts perspective to testing mindset |
| 3 | "What happens when...?" | Explores specific behaviors |
| 4 | "What scenarios are relevant?" | Identifies coverage scope |
| 5 | "What could go wrong?" | Uncovers error cases |
| 6 | "Is that within scope?" (follow-up) | Boundaries the AC appropriately |
| 7 | "What have we not thought about yet?" | Catches blind spots |
| 8 | "What would make this fail?" | Negative scenario discovery |
| 9 | "What are the boundaries?" | Edge case identification |
| 10 | "Who else is affected?" | Stakeholder/system impacts |

### Technique 2: Starbursting (6W Method)

Generate questions across six dimensions using a star diagram:

```
                    WHO?
                     |
        WHY? ────────●──────── WHAT?
                    /|\
                   / | \
              HOW?  WHEN?  WHERE?
```

**For each dimension, ask:**

| Dimension | Example Questions |
|-----------|-------------------|
| **WHO** | Who initiates this? Who is affected? Who needs to approve? |
| **WHAT** | What inputs are required? What outputs expected? What changes? |
| **WHEN** | When can this be triggered? When should it NOT happen? Time constraints? |
| **WHERE** | Where does this appear? Where is data stored? Where are errors shown? |
| **WHY** | Why would a user do this? Why might it fail? Why is the boundary here? |
| **HOW** | How does the user know it worked? How do we handle errors? How fast? |

### Technique 3: "Remember the Future"

Position yourself as if the feature is already live:
- "A user just used this feature. What did they experience?"
- "A bug was reported. What went wrong?"
- "Support received a call. What was confusing?"

### Technique 4: Multi-Stakeholder Workshop

Involve different perspectives (developer, tester, designer, end-user) to surface different types of AC:
- **Developer**: Technical constraints, performance, error handling
- **Tester**: Edge cases, boundaries, negative scenarios
- **Designer**: UX expectations, accessibility, error states
- **End-user**: Real-world usage patterns, expectations

---

## AC Categories Framework

For comprehensive coverage, consider AC across these six categories:

### Category 1: Functional Behavior (Happy Path)
What the system does when everything goes right.

```markdown
- [ ] User can select a niche from the dropdown
- [ ] Results display matching influencers
- [ ] Count updates to show total matches
```

### Category 2: Business Rules & Constraints
Policies, limits, and logic the system must enforce.

```markdown
- [ ] Only Premium users can export more than 50 profiles
- [ ] Rate limit: max 10 searches per minute
- [ ] Follower count must be validated against live data
```

### Category 3: User Interface & Experience
How things appear and behave visually.

```markdown
- [ ] Loading indicator displays during search
- [ ] Empty state shows "No influencers found" message
- [ ] Error messages appear inline below the failed field
```

### Category 4: Error Handling & Validation
What happens when things go wrong.

```markdown
- [ ] Invalid email format shows "Please enter a valid email"
- [ ] Network timeout displays retry option
- [ ] Missing required field prevents form submission
```

### Category 5: Non-Functional Requirements
Performance, security, accessibility constraints.

```markdown
- [ ] Search results return within 2 seconds for 95% of queries
- [ ] API requires authentication token
- [ ] All images have alt text for screen readers
```

### Category 6: Edge Cases & Boundaries
Unusual but valid scenarios at the limits.

```markdown
- [ ] Search with 0 results shows empty state (not error)
- [ ] Maximum 1000 characters in notes field
- [ ] Handles influencer with 0 followers (new account)
```

---

## Edge Case & Negative Scenario Identification

### Boundary Value Analysis

For any constrained input, test at these critical points:

```
Invalid ← | MIN | ← Valid Range → | MAX | → Invalid
    ↓      ↓                        ↓      ↓
   -1      0                       100   101
```

**Test these values:**
- Minimum valid value
- Maximum valid value
- Just below minimum (invalid)
- Just above maximum (invalid)
- Typical middle value

### Data Type Edge Cases

| Data Type | Edge Cases to Consider |
|-----------|------------------------|
| **Numbers** | 0, 1, -1, max, max+1, min, min-1, decimals, very large |
| **Strings** | empty (""), null, whitespace only, very long, special chars, unicode, HTML/script injection |
| **Dates** | today, past, future, leap year, timezone edge, DST transition |
| **Lists** | empty, single item, max items, duplicates |
| **Files** | 0 bytes, max size, wrong format, corrupt, special filename chars |
| **Booleans** | true, false, null/undefined |

### Equivalence Partitioning

Group inputs into classes that should behave identically:

```
Example: Age field (valid: 18-65)

Class 1: Invalid (< 18)     → Test with: 17, 0, -1
Class 2: Valid (18-65)      → Test with: 18, 40, 65
Class 3: Invalid (> 65)     → Test with: 66, 100, 999
Class 4: Invalid (non-numeric) → Test with: "abc", "", null
```

### Negative Scenario Prompts

Ask these questions to discover negative AC:

1. "What should NOT happen?"
2. "What if the user enters invalid data?"
3. "What if the network fails mid-operation?"
4. "What if another user modifies the same data?"
5. "What if required data is missing?"
6. "What if the user doesn't have permission?"
7. "What if external API is unavailable?"
8. "What if the operation times out?"

---

## Quality Frameworks

### SMART Criteria for AC

Each acceptance criterion should be:

| Criterion | Question | Example |
|-----------|----------|---------|
| **S**pecific | Is it clear what must happen? | ❌ "Fast loading" ✅ "Page loads in < 2 seconds" |
| **M**easurable | Can we objectively verify it? | ❌ "User-friendly" ✅ "Error messages include resolution steps" |
| **A**chievable | Is it technically feasible? | ❌ "100% uptime" ✅ "99.9% uptime during business hours" |
| **R**elevant | Does it relate to this story? | ❌ "Database is normalized" ✅ "Search returns relevant results" |
| **T**estable | Can we write a pass/fail test? | ❌ "Works properly" ✅ "Invalid email shows error message" |

### 3C Rule

Every criterion must be:

| Check | Meaning | Validation Question |
|-------|---------|---------------------|
| **Clear** | Understandable by business AND technical team | "Would a developer and product owner interpret this the same way?" |
| **Concise** | Brief, no unnecessary detail | "Can this be stated in fewer words without losing meaning?" |
| **Checkable** | Binary pass/fail when tested | "Can we definitively say 'yes, this is met' or 'no, this is not'?" |

### AC Quality Checklist

Before finalizing AC, verify:

- [ ] Each criterion is testable (pass/fail possible)
- [ ] No implementation details specified (says "what" not "how")
- [ ] Written from user perspective where applicable
- [ ] Covers happy path AND error cases
- [ ] Includes relevant edge cases
- [ ] Performance criteria are quantified
- [ ] No ambiguous terms (fast, good, easy, etc.)
- [ ] 3-7 criteria total (not too many, not too few)

---

## Anti-Patterns to Avoid

### Content Anti-Patterns

| Anti-Pattern | Example | Fix |
|--------------|---------|-----|
| **Too Vague** | "System should be fast" | "Response time < 2 seconds for 95% of requests" |
| **Too Specific** | "Use MySQL query with JOIN on user_id" | "User data is retrieved correctly" |
| **Implementation Coupled** | "Implemented using React hooks" | "State updates reflect in UI without page refresh" |
| **Untestable** | "The interface should be intuitive" | "New users complete registration in < 3 minutes without help" |
| **Missing 'So What'** | "Field accepts 100 characters" | "Field accepts up to 100 characters; overflow shows warning" |
| **Subjective** | "Results should be good" | "Results sorted by relevance score (engagement rate * recency)" |

### Process Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Too Many AC** | >7 criteria suggests story is too large | Split the user story |
| **Too Few AC** | <3 criteria suggests missing coverage | Apply brainstorming techniques |
| **Missing AC** | No criteria at all | Never accept story without AC |
| **Written in Isolation** | BA writes alone, team confused | Collaborative refinement sessions |
| **Changed Mid-Sprint** | Moving target for developers | Freeze AC once sprint starts |
| **Copy-Paste AC** | Generic criteria not specific to story | Tailor each AC to the specific story |

### Optimal AC Count

Research suggests:
- **3-5 criteria**: Typical well-sized story
- **6-7 criteria**: Upper limit before considering split
- **>7 criteria**: Strong signal to split the story

---

## Completeness Verification

### The 5W1H Review

Review each user story's AC by asking:

| Dimension | Verification Question |
|-----------|----------------------|
| **WHO** | Have we covered all user roles that interact with this? |
| **WHAT** | Have we specified what happens (and what doesn't)? |
| **WHEN** | Have we covered timing, sequencing, conditions? |
| **WHERE** | Have we specified context (page, state, platform)? |
| **WHY** | Does each AC tie back to user value? |
| **HOW** | Have we specified how success is measured? |

### Definition of Done vs Acceptance Criteria

Understand the distinction:

| Aspect | Definition of Done (DoD) | Acceptance Criteria (AC) |
|--------|--------------------------|--------------------------|
| **Scope** | Universal to all stories | Specific to each story |
| **Content** | Quality standards (tested, reviewed, documented) | Functional requirements |
| **Example** | "Code reviewed by peer" | "User can filter by niche" |

**Both must be satisfied** for a story to be complete.

### Final Completeness Checklist

Before marking AC as complete:

- [ ] Stakeholder consensus reached (PO, dev, QA reviewed)
- [ ] All 6 AC categories considered (not all needed, but all considered)
- [ ] Edge cases identified using boundary analysis
- [ ] Negative scenarios included
- [ ] Each criterion passes SMART validation
- [ ] Count is 3-7 (or story should be split)
- [ ] No ambiguous or subjective language remains

---

## Patterns & Best Practices

### 1. Start with the Happy Path, Then Expand
Write the main success scenario first, then ask "what could go wrong?" to generate error and edge case AC.

### 2. Use Templates for Consistency
Standardize format across the team:
```markdown
**Acceptance Criteria:**
- [ ] [Action/State] results in [Observable Outcome]
- [ ] When [Condition], then [Expected Behavior]
- [ ] [Metric] must be [Quantified Value]
```

### 3. Involve QA Early
Testers think in edge cases naturally. Include them in AC brainstorming.

### 4. Time-Box AC Sessions
15-20 minutes per story is sufficient. More time often indicates story needs splitting.

### 5. Use "Given" to Establish Context
Even in checklist format, specify preconditions:
```markdown
- [ ] When user is logged in, dashboard shows personalized metrics
- [ ] When user is guest, dashboard shows generic content
```

### 6. Make Performance Criteria Specific
```markdown
❌ "Search should be fast"
✅ "Search returns results in < 2 seconds for 95th percentile"
✅ "Page load time < 3 seconds on 3G connection"
```

### 7. Include Error Message Content
```markdown
❌ "Show error for invalid email"
✅ "Invalid email shows: 'Please enter a valid email address (e.g., name@example.com)'"
```

---

## Limitations & Edge Cases

### When Techniques Don't Apply

- **Highly technical stories**: May need implementation-aware AC written by developers
- **Research spikes**: May have time-box as only AC ("Investigation complete within 4 hours")
- **Bug fixes**: AC may simply be "Regression test passes" plus specific fix verification
- **NFR stories**: May require specialized metrics and monitoring AC

### Format Limitations

**Checklist format** struggles with:
- Complex conditional logic (use Given/When/Then)
- Multi-step workflows (consider scenario format)

**Given/When/Then** struggles with:
- Simple boolean conditions (overkill, use checklist)
- Non-functional requirements (awkward fit)

---

## Key Takeaways

1. **Systematic brainstorming beats ad-hoc listing.** Use the Ten Questions, Starbursting, and category coverage to ensure completeness.

2. **Six categories ensure coverage.** Consider functional, business rules, UI/UX, error handling, NFRs, and edge cases for every story.

3. **SMART + 3C = Quality AC.** Each criterion should be Specific, Measurable, Achievable, Relevant, Testable AND Clear, Concise, Checkable.

4. **3-7 criteria is the sweet spot.** More suggests story is too large; fewer suggests missing coverage.

5. **Edge cases follow patterns.** Use boundary value analysis and equivalence partitioning to systematically find them.

6. **Anti-patterns kill quality.** Vague, untestable, implementation-coupled, or too numerous AC cause rework.

7. **Verify with 5W1H review.** Check coverage across Who, What, When, Where, Why, How before finalizing.

---

## Remaining Unknowns

- [ ] Optimal balance between AC detail and story conversation
- [ ] How AI-generated AC should be validated by human teams
- [ ] Best practices for AC in distributed/async teams without real-time conversation
- [ ] Metrics for measuring AC quality over time (defect correlation)

---

## Implementation Context

<claude_context>
<application>
- when_to_use: After writing user story statement; during backlog refinement; when story moves to sprint
- when_not_to_use: Before story is understood; for epics (too high level); for technical tasks without user value
- prerequisites: User story with clear role, goal, and benefit; understanding of system context
</application>
<technical>
- formats: Checklist (simple), Given/When/Then (complex/BDD)
- ideal_count: 3-7 criteria per story
- quality_frameworks: SMART, 3C
- brainstorming: Ten Questions, Starbursting (6W), Category Coverage
</technical>
<integration>
- works_with: User stories, BDD/Cucumber, test case generation, QA processes
- complements: Definition of Done (universal standards), INVEST criteria (story quality)
- feeds_into: Test cases, sprint planning estimation, demo acceptance
</integration>
<subagent_application>
- purpose: Spawn after user story creation to brainstorm comprehensive AC
- approach: Apply Ten Questions + Category Coverage + Edge Case Analysis
- output: Validated AC list with SMART/3C checks
- guardrails: Flag if >7 criteria (story may need split), require at least 3 criteria
</subagent_application>
</claude_context>

---

## Sources

- [Ten Powerful Questions for Discovering Acceptance Criteria - Inside Product](https://insideproduct.co/questionsforacceptancecriteria/)
- [Starbursting Brainstorming - Miro](https://miro.com/brainstorming/what-is-starbursting-brainstorming/)
- [Acceptance Criteria Explained - Atlassian](https://www.atlassian.com/work-management/project-management/acceptance-criteria)
- [Acceptance Criteria: Purposes, Formats, Best Practices - AltexSoft](https://www.altexsoft.com/blog/acceptance-criteria-purposes-formats-and-best-practices/)
- [What is Acceptance Criteria - ProductPlan](https://www.productplan.com/glossary/acceptance-criteria/)
- [Edge Case Testing Explained - Virtuoso QA](https://www.virtuosoqa.com/post/edge-case-testing)
- [What Are Common Mistakes Writing AC - LinkedIn](https://www.linkedin.com/advice/3/what-most-common-mistakes-when-writing-acceptance)
- [Good and Bad AC for Complex Systems - LinkedIn](https://www.linkedin.com/advice/1/what-some-examples-good-bad-acceptance-criteria)
- [Acceptance Criteria Checklist: 7 Steps - ITX Corp](https://itx.com/software-quality/acceptance-criteria-checklist-7-easy-steps-to-better-quality/)
- [Definition of Done vs Acceptance Criteria - Visual Paradigm](https://www.visual-paradigm.com/scrum/definition-of-done-vs-acceptance-criteria/)
- [Agile Acceptance Criteria Complete Guide - 6Sigma](https://www.6sigma.us/six-sigma-in-focus/agile-acceptance-criteria/)
- [How to Make AC Testable and Measurable - LinkedIn](https://www.linkedin.com/advice/1/how-can-you-make-acceptance-criteria-testable-pquoe)
- [27 Product Backlog Anti-Patterns - Age of Product](https://age-of-product.com/28-product-backlog-anti-patterns/)
- [Given-When-Then - Martin Fowler](https://martinfowler.com/bliki/GivenWhenThen.html)
- [BDD Best Practices - Platform Dev Playbook](https://playbook.platformdev.amdigital.co.uk/Ways-of-Working/Toolkit/Test-Engineering/Best-Practices/BDD-best-practices-for-writing-test-scenarios/)
- [Acceptance and Evaluation Criteria - BABOK Guide](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/10-techniques/10-1-acceptance-and-evaluation-criteria/)
