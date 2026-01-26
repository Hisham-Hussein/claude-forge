---
name: ac-brainstorming
description: Use when reviewing or enhancing acceptance criteria for user stories. Preloaded into sub-agents that iterate over existing AC to ensure comprehensive coverage.
---

<objective>
Systematic methodology for brainstorming comprehensive acceptance criteria. Apply these techniques to review existing AC and identify gaps in coverage.
</objective>

<ten_questions>
## Ten Powerful Questions

Use these to discover missing AC for each user story:

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
## Starbursting (6W Method)

Generate AC by asking questions across six dimensions:

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
## 6 AC Categories Framework

For comprehensive coverage, verify AC exists for each relevant category:

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
## Edge Case Identification

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
## Quality Frameworks

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

**Optimal Count:** 3-7 criteria per story
- <3 suggests missing coverage
- >7 suggests story needs splitting
</quality_frameworks>

<anti_patterns>
## Anti-Patterns to Avoid

| Anti-Pattern | Fix |
|--------------|-----|
| Too vague ("should be fast") | Quantify ("< 2 seconds") |
| Too specific (implementation detail) | Describe behavior, not how |
| Untestable ("intuitive") | Observable outcome |
| Subjective ("good results") | Measurable criteria |
| Missing "so what" | Include user-visible outcome |
| >7 criteria | Split the story |
</anti_patterns>

<completeness_verification>
## Completeness Verification (5W1H Review)

Before finalizing, verify coverage:

| Check | Question |
|-------|----------|
| WHO | All user roles covered? |
| WHAT | Specified what happens AND what doesn't? |
| WHEN | Timing, sequencing, conditions covered? |
| WHERE | Context (page, state, platform) specified? |
| WHY | Each AC ties to user value? |
| HOW | Success measurement specified? |

**Final Checklist:**
- [ ] Happy path AND error cases covered
- [ ] Edge cases identified using boundary analysis
- [ ] Each criterion passes SMART validation
- [ ] Count is 3-7 per story
- [ ] No ambiguous language remains
</completeness_verification>

<success_criteria>
AC brainstorming is complete when:
- All 6 categories considered for each story
- Ten Questions applied to find gaps
- Edge cases identified using boundary analysis
- Each AC passes SMART + 3C validation
- 3-7 criteria per story (or flagged for splitting)
- No vague or untestable criteria remain
</success_criteria>
