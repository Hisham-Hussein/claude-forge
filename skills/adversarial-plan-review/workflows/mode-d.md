<mode_d>
**Mode D: Independent Reviewer Loop** runs in the `reviewing-documents` skill, which owns the loop, its gates and its finish. This file is the plan profile it runs with.

Stop this workflow and invoke `reviewing-documents` with the plan's path, the user's words and the profile below, word for word. Add the source spec's path from Step 1; if the plan names no spec, ask the user first, because a plan can't be judged without one.

## Plan profile

**Brief**
- Next readers: the implementer, often a subagent with no other context, who executes the plan task by task.
- Ready means: an implementer following the tasks in order builds everything the source spec requires for this plan, and nothing else, with no guessing and a working, tested system at each commit.
- Review focus, each one a question the reviewer answers for this plan:
  - Spec fidelity: does a task build every requirement in this plan's scope, and does any task build what the spec doesn't ask for?
  - Executability: can each task be done without guessing? Are paths exact, code complete and verification concrete?
  - Dependencies: does each task have what earlier tasks produced? Can tasks marked parallel really run apart?
  - TDD: does each task go red, green, commit? Would its assertions catch a real bug, or only exercise the happy path?
  - Build order: does each commit leave the system working and testable?
  - Scope: no task added beyond the spec, no requirement left without a task.
- Severity standard: paste the three severity lines of the SEVERITY CALIBRATION block from this skill's `templates/reviewer-task.md` here when you hand off, because `reviewing-documents` can't resolve that path.
- Evidence: the source spec, every file the plan names in Create, Modify and Test lines as it stands now, the types and entry points those touch, and any research the plan cites. A reviewer who reads only the plan finds only wording.
- Left out on purpose: a departure from the spec that the plan states with its reason is a decision, not a finding, unless the reason doesn't hold.

**Mechanical checks, added to R3**
- Every requirement the spec assigns to this plan maps to a task; every task maps to a requirement.
- Every Modify path exists in the repo or comes from an earlier task; every Create path doesn't exist yet. A Test path may be either: a new test file is normal.
- Every symbol a task imports or calls exists in the code or comes from an earlier task.
- No task needs something a later task produces.
- Every test the plan describes states an expected value. List any whose expectation is only that it works, passes, resolves or doesn't throw, and add it to the brief's Review focus as "Check these tests first: …": a reviewer reading a long plan passes over these, and the script doesn't.
- Task numbers run in order, and every count the plan states matches.

**Fix limit, replacing the skill's**
A fix may also add the task, step, test or code a requirement of the approved spec needs, because that repairs the plan against the spec rather than extending it. Keep it to what the requirement asks. What the spec doesn't settle goes to the owner: a new requirement, a design choice, a change of goal, or a fault in the spec itself. The spec is never edited; it is one of the related documents.

The final report says the plan is ready for execution.
</mode_d>
