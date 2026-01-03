"""HTTP client for Base44 REST API."""

from typing import Any, Optional

import httpx

from .config import Config


class Base44Client:
    """HTTP client for Base44 REST API."""

    def __init__(self, config: Config):
        self.config = config
        self.app_id = config.app_id
        self.user_token = config.user_token
        self.service_token = config.service_token
        self.base_url = config.server_url

        # Create httpx client with default headers
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=float(config.timeout),
            headers=self._get_default_headers(),
        )

    def _get_default_headers(self) -> dict[str, str]:
        """Get default headers for all requests."""
        headers = {
            "Content-Type": "application/json",
        }

        if self.user_token:
            headers["api_key"] = self.user_token

        return headers

    def _get_service_headers(self) -> dict[str, str]:
        """Get headers for service role operations."""
        headers = {
            "Content-Type": "application/json",
        }
        if self.service_token:
            headers["api_key"] = self.service_token
        return headers

    # Auth endpoints
    def auth_me(self) -> dict[str, Any]:
        """Get current user info."""
        response = self.client.get(f"/api/apps/{self.app_id}/auth/me")
        response.raise_for_status()
        return response.json()

    def auth_update_me(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update current user."""
        response = self.client.put(f"/api/apps/{self.app_id}/auth/me", json=data)
        response.raise_for_status()
        return response.json()

    def auth_login(
        self, email: str, password: str, turnstile_token: Optional[str] = None
    ) -> dict[str, Any]:
        """Login with email/password."""
        response = self.client.post(
            f"/api/apps/{self.app_id}/auth/login",
            json={"email": email, "password": password, "turnstile_token": turnstile_token},
        )
        response.raise_for_status()
        return response.json()

    def auth_register(
        self,
        email: str,
        password: str,
        turnstile_token: Optional[str] = None,
        referral_code: Optional[str] = None,
    ) -> dict[str, Any]:
        """Register a new user."""
        response = self.client.post(
            f"/api/apps/{self.app_id}/auth/register",
            json={
                "email": email,
                "password": password,
                "turnstile_token": turnstile_token,
                "referral_code": referral_code,
            },
        )
        response.raise_for_status()
        return response.json()

    def auth_invite(self, email: str, role: str = "user") -> dict[str, Any]:
        """Invite a user to the app."""
        response = self.client.post(
            f"/api/apps/{self.app_id}/auth/invite", json={"email": email, "role": role}
        )
        response.raise_for_status()
        return response.json()

    # Entity endpoints
    def entity_list(
        self,
        entity_name: str,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        fields: Optional[str] = None,
        use_service_role: bool = False,
    ) -> list[dict[str, Any]]:
        """List entity records."""
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort
        if limit:
            params["limit"] = limit
        if skip:
            params["skip"] = skip
        if fields:
            params["fields"] = fields

        headers = self._get_service_headers() if use_service_role else None

        response = self.client.get(
            f"/api/apps/{self.app_id}/entities/{entity_name}", params=params, headers=headers
        )
        response.raise_for_status()
        return response.json()

    def entity_filter(
        self,
        entity_name: str,
        query: dict[str, Any],
        limit: Optional[int] = None,
        use_service_role: bool = False,
    ) -> list[dict[str, Any]]:
        """Filter entity records."""
        headers = self._get_service_headers() if use_service_role else None
        body: dict[str, Any] = {"query": query}
        if limit:
            body["limit"] = limit

        response = self.client.post(
            f"/api/apps/{self.app_id}/entities/{entity_name}/filter", json=body, headers=headers
        )
        response.raise_for_status()
        return response.json()

    def entity_get(
        self, entity_name: str, record_id: str, use_service_role: bool = False
    ) -> dict[str, Any]:
        """Get specific entity record."""
        headers = self._get_service_headers() if use_service_role else None

        response = self.client.get(
            f"/api/apps/{self.app_id}/entities/{entity_name}/{record_id}", headers=headers
        )
        response.raise_for_status()
        return response.json()

    def entity_create(
        self, entity_name: str, data: dict[str, Any], use_service_role: bool = False
    ) -> dict[str, Any]:
        """Create entity record."""
        headers = self._get_service_headers() if use_service_role else None

        response = self.client.post(
            f"/api/apps/{self.app_id}/entities/{entity_name}", json=data, headers=headers
        )
        response.raise_for_status()
        return response.json()

    def entity_update(
        self,
        entity_name: str,
        record_id: str,
        data: dict[str, Any],
        use_service_role: bool = False,
    ) -> dict[str, Any]:
        """Update entity record."""
        headers = self._get_service_headers() if use_service_role else None

        response = self.client.put(
            f"/api/apps/{self.app_id}/entities/{entity_name}/{record_id}",
            json=data,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def entity_delete(
        self, entity_name: str, record_id: str, use_service_role: bool = False
    ) -> dict[str, Any]:
        """Delete entity record."""
        headers = self._get_service_headers() if use_service_role else None

        response = self.client.delete(
            f"/api/apps/{self.app_id}/entities/{entity_name}/{record_id}", headers=headers
        )
        response.raise_for_status()
        return response.json()

    def entity_bulk_create(
        self, entity_name: str, records: list[dict[str, Any]], use_service_role: bool = False
    ) -> dict[str, Any]:
        """Bulk create entity records."""
        headers = self._get_service_headers() if use_service_role else None

        response = self.client.post(
            f"/api/apps/{self.app_id}/entities/{entity_name}/bulk-create",
            json={"records": records},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def entity_delete_many(
        self, entity_name: str, query: dict[str, Any], use_service_role: bool = False
    ) -> dict[str, Any]:
        """Delete multiple entity records."""
        headers = self._get_service_headers() if use_service_role else None

        response = self.client.post(
            f"/api/apps/{self.app_id}/entities/{entity_name}/delete-many",
            json={"query": query},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    # Function endpoints
    def function_invoke(
        self, function_name: str, params: dict[str, Any], use_service_role: bool = False
    ) -> dict[str, Any]:
        """Invoke backend function."""
        headers = self._get_service_headers() if use_service_role else None

        response = self.client.post(
            f"/api/apps/{self.app_id}/functions/{function_name}", json=params, headers=headers
        )
        response.raise_for_status()
        return response.json()

    # Integration endpoints
    def integration_invoke_llm(
        self, prompt: str, response_format: str = "text"
    ) -> dict[str, Any]:
        """Invoke LLM integration."""
        response = self.client.post(
            f"/api/apps/{self.app_id}/integrations/Core/InvokeLLM",
            json={"prompt": prompt, "responseFormat": response_format},
        )
        response.raise_for_status()
        return response.json()

    def integration_send_email(
        self,
        to: str,
        subject: str,
        body: str,
        sender_name: Optional[str] = None,
        html: bool = False,
    ) -> dict[str, Any]:
        """Send email via Core integration."""
        payload: dict[str, Any] = {
            "to": to,
            "subject": subject,
            "body": body,
        }
        if sender_name:
            payload["senderName"] = sender_name
        if html:
            payload["html"] = True

        response = self.client.post(
            f"/api/apps/{self.app_id}/integrations/Core/SendEmail", json=payload
        )
        response.raise_for_status()
        return response.json()

    def integration_upload_file(self, file_path: str, metadata: Optional[dict] = None) -> dict[str, Any]:
        """Upload a file via Core integration."""
        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {}
            if metadata:
                data["metadata"] = str(metadata)

            # Use a new client without Content-Type header for multipart
            headers = {}
            if self.user_token:
                headers["api_key"] = self.user_token

            response = httpx.post(
                f"{self.base_url}/api/apps/{self.app_id}/integrations/Core/UploadFile",
                files=files,
                data=data,
                headers=headers,
                timeout=float(self.config.timeout),
            )
        response.raise_for_status()
        return response.json()

    # Agent endpoints
    def agent_list_conversations(self) -> list[dict[str, Any]]:
        """Get all agent conversations."""
        response = self.client.get(f"/api/apps/{self.app_id}/agents/conversations")
        response.raise_for_status()
        return response.json()

    def agent_get_conversation(self, conversation_id: str) -> dict[str, Any]:
        """Get specific conversation."""
        response = self.client.get(
            f"/api/apps/{self.app_id}/agents/conversations/{conversation_id}"
        )
        response.raise_for_status()
        return response.json()

    def agent_create_conversation(
        self, agent_name: str, metadata: Optional[dict] = None
    ) -> dict[str, Any]:
        """Create a new conversation."""
        payload: dict[str, Any] = {"agent_name": agent_name}
        if metadata:
            payload["metadata"] = metadata

        response = self.client.post(
            f"/api/apps/{self.app_id}/agents/conversations", json=payload
        )
        response.raise_for_status()
        return response.json()

    def agent_send_message(
        self, conversation_id: str, content: str, role: str = "user"
    ) -> dict[str, Any]:
        """Send message to agent."""
        response = self.client.post(
            f"/api/apps/{self.app_id}/agents/conversations/{conversation_id}/messages",
            json={"role": role, "content": content},
        )
        response.raise_for_status()
        return response.json()

    # Logs endpoints
    def logs_query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        level: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Query app logs."""
        params: dict[str, Any] = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if level:
            params["level"] = level
        if limit:
            params["limit"] = limit

        headers = self._get_service_headers()
        response = self.client.get(f"/api/apps/{self.app_id}/logs", params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def logs_stats(self) -> dict[str, Any]:
        """Get log statistics."""
        headers = self._get_service_headers()
        response = self.client.get(f"/api/apps/{self.app_id}/logs/stats", headers=headers)
        response.raise_for_status()
        return response.json()

    # Connector endpoints
    def connector_get_access_token(self, connector_type: str) -> dict[str, Any]:
        """Get OAuth access token for connector."""
        headers = self._get_service_headers()
        response = self.client.get(
            f"/api/apps/{self.app_id}/connectors/{connector_type}/access-token", headers=headers
        )
        response.raise_for_status()
        return response.json()

    # App info endpoints
    def app_get_info(self, app_id: Optional[str] = None) -> dict[str, Any]:
        """Get app information by app_id."""
        target_app_id = app_id or self.app_id
        response = self.client.get(f"/api/apps/public/prod/by-id/{target_app_id}")
        response.raise_for_status()
        return response.json()

    def app_get_id_from_domain(self, domain: str) -> str:
        """Get app_id from domain name."""
        # Use the old base URL for this endpoint
        response = httpx.get(
            f"https://base44.app/api/apps/public/prod/domain/{domain}",
            timeout=float(self.config.timeout),
        )
        response.raise_for_status()
        return response.json()

    def __del__(self) -> None:
        """Close HTTP client on cleanup."""
        if hasattr(self, "client"):
            self.client.close()
