# Base44 REST API Documentation (Reverse-Engineered)

## ⚠️ Important Notice

Base44 does **NOT** provide official REST API documentation or Swagger/OpenAPI specifications. This documentation is reverse-engineered from:
1. The `@base44/sdk` JavaScript/TypeScript SDK source code
2. Official Base44 documentation
3. SDK type definitions

**Recommendation**: While you can use direct HTTP calls, Base44 is primarily designed to be used via their SDK. The endpoints below are inferred and may change without notice.

---

## Base Configuration

**Base URL**: `https://base44.app`

**Authentication Headers**:
```
Authorization: Bearer <user-token>
Base44-Service-Authorization: Bearer <service-token>  # For admin operations
Base44-App-Id: <app-id>
Content-Type: application/json
```

---

## 1. Authentication Endpoints

### GET /api/apps/{app_id}/auth/me
Get current authenticated user information.

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
```

**Response** (200 OK):
```json
{
  "id": "user-123",
  "email": "[email protected]",
  "name": "John Doe",
  "created_date": "2024-01-01T00:00:00Z",
  "updated_date": "2024-01-02T00:00:00Z",
  "disabled": false,
  "email_verified": true,
  "app_id": "app-123",
  "is_service_account": false,
  "role": "user"
}
```

**cURL Example**:
```bash
curl -X GET "https://base44.app/api/apps/$APP_ID/auth/me" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID"
```

---

### PUT /api/apps/{app_id}/auth/me
Update current user's profile.

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "John Updated Doe",
  "custom_field": "value"
}
```

**cURL Example**:
```bash
curl -X PUT "https://base44.app/api/apps/$APP_ID/auth/me" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Updated"}'
```

---

### POST /api/apps/{app_id}/auth/login
Login with email and password.

**Request Body**:
```json
{
  "email": "[email protected]",
  "password": "secure-password",
  "turnstile_token": "optional-captcha-token"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user-123",
    "email": "[email protected]",
    "name": "John Doe",
    "role": "user"
  }
}
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/auth/login" \
  -H "Content-Type: application/json" \
  -H "Base44-App-Id: $APP_ID" \
  -d '{
    "email": "[email protected]",
    "password": "password123"
  }'
```

---

### POST /api/apps/{app_id}/auth/register
Register a new user.

**Request Body**:
```json
{
  "email": "[email protected]",
  "password": "secure-password",
  "turnstile_token": null,
  "referral_code": null
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": { ... }
}
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/auth/register" \
  -H "Content-Type: application/json" \
  -H "Base44-App-Id: $APP_ID" \
  -d '{
    "email": "[email protected]",
    "password": "newpassword123"
  }'
```

---

### POST /api/apps/{app_id}/auth/invite
Invite a user to the app (admin only).

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "[email protected]",
  "role": "user"
}
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/auth/invite" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "[email protected]",
    "role": "user"
  }'
```

---

### POST /api/apps/{app_id}/auth/verify-otp
Verify OTP code.

**Request Body**:
```json
{
  "email": "[email protected]",
  "otpCode": "123456"
}
```

---

### POST /api/apps/{app_id}/auth/resend-otp
Resend OTP to user.

**Request Body**:
```json
{
  "email": "[email protected]"
}
```

---

### POST /api/apps/{app_id}/auth/reset-password-request
Request password reset.

**Request Body**:
```json
{
  "email": "[email protected]"
}
```

---

### POST /api/apps/{app_id}/auth/reset-password
Reset password with token.

**Request Body**:
```json
{
  "resetToken": "token-from-email",
  "newPassword": "new-secure-password"
}
```

---

### POST /api/apps/{app_id}/auth/change-password
Change password (requires current password).

**Headers**:
```
Authorization: Bearer <user-token>
```

**Request Body**:
```json
{
  "userId": "user-123",
  "currentPassword": "old-password",
  "newPassword": "new-password"
}
```

---

## 2. Entity (CRUD) Endpoints

**Base Pattern**: `/api/apps/{app_id}/entities/{entity_name}`

### GET /api/apps/{app_id}/entities/{entity_name}
List all records from an entity.

**Query Parameters**:
- `sort`: Sort field (prefix with `-` for descending, e.g., `-created_date`)
- `limit`: Maximum number of records to return
- `skip`: Number of records to skip (pagination)
- `fields`: Comma-separated list of fields to return

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
```

