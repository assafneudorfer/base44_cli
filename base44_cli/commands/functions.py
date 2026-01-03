"""Backend function commands for Base44 CLI."""

import json
from typing import Optional

import typer

from ..client import Base44Client
from ..config import ConfigManager
from ..utils.formatters import print_error, print_output, print_success
from ..utils.helpers import load_json_file

app = typer.Typer(help="Backend function operations")


@app.command("invoke")
def invoke_function(
    function_name: str = typer.Argument(..., help="Function name"),
    params: Optional[str] = typer.Option(None, "--params", "-p", help="Function parameters as JSON"),
    from_file: Optional[str] = typer.Option(None, "--from-file", help="Load parameters from JSON file"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Invoke a backend function."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        # Load parameters
        if from_file:
            function_params = load_json_file(from_file)
        elif params:
            function_params = json.loads(params)
        else:
            function_params = {}

        result = client.function_invoke(function_name, function_params, use_service_role=service_role)
        print_success(f"Function '{function_name}' executed successfully")
        print_output(result, format)
    except json.JSONDecodeError:
        print_error("Invalid JSON parameters")
    except Exception as e:
        print_error(str(e))
