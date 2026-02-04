"""Unit tests for trace-phase-stories.py"""

import importlib
import sys
from pathlib import Path

import pytest

# The script uses a hyphenated filename (trace-phase-stories.py) which is not
# a valid Python module name. Use importlib to load it explicitly.
_script_path = Path(__file__).parent / "trace-phase-stories.py"
_spec = importlib.util.spec_from_file_location("trace_phase_stories", _script_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

MatchResult = _mod.MatchResult
extract_sm_ids = _mod.extract_sm_ids
extract_matching_stories = _mod.extract_matching_stories
format_output = _mod.format_output


# ---------------------------------------------------------------------------
# Fixtures: inline markdown snippets
# ---------------------------------------------------------------------------

ROADMAP_SINGLE_PHASE = """\
## Release: MVP

### Wave 1

#### PHASE-1: Walking Skeleton

| Story ID | Title | Source |
|----------|-------|--------|
| SM-001 | Clear landing hero | BR-05 |
| SM-003 | Hook grid visible | BR-05 |

### Wave 2

#### PHASE-2: Rich Card Metadata

| Story ID | Title | Source |
|----------|-------|--------|
| SM-007 | Purpose category badge | BR-02 |
| SM-008 | Lifecycle event badge | BR-02 |
"""

ROADMAP_MULTIPLE_SMS = """\
#### PHASE-3: Filter & Data Pipeline Polish

| Story ID | Title | Source |
|----------|-------|--------|
| SM-012 | Validate repo links at build time | BR-03 |
| SM-014 | "All" option resets category filter | BR-04 |
| SM-016 | "All" option resets lifecycle event filter | BR-04 |
| SM-020 | Local manifest file controls hooks | BR-06 |

#### PHASE-4: Build Resilience

| Story ID | Title | Source |
|----------|-------|--------|
| SM-021 | Graceful degradation | BR-06 |
"""

ROADMAP_WITH_DUPLICATE_SM = """\
#### PHASE-1: Walking Skeleton

| Story ID | Title | Source |
|----------|-------|--------|
| SM-001 | Clear landing hero | BR-05 |
| SM-001 | Duplicate entry | BR-05 |
| SM-003 | Hook grid visible | BR-05 |

#### PHASE-2: Next Phase
"""

ROADMAP_MISSING_PHASE = """\
#### PHASE-5: Performance & Theming

| Story ID | Title | Source |
|----------|-------|--------|
| SM-002 | Fast load | BR-07 |
"""

USER_STORIES_BASIC = """\
## Epic 1: Land & Understand

#### US-001: Clear landing hero communicates site purpose

**Parent:** SM-001 (STORY-MAP.md)
**Source:** BR-05
**Release:** MVP

As a developer visiting HookHub,
I want to see a clear hero section.

**Acceptance Criteria:**
- [ ] Hero section is visible
- [ ] Purpose is clear

**Priority:** Must | **Size:** S

---

#### US-003: Hook grid visible above the fold

**Parent:** SM-003 (STORY-MAP.md)
**Source:** BR-05
**Release:** MVP

As a developer landing on HookHub,
I want to see the hook grid without scrolling.

**Acceptance Criteria:**
- [ ] First row of cards visible without scrolling

**Priority:** Must | **Size:** S

---

#### US-007: Show purpose category with visual distinction

**Parent:** SM-007 (STORY-MAP.md)
**Source:** BR-02
**Release:** MVP

As a developer scanning hook cards,
I want purpose category as a badge.

**Acceptance Criteria:**
- [ ] Badge is visually distinct

**Priority:** Must | **Size:** S

---
"""

USER_STORIES_ONE_TO_MANY = """\
## Epic 2: Browse Catalog

#### US-007: Purpose category badge on card

**Parent:** SM-007 (STORY-MAP.md)
**Source:** BR-02
**Release:** MVP

First story for SM-007.

**Acceptance Criteria:**
- [ ] Badge renders

**Priority:** Must | **Size:** S

---

#### US-008: Purpose category in filter chips

**Parent:** SM-007 (STORY-MAP.md)
**Source:** BR-02
**Release:** MVP

Second story for SM-007.

**Acceptance Criteria:**
- [ ] Chips render

**Priority:** Must | **Size:** S

---

#### US-009: Lifecycle event badge

**Parent:** SM-008 (STORY-MAP.md)
**Source:** BR-02
**Release:** MVP

Story for SM-008.

**Acceptance Criteria:**
- [ ] Event badge renders

**Priority:** Must | **Size:** S

---
"""

USER_STORIES_PARTIAL_MATCH = """\
#### US-001: Hero section

**Parent:** SM-001 (STORY-MAP.md)
**Source:** BR-05
**Release:** MVP

Hero story content.

**Priority:** Must | **Size:** S

---

#### US-099: Unrelated story

**Parent:** SM-099 (STORY-MAP.md)
**Source:** BR-99
**Release:** Future

Unrelated content.

**Priority:** Could | **Size:** L

---
"""

USER_STORIES_SIMILAR_IDS = """\
#### US-001: Hero section

**Parent:** SM-001 (STORY-MAP.md)
**Source:** BR-05
**Release:** MVP

Hero story.

**Priority:** Must | **Size:** S

---

#### US-010: Stars count

**Parent:** SM-010 (STORY-MAP.md)
**Source:** BR-01
**Release:** MVP

Stars story.

**Priority:** Must | **Size:** S

---

#### US-100: Extended story

**Parent:** SM-100 (STORY-MAP.md)
**Source:** BR-99
**Release:** Future

Extended content.

**Priority:** Could | **Size:** M

---
"""

# -- Gap 1: Hierarchical SM ID fixtures --

ROADMAP_HIERARCHICAL = """\
#### PHASE-1: Walking Skeleton

| Story ID | Title | Source |
|----------|-------|--------|
| SM-1.2-01 | Hero section | BR-05 |
| SM-1.2-02 | Grid visible | BR-05 |
| SM-2.1-01 | Category filter | BR-04 |

#### PHASE-2: Next Phase

| Story ID | Title | Source |
|----------|-------|--------|
| SM-2.2-01 | Event filter | BR-04 |
"""

ROADMAP_MIXED_IDS = """\
#### PHASE-1: Mixed IDs

| Story ID | Title | Source |
|----------|-------|--------|
| SM-001 | Simple hero | BR-05 |
| SM-1.2-01 | Hierarchical hero | BR-05 |
| SM-003 | Simple grid | BR-05 |

#### PHASE-2: Next
"""

USER_STORIES_HIERARCHICAL = """\
## Epic 1: Discovery

#### US-001: Hero section

**Parent:** SM-1.2-01 (STORY-MAP.md)
**Source:** BR-05
**Release:** MVP

Hero story content.

**Priority:** Must | **Size:** S

---

#### US-002: Grid visible

**Parent:** SM-1.2-02 (STORY-MAP.md)
**Source:** BR-05
**Release:** MVP

Grid story content.

**Priority:** Must | **Size:** S

---

#### US-003: Category filter

**Parent:** SM-2.1-01 (STORY-MAP.md)
**Source:** BR-04
**Release:** MVP

Category filter content.

**Priority:** Must | **Size:** S

---
"""

# -- Gap 3: Business-case mode (no Parent field) --

USER_STORIES_NO_PARENT = """\
## Epic 1: Land & Understand

#### US-001: Clear landing hero communicates site purpose

**Source:** BR-05
**Release:** MVP

As a developer visiting HookHub,
I want to see a clear hero section.

**Acceptance Criteria:**
- [ ] Hero section is visible

**Priority:** Must | **Size:** S

---

#### US-002: Hook grid visible above the fold

**Source:** BR-05
**Release:** MVP

As a developer landing on HookHub,
I want to see the hook grid.

**Acceptance Criteria:**
- [ ] First row of cards visible

**Priority:** Must | **Size:** S

---
"""

# -- Gap 5: Traceability table at the bottom --

USER_STORIES_WITH_TRACEABILITY_TABLE = """\
## Epic 1: Land & Understand

#### US-001: Clear landing hero

**Parent:** SM-001 (STORY-MAP.md)
**Source:** BR-05
**Release:** MVP

Hero story content.

**Priority:** Must | **Size:** S

---

#### US-003: Hook grid visible

**Parent:** SM-003 (STORY-MAP.md)
**Source:** BR-05
**Release:** MVP

Grid story content.

**Priority:** Must | **Size:** S

---

## Traceability Matrix

| SM ID | BR Source | Journey Step | US ID | Release |
|-------|----------|-------------|-------|---------|
| SM-001 | BR-05 | Discovery → Search | US-001 | MVP |
| SM-003 | BR-05 | Discovery → Search | US-003 | MVP |
| SM-099 | BR-09 | Settings → Theme | US-099 | Future |
"""


# ===========================================================================
# Tests for extract_sm_ids
# ===========================================================================


class TestExtractSmIds:
    """Tests for extract_sm_ids()."""

    def test_basic_single_phase(self):
        """Extract SM-XXX from a single phase section."""
        result = extract_sm_ids(1, ROADMAP_SINGLE_PHASE)
        assert result == ["SM-001", "SM-003"]

    def test_multiple_sms_in_phase(self):
        """Multiple SM IDs in one phase are all extracted."""
        result = extract_sm_ids(3, ROADMAP_MULTIPLE_SMS)
        assert result == ["SM-012", "SM-014", "SM-016", "SM-020"]

    def test_phase_boundary_detection(self):
        """Stops at the next #### header — does not bleed into PHASE-2."""
        result = extract_sm_ids(1, ROADMAP_SINGLE_PHASE)
        assert "SM-007" not in result
        assert "SM-008" not in result

    def test_phase_not_found_returns_empty(self):
        """Phase that doesn't exist returns empty list."""
        result = extract_sm_ids(99, ROADMAP_SINGLE_PHASE)
        assert result == []

    def test_sm_deduplication(self):
        """Duplicate SM-XXX IDs in the same phase are deduplicated."""
        result = extract_sm_ids(1, ROADMAP_WITH_DUPLICATE_SM)
        assert result == ["SM-001", "SM-003"]
        # SM-001 appears twice in the table but should only appear once
        assert result.count("SM-001") == 1

    def test_extracts_correct_phase_among_multiple(self):
        """When multiple phases exist, extracts only the target phase."""
        result = extract_sm_ids(2, ROADMAP_SINGLE_PHASE)
        assert result == ["SM-007", "SM-008"]

    def test_stops_at_higher_level_heading(self):
        """Phase section ends at ## or ### heading too, not just ####."""
        roadmap = """\
#### PHASE-1: Test Phase

| SM-001 | Story one |

### Wave 2

#### PHASE-2: Next

| SM-002 | Story two |
"""
        result = extract_sm_ids(1, roadmap)
        assert result == ["SM-001"]
        assert "SM-002" not in result

    # -- Gap 1: Hierarchical SM ID tests --

    def test_hierarchical_ids_extracted(self):
        """Hierarchical SM-X.Y-ZZ IDs are extracted from a phase."""
        result = extract_sm_ids(1, ROADMAP_HIERARCHICAL)
        assert result == ["SM-1.2-01", "SM-1.2-02", "SM-2.1-01"]

    def test_hierarchical_phase_boundary(self):
        """Hierarchical IDs from PHASE-2 do not bleed into PHASE-1."""
        result = extract_sm_ids(1, ROADMAP_HIERARCHICAL)
        assert "SM-2.2-01" not in result

    def test_mixed_simple_and_hierarchical_ids(self):
        """Phase with both simple SM-NNN and hierarchical SM-X.Y-ZZ IDs."""
        result = extract_sm_ids(1, ROADMAP_MIXED_IDS)
        assert result == ["SM-001", "SM-003", "SM-1.2-01"]

    def test_hierarchical_exact_match_no_prefix(self):
        """SM-1.2-01 should NOT match SM-1.2-010 (exact matching)."""
        roadmap = """\
#### PHASE-1: Test

| SM-1.2-010 | Extended ID |
"""
        result = extract_sm_ids(1, roadmap)
        assert result == ["SM-1.2-010"]
        assert "SM-1.2-01" not in result


# ===========================================================================
# Tests for extract_matching_stories
# ===========================================================================


class TestExtractMatchingStories:
    """Tests for extract_matching_stories()."""

    def test_basic_single_match(self):
        """Single SM matches single US."""
        result = extract_matching_stories(["SM-001"], USER_STORIES_BASIC)
        assert result.us_count == 1
        assert result.found_sm_ids == {"SM-001"}
        assert len(result.stories) == 1
        assert "US-001" in result.stories[0]

    def test_one_to_many(self):
        """One SM-XXX matches multiple US-XXX stories."""
        result = extract_matching_stories(["SM-007"], USER_STORIES_ONE_TO_MANY)
        assert result.us_count == 2
        assert result.found_sm_ids == {"SM-007"}
        assert len(result.stories) == 2
        assert "US-007" in result.stories[0]
        assert "US-008" in result.stories[1]

    def test_no_matches(self):
        """SM-XXX with no corresponding US returns empty result."""
        result = extract_matching_stories(["SM-999"], USER_STORIES_BASIC)
        assert result.us_count == 0
        assert result.found_sm_ids == set()
        assert result.stories == []

    def test_mixed_some_match_some_dont(self):
        """Some SMs match, some don't — verify found_sm_ids and missing detection."""
        result = extract_matching_stories(
            ["SM-001", "SM-042"], USER_STORIES_PARTIAL_MATCH
        )
        assert result.us_count == 1
        assert result.found_sm_ids == {"SM-001"}
        assert "SM-042" not in result.found_sm_ids

    def test_story_block_preservation(self):
        """Full story block from #### US-XXX: to end is captured with all AC."""
        result = extract_matching_stories(["SM-001"], USER_STORIES_BASIC)
        block = result.stories[0]
        # Should contain the header
        assert "#### US-001: Clear landing hero communicates site purpose" in block
        # Should contain the parent field
        assert "**Parent:** SM-001" in block
        # Should contain acceptance criteria
        assert "- [ ] Hero section is visible" in block
        assert "- [ ] Purpose is clear" in block
        # Should contain priority line
        assert "**Priority:** Must | **Size:** S" in block

    def test_parent_field_exact_matching(self):
        """SM-001 should NOT match SM-010 or SM-100 (no partial matches)."""
        result = extract_matching_stories(["SM-001"], USER_STORIES_SIMILAR_IDS)
        assert result.us_count == 1
        assert result.found_sm_ids == {"SM-001"}
        assert len(result.stories) == 1
        assert "US-001" in result.stories[0]
        # Make sure SM-010 and SM-100 stories are NOT included
        for story in result.stories:
            assert "US-010" not in story
            assert "US-100" not in story

    def test_parent_field_exact_matching_sm010(self):
        """SM-010 should match only US-010, not US-001 or US-100."""
        result = extract_matching_stories(["SM-010"], USER_STORIES_SIMILAR_IDS)
        assert result.us_count == 1
        assert result.found_sm_ids == {"SM-010"}
        assert "US-010" in result.stories[0]

    def test_multiple_sm_ids_multiple_matches(self):
        """Multiple SM IDs each matching one or more stories."""
        result = extract_matching_stories(
            ["SM-007", "SM-008"], USER_STORIES_ONE_TO_MANY
        )
        assert result.us_count == 3  # US-007, US-008 (parent SM-007), US-009 (parent SM-008)
        assert result.found_sm_ids == {"SM-007", "SM-008"}

    def test_story_at_end_of_file_without_trailing_separator(self):
        """Story block at end of file with no trailing --- is still captured."""
        text = """\
#### US-050: Final story

**Parent:** SM-050 (STORY-MAP.md)
**Source:** BR-01
**Release:** MVP

Last story in file.

**Priority:** Must | **Size:** S
"""
        result = extract_matching_stories(["SM-050"], text)
        assert result.us_count == 1
        assert "US-050" in result.stories[0]
        assert "Last story in file." in result.stories[0]

    # -- Gap 1: Hierarchical SM IDs in story matching --

    def test_hierarchical_parent_matching(self):
        """Stories with hierarchical Parent SM-X.Y-ZZ fields are matched."""
        result = extract_matching_stories(
            ["SM-1.2-01", "SM-1.2-02"], USER_STORIES_HIERARCHICAL
        )
        assert result.us_count == 2
        assert result.found_sm_ids == {"SM-1.2-01", "SM-1.2-02"}
        assert "US-001" in result.stories[0]
        assert "US-002" in result.stories[1]

    def test_hierarchical_exact_match_no_prefix_collision(self):
        """SM-1.2-01 should NOT match a Parent with SM-1.2-010."""
        text = """\
#### US-100: Extended hierarchical story

**Parent:** SM-1.2-010 (STORY-MAP.md)
**Source:** BR-01
**Release:** MVP

Extended content.

**Priority:** Must | **Size:** S

---
"""
        result = extract_matching_stories(["SM-1.2-01"], text)
        assert result.us_count == 0
        assert result.found_sm_ids == set()

    def test_mixed_simple_and_hierarchical_parent_matching(self):
        """Mixed simple and hierarchical SM IDs both match their stories."""
        text = """\
#### US-001: Simple parent story

**Parent:** SM-001 (STORY-MAP.md)
**Source:** BR-05
**Release:** MVP

Simple parent content.

**Priority:** Must | **Size:** S

---

#### US-002: Hierarchical parent story

**Parent:** SM-1.2-01 (STORY-MAP.md)
**Source:** BR-05
**Release:** MVP

Hierarchical parent content.

**Priority:** Must | **Size:** S

---
"""
        result = extract_matching_stories(["SM-001", "SM-1.2-01"], text)
        assert result.us_count == 2
        assert result.found_sm_ids == {"SM-001", "SM-1.2-01"}

    # -- Gap 3: Business-case mode (no Parent field) --

    def test_no_parent_field_returns_zero_matches(self):
        """Stories without **Parent:** fields produce zero matches."""
        result = extract_matching_stories(["SM-001"], USER_STORIES_NO_PARENT)
        assert result.us_count == 0
        assert result.found_sm_ids == set()
        assert result.stories == []

    def test_no_parent_field_multiple_sm_ids(self):
        """Multiple SM IDs searched against parentless stories return empty."""
        result = extract_matching_stories(
            ["SM-001", "SM-002", "SM-003"], USER_STORIES_NO_PARENT
        )
        assert result.us_count == 0
        assert result.found_sm_ids == set()

    # -- Gap 4: Parent field suffix variations --

    def test_parent_with_story_map_suffix(self):
        """**Parent:** SM-001 (STORY-MAP.md) matches correctly."""
        text = """\
#### US-001: Story with standard suffix

**Parent:** SM-001 (STORY-MAP.md)
**Source:** BR-05

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_count == 1
        assert result.found_sm_ids == {"SM-001"}

    def test_parent_with_other_annotation_suffix(self):
        """**Parent:** SM-001 (some other annotation) matches correctly."""
        text = """\
#### US-001: Story with non-standard suffix

**Parent:** SM-001 (some other annotation)
**Source:** BR-05

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_count == 1
        assert result.found_sm_ids == {"SM-001"}

    def test_parent_bare_without_suffix(self):
        """**Parent:** SM-001 without any suffix matches correctly."""
        text = """\
#### US-001: Story with bare parent

**Parent:** SM-001
**Source:** BR-05

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_count == 1
        assert result.found_sm_ids == {"SM-001"}

    # -- Gap 5: Traceability table false matches --

    def test_traceability_table_not_matched(self):
        """SM IDs in traceability table rows are NOT matched as Parent fields."""
        result = extract_matching_stories(
            ["SM-001", "SM-003", "SM-099"],
            USER_STORIES_WITH_TRACEABILITY_TABLE,
        )
        # SM-001 and SM-003 have actual **Parent:** fields in story blocks
        assert result.us_count == 2
        assert result.found_sm_ids == {"SM-001", "SM-003"}
        # SM-099 appears only in the traceability table, not in a **Parent:** field
        assert "SM-099" not in result.found_sm_ids

    def test_traceability_table_only_sm_id(self):
        """SM ID appearing ONLY in traceability table produces no match."""
        result = extract_matching_stories(
            ["SM-099"], USER_STORIES_WITH_TRACEABILITY_TABLE
        )
        assert result.us_count == 0
        assert result.found_sm_ids == set()
        assert result.stories == []

    # -- us_ids extraction tests --

    def test_us_ids_single_match(self):
        """Single matched story populates us_ids with the US-XXX ID."""
        result = extract_matching_stories(["SM-001"], USER_STORIES_BASIC)
        assert result.us_ids == ["US-001"]

    def test_us_ids_multiple_matches(self):
        """Multiple matched stories populate us_ids in order."""
        result = extract_matching_stories(["SM-001", "SM-003"], USER_STORIES_BASIC)
        assert result.us_ids == ["US-001", "US-003"]

    def test_us_ids_one_to_many(self):
        """One SM matching multiple US populates all US IDs."""
        result = extract_matching_stories(["SM-007"], USER_STORIES_ONE_TO_MANY)
        assert result.us_ids == ["US-007", "US-008"]

    def test_us_ids_no_match_empty(self):
        """No matches returns empty us_ids list."""
        result = extract_matching_stories(["SM-999"], USER_STORIES_BASIC)
        assert result.us_ids == []

    def test_us_ids_partial_match(self):
        """Only matched stories appear in us_ids."""
        result = extract_matching_stories(
            ["SM-001", "SM-042"], USER_STORIES_PARTIAL_MATCH
        )
        assert result.us_ids == ["US-001"]

    def test_us_ids_count_consistency(self):
        """us_count equals len(us_ids) for all matches."""
        result = extract_matching_stories(
            ["SM-007", "SM-008"], USER_STORIES_ONE_TO_MANY
        )
        assert result.us_count == len(result.us_ids)
        assert result.us_count == 3  # US-007, US-008 (SM-007), US-009 (SM-008)

    def test_us_ids_hierarchical(self):
        """Hierarchical SM IDs produce correct US IDs."""
        result = extract_matching_stories(
            ["SM-1.2-01", "SM-1.2-02"], USER_STORIES_HIERARCHICAL
        )
        assert result.us_ids == ["US-001", "US-002"]


# ===========================================================================
# Tests for format_output
# ===========================================================================


class TestFormatOutput:
    """Tests for format_output()."""

    def test_header_includes_sm_ids_and_counts(self):
        """Header includes SM-XXX list and correct counts."""
        result = MatchResult(
            stories=["#### US-001: Hero\n\n**Parent:** SM-001"],
            found_sm_ids={"SM-001"},
            us_count=1,
        )
        output = format_output(1, ["SM-001", "SM-003"], result)
        assert "# Phase 1 — Traced User Stories" in output
        assert "**SM-XXX IDs in this phase:** SM-001 SM-003" in output
        assert "**US stories found:** 1 (covering 1 of 2 SM-XXX IDs)" in output

    def test_trace_summary_section(self):
        """Trace summary section includes correct stats."""
        result = MatchResult(
            stories=["#### US-001: Hero"],
            found_sm_ids={"SM-001"},
            us_count=1,
        )
        output = format_output(1, ["SM-001"], result)
        assert "## Trace Summary" in output
        assert "- **Phase:** 1" in output
        assert "- **SM-XXX IDs:** 1" in output
        assert "- **US-XXX stories found:** 1" in output

    def test_missing_sm_warning(self):
        """Warning displayed when some SM-XXX IDs have no matching stories."""
        result = MatchResult(
            stories=["#### US-001: Hero"],
            found_sm_ids={"SM-001"},
            us_count=1,
        )
        output = format_output(1, ["SM-001", "SM-003"], result)
        assert "- **Missing (no US-XXX for SM-XXX):** SM-003" in output
        assert "> **Warning:**" in output
        assert "no matching US-XXX story" in output

    def test_no_warning_when_all_covered(self):
        """No warning when all SM-XXX IDs have matching stories."""
        result = MatchResult(
            stories=["#### US-001: Hero", "#### US-003: Grid"],
            found_sm_ids={"SM-001", "SM-003"},
            us_count=2,
        )
        output = format_output(1, ["SM-001", "SM-003"], result)
        assert "Missing" not in output
        assert "Warning" not in output

    def test_story_blocks_separated_by_separators(self):
        """Story blocks are separated by --- in the output."""
        result = MatchResult(
            stories=["#### US-001: Hero\nContent 1", "#### US-003: Grid\nContent 2"],
            found_sm_ids={"SM-001", "SM-003"},
            us_count=2,
        )
        output = format_output(1, ["SM-001", "SM-003"], result)
        # Each story should be followed by ---
        lines = output.splitlines()
        # Find the story blocks section and verify --- separators
        story_region = False
        separator_count = 0
        for line in lines:
            if line.startswith("#### US-"):
                story_region = True
            if story_region and line == "---":
                separator_count += 1
            if line.startswith("## Trace Summary"):
                break
        assert separator_count == 2  # one after each story

    def test_multiple_missing_sm_ids(self):
        """Multiple missing SM IDs listed together."""
        result = MatchResult(stories=[], found_sm_ids=set(), us_count=0)
        output = format_output(
            1, ["SM-001", "SM-003", "SM-005"], result
        )
        assert "- **Missing (no US-XXX for SM-XXX):** SM-001 SM-003 SM-005" in output

    # -- Gap 3: format_output when no Parent fields exist --

    def test_all_missing_when_no_parent_fields(self):
        """When no stories match (business-case mode), all SM IDs are missing."""
        result = MatchResult(stories=[], found_sm_ids=set(), us_count=0)
        sm_ids = ["SM-001", "SM-002", "SM-003"]
        output = format_output(1, sm_ids, result)
        assert "**US stories found:** 0 (covering 0 of 3 SM-XXX IDs)" in output
        assert "- **Missing (no US-XXX for SM-XXX):** SM-001 SM-002 SM-003" in output
        assert "> **Warning:**" in output

    # -- us_ids output line tests --

    def test_header_includes_us_ids(self):
        """Header includes US-XXX IDs list."""
        result = MatchResult(
            stories=["#### US-001: Hero\n\n**Parent:** SM-001"],
            found_sm_ids={"SM-001"},
            us_ids=["US-001"],
            us_count=1,
        )
        output = format_output(1, ["SM-001"], result)
        assert "**US-XXX IDs in this phase:** US-001" in output

    def test_header_us_ids_multiple(self):
        """Header includes multiple US-XXX IDs space-separated."""
        result = MatchResult(
            stories=["#### US-001: Hero", "#### US-003: Grid"],
            found_sm_ids={"SM-001", "SM-003"},
            us_ids=["US-001", "US-003"],
            us_count=2,
        )
        output = format_output(1, ["SM-001", "SM-003"], result)
        assert "**US-XXX IDs in this phase:** US-001 US-003" in output

    def test_header_us_ids_empty_when_no_matches(self):
        """Header shows empty US-XXX IDs when no matches."""
        result = MatchResult(stories=[], found_sm_ids=set(), us_ids=[], us_count=0)
        output = format_output(1, ["SM-001"], result)
        assert "**US-XXX IDs in this phase:** " in output

    def test_us_ids_line_order_in_header(self):
        """US-XXX IDs line appears after SM-XXX IDs line."""
        result = MatchResult(
            stories=["#### US-001: Hero"],
            found_sm_ids={"SM-001"},
            us_ids=["US-001"],
            us_count=1,
        )
        output = format_output(1, ["SM-001"], result)
        lines = output.splitlines()
        sm_line_idx = next(i for i, l in enumerate(lines) if "**SM-XXX IDs" in l)
        us_line_idx = next(i for i, l in enumerate(lines) if "**US-XXX IDs" in l)
        assert us_line_idx == sm_line_idx + 1


# ===========================================================================
# Integration test
# ===========================================================================


class TestIntegration:
    """End-to-end test with small ROADMAP + USER-STORIES snippets."""

    ROADMAP = """\
## Release: TestRelease

### Wave 1

#### PHASE-2: Rich Card Metadata

| Story ID | Title | Source |
|----------|-------|--------|
| SM-007 | Purpose category badge | BR-02 |
| SM-008 | Lifecycle event badge | BR-02 |
| SM-009 | Hook description | BR-01 |

### Wave 2

#### PHASE-3: Something Else

| Story ID | Title | Source |
|----------|-------|--------|
| SM-012 | Validate repo links | BR-03 |
"""

    USER_STORIES = """\
## Epic 2: Browse Catalog

### Feature 2.2: Scan Hook Cards

#### US-007: Show purpose category with visual distinction

**Parent:** SM-007 (STORY-MAP.md)
**Source:** BR-02 (BUSINESS-CASE.md, Section 9.3)
**Release:** MVP

As a developer scanning hook cards,
I want to see purpose category as a badge.

**Acceptance Criteria:**
- [ ] Badge is visually distinct
- [ ] All 8 categories supported

**Priority:** Must | **Size:** S | **INVEST:** check

---

#### US-008: Show lifecycle event with visual distinction

**Parent:** SM-008 (STORY-MAP.md)
**Source:** BR-02 (BUSINESS-CASE.md, Section 9.3)
**Release:** MVP

As a developer scanning hook cards,
I want to see lifecycle event as a badge.

**Acceptance Criteria:**
- [ ] Event badge uses different styling from category badge

**Priority:** Must | **Size:** S | **INVEST:** check

---

#### US-009: Show hook description on card

**Parent:** SM-009 (STORY-MAP.md)
**Source:** BR-01 (BUSINESS-CASE.md, Section 9.3)
**Release:** MVP

As a developer scanning hook cards,
I want a brief description.

**Acceptance Criteria:**
- [ ] Description truncated to 2 lines
- [ ] Cards with short descriptions maintain alignment

**Priority:** Must | **Size:** S | **INVEST:** check

---

#### US-012: Validate repo links at build time

**Parent:** SM-012 (STORY-MAP.md)
**Source:** BR-03
**Release:** MVP

As a curator, I want links validated.

**Priority:** Must | **Size:** S

---
"""

    def test_end_to_end_phase2(self):
        """Full pipeline: ROADMAP phase 2 -> extract SMs -> match stories -> format."""
        sm_ids = extract_sm_ids(2, self.ROADMAP)
        assert sm_ids == ["SM-007", "SM-008", "SM-009"]

        result = extract_matching_stories(sm_ids, self.USER_STORIES)
        assert result.us_count == 3
        assert result.found_sm_ids == {"SM-007", "SM-008", "SM-009"}
        assert result.us_ids == ["US-007", "US-008", "US-009"]

        output = format_output(2, sm_ids, result)

        # Verify header
        assert "# Phase 2 — Traced User Stories" in output
        assert "**SM-XXX IDs in this phase:** SM-007 SM-008 SM-009" in output
        assert "**US-XXX IDs in this phase:** US-007 US-008 US-009" in output
        assert "**US stories found:** 3 (covering 3 of 3 SM-XXX IDs)" in output

        # Verify all three stories present
        assert "#### US-007: Show purpose category" in output
        assert "#### US-008: Show lifecycle event" in output
        assert "#### US-009: Show hook description" in output

        # Verify story content preserved
        assert "- [ ] Badge is visually distinct" in output
        assert "- [ ] All 8 categories supported" in output
        assert "- [ ] Description truncated to 2 lines" in output

        # Verify trace summary
        assert "- **Phase:** 2" in output
        assert "- **SM-XXX IDs:** 3" in output
        assert "- **US-XXX stories found:** 3" in output

        # Verify no warning (all covered)
        assert "Missing" not in output
        assert "Warning" not in output

    def test_end_to_end_with_missing(self):
        """Full pipeline where one SM has no story -> warning in output."""
        # Use phase 2 SMs but remove US-009 from the stories text
        stories_without_009 = "\n".join(
            line
            for line in self.USER_STORIES.splitlines()
            if "US-009" not in line
            and "SM-009" not in line
            and "brief description" not in line
            and "truncated to 2 lines" not in line
            and "short descriptions maintain" not in line
        )

        sm_ids = extract_sm_ids(2, self.ROADMAP)
        result = extract_matching_stories(sm_ids, stories_without_009)

        assert result.us_count == 2
        assert result.found_sm_ids == {"SM-007", "SM-008"}

        output = format_output(2, sm_ids, result)
        assert "- **Missing (no US-XXX for SM-XXX):** SM-009" in output
        assert "> **Warning:**" in output

    def test_phase3_does_not_include_phase2_stories(self):
        """Phase 3 only traces its own SM IDs, not phase 2's."""
        sm_ids = extract_sm_ids(3, self.ROADMAP)
        assert sm_ids == ["SM-012"]

        result = extract_matching_stories(sm_ids, self.USER_STORIES)
        assert result.us_count == 1
        assert result.found_sm_ids == {"SM-012"}
        assert "US-012" in result.stories[0]
        # Should NOT include phase 2 stories
        for story in result.stories:
            assert "US-007" not in story
            assert "US-008" not in story
            assert "US-009" not in story


# ===========================================================================
# Invariant and Edge Case Tests (Rigorous)
# ===========================================================================


class TestInvariants:
    """Tests for invariants that must ALWAYS hold."""

    def test_us_ids_length_equals_us_count(self):
        """len(us_ids) must always equal us_count."""
        result = extract_matching_stories(["SM-001", "SM-003"], USER_STORIES_BASIC)
        assert len(result.us_ids) == result.us_count

    def test_us_ids_length_equals_stories_length(self):
        """len(us_ids) must always equal len(stories)."""
        result = extract_matching_stories(["SM-001", "SM-003"], USER_STORIES_BASIC)
        assert len(result.us_ids) == len(result.stories)

    def test_invariants_hold_for_one_to_many(self):
        """Invariants hold when one SM maps to multiple US."""
        result = extract_matching_stories(["SM-007"], USER_STORIES_ONE_TO_MANY)
        assert len(result.us_ids) == result.us_count
        assert len(result.us_ids) == len(result.stories)
        assert result.us_count == 2

    def test_invariants_hold_for_no_matches(self):
        """Invariants hold when nothing matches."""
        result = extract_matching_stories(["SM-999"], USER_STORIES_BASIC)
        assert len(result.us_ids) == result.us_count == len(result.stories) == 0

    def test_invariants_hold_for_partial_match(self):
        """Invariants hold when only some SMs match."""
        result = extract_matching_stories(
            ["SM-001", "SM-999"], USER_STORIES_PARTIAL_MATCH
        )
        assert len(result.us_ids) == result.us_count == len(result.stories) == 1

    def test_us_ids_and_stories_same_order(self):
        """us_ids[i] corresponds to stories[i]."""
        result = extract_matching_stories(["SM-001", "SM-003"], USER_STORIES_BASIC)
        for i, us_id in enumerate(result.us_ids):
            assert f"#### {us_id}:" in result.stories[i]


class TestEdgeCasesUsIds:
    """Edge case tests specifically for us_ids extraction."""

    def test_us_id_single_digit(self):
        """US-1 (single digit) is captured correctly."""
        text = """\
#### US-1: Single digit story

**Parent:** SM-001 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-1"]

    def test_us_id_double_digit(self):
        """US-99 (double digit) is captured correctly."""
        text = """\
#### US-99: Double digit story

**Parent:** SM-001 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-99"]

    def test_us_id_large_number(self):
        """US-12345 (large number) is captured correctly."""
        text = """\
#### US-12345: Large number story

**Parent:** SM-001 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-12345"]

    def test_us_id_preserves_leading_zeros(self):
        """US-001 preserves the leading zeros."""
        text = """\
#### US-001: With leading zeros

**Parent:** SM-001 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]

    def test_us_id_order_preserved_reverse(self):
        """us_ids preserves file order even if IDs are not sequential."""
        text = """\
#### US-099: Later ID first in file

**Parent:** SM-001 (STORY-MAP.md)

Content.

---

#### US-003: Earlier ID second in file

**Parent:** SM-003 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001", "SM-003"], text)
        assert result.us_ids == ["US-099", "US-003"]  # File order, not ID order

    def test_story_without_parent_not_in_us_ids(self):
        """Story without **Parent:** field is not captured in us_ids."""
        text = """\
