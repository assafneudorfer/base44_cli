# Base44 CLI

Comprehensive command-line interface for the Base44 platform. This CLI provides access to all major Base44 capabilities through an intuitive command-line interface using direct HTTP/REST API calls.

## Features

- **Authentication**: Login, register, invite users, and manage authentication
- **Entity Operations**: Full CRUD operations on entities with filtering, bulk operations, and import/export
- **Backend Functions**: Invoke custom backend functions
- **Integrations**: Access to Core integrations (LLM, Email, File Upload)
- **AI Agents**: Manage conversations and interact with AI agents
- **Logs**: Query application logs
- **Connectors**: Manage OAuth connectors
- **Configuration**: Profile-based configuration management
- **Multiple Output Formats**: JSON, Table, YAML, CSV
- **Rich Terminal Output**: Beautiful tables, progress bars, and colored output

## Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/base44-cli.git
cd base44-cli

# Install with UV
uv pip install -e .

# Or install with dev dependencies
uv pip install -e ".[dev]"
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/base44-cli.git
cd base44-cli

# Install with pip
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### From PyPI (when published)

```bash
pip install base44-cli
# or
uv pip install base44-cli
```

## Quick Start

### 1. Set Up Configuration

Create a `.env` file or set environment variables:

```bash
BASE44_APP_ID=your-app-id
BASE44_USER_TOKEN=your-user-token
BASE44_SERVICE_TOKEN=your-service-token  # Optional, for admin operations
```

Or use the configuration management:

```bash
# Create a profile
base44 config create-profile production --app-id your-app-id

# Set as default
base44 config set-profile production
```

### 2. Authenticate

```bash
# Login and save token
base44 auth login --email user@example.com --password yourpassword --save

# Check authentication status
base44 auth status

# Get current user info
base44 auth me
```

### 3. Check Connectivity

```bash
base44 doctor
```

## Command Reference

### Authentication Commands

```bash
# Login
base44 auth login --email user@example.com --password <password> --save

# Register new user
base44 auth register --email user@example.com --password <password> --save

# Get current user
base44 auth me

# Update user profile
base44 auth update --name "John Doe"

# Invite user (requires permissions)
base44 auth invite --email newuser@example.com --role user

# Set token manually
base44 auth set-token <token>

# Check status
base44 auth status
```

### Entity Commands

```bash
# List records
base44 entity list Task
base44 entity list Task --limit 10 --sort "-created_date"

# Filter records
base44 entity filter Task --query '{"status": "pending"}'

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
base44 entity delete-many Task --query '{"status": "archived"}' --yes

# Export/Import
base44 entity export Task --output tasks.csv --format csv
base44 entity import Task --file tasks.csv --format csv

# Service role operations
base44 entity list User --service-role
```

### Function Commands

```bash
# Invoke function
base44 function invoke myFunction
base44 function invoke processOrder --params '{"orderId": "123"}'
base44 function invoke calculateTotal --from-file params.json
```

### Integration Commands

```bash
# LLM
base44 integration llm "Write a welcome email for new users"

# Email
base44 integration email \
  --to user@example.com \
  --subject "Welcome" \
  --body "Hello!" \
  --html

# Upload file
base44 integration upload-file --file image.png --metadata '{"type": "avatar"}'
```

### Agent Commands

```bash
# List conversations
base44 agent list

# Get conversation
base44 agent get conv-123

# Create conversation
base44 agent create --agent-name task-assistant

# Send message
base44 agent chat conv-123 "Help me organize my tasks"

# View history
base44 agent history conv-123 --limit 20
```

### Logs Commands

```bash
# Query logs (requires service token)
base44 logs query --level error --limit 100
base44 logs query --start 2024-01-01 --end 2024-01-31

# Get log statistics
base44 logs stats
```

### Connector Commands

```bash
# Get OAuth access token (requires service token)
base44 connector get-token GoogleDrive
```

### App Commands

```bash
# Get app information
base44 app info
base44 app info --app-id <app-id>

# Show detailed app information
base44 app details

# List all entities in the app
base44 app entities
base44 app entities --format json

# List all pages in the app
base44 app pages

# Switch to a different app by domain
base44 app switch family-flow-55bc26d2.base44.app
base44 app switch my-app.base44.app --no-save
```

**Note**: The `app switch` command allows you to switch between different Base44 apps using the same API key. It looks up the app ID from the domain name and saves it to your current profile.

### Configuration Commands

