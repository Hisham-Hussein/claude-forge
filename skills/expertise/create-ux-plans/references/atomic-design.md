<overview>
A classification framework and state completeness discipline for UX plan component specifications. Organizes components by ascending complexity (atoms, molecules, organisms, templates) and enforces systematic state documentation at each level so coding agents can implement without guesswork.
</overview>

<decision_rules>

## Classification Decision Tree

| Question | Yes | No |
|----------|-----|-----|
| Can this be decomposed into smaller functional parts? | Molecule or organism | **Atom** |
| Does this group serve a single responsibility? | **Molecule** | Might be organism |
| Does this form a distinct, identifiable page section? | **Organism** | Molecule |
| Does this combine organisms into a page layout? | **Template** | Organism |

## Level Tests

- **Atom test**: "Can I remove any sub-part and still have it make sense?" If removing any part destroys it, it's an atom.
- **Molecule test**: "Does this group of atoms do exactly one thing?" Single responsibility = molecule.
- **Organism test**: "Can I point to a page region and say 'that's the [X] section'?" Distinct section = organism.
- **Template**: Defines how organisms arrange on a specific page. Not a component — a layout.

## Gray Zone Resolution

When classification is unclear, decide by **independence and complexity**:
- Exists meaningfully in isolation + contains multiple functional sub-groups = organism
- Always used within a larger context + serves one purpose = molecule
- Simple card (title + description) = molecule. Complex card (title + description + metadata + badge + stars + link) = organism.

## Organism vs Template Boundary

- **Organism**: Reusable across pages (header appears on every page)
- **Template**: Defines a unique page structure (specific page layout)

## Build vs Document Order

- **Build order**: Atoms first, then molecules, then organisms (bottom-up)
- **Document order in UX plan**: Atoms first, then molecules, then organisms (same)
- **Derivation order**: Top-down from story map. Page sections (organisms) derived from user activities, then decomposed into molecules and atoms.

## State Documentation Principle

A component with only its default state documented is **incomplete**. State completeness is the primary discipline — more important than precise classification. Use the state applicability matrix below to determine which states each component type requires.

## State Description Style

Use emphasis-based descriptions, not specific visual values:
- "Hover: subtle emphasis increase over default"
- "Disabled: reduced to low emphasis, non-interactive cursor"
- "Error: high-emphasis warning treatment with icon and descriptive text"

The design system maps emphasis levels to specific colors/opacities.

## State Explosion Mitigation

Document primary states individually. For combinations (e.g., disabled + selected), only document **exceptions** — cases where the combined behavior isn't obvious from the individual states.

</decision_rules>

<state_taxonomy>

## Interactive States (User-Triggered)

| State | Trigger | Visual Treatment | Applies To |
|-------|---------|-----------------|------------|
| Default | No interaction | Base appearance | All |
| Hover | Cursor over | Subtle change (overlay, shadow, color shift) | Clickable elements; N/A touch |
| Focus | Tab/keyboard | Visible focus ring (3:1 contrast min) | All interactive elements |
| Active/Pressed | Click/tap in progress | Compressed/depressed appearance | Buttons, chips, links, cards |
| Dragged | Element being dragged | Elevated, semi-transparent | Drag-enabled only |

## System States (Application-Triggered)

| State | Trigger | Visual Treatment | Applies To |
|-------|---------|-----------------|------------|
| Disabled | Logic prevents interaction | Lower opacity, non-interactive cursor | Conditionally unavailable elements |
| Loading | Data being fetched | Spinner, skeleton, progress bar | Data-dependent components |
| Error | Operation failed | Warning color, icon, message | Components that can fail |
| Empty | No data available | Friendly message + suggested action | Data containers (grids, lists, results) |
| Success | Operation completed | Confirmation color, icon, brief message | Completable actions |
| Selected/Active | User toggled ON | Filled/highlighted, checkmark | Toggle-able elements |

## Content States (Data-Triggered)

| State | Trigger | Visual Treatment |
|-------|---------|-----------------|
| Skeleton | Content loading, shape known | Gray placeholder shapes matching dimensions |
| Partial | Some data loaded, some failed | Real content + error indicators for failed parts |
| Truncated | Content exceeds space | Ellipsis, "show more", or fade gradient |
| Overflow | Too many items | Pagination, "show all", or scrollable container |

</state_taxonomy>

<state_applicability_matrix>

| Component Type | Default | Hover | Focus | Active | Disabled | Loading | Error | Empty | Selected |
|---------------|---------|-------|-------|--------|----------|---------|-------|-------|----------|
| Button | YES | YES | YES | YES | Maybe | Maybe | N/A | N/A | N/A |
| Link | YES | YES | YES | YES | Maybe | N/A | N/A | N/A | N/A |
| Filter chip | YES | YES | YES | YES | Maybe | N/A | N/A | N/A | YES |
| Card | YES | YES | YES | YES | N/A | YES | YES | N/A | N/A |
| Input field | YES | YES | YES | YES | Maybe | N/A | YES | N/A | N/A |
| Badge | YES | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Icon | YES | N/A | N/A | N/A | Maybe | N/A | N/A | N/A | N/A |
| Grid/List | YES | N/A | N/A | N/A | N/A | YES | YES | YES | N/A |
| Search bar | YES | YES | YES | YES | N/A | YES | YES | YES | N/A |
| Navigation | YES | YES | YES | YES | N/A | N/A | N/A | N/A | YES |
| Hero section | YES | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