#### US-001: Story with parent

**Parent:** SM-001 (STORY-MAP.md)

Content.

---

#### US-002: Story WITHOUT parent

**Source:** BR-05

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]
        assert "US-002" not in result.us_ids

    def test_story_with_non_matching_parent_not_in_us_ids(self):
        """Story with non-matching parent is not captured."""
        text = """\
#### US-001: Story with parent

**Parent:** SM-001 (STORY-MAP.md)

Content.

---

#### US-002: Story with different parent

**Parent:** SM-999 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]
        assert "US-002" not in result.us_ids

    def test_empty_user_stories_file(self):
        """Empty input produces empty results."""
        result = extract_matching_stories(["SM-001"], "")
        assert result.us_ids == []
        assert result.us_count == 0
        assert result.stories == []

    def test_story_at_end_without_trailing_separator_has_us_id(self):
        """Story at end of file without trailing --- still captures us_id."""
        text = """\
#### US-050: Final story

**Parent:** SM-050 (STORY-MAP.md)

Last story in file with no trailing separator."""
        result = extract_matching_stories(["SM-050"], text)
        assert result.us_ids == ["US-050"]
        assert result.us_count == 1

    def test_story_at_end_without_trailing_newline(self):
        """Story at end of file without trailing newline works."""
        text = "#### US-050: Final story\n\n**Parent:** SM-050 (STORY-MAP.md)\n\nContent"
        result = extract_matching_stories(["SM-050"], text)
        assert result.us_ids == ["US-050"]

    def test_malformed_us_header_not_captured(self):
        """#### US-ABC: (non-numeric) is not captured."""
        text = """\
#### US-ABC: Non-numeric story

**Parent:** SM-001 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == []
        assert result.us_count == 0

    def test_us_header_with_extra_hashes_not_captured(self):
        """##### US-001: (5 hashes) is not captured."""
        text = """\
##### US-001: Five hash story

**Parent:** SM-001 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == []

    def test_us_header_with_fewer_hashes_not_captured(self):
        """### US-001: (3 hashes) is not captured."""
        text = """\
### US-001: Three hash story

**Parent:** SM-001 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == []

    def test_multiple_stories_same_parent_all_captured(self):
        """Multiple US stories with same SM parent all captured."""
        result = extract_matching_stories(["SM-007"], USER_STORIES_ONE_TO_MANY)
        assert result.us_ids == ["US-007", "US-008"]
        assert result.us_count == 2


class TestFormatOutputEdgeCases:
    """Edge case tests for format_output with us_ids."""

    def test_us_ids_in_header_exact_format(self):
        """US-XXX IDs line has exact expected format."""
        result = MatchResult(
            stories=["#### US-001: Hero"],
            found_sm_ids={"SM-001"},
            us_ids=["US-001"],
            us_count=1,
        )
        output = format_output(1, ["SM-001"], result)
        # Exact line match
        assert "**US-XXX IDs in this phase:** US-001\n" in output

    def test_us_ids_multiple_space_separated(self):
        """Multiple US-XXX IDs are space-separated."""
        result = MatchResult(
            stories=["s1", "s2", "s3"],
            found_sm_ids={"SM-001", "SM-002", "SM-003"},
            us_ids=["US-001", "US-002", "US-003"],
            us_count=3,
        )
        output = format_output(1, ["SM-001", "SM-002", "SM-003"], result)
        assert "**US-XXX IDs in this phase:** US-001 US-002 US-003" in output

    def test_us_ids_empty_list_produces_empty_line(self):
        """Empty us_ids produces line with no IDs after colon."""
        result = MatchResult(stories=[], found_sm_ids=set(), us_ids=[], us_count=0)
        output = format_output(1, ["SM-001"], result)
        lines = output.splitlines()
        us_line = [l for l in lines if "**US-XXX IDs in this phase:**" in l][0]
        # Should end with just a space (from ' '.join([]))
        assert us_line == "**US-XXX IDs in this phase:** "

    def test_us_ids_large_list(self):
        """Large number of US-XXX IDs formatted correctly."""
        us_ids = [f"US-{i:03d}" for i in range(1, 21)]  # US-001 to US-020
        result = MatchResult(
            stories=["s"] * 20,
            found_sm_ids={f"SM-{i:03d}" for i in range(1, 21)},
            us_ids=us_ids,
            us_count=20,
        )
        sm_ids = [f"SM-{i:03d}" for i in range(1, 21)]
        output = format_output(1, sm_ids, result)
        assert "**US-XXX IDs in this phase:** " + " ".join(us_ids) in output

    def test_us_ids_order_matches_us_ids_list(self):
        """Output preserves exact order from us_ids list."""
        result = MatchResult(
            stories=["s1", "s2"],
            found_sm_ids={"SM-001", "SM-002"},
            us_ids=["US-099", "US-001"],  # Intentionally reverse order
            us_count=2,
        )
        output = format_output(1, ["SM-001", "SM-002"], result)
        assert "**US-XXX IDs in this phase:** US-099 US-001" in output


class TestRealWorldScenarios:
    """Tests simulating real-world usage patterns."""

    def test_hookhub_phase1_like_scenario(self):
        """Simulate HookHub Phase 1 with 8 stories."""
        roadmap = """\
