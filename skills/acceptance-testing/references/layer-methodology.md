# Acceptance Testing — Layer Methodology Reference

This document provides detailed execution patterns for each testing layer. The main SKILL.md references this for specifics; read it before executing any layer.

---

## Layer 2: Backend Data Verification Patterns

### Schema Verification

Compare `mcp__convex__tables` output against the phase plan's expected schema:

1. **Table existence:** Every table mentioned in the phase plan's task outputs should exist in the deployment.
2. **Field types:** For each table, compare field names and types against the domain model (e.g., `convex/domain/influencer.ts`, `convex/schema.ts`).
3. **Index existence:** Check that indexes referenced in queries/mutations exist. Use the schema output to verify index definitions.

### Data Shape Queries

Use `mcp__convex__data` to read a page from each relevant table. For each row, check:

| Check | How | Example |
|-------|-----|---------|
| **Nullable fields are null, not fake defaults** | Scan for fields that should be null when source provides no data | `country` should be `null`, never `"Saudi Arabia"` as a guess |
| **Required fields are populated** | Every non-nullable field has a value | `platform`, `username`, `followers` must never be null |
| **Value ranges match domain rules** | Compare against domain constants | `followers >= 1000` (Nano floor), `sizeBucket` matches follower count |
| **Enum values are valid** | Compare against domain value objects | `status` must be one of the defined pipeline stages |
| **Referential integrity** | Cross-table references resolve | `discoveryRunId` on influencer points to an existing `discovery_runs` row |

### Data Quality One-Off Queries

Use `mcp__convex__runOneoffQuery` for aggregate checks:

```javascript
// Null audit: count of fake defaults in nullable fields
export default query({
  handler: async (ctx) => {
    const influencers = await ctx.db.query("influencers").collect();
    const fakeDefaults = influencers.filter(i =>
      i.country === "Saudi Arabia" || i.gender === "Other"
    );
    return { total: influencers.length, fakeDefaults: fakeDefaults.length };
  },
});

// Range validation: profiles outside configured follower band
export default query({
  handler: async (ctx) => {
    const runs = await ctx.db.query("discovery_runs").collect();
    for (const run of runs) {
      const profiles = await ctx.db
        .query("influencers")
        .withIndex("by_discovery_run", q => q.eq("discoveryRunId", run._id))
        .collect();
      const outOfRange = profiles.filter(p => {
        const followers = p.platformPresences?.[0]?.followers ?? 0;
        return followers < run.followerMin ||
          (run.followerMax !== null && followers > run.followerMax);
      });
      if (outOfRange.length > 0) {
        return { runId: run._id, outOfRange: outOfRange.length, total: profiles.length };
      }
    }
    return { allWithinRange: true };
  },
});

// Distribution check: size bucket breakdown
export default query({
  handler: async (ctx) => {
    const influencers = await ctx.db.query("influencers").collect();
    const buckets = {};
    for (const i of influencers) {
      const bucket = i.platformPresences?.[0]?.sizeBucket ?? "Unknown";
      buckets[bucket] = (buckets[bucket] || 0) + 1;
    }
    return buckets;
  },
});
```

---

## Layer 3: UI Interaction Patterns

### Mapping Acceptance Criteria to Playwright Actions

| AC Verb Pattern | Playwright Action | Verification |
|----------------|-------------------|--------------|
| "form presents fields for X" | `browser_snapshot` → check for input elements | Input refs visible in snapshot |
| "user selects from dropdown" | `browser_click` on trigger → `browser_click` on option | Snapshot shows selected value |
| "user enters text in field" | `browser_type` with ref and text | Snapshot shows entered value |
| "form validates X" | `browser_click` submit → `browser_snapshot` | Error message visible |
| "page displays list of X" | `browser_navigate` → `browser_snapshot` | List items visible with correct data |
| "user clicks button" | `browser_click` with ref | Page state changes (new snapshot) |
| "page shows loading state" | `browser_snapshot` immediately after action | Skeleton/spinner visible |
| "data persists after submission" | `browser_click` submit → `browser_navigate` away → `browser_navigate` back | Data still present |

### Edge Case Testing Checklist

For each form or interactive element, test:

1. **Empty required fields:** Submit with required fields blank. Expect validation error.
2. **Boundary values:** Use min/max values from domain rules (e.g., followerMin = 1000, the Nano floor).
3. **Arabic text:** Use actual domain values like niche names from `valueObjects.ts`. Example: `"الجمال"` (Beauty), `"الطبخ"` (Cooking).
4. **Special characters:** Hashtags with `#`, commas in multi-value fields, URLs in profile links.
5. **Max length inputs:** If character limits exist, test at and beyond the limit.
6. **Rapid interactions:** Double-click submit buttons, navigate away mid-submission.

### Evidence Collection

For every test action, capture evidence:
- **PASS:** `browser_snapshot` showing the expected state (accessibility tree proves element presence)
- **FAIL:** `browser_take_screenshot` for visual evidence + `browser_snapshot` for DOM state + `browser_console_messages` for JS errors

---

## Layer 4: Workflow Derivation

### How to Extract the Primary End-to-End Flow

1. Read the phase plan's **Story Summary** or **Acceptance Test Scenarios** section.
2. Identify the primary user journey — the one that touches the most stories in scope.
3. Order the steps chronologically as a user would experience them.

**Example for Phase 1 (Discovery Foundation):**
```
Step 1: Navigate to /discovery (US-001: see list of runs)
Step 2: Click "New Run" → navigate to /discovery/configure (US-001: start new run)
Step 3: Fill configuration form (US-004: configure parameters)
  - Select countries, niches, follower range, hashtags, profile limit
Step 4: Review confirmation → click "Start Discovery" (US-004: launch run)
Step 5: Verify run appears in list with "Running" status (US-001: run tracking)
Step 6: Wait for completion (poll status via Convex MCP)
Step 7: Verify run shows "Completed" status (US-001: status visibility)
Step 8: Verify profiles created in database (Convex MCP: data integrity)
Step 9: Navigate to run summary page (if implemented)
```

### Cross-Layer Verification Pattern

After each UI action that should modify backend state:

```
UI Action (Playwright) → Wait briefly → Backend Check (Convex MCP) → UI Refresh (Playwright) → Compare
```

Specifically:
1. Perform the action via `browser_click` or `browser_fill_form`
2. Wait 2-5 seconds for Convex real-time sync (`browser_wait_for` with time)
3. Query the relevant table via `mcp__convex__data` or `mcp__convex__runOneoffQuery`
4. Verify the data matches expectations (correct status, correct counts, correct field values)
5. Take a `browser_snapshot` to verify the UI reflects the backend state

---

## Layer 5: Severity Classification

### CRITICAL — Blocks User Workflow

The user cannot complete a core task. Examples:
- Form submission fails silently (no error, no data saved)
- Page crashes or shows blank white screen
- Navigation to a core route returns 404
- Data persists with corrupted values
- External API integration completely broken (all calls fail)
- Authentication blocks access to all pages

### IMPORTANT — Degrades Experience

The user can work around it, but the experience is notably broken. Examples:
- Validation missing on a field (accepts invalid data)
- Wrong error message displayed
- Loading state not shown (flash of empty content)
- Data displays but with wrong format (dates, numbers)
- CRUD operation works but UI doesn't update without refresh
- Accessibility issues (keyboard navigation broken, missing ARIA labels)

### MINOR — Cosmetic or Polish

No functional impact. Examples:
- Text alignment slightly off
- Inconsistent spacing between elements
- Placeholder text not matching design spec
- Color doesn't match brand guidelines exactly
- Animation missing or jittery
- Console warnings (not errors) in browser
