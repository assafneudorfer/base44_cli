# Claude Code Prompt: Build Base44 CLI Tool (HTTP/REST-based)

## Project Overview
Build a comprehensive, production-ready Command Line Interface (CLI) for Base44 platform that uses **direct HTTP/REST API calls** (not the JavaScript SDK) to provide access to all major Base44 capabilities through an intuitive command-line interface.

**Important**: This CLI uses reverse-engineered REST endpoints since Base44 doesn't provide official API documentation. See `base44_rest_api_endpoints.md` for the complete API reference.

## Technology Stack
- **Language**: Python 3.11+
- **CLI Framework**: Click or Typer (recommend Typer for better type hints)
- **HTTP Client**: httpx (for async support and modern HTTP/2)
- **Configuration**: python-dotenv for env vars, YAML for config files
- **Output Formatting**: Rich (for beautiful terminal output, tables, progress bars)
- **Testing**: pytest with pytest-httpx for mocking HTTP requests
- **Package Management**: UV (as specified in user preferences)

## Key Design Principle
**All operations must use direct HTTP requests to Base44's REST API endpoints, not the @base44/sdk JavaScript package.**

## Core Requirements

### 1. HTTP Client Implementation

Create a Base44 HTTP client class that handles all API communication:

```python
# base44_cli/client.py
import httpx
from typing import Optional, Dict, Any, List
from .config import Config

class Base44Client:
    """HTTP client for Base44 REST API"""
    
    BASE_URL = "https://base44.app"
    
    def __init__(self, config: Config):
        self.config = config
        self.app_id = config.app_id
        self.user_token = config.user_token
        self.service_token = config.service_token
        
        # Create httpx client with default headers
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=30.0,
            headers=self._get_default_headers()
        )
    
    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers for all requests"""
        headers = {
            "Content-Type": "application/json",
            "Base44-App-Id": self.app_id
        }
        
        if self.user_token:
            headers["Authorization"] = f"Bearer {self.user_token}"
        
        return headers
    
    def _get_service_headers(self) -> Dict[str, str]:
        """Get headers for service role operations"""
        headers = self._get_default_headers()
        if self.service_token:
            headers["Base44-Service-Authorization"] = f"Bearer {self.service_token}"
            # Remove user Authorization for service role
            headers.pop("Authorization", None)
        return headers
    
    # Auth endpoints
    def auth_me(self) -> Dict[str, Any]:
        """Get current user info"""
        response = self.client.get(f"/api/apps/{self.app_id}/auth/me")
        response.raise_for_status()
        return response.json()
    
    def auth_login(self, email: str, password: str, turnstile_token: Optional[str] = None) -> Dict[str, Any]:
        """Login with email/password"""
        response = self.client.post(
            f"/api/apps/{self.app_id}/auth/login",
            json={
                "email": email,
                "password": password,
                "turnstile_token": turnstile_token
            }
        )
        response.raise_for_status()
        return response.json()
    
    # Entity endpoints
    def entity_list(self, entity_name: str, sort: Optional[str] = None, 
                   limit: Optional[int] = None, skip: Optional[int] = None,
                   use_service_role: bool = False) -> List[Dict[str, Any]]:
        """List entity records"""
        params = {}
        if sort:
            params["sort"] = sort
        if limit:
            params["limit"] = limit
        if skip:
            params["skip"] = skip
        
        headers = self._get_service_headers() if use_service_role else None
        
        response = self.client.get(
            f"/api/apps/{self.app_id}/entities/{entity_name}",
            params=params,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    def entity_filter(self, entity_name: str, query: Dict[str, Any], 
                     limit: Optional[int] = None,
                     use_service_role: bool = False) -> List[Dict[str, Any]]:
        """Filter entity records"""
        headers = self._get_service_headers() if use_service_role else None
        
        response = self.client.post(
            f"/api/apps/{self.app_id}/entities/{entity_name}/filter",
            json={"query": query, "limit": limit},
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    def entity_get(self, entity_name: str, record_id: str,
                  use_service_role: bool = False) -> Dict[str, Any]:
        """Get specific entity record"""
        headers = self._get_service_headers() if use_service_role else None
        
        response = self.client.get(
            f"/api/apps/{self.app_id}/entities/{entity_name}/{record_id}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    def entity_create(self, entity_name: str, data: Dict[str, Any],
                     use_service_role: bool = False) -> Dict[str, Any]:
        """Create entity record"""
        headers = self._get_service_headers() if use_service_role else None
        
        response = self.client.post(
            f"/api/apps/{self.app_id}/entities/{entity_name}",
            json=data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    def entity_update(self, entity_name: str, record_id: str, data: Dict[str, Any],
                     use_service_role: bool = False) -> Dict[str, Any]:
        """Update entity record"""
        headers = self._get_service_headers() if use_service_role else None
        
        response = self.client.put(
            f"/api/apps/{self.app_id}/entities/{entity_name}/{record_id}",
            json=data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    def entity_delete(self, entity_name: str, record_id: str,
                     use_service_role: bool = False) -> Dict[str, Any]:
        """Delete entity record"""
        headers = self._get_service_headers() if use_service_role else None
        
        response = self.client.delete(
            f"/api/apps/{self.app_id}/entities/{entity_name}/{record_id}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    # Function endpoints
    def function_invoke(self, function_name: str, params: Dict[str, Any],
                       use_service_role: bool = False) -> Dict[str, Any]:
        """Invoke backend function"""
        headers = self._get_service_headers() if use_service_role else None
        
        response = self.client.post(
            f"/api/apps/{self.app_id}/functions/{function_name}",
            json=params,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    # Integration endpoints
    def integration_invoke_llm(self, prompt: str, response_format: str = "text") -> Dict[str, Any]:
        """Invoke LLM integration"""
        response = self.client.post(
            f"/api/apps/{self.app_id}/integrations/Core/InvokeLLM",
            json={"prompt": prompt, "responseFormat": response_format}
        )
        response.raise_for_status()
        return response.json()
    
    def integration_send_email(self, to: str, subject: str, body: str,
                              sender_name: Optional[str] = None) -> Dict[str, Any]:
        """Send email via Core integration"""
        response = self.client.post(
            f"/api/apps/{self.app_id}/integrations/Core/SendEmail",
            json={
                "to": to,
                "subject": subject,
                "body": body,
                "senderName": sender_name
            }
        )
        response.raise_for_status()
        return response.json()
    
    def __del__(self):
        """Close HTTP client on cleanup"""
        self.client.close()
```