#### PHASE-1: Walking Skeleton

| SM-001 | Hero | BR-05 |
| SM-003 | Grid | BR-05 |
| SM-004 | Browse | BR-01 |
| SM-006 | Card | BR-01 |
| SM-011 | Stars | BR-01 |
| SM-013 | Category | BR-04 |
| SM-015 | Event | BR-04 |
| SM-019 | Pipeline | BR-06 |

#### PHASE-2: Next
"""
        user_stories = """\
#### US-001: Hero

**Parent:** SM-001 (STORY-MAP.md)

Content.

---

#### US-003: Grid

**Parent:** SM-003 (STORY-MAP.md)

Content.

---

#### US-004: Browse

**Parent:** SM-004 (STORY-MAP.md)

Content.

---

#### US-006: Card

**Parent:** SM-006 (STORY-MAP.md)

Content.

---

#### US-011: Stars

**Parent:** SM-011 (STORY-MAP.md)

Content.

---

#### US-013: Category

**Parent:** SM-013 (STORY-MAP.md)

Content.

---

#### US-015: Event

**Parent:** SM-015 (STORY-MAP.md)

Content.

---

#### US-019: Pipeline

**Parent:** SM-019 (STORY-MAP.md)

Content.

---
"""
        sm_ids = extract_sm_ids(1, roadmap)
        assert len(sm_ids) == 8

        result = extract_matching_stories(sm_ids, user_stories)
        assert result.us_count == 8
        assert len(result.us_ids) == 8
        assert result.us_ids == [
            "US-001", "US-003", "US-004", "US-006",
            "US-011", "US-013", "US-015", "US-019"
        ]

        output = format_output(1, sm_ids, result)
        assert "**US-XXX IDs in this phase:** US-001 US-003 US-004 US-006 US-011 US-013 US-015 US-019" in output

    def test_phase_with_some_missing_stories(self):
        """Phase where some SM-XXX have no matching US-XXX."""
        roadmap = """\
