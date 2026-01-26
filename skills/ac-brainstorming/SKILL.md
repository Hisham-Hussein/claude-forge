---
name: ac-brainstorming
description: Use when reviewing or enhancing acceptance criteria for user stories. Applies systematic methodology to ensure comprehensive AC coverage across all 6 categories.
context: fork
agent: general-purpose
---

<objective>
Systematic methodology for brainstorming comprehensive acceptance criteria. Apply these techniques to review existing AC and identify gaps in coverage.
</objective>

<critical_principle>
**COMPREHENSIVE COVERAGE IS YOUR PRIMARY GOAL**

Your job is to ADD all acceptance criteria needed to achieve complete coverage of:
- All 6 categories (Functional, Business Rules, UI/UX, Error Handling, NFRs, Edge Cases)
- All SMART + 3C quality checks
- All negative scenarios (concurrency, authorization, timeouts, API failures, etc.)

**Add as MANY criteria as needed.** Do NOT limit yourself to 7 AC per story.

If a story ends up with more than 7 AC, simply FLAG it for splitting in your sign-off summary. A separate sub-agent handles the actual splitting — that is NOT your responsibility.

**Quality and coverage come first. Flagging for split comes after.**
</critical_principle>

<ten_questions>
Use these Ten Powerful Questions to discover missing AC for each user story:

| # | Question | Purpose |
|---|----------|---------|
| 1 | "What things should I account for?" | Surfaces obvious requirements |
| 2 | "If already implemented, what would I test?" | Shifts to testing mindset |
| 3 | "What happens when...?" | Explores specific behaviors |
| 4 | "What scenarios are relevant?" | Identifies coverage scope |
| 5 | "What could go wrong?" | Uncovers error cases |
| 6 | "Is that within scope?" | Boundaries the AC |
| 7 | "What haven't we thought about?" | Catches blind spots |
| 8 | "What would make this fail?" | Negative scenarios |
| 9 | "What are the boundaries?" | Edge case identification |
| 10 | "Who else is affected?" | Stakeholder/system impacts |
</ten_questions>

<starbursting>
Generate AC using the Starbursting (6W) method - ask questions across six dimensions:

| Dimension | Questions to Ask |
|-----------|------------------|
| **WHO** | Who initiates? Who is affected? Who approves? |
| **WHAT** | What inputs required? What outputs? What changes? |
| **WHEN** | When triggered? When should it NOT happen? Time constraints? |
| **WHERE** | Where does it appear? Where stored? Where are errors shown? |
| **WHY** | Why would user do this? Why might it fail? |
| **HOW** | How does user know it worked? How handle errors? How fast? |
</starbursting>

<six_categories>
For comprehensive coverage, verify AC exists for each of these 6 categories:

**1. Functional Behavior (Happy Path)**
What the system does when everything goes right.
```
- [ ] User can [action]
- [ ] Results display [expected output]
- [ ] Count/state updates correctly
```

**2. Business Rules & Constraints**
Policies, limits, and logic the system enforces.
```
- [ ] Only [role] can [action]
- [ ] Rate limit: max N per [time]
- [ ] [Field] must be validated against [source]
```

**3. User Interface & Experience**
How things appear and behave visually.
```
- [ ] Loading indicator displays during [action]
- [ ] Empty state shows [message]
- [ ] Error messages appear [location]
```

**4. Error Handling & Validation**
What happens when things go wrong.
```
- [ ] Invalid [input] shows [error message]
- [ ] Network timeout displays retry option
- [ ] Missing required field prevents submission
```

**5. Non-Functional Requirements**
Performance, security, accessibility constraints.
```
- [ ] [Action] completes within N seconds for 95% of requests
- [ ] API requires authentication
- [ ] All images have alt text
```

**6. Edge Cases & Boundaries**
Unusual but valid scenarios at the limits.
```
- [ ] Handles 0 results (empty state, not error)
- [ ] Maximum N characters in [field]
- [ ] Handles [edge value] gracefully
```
</six_categories>

<edge_case_identification>
**Boundary Value Analysis:**
For constrained inputs, test at critical points:
- Minimum valid value
- Maximum valid value
- Just below minimum (invalid)
- Just above maximum (invalid)

**Data Type Edge Cases:**

