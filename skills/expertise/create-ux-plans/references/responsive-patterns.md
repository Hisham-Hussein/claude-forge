<overview>
Responsive design patterns for UX plan specification. Defines how to specify layout, sizing, and behavioral changes across viewport tiers abstractly — without prescribing CSS or framework-specific implementation.
</overview>

<breakpoint_strategy>

## Semantic Viewport Tiers

Use abstract tier names that map to any framework, not pixel values:

```
Mobile      — single-column, touch-primary, portrait assumed
Tablet      — multi-column possible, touch-primary, portrait or landscape
Desktop     — full multi-column, pointer-primary, landscape
Wide        — desktop with maximum content width constraint
```

## How Many Tiers to Specify

| Project Type | Tiers | Rationale |
|-------------|-------|-----------|
| Simple content site (blog, marketing) | 2 (Mobile + Desktop) | Minimal layout changes |
| Standard web app | 3 (Mobile + Tablet + Desktop) | Covers 3 primary interaction modes |
| Complex dashboard / tool | 4 (Mobile + Tablet + Desktop + Wide) | Fine control over dense content |
| Design-system-level spec | 5 (match target framework) | Must align with implementation breakpoints |

## Framework Alignment (approximate convergence)

Mobile: ~<600px | Tablet: ~600-1024px | Desktop: ~1024-1400px | Wide: ~>1400px
(Tailwind, Bootstrap, Material Design 3 all converge on similar ranges despite different naming.)

## Per-Tier Specification Requirements

For each tier define: (1) grid columns, (2) navigation model, (3) content priority (visible vs hidden/collapsed), (4) layout direction, (5) touch vs pointer model, (6) max content width.

</breakpoint_strategy>

<layout_patterns>

## Five Canonical Responsive Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Mostly Fluid** | Content reflows within fixed-width parent; single breakpoint on parent | Simple content pages, blogs |
| **Column Drop** | Columns stack vertically as viewport narrows | Multi-section pages with distinct content blocks |
| **Layout Shifter** | Different layouts at each breakpoint | Complex apps where mobile/desktop have fundamentally different structures |
| **Tiny Tweaks** | Same layout at all sizes; only spacing and font sizes adjust | Single-column designs, articles, landing pages |
| **Off-Canvas** | Secondary content pushed off-screen, revealed on demand | Apps with heavy navigation or secondary panels |

## Material Design 3 Pane Strategies

| Strategy | Description | UX Plan Language |
|----------|-------------|------------------|
| **Show/Hide** | Panes conditionally displayed by available space | "Filter panel hidden at mobile, shown as persistent sidebar at desktop" |
| **Levitate** | Pane elevates to overlay (modal, bottom sheet) at narrow viewports | "Detail view as bottom sheet at mobile, inline pane at desktop" |
| **Reflow** | Panes change size, position, or orientation | "Two side-by-side panes at desktop stack vertically at mobile" |

## Grid Column Reduction

| Desktop | Tablet | Mobile | Typical Use |
|---------|--------|--------|-------------|
| 4 columns | 2 columns | 1 column | Card grids, product catalogs |
| 3 columns | 2 columns | 1 column | Feature grids, team pages |
| 3 columns | 1 column (stacked) | 1 column | Sidebar + content + aside |
| 2 columns | 2 columns | 1 column (stacked) | List + detail, content + sidebar |

## Element-Level Transformations

| Transformation | Example | UX Plan Specification |
|---------------|---------|----------------------|
| **Stack** | Side-by-side -> vertical | "Hero image and text side-by-side at desktop; image stacks above text at mobile" |
| **Collapse** | Full content -> accordion | "Secondary metadata visible at desktop; collapsed behind 'More details' at mobile" |
| **Replace** | One component -> different | "Horizontal filter bar at desktop; filter button opening bottom sheet at mobile" |
| **Hide** | Visible -> removed | "Decorative illustration visible at desktop; hidden at mobile" |
| **Reposition** | Move to different location | "Search bar in header at desktop; dedicated search page at mobile" |
| **Resize** | Proportionally scale | "Hero 60% viewport height at desktop; 40% at mobile" |
| **Reorder** | Change source order | "CTA after content at desktop; promoted to top at mobile" |

</layout_patterns>

<touch_targets>

Standards: WCAG 2.5.5 (AAA) 44x44 CSS px | WCAG 2.5.8 (AA) 24x24 CSS px | Apple HIG 44x44pt | Material 48x48dp

| Scenario | Minimum Target |
|----------|---------------|
| Touch-primary (mobile, tablet) | 44x44 abstract units |
| Touch-possible (laptop touchscreen) | 44x44 abstract units |
| Pointer-primary (desktop) | 24x24 minimum; 44x44 recommended |
| Dense displays (data tables) | 24x24 with adequate spacing |

