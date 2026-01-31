"""
Tool Contract Template

Copy this template for each tool in your LLM application.
Fill in the sections and delete this docstring.
"""

from typing import TypedDict


class ToolResult(TypedDict):
    """Return type for successful execution."""
    result: str  # Primary result
    metadata: dict  # Optional metadata


class ToolError(TypedDict):
    """Return type for errors."""
    error: str  # What went wrong
    suggestion: str  # How to fix or work around


def tool_name(
    required_param: str,
    optional_param: int = 10
) -> ToolResult | ToolError:
    """
    One-line description of what this tool does.

    Args:
        required_param: Description of this parameter
        optional_param: Description with default behavior (default: 10)

    Returns:
        ToolResult with {result, metadata} on success
        ToolError with {error, suggestion} on failure

    Example:
        >>> tool_name("input", optional_param=5)
        {"result": "...", "metadata": {...}}
    """
    # 1. Validate inputs (fail fast)
    if not required_param:
        return {
            "error": "required_param cannot be empty",
            "suggestion": "Provide a non-empty string value"
        }

    if optional_param < 1 or optional_param > 100:
        return {
            "error": f"optional_param must be 1-100, got {optional_param}",
            "suggestion": "Use a value between 1 and 100"
        }

    # 2. Execute operation
    try:
        result = do_the_thing(required_param, optional_param)
    except RateLimitError:
        return {
            "error": "Rate limit exceeded",
            "suggestion": "Wait 60 seconds before retrying, or use batch endpoint"
        }
    except Exception as e:
        return {
            "error": f"Operation failed: {str(e)}",
            "suggestion": "Check input format and try again"
        }

    # 3. Return structured result
    return {
        "result": result,
        "metadata": {
            "param_used": optional_param,
            "timestamp": "..."
        }
    }


def do_the_thing(param1: str, param2: int) -> str:
    """Placeholder for actual implementation."""
    raise NotImplementedError


class RateLimitError(Exception):
    """Placeholder exception."""
    pass
