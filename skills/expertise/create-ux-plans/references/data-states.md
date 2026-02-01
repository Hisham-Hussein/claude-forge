<overview>
Decision rules, pattern inventories, and microcopy guidance for specifying loading, empty, error, success, and partial data states in UX plans. Every data-dependent component must define all applicable states; components with only default-state specs are incomplete.
</overview>

<loading_indicators>

## Loading Indicator Decision Matrix

| Wait Duration | Pattern | Notes |
|---|---|---|
| < 1 second | **No indicator** | Any animation will flash and feel jarring |
| 1-2 seconds | **Skeleton screen** (preferred) or subtle spinner | Render after ~300ms delay to prevent skeleton flash |
| 2-10 seconds | **Skeleton screen** or **spinner** | Skeleton for content areas; spinner for small contained components |
| 10+ seconds | **Progress bar** (determinate) | Must show estimated progress; indeterminate loses trust beyond 10s |
| File upload/download/conversion | **Progress bar** (determinate) | Never skeleton screens for file operations |

## Pattern Selection Rules

### Skeleton Screens
**Use when**: Loading full pages or large content sections; layout is predictable and consistent (cards, lists, grids, tables); content loads progressively.
**Avoid when**: Loading single small components; layout is unpredictable; load time < 1 second; process is not a page load (file ops, background tasks).
**Key rule**: Skeletons must mirror actual content layout. Progressive reveal preferred over all-at-once replacement. Render only after ~300ms threshold.

### Spinners
**Use when**: Loading a small contained component (table row, dropdown options); component has no predictable layout to skeleton; brief transitions (2-5s).
**Avoid when**: Full page loads; long waits (>10s); video loading.

### Progress Bars
**Use when**: Wait > 10 seconds; progress is deterministic; file operations; multi-step wizards.
**Avoid when**: Progress cannot be accurately estimated; load time < 10 seconds.

### Placeholder Content
**Use when**: Showing sample/dummy data to preview loaded state; first-use scenarios.
**Avoid when**: Placeholder could be confused with real content.

</loading_indicators>

<loading_anti_patterns>

## Loading Anti-Patterns

1. **Skeleton flash** -- Showing skeleton for <300ms before content appears
2. **Layout mismatch** -- Skeleton bones that don't match actual content layout
3. **All-or-nothing reveal** -- Replacing entire skeleton at once instead of progressively
4. **Spinner for page loads** -- Full-screen spinner with no layout preview
5. **Fake progress bars** -- Progress bar that doesn't reflect actual progress
6. **Missing loading state** -- Content area goes blank during fetch

</loading_anti_patterns>

<empty_states>

## Empty State Taxonomy

| Type | Trigger | Goal | Content Strategy |
|---|---|---|---|
| **First-use** | Never used feature | Educate + activate | Explain purpose, show benefit, single CTA to create first content |
| **No data** | System has no content | Guide to action | Explain why empty, suggest what to do, provide CTA |
| **No results** | Search/filter returned nothing | Help recover | Suggest alternatives, show related content, broaden search |
| **User-cleared** | User completed/deleted all | Celebrate + guide | Acknowledge completion, suggest next action |
| **Error** | Data failed to load | Explain + recover | Clear error description, recovery action, no raw codes |

## Empty State Content Hierarchy

1. **Illustration/Icon** (optional) -- Sets tone, draws attention
2. **Headline** -- States what's happening ("No projects yet")
3. **Body text** -- Explains why + what to do next (1-2 sentences)
4. **Primary CTA** -- Single action to resolve empty state ("Create your first project")
5. **Secondary action** (optional) -- Docs link, import option, alternative path

## Layout Rules
- Left-align elements as a block (exception: small tiles center illustration above left-aligned text)
- Multiple empty states on one view: use tertiary buttons; only ONE gets a primary button
- Never leave a space truly empty -- no blank areas, no "undefined" text
- Search empty states must suggest alternatives
- Illustrations need alt text for accessibility

</empty_states>

<error_messages>

