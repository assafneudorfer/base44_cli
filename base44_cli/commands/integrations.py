"""Integration commands for Base44 CLI."""

from typing import Optional

import typer

from ..client import Base44Client
from ..config import ConfigManager
from ..utils.formatters import print_error, print_output, print_success

app = typer.Typer(help="Integration operations")


@app.command("llm")
def invoke_llm(
    prompt: str = typer.Argument(..., help="LLM prompt"),
    response_format: str = typer.Option("text", "--format-type", help="Response format (text or json)"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Invoke LLM integration."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.integration_invoke_llm(prompt, response_format)
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("email")
def send_email(
    to: str = typer.Option(..., "--to", help="Recipient email address"),
    subject: str = typer.Option(..., "--subject", "-s", help="Email subject"),
    body: str = typer.Option(..., "--body", "-b", help="Email body"),
    sender_name: Optional[str] = typer.Option(None, "--sender-name", help="Sender name"),
    html: bool = typer.Option(False, "--html", help="Body is HTML"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Send email via Core integration."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.integration_send_email(to, subject, body, sender_name, html)
        print_success(f"Email sent to {to}")
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("upload-file")
def upload_file(
    file: str = typer.Option(..., "--file", help="File path to upload"),
    metadata: Optional[str] = typer.Option(None, "--metadata", help="File metadata as JSON"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Upload a file via Core integration."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        metadata_dict = None
        if metadata:
            import json
            metadata_dict = json.loads(metadata)

        result = client.integration_upload_file(file, metadata_dict)
        print_success(f"File uploaded: {file}")
        print_output(result, format)
    except Exception as e:
        print_error(str(e))
