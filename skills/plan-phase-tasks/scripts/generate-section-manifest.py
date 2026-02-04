#!/usr/bin/env python3
"""
generate-section-manifest.py

Post-processes a Design OS export to create a manifest.json that maps
section directory names to US-XXX story IDs for use by /plan-phase-tasks.

The script parses the UX-FLOWS.md traceability matrix (UX Element → Story ID),
lists section directories from the Design OS export, then uses a lightweight
LLM (GPT-4.1-mini) to semantically match UX elements to their corresponding
section directories. The result is aggregated into a manifest.

Usage:
    python3 generate-section-manifest.py \
        --export-dir .charter/design-os-export \
        --ux-flows .charter/UX-FLOWS.md \
        --output .charter/design-os-export/manifest.json

Environment:
    OPENAI_API_KEY: Required. OpenAI API key for GPT-4.1-mini calls.
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import TypedDict

# Load .env.local file if present (Next.js convention for local secrets)
try:
    from dotenv import load_dotenv
    load_dotenv(".env.local")  # Next.js convention
    load_dotenv(".env")  # Fallback to standard .env
except ImportError:
    pass  # dotenv not installed, rely on environment variables

from openai import OpenAI, APIError, RateLimitError

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

MODEL = "gpt-4.1-mini"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Type Definitions
# -----------------------------------------------------------------------------

class TraceabilityRow(TypedDict):
    """A single row from the traceability matrix."""
    ux_element: str
    story_id: str  # US-XXX format


class SectionManifest(TypedDict):
    """Maps section directory names to their associated US-XXX story IDs."""
    sections: dict[str, list[str]]  # {"landing-and-hero": ["US-001", "US-002"], ...}
    metadata: dict[str, str]


# -----------------------------------------------------------------------------
# Traceability Parser
# -----------------------------------------------------------------------------

def parse_traceability_matrix(ux_flows_path: Path) -> list[TraceabilityRow]:
    """
    Parse UX-FLOWS.md Section 11 to extract UX Element → Story ID mappings.

    Expected table format:
    | UX Element | Plan Section | Source ID | Source Description |
    |------------|--------------|-----------|-------------------|
    | Hero headline | S1, S3 | SM-001 / US-001 | Description... |

    Returns:
        List of TraceabilityRow dicts with ux_element and story_id (US-XXX).
    """
    content = ux_flows_path.read_text(encoding="utf-8")

    # Find Section 11 (Traceability Matrix)
    section_match = re.search(
        r"##\s*(?:Section\s*)?11[:\.]?\s*Traceability.*?\n(.*?)(?=\n##\s|\Z)",
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not section_match:
        logger.warning("Could not find Section 11 (Traceability) in UX-FLOWS.md")
        return []

    section_content = section_match.group(1)
    rows: list[TraceabilityRow] = []

    for line in section_content.split("\n"):
        line = line.strip()

        # Skip empty lines, header rows, and separator rows
        if not line or line.startswith("|--") or "---" in line:
            continue
        if not line.startswith("|"):
            continue

        # Parse table cells
        cells = [cell.strip() for cell in line.split("|")]
        # Remove empty strings from split
        cells = [c for c in cells if c]

        if len(cells) < 3:
            continue

        # Skip header row
        if cells[0].lower() == "ux element":
            continue

        ux_element = cells[0]
        source_id = cells[2] if len(cells) > 2 else ""

        # Extract US-XXX from "SM-XXX / US-XXX" format
        us_match = re.search(r"US-(\d{3})", source_id)
        if us_match:
            story_id = f"US-{us_match.group(1)}"
            rows.append(TraceabilityRow(
                ux_element=ux_element,
                story_id=story_id
            ))

    logger.info(f"Parsed {len(rows)} traceability rows from UX-FLOWS.md")
    return rows


def list_export_sections(export_dir: Path) -> list[str]:
    """List all section directory names in the Design OS export."""
    sections_dir = export_dir / "sections"

    if not sections_dir.exists():
        logger.error(f"Sections directory not found: {sections_dir}")
        return []

    return sorted([
        d.name for d in sections_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])


def load_section_readmes(export_dir: Path, section_names: list[str]) -> dict[str, str]:
    """Load README.md content for each section to provide context to the LLM."""
    readmes: dict[str, str] = {}
    sections_dir = export_dir / "sections"

    for section in section_names:
        readme_path = sections_dir / section / "README.md"
        if readme_path.exists():
            # Load first 50 lines to keep context manageable
            content = readme_path.read_text(encoding="utf-8")
            lines = content.split("\n")[:50]
            readmes[section] = "\n".join(lines)
        else:
            readmes[section] = f"No README found for {section}"

    return readmes


# -----------------------------------------------------------------------------
# LLM-Based Section Matching
# -----------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a precise mapping assistant for a software project. Your task is to match
UX elements from a traceability matrix to their corresponding Design OS section
directories.

Context:
- UX elements describe UI features (e.g., "Hero headline", "Category filter chips")
- Section directories contain implementation code (e.g., "landing-and-hero", "filter-system")
- Each UX element has an associated story ID (US-XXX)
- The section README files describe what each section implements

Your job:
1. Read the UX elements and their story IDs
2. Read the section directory names and their README descriptions
3. Determine which section each UX element belongs to based on semantic similarity
4. Return the aggregated mapping: directory → list of story IDs

Rules:
- Each UX element maps to exactly one section (or "unmatched" if no clear fit)
- Multiple UX elements can map to the same section
- The story IDs should be deduplicated per section
- Return valid JSON only, no explanations
- Cross-cutting sections (like theming) may have no direct UX element matches
"""


