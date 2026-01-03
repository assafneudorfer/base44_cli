"""Tests for output formatters."""

import json

from base44_cli.utils.formatters import format_csv, format_output


def test_format_json() -> None:
    """Test JSON formatting."""
    data = {"key": "value", "number": 42}
    result = format_output(data, "json", pretty=False)
    assert json.loads(result) == data


def test_format_json_pretty() -> None:
    """Test pretty JSON formatting."""
    data = {"key": "value"}
    result = format_output(data, "json", pretty=True)
    assert "  " in result  # Check for indentation


def test_format_csv() -> None:
    """Test CSV formatting."""
    data = [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]
    result = format_csv(data)
    assert "id,name" in result
    assert "Alice" in result
    assert "Bob" in result


def test_format_csv_empty() -> None:
    """Test CSV formatting with empty data."""
    result = format_csv([])
    assert result == ""
