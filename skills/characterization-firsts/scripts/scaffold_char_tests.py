#!/usr/bin/env python3
"""
Scaffold characterization test files from target analysis.
Used in the CAPTURE phase of characterization-first workflow.

Usage:
    python scaffold_char_tests.py <target_file.py> [--output <test_file.py>]

Output:
    A pytest test file skeleton with:
    - Test class structure
    - Placeholder tests for each function
    - Mock setup for identified seams
    - Docstrings explaining characterization testing
"""

import ast
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Set


def get_module_path(file_path: str) -> str:
    """Convert file path to Python module import path."""
    path = Path(file_path)
    parts = list(path.with_suffix('').parts)

    # Remove common prefixes
    while parts and parts[0] in ('.', '..', 'src', 'lib'):
        parts.pop(0)

    return '.'.join(parts)


def extract_functions(file_path: str) -> List[dict]:
    """Extract function definitions from a Python file."""
    functions = []

    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return functions

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip private/dunder methods for initial scaffold
            if node.name.startswith('__') and node.name.endswith('__'):
                continue

            functions.append({
                'name': node.name,
                'lineno': node.lineno,
                'params': [arg.arg for arg in node.args.args if arg.arg != 'self'],
                'is_async': isinstance(node, ast.AsyncFunctionDef),
                'is_method': any(arg.arg == 'self' for arg in node.args.args),
            })

    return functions


def extract_classes(file_path: str) -> List[str]:
    """Extract class names from a Python file."""
    classes = []

    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception:
        return classes

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return classes


def extract_imports(file_path: str) -> Set[str]:
    """Extract imports that might need mocking."""
    mockable = set()
    mock_candidates = {
        'requests', 'httpx', 'aiohttp', 'urllib',
        'os', 'pathlib', 'open',
        'datetime', 'time',
        'sqlite3', 'psycopg2', 'pymongo', 'redis',
        'subprocess', 'shutil',
    }

    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception:
        return mockable

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base = alias.name.split('.')[0]
                if base in mock_candidates:
                    mockable.add(base)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                base = node.module.split('.')[0]
                if base in mock_candidates:
                    mockable.add(base)

    return mockable


