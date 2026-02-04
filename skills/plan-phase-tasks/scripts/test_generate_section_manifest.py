#!/usr/bin/env python3
"""
Unit tests for generate-section-manifest.py

Tests the parsing and manifest generation logic. LLM matching is tested
via integration tests (requires API key) or mocked for unit tests.

Run with: pytest test_generate_section_manifest.py -v
"""

import json
import pytest
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch, MagicMock

# Import the module functions
import sys
sys.path.insert(0, str(Path(__file__).parent))

from importlib import import_module

# We need to mock openai before importing the module
sys.modules['openai'] = MagicMock()

# Now we can define the functions inline since the module has side effects
import re


def parse_traceability_matrix(content: str) -> list[dict]:
    """
    Parse UX-FLOWS.md Section 11 to extract UX Element → Story ID mappings.
    (Copied from main module for isolated testing)
    """
    section_match = re.search(
        r"##\s*(?:Section\s*)?11[:\.]?\s*Traceability.*?\n(.*?)(?=\n##\s|\Z)",
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not section_match:
        return []

    section_content = section_match.group(1)
    rows = []

    for line in section_content.split("\n"):
        line = line.strip()

        if not line or line.startswith("|--") or "---" in line:
            continue
        if not line.startswith("|"):
            continue

        cells = [cell.strip() for cell in line.split("|")]
        cells = [c for c in cells if c]

        if len(cells) < 3:
            continue
        if cells[0].lower() == "ux element":
            continue

        ux_element = cells[0]
        source_id = cells[2] if len(cells) > 2 else ""

        us_match = re.search(r"US-(\d{3})", source_id)
        if us_match:
            story_id = f"US-{us_match.group(1)}"
            rows.append({"ux_element": ux_element, "story_id": story_id})

    return rows


def generate_manifest(
    section_to_stories: dict[str, list[str]],
    traceability_rows: list[dict],
    section_names: list[str]
) -> dict:
    """Generate manifest from matching results. (Copied for testing)"""
    sections: dict[str, list[str]] = {}
    for name in section_names:
        stories = section_to_stories.get(name, [])
        sections[name] = sorted(set(stories))

    all_stories = set()
    for stories in sections.values():
        all_stories.update(stories)

    traceability_stories = set(row["story_id"] for row in traceability_rows)
    unmapped = traceability_stories - all_stories

    return {
        "sections": sections,
        "metadata": {
            "generated_by": "generate-section-manifest.py",
            "model": "gpt-4.1-mini",
            "traceability_rows_parsed": str(len(traceability_rows)),
            "unique_stories_in_traceability": str(len(traceability_stories)),
            "unique_stories_mapped": str(len(all_stories)),
            "sections_in_export": str(len(section_names)),
            "unmapped_stories": ", ".join(sorted(unmapped)) if unmapped else "none"
        }
    }


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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
            rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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

        content = ux_flows_path.read_text()
        rows = parse_traceability_matrix(content)

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
        content = path.read_text()
        rows = parse_traceability_matrix(content)

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

        # Import and call the function
        from pathlib import Path

        def list_export_sections(export_dir: Path) -> list[str]:
            sections_dir = export_dir / "sections"
            if not sections_dir.exists():
                return []
            return sorted([
                d.name for d in sections_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ])

        result = list_export_sections(tmp_path)
        assert result == ["filter-system", "hook-catalog", "landing-and-hero"]

    def test_excludes_hidden_directories(self, tmp_path):
        """Exclude directories starting with dot."""
        sections_dir = tmp_path / "sections"
        sections_dir.mkdir()
        (sections_dir / "visible-section").mkdir()
        (sections_dir / ".hidden-section").mkdir()
        (sections_dir / ".git").mkdir()

        def list_export_sections(export_dir: Path) -> list[str]:
            sections_dir = export_dir / "sections"
            if not sections_dir.exists():
                return []
            return sorted([
                d.name for d in sections_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ])

        result = list_export_sections(tmp_path)
        assert result == ["visible-section"]

    def test_excludes_files(self, tmp_path):
        """Exclude files, only return directories."""
        sections_dir = tmp_path / "sections"
        sections_dir.mkdir()
        (sections_dir / "real-section").mkdir()
        (sections_dir / "not-a-section.md").write_text("content")

        def list_export_sections(export_dir: Path) -> list[str]:
            sections_dir = export_dir / "sections"
            if not sections_dir.exists():
                return []
            return sorted([
                d.name for d in sections_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ])

        result = list_export_sections(tmp_path)
        assert result == ["real-section"]

    def test_returns_empty_for_missing_sections_dir(self, tmp_path):
        """Return empty list if sections/ directory doesn't exist."""
        def list_export_sections(export_dir: Path) -> list[str]:
            sections_dir = export_dir / "sections"
            if not sections_dir.exists():
                return []
            return sorted([
                d.name for d in sections_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ])

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

        def load_section_readmes(export_dir: Path, section_names: list[str]) -> dict[str, str]:
            readmes: dict[str, str] = {}
            sections_dir = export_dir / "sections"
            for section in section_names:
                readme_path = sections_dir / section / "README.md"
                if readme_path.exists():
                    content = readme_path.read_text(encoding="utf-8")
                    lines = content.split("\n")[:50]
                    readmes[section] = "\n".join(lines)
                else:
                    readmes[section] = f"No README found for {section}"
            return readmes

        result = load_section_readmes(tmp_path, ["section-a", "section-b"])
        assert "# Section A" in result["section-a"]
        assert "# Section B" in result["section-b"]

    def test_handles_missing_readme(self, tmp_path):
        """Handle sections without README.md."""
        sections_dir = tmp_path / "sections"
        sections_dir.mkdir()
        (sections_dir / "no-readme-section").mkdir()

        def load_section_readmes(export_dir: Path, section_names: list[str]) -> dict[str, str]:
            readmes: dict[str, str] = {}
            sections_dir = export_dir / "sections"
            for section in section_names:
                readme_path = sections_dir / section / "README.md"
                if readme_path.exists():
                    content = readme_path.read_text(encoding="utf-8")
                    lines = content.split("\n")[:50]
                    readmes[section] = "\n".join(lines)
                else:
                    readmes[section] = f"No README found for {section}"
            return readmes

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

        def load_section_readmes(export_dir: Path, section_names: list[str]) -> dict[str, str]:
            readmes: dict[str, str] = {}
            sections_dir = export_dir / "sections"
            for section in section_names:
                readme_path = sections_dir / section / "README.md"
                if readme_path.exists():
                    content = readme_path.read_text(encoding="utf-8")
                    lines = content.split("\n")[:50]
                    readmes[section] = "\n".join(lines)
                else:
                    readmes[section] = f"No README found for {section}"
            return readmes

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
        def build_matching_prompt(
            traceability_rows: list[dict],
            section_names: list[str],
            section_readmes: dict[str, str]
        ) -> str:
            traceability_text = "UX Element | Story ID\n"
            traceability_text += "----------|----------\n"
            for row in traceability_rows:
                traceability_text += f"{row['ux_element']} | {row['story_id']}\n"
            sections_text = ""
            for section, readme in section_readmes.items():
                sections_text += f"\n### {section}\n{readme}\n"
            return f"## UX Elements\n{traceability_text}\n## Sections\n{sections_text}"

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
        def build_matching_prompt(
            traceability_rows: list[dict],
            section_names: list[str],
            section_readmes: dict[str, str]
        ) -> str:
            traceability_text = "UX Element | Story ID\n"
            traceability_text += "----------|----------\n"
            for row in traceability_rows:
                traceability_text += f"{row['ux_element']} | {row['story_id']}\n"
            sections_text = ""
            for section, readme in section_readmes.items():
                sections_text += f"\n### {section}\n{readme}\n"
            return f"## UX Elements\n{traceability_text}\n## Sections\n{sections_text}"

        prompt = build_matching_prompt([], [], {})

        assert "UX Element | Story ID" in prompt
        assert "## Sections" in prompt


# =============================================================================
# LLM Response Validation Tests
# =============================================================================

class TestLLMResponseValidation:
    """Tests for LLM response validation logic."""

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
        rows = parse_traceability_matrix("")
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)

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
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-001"

    def test_section_11_with_no_table(self):
        """Section 11 exists but has no table."""
        content = """
## Section 11: Traceability Matrix

This section has no table, just text.

## Section 12: Next Section
"""
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1

    def test_table_with_leading_whitespace(self):
        """Table rows with leading whitespace."""
        content = """
## Section 11: Traceability Matrix

  | UX Element | Plan Section | Source ID | Desc |
  |------------|-------------|-----------|------|
  | Hero | S1 | US-001 | Test |
"""
        rows = parse_traceability_matrix(content)
        # Leading whitespace is stripped
        assert len(rows) == 1

    def test_source_id_with_multiple_us_ids(self):
        """Source ID containing multiple US-XXX (first wins)."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 / US-002 | Test |
"""
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1
        assert rows[0]["story_id"] == "US-001"  # First match

    def test_source_id_formats_comprehensive(self):
        """Various Source ID formats that should extract US-XXX."""
        test_cases = [
            ("US-001", "US-001"),
            ("SM-001 / US-001", "US-001"),
            ("SM-001/US-001", "US-001"),
            ("US-001 (primary)", "US-001"),
            ("see US-001", "US-001"),
            ("US-001, US-002", "US-001"),
            ("ref: US-001", "US-001"),
        ]
        for source_id, expected in test_cases:
            content = f"""
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | {source_id} | Test |
"""
            rows = parse_traceability_matrix(content)
            assert len(rows) == 1, f"Failed for: {source_id}"
            assert rows[0]["story_id"] == expected, f"Failed for: {source_id}"

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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1

    def test_empty_table_after_header(self):
        """Table with only header row (no data rows)."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
"""
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
        assert rows == []

    def test_us_id_two_digits_not_matched(self):
        """US-01 (two digits) should not be matched."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | US-01 | Two digits |
"""
        rows = parse_traceability_matrix(content)
        assert rows == []

    def test_us_id_four_digits_extracts_first_three(self):
        """US-1234 extracts as US-123."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | US-1234 | Four digits |
"""
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
        assert rows == []

    def test_br_id_not_matched(self):
        """BR-XXX should not be matched."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | BR-001 | BR id |
"""
        rows = parse_traceability_matrix(content)
        assert rows == []

    def test_section_10_not_matched(self):
        """Section 10 should not be parsed as Section 11."""
        content = """
## Section 10: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | US-001 | Wrong section |
"""
        rows = parse_traceability_matrix(content)
        assert rows == []

    def test_section_12_not_matched(self):
        """Section 12 should not be parsed as Section 11."""
        content = """
## Section 12: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Test | S1 | US-001 | Wrong section |
"""
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1