## Error Message Formula

```
[What happened] + [Why it happened (if helpful)] + [What to do about it]
```

**Example**: "We couldn't save your changes. The file is too large (max 10MB). Try compressing the image first."

## Error Message Guidelines (3 categories)

### Visibility
1. Display errors adjacent to where they occurred
2. Bold, high-contrast, color-blind-accessible styling; animation for attention
3. Differentiate warnings from blocking errors; modals for severe issues
4. Validate on field blur, not during input; provide constraints upfront

### Communication
5. Plain language -- no jargon, no error codes shown to users
6. Precise description -- not "An error occurred"
7. Constructive advice -- offer specific remedy
8. Positive tone -- never blame user; avoid "invalid," "illegal," "incorrect"

### Efficiency
9. Detect common errors proactively (suggest corrections)
10. Preserve input -- allow editing, never force restart
11. Offer suggested fixes or selection lists
12. Educate via concise messaging or linked resources

## Tone Rules

| Do | Don't |
|---|---|
| "We couldn't find that page" | "You entered an invalid URL" |
| "Something went wrong on our end" | "Your request caused an error" |
| "We're working to fix this" | "Oopsie! We broke something!" |
| "This action couldn't be completed" | "CRITICAL ERROR! FAILURE!" |
| "Your password needs at least 8 characters" | "Invalid password" |

## Error Patterns by Context

| Context | Pattern |
|---|---|
| **Form validation** | Inline, adjacent to field. Validate on blur. Show constraints upfront. |
| **Page-level error** | Banner at top of content area. Persists until resolved. |
| **System-wide outage** | Global banner above navigation. Links to status page. |
| **Network failure** | Inline replacement: "Couldn't load [section]. Check your connection." + Retry |
| **Destructive action failure** | Modal or inline alert. High-severity styling. Explain what was NOT changed. |

## Hostile Error Anti-Patterns

- **Premature validation** -- "invalid email" while user is still typing
- **Red styling for non-errors** -- error-like treatment for informational messages
- **Multiple severity indicators** -- asterisk + red text + icon + border = visual overload
- **Hiding useful info** -- not telling user what format is expected
- **Requiring restart** -- forcing re-entry from scratch after an error

</error_messages>

<success_states>

## Success Feedback Scaling Matrix

| Action Type | Significance | Frequency | Feedback |
|---|---|---|---|
| Routine/trivial | Low | High | **No feedback** or subtle inline indicator (checkmark) |
| Standard action | Medium | Medium | **Toast** (auto-dismiss 3-8s) |
| Important action | High | Low | **Banner** or inline success with next-step guidance |
| Critical/irreversible | Very high | Very low | **Full-page confirmation** with summary + next actions |
| Background/async | Varies | Low | **System notification** (email, push) when complete |

## Feedback Pattern Details

- **Inline indicator**: Subtle visual change (checkmark, green flash). Duration: 1-2s or persistent. Minimal disruption.
- **Toast**: Non-modal, bottom or top-right. Auto-dismiss 3-8s. Pause on hover. If toast includes actionable link (e.g., "Undo"), do NOT auto-dismiss -- persist until user dismisses.
- **Banner**: Persistent in relevant section. Until user dismisses or condition resolves.
- **Full-page confirmation**: Summary of what happened + what happens next + primary CTA for next step.
- **Next-action success**: Confirmation + immediate guidance toward next logical action. Don't leave users stranded at a green checkmark.

## Success Microcopy Rules
- Be explicit: "Your order is placed!" not "Done!"
- Include next steps: "Track your order" / "Continue shopping"
- Set expectations: "Confirmation email within 5 minutes"
- Celebrate proportionally to action significance

## Success Anti-Patterns

1. **Over-celebrating routine actions** -- Toast for every auto-save creates fatigue
2. **Under-confirming critical actions** -- No confirmation after payment leads to retries
3. **Dead-end confirmation** -- "Success!" with no next step
4. **Delayed feedback** -- Confirming 3 steps after the action
5. **Self-evident redundancy** -- Toasting "Saved!" when UI already visually confirmed

