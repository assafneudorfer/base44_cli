"""Configuration management commands for Base44 CLI."""

import typer
from rich.console import Console

from ..config import ConfigManager
from ..utils.formatters import print_error, print_output, print_success

app = typer.Typer(help="Configuration management")
console = Console()


@app.command("show")
def show_config(
    format: str = typer.Option("table", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Show current configuration."""
    try:
        config_manager = ConfigManager()
        config = config_manager.load_config()

        config_data = {
            "server_url": config.server_url,
            "app_id": config.app_id,
            "user_token": "Set (hidden)" if config.user_token else "Not set",
            "service_token": "Set (hidden)" if config.service_token else "Not set",
            "output_format": config.output_format,
            "timeout": config.timeout,
            "max_retries": config.max_retries,
            "current_profile": config_manager.get_current_profile() or "None",
        }

        print_output(config_data, format)
    except Exception as e:
        print_error(str(e))


@app.command("set-profile")
def set_profile(
    profile_name: str = typer.Argument(..., help="Profile name"),
) -> None:
    """Set the default profile."""
    try:
        config_manager = ConfigManager()
        config_manager.set_profile(profile_name)
        print_success(f"Default profile set to: {profile_name}")
    except Exception as e:
        print_error(str(e))


@app.command("create-profile")
def create_profile(
    profile_name: str = typer.Argument(..., help="Profile name"),
    app_id: str = typer.Option(..., "--app-id", help="Application ID"),
    server_url: str = typer.Option("https://app.base44.com", "--server-url", help="Server URL"),
) -> None:
    """Create a new configuration profile."""
    try:
        config_manager = ConfigManager()
        config_manager.create_profile(profile_name, app_id, server_url)
        print_success(f"Profile '{profile_name}' created successfully")
    except Exception as e:
        print_error(str(e))


@app.command("list-profiles")
def list_profiles(
    format: str = typer.Option("table", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """List all available profiles."""
    try:
        config_manager = ConfigManager()
        profiles = config_manager.list_profiles()

        if not profiles:
            console.print("[yellow]No profiles configured[/yellow]")
            return

        current_profile = config_manager.get_current_profile()

        # Format profiles with current indicator
        profile_data = []
        for profile in profiles:
            is_current = " (current)" if profile == current_profile else ""
            profile_data.append({"profile": f"{profile}{is_current}"})

        print_output(profile_data, format)
    except Exception as e:
        print_error(str(e))
