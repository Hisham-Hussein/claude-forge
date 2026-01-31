#!/usr/bin/env python3
"""
Analyze a Python file to identify functions, inputs, outputs, and seams.
Used in the SELECT phase of characterization-first workflow.

Usage:
    python analyze_target.py <target_file.py> [--json]

Output:
    Structured analysis of the target file including:
    - Functions and classes
    - Parameters (explicit inputs)
    - Imports (potential seams)
    - Global variable access (implicit inputs)
    - File/network operations (side effects)
"""

import ast
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Set


@dataclass
class FunctionAnalysis:
    name: str
    lineno: int
    parameters: List[str]
    returns_value: bool
    calls_made: List[str] = field(default_factory=list)
    globals_accessed: List[str] = field(default_factory=list)
    potential_side_effects: List[str] = field(default_factory=list)


@dataclass
class SeamAnalysis:
    location: str
    seam_type: str  # "import", "file_io", "network", "env_var", "datetime"
    description: str
    mockable: bool = True


@dataclass
class TargetAnalysis:
    file_path: str
    functions: List[FunctionAnalysis] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    seams: List[SeamAnalysis] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class TargetAnalyzer(ast.NodeVisitor):
    """AST visitor to extract characterization-relevant information."""

    # Patterns that indicate seams
    SEAM_IMPORTS = {
        'requests': ('network', 'HTTP requests - mock responses'),
        'urllib': ('network', 'URL operations - mock responses'),
        'httpx': ('network', 'HTTP client - mock responses'),
        'aiohttp': ('network', 'Async HTTP - mock responses'),
        'os': ('env_var', 'OS operations - mock env vars and paths'),
        'pathlib': ('file_io', 'Path operations - mock filesystem'),
        'open': ('file_io', 'File operations - mock file contents'),
        'datetime': ('datetime', 'Time operations - mock current time'),
        'time': ('datetime', 'Time operations - mock sleep/time'),
        'random': ('datetime', 'Random values - mock with seed'),
        'sqlite3': ('database', 'SQLite - mock database'),
        'psycopg2': ('database', 'PostgreSQL - mock database'),
        'pymongo': ('database', 'MongoDB - mock database'),
        'redis': ('database', 'Redis - mock cache'),
        'subprocess': ('process', 'Subprocesses - mock command output'),
        'json': ('file_io', 'JSON parsing - usually no mock needed'),
    }

    SIDE_EFFECT_CALLS = {
        'open', 'write', 'print', 'logging', 'logger',
        'requests.post', 'requests.put', 'requests.delete',
        'os.remove', 'os.makedirs', 'os.rename',
        'shutil.copy', 'shutil.move', 'shutil.rmtree',
    }

    def __init__(self):
        self.analysis = TargetAnalysis(file_path="")
        self.current_function = None
        self._all_imports: Set[str] = set()

    def analyze_file(self, file_path: str) -> TargetAnalysis:
        """Analyze a Python file and return structured analysis."""
        self.analysis.file_path = file_path

        try:
            with open(file_path, 'r') as f:
                source = f.read()
        except FileNotFoundError:
            self.analysis.warnings.append(f"File not found: {file_path}")
            return self.analysis
        except Exception as e:
            self.analysis.warnings.append(f"Error reading file: {e}")
            return self.analysis

        try:
            tree = ast.parse(source)
            self.visit(tree)
        except SyntaxError as e:
            self.analysis.warnings.append(f"Syntax error: {e}")
            return self.analysis

        # Identify seams from imports
        self._identify_seams()

        return self.analysis

    def visit_Import(self, node):
        for alias in node.names:
            self.analysis.imports.append(alias.name)
            self._all_imports.add(alias.name.split('.')[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.analysis.imports.append(node.module)
            self._all_imports.add(node.module.split('.')[0])
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.analysis.classes.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        func = FunctionAnalysis(
            name=node.name,
            lineno=node.lineno,
            parameters=[arg.arg for arg in node.args.args],
            returns_value=self._has_return(node),
        )

        # Analyze function body
        self.current_function = func
        self.generic_visit(node)
        self.current_function = None

        self.analysis.functions.append(func)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Call(self, node):
        if self.current_function:
            call_name = self._get_call_name(node)
            if call_name:
                self.current_function.calls_made.append(call_name)

                # Check for side effects
                for pattern in self.SIDE_EFFECT_CALLS:
                    if pattern in call_name:
                        self.current_function.potential_side_effects.append(
                            f"Line {node.lineno}: {call_name}"
                        )
                        break

        self.generic_visit(node)

    def visit_Name(self, node):
        if self.current_function and isinstance(node.ctx, ast.Load):
            # Check if accessing a global (not a parameter or local)
            if node.id.isupper():  # Convention: CONSTANTS are globals
                self.current_function.globals_accessed.append(node.id)
        self.generic_visit(node)

    def _has_return(self, node) -> bool:
        """Check if function has a return statement with a value."""
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value is not None:
                return True
        return False

    def _get_call_name(self, node) -> str:
        """Extract the name of a function call."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            parts = []
            current = node.func
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            return '.'.join(reversed(parts))
        return ""

    def _identify_seams(self):
        """Identify seams based on imports and patterns."""
        for imp in self._all_imports:
            base_import = imp.split('.')[0]
            if base_import in self.SEAM_IMPORTS:
                seam_type, description = self.SEAM_IMPORTS[base_import]
                self.analysis.seams.append(SeamAnalysis(
                    location=f"import {imp}",
                    seam_type=seam_type,
                    description=description,
                ))

        # Check for env var access
        if 'os' in self._all_imports:
            self.analysis.seams.append(SeamAnalysis(
                location="os.environ / os.getenv",
                seam_type="env_var",
                description="Environment variables - mock with monkeypatch",
            ))


def format_text_report(analysis: TargetAnalysis) -> str:
    """Format analysis as human-readable text."""
    lines = []
    lines.append(f"# Characterization Analysis: {analysis.file_path}")
    lines.append("")

    if analysis.warnings:
        lines.append("## Warnings")
        for w in analysis.warnings:
            lines.append(f"  - {w}")
        lines.append("")

    # Functions
    lines.append("## Functions to Characterize")
    lines.append("")
    if analysis.functions:
        for func in analysis.functions:
            lines.append(f"### {func.name} (line {func.lineno})")
            lines.append(f"  Parameters: {', '.join(func.parameters) or 'none'}")
            lines.append(f"  Returns value: {'yes' if func.returns_value else 'no'}")
            if func.calls_made:
                lines.append(f"  Calls: {', '.join(list(set(func.calls_made))[:10])}")
            if func.globals_accessed:
                lines.append(f"  Globals: {', '.join(set(func.globals_accessed))}")
            if func.potential_side_effects:
                lines.append("  Side effects:")
                for se in func.potential_side_effects[:5]:
                    lines.append(f"    - {se}")
            lines.append("")
    else:
        lines.append("  No functions found.")
        lines.append("")

    # Classes
    if analysis.classes:
        lines.append("## Classes")
        for cls in analysis.classes:
            lines.append(f"  - {cls}")
        lines.append("")

    # Seams
    lines.append("## Identified Seams (Mockable Dependencies)")
    lines.append("")
    if analysis.seams:
        lines.append("| Location | Type | How to Mock |")
        lines.append("|----------|------|-------------|")
        for seam in analysis.seams:
            lines.append(f"| {seam.location} | {seam.seam_type} | {seam.description} |")
        lines.append("")
    else:
        lines.append("  No obvious seams identified. Code may be tightly coupled.")
        lines.append("")

    # Imports
    if analysis.imports:
        lines.append("## Imports")
        for imp in analysis.imports:
            lines.append(f"  - {imp}")
        lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python file for characterization testing"
    )
    parser.add_argument("target", help="Path to Python file to analyze")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not Path(args.target).exists():
        print(f"Error: File not found: {args.target}", file=sys.stderr)
        sys.exit(1)

    analyzer = TargetAnalyzer()
    analysis = analyzer.analyze_file(args.target)

    if args.json:
        # Convert to JSON-serializable dict
        output = asdict(analysis)
        print(json.dumps(output, indent=2))
    else:
        print(format_text_report(analysis))


if __name__ == "__main__":
    main()
