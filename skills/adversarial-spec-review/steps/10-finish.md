
**Step 10: Finish.** Delete `.review-state/` (`active.json` and every round folder), so the gates stop and no old gate file satisfies a later review's gates.

</process>

<success_criteria>
This workflow is complete when:
- [ ] Spec analyzed and domain dimensions identified
- [ ] Review team selected based on spec content (not defaults; Mode D: one fresh reviewer per round)
- [ ] All reviewers read real source files, not just the spec
- [ ] Each round synthesized with critical judgment (not rubber-stamped)
- [ ] User approved all fixes before they were applied (Mode D: the user chose Mode D)
- [ ] All fixes verified by orchestrator before committing (fix-to-finding, consistency scan, re-read)
- [ ] Final round: zero Critical/Major remain after synthesis
- [ ] Orchestrator confirmed the verdict with own judgment
- [ ] User received "implementation-ready" declaration
- [ ] `.review-state/` deleted
</success_criteria>