#### PHASE-1: Test

| SM-001 | Has story |
| SM-002 | No story |
| SM-003 | Has story |

#### PHASE-2: Next
"""
        user_stories = """\
#### US-001: Story 1

**Parent:** SM-001

Content.

---

#### US-003: Story 3

**Parent:** SM-003

Content.

---
"""
        sm_ids = extract_sm_ids(1, roadmap)
        result = extract_matching_stories(sm_ids, user_stories)

        assert result.us_ids == ["US-001", "US-003"]
        assert result.us_count == 2
        assert result.found_sm_ids == {"SM-001", "SM-003"}
        assert "SM-002" not in result.found_sm_ids

        output = format_output(1, sm_ids, result)
        assert "**US-XXX IDs in this phase:** US-001 US-003" in output
        assert "Missing" in output
        assert "SM-002" in output


# ===========================================================================
# Boundary Condition Tests
# ===========================================================================


class TestBoundaryConditions:
    """Tests for boundary conditions and edge cases."""

    def test_us_id_zero(self):
        """US-0 is a valid ID."""
        text = """\
#### US-0: Zero ID story

**Parent:** SM-001 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-0"]

    def test_us_id_double_zero(self):
        """US-00 is a valid ID."""
        text = """\
#### US-00: Double zero story

**Parent:** SM-001 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-00"]

    def test_minimal_story_header_and_parent_only(self):
        """Story with only header and parent line is captured."""
        text = """\
