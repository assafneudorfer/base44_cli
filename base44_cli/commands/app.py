"""App management commands for Base44 CLI."""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from ..client import Base44Client
from ..config import ConfigManager
from ..utils.formatters import print_error, print_output, print_success

app = typer.Typer(help="App information and management")
console = Console()


@app.command("info")
def app_info(
    app_id: Optional[str] = typer.Option(None, "--app-id", help="Specific app ID to query"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Get application information."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.app_get_info(app_id)
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("entities")
def list_entities(
    app_id: Optional[str] = typer.Option(None, "--app-id", help="Specific app ID to query"),
    format: str = typer.Option("table", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """List all entities defined in the app."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        app_data = client.app_get_info(app_id)

        # Extract entities from app data
        entities = app_data.get("entities", {})

        if not entities:
            console.print("[yellow]No entities found in this app[/yellow]")
            return

        # Format entities for output
        if format == "table":
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Entity Name")
            table.add_column("Fields Count")
            table.add_column("Has Permissions")

            for entity_name, entity_config in entities.items():
                fields_count = len(entity_config.get("fields", []))
                has_perms = "Yes" if entity_config.get("permissions") else "No"
                table.add_row(entity_name, str(fields_count), has_perms)

            console.print(table)
        else:
            # For JSON/YAML, output the entities dict
            entity_list = [
                {
                    "name": name,
                    "fields": config.get("fields", []),
                    "permissions": config.get("permissions"),
                }
                for name, config in entities.items()
            ]
            print_output(entity_list, format)

    except Exception as e:
        print_error(str(e))


@app.command("pages")
def list_pages(
    app_id: Optional[str] = typer.Option(None, "--app-id", help="Specific app ID to query"),
    format: str = typer.Option("table", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """List all pages in the app."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        app_data = client.app_get_info(app_id)

        pages = app_data.get("pages", {})

        if not pages:
            console.print("[yellow]No pages found in this app[/yellow]")
            return

        # Format pages for output
        if format == "table":
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Page Name")
            table.add_column("Code Length")

            for page_name, page_code in pages.items():
                code_length = len(page_code) if page_code else 0
                table.add_row(page_name, f"{code_length:,} chars")

            console.print(table)
        else:
            # For JSON/YAML, output page names and code lengths
            page_list = [
                {"name": name, "code_length": len(code) if code else 0}
                for name, code in pages.items()
            ]
            print_output(page_list, format)

    except Exception as e:
        print_error(str(e))


@app.command("switch")
def switch_app(
    domain: str = typer.Argument(..., help="Domain name (without https://)"),
    save: bool = typer.Option(True, "--save/--no-save", help="Save as current app in config"),
) -> None:
    """Switch to a different app by domain name."""
    try:
        config_manager = ConfigManager()
        config = config_manager.load_config()
        client = Base44Client(config)

        # Get app_id from domain
        console.print(f"[blue]Looking up app ID for domain:[/blue] {domain}")
        app_id = client.app_get_id_from_domain(domain)

        console.print(f"[green]Found app ID:[/green] {app_id}")

        # Get app info to show details
        app_data = client.app_get_info(app_id)
        app_name = app_data.get("name", "Unknown")
        app_description = app_data.get("user_description", "")

        console.print(f"[bold]App Name:[/bold] {app_name}")
        if app_description:
            console.print(f"[dim]Description:[/dim] {app_description}")

        if save:
            # Get current profile
            current_profile = config_manager.get_current_profile() or "production"

            # Update the profile with new app_id
            if config_manager.config_file.exists():
                import yaml
                with open(config_manager.config_file) as f:
                    config_data = yaml.safe_load(f) or {}
            else:
                config_data = {}

            if "profiles" not in config_data:
                config_data["profiles"] = {}

            if current_profile not in config_data["profiles"]:
                config_data["profiles"][current_profile] = {}

            # Keep the existing api_key, just update app_id
            config_data["profiles"][current_profile]["app_id"] = app_id

            import yaml
            with open(config_manager.config_file, "w") as f:
                yaml.dump(config_data, f, default_flow_style=False)

            print_success(f"Switched to app: {app_name} ({app_id})")
            print_success(f"App ID saved to profile: {current_profile}")
        else:
            console.print(f"\n[yellow]App ID not saved.[/yellow] To use this app, run:")
            console.print(f"  export BASE44_APP_ID={app_id}")

    except Exception as e:
        print_error(str(e))


@app.command("details")
def app_details(
    app_id: Optional[str] = typer.Option(None, "--app-id", help="Specific app ID to query"),
) -> None:
    """Show detailed app information in a formatted view."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        app_data = client.app_get_info(app_id)

        # Display app details
        console.print("\n[bold cyan]═══ Application Details ═══[/bold cyan]\n")

        # Basic info
        console.print(f"[bold]Name:[/bold] {app_data.get('name', 'N/A')}")
        console.print(f"[bold]ID:[/bold] {app_data.get('id', 'N/A')}")
        console.print(f"[bold]Organization ID:[/bold] {app_data.get('organization_id', 'N/A')}")

        if app_data.get("user_description"):
            console.print(f"\n[bold]Description:[/bold]\n{app_data['user_description']}")

        if app_data.get("logo_url"):
            console.print(f"\n[bold]Logo:[/bold] {app_data['logo_url']}")

        # Dates
        console.print(f"\n[bold]Created:[/bold] {app_data.get('created_date', 'N/A')}")
        console.print(f"[bold]Updated:[/bold] {app_data.get('updated_date', 'N/A')}")

        # Entities
        entities = app_data.get("entities", {})
        console.print(f"\n[bold cyan]Entities ({len(entities)}):[/bold cyan]")
        for entity_name in entities.keys():
            console.print(f"  • {entity_name}")

        # Pages
        pages = app_data.get("pages", {})
        console.print(f"\n[bold cyan]Pages ({len(pages)}):[/bold cyan]")
        for page_name in pages.keys():
            console.print(f"  • {page_name}")

        console.print()

    except Exception as e:
        print_error(str(e))