### 2. Architecture & Design

Create a modular CLI with the following structure:
```
base44-cli/
├── base44_cli/
│   ├── __init__.py
│   ├── main.py              # Main CLI entry point
│   ├── config.py            # Configuration management
│   ├── client.py            # Base44 SDK client wrapper
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication commands
│   │   ├── entities.py      # Entity CRUD operations
│   │   ├── functions.py     # Backend function operations
│   │   ├── integrations.py  # Integration commands
│   │   ├── agents.py        # AI agent operations
│   │   └── logs.py          # App logs queries
│   ├── utils/
│   │   ├── formatters.py    # Output formatting utilities
│   │   ├── validators.py    # Input validation
│   │   └── helpers.py       # Common utilities
│   └── models.py            # Data models/schemas
├── tests/
│   ├── test_auth.py
│   ├── test_entities.py
│   └── ...
├── pyproject.toml
├── README.md
└── .env.example
```

### 2. Configuration Management

Implement flexible configuration supporting:

**Environment Variables** (.env file):
```bash
BASE44_SERVER_URL=https://base44.app
BASE44_APP_ID=your-app-id
BASE44_USER_TOKEN=your-user-token
BASE44_SERVICE_TOKEN=your-service-token  # Optional
BASE44_OUTPUT_FORMAT=json  # json, table, yaml
```

**Config File** (~/.base44/config.yaml):
```yaml
default_profile: production

profiles:
  production:
    server_url: https://base44.app
    app_id: prod-app-123
    output_format: json
  
  development:
    server_url: https://base44.app
    app_id: dev-app-456
    output_format: table

# Global settings
timeout: 30
max_retries: 3
```

**Profile Management**:
```bash
# Switch between profiles
base44 config profile set production
base44 config profile list
base44 config profile create staging --app-id=staging-123

# View current configuration
base44 config show
```

### 3. Command Structure

#### Authentication Commands
```bash
# Login with email/password
base44 auth login --email user@example.com --password <password>

# Login and save token
base44 auth login --email user@example.com --password <password> --save

# Set token manually
base44 auth set-token <token>

# Get current user info
base44 auth me

# Update current user
base44 auth update --name "John Doe"

# Logout
base44 auth logout

# Invite user
base44 auth invite --email newuser@example.com --role user

# Register new user
base44 auth register --email user@example.com --password <password> --name "User"

# Check authentication status
base44 auth status
```

