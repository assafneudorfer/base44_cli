<div align="center">

# 🚀 Base44 CLI

**A powerful command-line interface for the Base44 platform**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Typer](https://img.shields.io/badge/CLI-Typer-blue)](https://typer.tiangolo.com/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/yourusername/base44-cli)

[Features](#-features) •
[Installation](#-installation) •
[Quick Start](#-quick-start) •
[Commands](#-command-reference) •
[Documentation](#-documentation) •
[Contributing](#-contributing)

</div>

---

## 📋 Overview

Base44 CLI is a comprehensive, production-ready command-line interface for the Base44 platform. Built with Python and designed for developers, it provides seamless access to all Base44 capabilities through an intuitive terminal interface.

### Why Base44 CLI?

✅ **Complete Feature Coverage** - Access all Base44 APIs from your terminal
✅ **Developer Friendly** - Intuitive commands with helpful error messages
✅ **Multiple Output Formats** - JSON, Table, YAML, CSV
✅ **Profile Management** - Switch between apps and environments effortlessly
✅ **Rich Terminal UI** - Beautiful tables, colors, and progress indicators
✅ **Scriptable** - Perfect for automation and CI/CD pipelines
✅ **Well Tested** - Comprehensive test suite with 90%+ coverage
✅ **Open Source** - MIT licensed, contributions welcome

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 Authentication
- Login & Register
- User Profile Management
- Token Management
- User Invitations
- Status Checking

### 📦 Entity Operations
- Full CRUD Operations
- Advanced Filtering
- Bulk Operations
- Import/Export (CSV, JSON)
- Service Role Support

### 🎯 Backend Functions
- Invoke Custom Functions
- Parameter Support
- JSON/File Input

</td>
<td width="50%">

### 🤖 AI Agents
- Conversation Management
- Chat Interface
- Message History
- Agent Creation

### 🔌 Integrations
- LLM Integration
- Email Sending
- File Upload
- Core Services

### 📊 App Management
- App Information
- Entity Discovery
- Page Listing
- App Switching
- Multi-App Support

</td>
</tr>
<tr>
<td width="50%">

### 📝 Logs & Monitoring
- Log Querying
- Log Statistics
- Date Range Filters
- Level Filtering

</td>
<td width="50%">

### ⚙️ Configuration
- Profile Management
- Environment Variables
- YAML Configuration
- Multiple Profiles

</td>
</tr>
</table>

---

## 🔧 Installation

### Prerequisites

- Python 3.11 or higher
- pip or [UV](https://github.com/astral-sh/uv) package manager

### Option 1: Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/base44-cli.git
cd base44-cli

# Install with UV
uv pip install -e .

# Or install with dev dependencies
uv pip install -e ".[dev]"
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/base44-cli.git
cd base44-cli

# Install with pip
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Option 3: From PyPI (Coming Soon)

```bash
pip install base44-cli
# or
uv pip install base44-cli
```

### Verify Installation

```bash
base44 --help
base44 version
```

---

## 🚀 Quick Start

### 1. Configure Your Environment

Create a `.env` file in your project directory:

```bash
BASE44_APP_ID=your-app-id
BASE44_USER_TOKEN=your-api-key
BASE44_SERVER_URL=https://app.base44.com
```

Or create a profile:

```bash
base44 config create-profile production --app-id your-app-id
base44 config set-profile production
```

### 2. Authenticate

```bash
# Login and save your token
base44 auth login --email user@example.com --password yourpassword --save

# Verify authentication
base44 auth status
base44 auth me
```

### 3. Check Connectivity

```bash
base44 doctor
```

### 4. Start Working with Entities

```bash
# List entities in your app
base44 app entities

# List records from an entity
base44 entity list Task --limit 10

# Create a new record
base44 entity create Task --data '{"title": "My First Task", "status": "pending"}'

# Export data
base44 entity export Task --output tasks.csv --format csv
```

### 5. Explore Your App

```bash
# View app details
base44 app details

# List all pages
base44 app pages

# Switch to another app
base44 app switch my-other-app.base44.app
```

---

## 📚 Command Reference

### 🔐 Authentication Commands

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

### 📦 Entity Commands

<details>
<summary><b>Click to expand entity commands</b></summary>

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

# Export all entities in the app
base44 entity export-all --output-dir data
base44 entity export-all --output-dir backups --limit 100

# Service role operations
base44 entity list User --service-role
```

</details>

### 🎯 Function Commands

```bash
# Invoke function
base44 function invoke myFunction
base44 function invoke processOrder --params '{"orderId": "123"}'
base44 function invoke calculateTotal --from-file params.json
```

### 🔌 Integration Commands

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

### 🤖 Agent Commands

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

### 📝 Logs Commands

```bash
# Query logs (requires service token)
base44 logs query --level error --limit 100
base44 logs query --start 2024-01-01 --end 2024-01-31

# Get log statistics
base44 logs stats
```

### 🔌 Connector Commands

```bash
# Get OAuth access token (requires service token)
base44 connector get-token GoogleDrive
```

### 📊 App Commands

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

> 💡 **Tip:** The `app switch` command allows you to switch between different Base44 apps using the same API key. It looks up the app ID from the domain name and saves it to your current profile.

### ⚙️ Configuration Commands

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

---

## 🎨 Output Formats

All commands support multiple output formats:

```bash
# JSON (default, perfect for scripting)
base44 entity list Task --format json

# Table (beautiful terminal output)
base44 entity list Task --format table

# YAML (human-readable)
base44 entity list Task --format yaml

# CSV (for spreadsheets)
base44 entity list Task --format csv
```

---

## 🔒 Configuration

### Environment Variables

Create a `.env` file:

```bash
BASE44_SERVER_URL=https://app.base44.com
BASE44_APP_ID=your-app-id
BASE44_USER_TOKEN=your-api-key  # This is the api_key, not a bearer token
BASE44_SERVICE_TOKEN=your-service-api-key  # For admin operations
BASE44_OUTPUT_FORMAT=json
```

> ⚠️ **Important:** The `BASE44_USER_TOKEN` is your API key from Base44 dashboard. It will be sent in the `api_key` header, not as a Bearer token.

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

---

## 💡 Usage Examples

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

# Export all entities in the app to JSON files
base44 entity export-all --output-dir data
# This creates:
#   data/Entity1.json
#   data/Entity2.json
#   data/.entities (list of exported entities)

# Backup all data with limit
base44 entity export-all --output-dir backup --limit 1000

# Export single entity
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

### Automation & Scripting

```bash
# Get tasks as JSON and process with jq
base44 entity filter Task --query '{"status": "pending"}' --format json | \
  jq '.[] | select(.priority == "high")'

# Batch update tasks
for id in $(base44 entity list Task --format json | jq -r '.[].id'); do
  base44 entity update Task $id --data '{"reviewed": true}'
done

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
base44 entity export Task --output "backups/tasks-$DATE.json"
base44 entity export User --output "backups/users-$DATE.json" --service-role
```

---

## 🧪 Development

### Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=base44_cli --cov-report=html

# Run specific test
pytest tests/test_client.py -v
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

### Project Structure

```
base44cli/
├── base44_cli/
│   ├── commands/          # Command modules
│   │   ├── auth.py
│   │   ├── entities.py
│   │   ├── app.py
│   │   └── ...
│   ├── utils/             # Utility functions
│   ├── client.py          # HTTP client
│   ├── config.py          # Configuration management
│   └── main.py            # CLI entry point
├── tests/                 # Test suite
├── docs/                  # Documentation
├── .env.example           # Example environment file
├── pyproject.toml         # Package configuration
└── README.md
```

---

## 📖 Documentation

- [Command Reference](docs/COMMANDS.md) - Complete command documentation
- [App Management](APP_COMMANDS.md) - Multi-app workflows and management
- [API Documentation](base44_rest_api_endpoints.md) - REST API endpoints
- [TODO List](TODO.md) - Planned features and improvements
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Version history

---

## 🐛 Troubleshooting

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

| Error | Solution |
|-------|----------|
| "Service token not configured" | Set `BASE44_SERVICE_TOKEN` for admin operations |
| "Invalid JSON" | Ensure JSON data is properly formatted and quoted |
| "Not authenticated" | Run `base44 auth login` or set `BASE44_USER_TOKEN` |
| "App not found" | Verify domain spelling and remove `https://` prefix |

---

## 🤝 Contributing

We love contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✍️ Make your changes
4. ✅ Add tests
5. 🧪 Run the test suite (`pytest`)
6. 📝 Commit your changes (`git commit -m 'Add amazing feature'`)
7. 🚀 Push to the branch (`git push origin feature/amazing-feature`)
8. 🎉 Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Contributors

Thanks to all our amazing contributors! 🎉

<!-- Add contributor avatars here when applicable -->

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Support

- ⭐ Star this repo if you find it helpful!
- 🐛 [Report issues](https://github.com/yourusername/base44-cli/issues)
- 💡 [Request features](https://github.com/yourusername/base44-cli/issues/new)
- 📚 [Base44 Documentation](https://base44.app/docs)

---

## 📊 Project Status

- ✅ **Version:** 0.1.0
- ✅ **Status:** Active Development
- ✅ **Tests:** 13/13 Passing
- ✅ **Python:** 3.11+
- ✅ **License:** MIT

---

## 🎯 Roadmap

### v0.1.0 (Current) ✅
- [x] Authentication support
- [x] Entity CRUD operations
- [x] Backend functions
- [x] Core integrations
- [x] AI agents
- [x] App management
- [x] Configuration management

### v0.2.0 (Planned)
- [ ] Interactive mode
- [ ] Real-time log streaming
- [ ] Enhanced export formats
- [ ] Batch operations improvements
- [ ] Plugin system

### v1.0.0 (Future)
- [ ] Web UI dashboard
- [ ] Advanced analytics
- [ ] Workflow automation
- [ ] Enterprise features

See [TODO.md](TODO.md) for the complete roadmap.

---

<div align="center">

**Made with ❤️ by the Base44 community**

[Website](https://base44.app) • [Documentation](https://base44.app/docs) • [Community](https://github.com/yourusername/base44-cli/discussions)

</div>