| Type | Consider |
|------|----------|
| Numbers | 0, 1, -1, max, min, decimals, very large |
| Strings | empty, null, whitespace, very long, special chars, unicode |
| Dates | today, past, future, leap year, timezone edge |
| Lists | empty, single item, max items, duplicates |
| Files | 0 bytes, max size, wrong format, corrupt |

**Negative Scenario Prompts:**
- What should NOT happen?
- What if invalid data entered?
- What if network fails mid-operation?
- What if user lacks permission?
- What if external API unavailable?
</edge_case_identification>

<quality_frameworks>
**SMART Criteria:**
Each AC must be:
- **S**pecific: Clear what must happen (not "fast" → "< 2 seconds")
- **M**easurable: Objectively verifiable
- **A**chievable: Technically feasible
- **R**elevant: Relates to this story
- **T**estable: Can write pass/fail test

**3C Rule:**
- **Clear**: Business AND technical team interpret same way
- **Concise**: No unnecessary detail
- **Checkable**: Binary pass/fail when tested

**AC Count Guideline (for flagging only):**
- <3 criteria: Likely missing coverage — apply brainstorming techniques
- 3-7 criteria: Typical for well-sized stories
- >7 criteria: FLAG for splitting in sign-off (but do NOT stop adding criteria)

**Important:** The 7 AC threshold is a FLAG, not a LIMIT. Add ALL criteria needed for comprehensive coverage. If count exceeds 7, note it in sign-off. Splitting is handled by a separate sub-agent.
</quality_frameworks>

<anti_patterns>
| Anti-Pattern | Fix |
|--------------|-----|
| Too vague ("should be fast") | Quantify ("< 2 seconds") |
| Too specific (implementation detail) | Describe behavior, not how |
| Untestable ("intuitive") | Observable outcome |
| Subjective ("good results") | Measurable criteria |
| Missing "so what" | Include user-visible outcome |
| Missing categories | Ensure all 6 categories considered |
| Stopped at 7 to avoid count | Add ALL needed criteria, then flag for split |
</anti_patterns>

<self_verification>
**MANDATORY: Before finalizing, verify your own work against these checks.**

**Step 1: Category Coverage Check**
For EACH story, verify you have criteria for:
- [ ] Functional Behavior (happy path)
- [ ] Business Rules & Constraints
- [ ] UI/UX (loading states, empty states, visual feedback)
- [ ] Error Handling & Validation
- [ ] Non-Functional Requirements (performance, security)
- [ ] Edge Cases & Boundaries

If any category is missing, GO BACK and add criteria for it.

**Step 2: Negative Scenario Check**
Verify you've addressed:
- [ ] What if user enters invalid data?
- [ ] What if network/API fails?
- [ ] What if user lacks permission? (authorization)
- [ ] What if another user modifies same data? (concurrency)
- [ ] What if operation times out? (with consequence)

**Step 3: Quality Check (SMART + 3C)**
For each criterion:
- [ ] Is it Specific? (no vague words like "correctly", "properly", "good")
- [ ] Is it Measurable/Testable? (can write pass/fail test)
- [ ] Is it Clear? (one interpretation only)
- [ ] Does it include the consequence? (not just "max 100 chars" but what happens at 101)

**Step 4: 5W1H Review**
| Check | Question |
|-------|----------|
| WHO | All user roles covered? |
| WHAT | Specified what happens AND what doesn't? |
| WHEN | Timing, sequencing, conditions covered? |
| WHERE | Context (page, state, platform) specified? |
| WHY | Each AC ties to user value? |
| HOW | Success measurement specified? |

**Step 5: Flag Stories for Splitting**
After completing all criteria, count AC per story:
- Stories with >7 AC → List in sign-off under "Stories flagged for splitting"
- Do NOT remove criteria to get below 7. Just flag.
</self_verification>

<success_criteria>
AC brainstorming is complete when:
- All 6 categories have criteria for EVERY story (100% coverage)
- Ten Questions applied to find gaps
- Negative scenarios covered (authorization, concurrency, timeouts, API failures)
- Edge cases identified using boundary analysis
- Each AC passes SMART + 3C validation (no vague language)
- Each boundary condition includes its consequence
- Self-verification checklist completed
- Stories with >7 AC flagged for splitting (but ALL criteria retained)
- Sign-off summary documents coverage statistics and flagged stories
</success_criteria>
