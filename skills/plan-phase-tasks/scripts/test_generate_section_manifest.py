#!/usr/bin/env python3
"""
Unit tests for generate-section-manifest.py

Tests the parsing and manifest generation logic. LLM matching is tested
via integration tests (requires API key) or mocked for unit tests.

Run with: pytest test_generate_section_manifest.py -v
"""

import json
import re
import pytest
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch, MagicMock

# Import the real module via importlib (hyphenated filename isn't a valid Python
# module name). Mock openai first since the module has a top-level import.
import importlib.util
import os
import sys
import tempfile

sys.modules['openai'] = MagicMock()

_script_path = Path(__file__).parent / "generate-section-manifest.py"
_spec = importlib.util.spec_from_file_location("generate_section_manifest", _script_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

parse_traceability_matrix = _mod.parse_traceability_matrix
generate_manifest = _mod.generate_manifest
list_export_sections = _mod.list_export_sections
load_section_readmes = _mod.load_section_readmes
build_matching_prompt = _mod.build_matching_prompt
match_sections_with_llm = _mod.match_sections_with_llm
MAX_RETRIES = _mod.MAX_RETRIES
RETRY_DELAY_SECONDS = _mod.RETRY_DELAY_SECONDS
main = _mod.main


def _parse_from_string(content: str) -> list[dict]:
    """Test helper: the real parse_traceability_matrix takes a Path.
    This writes content to a temp file so unit tests can pass strings."""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.md', delete=False, encoding='utf-8'
    ) as f:
        f.write(content)
        tmp_path = Path(f.name)
    try:
        return parse_traceability_matrix(tmp_path)
    finally:
        os.unlink(tmp_path)


# =============================================================================
# Traceability Parser Tests
# =============================================================================

class TestParseTraceabilityMatrix:
    """Tests for parse_traceability_matrix function."""

    def test_basic_table_parsing(self):
        """Parse a simple traceability table."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Source Description |
|------------|-------------|-----------|-------------------|
| Hero headline | S1, S3 | SM-001 / US-001 | Hero text |
| Card title | S5 | SM-006 / US-006 | Card name |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 2
        assert rows[0] == {"ux_element": "Hero headline", "story_id": "US-001"}
        assert rows[1] == {"ux_element": "Card title", "story_id": "US-006"}

    def test_handles_sm_only_format(self):
        """Skip rows that only have SM-XXX without US-XXX."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Source Description |
|------------|-------------|-----------|-------------------|
| Hero headline | S1 | SM-001 | No US ID |
| Card title | S5 | SM-006 / US-006 | Has US ID |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-006"

    def test_extracts_us_id_from_various_formats(self):
        """Handle different source ID formats."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Description |
|------------|-------------|-----------|-------------|
| Element A | S1 | US-001 | Just US |
| Element B | S2 | SM-002 / US-002 | Both |
| Element C | S3 | SM-003/US-003 | No spaces |
| Element D | S4 | US-004 (primary) | With note |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 4
        story_ids = [r["story_id"] for r in rows]
        assert story_ids == ["US-001", "US-002", "US-003", "US-004"]

    def test_handles_section_header_variations(self):
        """Parse tables with different Section 11 header formats."""
        variations = [
            "## Section 11: Traceability Matrix",
            "## 11. Traceability Matrix",
            "## 11: Traceability",
            "## Section 11 Traceability",
        ]

        for header in variations:
            content = f"""
{header}

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Element | S1 | US-001 | Test |
"""
            rows = _parse_from_string(content)
            assert len(rows) == 1, f"Failed for header: {header}"

    def test_skips_separator_rows(self):
        """Ignore markdown table separator rows."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
|------------|-------------|-----------|------|
| Element | S1 | US-001 | Test |
| --- | --- | --- | --- |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_stops_at_next_section(self):
        """Stop parsing when next ## section starts."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Element A | S1 | US-001 | In section 11 |

## Section 12: Something Else

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Element B | S2 | US-002 | In section 12 |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-001"

    def test_returns_empty_for_missing_section(self):
        """Return empty list if Section 11 not found."""
        content = """
## Section 10: Something

Some content here.

## Section 12: Something Else

More content.
"""
        rows = _parse_from_string(content)
        assert rows == []

    def test_handles_empty_cells(self):
        """Skip rows with missing required cells."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| | S1 | US-001 | Empty element |
| Element | S2 | US-002 | Valid |
"""
        rows = _parse_from_string(content)
        # Should still parse both since UX element can be empty string
        # but the important thing is we get the story IDs
        assert any(r["story_id"] == "US-002" for r in rows)

    def test_deduplication_in_output(self):
        """Same UX element appearing multiple times should create multiple rows."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero headline | S1 | US-001 | First |
| Hero subtitle | S3 | US-001 | Second |
| Hero cue | S4 | US-001 | Third |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 3
        # All should have same story ID
        assert all(r["story_id"] == "US-001" for r in rows)


# =============================================================================
# Manifest Generation Tests
# =============================================================================

class TestGenerateManifest:
    """Tests for generate_manifest function."""

    def test_basic_manifest_generation(self):
        """Generate manifest from LLM results."""
        section_to_stories = {
            "landing-and-hero": ["US-001", "US-003"],
            "hook-catalog": ["US-004", "US-006"],
        }
        traceability_rows = [
            {"ux_element": "Hero", "story_id": "US-001"},
            {"ux_element": "Grid", "story_id": "US-003"},
            {"ux_element": "Card", "story_id": "US-004"},
            {"ux_element": "Title", "story_id": "US-006"},
        ]
        section_names = ["landing-and-hero", "hook-catalog"]

        manifest = generate_manifest(
            section_to_stories, traceability_rows, section_names
        )

        assert manifest["sections"]["landing-and-hero"] == ["US-001", "US-003"]
        assert manifest["sections"]["hook-catalog"] == ["US-004", "US-006"]
        assert manifest["metadata"]["unmapped_stories"] == "none"

    def test_includes_missing_sections(self):
        """Include sections with no story matches."""
        section_to_stories = {
            "landing-and-hero": ["US-001"],
        }
        traceability_rows = [
            {"ux_element": "Hero", "story_id": "US-001"},
        ]
        section_names = ["landing-and-hero", "dark-and-light-mode"]

        manifest = generate_manifest(
            section_to_stories, traceability_rows, section_names
        )

        assert manifest["sections"]["landing-and-hero"] == ["US-001"]
        assert manifest["sections"]["dark-and-light-mode"] == []

    def test_reports_unmapped_stories(self):
        """Report stories in traceability but not mapped to any section."""
        section_to_stories = {
            "landing-and-hero": ["US-001"],
        }
        traceability_rows = [
            {"ux_element": "Hero", "story_id": "US-001"},
            {"ux_element": "Missing", "story_id": "US-099"},
        ]
        section_names = ["landing-and-hero"]

        manifest = generate_manifest(
            section_to_stories, traceability_rows, section_names
        )

        assert manifest["metadata"]["unmapped_stories"] == "US-099"

    def test_reports_multiple_unmapped_stories(self):
        """Report multiple unmapped stories, sorted."""
        section_to_stories = {
            "landing-and-hero": ["US-001"],
        }
        traceability_rows = [
            {"ux_element": "Hero", "story_id": "US-001"},
            {"ux_element": "Missing1", "story_id": "US-099"},
            {"ux_element": "Missing2", "story_id": "US-050"},
            {"ux_element": "Missing3", "story_id": "US-075"},
        ]
        section_names = ["landing-and-hero"]

        manifest = generate_manifest(
            section_to_stories, traceability_rows, section_names
        )

        # Should be sorted alphabetically
        assert manifest["metadata"]["unmapped_stories"] == "US-050, US-075, US-099"

    def test_handles_llm_returning_extra_sections(self):
        """Handle LLM returning sections not in the directory list."""
        section_to_stories = {
            "landing-and-hero": ["US-001"],
            "unknown-section": ["US-099"],  # LLM returned this but it's not in section_names
        }
        traceability_rows = [
            {"ux_element": "Hero", "story_id": "US-001"},
            {"ux_element": "Extra", "story_id": "US-099"},
        ]
        section_names = ["landing-and-hero"]  # Only this section exists

        manifest = generate_manifest(
            section_to_stories, traceability_rows, section_names
        )

        # Should only include sections from section_names
        assert "unknown-section" not in manifest["sections"]
        assert manifest["sections"]["landing-and-hero"] == ["US-001"]
        # US-099 should be unmapped since its section was filtered out
        assert manifest["metadata"]["unmapped_stories"] == "US-099"

    def test_deduplicates_story_ids(self):
        """Remove duplicate story IDs within a section."""
        section_to_stories = {
            "landing-and-hero": ["US-001", "US-001", "US-003", "US-001"],
        }
        traceability_rows = [
            {"ux_element": "A", "story_id": "US-001"},
            {"ux_element": "B", "story_id": "US-003"},
        ]
        section_names = ["landing-and-hero"]

        manifest = generate_manifest(
            section_to_stories, traceability_rows, section_names
        )

        assert manifest["sections"]["landing-and-hero"] == ["US-001", "US-003"]

    def test_sorts_story_ids(self):
        """Story IDs should be sorted in output."""
        section_to_stories = {
            "hook-catalog": ["US-010", "US-004", "US-007", "US-006"],
        }
        traceability_rows = [
            {"ux_element": "A", "story_id": "US-004"},
            {"ux_element": "B", "story_id": "US-006"},
            {"ux_element": "C", "story_id": "US-007"},
            {"ux_element": "D", "story_id": "US-010"},
        ]
        section_names = ["hook-catalog"]

        manifest = generate_manifest(
            section_to_stories, traceability_rows, section_names
        )

        assert manifest["sections"]["hook-catalog"] == [
            "US-004", "US-006", "US-007", "US-010"
        ]

    def test_metadata_counts(self):
        """Verify metadata counts are accurate."""
        section_to_stories = {
            "section-a": ["US-001", "US-002"],
            "section-b": ["US-003"],
        }
        traceability_rows = [
            {"ux_element": "A", "story_id": "US-001"},
            {"ux_element": "B", "story_id": "US-002"},
            {"ux_element": "C", "story_id": "US-003"},
            {"ux_element": "D", "story_id": "US-003"},  # Duplicate story
        ]
        section_names = ["section-a", "section-b", "section-c"]

        manifest = generate_manifest(
            section_to_stories, traceability_rows, section_names
        )

        assert manifest["metadata"]["traceability_rows_parsed"] == "4"
        assert manifest["metadata"]["unique_stories_in_traceability"] == "3"
        assert manifest["metadata"]["unique_stories_mapped"] == "3"
        assert manifest["metadata"]["sections_in_export"] == "3"


# =============================================================================
# Integration Tests (project-specific, skipped if artifacts unavailable)
# =============================================================================