</state_applicability_matrix>

<patterns>

## Universal Component Inventory

### Atoms (Indivisible Building Blocks)

| Category | Components |
|----------|-----------|
| Actions | Button (primary, secondary, ghost, icon), Link, Icon button |
| Display | Icon, Badge, Avatar, Divider, Skeleton placeholder |
| Text | Heading (h1-h6), Body text, Caption, Label, Code/monospace |
| Input | Text input, Textarea, Checkbox, Radio button, Toggle switch, Slider |
| Feedback | Spinner, Progress bar |
| Layout | Box (primitive container), Spacer |

### Molecules (Simple Functional Groups)

| Category | Components |
|----------|-----------|
| Input groups | Search bar (input + button), Form field (label + input + validation), Select/Dropdown (input + options list) |
| Display groups | Card header (title + badge/metadata), Metadata row (icon + text + timestamp), Stat display (number + label), Chip/Tag (label + optional close icon) |
| Navigation | Breadcrumb (link chain), Tab item (label + indicator), Pagination controls (prev + page numbers + next) |
| Feedback | Toast/Notification (icon + message + action), Empty state (icon + message + CTA), Error message (icon + text + retry) |

### Organisms (Complex Interface Sections)

| Category | Components |
|----------|-----------|
| Page sections | Header (logo + nav + search), Hero section (heading + subtitle + CTA), Footer (links + attribution) |
| Content | Card grid (repeated card molecules), Data table (headers + rows + pagination), Accordion/FAQ section |
| Interactive | Filter section (label + chip groups + clear button), Navigation bar (links + active indicator + responsive), Form (fields + submission) |
| Overlay | Modal/Dialog (header + body + actions), Drawer/Sidebar (nav items + close), Popover (trigger + content) |

### Templates (Page-Level Layouts)

- Landing page: Hero + filter section + content grid + footer
- Detail page: Header + content body + sidebar + footer
- Search results: Header + search/filter bar + results list + pagination + footer
- Dashboard: Header + stat cards + data tables + charts

</patterns>

<component_doc_format>

```
### [Component Name] — [Atomic Level]

**Purpose**: [What this component does, traced to SM-XXX / US-XXX]

**States**:
| State | Visual Description | Behavior |
|-------|-------------------|----------|
| Default | [How it looks at rest] | [What user can do] |
| Hover | [Visual change on hover] | [Feedback purpose] |
| Focus | [Focus ring description] | [Keyboard interaction] |
| Active | [Pressed appearance] | [What happens on click/tap] |
| Disabled | [De-emphasized appearance] | [Why disabled, what to do] |
| Loading | [Skeleton/spinner] | [What's being loaded] |
| Error | [Error appearance + microcopy] | [Recovery action] |
| Empty | [Empty appearance + microcopy] | [Suggested action] |
| Selected | [Active/toggled appearance] | [Toggle behavior] |

**Accessibility**: [Semantic HTML, ARIA attributes, keyboard behavior]
```

Only include rows for applicable states per the applicability matrix.

</component_doc_format>

<examples>

## Filter Chip (Molecule) — Complete State Documentation

**Composition**: Label atom + visual container

| State | Visual Description | Behavior |
|-------|-------------------|----------|
| Default (inactive) | Outlined container, medium-emphasis text | Available for selection |
| Hover (inactive) | Subtle emphasis increase over outline | Cursor: pointer |
| Focus (inactive) | Focus ring visible (3:1 contrast), outlined | Tab-navigable. Space/Enter toggles to active |
| Active/Pressed | Brief pressed feedback | Transitions to Selected |
| Selected (active) | Filled container, high-emphasis text | Filter applied. Click to deselect |
| Hover (active) | Subtle emphasis increase over filled bg | Cursor: pointer |
| Focus (active) | Focus ring visible, filled container | Space/Enter toggles to inactive |
| Disabled | Low emphasis, non-interactive cursor | Cannot toggle |

**Accessibility**: Role `checkbox`/`switch`, `aria-pressed`, keyboard Space/Enter toggle, part of `role="group"` with `aria-label`.

</examples>

<anti_patterns>

1. **Classification over completeness**: Spending time debating atom vs molecule while states go undocumented
2. **Default-only components**: Specifying only the happy/loaded state; no hover, focus, loading, error, or empty
3. **Re-specification**: Higher-level components re-describing lower-level parts instead of referencing them
4. **Forced classification**: Making every element fit a level; third-party embeds and edge cases may not classify cleanly
5. **Visual-value leakage**: Specifying "opacity: 0.38" or "#ef4444" instead of emphasis-based descriptions
6. **State matrix overkill**: Documenting every state combination (10+ combos per chip) instead of documenting primaries + exceptions
7. **Missing level**: Jumping from atoms to organisms without documenting the molecule compositions
8. **Terminology in UI**: Using "atom", "molecule", "organism" in user-facing specs; these are internal vocabulary only

</anti_patterns>