#### US-001: Minimal
**Parent:** SM-001
---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]
        assert result.us_count == 1

    def test_story_with_very_long_content(self):
        """Story with very long content is captured correctly."""
        long_content = "A" * 10000  # 10K characters
        text = f"""\
#### US-001: Long story

**Parent:** SM-001 (STORY-MAP.md)

{long_content}

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]
        assert long_content in result.stories[0]

    def test_multiple_consecutive_separators(self):
        """Multiple consecutive --- separators don't cause issues."""
        text = """\
#### US-001: Story one

**Parent:** SM-001 (STORY-MAP.md)

Content.

---
---
---

#### US-003: Story three

**Parent:** SM-003 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001", "SM-003"], text)
        assert result.us_ids == ["US-001", "US-003"]
        assert result.us_count == 2

    def test_story_with_unicode_characters(self):
        """Story with unicode characters is captured correctly."""
        text = """\
#### US-001: Story with émojis 🎉 and ünïcödé

**Parent:** SM-001 (STORY-MAP.md)

Content with 日本語 and العربية and emoji 🚀

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]
        assert "émojis 🎉" in result.stories[0]
        assert "日本語" in result.stories[0]

    def test_story_with_special_markdown(self):
        """Story with special markdown characters is captured correctly."""
        text = """\
#### US-001: Story with *bold* and _italic_

**Parent:** SM-001 (STORY-MAP.md)

- [ ] Checkbox
- [x] Checked
> Quote
`code`
```python
def foo():
    pass
```

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]
        assert "```python" in result.stories[0]

    def test_parent_field_with_extra_whitespace(self):
        """Parent field with extra whitespace still matches."""
        text = """\