```bash
# Show current configuration
base44 config show

# Create profile
base44 config create-profile staging --app-id staging-123

# Set default profile
base44 config set-profile staging

# List profiles
base44 config list-profiles
```

## Output Formats

All commands support multiple output formats:

```bash
# JSON (default)
base44 entity list Task --format json

# Table (pretty)
base44 entity list Task --format table

# YAML
base44 entity list Task --format yaml

# CSV
base44 entity list Task --format csv
```

## Configuration

### Environment Variables

Create a `.env` file:

```bash
BASE44_SERVER_URL=https://app.base44.com
BASE44_APP_ID=your-app-id
BASE44_USER_TOKEN=your-api-key  # This is the api_key, not a bearer token
BASE44_SERVICE_TOKEN=your-service-api-key  # For admin operations
BASE44_OUTPUT_FORMAT=json
```

**Important**: The `BASE44_USER_TOKEN` is your API key from Base44 dashboard. It will be sent in the `api_key` header, not as a Bearer token.

### Config File

The CLI creates a config file at `~/.base44/config.yaml`:

```yaml
default_profile: production

profiles:
  production:
    server_url: https://app.base44.com
    app_id: prod-app-123
    user_token: your-api-key  # This is your api_key
    output_format: json

  development:
    server_url: https://app.base44.com
    app_id: dev-app-456
    output_format: table

timeout: 30
max_retries: 3
```

## Advanced Usage

### Scripting & Automation

```bash
# Get tasks as JSON and process with jq
base44 entity filter Task --query '{"status": "pending"}' --format json | jq '.[] | select(.priority == "high")'

# Batch update tasks
for id in $(base44 entity list Task --format json | jq -r '.[].id'); do
  base44 entity update Task $id --data '{"reviewed": true}'
done
```

### Service Role Operations

Some operations require service role authentication:

```bash
# Set service token
export BASE44_SERVICE_TOKEN=your-service-token

# List all users (admin only)
base44 entity list User --service-role

# Query logs
base44 logs query --level error
```

## Development

### Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=base44_cli --cov-report=html
```

### Code Quality

```bash
# Format code
black base44_cli/

# Lint
ruff check base44_cli/

# Type checking
mypy base44_cli/
```

## Examples

### Daily Task Management

```bash
# Morning: Check pending tasks
base44 entity filter Task --query '{"status": "pending"}' --format table

# Create new task
base44 entity create Task --data '{"title": "Review PRs", "priority": "high"}'

# Update task status
base44 entity update Task task-123 --data '{"status": "completed"}'

# Get AI suggestions
base44 integration llm "What should I prioritize today?"
```

### Data Export/Import

```bash
# Export all products to CSV
base44 entity export Product --output products.csv --format csv

# Modify in Excel/Google Sheets, then import
base44 entity import Product --file products-updated.csv --format csv

# Backup all data
base44 entity export Task --output backup/tasks.json
base44 entity export User --output backup/users.json --service-role
```

### Managing Multiple Apps

```bash
# View current app details
base44 app details

# Switch to a different app using its domain
base44 app switch my-other-app.base44.app

# List entities in the new app
base44 app entities

# Work with entities from the new app
base44 entity list User --limit 5

# Switch back to original app
base44 app switch my-original-app.base44.app

# Query specific app without switching
base44 app entities --app-id 68630c0fcb589f2fa5c22132
```

## Troubleshooting

### Authentication Issues

```bash
# Check authentication status
base44 auth status

# Verify token is set
base44 config show

# Re-login
base44 auth login --email your@email.com --password <password> --save
```

### Connection Issues

```bash
# Run diagnostics
base44 doctor

# Check server URL
echo $BASE44_SERVER_URL
```

### Common Errors

**"Service token not configured"**: Set `BASE44_SERVICE_TOKEN` for admin operations

**"Invalid JSON"**: Ensure JSON data is properly formatted and quoted

**"Not authenticated"**: Run `base44 auth login` or set `BASE44_USER_TOKEN`

## API Documentation

This CLI uses reverse-engineered Base44 REST API endpoints. For detailed API documentation, see [base44_rest_api_endpoints.md](base44_rest_api_endpoints.md).

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- Issues: https://github.com/yourusername/base44-cli/issues
- Base44 Documentation: https://base44.app/docs

## Changelog

### 0.1.0 (Initial Release)

- Full authentication support
- Complete entity CRUD operations
- Backend function invocation
- Core integrations (LLM, Email, File Upload)
- AI agent operations
- Log querying
- Configuration management
- Multiple output formats
- Rich terminal output
