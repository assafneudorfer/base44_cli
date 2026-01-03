# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Base44 CLI is a comprehensive command-line interface for the Base44 platform. It provides direct HTTP/REST API access to all Base44 capabilities using Python and Typer framework.

**Key Technologies:**
- **CLI Framework**: Typer (Click-based)
- **HTTP Client**: httpx (synchronous)
- **Configuration**: pydantic + pydantic-settings with YAML profiles
- **Terminal UI**: Rich library for tables, colors, and formatting
- **Testing**: pytest with pytest-httpx for HTTP mocking

## Development Commands

### Installation
```bash
# Install in editable mode with dev dependencies
uv pip install -e ".[dev]"
# or
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=base44_cli --cov-report=html

# Run specific test file
pytest tests/test_client.py -v

# Run specific test
pytest tests/test_client.py::test_entity_list -v

# Run only failed tests from last run
pytest --lf
```

### Code Quality
```bash
# Format code (line length: 100)
black base44_cli/

# Check formatting without changes
black --check base44_cli/

# Lint
ruff check base44_cli/

# Auto-fix linting issues
ruff check --fix base44_cli/

# Type checking
mypy base44_cli/
```

### Running the CLI Locally
```bash
# After installing in editable mode, use directly
base44 --help

# Or run as module
python -m base44_cli.main --help

# Test with real API (requires .env setup)
base44 auth status
base44 entity list Task --limit 5
```

## Architecture

### Core Components

**1. Client Layer (`client.py`)**
- `Base44Client`: Main HTTP client wrapping httpx
- All API methods are defined here (auth, entities, functions, integrations, agents, logs, connectors, app)
- **Authentication**: Uses `api_key` header (NOT `Authorization: Bearer`)
- **Two authentication modes**:
  - User token: `headers["api_key"] = user_token`
  - Service token: `headers["api_key"] = service_token` (for admin operations)

**2. Configuration Layer (`config.py`)**
- `Config`: Pydantic model loading from environment variables with `BASE44_` prefix
- `ConfigManager`: Manages YAML profiles at `~/.base44/config.yaml`
- **Configuration priority**: Environment variables → Profile settings → Defaults
- **Profile system**: Allows switching between different apps/environments

**3. Command Layer (`commands/`)**
Each command module is a Typer app registered in `main.py`:
- `auth.py`: Authentication (login, register, invite, me)
- `entities.py`: Entity CRUD operations (list, filter, create, update, delete, bulk operations, import/export)
- `functions.py`: Backend function invocation
- `integrations.py`: Core integrations (LLM, email, file upload)
- `agents.py`: AI agent conversations
- `logs.py`: Application logs querying (requires service token)
- `connectors.py`: OAuth connector management (requires service token)
- `app.py`: App information and switching
- `config_cmd.py`: Profile management

**4. Utilities (`utils/`)**
- `formatters.py`: Output formatting (JSON, table, YAML, CSV)
- `helpers.py`: Common helper functions

### Data Flow

1. **User runs command**: `base44 entity list Task --limit 10`
2. **Typer parses**: Command routed to `entities.py:list_entities()`
3. **Config loaded**: `ConfigManager.load_config()` merges env + profile
4. **Client created**: `Base44Client(config)` with appropriate headers
5. **API called**: `client.entity_list("Task", limit=10)`
6. **Response formatted**: `print_output(result, format)` using Rich
7. **Output displayed**: JSON/table/YAML/CSV to terminal

### Authentication Pattern

**CRITICAL**: Base44 API uses `api_key` header, NOT Bearer tokens:
```python
# Correct
headers = {"api_key": user_token, "Content-Type": "application/json"}

# Wrong (do not use)
headers = {"Authorization": f"Bearer {user_token}"}
```

### API Endpoints

**Base URL**: `https://app.base44.com`

**App discovery**: `https://base44.app` (different domain for domain-to-app-id lookup)

**Pattern**: `/api/apps/{app_id}/{resource}/{operation}`

Examples:
- `/api/apps/{app_id}/auth/me`
- `/api/apps/{app_id}/entities/{entity_name}`
- `/api/apps/{app_id}/functions/{function_name}`
- `/api/apps/public/prod/by-id/{app_id}` (public endpoint)
- Domain lookup: `https://base44.app/api/apps/public/prod/domain/{domain}` (public)

### Testing Pattern

Tests use `pytest-httpx` to mock HTTP requests:

