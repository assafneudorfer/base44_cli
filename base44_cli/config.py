"""Configuration management for Base44 CLI."""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Base44 configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="BASE44_",
        case_sensitive=False,
        extra="allow",
    )

    server_url: str = Field(default="https://app.base44.com", description="Base44 server URL")
    app_id: str = Field(default="", description="Base44 application ID")
    user_token: Optional[str] = Field(default=None, description="User authentication token")
    service_token: Optional[str] = Field(default=None, description="Service role token")
    output_format: str = Field(default="json", description="Default output format")
    timeout: int = Field(default=30, description="HTTP request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retries")


class ConfigManager:
    """Manages configuration profiles and settings."""

    def __init__(self) -> None:
        self.config_dir = Path.home() / ".base44"
        self.config_file = self.config_dir / "config.yaml"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self, profile: Optional[str] = None) -> Config:
        """Load configuration from environment and config file."""
        # First, load from environment variables and .env file
        config = Config()

        # Then, try to load from config file
        if self.config_file.exists():
            with open(self.config_file) as f:
                config_data = yaml.safe_load(f) or {}

            # Determine which profile to use
            profile_name = profile or config_data.get("default_profile", "production")

            # Load profile settings
            profiles = config_data.get("profiles", {})
            if profile_name in profiles:
                profile_settings = profiles[profile_name]
                # Override with profile settings
                for key, value in profile_settings.items():
                    if value is not None:
                        setattr(config, key, value)

            # Load global settings
            if "timeout" in config_data:
                config.timeout = config_data["timeout"]
            if "max_retries" in config_data:
                config.max_retries = config_data["max_retries"]

        return config

    def save_config(self, config_data: dict) -> None:
        """Save configuration to file."""
        if self.config_file.exists():
            with open(self.config_file) as f:
                existing_data = yaml.safe_load(f) or {}
        else:
            existing_data = {}

        existing_data.update(config_data)

        with open(self.config_file, "w") as f:
            yaml.dump(existing_data, f, default_flow_style=False)

    def set_profile(self, profile_name: str) -> None:
        """Set the default profile."""
        self.save_config({"default_profile": profile_name})

    def create_profile(
        self, profile_name: str, app_id: str, server_url: str = "https://app.base44.com"
    ) -> None:
        """Create a new profile."""
        if self.config_file.exists():
            with open(self.config_file) as f:
                config_data = yaml.safe_load(f) or {}
        else:
            config_data = {}

        if "profiles" not in config_data:
            config_data["profiles"] = {}

        config_data["profiles"][profile_name] = {
            "server_url": server_url,
            "app_id": app_id,
        }

        self.save_config(config_data)

    def list_profiles(self) -> list[str]:
        """List all available profiles."""
        if not self.config_file.exists():
            return []

        with open(self.config_file) as f:
            config_data = yaml.safe_load(f) or {}

        return list(config_data.get("profiles", {}).keys())

    def get_current_profile(self) -> Optional[str]:
        """Get the current default profile."""
        if not self.config_file.exists():
            return None

        with open(self.config_file) as f:
            config_data = yaml.safe_load(f) or {}

        return config_data.get("default_profile")

    def save_token(self, token: str, token_type: str = "user") -> None:
        """Save authentication token to config."""
        profile = self.get_current_profile() or "production"

        if self.config_file.exists():
            with open(self.config_file) as f:
                config_data = yaml.safe_load(f) or {}
        else:
            config_data = {}

        if "profiles" not in config_data:
            config_data["profiles"] = {}
        if profile not in config_data["profiles"]:
            config_data["profiles"][profile] = {}

        key = "user_token" if token_type == "user" else "service_token"
        config_data["profiles"][profile][key] = token

        self.save_config(config_data)
