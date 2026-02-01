<overview>
Decision rules and pattern inventories for specifying filter/search, card grid, animation, feedback timing, navigation, and micro-interaction behaviors in UX plans. Specs must be design-system-agnostic yet precise enough to eliminate developer guesswork.
</overview>

<filter_patterns>

## Filter Placement Taxonomy

| Pattern | Scalability | Best For |
|---|---|---|
| **Left sidebar** | High (vertically scrollable) | Complex filtering, 5+ facets, directories, catalogs |
| **Horizontal top bar** | Low-Medium (viewport-constrained) | Fewer categories (<5), dashboards, inline filtering |
| **Chips / Pills** | Low-Medium (horizontal scroll) | Active filter display, single-dimension toggling, mobile |
| **Bottom sheet / Modal** | Medium (full-screen mobile) | Mobile filtering with many options |

## Filter Application Method Decision

**Interactive (Live Results)** -- Use when: users are exploring; results return in <1s; few filter dimensions (1-3).
Must specify: result-area loading behavior; scroll position after update; result enter/leave animation; delay before applying (1-2s inactivity recommended).

**Batch (Apply Button)** -- Use when: users have clear criteria; performance inconsistent; multiple simultaneous filters; heavy datasets.
Must specify: persistent "Apply" button; unapplied changes indicator; "Reset"/"Clear All" at individual and global levels.

**Hybrid** -- Interactive for simple controls (chips), batch for complex ones (date ranges, multi-select).

## Filter Specification Checklist

1. **Placement**: Sidebar, top bar, chips, or combination
2. **Application method**: Interactive, batch, or hybrid
3. **Multi-select**: Checkboxes (multi) vs radio buttons (single) within one facet
4. **Boolean logic**: AND between facets or OR within a facet
5. **Applied filter visibility**: Chip summary, inline indicators, count badges
6. **Clear/reset**: Per-filter clear, global "Clear All", reset to defaults
7. **No-results handling**: Message, suggestion to broaden, auto-disable zero-result facets
8. **Mobile adaptation**: Bottom sheet, modal, collapsed accordion
9. **Result count display**: "(N)" count per filter option
10. **URL persistence**: Filter state in URL for sharing/bookmarking

## Applied Filter Communication (Three-Layer Redundancy)

1. **Source preservation** -- Control retains visual state (checked checkbox, highlighted chip)
2. **Indicator labels** -- Count badges "(3)" next to group labels, bold for active groups
3. **Summary section** -- "Applied Filters" area with removable chips

</filter_patterns>

<card_patterns>

## Card Interaction States (all must be defined)

| State | Visual Behavior | Trigger |
|---|---|---|
| **Default** | Border/shadow/background distinguishes from page | Passive |
| **Hover** | Elevated shadow, scale (1.01-1.02x), border/background shift | Cursor enters |
| **Focused** | Focus ring (3:1 contrast min) | Keyboard tab |
| **Pressed** | Depression (reduced shadow, slight scale-down) | Click/tap begins |
| **Selected** | Checkmark, border highlight, tint | User selects |
| **Disabled** | Reduced opacity, no hover/click | System condition |
| **Loading** | Skeleton or spinner within bounds | Data fetching |

## Card Click Behaviors

**Full-Card -> Navigate**: Entire card is one target. For directories, link collections. Specify: same/new tab; cursor style; how secondary actions stop propagation.

**Card -> Expand/Reveal**: Expands in-place or opens overlay. For dashboards, summaries. Specify: animation; overlay vs push-aside; collapse method (click outside, close button, Escape).

**Multiple Actions**: Distinct zones -- main area + buttons. Specify: target boundaries; visual zone distinction; touch targets min 44x44px.

## Card Grid Layouts

| Pattern | When to Use |
|---|---|
| **Uniform grid** | Homogeneous content, similar data density |
| **Masonry** | Varying content amounts |
| **Bento grid** | Dashboard/showcase where hierarchy matters |

## Card Content Hierarchy
1. Primary visual (image/icon) -- optional  2. Title (5-7 words, high emphasis)  3. Supporting text (1-2 lines)  4. Metadata (~10-15 words, low emphasis)  5. Action(s) -- visually distinct

## When NOT to Use Cards
Search-focused interfaces (lists scan faster); homogeneous item lists; comparison workflows; photo galleries.

</card_patterns>

<animation_rules>

## Duration Decision Matrix

| The change... | Category | Range |
|---|---|---|
| Is a micro-interaction (toggle, check, button) | **Short** | 50-200ms |
| Is a standard transition (modal, expand, filter) | **Medium** | 200-400ms |
| Involves large screen area changes | **Long** | 400-600ms |
| Is decorative/celebratory | **Extra-long** | 600ms-1s |
| Has no perceptible wait | **None** | Instant |

**Rules**: Max 500ms for any standard UI animation. Exit animations 20-25% shorter than entry. Platform: desktop faster than mobile (300ms baseline); tablet ~30% longer; wearables ~30% shorter.

## Easing Decision Table

| Easing | When to Use |
|---|---|
| **Ease-out** | **Default.** Elements entering or transitioning. Starts fast, slows to rest. |
| **Ease-in** | Elements **leaving** the screen. Accelerates away. |
| **Ease-in-out** | Elements **staying on screen** while transforming (grow/shrink, reposition). |
| **Linear** | **Almost never.** Only: spinners, opacity-only fades, color interpolation. |

## Safe to Animate vs Avoid