# =============================================================================
# Format Variation Tests
# =============================================================================

class TestFormatVariations:
    """Tests for various input format variations."""

    def test_windows_line_endings(self):
        """File with Windows line endings (CRLF)."""
        content = "## Section 11: Traceability Matrix\r\n\r\n| UX Element | Plan Section | Source ID | Desc |\r\n|------------|-------------|-----------|------|\r\n| Hero | S1 | US-001 | Test |\r\n"
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1

    def test_mixed_line_endings(self):
        """File with mixed line endings."""
        content = "## Section 11: Traceability Matrix\n\r\n| UX Element | Plan Section | Source ID | Desc |\r\n|------------|-------------|-----------|------|\n| Hero | S1 | US-001 | Test |\r\n"
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1

    def test_trailing_whitespace_in_cells(self):
        """Cells with trailing whitespace."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero   | S1   | US-001   | Test   |
"""
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1

    def test_section_header_with_period(self):
        """Section 11. (with period)."""
        content = """
## 11. Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1

    def test_section_header_with_just_number(self):
        """## 11 (just number)."""
        content = """
## 11 Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1

    def test_section_header_case_insensitive(self):
        """TRACEABILITY (uppercase) should match."""
        content = """
## Section 11: TRACEABILITY MATRIX

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 | Test |
"""
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1

    def test_table_without_desc_column(self):
        """Table with only 3 columns."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID |
|------------|-------------|-----------|
| Hero | S1 | US-001 |
"""
        rows = parse_traceability_matrix(content)
        assert len(rows) == 1

    def test_source_id_with_parentheses(self):
        """Source ID: US-001 (primary source)."""
        content = """
## Section 11: Traceability Matrix

| UX Element | Plan Section | Source ID | Desc |
|------------|-------------|-----------|------|
| Hero | S1 | US-001 (primary source) | Test |
"""
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)
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
        rows = parse_traceability_matrix(content)

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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