#### Entity Commands
```bash
# List all entities in the app
base44 entity list-types

# List records from an entity
base44 entity list Task
base44 entity list Task --limit 10 --sort "-created_date"
base44 entity list Task --fields id,title,status

# Filter records
base44 entity filter Task --query '{"status": "pending"}'
base44 entity filter Product --query '{"category": ["electronics"]}' --limit 5

# Get specific record
base44 entity get Task task-123

# Create record
base44 entity create Task --data '{"title": "New task", "status": "pending"}'
base44 entity create Task --from-file task.json

# Update record
base44 entity update Task task-123 --data '{"status": "completed"}'

# Delete record
base44 entity delete Task task-123

# Bulk operations
base44 entity bulk-create Task --from-file tasks.json
base44 entity delete-many Task --query '{"status": "archived"}'

# Export to file
base44 entity export Task --output tasks.csv --format csv
base44 entity export Task --output tasks.json --format json

# Import from file
base44 entity import Task --file tasks.csv --format csv

# Service role operations
base44 entity list User --service-role
```

#### Function Commands
```bash
# List available functions
base44 function list

# Invoke function without params
base44 function invoke myFunction

# Invoke with parameters
base44 function invoke processOrder --params '{"orderId": "123", "action": "fulfill"}'
base44 function invoke calculateTotal --from-file params.json

# Service role execution
base44 function invoke adminFunction --service-role

# View function logs
base44 function logs myFunction --tail 50
```

#### Integration Commands
```bash
# List available integrations
base44 integration list

# Core integrations
base44 integration llm "Write a welcome email for new users"
base44 integration llm --prompt "Summarize this text" --format json

base44 integration email send \
  --to user@example.com \
  --subject "Welcome" \
  --body "Hello!" \
  --html

base44 integration upload-file --file image.png --metadata '{"type": "avatar"}'

# Custom integrations
base44 integration invoke CustomPackage.CustomEndpoint --params '{"key": "value"}'

# Integration catalog
base44 integration catalog list
base44 integration catalog search stripe
base44 integration catalog info Resend
```

#### AI Agent Commands
```bash
# List agents
base44 agent list

# Send message to agent
base44 agent chat agent-123 "Help me organize my tasks"

# Interactive chat mode
base44 agent chat agent-123 --interactive

# Get conversation history
base44 agent history agent-123
base44 agent history agent-123 --limit 20

# Create agent
base44 agent create "Task Assistant" \
  --instructions "Help users manage their tasks" \
  --tools entities,web_search

# Update agent
base44 agent update agent-123 --instructions "New instructions"

# Delete agent
base44 agent delete agent-123

# Export conversation
base44 agent export agent-123 --output conversation.json
```

#### Logs Commands
```bash
# Query app logs
base44 logs query --start 2024-01-01 --end 2024-01-31

# Filter by level
base44 logs query --level error --limit 100

# Tail logs in real-time
base44 logs tail --follow

# Get specific log entry
base44 logs get log-id-123

# Export logs
base44 logs export --output app-logs.json --start 2024-01-01
```

#### Connector Commands
```bash
# List available connectors
base44 connector list

# List authorized connectors
base44 connector list --authorized

# Get connector info
base44 connector info GoogleDrive

# Authorize connector (opens browser for OAuth)
base44 connector auth Slack

# Revoke connector
base44 connector revoke Slack

# Test connector
base44 connector test GoogleDrive
```

### 4. Output Formatting

Support multiple output formats with Rich library:

```bash
# JSON output (default)
base44 entity list Task --format json

# Table output
base44 entity list Task --format table

# YAML output
base44 entity list Task --format yaml

# CSV output
base44 entity list Task --format csv

# Quiet mode (minimal output)
base44 entity list Task --quiet

# Pretty JSON
base44 entity list Task --format json --pretty

# No color (for piping)
base44 entity list Task --no-color
```

**Rich Terminal Features**:
- Progress bars for bulk operations
- Colored output for status (green=success, red=error, yellow=warning)
- Tables with borders and headers
- Syntax highlighting for JSON/YAML
- Interactive prompts when needed

### 5. Advanced Features

#### Scripting & Automation
```bash
# JSON output for scripting
tasks=$(base44 entity filter Task --query '{"status": "pending"}' --format json)

# Pipe to jq
base44 entity list Task --format json | jq '.[] | select(.priority == "high")'

# Batch processing
for id in $(base44 entity list Task --format json | jq -r '.[].id'); do
  base44 entity update Task $id --data '{"reviewed": true}'
done
```

