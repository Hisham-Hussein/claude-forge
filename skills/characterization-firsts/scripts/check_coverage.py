#!/usr/bin/env python3
"""
Parse and report mutation testing results from mutmut.
Used in the VERIFY phase of characterization-first workflow.

Usage:
    python check_coverage.py [--json] [--show-survivors]

Requirements:
    - mutmut must have been run (creates .mutmut-cache)

Output:
    Structured report of mutation testing results including:
    - Mutation score
    - Survivor analysis
    - Recommendations
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Mutant:
    id: int
    status: str  # killed, survived, timeout, suspicious
    line: Optional[int] = None
    description: Optional[str] = None


@dataclass
class MutationReport:
    total: int
    killed: int
    survived: int
    timeout: int
    suspicious: int
    mutation_score: float
    confidence: str  # HIGH, MEDIUM, LOW
    survivors: List[Mutant]
    recommendations: List[str]


def get_mutmut_results() -> Optional[str]:
    """Get mutmut results output."""
    try:
        result = subprocess.run(
            ['mutmut', 'results'],
            capture_output=True,
            text=True,
        )
        return result.stdout
    except FileNotFoundError:
        print("Error: mutmut not found. Install with: pip install mutmut", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error running mutmut results: {e}", file=sys.stderr)
        return None


def get_mutant_details(mutant_id: int) -> Optional[str]:
    """Get details for a specific mutant."""
    try:
        result = subprocess.run(
            ['mutmut', 'show', str(mutant_id)],
            capture_output=True,
            text=True,
        )
        return result.stdout
    except Exception:
        return None


def parse_results(output: str) -> MutationReport:
    """Parse mutmut results output into structured report."""
    lines = output.strip().split('\n')

    total = 0
    killed = 0
    survived = 0
    timeout = 0
    suspicious = 0
    survivors = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Parse individual mutant lines (e.g., "1  killed", "2  survived")
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit():
            mutant_id = int(parts[0])
            status = parts[1].lower()
            total += 1

            if 'killed' in status:
                killed += 1
            elif 'survived' in status:
                survived += 1
                survivors.append(Mutant(id=mutant_id, status='survived'))
            elif 'timeout' in status:
                timeout += 1
            elif 'suspicious' in status:
                suspicious += 1

    # Calculate mutation score
    if total > 0:
        mutation_score = (killed / total) * 100
    else:
        mutation_score = 0.0

    # Determine confidence level
    if mutation_score >= 90:
        confidence = "HIGH"
    elif mutation_score >= 70:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    # Generate recommendations
    recommendations = []
    if survived > 0:
        recommendations.append(f"Investigate {survived} surviving mutant(s)")
        recommendations.append("For each survivor: run 'mutmut show <id>' to see the mutation")
        recommendations.append("Add tests to kill non-equivalent mutants")

    if confidence == "LOW":
        recommendations.append("Add more characterization tests before refactoring")
        recommendations.append("Focus on edge cases and boundary conditions")
    elif confidence == "MEDIUM":
        recommendations.append("Review survivors - may proceed with caution")
    else:
        recommendations.append("Characterization coverage is sufficient")
        recommendations.append("Safe to proceed with refactoring")

    if timeout > 0:
        recommendations.append(f"Investigate {timeout} timeout(s) - tests may be too slow")

    return MutationReport(
        total=total,
        killed=killed,
        survived=survived,
        timeout=timeout,
        suspicious=suspicious,
        mutation_score=round(mutation_score, 1),
        confidence=confidence,
        survivors=survivors,
        recommendations=recommendations,
    )


def format_text_report(report: MutationReport, show_survivors: bool = False) -> str:
    """Format report as human-readable text."""
    lines = []

    lines.append("=" * 60)
    lines.append("  MUTATION TESTING COVERAGE REPORT")
    lines.append("=" * 60)
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"  Total mutants:    {report.total}")
    lines.append(f"  Killed:           {report.killed}")
    lines.append(f"  Survived:         {report.survived}")
    lines.append(f"  Timeout:          {report.timeout}")
    if report.suspicious:
        lines.append(f"  Suspicious:       {report.suspicious}")
    lines.append("")
    lines.append(f"  Mutation Score:   {report.mutation_score}%")
    lines.append(f"  Confidence:       {report.confidence}")
    lines.append("")

    # Confidence interpretation
    if report.confidence == "HIGH":
        lines.append("  ✓ HIGH confidence - Safe to refactor")
    elif report.confidence == "MEDIUM":
        lines.append("  ⚠ MEDIUM confidence - Review survivors before refactoring")
    else:
        lines.append("  ✗ LOW confidence - More characterization tests needed")
    lines.append("")

    # Survivors
    if report.survivors and show_survivors:
        lines.append("## Surviving Mutants")
        lines.append("")
        lines.append("  These mutants were not killed by tests.")
        lines.append("  For each, determine if it's:")
        lines.append("    - Missing test: Write a test to kill it")
        lines.append("    - Equivalent mutant: Document and accept")
        lines.append("    - Dead code: Consider removal in refactor")
        lines.append("")

        for survivor in report.survivors[:20]:  # Limit to first 20
            details = get_mutant_details(survivor.id)
            lines.append(f"  Mutant #{survivor.id}:")
            if details:
                # Show first few lines of diff
                detail_lines = details.strip().split('\n')[:10]
                for dl in detail_lines:
                    lines.append(f"    {dl}")
            lines.append("")

        if len(report.survivors) > 20:
            lines.append(f"  ... and {len(report.survivors) - 20} more survivors")
            lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    for rec in report.recommendations:
        lines.append(f"  • {rec}")
    lines.append("")

    # Next steps
    lines.append("## Next Steps")
    lines.append("")
    if report.confidence == "HIGH":
        lines.append("  1. Proceed to refactoring phase")
        lines.append("  2. Make ONE change at a time")
        lines.append("  3. Run characterization tests after each change")
    elif report.confidence == "MEDIUM":
        lines.append("  1. Review each surviving mutant")
        lines.append("  2. Add tests for non-equivalent survivors")
        lines.append("  3. Re-run mutation testing")
        lines.append("  4. Proceed when satisfied with coverage")
    else:
        lines.append("  1. Add more characterization tests")
        lines.append("  2. Focus on:")
        lines.append("     - Edge cases (empty, null, boundary)")
        lines.append("     - Error conditions")
        lines.append("     - All code branches")
        lines.append("  3. Re-run mutation testing")
        lines.append("  4. Repeat until confidence is acceptable")
    lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Parse and report mutation testing results"
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--show-survivors", action="store_true",
        help="Show details of surviving mutants"
    )

    args = parser.parse_args()

    # Check if mutmut cache exists
    if not Path('.mutmut-cache').exists():
        print("Error: No mutation testing results found.", file=sys.stderr)
        print("Run mutation testing first:", file=sys.stderr)
        print("  ./run_mutation.sh <target.py> <test.py>", file=sys.stderr)
        sys.exit(1)

    # Get mutmut results
    output = get_mutmut_results()
    if not output:
        sys.exit(1)

    # Parse results
    report = parse_results(output)

    # Output
    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print(format_text_report(report, show_survivors=args.show_survivors))

    # Exit with appropriate code
    if report.confidence == "LOW":
        sys.exit(2)  # Needs more tests
    elif report.confidence == "MEDIUM":
        sys.exit(1)  # Proceed with caution
    else:
        sys.exit(0)  # Good to go


if __name__ == "__main__":
    main()