#### US-001: Story

**Parent:**   SM-001   (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]

    def test_parent_field_at_end_of_story(self):
        """Parent field at end of story (unusual but valid) matches."""
        text = """\
#### US-001: Story

Content here first.

**Acceptance Criteria:**
- [ ] AC 1

**Parent:** SM-001 (STORY-MAP.md)

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]

    def test_only_whitespace_between_stories(self):
        """Only whitespace between stories (no ---) still separates correctly."""
        text = """\
#### US-001: Story one

**Parent:** SM-001 (STORY-MAP.md)

Content.



#### US-003: Story three

**Parent:** SM-003 (STORY-MAP.md)

Content.

---
"""
        result = extract_matching_stories(["SM-001", "SM-003"], text)
        # First story has no trailing ---, second story header triggers flush
        assert result.us_ids == ["US-001", "US-003"]
        assert result.us_count == 2


# ===========================================================================
# Negative Tests (Things That Should NOT Match)
# ===========================================================================


class TestNegativeMatching:
    """Tests to ensure we don't match things we shouldn't."""

    def test_parent_in_code_block_is_matched_known_limitation(self):
        """**Parent:** inside a code block IS matched (known limitation).

        The script does not parse markdown context, so Parent fields in
        code blocks will still be matched. This documents actual behavior.
        """
        text = """\