#### Interactive Mode
```bash
# Interactive entity explorer
base44 entity explore

# Interactive prompts for complex operations
base44 entity create Task  # Will prompt for required fields
```

#### Watch Mode
```bash
# Watch for changes
base44 entity watch Task --interval 5

# Trigger command on changes
base44 entity watch Task --exec "echo 'Task updated'"
```

#### Bulk Operations with Progress
```bash
# Show progress bar for bulk operations
base44 entity bulk-create Task --file 1000-tasks.json --progress

# Parallel execution
base44 entity bulk-update Task --file updates.json --workers 5
```

#### Validation & Dry Run
```bash
# Validate data before creation
base44 entity create Task --data '{"title": "Test"}' --validate

# Dry run (show what would happen)
base44 entity delete-many Task --query '{"old": true}' --dry-run
```

### 6. Error Handling

Implement robust error handling:

```python
# Proper error messages
class Base44CLIError(Exception):
    pass

class AuthenticationError(Base44CLIError):
    pass

class EntityNotFoundError(Base44CLIError):
    pass

# User-friendly error messages
try:
    result = client.entities.Task.get(task_id)
except EntityNotFoundError:
    console.print(f"[red]Error:[/red] Task '{task_id}' not found")
    sys.exit(1)
except AuthenticationError:
    console.print("[red]Error:[/red] Not authenticated. Run 'base44 auth login' first")
    sys.exit(1)
```

Error handling should:
- Show clear, actionable error messages
- Suggest fixes when possible
- Provide debug mode with `--verbose` flag
- Log errors to file in debug mode
- Return appropriate exit codes

### 7. Testing Requirements

Implement comprehensive testing:

```python
# Unit tests for all commands
def test_entity_list():
    result = runner.invoke(cli, ['entity', 'list', 'Task'])
    assert result.exit_code == 0

# Integration tests with mock server
@pytest.fixture
def mock_base44():
    with requests_mock.Mocker() as m:
        m.get('https://base44.app/api/entities/Task', json=[...])
        yield m

# Test error scenarios
def test_entity_not_found():
    result = runner.invoke(cli, ['entity', 'get', 'Task', 'nonexistent'])
    assert result.exit_code == 1
    assert 'not found' in result.output.lower()
```

### 8. Documentation

Include comprehensive documentation:

**README.md**:
- Installation instructions
- Quick start guide
- Configuration guide
- Command reference (auto-generated)
- Examples for common use cases
- Troubleshooting section

**Help System**:
```bash
# Built-in help for every command
base44 --help
base44 entity --help
base44 entity list --help

# Examples in help
base44 entity create --help
# Should show usage examples
```

### 9. Performance Considerations

- Implement connection pooling for HTTP requests
- Cache configuration to avoid repeated file reads
- Lazy load modules to improve startup time
- Support batch operations to reduce API calls
- Add timeout and retry logic for all API calls

### 10. Security

- Never log tokens or sensitive data
- Securely store tokens using system keyring (optional)
- Validate all user inputs
- Support for environment variable token injection
- Clear warnings when using service role

### 11. User Experience

- Colorful, informative output
- Progress indicators for long operations
- Confirmations for destructive operations (delete, bulk delete)
- Smart defaults (e.g., auto-detect format from file extension)
- Shell completion (bash, zsh, fish)
- Emoji support for status indicators ✅ ❌ ⚠️

### 12. Special Requirements

**Based on Base44 API constraints**:

1. User entity operations:
   - Warn that users can't be created via entity commands
   - Redirect to `base44 auth invite` or `base44 auth register`

2. Service role operations:
   - Validate that service token is configured
   - Show warnings about security implications
   - Don't allow auth module operations with service role

3. Integration credits:
   - Show credit cost warnings for expensive operations (LLM, agents)
   - Option to display remaining credits

4. Backend functions:
   - Check if backend functions are enabled
   - Provide helpful error if not (suggest enabling in dashboard)

### 13. Package Distribution

**Setup for distribution**:
```toml
[project]
name = "base44-cli"
version = "0.1.0"
description = "Comprehensive CLI for Base44 platform"
dependencies = [
    "click>=8.1.0",
    "rich>=13.0.0",
    "httpx>=0.25.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "pydantic>=2.0.0"
]

[project.scripts]
base44 = "base44_cli.main:cli"
```