**Animate**: Opacity (lightest cost), transform: translate (GPU), transform: scale (GPU), color/background (moderate), box-shadow (moderate).
**Avoid animating**: Width/height (reflow -- use scale), margin/padding (reflow), border-radius (sparingly), font-size (reflow), content/text (appear or replace, don't animate).

## Accessibility (non-negotiable)
- Respect `prefers-reduced-motion`: disable/minimize all non-essential animations
- No auto-playing animations without pause/stop (WCAG 2.2.2)
- Nothing flashing >3 times/second (WCAG 2.3.1)
- Critical state changes need non-animated fallback (text change, icon swap)

</animation_rules>

<feedback_timing>

## Optimistic vs Pessimistic UI

### Optimistic (immediate update, assume success)
**Use when ALL true**: Success rate >97%; low-consequence failure; binary action; clean rollback; response <2s.
**Good for**: Like/favorite, filter toggle, add/remove tag, post comment, reorder items.
**Bad for**: Financial transactions, deletion, server-validated forms, sensitive data.

### Pessimistic (wait for confirmation)
**Use when ANY true**: Financial/sensitive; server validation required; irreversible; failure rate >3-5%; user needs processing confirmation.

### Hybrid (typical in real apps)
Filter chips: optimistic. Search: semi-optimistic (debounce 300ms). External links: no feedback. Data export: pessimistic + async notification.

### Long-Running Operations

| Duration | Pattern |
|---|---|
| 0-2s | Pessimistic with inline loading |
| 2-10s | Pessimistic with progress/skeleton |
| 10s+ | Deferred -- acknowledge, let user continue, notify on completion |

**Example**: `Toggle favorite -> Optimistic: icon fills immediately. Rollback on failure: revert + toast "Couldn't save. Try again."`
**Example**: `Submit form -> Pessimistic: button spinner, fields disabled. Success: confirmation page. Error: inline banner, fields re-enabled, input preserved.`

</feedback_timing>

<navigation>

## Navigation Models

| Model | Structure | When to Use |
|---|---|---|
| **Flat** | All pages same level | Small sites (<10 pages), catalogs with filtering |
| **Hierarchical** | Categories -> subcategories -> items | Large content sites, docs, deep e-commerce |
| **Hub-and-spoke** | Central hub -> independent sub-pages | Dashboards, settings, independent features |
| **Sequential** | Step 1 -> step 2 -> step 3 | Onboarding, checkout, wizards |
| **Matrix** | Multiple pathways, no single hierarchy | Research tools, interconnected references |

## Navigation Components

| Component | Specify |
|---|---|
| **Top nav bar** | Items, order, active state, mobile collapse |
| **Sidebar nav** | Expandable sections, active highlight, mobile collapse |
| **Breadcrumbs** | Separator, truncation, clickable ancestors |
| **Tabs** | Labels, active state, load on-switch vs pre-loaded |
| **Pagination** | Page numbers vs load-more vs infinite scroll, items/page |
| **Back/forward** | SPA must update browser history (History API) |

## Navigation Checklist
1. Items and order  2. Active state styling  3. Mobile behavior (hamburger, bottom tabs, drawer)  4. Transition behavior (instant, fade, slide, reload)  5. Deep linking for bookmarking/sharing  6. Keyboard nav (Tab order, Enter, Escape)

</navigation>

<micro_interactions>

## Structure (Saffer's 4 Parts)
1. **Trigger**: User action or system event  2. **Rules**: Response logic  3. **Feedback**: Visual/audio change  4. **Loops & Modes**: Behavior over time or conditions

## Specification Template

```
### [Interaction Name]
- Trigger: [user action or system event]
- Response: [UI changes]
- Animation: [duration category + easing]
- Reversibility: [undo method]
- Accessibility: [keyboard equivalent, screen reader announcement]
- Frequency: [routine/occasional/rare -- informs feedback intensity]
```

**Example**:
```
### Filter Chip Toggle
- Trigger: Click/tap on category chip
- Response: Chip toggles state. Grid filters immediately (optimistic). Count updates.
- Animation: Chip -- short, ease-out. Grid -- fade, medium, ease-out.
- Reversibility: Click to deselect. "Clear all" removes all.
- Accessibility: role="checkbox" + aria-checked. Grid: aria-live "N results".
- Frequency: High -- subtle animation, no toast.
```

**Longevity test**: "Annoying on the 100th use?" Confetti, sounds, bouncy animations -> rare significant actions only.

</micro_interactions>

<anti_patterns>

## Interaction Anti-Patterns
- Over-specifying obvious behaviors ("clicking nav link navigates")
- Animating width/height/margin instead of transforms (causes reflow)
- Linear easing for UI transitions (feels mechanical)
- Animations >500ms for standard transitions
- Missing `prefers-reduced-motion` fallback
- Filter UI with no clear/reset mechanism
- Ambiguous card click targets
- No-results state with no recovery path
- Auto-dismissing toasts containing actionable links
- Touch targets under 44x44px on mobile

</anti_patterns>

<specification_template>

## Per-Component Interaction Template

```
### [Component Name] -- Interactions
**Primary action**: [Click/tap] -> [result]
**Hover**: [Visual change]
**Keyboard**: [Tab focus, Enter/Space, Escape]
**Feedback**: [Optimistic / Pessimistic / None]
**Animation**: [Duration category] + [Easing]
**Mobile**: [Touch target size, gesture variant]
**Reduced motion**: [Fallback when animations disabled]
```

</specification_template>
