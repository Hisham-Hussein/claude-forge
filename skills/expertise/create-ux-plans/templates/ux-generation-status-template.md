# UX Generation Status

> Pipeline state manifest for resume capability. Updated after each stage completes.

```yaml
pipeline_run: [YYYY-MM-DD]
platform: [detected platform]
constrained: [true/false]
constraint_manifest: .charter/UX-CONSTRAINTS.md
story_map: [path to story map]
scope: [MVP / slice name]
depth: [lean / full]
# lean: UX-COMPONENTS, UX-INTERACTIONS, UX-ACCESSIBILITY are "skipped" with reason "lean depth"
documents:
  UX-DESIGN-PLAN:
    status: pending
    # status values: pending | generating | verifying | verified | failed-verification | user-approved | skipped
    checks_passed: null
    checks_total: null
    user_approved: null
    verification_loop: 0
  UX-FLOWS:
    status: pending
    checks_passed: null
    checks_total: null
    user_approved: null
    verification_loop: 0
  UX-LAYOUTS:
    status: pending
    checks_passed: null
    checks_total: null
    user_approved: null
    verification_loop: 0
  UX-COMPONENTS:
    status: pending
    reason: null
    checks_passed: null
    checks_total: null
    verification_loop: 0
  UX-INTERACTIONS:
    status: pending
    reason: null
    checks_passed: null
    checks_total: null
    verification_loop: 0
  UX-ACCESSIBILITY:
    status: pending
    # may be set to "skipped" with reason during Stage 0 ("lean depth" or "platform handles a11y")
    reason: null
    checks_passed: null
    checks_total: null
    verification_loop: 0
```
