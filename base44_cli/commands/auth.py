"""Authentication commands for Base44 CLI."""

from typing import Optional

import typer
from rich.console import Console

from ..client import Base44Client
from ..config import Config, ConfigManager
from ..utils.formatters import print_error, print_output, print_success

app = typer.Typer(help="Authentication commands")
console = Console()


@app.command()
def login(
    email: str = typer.Option(..., "--email", "-e", help="Email address"),
    password: str = typer.Option(..., "--password", "-p", help="Password", prompt=True, hide_input=True),
    save: bool = typer.Option(False, "--save", "-s", help="Save token to config"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Login with email and password."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.auth_login(email, password)

        if save and "access_token" in result:
            ConfigManager().save_token(result["access_token"])
            print_success(f"Logged in as {email} and saved token")
        else:
            print_success(f"Logged in as {email}")

        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command()
def register(
    email: str = typer.Option(..., "--email", "-e", help="Email address"),
    password: str = typer.Option(..., "--password", "-p", help="Password", prompt=True, hide_input=True),
    save: bool = typer.Option(False, "--save", "-s", help="Save token to config"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Register a new user."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.auth_register(email, password)

        if save and "access_token" in result:
            ConfigManager().save_token(result["access_token"])
            print_success(f"Registered as {email} and saved token")
        else:
            print_success(f"Registered as {email}")

        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command()
def me(
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Get current user information."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.auth_me()
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command()
def update(
    name: Optional[str] = typer.Option(None, "--name", help="Update user name"),
    data: Optional[str] = typer.Option(None, "--data", help="JSON data to update"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Update current user profile."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        update_data = {}
        if data:
            import json
            update_data = json.loads(data)
        if name:
            update_data["name"] = name

        if not update_data:
            print_error("No data provided to update")

        result = client.auth_update_me(update_data)
        print_success("User profile updated")
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command()
def invite(
    email: str = typer.Option(..., "--email", "-e", help="Email address to invite"),
    role: str = typer.Option("user", "--role", "-r", help="User role"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Invite a user to the app."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.auth_invite(email, role)
        print_success(f"Invitation sent to {email}")
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("set-token")
def set_token(
    token: str = typer.Argument(..., help="Authentication token"),
    token_type: str = typer.Option("user", "--type", "-t", help="Token type (user or service)"),
) -> None:
    """Set authentication token manually."""
    try:
        ConfigManager().save_token(token, token_type)
        print_success(f"{token_type.capitalize()} token saved successfully")
    except Exception as e:
        print_error(str(e))


@app.command()
def status(
    format: str = typer.Option("table", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Check authentication status."""
    try:
        config = ConfigManager().load_config()

        status_data = {
            "server_url": config.server_url,
            "app_id": config.app_id,
            "user_token": "Set" if config.user_token else "Not set",
            "service_token": "Set" if config.service_token else "Not set",
        }

        # Try to get current user if token is set
        if config.user_token:
            try:
                client = Base44Client(config)
                user = client.auth_me()
                status_data["authenticated_as"] = user.get("email", "Unknown")
                status_data["user_id"] = user.get("id", "Unknown")
            except Exception:
                status_data["authenticated_as"] = "Invalid token"

        print_output(status_data, format)
    except Exception as e:
        print_error(str(e))