**Installation**:
```bash
# Via UV
uv pip install base44-cli

# Via pip
pip install base44-cli

# Development installation
git clone <repo>
cd base44-cli
uv pip install -e ".[dev]"
```

---

## Implementation Checklist

- [ ] Project structure and initial setup
- [ ] Configuration system (env, YAML, profiles)
- [ ] Client wrapper for Base44 SDK
- [ ] Authentication commands
- [ ] Entity CRUD commands
- [ ] Function invocation commands
- [ ] Integration commands
- [ ] AI agent commands
- [ ] Logs query commands
- [ ] Connector commands
- [ ] Output formatting (JSON, table, YAML, CSV)
- [ ] Error handling and user feedback
- [ ] Progress bars and status indicators
- [ ] Configuration management commands
- [ ] Tests (unit + integration)
- [ ] Documentation (README, help text, examples)
- [ ] Package configuration and distribution
- [ ] Shell completion scripts
- [ ] CI/CD setup (optional)

---

## Example Usage Scenarios

### Scenario 1: Daily Task Management
```bash
# Morning: Check pending tasks using HTTP GET
base44 entity filter Task --query '{"status": "pending"}' --format table

# Create new task using HTTP POST
base44 entity create Task --data '{"title": "Review PRs", "priority": "high"}'

# Update task status using HTTP PUT
base44 entity update Task task-123 --data '{"status": "completed"}'

# Get AI suggestions using HTTP POST to integration endpoint
base44 integration llm "What should I prioritize today?"
```

### Scenario 2: Authentication Flow
```bash
# Login and save token (HTTP POST to /auth/login)
base44 auth login --email user@example.com --password <password> --save

# Check authentication status (HTTP GET to /auth/me)
base44 auth me

# The CLI stores the token and uses it in Authorization header for subsequent requests
```

### Scenario 3: Data Export/Import
```bash
# Export all products to CSV using HTTP GET
base44 entity export Product --output products.csv --format csv

# Modify in Excel/Google Sheets, then import using HTTP POST
base44 entity import Product --file products-updated.csv --format csv

# Backup all entities (multiple HTTP GET requests)
for entity in $(base44 entity list-types --format json | jq -r '.[]'); do
  base44 entity export "$entity" --output "backup/${entity}.json"
done
```

### Scenario 4: Service Role Operations
```bash
# List all users (admin) using service token in Base44-Service-Authorization header
base44 entity list User --service-role --format table

# Bulk update user status (HTTP PUT with service role headers)
base44 entity filter User --query '{"inactive": true}' --service-role \
  | jq -r '.[].id' \
  | xargs -I {} base44 entity update User {} --data '{"status": "archived"}' --service-role
```

### Scenario 5: HTTP Request Flow Example

When you run: `base44 entity list Task --limit 10`

The CLI makes this HTTP request:
```http
GET https://base44.app/api/apps/{app-id}/entities/Task?limit=10
Headers:
  Authorization: Bearer {user-token}
  Base44-App-Id: {app-id}
  Content-Type: application/json
```

When you run: `base44 entity create Task --data '{"title": "New"}'`

The CLI makes this HTTP request:
```http
POST https://base44.app/api/apps/{app-id}/entities/Task
Headers:
  Authorization: Bearer {user-token}
  Base44-App-Id: {app-id}
  Content-Type: application/json
Body:
  {"title": "New"}
```

---

## Additional Notes

- Use async/await where appropriate for better performance
- Implement proper logging with log levels (DEBUG, INFO, WARNING, ERROR)
- Support `--verbose` and `--debug` flags globally
- Add version command: `base44 --version`
- Consider adding `base44 doctor` command to check configuration and connectivity
- Add shell completion generation: `base44 completion bash > /etc/bash_completion.d/base44`

---

## API Reference Integration

This CLI should implement all capabilities documented in the Base44 API research document. Refer to `base44_api_research.md` for detailed API specifications, including:

- All entity operations (list, filter, get, create, update, delete, bulkCreate, deleteMany)
- Authentication methods (login, register, invite, me, updateMe, logout)
- Function invocation patterns
- Integration endpoints (Core and custom)
- AI agent interactions
- Logging queries
- Error handling patterns

Ensure the CLI provides a 1:1 mapping of SDK capabilities to command-line operations while maintaining an intuitive and user-friendly interface.