def generate_test_file(
    target_path: str,
    functions: List[dict],
    classes: List[str],
    mockable_imports: Set[str],
) -> str:
    """Generate the test file content."""
    module_path = get_module_path(target_path)
    target_name = Path(target_path).stem
    timestamp = datetime.now().strftime("%Y-%m-%d")

    lines = []

    # Header
    lines.append('"""')
    lines.append(f"Characterization tests for {target_path}")
    lines.append("")
    lines.append("IMPORTANT: These tests capture CURRENT behavior, including bugs.")
    lines.append("DO NOT 'fix' failing tests - they document actual behavior.")
    lines.append("")
    lines.append(f"Generated: {timestamp}")
    lines.append(f"Target: {target_path}")
    lines.append("")
    lines.append("Before modifying target code:")
    lines.append("1. Run these tests - they should all pass")
    lines.append("2. Make ONE small change to target")
    lines.append("3. Run tests again")
    lines.append("4. If tests fail unexpectedly, characterization was incomplete")
    lines.append('"""')
    lines.append("")

    # Imports
    lines.append("import pytest")
    if mockable_imports:
        lines.append("from unittest.mock import Mock, patch, MagicMock")
    lines.append("")

    # Try to import the target module
    lines.append("# Import target module")
    lines.append(f"# Adjust this import path as needed for your project structure")
    if functions:
        func_names = [f['name'] for f in functions if not f['is_method']]
        if func_names:
            lines.append(f"# from {module_path} import {', '.join(func_names[:5])}")
    if classes:
        lines.append(f"# from {module_path} import {', '.join(classes[:3])}")
    lines.append("")
    lines.append("")

    # Fixtures for mocks
    if mockable_imports:
        lines.append("# ============================================================")
        lines.append("# FIXTURES - Mock external dependencies")
        lines.append("# ============================================================")
        lines.append("")

        for imp in sorted(mockable_imports):
            if imp == 'requests':
                lines.append("@pytest.fixture")
                lines.append("def mock_requests(mocker):")
                lines.append('    """Mock HTTP requests - configure return values per test."""')
                lines.append(f"    mock = mocker.patch('{module_path}.requests')")
                lines.append("    mock.get.return_value.status_code = 200")
                lines.append("    mock.get.return_value.json.return_value = {}")
                lines.append("    return mock")
                lines.append("")
            elif imp == 'os':
                lines.append("@pytest.fixture")
                lines.append("def mock_env(monkeypatch):")
                lines.append('    """Mock environment variables."""')
                lines.append("    # monkeypatch.setenv('VAR_NAME', 'value')")
                lines.append("    pass")
                lines.append("")
            elif imp in ('datetime', 'time'):
                lines.append("@pytest.fixture")
                lines.append("def mock_datetime(mocker):")
                lines.append('    """Mock current time for deterministic tests."""')
                lines.append("    # from datetime import datetime")
                lines.append("    # mock = mocker.patch(f'{module_path}.datetime')")
                lines.append("    # mock.now.return_value = datetime(2024, 1, 15, 12, 0, 0)")
                lines.append("    pass")
                lines.append("")

        lines.append("")

    # Test class
    class_name = ''.join(word.capitalize() for word in target_name.split('_'))
    lines.append("# ============================================================")
    lines.append(f"# CHARACTERIZATION TESTS - {target_name}")
    lines.append("# ============================================================")
    lines.append("")
    lines.append(f"class TestCharacterization{class_name}:")
    lines.append('    """')
    lines.append(f"    Characterization tests for {target_path}")
    lines.append("")
    lines.append("    These tests document CURRENT behavior. When refactoring:")
    lines.append("    - All tests should pass before AND after changes")
    lines.append("    - If a test fails, your refactor changed behavior")
    lines.append("    - Add new tests for edge cases you discover")
    lines.append('    """')
    lines.append("")

    # Generate test stubs for each function
    if functions:
        for func in functions:
            test_name = f"test_{func['name']}_basic"
            params_str = ', '.join(func['params']) if func['params'] else ''

            lines.append(f"    def {test_name}(self):")
            lines.append(f'        """')
            lines.append(f"        Characterization: {func['name']} basic behavior")
            lines.append(f"        Target line: {func['lineno']}")
            lines.append(f'        """')
            lines.append(f"        # TODO: Capture actual behavior")
            lines.append(f"        #")
            lines.append(f"        # Setup")
            if func['params']:
                lines.append(f"        # {params_str} = ...")
            lines.append(f"        #")
            lines.append(f"        # Execute")
            if func['is_async']:
                lines.append(f"        # result = await {func['name']}({params_str})")
            else:
                lines.append(f"        # result = {func['name']}({params_str})")
            lines.append(f"        #")
            lines.append(f"        # Characterize (capture ACTUAL output)")
            lines.append(f"        # assert result == ...  # Fill with actual value")
            lines.append(f"        pytest.skip('TODO: Implement characterization')")
            lines.append("")

            # Add edge case placeholder
            lines.append(f"    def test_{func['name']}_edge_cases(self):")
            lines.append(f'        """')
            lines.append(f"        Characterization: {func['name']} edge cases")
            lines.append(f"        ")
            lines.append(f"        Test with:")
            lines.append(f"        - Empty inputs")
            lines.append(f"        - None values")
            lines.append(f"        - Boundary values")
            lines.append(f'        """')
            lines.append(f"        pytest.skip('TODO: Add edge case characterization')")
            lines.append("")
    else:
        lines.append("    def test_placeholder(self):")
        lines.append('        """No functions found - add tests manually."""')
        lines.append("        pytest.skip('Add characterization tests')")
        lines.append("")

    # Known bugs section
    lines.append("")
    lines.append("# ============================================================")
    lines.append("# KNOWN BUGS - Document bugs as 'expected' behavior")
    lines.append("# ============================================================")
    lines.append("")
    lines.append(f"class TestKnownBugs{class_name}:")
    lines.append('    """')
    lines.append("    Tests that document KNOWN BUGS in current behavior.")
    lines.append("")
    lines.append("    These tests assert the BUGGY output, not the correct output.")
    lines.append("    Fix bugs AFTER refactoring is complete, not during.")
    lines.append('    """')
    lines.append("")
    lines.append("    def test_example_known_bug(self):")
    lines.append('        """')
    lines.append("        KNOWN BUG: [Describe the bug]")
    lines.append("")
    lines.append("        Current behavior: [what it does]")
    lines.append("        Expected behavior: [what it should do]")
    lines.append("        Fix planned for: After refactoring")
    lines.append('        """')
    lines.append("        pytest.skip('No known bugs documented yet')")
    lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold characterization tests for a Python file"
    )
    parser.add_argument("target", help="Path to Python file to characterize")
    parser.add_argument(
        "--output", "-o",
        help="Output path for test file (default: tests/characterization/test_<name>_char.py)"
    )

    args = parser.parse_args()

    target_path = Path(args.target)
    if not target_path.exists():
        print(f"Error: File not found: {args.target}", file=sys.stderr)
        sys.exit(1)

    if not target_path.suffix == '.py':
        print(f"Error: Target must be a Python file: {args.target}", file=sys.stderr)
        sys.exit(1)

    # Extract information from target
    functions = extract_functions(str(target_path))
    classes = extract_classes(str(target_path))
    mockable = extract_imports(str(target_path))

    # Generate test file
    test_content = generate_test_file(
        str(target_path),
        functions,
        classes,
        mockable,
    )

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(f"tests/characterization/test_{target_path.stem}_char.py")

    # Create directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write test file
    output_path.write_text(test_content)
    print(f"Created: {output_path}")
    print(f"  Functions: {len(functions)}")
    print(f"  Classes: {len(classes)}")
    print(f"  Mockable imports: {', '.join(mockable) or 'none'}")


if __name__ == "__main__":
    main()
