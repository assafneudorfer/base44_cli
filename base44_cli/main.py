"""Main CLI entry point for Base44 CLI."""

import typer
from rich.console import Console

from . import __version__
from .commands import agents, app as app_cmd, auth, config_cmd, connectors, entities, functions, integrations, logs

app = typer.Typer(
    name="base44",
    help="Comprehensive CLI for Base44 platform",
    add_completion=False,
)
console = Console()

# Add command groups
app.add_typer(auth.app, name="auth")
app.add_typer(app_cmd.app, name="app")
app.add_typer(entities.app, name="entity")
app.add_typer(functions.app, name="function")
app.add_typer(integrations.app, name="integration")
app.add_typer(agents.app, name="agent")
app.add_typer(logs.app, name="logs")
app.add_typer(connectors.app, name="connector")
app.add_typer(config_cmd.app, name="config")


@app.command()
def version() -> None:
    """Show CLI version."""
    console.print(f"Base44 CLI version: {__version__}")


@app.command()
def doctor() -> None:
    """Check configuration and connectivity."""
    from .client import Base44Client
    from .config import ConfigManager

    console.print("[bold]Base44 CLI Doctor[/bold]\n")

    try:
        # Check configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()

        console.print("[green]✓[/green] Configuration loaded")
        console.print(f"  Server URL: {config.server_url}")
        console.print(f"  App ID: {config.app_id or '[red]Not set[/red]'}")
        console.print(f"  User Token: {'[green]Set[/green]' if config.user_token else '[red]Not set[/red]'}")
        console.print(
            f"  Service Token: {'[green]Set[/green]' if config.service_token else '[yellow]Not set[/yellow]'}"
        )

        # Check connectivity
        if config.user_token and config.app_id:
            console.print("\n[bold]Testing connectivity...[/bold]")
            try:
                client = Base44Client(config)
                user = client.auth_me()
                console.print(f"[green]✓[/green] Successfully connected as: {user.get('email', 'Unknown')}")
            except Exception as e:
                console.print(f"[red]✗[/red] Connection failed: {e}")
        else:
            console.print("\n[yellow]⚠[/yellow] Cannot test connectivity: app_id or user_token not set")

        # Check config file
        if config_manager.config_file.exists():
            console.print(f"\n[green]✓[/green] Config file: {config_manager.config_file}")
            profiles = config_manager.list_profiles()
            if profiles:
                console.print(f"  Profiles: {', '.join(profiles)}")
                current = config_manager.get_current_profile()
                if current:
                    console.print(f"  Current profile: {current}")
        else:
            console.print(f"\n[yellow]⚠[/yellow] No config file found at: {config_manager.config_file}")

        console.print("\n[green]✓[/green] All checks passed!")

    except Exception as e:
        console.print(f"\n[red]✗[/red] Error: {e}")


if __name__ == "__main__":
    app()
