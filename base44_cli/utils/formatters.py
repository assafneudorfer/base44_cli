"""Output formatting utilities."""

import csv
import json
import sys
from io import StringIO
from typing import Any

import yaml
from rich.console import Console
from rich.table import Table

console = Console()


def format_output(data: Any, format_type: str = "json", pretty: bool = True) -> str:
    """Format data according to specified format type."""
    if format_type == "json":
        if pretty:
            return json.dumps(data, indent=2, default=str)
        return json.dumps(data, default=str)
    elif format_type == "yaml":
        return yaml.dump(data, default_flow_style=False)
    elif format_type == "csv":
        return format_csv(data)
    elif format_type == "table":
        return format_table(data)
    else:
        return str(data)


def format_table(data: Any) -> str:
    """Format data as a rich table."""
    if not data:
        return "No data to display"

    # Handle list of dictionaries
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        table = Table(show_header=True, header_style="bold magenta")

        # Add columns
        keys = list(data[0].keys())
        for key in keys:
            table.add_column(key)

        # Add rows
        for item in data:
            row = [str(item.get(key, "")) for key in keys]
            table.add_row(*row)

        # Render to string
        with console.capture() as capture:
            console.print(table)
        return capture.get()

    # Handle single dictionary
    elif isinstance(data, dict):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")

        for key, value in data.items():
            table.add_row(str(key), str(value))

        with console.capture() as capture:
            console.print(table)
        return capture.get()

    else:
        return str(data)


def format_csv(data: Any) -> str:
    """Format data as CSV."""
    if not data:
        return ""

    output = StringIO()
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        keys = list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
    else:
        return str(data)


def print_output(data: Any, format_type: str = "json", pretty: bool = True) -> None:
    """Print formatted output to console."""
    if format_type == "table":
        # Table formatting uses Rich console directly
        output = format_table(data)
        print(output)
    else:
        output = format_output(data, format_type, pretty)
        print(output)


def print_error(message: str, exit_code: int = 1) -> None:
    """Print error message and exit."""
    console.print(f"[red]Error:[/red] {message}", file=sys.stderr)
    sys.exit(exit_code)


def print_success(message: str) -> None:
    """Print success message."""
    console.print(f"[green]Success:[/green] {message}")


def print_warning(message: str) -> None:
    """Print warning message."""
    console.print(f"[yellow]Warning:[/yellow] {message}")


def print_info(message: str) -> None:
    """Print info message."""
    console.print(f"[blue]Info:[/blue] {message}")