</success_states>

<microcopy>

## Microcopy Taxonomy (12 types)

| Type | Specification Guidance |
|---|---|
| **Action labels** | Verb + object: "Download report", "Add to cart" |
| **Form labels** | Unambiguous, close to field, never replaced by placeholder |
| **Placeholder text** | Format examples ("MM/DD/YYYY"), not instructions. Never sole label. |
| **Instructional copy** | Explain "why" before "how": "To receive updates, enter your email" |
| **Error messages** | Three-part: what happened + why + what to do |
| **Confirmation messages** | Explicit + next steps: "Order placed! Track it here." |
| **Tooltips** | Definitions/clarifications only. Never critical info. Must be keyboard-focusable. |
| **Empty state copy** | Headline + explanation + CTA |
| **Concern alleviators** | Trust-building: "Your data is encrypted" near payment forms |
| **Navigation labels** | Consistent terminology, one term per concept |
| **Status text** | "Saving...", "Last updated 2 min ago", "3 of 12 loaded" |
| **Loading text** | "Loading your hooks..." -- only when skeleton/spinner insufficient |

## Core Writing Rules

1. **One idea per element** -- don't combine instructions with warnings in one label
2. **Verb + object for actions** -- "Save changes", not "Submit" or "OK"
3. **Specific over generic** -- "Add profile picture" beats "Add"
4. **Consistent terminology** -- one term per concept throughout the product
5. **Positive framing** -- "Use only numbers and letters" not "Don't use special characters"
6. **Concrete examples over abstract rules** -- real numbers, real dates
7. **Why before how** -- "To receive shipping updates, enter your phone number"

## Content-Specific Rules

**Labels**: Never use placeholder as sole label (accessibility). Required fields: asterisk or "required" -- pick one.
**Tooltips**: Sparingly. Definitions only. Must be focusable for keyboard/screen reader.
**Help text**: Below input field. Progressive disclosure: essential context upfront, "Learn more" for depth.
**Placeholder text**: Format examples only. Adequate contrast. Never sole labeling.

## Tone by Data State

| Context | Tone | Example |
|---|---|---|
| Default/guidance | Helpful, patient | "Enter your email to get started" |
| Error | Concerned, reassuring | "We couldn't save your changes. Try again." |
| Success | Warm, confirmatory | "Your profile is updated!" |
| Empty state | Encouraging, activating | "No hooks yet. Add your first one." |
| Loading | Informational, brief | "Loading your dashboard..." |
| Warning | Calm, specific | "This action can't be undone" |

</microcopy>

<partial_states>

## Partial / Mixed Data States

### Primary vs Secondary Experience Rule
- **Primary experience** (essential for page to be useful): If fails -> show error page
- **Secondary experience** (enriches but not essential): If fails -> render degraded page

### Degradation Strategies

| Component | Strategy When Data Unavailable |
|---|---|
| Content sections | Replace with error blankslate (alert icon + message + optional retry) |
| Navigation links | Remove unavailable links entirely (don't show broken links) |
| Counts/badges | Hide rather than showing "undefined" or "0" |
| Buttons (non-critical) | Remove from view |
| Buttons (critical) | Inactive state with tooltip explaining why disabled |
| Dialogs | Prevent opening if content can't load; or blankslate inside dialog |

### Communication Rules
1. Don't conceal problems -- be transparent
2. Global banner for system-wide issues (above nav, links to status page)
3. Contextual inline errors in addition to global banner
4. Specific over generic: "Couldn't load star counts" not "Some data is unavailable"

</partial_states>

<specification_template>

## Per-Component Data State Template

```
### [Component Name] -- Data States

**Loading**: [Skeleton/Spinner/None] -- [what appears]
**Empty**: [headline] / [body] / [CTA label]
**Error**: [what + why + recovery action]
**Success**: [inline/toast/banner/page] -- [microcopy]
**Partial**: [hide/replace/degrade strategy]
```

</specification_template>