def build_matching_prompt(
    traceability_rows: list[TraceabilityRow],
    section_names: list[str],
    section_readmes: dict[str, str]
) -> str:
    """Construct the user prompt for section matching."""

    # Format traceability as a simple table
    traceability_text = "UX Element | Story ID\n"
    traceability_text += "----------|----------\n"
    for row in traceability_rows:
        traceability_text += f"{row['ux_element']} | {row['story_id']}\n"

    # Format section READMEs
    sections_text = ""
    for section, readme in section_readmes.items():
        sections_text += f"\n### {section}\n{readme}\n"

    return f"""\
Match the UX elements to their corresponding section directories.

## UX Elements (from traceability matrix)

{traceability_text}

## Section Directories (from Design OS export)

{sections_text}

## Task

Return a JSON object where:
- Keys are section directory names (exactly as shown above)
- Values are arrays of story IDs (US-XXX format) that belong to that section
- Deduplicate story IDs within each section
- Include all sections, even if they have no matching story IDs (use empty array)

Example output format:
{{
  "landing-and-hero": ["US-001", "US-003"],
  "hook-catalog": ["US-004", "US-006"],
  "filter-system": ["US-013", "US-014"],
  "dark-and-light-mode": []
}}
"""


def match_sections_with_llm(
    traceability_rows: list[TraceabilityRow],
    section_names: list[str],
    section_readmes: dict[str, str],
    client: OpenAI
) -> dict[str, list[str]]:
    """
    Use LLM to semantically match UX elements to section directories.

    Args:
        traceability_rows: Parsed rows from UX-FLOWS.md traceability matrix
        section_names: Directory names from Design OS export
        section_readmes: README.md content for each section
        client: OpenAI client instance

    Returns:
        Dict mapping directory names to lists of US-XXX story IDs

    Raises:
        RuntimeError: If LLM call fails after retries
    """
    user_prompt = build_matching_prompt(
        traceability_rows,
        section_names,
        section_readmes
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Calling {MODEL} for section matching (attempt {attempt})")

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0,  # Deterministic output
                max_tokens=2048
            )

            result = json.loads(response.choices[0].message.content)

            # Validate structure
            if not isinstance(result, dict):
                raise ValueError("Response is not a dictionary")

            for key, value in result.items():
                if not isinstance(value, list):
                    raise ValueError(f"Value for '{key}' is not a list")
                for item in value:
                    if not isinstance(item, str) or not item.startswith("US-"):
                        raise ValueError(f"Invalid story ID: {item}")

            logger.info(f"Successfully matched sections: {list(result.keys())}")
            return result

        except RateLimitError:
            wait_time = RETRY_DELAY_SECONDS * attempt
            logger.warning(f"Rate limited, waiting {wait_time}s")
            time.sleep(wait_time)

        except APIError as e:
            logger.error(f"API error: {e}")
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"LLM matching failed after {MAX_RETRIES} attempts") from e
            time.sleep(RETRY_DELAY_SECONDS)

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Invalid response: {e}")
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"LLM returned invalid response: {e}") from e
            time.sleep(RETRY_DELAY_SECONDS)

    raise RuntimeError("LLM matching failed")


