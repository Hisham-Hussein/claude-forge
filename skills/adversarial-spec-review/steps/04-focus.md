<step_4>
**Step 4: Generate Focus Areas per Reviewer**

**Read `templates/reviewer-task.md` now** — it contains the prompt template, dynamic fields, and focus area generation guidance.

For each reviewer, generate 3-7 specific QUESTIONS (not instructions) based on:
- The spec's section structure mapped to the reviewer's expertise
- The specific concerns that archetype is designed to catch
- The source files they'll be reading

Questions should be specific to THIS spec, not generic. Reference actual section numbers, field names, function names from the spec.

See templates/reviewer-task.md `<focus_area_generation>` for examples.

**Self-check before proceeding:** For each focus area question, verify: (a) it references a specific section number or field name from the spec, (b) it asks the reviewer to TRACE or VERIFY something concrete, not just "check if X is correct." Rewrite any question that fails this test.

**Round 2+ focus area rules:** In subsequent rounds, focus areas MUST narrow, not deepen. Generate questions ONLY from these three categories:
1. **Fix verification** — "Did the fix for [prior finding] resolve the concern? Did it introduce any inconsistency with [related section]?"
2. **Regression check** — "Is [section that was clean in Round N-1] still consistent after the fixes?"
3. **Fix-adjacent gaps** — "Did fixing [X] reveal a gap in [Y] that was hidden by the original error?"

Do NOT generate "go deeper" questions, "find what Round N missed" questions, or questions that expand scope beyond Round 1's coverage. Round 2+ is convergence, not discovery. If the spec was clean in an area during Round 1, it's still clean — don't re-investigate it with deeper scrutiny.
</step_4>

