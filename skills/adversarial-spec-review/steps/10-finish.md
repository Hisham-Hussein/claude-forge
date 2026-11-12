
**Step 10: Finish.** Delete your session folder `<S>` = `.review-state/${CLAUDE_SESSION_ID}/` (`active.json` and every round folder; never another session's folder), so the gates stop and no old gate file satisfies a later review's gates.

</process>

<success_criteria>
This workflow is complete when:
- [ ] Spec analyzed and domain dimensions identified
- [ ] Review team selected based on spec content (not defaults)
- [ ] All reviewers read real source files, not just the spec
- [ ] Each round synthesized with critical judgment (not rubber-stamped)
- [ ] User approved all fixes before they were applied
- [ ] All fixes verified by orchestrator before committing (fix-to-finding, consistency scan, re-read)
- [ ] Final round: zero Critical/Major remain after synthesis
- [ ] Orchestrator confirmed the verdict with own judgment
- [ ] User received "implementation-ready" declaration
- [ ] session folder `<S>` deleted
</success_criteria>