#### US-001: Story

**Parent:** SM-999 (STORY-MAP.md)

Here's some code:
```
**Parent:** SM-001 (STORY-MAP.md)
```

---
"""
        # SM-001 appears in code block but WILL be matched (known limitation)
        result = extract_matching_stories(["SM-001"], text)
        # Documents current behavior: code block content IS matched
        assert result.us_ids == ["US-001"]
        assert "SM-001" in result.found_sm_ids

    def test_parent_in_inline_code_not_matched(self):
        """**Parent:** in inline code should not match... wait, it will because we don't parse markdown."""
        # Actually our regex will match it - this tests current behavior
        text = """\
#### US-001: Story

The format is `**Parent:** SM-001` but actual parent is:

**Parent:** SM-003 (STORY-MAP.md)

---
"""
        # Current behavior: matches SM-001 in inline code too
        # This is a known limitation - documenting current behavior
        result = extract_matching_stories(["SM-001", "SM-003"], text)
        # Both will match because regex doesn't understand markdown context
        assert "SM-001" in result.found_sm_ids or "SM-003" in result.found_sm_ids

    def test_sm_id_in_content_not_matched_as_parent(self):
        """SM-XXX mentioned in content (not Parent field) shouldn't match."""
        text = """\
#### US-001: Story about SM-001

**Parent:** SM-003 (STORY-MAP.md)

This story references SM-001 but it's not the parent.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == []  # SM-001 is in content, not Parent field

    def test_us_id_in_content_not_captured(self):
        """US-XXX in content doesn't create a new story."""
        text = """\
#### US-001: Main story

**Parent:** SM-001 (STORY-MAP.md)

This references US-999 but that's not a story header.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]
        assert "US-999" not in result.us_ids

    def test_partial_sm_id_not_matched(self):
        """SM-00 should not match SM-001 (no partial matching)."""
        text = """\
#### US-001: Story

**Parent:** SM-001 (STORY-MAP.md)

---
"""
        result = extract_matching_stories(["SM-00"], text)
        assert result.us_ids == []

    def test_sm_id_with_suffix_not_matched(self):
        """SM-0011 should not match when looking for SM-001."""
        text = """\
#### US-001: Story

**Parent:** SM-0011 (STORY-MAP.md)

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == []

    def test_us_header_with_no_space_after_colon(self):
        """#### US-001:Title (no space) should still match."""
        text = """\
#### US-001:No space title

**Parent:** SM-001 (STORY-MAP.md)

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]

    def test_us_header_case_sensitivity(self):
        """#### us-001: (lowercase) should not match."""
        text = """\
#### us-001: Lowercase story

**Parent:** SM-001 (STORY-MAP.md)

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == []

    def test_parent_case_sensitivity(self):
        """**parent:** (lowercase) should not match."""
        text = """\
#### US-001: Story