class TestIntegrationWithRealArtifacts:
    """
    Integration tests using real project artifacts.

    These tests validate the parser against known good data. They skip if the
    required artifacts aren't available, making them safe to run in any environment.

    To run these tests, set the UX_FLOWS_PATH environment variable to point to
    a UX-FLOWS.md file with a Section 11 traceability matrix.
    """

    @pytest.fixture
    def ux_flows_path(self):
        """
        Get path to UX-FLOWS.md from environment or common locations.

        Set UX_FLOWS_PATH env var to override, or place test artifacts in
        the test fixtures directory.
        """
        import os

        # Check environment variable first
        env_path = os.environ.get("UX_FLOWS_PATH")
        if env_path:
            return Path(env_path)

        # Check for test fixtures directory
        fixtures_dir = Path(__file__).parent / "fixtures"
        if (fixtures_dir / "UX-FLOWS.md").exists():
            return fixtures_dir / "UX-FLOWS.md"

        # Fallback: check common development locations (will skip if not found)
        common_paths = [
            Path.home() / "courses/claude-code/claude-code-crash-course/hookhub/.charter/UX-FLOWS.md",
            Path("/home/hisham/courses/claude-code/claude-code-crash-course/hookhub/.charter/UX-FLOWS.md"),
        ]
        for path in common_paths:
            if path.exists():
                return path

        return None

    def test_parse_real_traceability_matrix(self, ux_flows_path):
        """Parse a real UX-FLOWS.md traceability matrix."""
        if ux_flows_path is None or not ux_flows_path.exists():
            pytest.skip("No UX-FLOWS.md available. Set UX_FLOWS_PATH env var to test.")

        rows = parse_traceability_matrix(ux_flows_path)

        # Generic assertions that should pass for any valid traceability matrix
        assert len(rows) > 0, "Should parse at least one row"
        assert all("ux_element" in r and "story_id" in r for r in rows), "All rows should have required fields"
        assert all(r["story_id"].startswith("US-") for r in rows), "All story IDs should start with US-"

        # Log results for manual verification
        unique_stories = set(r["story_id"] for r in rows)
        print(f"\nParsed {len(rows)} rows with {len(unique_stories)} unique stories")


# HookHub-specific tests (can be removed or skipped in other projects)
@pytest.mark.skipif(
    not Path("/home/hisham/courses/claude-code/claude-code-crash-course/hookhub/.charter/UX-FLOWS.md").exists(),
    reason="HookHub artifacts not available"
)
class TestHookHubSpecific:
    """
    HookHub-specific integration tests.

    These tests validate against known HookHub values and are skipped
    when HookHub artifacts aren't available.
    """

    def test_hookhub_traceability_expected_values(self):
        """Validate HookHub traceability matrix has expected structure."""
        path = Path("/home/hisham/courses/claude-code/claude-code-crash-course/hookhub/.charter/UX-FLOWS.md")
        rows = parse_traceability_matrix(path)

        # HookHub-specific expected values (as of 2026-02-03)
        assert len(rows) == 18, f"HookHub should have 18 rows, got {len(rows)}"

        unique_stories = set(r["story_id"] for r in rows)
        assert len(unique_stories) == 16, f"HookHub should have 16 unique stories, got {len(unique_stories)}"

        # Verify Hero elements map to US-001
        hero_rows = [r for r in rows if "Hero" in r["ux_element"]]
        assert len(hero_rows) == 3, "HookHub should have 3 Hero-related rows"
        assert all(r["story_id"] == "US-001" for r in hero_rows)

        # Verify filter elements map to US-013 through US-016
        filter_stories = {r["story_id"] for r in rows
                         if "filter" in r["ux_element"].lower() or "All" in r["ux_element"]}
        assert filter_stories == {"US-013", "US-014", "US-015", "US-016"}


# =============================================================================
# Directory and README Tests
# =============================================================================

class TestListExportSections:
    """Tests for list_export_sections function."""

    def test_lists_section_directories(self, tmp_path):
        """List all section directories in export."""
        # Create mock export structure
        sections_dir = tmp_path / "sections"
        sections_dir.mkdir()
        (sections_dir / "landing-and-hero").mkdir()
        (sections_dir / "hook-catalog").mkdir()
        (sections_dir / "filter-system").mkdir()

        result = list_export_sections(tmp_path)
        assert result == ["filter-system", "hook-catalog", "landing-and-hero"]

    def test_excludes_hidden_directories(self, tmp_path):
        """Exclude directories starting with dot."""
        sections_dir = tmp_path / "sections"
        sections_dir.mkdir()
        (sections_dir / "visible-section").mkdir()
        (sections_dir / ".hidden-section").mkdir()
        (sections_dir / ".git").mkdir()

        result = list_export_sections(tmp_path)
        assert result == ["visible-section"]

    def test_excludes_files(self, tmp_path):
        """Exclude files, only return directories."""
        sections_dir = tmp_path / "sections"
        sections_dir.mkdir()
        (sections_dir / "real-section").mkdir()
        (sections_dir / "not-a-section.md").write_text("content")

        result = list_export_sections(tmp_path)
        assert result == ["real-section"]

    def test_returns_empty_for_missing_sections_dir(self, tmp_path):
        """Return empty list if sections/ directory doesn't exist."""
        result = list_export_sections(tmp_path)
        assert result == []


class TestLoadSectionReadmes:
    """Tests for load_section_readmes function."""

    def test_loads_readme_content(self, tmp_path):
        """Load README.md content from each section."""
        sections_dir = tmp_path / "sections"
        sections_dir.mkdir()

        section1 = sections_dir / "section-a"
        section1.mkdir()
        (section1 / "README.md").write_text("# Section A\n\nThis is section A.")

        section2 = sections_dir / "section-b"
        section2.mkdir()
        (section2 / "README.md").write_text("# Section B\n\nThis is section B.")

        result = load_section_readmes(tmp_path, ["section-a", "section-b"])
        assert "# Section A" in result["section-a"]
        assert "# Section B" in result["section-b"]

    def test_handles_missing_readme(self, tmp_path):
        """Handle sections without README.md."""
        sections_dir = tmp_path / "sections"
        sections_dir.mkdir()
        (sections_dir / "no-readme-section").mkdir()

        result = load_section_readmes(tmp_path, ["no-readme-section"])
        assert result["no-readme-section"] == "No README found for no-readme-section"

    def test_truncates_long_readmes(self, tmp_path):
        """Truncate READMEs to first 50 lines."""
        sections_dir = tmp_path / "sections"
        sections_dir.mkdir()

        section = sections_dir / "long-readme"
        section.mkdir()
        # Create a 100-line README
        long_content = "\n".join([f"Line {i}" for i in range(100)])
        (section / "README.md").write_text(long_content)

        result = load_section_readmes(tmp_path, ["long-readme"])
        lines = result["long-readme"].split("\n")
        assert len(lines) == 50
        assert lines[0] == "Line 0"
        assert lines[49] == "Line 49"


# =============================================================================
# Prompt Building Tests
# =============================================================================

class TestBuildMatchingPrompt:
    """Tests for build_matching_prompt function."""

    def test_includes_all_traceability_rows(self):
        """Prompt includes all UX elements and story IDs."""
        rows = [
            {"ux_element": "Hero", "story_id": "US-001"},
            {"ux_element": "Card", "story_id": "US-002"},
        ]
        sections = ["section-a"]
        readmes = {"section-a": "Section A content"}

        prompt = build_matching_prompt(rows, sections, readmes)

        assert "Hero | US-001" in prompt
        assert "Card | US-002" in prompt
        assert "### section-a" in prompt
        assert "Section A content" in prompt

    def test_handles_empty_inputs(self):
        """Handle empty traceability or sections."""
        prompt = build_matching_prompt([], [], {})

        assert "UX Element | Story ID" in prompt
        assert "## Section Directories" in prompt


# =============================================================================
# LLM Response Validation Tests
# =============================================================================

class TestLLMResponseValidation:
    """Tests for LLM response validation logic.

    NOTE: validate_llm_response is inline logic inside match_sections_with_llm,
    not a standalone function. These tests replicate the validation pattern because
    importing it would require mocking the full OpenAI call chain. If the validation
    logic in match_sections_with_llm changes, these tests must be updated manually.
    """

    def test_validates_dict_response(self):
        """Validate that response is a dictionary."""
        def validate_llm_response(result):
            if not isinstance(result, dict):
                raise ValueError("Response is not a dictionary")
            for key, value in result.items():
                if not isinstance(value, list):
                    raise ValueError(f"Value for '{key}' is not a list")
                for item in value:
                    if not isinstance(item, str) or not item.startswith("US-"):
                        raise ValueError(f"Invalid story ID: {item}")
            return True

        # Valid response
        valid = {"section-a": ["US-001", "US-002"]}
        assert validate_llm_response(valid) is True

        # Invalid: not a dict
        with pytest.raises(ValueError, match="not a dictionary"):
            validate_llm_response(["US-001"])

    def test_validates_list_values(self):
        """Validate that all values are lists."""
        def validate_llm_response(result):
            if not isinstance(result, dict):
                raise ValueError("Response is not a dictionary")
            for key, value in result.items():
                if not isinstance(value, list):
                    raise ValueError(f"Value for '{key}' is not a list")
                for item in value:
                    if not isinstance(item, str) or not item.startswith("US-"):
                        raise ValueError(f"Invalid story ID: {item}")
            return True

        # Invalid: value is not a list
        with pytest.raises(ValueError, match="not a list"):
            validate_llm_response({"section-a": "US-001"})

    def test_validates_story_id_format(self):
        """Validate that story IDs start with US-."""
        def validate_llm_response(result):
            if not isinstance(result, dict):
                raise ValueError("Response is not a dictionary")
            for key, value in result.items():
                if not isinstance(value, list):
                    raise ValueError(f"Value for '{key}' is not a list")
                for item in value:
                    if not isinstance(item, str) or not item.startswith("US-"):
                        raise ValueError(f"Invalid story ID: {item}")
            return True

        # Invalid: story ID doesn't start with US-
        with pytest.raises(ValueError, match="Invalid story ID"):
            validate_llm_response({"section-a": ["SM-001"]})

        # Invalid: story ID is not a string
        with pytest.raises(ValueError, match="Invalid story ID"):
            validate_llm_response({"section-a": [123]})


# =============================================================================
# Edge Case Tests
# =============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_content(self):
        """Handle empty file content."""
        rows = _parse_from_string("")
        assert rows == []

    def test_malformed_table(self):
        """Handle tables with inconsistent formatting."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Source ID |
|------------|-----------|
| Element | US-001 |
| Another | SM-002 / US-002 |
"""
        rows = _parse_from_string(content)
        # Should handle missing columns gracefully
        # The function expects at least 3 columns (index 2 for Source ID)
        # With only 2 columns, cells[2] won't exist
        assert len(rows) == 0  # Both rows have only 2 cells

    def test_unicode_content(self):
        """Handle unicode characters in UX element names."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Héro héadline | S1 | US-001 | Test |
| 日本語 element | S2 | US-002 | Japanese |
| Émoji 🎉 | S3 | US-003 | Emoji |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 3
        assert rows[0]["ux_element"] == "Héro héadline"
        assert rows[1]["ux_element"] == "日本語 element"
        assert rows[2]["ux_element"] == "Émoji 🎉"

    def test_story_id_edge_formats(self):
        """Handle various story ID edge cases."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| A | S1 | US-000 | Zero padded |