**Response** (200 OK):
```json
[
  {
    "id": "record-1",
    "field1": "value1",
    "field2": "value2",
    "created_date": "2024-01-01T00:00:00Z"
  },
  {
    "id": "record-2",
    "field1": "value3",
    "field2": "value4"
  }
]
```

**cURL Example**:
```bash
# List all tasks
curl -X GET "https://base44.app/api/apps/$APP_ID/entities/Task" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID"

# With parameters
curl -X GET "https://base44.app/api/apps/$APP_ID/entities/Task?sort=-created_date&limit=10&skip=0" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID"

# Service role (all records)
curl -X GET "https://base44.app/api/apps/$APP_ID/entities/Task" \
  -H "Base44-Service-Authorization: Bearer $SERVICE_TOKEN" \
  -H "Base44-App-Id: $APP_ID"
```

---

### POST /api/apps/{app_id}/entities/{entity_name}/filter
Filter records by query.

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
Content-Type: application/json
```

**Request Body**:
```json
{
  "query": {
    "status": "pending",
    "priority": ["high", "medium"]
  },
  "limit": 10
}
```

**Response** (200 OK):
```json
[
  {
    "id": "record-1",
    "status": "pending",
    "priority": "high"
  }
]
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/entities/Task/filter" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {"status": "pending"},
    "limit": 5
  }'
```

---

### GET /api/apps/{app_id}/entities/{entity_name}/{id}
Get a specific record by ID.

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
```

**Response** (200 OK):
```json
{
  "id": "record-123",
  "field1": "value1",
  "field2": "value2"
}
```

**cURL Example**:
```bash
curl -X GET "https://base44.app/api/apps/$APP_ID/entities/Task/task-123" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID"
```

---

### POST /api/apps/{app_id}/entities/{entity_name}
Create a new record.

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "New Task",
  "status": "pending",
  "priority": "high",
  "dueDate": "2024-12-31"
}
```

**Response** (201 Created):
```json
{
  "id": "newly-created-id",
  "title": "New Task",
  "status": "pending",
  "created_date": "2024-01-01T00:00:00Z"
}
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/entities/Task" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Task",
    "status": "pending"
  }'
```

---

### PUT /api/apps/{app_id}/entities/{entity_name}/{id}
Update an existing record.

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
Content-Type: application/json
```

**Request Body**:
```json
{
  "status": "completed",
  "completedDate": "2024-01-02"
}
```

**Response** (200 OK):
```json
{
  "id": "record-123",
  "status": "completed",
  "updated_date": "2024-01-02T00:00:00Z"
}
```

**cURL Example**:
```bash
curl -X PUT "https://base44.app/api/apps/$APP_ID/entities/Task/task-123" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

---

### DELETE /api/apps/{app_id}/entities/{entity_name}/{id}
Delete a single record.

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
```

**Response** (200 OK):
```json
{
  "deleted": true,
  "id": "record-123"
}
```

**cURL Example**:
```bash
curl -X DELETE "https://base44.app/api/apps/$APP_ID/entities/Task/task-123" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID"
```

---

### POST /api/apps/{app_id}/entities/{entity_name}/delete-many
Delete multiple records matching a query.

**Request Body**:
```json
{
  "query": {
    "status": "archived"
  }
}
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/entities/Task/delete-many" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{"query": {"status": "archived"}}'
```

---

### POST /api/apps/{app_id}/entities/{entity_name}/bulk-create
Create multiple records at once.

**Request Body**:
```json
{
  "records": [
    {"title": "Task 1", "status": "pending"},
    {"title": "Task 2", "status": "pending"}
  ]
}
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/entities/Task/bulk-create" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"title": "Task 1"},
      {"title": "Task 2"}
    ]
  }'
```

---

## 3. Backend Functions Endpoints

### POST /api/apps/{app_id}/functions/{function_name}
Invoke a backend function.

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
Content-Type: application/json
```

**Request Body**:
```json
{
  "param1": "value1",
  "param2": "value2"
}
```

**Response** (200 OK):
```json
{
  "result": "function output",
  "status": "success"
}
```

**cURL Example**:
```bash
# Without parameters
curl -X POST "https://base44.app/api/apps/$APP_ID/functions/myFunction" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{}'

