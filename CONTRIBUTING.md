# Contributing to Base44 CLI

Thank you for your interest in contributing to Base44 CLI! We welcome contributions from everyone and appreciate your help in making this project better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Community](#community)

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors include:**
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Project maintainers are responsible for clarifying standards of acceptable behavior and will take appropriate action in response to unacceptable behavior.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/base44-cli.git
   cd base44-cli
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/base44-cli.git
   ```

## Development Setup

### Prerequisites

- Python 3.11 or higher
- [UV](https://github.com/astral-sh/uv) package manager (recommended) or pip
- Git

### Setting Up Your Development Environment

1. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   # Using UV (recommended)
   uv pip install -e ".[dev]"

   # Or using pip
   pip install -e ".[dev]"
   ```

3. **Set up pre-commit hooks** (optional but recommended):
   ```bash
   pre-commit install
   ```

4. **Create a `.env` file** for testing:
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

### Verify Your Setup

```bash
# Run tests
pytest

# Check code formatting
black --check base44_cli/

# Run linter
ruff check base44_cli/

# Type checking
mypy base44_cli/
```

## How to Contribute

### Types of Contributions

We welcome many types of contributions:

- 🐛 **Bug fixes**
- ✨ **New features**
- 📝 **Documentation improvements**
- 🧪 **Test coverage improvements**
- 🎨 **Code refactoring**
- 🌐 **Translations**
- 💡 **Ideas and suggestions**

### Workflow

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes**
   - Write clear, concise code
   - Follow the coding standards (see below)
   - Add tests for new features
   - Update documentation as needed

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring
   - `style:` for formatting changes
   - `chore:` for maintenance tasks

4. **Keep your branch updated**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

5. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Formatting**: Use [Black](https://github.com/psf/black) for automatic formatting
- **Linting**: Use [Ruff](https://github.com/astral-sh/ruff) for linting
- **Type hints**: Use type hints for all function signatures
- **Docstrings**: Use Google-style docstrings

### Code Formatting

Before committing, format your code:

```bash
# Format with black
black base44_cli/

# Check linting
ruff check base44_cli/

# Fix auto-fixable issues
ruff check --fix base44_cli/
```

### Type Hints

All functions should have type hints:

```python
def entity_list(
    entity_name: str,
    limit: Optional[int] = None,
    use_service_role: bool = False,
) -> list[dict[str, Any]]:
    """List entity records.

    Args:
        entity_name: Name of the entity to list
        limit: Maximum number of records to return
        use_service_role: Whether to use service role authentication

    Returns:
        List of entity records

    Raises:
        ValueError: If entity_name is empty
        httpx.HTTPError: If the API request fails
    """
    pass
```

### Documentation

- **Code comments**: Explain *why*, not *what*
- **Docstrings**: Required for all public functions, classes, and modules
- **README updates**: Update README.md if adding user-facing features
- **Changelog**: Add entry to CHANGELOG.md for notable changes

### Project Structure

When adding new features, follow the existing structure:

```
base44_cli/
├── commands/          # Command modules (one per feature area)
│   ├── auth.py       # Authentication commands
│   ├── entities.py   # Entity commands
│   └── app.py        # App management commands
├── utils/            # Utility functions
│   ├── formatters.py # Output formatting
│   └── validators.py # Input validation
├── client.py         # HTTP client
├── config.py         # Configuration management
└── main.py          # CLI entry point
```

## Testing Guidelines

### Writing Tests

- **Coverage**: Aim for 90%+ code coverage
- **Test files**: Mirror the structure of `base44_cli/`
- **Naming**: Test files should be named `test_*.py`
- **Fixtures**: Use pytest fixtures for common setup
- **Mocking**: Use `pytest-httpx` for mocking HTTP requests

### Test Structure

```python
"""Tests for entity commands."""

import pytest
from pytest_httpx import HTTPXMock

from base44_cli.client import Base44Client
from base44_cli.config import Config


def test_entity_list(httpx_mock: HTTPXMock) -> None:
    """Test listing entities."""
    # Arrange
    config = Config(app_id="test-app", user_token="test-token")
    client = Base44Client(config)

    httpx_mock.add_response(
        url="https://app.base44.com/api/apps/test-app/entities/Task",
        json=[{"id": "1", "title": "Test"}],
    )

    # Act
    result = client.entity_list("Task")

    # Assert
    assert len(result) == 1
    assert result[0]["title"] == "Test"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=base44_cli --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run specific test
pytest tests/test_client.py::test_entity_list -v

# Run with verbose output
pytest -v

# Run only failed tests from last run
pytest --lf
```

### Test Categories

- **Unit tests**: Test individual functions in isolation
- **Integration tests**: Test interactions between components
- **End-to-end tests**: Test complete workflows (use sparingly)

## Pull Request Process

### Before Submitting

1. ✅ **Run all tests** and ensure they pass
2. ✅ **Format your code** with Black
3. ✅ **Run linter** and fix any issues
4. ✅ **Update documentation** if needed
5. ✅ **Add/update tests** for your changes
6. ✅ **Update CHANGELOG.md** with your changes
7. ✅ **Rebase on latest main** branch

### Pull Request Template

When opening a PR, include:

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Related Issues
Closes #123

## Changes Made
- Added feature X
- Fixed bug Y
- Updated documentation for Z

## Testing
- [ ] All tests pass
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated
- [ ] CHANGELOG.md updated
```

### Review Process

1. **Automated checks** will run (tests, linting, formatting)
2. **Maintainers will review** your code
3. **Address feedback** by pushing new commits
4. Once approved, your PR will be **merged**

### After Merge

- Your contribution will be included in the next release
- You'll be added to the contributors list
- Thank you for your contribution! 🎉

## Reporting Bugs

### Before Reporting

1. **Check existing issues** to avoid duplicates
2. **Update to the latest version** and see if the bug persists
3. **Gather information** about the bug

### Bug Report Template

When reporting bugs, include:

```markdown
## Bug Description
Clear description of what went wrong

## Steps to Reproduce
1. Run command `base44 entity list Task`
2. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., macOS 13.0]
- Python version: [e.g., 3.11.5]
- Base44 CLI version: [e.g., 0.1.0]
- Installation method: [pip/uv]

## Error Output
```bash
Paste full error message here
```

## Additional Context
Any other relevant information
```

## Suggesting Features

We love feature ideas! Here's how to suggest one:

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Problem It Solves
What problem does this solve?

## Proposed Solution
How should it work?

## Alternatives Considered
What other solutions did you consider?

## Example Usage
```bash
base44 new-command --option value
```

## Additional Context
Any other relevant information
```

### Feature Prioritization

Features are prioritized based on:
- **Impact**: How many users will benefit?
- **Effort**: How complex is the implementation?
- **Alignment**: Does it fit the project goals?
- **Community interest**: How many 👍 on the issue?

## Community

### Getting Help

- 📖 [Documentation](https://github.com/yourusername/base44-cli/wiki)
- 💬 [Discussions](https://github.com/yourusername/base44-cli/discussions)
- 🐛 [Issues](https://github.com/yourusername/base44-cli/issues)

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

### Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- CHANGELOG.md

## Development Tips

### Debugging

Enable debug logging:

```bash
export BASE44_DEBUG=1
base44 entity list Task
```

### Testing with Real API

Create a test app on Base44 for development:

```bash
# Use a separate .env file
cp .env .env.test
# Edit .env.test with test app credentials

# Run commands with test config
BASE44_APP_ID=test-app-id base44 entity list Task
```

### Quick Development Cycle

```bash
# Install in editable mode
uv pip install -e .

# Make changes to code
# Test immediately
base44 your-command

# No need to reinstall!
```

### Common Issues

**Import errors after adding dependencies**:
```bash
uv pip install -e ".[dev]"
```

**Tests fail with authentication errors**:
- Check your `.env` file
- Ensure test credentials are valid

**Type checking errors**:
```bash
mypy base44_cli/
```

## Questions?

If you have questions about contributing, feel free to:
- Open a [Discussion](https://github.com/yourusername/base44-cli/discussions)
- Comment on a related issue
- Reach out to maintainers

---

Thank you for contributing to Base44 CLI! Your efforts make this project better for everyone. 🚀
