"""Pytest configuration for plan-phase-tasks script tests."""


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "costly: tests that call paid APIs (OpenAI, etc.) — run with: pytest -m costly",
    )