# With parameters
curl -X POST "https://base44.app/api/apps/$APP_ID/functions/processOrder" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "orderId": "123",
    "action": "fulfill"
  }'

# Service role
curl -X POST "https://base44.app/api/apps/$APP_ID/functions/adminFunction" \
  -H "Base44-Service-Authorization: Bearer $SERVICE_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 4. Integration Endpoints

### Core Integrations

#### POST /api/apps/{app_id}/integrations/Core/InvokeLLM
Generate AI responses.

**Request Body**:
```json
{
  "prompt": "Write a welcome email for new users",
  "responseFormat": "text"
}
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/integrations/Core/InvokeLLM" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "responseFormat": "text"
  }'
```

---

#### POST /api/apps/{app_id}/integrations/Core/SendEmail
Send email to app users.

**Request Body**:
```json
{
  "to": "[email protected]",
  "subject": "Welcome!",
  "body": "<h1>Welcome to our app!</h1>",
  "senderName": "My App"
}
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/integrations/Core/SendEmail" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "[email protected]",
    "subject": "Test Email",
    "body": "Hello World"
  }'
```

---

#### POST /api/apps/{app_id}/integrations/Core/UploadFile
Upload a file.

**Request**: Multipart form data

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/integrations/Core/UploadFile" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -F "file=@/path/to/file.png" \
  -F "metadata={\"type\":\"avatar\"}"
```

---

## 5. AI Agents Endpoints

### GET /api/apps/{app_id}/agents/conversations
Get all conversations.

**Headers**:
```
Authorization: Bearer <user-token>
Base44-App-Id: <app-id>
```

**cURL Example**:
```bash
curl -X GET "https://base44.app/api/apps/$APP_ID/agents/conversations" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID"
```

---

### GET /api/apps/{app_id}/agents/conversations/{conversation_id}
Get specific conversation.

**cURL Example**:
```bash
curl -X GET "https://base44.app/api/apps/$APP_ID/agents/conversations/conv-123" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID"
```

---

### POST /api/apps/{app_id}/agents/conversations
Create a new conversation.

**Request Body**:
```json
{
  "agent_name": "task-assistant",
  "metadata": {
    "context": "task management"
  }
}
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/agents/conversations" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "assistant",
    "metadata": {}
  }'
```

---

### POST /api/apps/{app_id}/agents/conversations/{conversation_id}/messages
Add message to conversation.

**Request Body**:
```json
{
  "role": "user",
  "content": "Help me organize my tasks"
}
```

**cURL Example**:
```bash
curl -X POST "https://base44.app/api/apps/$APP_ID/agents/conversations/conv-123/messages" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Base44-App-Id: $APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "content": "What tasks are due today?"
  }'
```

---

## 6. App Logs Endpoints

### POST /api/apps/{app_id}/logs/user-action
Log user action in app.

**Request Body**:
```json
{
  "pageName": "/dashboard"
}
```

---

### GET /api/apps/{app_id}/logs
Fetch app logs.

**Query Parameters**:
- `startDate`: ISO date string
- `endDate`: ISO date string
- `level`: error | warn | info | debug
- `limit`: number

**cURL Example**:
```bash
curl -X GET "https://base44.app/api/apps/$APP_ID/logs?level=error&limit=100" \
  -H "Base44-Service-Authorization: Bearer $SERVICE_TOKEN" \
  -H "Base44-App-Id: $APP_ID"
```

---

### GET /api/apps/{app_id}/logs/stats
Get log statistics.

**cURL Example**:
```bash
curl -X GET "https://base44.app/api/apps/$APP_ID/logs/stats" \
  -H "Base44-Service-Authorization: Bearer $SERVICE_TOKEN" \
  -H "Base44-App-Id: $APP_ID"
```

---

## 7. Connectors Endpoints

### GET /api/apps/{app_id}/connectors/{connector_type}/access-token
Get OAuth access token for connector.

**Connector Types**: `GoogleDrive`, `GoogleCalendar`, `Slack`, `Notion`, `Salesforce`, `HubSpot`

**Headers**:
```
Base44-Service-Authorization: Bearer <service-token>
Base44-App-Id: <app-id>
```

**Response** (200 OK):
```json
{
  "access_token": "ya29.xxx",
  "refresh_token": "1//xxx",
  "expires_at": "2024-01-02T00:00:00Z"
}
```

**cURL Example**:
```bash
curl -X GET "https://base44.app/api/apps/$APP_ID/connectors/GoogleDrive/access-token" \
  -H "Base44-Service-Authorization: Bearer $SERVICE_TOKEN" \
  -H "Base44-App-Id: $APP_ID"
