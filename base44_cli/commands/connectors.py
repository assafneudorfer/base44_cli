"""Connector commands for Base44 CLI."""

import typer

from ..client import Base44Client
from ..config import ConfigManager
from ..utils.formatters import print_error, print_output

app = typer.Typer(help="Connector operations")


@app.command("get-token")
def get_access_token(
    connector_type: str = typer.Argument(..., help="Connector type (GoogleDrive, Slack, etc.)"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Get OAuth access token for a connector."""
    try:
        config = ConfigManager().load_config()

        if not config.service_token:
            print_error("Service token required for connector operations")

        client = Base44Client(config)

        result = client.connector_get_access_token(connector_type)
        print_output(result, format)
    except Exception as e:
        print_error(str(e))