# -----------------------------------------------------------------------------
# Manifest Generation
# -----------------------------------------------------------------------------

def generate_manifest(
    section_to_stories: dict[str, list[str]],
    traceability_rows: list[TraceabilityRow],
    section_names: list[str]
) -> SectionManifest:
    """
    Generate the final manifest from LLM matching results.

    Args:
        section_to_stories: From match_sections_with_llm()
        traceability_rows: Original parsed rows (for metadata)
        section_names: Original directory names (for validation)

    Returns:
        SectionManifest ready for JSON serialization
    """
    # Ensure all sections are present (even if LLM missed some)
    sections: dict[str, list[str]] = {}
    for name in section_names:
        stories = section_to_stories.get(name, [])
        # Sort and deduplicate
        sections[name] = sorted(set(stories))

    # Count total unique stories mapped
    all_stories = set()
    for stories in sections.values():
        all_stories.update(stories)

    # Count stories from traceability
    traceability_stories = set(row["story_id"] for row in traceability_rows)
    unmapped = traceability_stories - all_stories

    if unmapped:
        logger.warning(f"Stories in traceability but not mapped to any section: {unmapped}")

    return SectionManifest(
        sections=sections,
        metadata={
            "generated_by": "generate-section-manifest.py",
            "model": MODEL,
            "traceability_rows_parsed": str(len(traceability_rows)),
            "unique_stories_in_traceability": str(len(traceability_stories)),
            "unique_stories_mapped": str(len(all_stories)),
            "sections_in_export": str(len(section_names)),
            "unmapped_stories": ", ".join(sorted(unmapped)) if unmapped else "none"
        }
    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate section manifest for Design OS export"
    )
    parser.add_argument(
        "--export-dir",
        type=Path,
        required=True,
        help="Path to .charter/design-os-export directory"
    )
    parser.add_argument(
        "--ux-flows",
        type=Path,
        required=True,
        help="Path to UX-FLOWS.md"
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output path for manifest.json"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print manifest without writing to file"
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.export_dir.exists():
        logger.error(f"Export directory not found: {args.export_dir}")
        return 1

    if not args.ux_flows.exists():
        logger.error(f"UX-FLOWS.md not found: {args.ux_flows}")
        return 1

    # Initialize OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        return 1

    client = OpenAI(api_key=api_key)

    # Step 1: Parse traceability matrix
    logger.info(f"Parsing traceability matrix from {args.ux_flows}")
    traceability_rows = parse_traceability_matrix(args.ux_flows)

    if not traceability_rows:
        logger.error("No traceability data found — cannot generate manifest")
        return 1

    # Step 2: List export sections
    section_names = list_export_sections(args.export_dir)
    logger.info(f"Found {len(section_names)} section directories: {section_names}")

    if not section_names:
        logger.error("No section directories found in export")
        return 1

    # Step 3: Load section READMEs for context
    section_readmes = load_section_readmes(args.export_dir, section_names)

    # Step 4: Match with LLM
    section_to_stories = match_sections_with_llm(
        traceability_rows=traceability_rows,
        section_names=section_names,
        section_readmes=section_readmes,
        client=client
    )

    # Step 5: Generate manifest
    manifest = generate_manifest(
        section_to_stories=section_to_stories,
        traceability_rows=traceability_rows,
        section_names=section_names
    )

    # Output
    manifest_json = json.dumps(manifest, indent=2)

    if args.dry_run:
        print(manifest_json)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(manifest_json, encoding="utf-8")
        logger.info(f"Manifest written to {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
