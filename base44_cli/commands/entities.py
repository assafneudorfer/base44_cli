"""Entity CRUD commands for Base44 CLI."""

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from ..client import Base44Client
from ..config import ConfigManager
from ..utils.formatters import print_error, print_output, print_success, print_warning
from ..utils.helpers import confirm_action, load_json_file, save_json_file

app = typer.Typer(help="Entity CRUD operations")
console = Console()


@app.command("list")
def list_records(
    entity_name: str = typer.Argument(..., help="Entity name"),
    sort: Optional[str] = typer.Option(None, "--sort", "-s", help="Sort field (prefix with - for descending)"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Maximum number of records"),
    skip: Optional[int] = typer.Option(None, "--skip", help="Number of records to skip"),
    fields: Optional[str] = typer.Option(None, "--fields", help="Comma-separated list of fields"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml, csv)"),
) -> None:
    """List records from an entity."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        if service_role and not config.service_token:
            print_error("Service token not configured")

        result = client.entity_list(
            entity_name, sort=sort, limit=limit, skip=skip, fields=fields, use_service_role=service_role
        )
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("filter")
def filter_records(
    entity_name: str = typer.Argument(..., help="Entity name"),
    query: str = typer.Option(..., "--query", "-q", help="Filter query as JSON"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Maximum number of records"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml, csv)"),
) -> None:
    """Filter entity records by query."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        query_obj = json.loads(query)
        result = client.entity_filter(entity_name, query_obj, limit=limit, use_service_role=service_role)
        print_output(result, format)
    except json.JSONDecodeError:
        print_error("Invalid JSON query")
    except Exception as e:
        print_error(str(e))


@app.command("get")
def get_record(
    entity_name: str = typer.Argument(..., help="Entity name"),
    record_id: str = typer.Argument(..., help="Record ID"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Get a specific entity record."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.entity_get(entity_name, record_id, use_service_role=service_role)
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("create")
def create_record(
    entity_name: str = typer.Argument(..., help="Entity name"),
    data: Optional[str] = typer.Option(None, "--data", "-d", help="Record data as JSON"),
    from_file: Optional[str] = typer.Option(None, "--from-file", help="Load data from JSON file"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Create a new entity record."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        # Load data
        if from_file:
            record_data = load_json_file(from_file)
        elif data:
            record_data = json.loads(data)
        else:
            print_error("Either --data or --from-file must be provided")
            return

        result = client.entity_create(entity_name, record_data, use_service_role=service_role)
        print_success(f"Created {entity_name} record: {result.get('id', 'unknown')}")
        print_output(result, format)
    except json.JSONDecodeError:
        print_error("Invalid JSON data")
    except Exception as e:
        print_error(str(e))


@app.command("update")
def update_record(
    entity_name: str = typer.Argument(..., help="Entity name"),
    record_id: str = typer.Argument(..., help="Record ID"),
    data: str = typer.Option(..., "--data", "-d", help="Update data as JSON"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Update an entity record."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        update_data = json.loads(data)
        result = client.entity_update(entity_name, record_id, update_data, use_service_role=service_role)
        print_success(f"Updated {entity_name} record: {record_id}")
        print_output(result, format)
    except json.JSONDecodeError:
        print_error("Invalid JSON data")
    except Exception as e:
        print_error(str(e))


@app.command("delete")
def delete_record(
    entity_name: str = typer.Argument(..., help="Entity name"),
    record_id: str = typer.Argument(..., help="Record ID"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Delete an entity record."""
    try:
        if not yes:
            if not confirm_action(f"Are you sure you want to delete {entity_name} record {record_id}?"):
                print_warning("Operation cancelled")
                return

        config = ConfigManager().load_config()
        client = Base44Client(config)

        result = client.entity_delete(entity_name, record_id, use_service_role=service_role)
        print_success(f"Deleted {entity_name} record: {record_id}")
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("bulk-create")
def bulk_create(
    entity_name: str = typer.Argument(..., help="Entity name"),
    from_file: str = typer.Option(..., "--from-file", help="Load records from JSON file"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Bulk create entity records."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        records = load_json_file(from_file)
        if not isinstance(records, list):
            print_error("File must contain a JSON array of records")
            return

        result = client.entity_bulk_create(entity_name, records, use_service_role=service_role)
        print_success(f"Bulk created {len(records)} {entity_name} records")
        print_output(result, format)
    except Exception as e:
        print_error(str(e))


@app.command("delete-many")
def delete_many(
    entity_name: str = typer.Argument(..., help="Entity name"),
    query: str = typer.Option(..., "--query", "-q", help="Filter query as JSON"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be deleted without deleting"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table, yaml)"),
) -> None:
    """Delete multiple entity records matching a query."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        query_obj = json.loads(query)

        if dry_run:
            # Show what would be deleted
            matching_records = client.entity_filter(entity_name, query_obj, use_service_role=service_role)
            print_warning(f"Would delete {len(matching_records)} records:")
            print_output(matching_records, format)
            return

        if not yes:
            # Show preview and ask for confirmation
            matching_records = client.entity_filter(entity_name, query_obj, use_service_role=service_role)
            print_warning(f"This will delete {len(matching_records)} records")
            if not confirm_action("Are you sure you want to proceed?"):
                print_warning("Operation cancelled")
                return

        result = client.entity_delete_many(entity_name, query_obj, use_service_role=service_role)
        print_success(f"Deleted records matching query")
        print_output(result, format)
    except json.JSONDecodeError:
        print_error("Invalid JSON query")
    except Exception as e:
        print_error(str(e))


@app.command("export")
def export_records(
    entity_name: str = typer.Argument(..., help="Entity name"),
    output: str = typer.Option(..., "--output", "-o", help="Output file path"),
    export_format: str = typer.Option("json", "--format", "-f", help="Export format (json, csv, yaml)"),
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Filter query as JSON"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Maximum number of records"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
) -> None:
    """Export entity records to a file."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        # Fetch records
        if query:
            query_obj = json.loads(query)
            records = client.entity_filter(entity_name, query_obj, limit=limit, use_service_role=service_role)
        else:
            records = client.entity_list(entity_name, limit=limit, use_service_role=service_role)

        # Save to file
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if export_format == "json":
            save_json_file(records, str(output_path))
        elif export_format == "yaml":
            import yaml
            with open(output_path, "w") as f:
                yaml.dump(records, f, default_flow_style=False)
        elif export_format == "csv":
            import csv
            if records and isinstance(records, list) and len(records) > 0:
                keys = list(records[0].keys())
                with open(output_path, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(records)
        else:
            print_error(f"Unsupported export format: {export_format}")
            return

        print_success(f"Exported {len(records)} records to {output}")
    except json.JSONDecodeError:
        print_error("Invalid JSON query")
    except Exception as e:
        print_error(str(e))


def _clean_record_for_import(record: dict) -> dict:
    """Remove system fields that shouldn't be imported."""
    # System fields that are auto-generated
    system_fields = {"id", "_id", "created_date", "updated_date", "created_at", "updated_at",
                     "created_by_id", "created_by", "is_sample"}
    return {k: v for k, v in record.items() if k not in system_fields}


@app.command("import")
def import_records(
    entity_name: str = typer.Argument(..., help="Entity name"),
    file: str = typer.Option(..., "--file", help="Input file path"),
    import_format: str = typer.Option("json", "--format", "-f", help="Import format (json, csv)"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    skip_clean: bool = typer.Option(False, "--skip-clean", help="Skip cleaning system fields"),
) -> None:
    """Import entity records from a file."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        # Load records from file
        file_path = Path(file)
        if not file_path.exists():
            print_error(f"File not found: {file}")
            return

        if import_format == "json":
            records = load_json_file(str(file_path))
        elif import_format == "csv":
            import csv
            records = []
            with open(file_path, newline="") as f:
                reader = csv.DictReader(f)
                records = list(reader)
        else:
            print_error(f"Unsupported import format: {import_format}")
            return

        if not isinstance(records, list):
            print_error("File must contain an array of records")
            return

        # Clean system fields unless skip-clean is specified
        if not skip_clean:
            records = [_clean_record_for_import(record) for record in records]
            console.print(f"[dim]Cleaned system fields from {len(records)} records[/dim]")

        # Bulk create
        console.print(f"[blue]Importing {len(records)} records...[/blue]")
        result = client.entity_bulk_create(entity_name, records, use_service_role=service_role)
        print_success(f"Imported {len(result)} records from {file}")
    except Exception as e:
        print_error(str(e))


@app.command("export-all")
def export_all_entities(
    output_dir: str = typer.Option("data", "--output-dir", "-o", help="Output directory"),
    service_role: bool = typer.Option(False, "--service-role", help="Use service role"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Maximum records per entity"),
) -> None:
    """Export all entities in the app to JSON files."""
    try:
        config = ConfigManager().load_config()
        client = Base44Client(config)

        # Get app info to retrieve all entities
        console.print("[blue]Fetching app information...[/blue]")
        app_data = client.app_get_info()
        entities = app_data.get("entities", {})

        if not entities:
            print_warning("No entities found in this app")
            return

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        entity_names = list(entities.keys())
        console.print(f"[cyan]Found {len(entity_names)} entities to export[/cyan]")

        # Export each entity
        exported_entities = []
        for entity_name in entity_names:
            try:
                console.print(f"[blue]Exporting {entity_name}...[/blue]")

                # Fetch all records for this entity
                records = client.entity_list(entity_name, limit=limit, use_service_role=service_role)

                # Save to JSON file
                entity_file = output_path / f"{entity_name}.json"
                save_json_file(records, str(entity_file))

                exported_entities.append(entity_name)
                console.print(f"[green]✓[/green] Exported {len(records)} {entity_name} records to {entity_file}")

            except Exception as e:
                console.print(f"[red]✗[/red] Failed to export {entity_name}: {e}")
                continue

        # Save .entities file with list of exported entities
        entities_file = output_path / ".entities"
        with open(entities_file, "w") as f:
            f.write("\n".join(exported_entities))

        print_success(f"Exported {len(exported_entities)} entities to {output_dir}/")
        console.print(f"[dim]Entity list saved to {entities_file}[/dim]")

    except Exception as e:
        print_error(str(e))