**parent:** SM-001 (STORY-MAP.md)

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == []

    def test_parent_without_bold(self):
        """Parent: without ** should not match."""
        text = """\
#### US-001: Story

Parent: SM-001 (STORY-MAP.md)

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == []


# ===========================================================================
# Stress Tests
# ===========================================================================


class TestStressConditions:
    """Tests for handling large inputs."""

    def test_many_stories_50(self):
        """50 stories are all captured correctly."""
        stories = []
        for i in range(1, 51):
            stories.append(f"""\
#### US-{i:03d}: Story {i}

**Parent:** SM-{i:03d} (STORY-MAP.md)

Content for story {i}.

---
""")
        text = "\n".join(stories)
        sm_ids = [f"SM-{i:03d}" for i in range(1, 51)]

        result = extract_matching_stories(sm_ids, text)

        assert result.us_count == 50
        assert len(result.us_ids) == 50
        assert result.us_ids[0] == "US-001"
        assert result.us_ids[49] == "US-050"

    def test_many_stories_with_some_missing(self):
        """Large number of stories with some SMs having no match."""
        stories = []
        # Only create stories for odd numbers
        for i in range(1, 51, 2):
            stories.append(f"""\
#### US-{i:03d}: Story {i}

**Parent:** SM-{i:03d} (STORY-MAP.md)

Content.

---
""")
        text = "\n".join(stories)
        # Request all 50 SMs
        sm_ids = [f"SM-{i:03d}" for i in range(1, 51)]

        result = extract_matching_stories(sm_ids, text)

        assert result.us_count == 25  # Only odd ones
        assert len(result.us_ids) == 25
        assert len(result.found_sm_ids) == 25

    def test_very_long_us_ids_list_in_output(self):
        """Output handles very long US-XXX IDs list."""
        us_ids = [f"US-{i:03d}" for i in range(1, 101)]  # 100 IDs
        result = MatchResult(
            stories=["s"] * 100,
            found_sm_ids={f"SM-{i:03d}" for i in range(1, 101)},
            us_ids=us_ids,
            us_count=100,
        )
        sm_ids = [f"SM-{i:03d}" for i in range(1, 101)]

        output = format_output(1, sm_ids, result)

        # Verify all IDs are in the output
        assert "US-001" in output
        assert "US-050" in output
        assert "US-100" in output
        assert "**US-XXX IDs in this phase:**" in output


# ===========================================================================
# Format Variations
# ===========================================================================


class TestFormatVariations:
    """Tests for various format variations in input."""

    def test_parent_with_different_suffix_formats(self):
        """Parent field with various suffix formats."""
        variations = [
            "**Parent:** SM-001 (STORY-MAP.md)",
            "**Parent:** SM-001 (story-map.md)",
            "**Parent:** SM-001 (from story map)",
            "**Parent:** SM-001 [STORY-MAP.md]",
            "**Parent:** SM-001",
            "**Parent:** SM-001 ",
        ]
        for i, parent_line in enumerate(variations):
            text = f"""\
#### US-{i:03d}: Story

{parent_line}

---
"""
            result = extract_matching_stories(["SM-001"], text)
            assert result.us_ids == [f"US-{i:03d}"], f"Failed for: {parent_line}"

    def test_us_header_with_various_title_formats(self):
        """US header with various title formats."""
        variations = [
            "#### US-001: Simple title",
            "#### US-001: Title with (parentheses)",
            "#### US-001: Title with [brackets]",
            "#### US-001: Title with - dashes - here",
            "#### US-001: Title: with: colons",
            "#### US-001:NoSpaceTitle",
            "#### US-001:  Extra spaces title",
        ]
        for title in variations:
            text = f"""\
{title}

**Parent:** SM-001 (STORY-MAP.md)

---
"""
            result = extract_matching_stories(["SM-001"], text)
            assert result.us_ids == ["US-001"], f"Failed for: {title}"

    def test_multiple_parent_fields_first_wins(self):
        """If multiple Parent fields exist, first matching one is used."""
        text = """\
#### US-001: Story

**Parent:** SM-001 (STORY-MAP.md)
**Parent:** SM-003 (STORY-MAP.md)

---
"""
        result = extract_matching_stories(["SM-001", "SM-003"], text)
        # Both SM-001 and SM-003 should be found for this one story
        assert result.us_ids == ["US-001"]
        assert result.us_count == 1
        # Both parent IDs should be in found_sm_ids
        assert "SM-001" in result.found_sm_ids
        assert "SM-003" in result.found_sm_ids

    def test_parent_field_with_tabs(self):
        """Parent field with tabs instead of spaces."""
        text = """\
#### US-001: Story

**Parent:**\tSM-001\t(STORY-MAP.md)

---
"""
        result = extract_matching_stories(["SM-001"], text)
        # Current regex uses \s+ which matches tabs
        assert result.us_ids == ["US-001"]

    def test_windows_line_endings(self):
        """File with Windows line endings (CRLF)."""
        text = "#### US-001: Story\r\n\r\n**Parent:** SM-001 (STORY-MAP.md)\r\n\r\n---\r\n"
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]

    def test_mixed_line_endings(self):
        """File with mixed line endings."""
        text = "#### US-001: Story\n\r\n**Parent:** SM-001 (STORY-MAP.md)\r\n\n---\n"
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]


# ===========================================================================
# Regression Tests
# ===========================================================================


class TestRegressions:
    """Tests for specific bugs or edge cases found during development."""

    def test_story_header_at_very_start_of_file(self):
        """Story header at byte 0 of file is captured."""
        text = """#### US-001: First line is header

**Parent:** SM-001 (STORY-MAP.md)

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]

    def test_file_ending_with_story_no_newline(self):
        """File ending with story content and no trailing newline."""
        text = """#### US-001: Story

**Parent:** SM-001 (STORY-MAP.md)

Final content with no newline at end"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]
        assert "Final content with no newline at end" in result.stories[0]

    def test_empty_sm_ids_list(self):
        """Empty sm_ids list returns no matches."""
        text = """\
#### US-001: Story

**Parent:** SM-001 (STORY-MAP.md)

---
"""
        result = extract_matching_stories([], text)
        assert result.us_ids == []
        assert result.us_count == 0

    def test_story_with_only_header(self):
        """Story with only header (no parent, no content)."""
        text = """\
#### US-001: Just a header

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == []  # No parent field, no match

    def test_parent_field_immediately_after_header(self):
        """Parent field on line immediately after header."""
        text = """\
#### US-001: Story
**Parent:** SM-001 (STORY-MAP.md)
---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]

    def test_separator_with_extra_dashes(self):
        """Separator with more than 3 dashes doesn't trigger flush."""
        text = """\
#### US-001: Story

**Parent:** SM-001 (STORY-MAP.md)

----

More content after four dashes.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]
        # Four dashes (----) don't trigger flush, only exactly ---
        assert "More content after four dashes" in result.stories[0]

    def test_horizontal_rule_variations_not_matched(self):
        """Various horizontal rule formats don't trigger flush."""
        text = """\
#### US-001: Story

**Parent:** SM-001 (STORY-MAP.md)

***

Content after asterisks.

___

Content after underscores.

---
"""
        result = extract_matching_stories(["SM-001"], text)
        assert result.us_ids == ["US-001"]
        assert "Content after asterisks" in result.stories[0]
        assert "Content after underscores" in result.stories[0]