```python
from pytest_httpx import HTTPXMock

def test_entity_list(httpx_mock: HTTPXMock) -> None:
    config = Config(app_id="test-app", user_token="test-token")
    client = Base44Client(config)

    httpx_mock.add_response(
        url="https://app.base44.com/api/apps/test-app/entities/Task",
        json=[{"id": "1", "title": "Test"}]
    )

    result = client.entity_list("Task")
    assert len(result) == 1
```

## Adding New Features

### Adding a New Command

1. **Create command file** in `base44_cli/commands/`:
```python
import typer
from ..client import Base44Client
from ..config import ConfigManager

app = typer.Typer(help="Description of command group")

@app.command("action")
def my_action(param: str = typer.Option(...)) -> None:
    """Action description."""
    config = ConfigManager().load_config()
    client = Base44Client(config)
    result = client.my_api_method(param)
    print_output(result, "json")
```

2. **Add API method** to `Base44Client` in `client.py`:
```python
def my_api_method(self, param: str) -> dict[str, Any]:
    """Method description."""
    response = self.client.post(
        f"/api/apps/{self.app_id}/my-endpoint",
        json={"param": param}
    )
    response.raise_for_status()
    return response.json()
```

3. **Register command** in `main.py`:
```python
from .commands import my_commands
app.add_typer(my_commands.app, name="mygroup")
```

4. **Add tests** in `tests/test_my_commands.py`

### Adding New API Client Methods

When adding methods to `Base44Client`:
- Use type hints for all parameters and return values
- Use `self.client.get/post/put/delete()` for authenticated requests
- Use `httpx.get/post()` directly for public endpoints (like domain lookup)
- Call `response.raise_for_status()` after requests
- For service role operations, accept `use_service_role: bool = False` parameter
- Use `self._get_service_headers()` when `use_service_role=True`

## Configuration Files

### `.env` File
Users create this from `.env.example` with their credentials:
- `BASE44_APP_ID`: Application ID
- `BASE44_USER_TOKEN`: User API key (NOT a bearer token)
- `BASE44_SERVICE_TOKEN`: Service API key for admin operations
- `BASE44_SERVER_URL`: Default is `https://app.base44.com`

### `~/.base44/config.yaml` Profile System
Allows users to manage multiple apps/environments:
```yaml
default_profile: production

profiles:
  production:
    server_url: https://app.base44.com
    app_id: prod-app-123
    user_token: api-key-here
    output_format: json

  development:
    server_url: https://app.base44.com
    app_id: dev-app-456
    user_token: different-api-key
    output_format: table

timeout: 30
max_retries: 3
```

### App Switching
The `base44 app switch <domain>` command:
1. Calls `https://base44.app/api/apps/public/prod/domain/{domain}` to get app_id
2. Updates current profile's `app_id` in config.yaml
3. Keeps existing `user_token` (assumes same key works for all apps in organization)

## Output Formatting

All commands support `--format` flag:
- `json`: Machine-readable, default for scripting
- `table`: Rich tables for human reading
- `yaml`: Human-readable structured format
- `csv`: Spreadsheet-compatible (for entity exports)

Use `utils.formatters.print_output(data, format)` for consistency.

## Common Patterns

### Service Role Operations
Some endpoints require service token (logs, connectors, admin entity access):
```python
@app.command()
def admin_command() -> None:
    config = ConfigManager().load_config()
    if not config.service_token:
        raise ValueError("Service token not configured")
    client = Base44Client(config)
    result = client.entity_list("User", use_service_role=True)
```

### Import/Export
Entity import/export supports JSON and CSV:
- Use pandas for CSV reading/writing
- Validate data structure before bulk operations
- Provide progress feedback for large operations

### Export-All Feature
The `entity export-all` command exports all entities in the app:
- Calls `client.app_get_info()` to get list of entities
- Creates output directory (default: `data/`)
- Exports each entity to `{entity_name}.json`
- Creates `.entities` file with list of exported entities
- Continues on errors (skips failed entities)
- Supports `--limit` to limit records per entity

### Profile Management
Profile commands in `config_cmd.py` modify `~/.base44/config.yaml`:
- Always use `ConfigManager` methods
- Don't manually parse YAML unless necessary
- Preserve existing data when updating profiles

## Testing Requirements

- All new API methods must have corresponding tests
- Use `HTTPXMock` fixture for mocking HTTP requests
- Test both success and error cases
- Maintain 90%+ code coverage
- Type hints required for all test functions

## Documentation

When adding features, update:
- `README.md`: User-facing documentation with examples
- `TODO.md`: Add future enhancement ideas
- `APP_COMMANDS.md`: If adding app-related commands
- Docstrings: Google-style format for all public functions
