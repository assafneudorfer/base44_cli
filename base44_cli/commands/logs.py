"""App logs commands for Base44 CLI."""

from typing import Optional

import typer

from ..client import Base44Client
from ..config import ConfigManager
from ..utils.formatters import print_error, print_output

app = typer.Typer(help="App logs operations")


@app.command("query")
def query_logs(
    start: Optional[str] = typer.Option(None, "--start", help="Start date (ISO format)"),
    end: Optional[str] = typer.Option(None, "--end", help="End date (ISO format)"),
    level: Optional[str] = typer.Option(None, "--level", help="Log level (error, warn, info, debug)"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Maximum number of log entries"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Query app logs."""
    try:
        config = ConfigManager().load_config()

        if not config.service_token:
            print_error("Service token required for logs operations")

        client = Base44Client(config)

        result = client.logs_query(start_date=start, end_date=end, level=level, limit=limit)
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("stats")
def log_stats(
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Get log statistics."""
    try:
        config = ConfigManager().load_config()

        if not config.service_token:
            print_error("Service token required for logs operations")

        client = Base44Client(config)

        result = client.logs_stats()
        print_output(result, format)
    except Exception as e:
        print_error(str(e))
