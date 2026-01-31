---
name: fix-drifts
description: Use when fixing contract drifts between directives and scripts, correcting misalignments after running contract verification, or resolving detected drift issues. Triggers include "fix drift", "correct drift", "resolve misalignment", "fix contract", or when drift has been detected by contract-driven-integration skill.
---

<objective>
Automatically correct drifts detected by the contract-driven-integration skill. Completes the detect-fix loop by analyzing drift direction and applying appropriate corrections.
</objective>

<essential_principles>

<fix_direction>
Drift fixes go in one of two directions:

| Drift Type | Direction | What to Update |
|------------|-----------|----------------|
| **Script Drift** | Script does more than directive documents | Update **directive** to document the behavior |
| **Directive Drift** | Directive promises more than script delivers | Update **script** to implement the promise |

**Default recommendations:**
- Script drift (extra fields, undocumented behavior) → Fix directive (document it)
- Directive drift (missing implementation) → Fix script (implement it)

User always chooses final direction.
</fix_direction>

<assisted_not_blind>
This is assisted correction, not blind automation:
- Always show what was detected
- Always recommend a fix direction with reasoning
- Always ask user to confirm before applying
- Never delete code or documentation without explicit approval
</assisted_not_blind>

<verification_loop>
After each fix:
1. Re-run drift detection on the affected directive
2. Confirm drift is resolved
3. Update mapping file status to "aligned"
</verification_loop>

</essential_principles>

<intake>
What would you like to do?

1. **Detect and propose fixes** - Run drift detection, analyze results, propose corrections
2. **Fix directive** - Update directive to match what script actually does
3. **Fix script** - Update script to match what directive promises
4. **Re-verify** - Check if previous fixes resolved the drift

**Provide the directive path with your selection.**
</intake>

<routing>
| Response | Workflow | Purpose |
|----------|----------|---------|
| 1, "detect", "propose", "check", "analyze" | workflows/detect-and-propose.md | Full analysis with recommendations |
| 2, "fix directive", "update directive", "document" | workflows/fix-directive.md | Add missing documentation |
| 3, "fix script", "update script", "implement" | workflows/fix-script.md | Add missing implementation |
| 4, "verify", "re-check", "confirm" | Re-run contract-driven-integration detect-drift | Verify alignment |

**After selecting a workflow, read it and follow exactly.**
</routing>

<quick_start>
Most common flow:

1. User runs `/fix-drift path/to/directive`
2. Skill invokes contract-driven-integration to detect drift
3. Skill analyzes each drift item and proposes fix direction
4. User approves fixes
5. Skill applies corrections and verifies alignment
</quick_start>

<success_criteria>
Drift correction complete when:
- [ ] All drift items addressed (fixed or explicitly deferred)
- [ ] Verification shows no remaining drift
- [ ] Mapping file updated to "aligned" status
</success_criteria>
