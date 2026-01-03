"""Tests for Base44 HTTP client."""

import pytest
from pytest_httpx import HTTPXMock

from base44_cli.client import Base44Client
from base44_cli.config import Config


def test_client_init() -> None:
    """Test client initialization."""
    config = Config(app_id="test-app", user_token="test-token")
    client = Base44Client(config)

    assert client.app_id == "test-app"
    assert client.user_token == "test-token"
    assert client.base_url == "https://app.base44.com"


def test_client_headers() -> None:
    """Test client headers."""
    config = Config(app_id="test-app", user_token="test-token")
    client = Base44Client(config)

    headers = client._get_default_headers()
    assert headers["api_key"] == "test-token"
    assert headers["Content-Type"] == "application/json"


def test_client_service_headers() -> None:
    """Test service role headers."""
    config = Config(app_id="test-app", service_token="service-token")
    client = Base44Client(config)

    headers = client._get_service_headers()
    assert headers["api_key"] == "service-token"
    assert headers["Content-Type"] == "application/json"


def test_auth_me(httpx_mock: HTTPXMock) -> None:
    """Test auth/me endpoint."""
    config = Config(app_id="test-app", user_token="test-token")
    client = Base44Client(config)

    httpx_mock.add_response(
        method="GET",
        url="https://app.base44.com/api/apps/test-app/auth/me",
        json={"id": "user-123", "email": "[email protected]"},
    )

    result = client.auth_me()
    assert result["id"] == "user-123"
    assert result["email"] == "[email protected]"


def test_entity_list(httpx_mock: HTTPXMock) -> None:
    """Test entity list endpoint."""
    config = Config(app_id="test-app", user_token="test-token")
    client = Base44Client(config)

    httpx_mock.add_response(
        method="GET",
        url="https://app.base44.com/api/apps/test-app/entities/Task?limit=10",
        json=[{"id": "task-1", "title": "Test"}],
    )

    result = client.entity_list("Task", limit=10)
    assert len(result) == 1
    assert result[0]["id"] == "task-1"