```

---

## 8. SSO Endpoints (Admin Only)

### GET /api/apps/{app_id}/sso/access-token/{user_id}
Get SSO access token for a user (admin operation).

**Headers**:
```
Base44-Service-Authorization: Bearer <service-token>
Base44-App-Id: <app-id>
```

**cURL Example**:
```bash
curl -X GET "https://base44.app/api/apps/$APP_ID/sso/access-token/user-123" \
  -H "Base44-Service-Authorization: Bearer $SERVICE_TOKEN" \
  -H "Base44-App-Id: $APP_ID"
```

---

## Complete Python Example Using `requests`

```python
import requests
import os

# Configuration
BASE_URL = "https://base44.app"
APP_ID = os.getenv("BASE44_APP_ID")
USER_TOKEN = os.getenv("BASE44_USER_TOKEN")
SERVICE_TOKEN = os.getenv("BASE44_SERVICE_TOKEN")  # Optional

# Headers for user operations
user_headers = {
    "Authorization": f"Bearer {USER_TOKEN}",
    "Base44-App-Id": APP_ID,
    "Content-Type": "application/json"
}

# Headers for service role operations
service_headers = {
    "Base44-Service-Authorization": f"Bearer {SERVICE_TOKEN}",
    "Base44-App-Id": APP_ID,
    "Content-Type": "application/json"
}

# 1. Get current user
response = requests.get(
    f"{BASE_URL}/api/apps/{APP_ID}/auth/me",
    headers=user_headers
)
user = response.json()
print(f"Current user: {user['email']}")

# 2. List tasks
response = requests.get(
    f"{BASE_URL}/api/apps/{APP_ID}/entities/Task",
    headers=user_headers,
    params={"limit": 10, "sort": "-created_date"}
)
tasks = response.json()
print(f"Found {len(tasks)} tasks")

# 3. Create a new task
response = requests.post(
    f"{BASE_URL}/api/apps/{APP_ID}/entities/Task",
    headers=user_headers,
    json={
        "title": "New task from API",
        "status": "pending",
        "priority": "high"
    }
)
new_task = response.json()
print(f"Created task: {new_task['id']}")

# 4. Filter tasks
response = requests.post(
    f"{BASE_URL}/api/apps/{APP_ID}/entities/Task/filter",
    headers=user_headers,
    json={
        "query": {"status": "pending"},
        "limit": 5
    }
)
pending_tasks = response.json()
print(f"Pending tasks: {len(pending_tasks)}")

# 5. Update a task
response = requests.put(
    f"{BASE_URL}/api/apps/{APP_ID}/entities/Task/{new_task['id']}",
    headers=user_headers,
    json={"status": "completed"}
)
updated_task = response.json()

# 6. Invoke a function
response = requests.post(
    f"{BASE_URL}/api/apps/{APP_ID}/functions/processData",
    headers=user_headers,
    json={"input": "test data"}
)
function_result = response.json()

# 7. Use Core integration (LLM)
response = requests.post(
    f"{BASE_URL}/api/apps/{APP_ID}/integrations/Core/InvokeLLM",
    headers=user_headers,
    json={
        "prompt": "Summarize this text",
        "responseFormat": "text"
    }
)
llm_response = response.json()

# 8. Service role operation (list all users)
response = requests.get(
    f"{BASE_URL}/api/apps/{APP_ID}/entities/User",
    headers=service_headers
)
all_users = response.json()
print(f"Total users (admin): {len(all_users)}")
```

---

## Notes

1. **No Official Documentation**: These endpoints are reverse-engineered and may change.
2. **Use SDK When Possible**: Base44 recommends using their JavaScript SDK.
3. **Authentication**: Most endpoints require the `Authorization` header with Bearer token.
4. **Service Role**: Admin operations require `Base44-Service-Authorization` header.
5. **App ID**: Always include `Base44-App-Id` header.
6. **Error Handling**: All endpoints can return Base44Error with `status`, `message`, and `code`.

---

## Error Responses

**401 Unauthorized**:
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token"
}
```

**403 Forbidden**:
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions for this operation"
}
```

**404 Not Found**:
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```
