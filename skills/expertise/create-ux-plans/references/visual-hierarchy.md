<overview>
Procedural reference for specifying abstract visual hierarchy in UX plans.
Covers type role taxonomy, emphasis levels, scanning patterns, spatial hierarchy via Gestalt principles, and the element specification template. All specifications are design-system-agnostic.
</overview>


<type_roles>

## Universal Type Role Taxonomy

| Universal Role | Semantic Meaning | Usage |
|---|---|---|
| **Display** | Hero-level, short impactful text | Feature headlines, hero numbers |
| **Heading** (1-6) | Section structure, content hierarchy | Page titles, section markers, card titles |
| **Body** | Paragraph text, descriptions | Long-form reading, content blocks |
| **Body Small** | Supporting text, secondary info | Supplementary descriptions |
| **Caption** | Metadata, timestamps, fine print | Auxiliary information |
| **Label** | Buttons, form labels, tags, chips | Short functional text |
| **Overline** | Category labels above headings | Pre-heading category markers |
| **Code** | Monospace technical content | Code blocks, inline code |

Assign type roles based on **functional purpose**, not visual appearance. A screen title should use a Heading role, not a manually enlarged body style.

## Semantic Token Layers

The UX plan operates at **Layer 2** (semantic tokens):

```
Layer 1: Primitive tokens (raw values)     -> font-size-16, font-weight-600
Layer 2: Semantic tokens (role-based)       -> heading-md-size, heading-md-weight
Layer 3: Component tokens (contextual)      -> card-title-size -> heading-md-size
```

UX plans specify "card-title uses heading-3, medium emphasis" (Layer 2), not pixel values (Layer 1) or component token names (Layer 3).

</type_roles>


<emphasis_model>

## Emphasis Levels

| Level | Usage | Examples |
|---|---|---|
| **High** | Primary text, titles, active labels, important content | Page titles, primary CTAs, active nav items |
| **Medium** | Secondary text, supporting info, inactive labels | Card descriptions, secondary buttons, filter labels |
| **Low** | Supplementary, de-emphasized content | Metadata, timestamps, helper text, footer |
| **Disabled** | Non-interactive, unavailable content | Disabled controls, placeholder text |

Emphasis is **orthogonal to type role**. Any role can be rendered at any emphasis level. "heading-3, high emphasis" and "heading-3, low emphasis" are both valid.

## Combined Role + Emphasis Model

Every text element gets BOTH a type role AND an emphasis level:

```
Visual Hierarchy (highest to lowest):
1. page-title         -> display,    high emphasis
2. section-title      -> heading-2,  high emphasis
3. card-title         -> heading-3,  medium emphasis
4. card-description   -> body,       medium emphasis
5. card-metadata      -> caption,    low emphasis
6. filter-label       -> label,      medium emphasis
7. filter-chip-text   -> label-sm,   medium emphasis
8. empty-state-title  -> heading-3,  medium emphasis
9. empty-state-body   -> body,       low emphasis
10. footer-text       -> body-sm,    low emphasis
```

Resolution chain: UX plan says "card-title -> heading-3, medium emphasis" + design system says "heading-3 = 18px semibold; medium emphasis = 70% opacity" = coding agent implements "18px semibold at 70% opacity."

## Attention Hierarchy Beyond Text

Classify ALL visual elements into emphasis levels, not just text. Interactive elements (buttons, links, CTAs), badges, icons, dividers, and containers all need emphasis classification.

Principle: "When everything is important, nothing is important." Limit high-emphasis elements to enforce meaningful contrast.

## Importance Dimension (Component-Level)

Relative emphasis between instances of the same element type:

| Level | Example |
|---|---|
| Primary | Primary button, main CTA |
| Secondary | Secondary button, supporting action |
| Tertiary | Ghost button, minimal action |

</emphasis_model>


<scanning_patterns>

## Pattern Selection Rules

| Pattern | When to Specify | Page Characteristics |
|---|---|---|
| **F-pattern** | Content-heavy pages with multiple text blocks | Catalogs, docs, search results, data tables |
| **Z-pattern** | Minimal-content pages with clear CTAs | Landing pages, marketing, login, hero sections |
| **Layer-cake** | Pages with strong heading structure | FAQ, structured forms, settings panels |
| **Spotted** | Pages where users skip to specific elements | Forms with scattered inputs, widget dashboards |
| **Commitment** | Content users read word-by-word | Legal text, critical instructions, pricing |

## Selection Decision Rules

1. **Default to F-pattern** for content-heavy pages (catalogs, feeds, documentation)
2. **Use Z-pattern** for pages with < 5 major content elements and a clear CTA
3. **Use layer-cake** when strong heading structure is the primary navigation aid
4. **Never specify a pattern for forms** -- forms follow their own field-order logic
5. **Always place highest-priority content** in the first horizontal band (F) or top-left (Z)
6. **Account for RTL**: If the product supports right-to-left languages, note that patterns mirror

## Specification Format

Scanning pattern is specified **per page**, not globally:

```
Page: Hook Catalog (Homepage)
Scanning pattern: F-pattern
Content placement by scan zone:
  - F-bar-1 (top horizontal): Page title, filter controls
  - F-bar-2 (second horizontal): Active filter summary, result count
  - F-stem (left vertical): Card titles, card categories (left-aligned)
  - Right zone (low attention): Card metadata, star counts
```

```
Page: About / Info
Scanning pattern: Z-pattern
Content placement by scan zone:
  - Z-point-1 (top-left): Logo / brand mark
  - Z-point-2 (top-right): Primary navigation / CTA
  - Z-diagonal (center): Hero illustration or value proposition
  - Z-point-3 (bottom-left): Supporting info / social proof
  - Z-point-4 (bottom-right): Primary CTA button
```

Scanning patterns are descriptive of typical behavior, not rigid prescriptions. State the expected pattern, justify based on content density, map content to zones, but do NOT dictate pixel positions.

</scanning_patterns>


<spatial_hierarchy>

## Gestalt Principles for Spatial Specification

| Principle | Rule | Specification Example |
|---|---|---|
| **Proximity** | Elements placed close = perceived group. More powerful than color. | "Filter chips: tight spacing (related). Filter-to-grid: increased spacing (separate sections)." |
| **Alignment** | Shared alignment edge = perceived relation and order. | "All card content left-aligned to content edge. Metadata row baseline-aligned." |
| **Common Region** | Shared boundary = group. | "Each card enclosed in container. Filter section in its own region." |
| **Whitespace** | More surrounding space = higher perceived importance. | "Section gaps > card gaps > intra-card gaps. Page title has most whitespace." |

## Abstract Spacing Scale

| Level | Name | Usage |
|---|---|---|
| **XS** | Compact | Related elements within a component (label to value) |
| **S** | Tight | Elements within a group (card title to description) |
| **M** | Standard | Default spacing between siblings (card to card) |
| **L** | Relaxed | Section breaks (filter area to grid area) |
| **XL** | Spacious | Major page divisions (hero to content, content to footer) |

**Mapping rule**: Spacing level = relationship distance:
- Same component -> XS or S
- Same section -> M
- Different sections -> L
- Different page regions -> XL

## Container Nesting Hierarchy

```
Page (outermost container)
  -> Section (major content area)
    -> Component Group (organism)
      -> Component (molecule)
        -> Element (atom)
```

Each nesting level gets decreasing internal spacing and decreasing corner radius. Outer containers have more visual weight than inner ones.

## Visual Weight Dimensions (Abstract)

| Dimension | Higher Weight | Lower Weight | Specification Method |
|---|---|---|---|
| **Size** | Larger | Smaller | "Large" / "Medium" / "Small" relative to siblings |
| **Contrast** | High contrast | Low contrast | "High emphasis" / "Low emphasis" |
| **Position** | Top-left (F), center | Bottom, periphery | Scanning zone reference |
| **Whitespace** | More surrounding space | Less space | Spacing level (XS-XL) |
| **Density** | More content/detail | Less content | "Dense" / "Comfortable" / "Sparse" |
| **Elevation** | Raised/floating | Flat/embedded | "Elevated" / "Surface-level" / "Recessed" |

</spatial_hierarchy>


<element_template>

## Element Specification Template

For each element in the Visual Hierarchy Map:

```
Element: [role-based name, e.g., "card-title"]
  Type role: [heading-3 | body | caption | label | ...]
  Emphasis: [high | medium | low | disabled]
  Position: [scanning zone, e.g., "F-bar-1, left-aligned"]
  Container: [parent component, e.g., "hook-card"]
  Spatial: [spacing to adjacent elements, e.g., "S below, XS right of badge"]
  Semantic HTML: [h3 | p | span | time | ...]
  Hierarchy rank: [1-N, ordered from most to least prominent on page]
```

Example:

```
Element: card-title
  Type role: heading-3
  Emphasis: medium
  Position: Top of card, left-aligned
  Container: hook-card (organism)
  Spatial: S spacing below, XS spacing right of category badge
  Semantic HTML: h3
  Hierarchy rank: 3 (after page-title and section-title)
```

</element_template>


<anti_patterns>

- Do NOT conflate type role with emphasis. "heading-3 at low emphasis" is valid (e.g., de-emphasized sidebar section title).
- Do NOT specify more than ~20-25 unique hierarchy entries per page. If more are needed, the page likely needs splitting.
- Do NOT forget non-text elements. Badges, icons, dividers, and containers all have hierarchy positions.
- Do NOT mark everything as "high emphasis" (emphasis inflation). Limit to 3 contrast/emphasis variations maximum per view.
- Do NOT use color as a primary hierarchy method. Use size and weight first.
- Do NOT specify pixel values or concrete design tokens. Use abstract roles, emphasis levels, and spacing scale.
- Do NOT assign a single global scanning pattern. Each page gets its own pattern based on content density.
- Do NOT start visual design before defining hierarchy. Hierarchy must come first.
- Do NOT assume scanning patterns are left-to-right by default without noting RTL support needs.

</anti_patterns>
