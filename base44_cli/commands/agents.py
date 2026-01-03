"""AI agent commands for Base44 CLI."""

from typing import Optional

import typer
from rich.console import Console

from ..client import Base44Client
from ..config import ConfigManager
from ..utils.formatters import print_error, print_output, print_success

app = typer.Typer(help="AI agent operations")
console = Console()


@app.command("list")
def list_conversations(
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """List all agent conversations."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.agent_list_conversations()
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("get")
def get_conversation(
    conversation_id: str = typer.Argument(..., help="Conversation ID"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Get a specific conversation."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.agent_get_conversation(conversation_id)
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("create")
def create_conversation(
    agent_name: str = typer.Option(..., "--agent-name", help="Agent name"),
    metadata: Optional[str] = typer.Option(None, "--metadata", help="Metadata as JSON"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Create a new agent conversation."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        metadata_dict = None
        if metadata:
            import json
            metadata_dict = json.loads(metadata)

        result = client.agent_create_conversation(agent_name, metadata_dict)
        print_success(f"Created conversation: {result.get('id', 'unknown')}")
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("chat")
def send_message(
    conversation_id: str = typer.Argument(..., help="Conversation ID"),
    message: str = typer.Argument(..., help="Message to send"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Send a message to an agent."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.agent_send_message(conversation_id, message)
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("history")
def conversation_history(
    conversation_id: str = typer.Argument(..., help="Conversation ID"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Maximum number of messages"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Get conversation history."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        conversation = client.agent_get_conversation(conversation_id)

        # Extract messages from conversation
        messages = conversation.get("messages", [])
        if limit:
            messages = messages[-limit:]

        print_output(messages, format)
    except Exception as e:
        print_error(str(e))