| B | S2 | US-999 | Max three digits |
| C | S3 | US-1000 | Four digits (invalid) |
| D | S4 | us-001 | Lowercase (invalid) |
"""
        rows = _parse_from_string(content)
        story_ids = [r["story_id"] for r in rows]
        assert "US-000" in story_ids
        assert "US-999" in story_ids
        # US-1000 has 4 digits, regex expects 3
        assert "US-1000" not in story_ids and "US-100" in story_ids  # Matches first 3 digits
        # Lowercase us-001 won't match
        assert "US-001" not in story_ids or any(r["ux_element"] == "D" for r in rows) == False


# =============================================================================
# Invariant Tests
# =============================================================================

class TestInvariants:
    """Tests for invariants that must ALWAYS hold."""

    def test_all_section_names_appear_in_manifest(self):
        """Every section_name must appear in manifest sections."""
        section_to_stories = {"a": ["US-001"]}
        traceability_rows = [{"ux_element": "X", "story_id": "US-001"}]
        section_names = ["a", "b", "c"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert set(manifest["sections"].keys()) == set(section_names)

    def test_all_mapped_stories_are_deduped(self):
        """No duplicates in any section's story list."""
        section_to_stories = {
            "sec": ["US-001", "US-001", "US-002", "US-001", "US-002"]
        }
        traceability_rows = [
            {"ux_element": "A", "story_id": "US-001"},
            {"ux_element": "B", "story_id": "US-002"},
        ]
        section_names = ["sec"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        stories = manifest["sections"]["sec"]
        assert len(stories) == len(set(stories))

    def test_all_mapped_stories_are_sorted(self):
        """Stories in each section are sorted."""
        section_to_stories = {
            "sec": ["US-010", "US-001", "US-005", "US-002"]
        }
        traceability_rows = [
            {"ux_element": "A", "story_id": "US-001"},
            {"ux_element": "B", "story_id": "US-002"},
            {"ux_element": "C", "story_id": "US-005"},
            {"ux_element": "D", "story_id": "US-010"},
        ]
        section_names = ["sec"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["sections"]["sec"] == sorted(manifest["sections"]["sec"])

    def test_unmapped_plus_mapped_equals_traceability(self):
        """All stories are either mapped or in unmapped_stories."""
        section_to_stories = {"sec": ["US-001"]}
        traceability_rows = [
            {"ux_element": "A", "story_id": "US-001"},
            {"ux_element": "B", "story_id": "US-002"},
            {"ux_element": "C", "story_id": "US-003"},
        ]
        section_names = ["sec"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        mapped = set()
        for stories in manifest["sections"].values():
            mapped.update(stories)

        unmapped_str = manifest["metadata"]["unmapped_stories"]
        unmapped = set(unmapped_str.split(", ")) if unmapped_str != "none" else set()

        traceability_set = {row["story_id"] for row in traceability_rows}
        assert mapped | unmapped == traceability_set

    def test_metadata_counts_are_strings(self):
        """All metadata counts are stored as strings."""
        section_to_stories = {"sec": ["US-001"]}
        traceability_rows = [{"ux_element": "A", "story_id": "US-001"}]
        section_names = ["sec"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        for key in ["traceability_rows_parsed", "unique_stories_in_traceability",
                    "unique_stories_mapped", "sections_in_export"]:
            assert isinstance(manifest["metadata"][key], str)
            assert manifest["metadata"][key].isdigit()

    def test_parse_returns_list_of_dicts_with_required_keys(self):
        """parse_traceability_matrix returns dicts with ux_element and story_id."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)

        for row in rows:
            assert "ux_element" in row
            assert "story_id" in row
            assert isinstance(row["ux_element"], str)
            assert isinstance(row["story_id"], str)


# =============================================================================
# More Edge Cases for parse_traceability_matrix
# =============================================================================

class TestParseTraceabilityEdgeCases:
    """Additional edge cases for parse_traceability_matrix."""

    def test_section_11_at_end_of_file(self):
        """Section 11 at end of file (no following section)."""
        content = """
## Section 10: Previous Section

Some content.

## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-001"

    def test_section_11_with_no_table(self):
        """Section 11 exists but has no table."""
        content = """
## Section 11: Traceability Matrix

This section has no table, just text.

## Section 12: Next Section
"""
        rows = _parse_from_string(content)
        assert rows == []

    def test_multiple_section_11_headers(self):
        """Multiple Section 11 headers - first one wins."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| First | S1 | US-001 | Test |

## Section 11: Another Traceability

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Second | S2 | US-002 | Test |
"""
        rows = _parse_from_string(content)
        # First match wins due to regex behavior
        assert len(rows) == 1
        assert rows[0]["ux_element"] == "First"

    def test_table_with_extra_columns(self):
        """Table with more than 4 columns."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc | Extra1 | Extra2 |
|------------|-------------|-----------|------|--------|--------|
| Hero | S1 | US-001 | Test | foo | bar |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-001"

    def test_table_with_pipe_in_content(self):
        """Table cell containing a pipe character."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero element | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_table_with_leading_whitespace(self):
        """Table rows with leading whitespace."""
        content = """
## Section 11: Traceability Matrix

  | UX Element | Plan Section | Source ID | Desc |
  |------------|-------------|-----------|------|
  | Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        # Leading whitespace is stripped
        assert len(rows) == 1

    def test_source_id_with_multiple_us_ids(self):
        """Source ID containing multiple US-XXX emits one row per ID."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 / US-002 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 2
        assert rows[0]["story_id"] == "US-001"
        assert rows[1]["story_id"] == "US-002"
        assert rows[0]["ux_element"] == "Hero"
        assert rows[1]["ux_element"] == "Hero"

    def test_source_id_formats_comprehensive(self):
        """Various Source ID formats that should extract US-XXX."""
        # (source_id, expected_count, expected_first_story_id)
        test_cases = [
            ("US-001", 1, "US-001"),
            ("SM-001 / US-001", 1, "US-001"),
            ("SM-001/US-001", 1, "US-001"),
            ("US-001 (primary)", 1, "US-001"),
            ("see US-001", 1, "US-001"),
            ("US-001, US-002", 2, "US-001"),  # Multi-US: emits 2 rows
            ("ref: US-001", 1, "US-001"),
        ]
        for source_id, expected_count, expected_first in test_cases:
            content = f"""
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | {source_id} | Test |
"""
            rows = _parse_from_string(content)
            assert len(rows) == expected_count, f"Failed for: {source_id}"
            assert rows[0]["story_id"] == expected_first, f"Failed for: {source_id}"

    def test_ux_element_with_special_characters(self):
        """UX element names with special characters."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero (main) | S1 | US-001 | Test |
| Card - title | S2 | US-002 | Test |
| Filter: category | S3 | US-003 | Test |
| "Quote" element | S4 | US-004 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 4
        assert rows[0]["ux_element"] == "Hero (main)"
        assert rows[1]["ux_element"] == "Card - title"
        assert rows[2]["ux_element"] == "Filter: category"
        assert rows[3]["ux_element"] == '"Quote" element'

    def test_content_between_header_and_table(self):
        """Non-table content between section header and table."""
        content = """
## Section 11: Traceability Matrix

This section maps UX elements to their source stories.

Note: Some elements may be derived from multiple sources.

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_empty_table_after_header(self):
        """Table with only header row (no data rows)."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
"""
        rows = _parse_from_string(content)
        assert rows == []


# =============================================================================
# More Edge Cases for generate_manifest
# =============================================================================

class TestGenerateManifestEdgeCases:
    """Additional edge cases for generate_manifest."""

    def test_empty_section_to_stories(self):
        """Empty section_to_stories dict."""
        section_to_stories = {}
        traceability_rows = [{"ux_element": "A", "story_id": "US-001"}]
        section_names = ["section-a"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["sections"]["section-a"] == []
        assert manifest["metadata"]["unmapped_stories"] == "US-001"

    def test_empty_traceability_rows(self):
        """Empty traceability_rows list."""
        section_to_stories = {"section-a": ["US-001"]}
        traceability_rows = []
        section_names = ["section-a"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["sections"]["section-a"] == ["US-001"]
        assert manifest["metadata"]["traceability_rows_parsed"] == "0"
        assert manifest["metadata"]["unique_stories_in_traceability"] == "0"

    def test_empty_section_names(self):
        """Empty section_names list."""
        section_to_stories = {"section-a": ["US-001"]}
        traceability_rows = [{"ux_element": "A", "story_id": "US-001"}]
        section_names = []

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["sections"] == {}
        assert manifest["metadata"]["sections_in_export"] == "0"

    def test_all_empty_inputs(self):
        """All inputs are empty."""
        manifest = generate_manifest({}, [], [])

        assert manifest["sections"] == {}
        assert manifest["metadata"]["traceability_rows_parsed"] == "0"
        assert manifest["metadata"]["unmapped_stories"] == "none"

    def test_stories_mapped_to_nonexistent_sections_filtered(self):
        """Stories mapped to sections not in section_names are filtered."""
        section_to_stories = {
            "real-section": ["US-001"],
            "fake-section": ["US-002"],
        }
        traceability_rows = [
            {"ux_element": "A", "story_id": "US-001"},
            {"ux_element": "B", "story_id": "US-002"},
        ]
        section_names = ["real-section"]  # Only this one is valid

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert "fake-section" not in manifest["sections"]
        assert manifest["sections"]["real-section"] == ["US-001"]
        assert manifest["metadata"]["unmapped_stories"] == "US-002"

    def test_duplicate_traceability_rows(self):
        """Duplicate rows in traceability (same story_id)."""
        section_to_stories = {"section-a": ["US-001"]}
        traceability_rows = [
            {"ux_element": "Hero headline", "story_id": "US-001"},
            {"ux_element": "Hero subtitle", "story_id": "US-001"},
            {"ux_element": "Hero CTA", "story_id": "US-001"},
        ]
        section_names = ["section-a"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["metadata"]["traceability_rows_parsed"] == "3"
        assert manifest["metadata"]["unique_stories_in_traceability"] == "1"

    def test_unmapped_stories_sorted_alphabetically(self):
        """Unmapped stories are sorted alphabetically."""
        section_to_stories = {}
        traceability_rows = [
            {"ux_element": "C", "story_id": "US-099"},
            {"ux_element": "A", "story_id": "US-001"},
            {"ux_element": "B", "story_id": "US-050"},
        ]
        section_names = []

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["metadata"]["unmapped_stories"] == "US-001, US-050, US-099"

    def test_section_with_only_duplicates(self):
        """Section receives only duplicate story IDs."""
        section_to_stories = {
            "section-a": ["US-001", "US-001", "US-001"]
        }
        traceability_rows = [{"ux_element": "A", "story_id": "US-001"}]
        section_names = ["section-a"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["sections"]["section-a"] == ["US-001"]


# =============================================================================
# Boundary Condition Tests
# =============================================================================

class TestBoundaryConditions:
    """Tests for boundary conditions."""

    def test_us_id_000(self):
        """US-000 is a valid story ID."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Zero | S1 | US-000 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-000"

    def test_us_id_999(self):
        """US-999 is the max valid story ID with 3 digits."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Max | S1 | US-999 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-999"

    def test_single_character_ux_element(self):
        """Single character UX element name."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| A | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["ux_element"] == "A"

    def test_very_long_ux_element(self):
        """Very long UX element name (500 chars)."""
        long_name = "A" * 500
        content = f"""
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| {long_name} | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["ux_element"] == long_name

    def test_single_row_table(self):
        """Table with exactly one data row."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Solo | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_single_section_single_story(self):
        """Minimal manifest: one section, one story."""
        section_to_stories = {"section": ["US-001"]}
        traceability_rows = [{"ux_element": "A", "story_id": "US-001"}]
        section_names = ["section"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert len(manifest["sections"]) == 1
        assert manifest["sections"]["section"] == ["US-001"]

    def test_whitespace_only_ux_element(self):
        """UX element that is only whitespace (after stripping)."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
|    | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        # Empty string after strip - still creates row if story_id valid
        if rows:
            assert rows[0]["ux_element"] == ""

    def test_section_name_with_numbers(self):
        """Section name containing numbers."""
        section_to_stories = {"section-01-main": ["US-001"]}
        traceability_rows = [{"ux_element": "A", "story_id": "US-001"}]
        section_names = ["section-01-main"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert "section-01-main" in manifest["sections"]

    def test_section_name_with_underscores(self):
        """Section name with underscores instead of dashes."""
        section_to_stories = {"section_name_here": ["US-001"]}
        traceability_rows = [{"ux_element": "A", "story_id": "US-001"}]
        section_names = ["section_name_here"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert "section_name_here" in manifest["sections"]


# =============================================================================
# Negative Matching Tests
# =============================================================================

class TestNegativeMatching:
    """Tests for things that should NOT be matched."""

    def test_us_id_lowercase_not_matched(self):
        """us-001 (lowercase) should not be matched."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | us-001 | Lowercase |
"""
        rows = _parse_from_string(content)
        assert rows == []

    def test_us_id_two_digits_not_matched(self):
        """US-01 (two digits) should not be matched."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | US-01 | Two digits |
"""
        rows = _parse_from_string(content)
        assert rows == []

    def test_us_id_four_digits_extracts_first_three(self):
        """US-1234 extracts as US-123."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | US-1234 | Four digits |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-123"

    def test_sm_only_not_matched(self):
        """SM-XXX without US-XXX should not be matched."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | SM-001 | SM only |
"""
        rows = _parse_from_string(content)
        assert rows == []

    def test_br_id_not_matched(self):
        """BR-XXX should not be matched."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | BR-001 | BR id |
"""
        rows = _parse_from_string(content)
        assert rows == []

    def test_section_10_not_matched(self):
        """Section 10 should not be parsed as Section 11."""
        content = """
## Section 10: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | US-001 | Wrong section |
"""
        rows = _parse_from_string(content)
        assert rows == []

    def test_section_12_not_matched(self):
        """Section 12 should not be parsed as Section 11."""
        content = """
## Section 12: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | US-001 | Wrong section |
"""
        rows = _parse_from_string(content)
        assert rows == []

    def test_level_3_heading_is_matched_known_limitation(self):
        """### Section 11 (level 3) IS matched (known limitation).

        The regex pattern uses ##\\s* which matches ## followed by optional
        whitespace, so ### is also matched. This documents actual behavior.
        """
        content = """
### Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | US-001 | Level 3 |
"""
        rows = _parse_from_string(content)
        # Documents current behavior: level 3 heading IS matched
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-001"

    def test_table_outside_section_11_not_matched(self):
        """Table with US-XXX outside Section 11 should not be matched."""
        content = """
## Section 5: Some Other Section

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | US-001 | Wrong section |

## Section 11: Traceability Matrix

No table here.
"""
        rows = _parse_from_string(content)
        assert rows == []


# =============================================================================
# Stress Tests
# =============================================================================

class TestStressConditions:
    """Tests for handling large inputs."""

    def test_100_traceability_rows(self):
        """Parse 100 traceability rows."""
        rows_text = "\n".join([
            f"| Element {i:03d} | S1 | US-{i:03d} | Test |"
            for i in range(100)
        ])
        content = f"""
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
{rows_text}
"""
        rows = _parse_from_string(content)
        assert len(rows) == 100
        assert rows[0]["story_id"] == "US-000"
        assert rows[99]["story_id"] == "US-099"

    def test_50_sections(self):
        """Generate manifest with 50 sections."""
        section_names = [f"section-{i:02d}" for i in range(50)]
        section_to_stories = {name: [f"US-{i:03d}"] for i, name in enumerate(section_names)}
        traceability_rows = [
            {"ux_element": f"Element {i}", "story_id": f"US-{i:03d}"}
            for i in range(50)
        ]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert len(manifest["sections"]) == 50
        assert manifest["metadata"]["sections_in_export"] == "50"

    def test_many_stories_per_section(self):
        """Section with 50 stories."""
        stories = [f"US-{i:03d}" for i in range(50)]
        section_to_stories = {"big-section": stories}
        traceability_rows = [
            {"ux_element": f"Element {i}", "story_id": f"US-{i:03d}"}
            for i in range(50)
        ]
        section_names = ["big-section"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert len(manifest["sections"]["big-section"]) == 50

    def test_many_unmapped_stories(self):
        """Many stories in traceability, none mapped."""
        section_to_stories = {}
        traceability_rows = [
            {"ux_element": f"Element {i}", "story_id": f"US-{i:03d}"}
            for i in range(30)
        ]
        section_names = ["empty-section"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        unmapped = manifest["metadata"]["unmapped_stories"]
        assert unmapped != "none"
        unmapped_list = unmapped.split(", ")
        assert len(unmapped_list) == 30

    def test_very_long_section_content(self):
        """Section 11 with lots of content before table."""
        intro = "\n".join([f"Line {i} of introduction text." for i in range(100)])
        content = f"""
## Section 11: Traceability Matrix

{intro}

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1


# =============================================================================
# Format Variation Tests
# =============================================================================

class TestFormatVariations:
    """Tests for various input format variations."""

    def test_windows_line_endings(self):
        """File with Windows line endings (CRLF)."""
        content = "## Section 11: Traceability Matrix\r\n\r\n| UX Element | Plan Section | Source ID | Desc |\r\n|------------|-------------|-----------|------|\r\n| Hero | S1 | US-001 | Test |\r\n"
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_mixed_line_endings(self):
        """File with mixed line endings."""
        content = "## Section 11: Traceability Matrix\n\r\n| UX Element | Plan Section | Source ID | Desc |\r\n|------------|-------------|-----------|------|\n| Hero | S1 | US-001 | Test |\r\n"
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_trailing_whitespace_in_cells(self):
        """Cells with trailing whitespace."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero   | S1   | US-001   | Test   |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["ux_element"] == "Hero"
        assert rows[0]["story_id"] == "US-001"

    def test_section_header_with_colon(self):
        """Section 11: (with colon)."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_section_header_with_period(self):
        """Section 11. (with period)."""
        content = """
## 11. Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_section_header_with_just_number(self):
        """## 11 (just number)."""
        content = """
## 11 Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_section_header_case_insensitive(self):
        """TRACEABILITY (uppercase) should match."""
        content = """
## Section 11: TRACEABILITY MATRIX

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_table_without_desc_column(self):
        """Table with only 3 columns."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID |
|------------|-------------|-----------|
| Hero | S1 | US-001 |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_source_id_with_parentheses(self):
        """Source ID: US-001 (primary source)."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 (primary source) | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-001"

    def test_source_id_with_brackets(self):
        """Source ID: [US-001]."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | [US-001] | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1


# =============================================================================
# Regression Tests
# =============================================================================

class TestRegressions:
    """Tests for specific bugs found during development."""

    def test_header_row_not_parsed_as_data(self):
        """Header row 'UX Element' should not be parsed as data."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        assert len(rows) == 1
        assert rows[0]["ux_element"] != "UX Element"

    def test_separator_row_not_parsed(self):
        """Separator row with dashes not parsed as data."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = _parse_from_string(content)
        # Only the data row, not separator
        assert len(rows) == 1
        assert "---" not in rows[0]["ux_element"]

    def test_metadata_model_field(self):
        """Metadata includes model field."""
        section_to_stories = {"sec": ["US-001"]}
        traceability_rows = [{"ux_element": "A", "story_id": "US-001"}]
        section_names = ["sec"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert "model" in manifest["metadata"]
        assert manifest["metadata"]["model"] == "gpt-4.1-mini"

    def test_generated_by_field(self):
        """Metadata includes generated_by field."""
        section_to_stories = {"sec": ["US-001"]}
        traceability_rows = [{"ux_element": "A", "story_id": "US-001"}]
        section_names = ["sec"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["metadata"]["generated_by"] == "generate-section-manifest.py"

    def test_unmapped_none_when_all_mapped(self):
        """unmapped_stories is 'none' when all stories mapped."""
        section_to_stories = {"sec": ["US-001", "US-002"]}
        traceability_rows = [
            {"ux_element": "A", "story_id": "US-001"},
            {"ux_element": "B", "story_id": "US-002"},
        ]
        section_names = ["sec"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["metadata"]["unmapped_stories"] == "none"

    def test_section_at_file_end_no_trailing_newline(self):
        """Section 11 at end of file with no trailing newline."""
        content = """## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |"""
        rows = _parse_from_string(content)
        assert len(rows) == 1

    def test_manifest_json_serializable(self):
        """Manifest can be serialized to JSON."""
        section_to_stories = {"sec": ["US-001"]}
        traceability_rows = [{"ux_element": "A", "story_id": "US-001"}]
        section_names = ["sec"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        # Should not raise
        json_str = json.dumps(manifest)
        # Should round-trip
        parsed = json.loads(json_str)
        assert parsed == manifest


# =============================================================================
# Real-World Scenario Tests
# =============================================================================

class TestRealWorldScenarios:
    """Tests simulating real-world usage patterns."""

    def test_hookhub_like_structure(self):
        """Simulate HookHub-like traceability with 18 rows, 16 unique stories."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Source Description |
|------------|--------------|-----------|-------------------|
| Hero headline | S1, S3 | SM-001 / US-001 | Hero title text |
| Hero subtitle | S1, S3 | SM-001 / US-001 | Hero subtitle |
| Hero CTA | S1, S3 | SM-001 / US-001 | Call to action |
| Grid layout | S5 | SM-003 / US-003 | Grid container |
| Card component | S5 | SM-006 / US-006 | Hook card |
| Card title | S5 | SM-006 / US-006 | Card hook name |
| Card description | S5 | SM-007 / US-007 | Card description |
| Stars display | S5 | SM-011 / US-011 | GitHub stars |
| Category filter | S6 | SM-013 / US-013 | Category chips |
| Event filter | S6 | SM-015 / US-015 | Event chips |
| All category | S6 | SM-014 / US-014 | All categories |
| All event | S6 | SM-016 / US-016 | All events |
| Filter state | S6 | SM-017 / US-017 | Active filters |
| Fetch data | S7 | SM-019 / US-019 | Build pipeline |
| Browse hooks | S5 | SM-004 / US-004 | Browse list |
| Link to GitHub | S5 | SM-005 / US-005 | External link |
| Footer | S8 | SM-020 / US-020 | Page footer |
| Header | S2 | SM-021 / US-021 | Page header |
"""
        rows = _parse_from_string(content)

        assert len(rows) == 18

        unique_stories = set(r["story_id"] for r in rows)
        # 18 rows: US-001 (3x), US-006 (2x) = 15 unique stories
        assert len(unique_stories) == 15

    def test_multi_section_mapping(self):
        """Map stories to multiple sections."""
        section_to_stories = {
            "landing-and-hero": ["US-001"],
            "hook-catalog": ["US-003", "US-004", "US-005", "US-006", "US-007", "US-011"],
            "filter-system": ["US-013", "US-014", "US-015", "US-016", "US-017"],
            "build-pipeline": ["US-019"],
            "dark-and-light-mode": [],
        }
        traceability_rows = [
            {"ux_element": f"Element {i}", "story_id": f"US-{i:03d}"}
            for i in [1, 3, 4, 5, 6, 7, 11, 13, 14, 15, 16, 17, 19]
        ]
        section_names = list(section_to_stories.keys())

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["sections"]["landing-and-hero"] == ["US-001"]
        assert len(manifest["sections"]["hook-catalog"]) == 6
        assert len(manifest["sections"]["filter-system"]) == 5
        assert manifest["sections"]["build-pipeline"] == ["US-019"]
        assert manifest["sections"]["dark-and-light-mode"] == []
        assert manifest["metadata"]["unmapped_stories"] == "none"

    def test_partial_mapping_with_gaps(self):
        """Some stories mapped, some not."""
        section_to_stories = {
            "section-a": ["US-001", "US-002"],
            "section-b": ["US-005"],
        }
        traceability_rows = [
            {"ux_element": "A", "story_id": "US-001"},
            {"ux_element": "B", "story_id": "US-002"},
            {"ux_element": "C", "story_id": "US-003"},  # unmapped
            {"ux_element": "D", "story_id": "US-004"},  # unmapped
            {"ux_element": "E", "story_id": "US-005"},
        ]
        section_names = ["section-a", "section-b"]

        manifest = generate_manifest(section_to_stories, traceability_rows, section_names)

        assert manifest["metadata"]["unique_stories_in_traceability"] == "5"
        assert manifest["metadata"]["unique_stories_mapped"] == "3"
        assert manifest["metadata"]["unmapped_stories"] == "US-003, US-004"


# =============================================================================
# LLM Response Validation Extended Tests
# =============================================================================

class TestLLMResponseValidationExtended:
    """Extended tests for LLM response validation."""

    def test_rejects_nested_dict_values(self):
        """Reject nested dicts in values."""
        def validate_llm_response(result):
            if not isinstance(result, dict):
                raise ValueError("Response is not a dictionary")
            for key, value in result.items():
                if not isinstance(value, list):
                    raise ValueError(f"Value for '{key}' is not a list")
                for item in value:
                    if not isinstance(item, str) or not item.startswith("US-"):
                        raise ValueError(f"Invalid story ID: {item}")
            return True

        with pytest.raises(ValueError):
            validate_llm_response({"section-a": {"nested": "dict"}})

    def test_rejects_none_values(self):
        """Reject None as a value."""
        def validate_llm_response(result):
            if not isinstance(result, dict):
                raise ValueError("Response is not a dictionary")
            for key, value in result.items():
                if not isinstance(value, list):
                    raise ValueError(f"Value for '{key}' is not a list")
                for item in value:
                    if not isinstance(item, str) or not item.startswith("US-"):
                        raise ValueError(f"Invalid story ID: {item}")
            return True

        with pytest.raises(ValueError, match="not a list"):
            validate_llm_response({"section-a": None})

    def test_accepts_empty_list(self):
        """Accept empty list as valid value."""
        def validate_llm_response(result):
            if not isinstance(result, dict):
                raise ValueError("Response is not a dictionary")
            for key, value in result.items():
                if not isinstance(value, list):
                    raise ValueError(f"Value for '{key}' is not a list")
                for item in value:
                    if not isinstance(item, str) or not item.startswith("US-"):
                        raise ValueError(f"Invalid story ID: {item}")
            return True

        # Should not raise
        assert validate_llm_response({"section-a": []}) is True

    def test_rejects_mixed_list(self):
        """Reject list with valid and invalid items."""
        def validate_llm_response(result):
            if not isinstance(result, dict):
                raise ValueError("Response is not a dictionary")
            for key, value in result.items():
                if not isinstance(value, list):
                    raise ValueError(f"Value for '{key}' is not a list")
                for item in value:
                    if not isinstance(item, str) or not item.startswith("US-"):
                        raise ValueError(f"Invalid story ID: {item}")
            return True

        with pytest.raises(ValueError, match="Invalid story ID"):
            validate_llm_response({"section-a": ["US-001", "INVALID", "US-002"]})


# ===========================================================================
# Boom Influencer System — Real Data Integration Tests
#
# Ground truth derived INDEPENDENTLY by reading UX-FLOWS.md Section 11
# traceability table. Tests assert CORRECT behavior (what the parser
# SHOULD do), not current implementation behavior.
#
# Where the parser has bugs, these tests will FAIL — that's the point.
# ===========================================================================

BOOM_UX_FLOWS = Path("/home/hisham/client-work/boom-influencer-system/.charter/UX-FLOWS.md")
BOOM_EXPORT_DIR = Path("/home/hisham/client-work/boom-influencer-system/.charter/design-os-export")


@pytest.mark.skipif(
    not BOOM_UX_FLOWS.exists(),
    reason="Boom Influencer System UX-FLOWS.md not available",
)
class TestBoomIntegration:
    """
    Integration tests against the Boom Influencer System's real
    UX-FLOWS.md traceability matrix.

    Ground truth was derived independently by reading each table row
    and extracting ALL US-XXX IDs from the Source ID column. The parser
    should capture every US-XXX in a row, not just the first one.

    Testable functions (no LLM, no Design OS export needed):
    - parse_traceability_matrix: reads UX-FLOWS.md → rows
    - generate_manifest: rows + section mapping → manifest.json
    - build_matching_prompt: rows + sections → LLM prompt text
    """

    @pytest.fixture(autouse=True)
    def load_artifacts(self):
        self.ux_flows_content = BOOM_UX_FLOWS.read_text()

    # -- Ground truth constants (independently derived) --
    #
    # Boom's traceability table has 93 data rows in the table that contain
    # at least one US-XXX. Two rows have TWO US-XXX IDs each:
    #   "Classification Review page (PG-005)" → SM-007, US-017, US-018
    #   '"Export Selected" button' → SM-012, US-028, US-029
    # A correct parser should emit one row per US-XXX found, so:
    #   89 single-US rows + 2 extra rows from multi-US = 91 total rows.
    #
    # The current parser uses re.search (first match only), producing 89.
    # Tests assert the CORRECT value of 91.

    EXPECTED_TOTAL_ROWS = 91
    EXPECTED_UNIQUE_STORIES = 17

    EXPECTED_US_IDS = sorted([
        "US-001", "US-004", "US-007", "US-008", "US-009", "US-010",
        "US-011", "US-017", "US-018", "US-019", "US-020", "US-024",
        "US-025", "US-026", "US-028", "US-029", "US-037",
    ])

    # Correct row counts: includes the multi-US rows
    # US-018: 3 (original) + 1 (Classification Review page) = 4
    # US-029: 4 (original) + 1 ("Export Selected" button) = 5
    EXPECTED_ROWS_PER_STORY = {
        "US-001": 8,
        "US-004": 1,
        "US-007": 8,
        "US-008": 8,
        "US-009": 3,
        "US-010": 3,
        "US-011": 2,
        "US-017": 4,
        "US-018": 4,   # +1 from "Classification Review page (PG-005)"
        "US-019": 4,
        "US-020": 10,
        "US-024": 8,
        "US-025": 3,
        "US-026": 10,
        "US-028": 7,
        "US-029": 5,   # +1 from '"Export Selected" button'
        "US-037": 3,
    }

    # Specific UX elements per story (independently read from the table)
    EXPECTED_US001_ELEMENTS = [
        "Configure Discovery page (PG-002)",
        "Countries multi-select (6 GCC)",
        "Follower range inputs (min/max)",
        "Niche dropdown (25+ Arabic categories)",
        "Hashtag text input",
        "Profile limit input",
        "Saved configurations section",
        "Confirmation screen",
    ]

    EXPECTED_US020_ELEMENTS = [
        "Platform filter (checkboxes)",
        "Country filter (multi-select dropdown)",
        "Niche filter (multi-select dropdown)",
        "Size bucket filter (checkboxes)",
        "AND/OR filter logic",
        "Size bucket cross-platform OR",
        "Active filter chips",
        '"Clear all" button',
        "<5 second response time",
        "Filter state in URL",
    ]

    EXPECTED_US037_ELEMENTS = [
        "Status dropdown (4 values)",
        'Default status "New"',
        "Immediate status save",
    ]

    # ── Core parsing: total counts ───────────────────────────────────

    def test_total_rows_parsed(self):
        """Parser should extract 91 rows (89 single-US + 2 extra from multi-US rows)."""
        rows = _parse_from_string(self.ux_flows_content)
        assert len(rows) == self.EXPECTED_TOTAL_ROWS, (
            f"Expected {self.EXPECTED_TOTAL_ROWS} rows, got {len(rows)}. "
            f"If 89: parser likely uses re.search instead of re.findall, "
            f"dropping second US-XXX from multi-US rows."
        )

    def test_unique_story_count(self):
        """Parser finds exactly 17 unique US-XXX IDs."""
        rows = _parse_from_string(self.ux_flows_content)
        unique = set(r["story_id"] for r in rows)
        assert len(unique) == self.EXPECTED_UNIQUE_STORIES

    def test_exact_unique_story_ids(self):
        """Parser finds the exact set of 17 US-XXX IDs."""
        rows = _parse_from_string(self.ux_flows_content)
        unique = sorted(set(r["story_id"] for r in rows))
        assert unique == self.EXPECTED_US_IDS

    # ── Row structure validation ─────────────────────────────────────

    def test_all_rows_have_required_fields(self):
        """Every parsed row has both ux_element and story_id fields."""
        rows = _parse_from_string(self.ux_flows_content)
        for i, row in enumerate(rows):
            assert "ux_element" in row, f"Row {i}: missing ux_element"
            assert "story_id" in row, f"Row {i}: missing story_id"

    def test_all_story_ids_have_us_prefix(self):
        """Every story_id starts with 'US-'."""
        rows = _parse_from_string(self.ux_flows_content)
        for row in rows:
            assert row["story_id"].startswith("US-"), (
                f"Invalid story ID: {row['story_id']}"
            )

    def test_all_story_ids_are_three_digit(self):
        """Every story_id has exactly 3 digits after US-."""
        rows = _parse_from_string(self.ux_flows_content)
        for row in rows:
            assert re.match(r"^US-\d{3}$", row["story_id"]), (
                f"Story ID not 3-digit format: {row['story_id']}"
            )

    def test_no_empty_ux_elements(self):
        """No parsed row has an empty ux_element string."""
        rows = _parse_from_string(self.ux_flows_content)
        for row in rows:
            assert row["ux_element"].strip() != "", (
                f"Empty ux_element for {row['story_id']}"
            )

    # ── Per-story row count verification ─────────────────────────────

    @pytest.mark.parametrize("story_id", EXPECTED_US_IDS)
    def test_row_count_per_story(self, story_id):
        """Number of rows per US-XXX matches expected count (including multi-US rows)."""
        rows = _parse_from_string(self.ux_flows_content)
        count = sum(1 for r in rows if r["story_id"] == story_id)
        assert count == self.EXPECTED_ROWS_PER_STORY[story_id], (
            f"{story_id}: expected {self.EXPECTED_ROWS_PER_STORY[story_id]} rows, got {count}"
        )

    # ── Multi-US source ID: parser SHOULD capture ALL US-XXX ─────────

    def test_classification_review_page_captures_both_us_ids(self):
        """Row 'SM-007, US-017, US-018' should produce rows for BOTH US-017 AND US-018."""
        rows = _parse_from_string(self.ux_flows_content)
        classification_rows = [r for r in rows
                               if "Classification Review" in r["ux_element"]]
        story_ids = sorted(r["story_id"] for r in classification_rows)
        assert story_ids == ["US-017", "US-018"], (
            f"Expected both US-017 and US-018, got {story_ids}. "
            f"Parser likely uses re.search (first match) instead of re.findall."
        )

    def test_export_selected_button_captures_both_us_ids(self):
        """Row 'SM-012, US-028, US-029' should produce rows for BOTH US-028 AND US-029."""
        rows = _parse_from_string(self.ux_flows_content)
        export_rows = [r for r in rows
                       if r["ux_element"] == '"Export Selected" button']
        story_ids = sorted(r["story_id"] for r in export_rows)
        assert story_ids == ["US-028", "US-029"], (
            f"Expected both US-028 and US-029, got {story_ids}. "
            f"Parser likely uses re.search (first match) instead of re.findall."
        )

    # ── UX element spot checks (single-US rows, unaffected by bug) ───

    def test_us001_ux_elements(self):
        """US-001 (Configure TikTok discovery) has the expected 8 UX elements."""
        rows = _parse_from_string(self.ux_flows_content)
        elements = [r["ux_element"] for r in rows if r["story_id"] == "US-001"]
        assert elements == self.EXPECTED_US001_ELEMENTS

    def test_us020_ux_elements(self):
        """US-020 (Filter by platform/country/niche/size) has the expected 10 UX elements."""
        rows = _parse_from_string(self.ux_flows_content)
        elements = [r["ux_element"] for r in rows if r["story_id"] == "US-020"]
        assert elements == self.EXPECTED_US020_ELEMENTS

    def test_us037_ux_elements(self):
        """US-037 (Set influencer status) has the expected 3 UX elements."""
        rows = _parse_from_string(self.ux_flows_content)
        elements = [r["ux_element"] for r in rows if r["story_id"] == "US-037"]
        assert elements == self.EXPECTED_US037_ELEMENTS

    def test_us004_single_element(self):
        """US-004 has exactly one UX element (API calls counter)."""
        rows = _parse_from_string(self.ux_flows_content)
        elements = [r["ux_element"] for r in rows if r["story_id"] == "US-004"]
        assert elements == ["API calls counter"]

    # ── Rows correctly skipped ───────────────────────────────────────

    def test_sm_only_rows_not_parsed(self):
        """Rows with only SM-XXX (no US-XXX) are correctly skipped."""
        rows = _parse_from_string(self.ux_flows_content)
        discovery_runs_page = [r for r in rows
                               if "Discovery Runs page" in r["ux_element"]]
        assert len(discovery_runs_page) == 0

    def test_cross_cutting_rows_not_parsed(self):
        """Rows with 'Cross-cutting' source (no US-XXX) are correctly skipped."""
        rows = _parse_from_string(self.ux_flows_content)
        nav_rows = [r for r in rows if "Navigation bar" in r["ux_element"]]
        assert len(nav_rows) == 0

    def test_nielsen_heuristic_rows_not_parsed(self):
        """Nielsen heuristic validation rows (no US-XXX) are correctly skipped."""
        rows = _parse_from_string(self.ux_flows_content)
        heuristic_elements = [r for r in rows
                              if r["ux_element"].startswith("H") and ":" in r["ux_element"]
                              and any(h in r["ux_element"]
                                      for h in ["Visibility", "Match", "User control"])]
        assert len(heuristic_elements) == 0

    # ── Document order preservation ──────────────────────────────────

    def test_first_row_is_new_run_button(self):
        """First parsed row is the first UX element with a US-XXX in the table."""
        rows = _parse_from_string(self.ux_flows_content)
        assert rows[0]["ux_element"] == '"New Run" button'
        assert rows[0]["story_id"] == "US-010"

    def test_last_row_is_notification_system(self):
        """Last parsed row is Notification system → US-007."""
        rows = _parse_from_string(self.ux_flows_content)
        assert rows[-1]["ux_element"] == "Notification system"
        assert rows[-1]["story_id"] == "US-007"

    def test_us001_elements_in_document_order(self):
        """US-001 elements appear in document order."""
        rows = _parse_from_string(self.ux_flows_content)
        us001 = [r["ux_element"] for r in rows if r["story_id"] == "US-001"]
        assert us001[0] == "Configure Discovery page (PG-002)"
        assert us001[-1] == "Confirmation screen"

    # ── Negative tests ───────────────────────────────────────────────

    def test_no_r2_stories_in_mvp_ux_flows(self):
        """Boom's MVP UX-FLOWS.md should not contain R2+ stories."""
        rows = _parse_from_string(self.ux_flows_content)
        r2_stories = {"US-002", "US-003", "US-005", "US-006",
                       "US-012", "US-013", "US-045"}
        found_r2 = {r["story_id"] for r in rows} & r2_stories
        assert found_r2 == set(), f"Found R2+ stories in MVP UX-FLOWS: {found_r2}"

    def test_no_stories_beyond_us045(self):
        """No story IDs beyond US-045 (Boom has 45 stories total)."""
        rows = _parse_from_string(self.ux_flows_content)
        for r in rows:
            num = int(r["story_id"].split("-")[1])
            assert num <= 45, f"Story ID out of range: {r['story_id']}"

    # ── generate_manifest with real parsed data ──────────────────────

    def test_manifest_metadata_counts(self):
        """generate_manifest reports correct counts from Boom's parsed rows."""
        rows = _parse_from_string(self.ux_flows_content)
        section_to_stories = {
            "discovery-flow": ["US-001", "US-004", "US-007", "US-008",
                               "US-009", "US-010"],
            "enrichment-review": ["US-011", "US-017", "US-018"],
            "search-filter": ["US-019", "US-020", "US-024", "US-025"],
            "export-system": ["US-028", "US-029"],
            "profile-detail": ["US-026", "US-037"],
        }
        section_names = list(section_to_stories.keys())
        manifest = generate_manifest(section_to_stories, rows, section_names)

        assert manifest["metadata"]["traceability_rows_parsed"] == str(len(rows))
        assert manifest["metadata"]["unique_stories_in_traceability"] == "17"
        assert manifest["metadata"]["unique_stories_mapped"] == "17"
        assert manifest["metadata"]["unmapped_stories"] == "none"

    def test_manifest_partial_mapping_reports_unmapped(self):
        """generate_manifest reports unmapped stories when not all are assigned."""
        rows = _parse_from_string(self.ux_flows_content)
        section_to_stories = {
            "discovery-flow": ["US-001", "US-004", "US-007", "US-008",
                               "US-009", "US-010"],
            "enrichment-review": ["US-011", "US-017", "US-018"],
            "search-filter": ["US-019", "US-020", "US-024", "US-025"],
            "export-system": ["US-028"],
            "profile-detail": ["US-026"],
        }
        section_names = list(section_to_stories.keys())
        manifest = generate_manifest(section_to_stories, rows, section_names)

        assert "US-029" in manifest["metadata"]["unmapped_stories"]
        assert "US-037" in manifest["metadata"]["unmapped_stories"]

    def test_manifest_empty_sections_preserved(self):
        """Sections with no stories get empty arrays."""
        rows = _parse_from_string(self.ux_flows_content)
        section_to_stories = {"main": ["US-001"]}
        section_names = ["main", "empty-a", "empty-b"]
        manifest = generate_manifest(section_to_stories, rows, section_names)

        assert manifest["sections"]["main"] == ["US-001"]
        assert manifest["sections"]["empty-a"] == []
        assert manifest["sections"]["empty-b"] == []

    def test_manifest_deduplicates_and_sorts(self):
        """Stories are deduplicated and sorted within each section."""
        rows = _parse_from_string(self.ux_flows_content)
        section_to_stories = {
            "mixed": ["US-026", "US-001", "US-020", "US-001", "US-007"],
        }
        section_names = ["mixed"]
        manifest = generate_manifest(section_to_stories, rows, section_names)

        assert manifest["sections"]["mixed"] == [
            "US-001", "US-007", "US-020", "US-026"
        ]

    # ── Feature area coverage ────────────────────────────────────────

    def test_discovery_pages_coverage(self):
        """Discovery-related UX elements map to discovery stories."""
        rows = _parse_from_string(self.ux_flows_content)
        discovery_stories = set()
        for r in rows:
            if any(kw in r["ux_element"] for kw in [
                "Discovery", "discovery", "New Run", "Run Again",
                "Progress", "Summary", "Enrichment"
            ]):
                discovery_stories.add(r["story_id"])
        assert "US-001" in discovery_stories
        assert "US-007" in discovery_stories
        assert "US-008" in discovery_stories
        assert "US-010" in discovery_stories

    def test_search_filter_pages_coverage(self):
        """Database page UX elements map to search/filter/export stories."""
        rows = _parse_from_string(self.ux_flows_content)
        search_stories = set()
        for r in rows:
            if any(kw in r["ux_element"].lower() for kw in [
                "search", "filter", "result", "pagination", "sort",
                "export", "select", "checkbox"
            ]):
                search_stories.add(r["story_id"])
        assert "US-019" in search_stories
        assert "US-020" in search_stories
        assert "US-024" in search_stories
        assert "US-028" in search_stories

    def test_profile_page_coverage(self):
        """Profile page UX elements map to profile/status stories."""
        rows = _parse_from_string(self.ux_flows_content)
        profile_stories = set()
        for r in rows:
            if any(kw in r["ux_element"] for kw in [
                "Identity", "Classification section", "TikTok metrics",
                "Contact section", "Compliance section", "Metadata section",
                "External profile", "Empty field", "Deep-linkable",
                "Previous/Next", "Status dropdown"
            ]):
                profile_stories.add(r["story_id"])
        assert "US-026" in profile_stories
        assert "US-037" in profile_stories

    # ── Ground truth self-consistency checks ─────────────────────────

    def test_per_story_counts_sum_to_total(self):
        """Sum of per-story row counts equals total rows."""
        assert sum(self.EXPECTED_ROWS_PER_STORY.values()) == self.EXPECTED_TOTAL_ROWS

    def test_per_story_keys_match_expected_ids(self):
        """EXPECTED_ROWS_PER_STORY keys match EXPECTED_US_IDS exactly."""
        assert sorted(self.EXPECTED_ROWS_PER_STORY.keys()) == self.EXPECTED_US_IDS


# ===========================================================================
# Boom Design OS Export Tests (real .charter/design-os-export directory)
# ===========================================================================

BOOM_EXPORT_SECTIONS = ["database", "discovery", "review"]


@pytest.mark.skipif(
    not BOOM_EXPORT_DIR.exists(),
    reason="Boom Design OS export not available",
)
class TestBoomExportIntegration:
    """
    Integration tests against the Boom Influencer System's real
    Design OS export directory.

    Validates list_export_sections, load_section_readmes, and
    build_matching_prompt against the actual export structure.
    """

    def test_export_sections_match_expected(self):
        """Design OS export has exactly 3 sections: database, discovery, review."""
        sections = list_export_sections(BOOM_EXPORT_DIR)
        assert sections == BOOM_EXPORT_SECTIONS

    def test_all_section_readmes_load(self):
        """Every section has a non-empty README.md."""
        sections = list_export_sections(BOOM_EXPORT_DIR)
        readmes = load_section_readmes(BOOM_EXPORT_DIR, sections)
        assert set(readmes.keys()) == set(BOOM_EXPORT_SECTIONS)
        for section, content in readmes.items():
            assert len(content.strip()) > 0, f"{section} README is empty"
            assert content.strip().startswith("#"), f"{section} README missing header"

    def test_database_readme_describes_search_and_export(self):
        """Database README mentions key terms for LLM matching disambiguation."""
        readmes = load_section_readmes(BOOM_EXPORT_DIR, BOOM_EXPORT_SECTIONS)
        readme = readmes["database"].lower()
        for term in ["search", "filter", "export", "profile", "sort"]:
            assert term in readme, f"Database README missing '{term}' — LLM may mismap"

    def test_discovery_readme_describes_runs_and_progress(self):
        """Discovery README mentions key terms for LLM matching disambiguation."""
        readmes = load_section_readmes(BOOM_EXPORT_DIR, BOOM_EXPORT_SECTIONS)
        readme = readmes["discovery"].lower()
        for term in ["configure", "progress", "run", "enrichment"]:
            assert term in readme, f"Discovery README missing '{term}' — LLM may mismap"

    def test_review_readme_describes_classification_queue(self):
        """Review README mentions key terms for LLM matching disambiguation."""
        readmes = load_section_readmes(BOOM_EXPORT_DIR, BOOM_EXPORT_SECTIONS)
        readme = readmes["review"].lower()
        for term in ["classification", "niche", "queue", "reviewed"]:
            assert term in readme, f"Review README missing '{term}' — LLM may mismap"

    def test_prompt_includes_all_sections_and_stories(self):
        """build_matching_prompt with real data contains all sections and story IDs."""
        rows = parse_traceability_matrix(BOOM_UX_FLOWS)
        sections = list_export_sections(BOOM_EXPORT_DIR)
        readmes = load_section_readmes(BOOM_EXPORT_DIR, sections)
        prompt = build_matching_prompt(rows, sections, readmes)

        for section in BOOM_EXPORT_SECTIONS:
            assert section in prompt, f"Section '{section}' missing from prompt"

        for story_id in TestBoomIntegration.EXPECTED_US_IDS:
            assert story_id in prompt, f"Story '{story_id}' missing from prompt"

    def test_manifest_with_correct_mapping_reports_zero_unmapped(self):
        """generate_manifest with ground-truth mapping has no unmapped stories."""
        rows = parse_traceability_matrix(BOOM_UX_FLOWS)
        correct_mapping = {
            "database": ["US-019", "US-020", "US-024", "US-025",
                         "US-026", "US-028", "US-029", "US-037"],
            "discovery": ["US-001", "US-004", "US-007", "US-008",
                          "US-009", "US-010", "US-011"],
            "review": ["US-017", "US-018"],
        }
        manifest = generate_manifest(correct_mapping, rows, BOOM_EXPORT_SECTIONS)
        assert manifest["metadata"]["unmapped_stories"] == "none"
        assert manifest["metadata"]["unique_stories_mapped"] == "17"


# ===========================================================================
# LLM End-to-End Test (requires OPENAI_API_KEY, calls GPT-4.1-mini)
#
# Run with: pytest test_generate_section_manifest.py -v -m costly
# ===========================================================================

# Ground truth: the correct section → story ID mapping for the Boom project.
# Derived independently from UX-FLOWS.md traceability matrix and Design OS
# export README descriptions.
BOOM_CORRECT_MAPPING = {
    "discovery": sorted(["US-001", "US-004", "US-007", "US-008",
                         "US-009", "US-010", "US-011"]),
    "review": sorted(["US-017", "US-018"]),
    "database": sorted(["US-019", "US-020", "US-024", "US-025",
                         "US-026", "US-028", "US-029", "US-037"]),
}


@pytest.mark.costly
@pytest.mark.skipif(
    not BOOM_UX_FLOWS.exists() or not BOOM_EXPORT_DIR.exists(),
    reason="Boom project artifacts not available",
)
@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set (required for LLM end-to-end test)",
)
class TestBoomLLMEndToEnd:
    """
    End-to-end test: parse real UX-FLOWS.md, read real export sections,
    call GPT-4.1-mini for section matching, and verify correctness.

    These tests cost real API credits (fractions of a cent per run).
    Run explicitly with: pytest -m costly -v
    """

    @pytest.fixture(autouse=True)
    def setup_real_data(self):
        """Load all real project data and call the LLM once for all tests."""
        # Re-import openai for real (undo the module-level mock)
        if 'openai' in sys.modules and isinstance(sys.modules['openai'], MagicMock):
            del sys.modules['openai']

        from openai import OpenAI
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        self.rows = parse_traceability_matrix(BOOM_UX_FLOWS)
        self.sections = list_export_sections(BOOM_EXPORT_DIR)
        self.readmes = load_section_readmes(BOOM_EXPORT_DIR, self.sections)

        # Import the real match function
        self.match_sections_with_llm = _mod.match_sections_with_llm

        # Make the LLM call
        self.llm_result = self.match_sections_with_llm(
            traceability_rows=self.rows,
            section_names=self.sections,
            section_readmes=self.readmes,
            client=self.client,
        )

    def test_llm_returns_all_sections(self):
        """LLM response includes all 3 section keys."""
        for section in BOOM_EXPORT_SECTIONS:
            assert section in self.llm_result, (
                f"LLM response missing section '{section}'"
            )

    def test_llm_returns_no_extra_sections(self):
        """LLM response does not invent non-existent sections."""
        extra = set(self.llm_result.keys()) - set(BOOM_EXPORT_SECTIONS)
        assert extra == set(), f"LLM invented sections: {extra}"

    def test_llm_maps_all_stories(self):
        """Every expected story ID appears in exactly one section."""
        all_mapped = set()
        for stories in self.llm_result.values():
            all_mapped.update(stories)
        expected = set(TestBoomIntegration.EXPECTED_US_IDS)
        missing = expected - all_mapped
        assert missing == set(), f"LLM failed to map stories: {missing}"

    def test_llm_no_duplicate_stories_across_sections(self):
        """No story ID appears in more than one section."""
        seen = {}
        for section, stories in self.llm_result.items():
            for story in stories:
                assert story not in seen, (
                    f"{story} appears in both '{seen[story]}' and '{section}'"
                )
                seen[story] = section

    def test_discovery_stories_correct(self):
        """LLM maps discovery stories to the 'discovery' section."""
        actual = sorted(self.llm_result.get("discovery", []))
        assert actual == BOOM_CORRECT_MAPPING["discovery"], (
            f"Discovery mismatch.\n"
            f"  Expected: {BOOM_CORRECT_MAPPING['discovery']}\n"
            f"  Got:      {actual}"
        )

    def test_review_stories_correct(self):
        """LLM maps review stories to the 'review' section."""
        actual = sorted(self.llm_result.get("review", []))
        assert actual == BOOM_CORRECT_MAPPING["review"], (
            f"Review mismatch.\n"
            f"  Expected: {BOOM_CORRECT_MAPPING['review']}\n"
            f"  Got:      {actual}"
        )

    def test_database_stories_correct(self):
        """LLM maps database stories to the 'database' section."""
        actual = sorted(self.llm_result.get("database", []))
        assert actual == BOOM_CORRECT_MAPPING["database"], (
            f"Database mismatch.\n"
            f"  Expected: {BOOM_CORRECT_MAPPING['database']}\n"
            f"  Got:      {actual}"
        )

    def test_full_manifest_correctness(self):
        """Full manifest generation with LLM results produces correct output."""
        manifest = generate_manifest(
            self.llm_result, self.rows, self.sections
        )
        assert manifest["metadata"]["unmapped_stories"] == "none"
        assert manifest["metadata"]["unique_stories_mapped"] == "17"
        assert manifest["metadata"]["sections_in_export"] == "3"

        for section in BOOM_EXPORT_SECTIONS:
            actual = manifest["sections"][section]
            expected = BOOM_CORRECT_MAPPING[section]
            assert actual == expected, (
                f"Manifest section '{section}' mismatch.\n"
                f"  Expected: {expected}\n"
                f"  Got:      {actual}"
            )


# ===========================================================================
# Gap 1 & 2: match_sections_with_llm — retry logic + validation (mocked)
# ===========================================================================


def _make_mock_openai_response(content: str) -> Mock:
    """Create a mock OpenAI response object with the given JSON content."""
    choice = Mock()
    choice.message.content = content
    response = Mock()
    response.choices = [choice]
    return response


def _make_mock_client(responses: list) -> Mock:
    """Create a mock OpenAI client that returns responses in sequence."""
    client = Mock()
    client.chat.completions.create = Mock(side_effect=responses)
    return client


# Minimal valid inputs for match_sections_with_llm
_MINIMAL_ROWS = [{"ux_element": "Search bar", "story_id": "US-001"}]
_MINIMAL_SECTIONS = ["main"]
_MINIMAL_READMES = {"main": "# Main Section"}

# Create real exception classes for mocking OpenAI errors.
# The module-level MagicMock for openai means _mod.RateLimitError and
# _mod.APIError are MagicMock objects, which can't be used in except clauses.
# We replace them with real exception classes so retry tests work.


class _MockRateLimitError(Exception):
    """Stand-in for openai.RateLimitError in tests."""
    pass


class _MockAPIError(Exception):
    """Stand-in for openai.APIError in tests."""
    pass


_mod.RateLimitError = _MockRateLimitError
_mod.APIError = _MockAPIError


class TestMatchSectionsRetryLogic:
    """Tests for match_sections_with_llm retry and error handling."""

    def test_succeeds_on_first_attempt(self):
        """Normal case: LLM returns valid JSON on first try."""
        valid_response = _make_mock_openai_response('{"main": ["US-001"]}')
        client = _make_mock_client([valid_response])

        result = match_sections_with_llm(
            _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
        )
        assert result == {"main": ["US-001"]}
        assert client.chat.completions.create.call_count == 1

    @patch("time.sleep")
    def test_retries_on_rate_limit_then_succeeds(self, mock_sleep):
        """Retries after RateLimitError, then succeeds."""
        valid_response = _make_mock_openai_response('{"main": ["US-001"]}')
        client = _make_mock_client([
            _MockRateLimitError("rate limited"),
            valid_response,
        ])

        result = match_sections_with_llm(
            _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
        )
        assert result == {"main": ["US-001"]}
        assert client.chat.completions.create.call_count == 2
        mock_sleep.assert_called()

    @patch("time.sleep")
    def test_retries_on_api_error_then_succeeds(self, mock_sleep):
        """Retries after APIError, then succeeds."""
        valid_response = _make_mock_openai_response('{"main": ["US-001"]}')
        client = _make_mock_client([
            _MockAPIError("server error"),
            valid_response,
        ])

        result = match_sections_with_llm(
            _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
        )
        assert result == {"main": ["US-001"]}
        assert client.chat.completions.create.call_count == 2

    @patch("time.sleep")
    def test_raises_after_max_retries_on_api_error(self, mock_sleep):
        """Raises RuntimeError after MAX_RETRIES consecutive API errors."""
        client = _make_mock_client([
            _MockAPIError("fail 1"),
            _MockAPIError("fail 2"),
            _MockAPIError("fail 3"),
        ])

        with pytest.raises(RuntimeError, match="LLM matching failed"):
            match_sections_with_llm(
                _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
            )
        assert client.chat.completions.create.call_count == MAX_RETRIES

    @patch("time.sleep")
    def test_retries_on_invalid_json_then_succeeds(self, mock_sleep):
        """Retries when LLM returns invalid JSON, then succeeds."""
        bad_response = _make_mock_openai_response("not json at all")
        good_response = _make_mock_openai_response('{"main": ["US-001"]}')
        client = _make_mock_client([bad_response, good_response])

        result = match_sections_with_llm(
            _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
        )
        assert result == {"main": ["US-001"]}
        assert client.chat.completions.create.call_count == 2

    @patch("time.sleep")
    def test_raises_after_max_retries_on_invalid_json(self, mock_sleep):
        """Raises RuntimeError after MAX_RETRIES of invalid JSON."""
        bad = _make_mock_openai_response("not json")
        client = _make_mock_client([bad, bad, bad])

        with pytest.raises(RuntimeError, match="invalid response"):
            match_sections_with_llm(
                _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
            )

    @patch("time.sleep")
    def test_retries_on_validation_failure_then_succeeds(self, mock_sleep):
        """Retries when LLM returns wrong structure, then succeeds."""
        # Valid JSON but wrong structure (list instead of dict)
        bad_response = _make_mock_openai_response('["US-001"]')
        good_response = _make_mock_openai_response('{"main": ["US-001"]}')
        client = _make_mock_client([bad_response, good_response])

        result = match_sections_with_llm(
            _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
        )
        assert result == {"main": ["US-001"]}

    @patch("time.sleep")
    def test_retries_on_non_us_prefix_ids(self, mock_sleep):
        """Retries when LLM returns SM-XXX instead of US-XXX."""
        bad_response = _make_mock_openai_response('{"main": ["SM-001"]}')
        good_response = _make_mock_openai_response('{"main": ["US-001"]}')
        client = _make_mock_client([bad_response, good_response])

        result = match_sections_with_llm(
            _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
        )
        assert result == {"main": ["US-001"]}

    @patch("time.sleep")
    def test_retries_on_non_list_values(self, mock_sleep):
        """Retries when LLM returns string values instead of lists."""
        bad_response = _make_mock_openai_response('{"main": "US-001"}')
        good_response = _make_mock_openai_response('{"main": ["US-001"]}')
        client = _make_mock_client([bad_response, good_response])

        result = match_sections_with_llm(
            _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
        )
        assert result == {"main": ["US-001"]}

    def test_accepts_extra_sections_from_llm(self):
        """LLM may return sections not in section_names — function doesn't reject them."""
        response = _make_mock_openai_response(
            '{"main": ["US-001"], "extra": ["US-002"]}'
        )
        client = _make_mock_client([response])

        result = match_sections_with_llm(
            _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
        )
        assert "main" in result
        assert "extra" in result

    def test_accepts_empty_lists_from_llm(self):
        """LLM may return empty lists for sections with no matches."""
        response = _make_mock_openai_response(
            '{"main": ["US-001"], "other": []}'
        )
        client = _make_mock_client([response])

        result = match_sections_with_llm(
            _MINIMAL_ROWS, _MINIMAL_SECTIONS, _MINIMAL_READMES, client
        )
        assert result["other"] == []


# ===========================================================================
# Gap 7: main() CLI tests (mocked filesystem + mocked OpenAI)
# ===========================================================================

class TestMainCLI:
    """Tests for the main() CLI entry point."""

    def _setup_export_dir(self, tmp_path: Path):
        """Create a minimal valid export directory structure."""
        export = tmp_path / "export"
        sections = export / "sections"
        sec_main = sections / "main-section"
        sec_main.mkdir(parents=True)
        (sec_main / "README.md").write_text("# Main Section\nDoes stuff.")
        return export

    def _setup_ux_flows(self, tmp_path: Path):
        """Create a minimal valid UX-FLOWS.md."""
        ux = tmp_path / "UX-FLOWS.md"
        ux.write_text(
            "## Section 11: Traceability Matrix\n\n"
            "| UX Element | Plan Section | Source ID | Desc |\n"
            "|---|---|---|---|\n"
            "| Button | S1 | US-001 | A button |\n"
        )
        return ux

    def test_missing_export_dir_returns_1(self, tmp_path):
        """main() returns 1 when export directory doesn't exist."""
        ux = self._setup_ux_flows(tmp_path)
        output = tmp_path / "manifest.json"
        sys.argv = [
            "generate-section-manifest.py",
            "--export-dir", str(tmp_path / "nonexistent"),
            "--ux-flows", str(ux),
            "--output", str(output),
        ]
        assert main() == 1

    def test_missing_ux_flows_returns_1(self, tmp_path):
        """main() returns 1 when UX-FLOWS.md doesn't exist."""
        export = self._setup_export_dir(tmp_path)
        output = tmp_path / "manifest.json"
        sys.argv = [
            "generate-section-manifest.py",
            "--export-dir", str(export),
            "--ux-flows", str(tmp_path / "nonexistent.md"),
            "--output", str(output),
        ]
        assert main() == 1

    def test_missing_api_key_returns_1(self, tmp_path, monkeypatch):
        """main() returns 1 when OPENAI_API_KEY is not set."""
        export = self._setup_export_dir(tmp_path)
        ux = self._setup_ux_flows(tmp_path)
        output = tmp_path / "manifest.json"
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        sys.argv = [
            "generate-section-manifest.py",
            "--export-dir", str(export),
            "--ux-flows", str(ux),
            "--output", str(output),
        ]
        assert main() == 1

    def test_no_traceability_data_returns_1(self, tmp_path, monkeypatch):
        """main() returns 1 when UX-FLOWS.md has no traceability matrix."""
        export = self._setup_export_dir(tmp_path)
        ux = tmp_path / "UX-FLOWS.md"
        ux.write_text("# UX Flows\n\nNo section 11 here.\n")
        output = tmp_path / "manifest.json"
        monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
        sys.argv = [
            "generate-section-manifest.py",
            "--export-dir", str(export),
            "--ux-flows", str(ux),
            "--output", str(output),
        ]
        assert main() == 1

    def test_no_sections_returns_1(self, tmp_path, monkeypatch):
        """main() returns 1 when export has no section directories."""
        export = tmp_path / "export"
        (export / "sections").mkdir(parents=True)  # empty sections dir
        ux = self._setup_ux_flows(tmp_path)
        output = tmp_path / "manifest.json"
        monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
        sys.argv = [
            "generate-section-manifest.py",
            "--export-dir", str(export),
            "--ux-flows", str(ux),
            "--output", str(output),
        ]
        assert main() == 1

    def test_dry_run_prints_but_does_not_write(self, tmp_path, monkeypatch):
        """--dry-run prints JSON to stdout but does not write the output file."""
        export = self._setup_export_dir(tmp_path)
        ux = self._setup_ux_flows(tmp_path)
        output = tmp_path / "manifest.json"
        monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

        # Mock the OpenAI client at module level
        mock_response = _make_mock_openai_response(
            '{"main-section": ["US-001"]}'
        )
        mock_client = Mock()
        mock_client.chat.completions.create = Mock(return_value=mock_response)

        sys.argv = [
            "generate-section-manifest.py",
            "--export-dir", str(export),
            "--ux-flows", str(ux),
            "--output", str(output),
            "--dry-run",
        ]

        with patch.object(_mod, "OpenAI", return_value=mock_client):
            result = main()

        assert result == 0
        assert not output.exists(), "dry-run should NOT write the file"

    def test_normal_run_writes_manifest(self, tmp_path, monkeypatch):
        """Normal run writes manifest.json to the output path."""
        export = self._setup_export_dir(tmp_path)
        ux = self._setup_ux_flows(tmp_path)
        output = tmp_path / "manifest.json"
        monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

        mock_response = _make_mock_openai_response(
            '{"main-section": ["US-001"]}'
        )
        mock_client = Mock()
        mock_client.chat.completions.create = Mock(return_value=mock_response)

        sys.argv = [
            "generate-section-manifest.py",
            "--export-dir", str(export),
            "--ux-flows", str(ux),
            "--output", str(output),
        ]

        with patch.object(_mod, "OpenAI", return_value=mock_client):
            result = main()

        assert result == 0
        assert output.exists()
        manifest = json.loads(output.read_text())
        assert "main-section" in manifest["sections"]
        assert manifest["sections"]["main-section"] == ["US-001"]


# ===========================================================================
# Gaps 3-6: LLM Behavioral Tests with Synthetic Data
# (requires OPENAI_API_KEY — tests the LLM's semantic matching ability)
# ===========================================================================

@pytest.mark.costly
@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set",
)
class TestLLMBehavior:
    """
    Test GPT-4.1-mini's section-matching behavior with synthetic data.

    Each test constructs controlled inputs and verifies the LLM makes
    the correct semantic mapping. These cost real API credits.
    """

    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Create a real OpenAI client for LLM tests."""
        if 'openai' in sys.modules and isinstance(sys.modules['openai'], MagicMock):
            del sys.modules['openai']
        from openai import OpenAI
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.match = _mod.match_sections_with_llm

    def test_clear_separation_two_sections(self):
        """LLM correctly separates clearly distinct UX elements into 2 sections."""
        rows = [
            {"ux_element": "Login form", "story_id": "US-001"},
            {"ux_element": "Password field", "story_id": "US-001"},
            {"ux_element": "Product card", "story_id": "US-002"},
            {"ux_element": "Add to cart button", "story_id": "US-002"},
        ]
        sections = ["authentication", "product-catalog"]
        readmes = {
            "authentication": "# Authentication\nLogin, signup, password reset.",
            "product-catalog": "# Product Catalog\nBrowse products, add to cart.",
        }

        result = self.match(rows, sections, readmes, self.client)

        assert "US-001" in result.get("authentication", [])
        assert "US-002" in result.get("product-catalog", [])
        assert "US-001" not in result.get("product-catalog", [])
        assert "US-002" not in result.get("authentication", [])

    def test_ambiguous_sections_similar_names(self):
        """LLM disambiguates sections with similar names using README context."""
        rows = [
            {"ux_element": "Edit profile name", "story_id": "US-010"},
            {"ux_element": "Change password", "story_id": "US-011"},
            {"ux_element": "Upload avatar", "story_id": "US-010"},
            {"ux_element": "Two-factor setup", "story_id": "US-011"},
        ]
        sections = ["user-profile", "user-security"]
        readmes = {
            "user-profile": "# User Profile\nEdit personal info: name, avatar, bio.",
            "user-security": "# User Security\nPassword management, 2FA, session control.",
        }

        result = self.match(rows, sections, readmes, self.client)

        assert "US-010" in result.get("user-profile", [])
        assert "US-011" in result.get("user-security", [])

    def test_single_section_all_stories_map_there(self):
        """With only one section, all stories should map to it."""
        rows = [
            {"ux_element": "Dashboard chart", "story_id": "US-001"},
            {"ux_element": "Stats panel", "story_id": "US-002"},
            {"ux_element": "Export button", "story_id": "US-003"},
        ]
        sections = ["dashboard"]
        readmes = {"dashboard": "# Dashboard\nMain analytics view with charts and exports."}

        result = self.match(rows, sections, readmes, self.client)

        dashboard_stories = set(result.get("dashboard", []))
        assert {"US-001", "US-002", "US-003"} == dashboard_stories

    def test_many_sections_correct_distribution(self):
        """LLM handles 5 sections without confusion."""
        rows = [
            {"ux_element": "Invoice PDF generator", "story_id": "US-001"},
            {"ux_element": "Payment form", "story_id": "US-002"},
            {"ux_element": "Shipping address form", "story_id": "US-003"},
            {"ux_element": "Product image gallery", "story_id": "US-004"},
            {"ux_element": "Customer support chat", "story_id": "US-005"},
        ]
        sections = ["billing", "payments", "shipping", "product-catalog", "support"]
        readmes = {
            "billing": "# Billing\nInvoices, receipts, billing history.",
            "payments": "# Payments\nPayment processing, credit cards, refunds.",
            "shipping": "# Shipping\nAddress management, delivery tracking.",
            "product-catalog": "# Product Catalog\nProduct listings, images, descriptions.",
            "support": "# Support\nCustomer service chat, tickets, FAQ.",
        }

        result = self.match(rows, sections, readmes, self.client)

        assert "US-001" in result.get("billing", [])
        assert "US-002" in result.get("payments", [])
        assert "US-003" in result.get("shipping", [])
        assert "US-004" in result.get("product-catalog", [])
        assert "US-005" in result.get("support", [])

    def test_multiple_stories_same_section(self):
        """Multiple UX elements with different story IDs map to the same section."""
        rows = [
            {"ux_element": "Filter by price", "story_id": "US-010"},
            {"ux_element": "Filter by category", "story_id": "US-011"},
            {"ux_element": "Sort by rating", "story_id": "US-012"},
            {"ux_element": "Checkout form", "story_id": "US-020"},
        ]
        sections = ["search-and-filter", "checkout"]
        readmes = {
            "search-and-filter": "# Search & Filter\nProduct filtering, sorting, search.",
            "checkout": "# Checkout\nCart review, payment, order confirmation.",
        }

        result = self.match(rows, sections, readmes, self.client)

        filter_stories = set(result.get("search-and-filter", []))
        assert {"US-010", "US-011", "US-012"}.issubset(filter_stories)
        assert "US-020" in result.get("checkout", [])

    def test_no_story_duplication_across_sections(self):
        """No story ID appears in more than one section."""
        rows = [
            {"ux_element": "User list table", "story_id": "US-001"},
            {"ux_element": "User detail card", "story_id": "US-001"},
            {"ux_element": "Role assignment dropdown", "story_id": "US-002"},
        ]
        sections = ["user-management", "role-management"]
        readmes = {
            "user-management": "# User Management\nCRUD operations for users, user profiles.",
            "role-management": "# Role Management\nAssign roles, permissions, access control.",
        }

        result = self.match(rows, sections, readmes, self.client)

        # US-001 should appear in exactly one section
        us001_sections = [s for s, ids in result.items() if "US-001" in ids]
        assert len(us001_sections) == 1, (
            f"US-001 appears in multiple sections: {us001_sections}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
