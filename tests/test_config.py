"""Tests for configuration management."""

import tempfile
from pathlib import Path

import pytest

from base44_cli.config import Config, ConfigManager


def test_config_defaults() -> None:
    """Test default configuration values."""
    config = Config(app_id="test-app")
    assert config.server_url == "https://app.base44.com"
    assert config.app_id == "test-app"
    assert config.output_format == "json"
    assert config.timeout == 30


def test_config_manager_init() -> None:
    """Test ConfigManager initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_manager = ConfigManager()
        config_manager.config_dir = Path(tmpdir)
        config_manager.config_file = Path(tmpdir) / "config.yaml"

        assert config_manager.config_dir.exists()


def test_config_manager_create_profile() -> None:
    """Test creating a profile."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_manager = ConfigManager()
        config_manager.config_dir = Path(tmpdir)
        config_manager.config_file = Path(tmpdir) / "config.yaml"

        config_manager.create_profile("test", "test-app-123")

        profiles = config_manager.list_profiles()
        assert "test" in profiles


def test_config_manager_set_profile() -> None:
    """Test setting default profile."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_manager = ConfigManager()
        config_manager.config_dir = Path(tmpdir)
        config_manager.config_file = Path(tmpdir) / "config.yaml"

        config_manager.create_profile("prod", "prod-app")
        config_manager.set_profile("prod")

        current = config_manager.get_current_profile()
        assert current == "prod"