**Spacing exception (WCAG 2.5.8):** Targets < 24x24 allowed if 24px-diameter circle centered on target doesn't intersect adjacent targets. Inline text links exempt.

</touch_targets>

<mobile_first_specification>

**Default: Mobile-first specification direction.** Forces content prioritization; additive language is clearer ("sidebar becomes visible" > "sidebar is hidden"); aligns with Tailwind/Bootstrap mobile-first queries.

**Exception:** Enterprise dashboards with >80% desktop traffic -- desktop-first may be more natural.

**Pattern:** Describe mobile fully as base tier, then list what each wider tier _adds_ (`+ sidebar becomes visible`, `+ filter bar replaces button`).

</mobile_first_specification>

<responsive_typography>

## Scaling Approaches

- **Breakpoint-stepped**: Sizes change at breakpoints. Simple, easy to specify.
- **Fluid scaling**: Sizes interpolate between min/max. Harder to specify abstractly.
- **Hybrid** (recommended): Body stepped, headings fluid.

## Type Scale Ratios

1.067 (Minor Second) -- dense UI | 1.125 (Major Second) -- mobile body | 1.200 (Minor Third) -- mobile headings | 1.250 (Major Third) -- desktop headings | 1.333 (Perfect Fourth) -- marketing | 1.414 (Augmented Fourth) -- hero/landing | 1.500 (Perfect Fifth) -- display only

## Recommended Pairing

- Mobile (base): 1.125-1.200 (tighter hierarchy)
- Desktop (max): 1.200-1.333 (stronger differentiation)
- Use semantic step names (+1, +2, etc.) not pixel values. Steps: -1 caption, 0 body, +1 subheading, +2 H3, +3 H2, +4 H1, +5 display/hero.

## Accessibility Constraint

WCAG 1.4.4: Text must be resizable to 200% without loss of content. No viewport-unit-only font sizes.

</responsive_typography>

<anti_patterns>

## Specification-Level

| Anti-Pattern | Remedy |
|-------------|--------|
| **"It stacks"** — mobile spec only says elements stack vertically | Specify explicit stacking order with priority; define hidden vs. collapsed vs. preserved |
| **Desktop-only thinking** — detailed desktop, footnote says "responsive" | Start with mobile tier; describe each tier explicitly |
| **Pixel-value leakage** — "768px breakpoint" in UX plan | Use semantic tier names and abstract sizing |
| **Implicit behaviors** — assuming developer will "figure out" mobile nav | Every component needs explicit responsive behavior per tier |
| **Missing intermediate tiers** — only mobile and desktop | Define at least 3 tiers; tablet is often hardest |
| **Responsive as afterthought** — separate "responsive notes" section | Responsive behavior within each component spec |
| **One-direction-only** — only what happens when viewport shrinks | State behavior at each tier independently |
| **Ignoring orientation** — no landscape mobile / portrait tablet | Note where orientation matters |

## Layout-Level

| Anti-Pattern | Better Approach |
|-------------|-----------------|
| **Oversized sticky headers** (>15% mobile viewport) | Header scrolls away or collapses to compact form |
| **Hidden-by-default content** at all viewports | Define content hierarchy; only hide at constrained tiers |
| **Zoom-breaking layouts** | All layouts must accommodate 200% zoom without horizontal scroll |
| **Touch-hostile desktop** — hover-only with no touch alternative | Specify both pointer and touch interaction models |

</anti_patterns>

<validation_checklist>

For every component in the UX plan, verify:

- [ ] All tiers defined (not just desktop)
- [ ] Transformation pattern named (column-drop, reflow, show/hide, etc.)
- [ ] Content priority clear (what hides/collapses, in what order)
- [ ] Touch targets adequate at touch tiers
- [ ] Typography tier-appropriate (correct hierarchy step)
- [ ] Navigation model stated per tier
- [ ] Stacking order explicit (not assumed from source order)
- [ ] Orientation considered where relevant

</validation_checklist>

<examples>

## Per-Component Responsive Spec Example

```
Hook Card Grid:
  Desktop:  4 columns, cards at fixed aspect ratio, all metadata visible
  Tablet:   2 columns, cards maintain aspect ratio, metadata truncated to 2 lines
  Mobile:   1 column, full-width cards, metadata collapsed behind "more" toggle
  Pattern:  Column drop with progressive disclosure
```

## Responsive Specification Table Template

| Aspect | Mobile | Tablet | Desktop |
|--------|--------|--------|---------|
| Layout | [description] | [description] | [description] |
| Navigation | [model] | [model] | [model] |
| Content visibility | [what's visible] | [what's added] | [what's added] |
| Interactive elements | [touch targets] | [touch/pointer] | [pointer primary] |
| Typography scale | [tier ratio] | [tier ratio] | [tier ratio] |

</examples>
