# App Management Commands

The Base44 CLI now includes powerful app management commands that allow you to work with multiple apps and explore app metadata.

## New Commands

### 1. `base44 app info`
Get detailed information about a Base44 application.

```bash
# Get info for current app
base44 app info

# Get info for specific app
base44 app info --app-id 68630c0fcb589f2fa5c22132

# Output formats
base44 app info --format json
base44 app info --format table
base44 app info --format yaml
```

**Returns:**
- App ID, name, description
- Organization ID
- Logo URL
- Creation and update dates
- Entities and pages

### 2. `base44 app details`
Show a beautifully formatted view of app information.

```bash
base44 app details
```

**Example output:**
```
═══ Application Details ═══

Name: FamilyFlow
ID: 68642fa07b411bd555bc26d2
Organization ID: 68404d03e22b7a4b1f40e2d2

Description:
FamilyFlow מארגן את חיי המשפחה שלך

Created: 2025-07-01T18:57:36.259000
Updated: 2026-01-03T09:24:51.590000

Entities (4):
  • FamilyMember
  • FamilyEvent
  • TodoItem
  • FamilyInvitation

Pages (5):
  • Calendar
  • AddEvent
  • FamilyMembers
```

### 3. `base44 app entities`
List all entities defined in the app.

```bash
# List entities in table format
base44 app entities

# List entities in JSON format
base44 app entities --format json

# List entities from specific app
base44 app entities --app-id 68630c0fcb589f2fa5c22132
```

**Example output:**
```
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Entity Name     ┃ Fields Count ┃ Has Permissions ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ Story           │ 0            │ No              │
│ Child           │ 0            │ No              │
│ PrintingHouse   │ 0            │ No              │
└─────────────────┴──────────────┴─────────────────┘
```

### 4. `base44 app pages`
List all pages in the app with their code size.

```bash
# List pages in table format
base44 app pages

# List pages in JSON format
base44 app pages --format json
```

**Example output:**
```
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Page Name     ┃ Code Length  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Calendar      │ 6,760 chars  │
│ AddEvent      │ 15,364 chars │
│ FamilyMembers │ 23,645 chars │
│ Settings      │ 44,283 chars │
└───────────────┴──────────────┘
```

### 5. `base44 app switch`
Switch between different Base44 apps using domain names.

```bash
# Switch to a different app and save
base44 app switch family-flow-55bc26d2.base44.app

# Switch without saving (temporary)
base44 app switch my-app.base44.app --no-save
```

**How it works:**
1. Takes a domain name (without `https://`)
2. Looks up the app ID from Base44's domain API
3. Updates your current profile with the new app ID
4. **Keeps your existing API key** (assumes same key works for all apps)

**Example:**
```bash
$ base44 app switch family-flow-55bc26d2.base44.app
Looking up app ID for domain: family-flow-55bc26d2.base44.app
Found app ID: 68642fa07b411bd555bc26d2
App Name: FamilyFlow
Description: FamilyFlow מארגן את חיי המשפחה שלך
Success: Switched to app: FamilyFlow (68642fa07b411bd555bc26d2)
Success: App ID saved to profile: production
```

## Use Cases

### 1. Discover App Structure
Before working with a new app, explore its structure:

```bash
# Get overview
base44 app details

# List available entities
base44 app entities

# See what pages exist
base44 app pages
```

### 2. Work with Multiple Apps
Switch between apps seamlessly:

```bash
# Switch to app 1
base44 app switch app1.base44.app

# Work with entities
base44 entity list User --limit 5

# Switch to app 2
base44 app switch app2.base44.app

# Work with different entities
base44 entity list Task
```

### 3. Query Specific Apps Without Switching
Use `--app-id` to query other apps without changing your current context:

```bash
# Check entities in another app
base44 app entities --app-id 68630c0fcb589f2fa5c22132

# Get info from another app
base44 app info --app-id 68630c0fcb589f2fa5c22132
```

## API Endpoints Used

### 1. App Information
- **Endpoint:** `GET https://app.base44.com/api/apps/public/prod/by-id/{app_id}`
- **Authentication:** Requires `api_key` header
- **Returns:** Full app metadata including entities, pages, settings

### 2. Domain to App ID Lookup
- **Endpoint:** `GET https://base44.app/api/apps/public/prod/domain/{domain}`
- **Authentication:** Public endpoint (no auth required)
- **Returns:** App ID as a string

## Configuration

When you use `base44 app switch`, the CLI updates your `~/.base44/config.yaml`:

**Before:**
```yaml
default_profile: production

profiles:
  production:
    server_url: https://app.base44.com
    app_id: old-app-id
    user_token: your-api-key
```

**After:**
```yaml
default_profile: production

profiles:
  production:
    server_url: https://app.base44.com
    app_id: new-app-id    # Updated!
    user_token: your-api-key  # Unchanged
```

## Tips

1. **Same API Key for All Apps:** The `switch` command assumes your API key works for all apps under your organization. This is typical for Base44 apps in the same organization.

2. **Domain Format:** Always use the domain without `https://`:
   - ✅ `family-flow-55bc26d2.base44.app`
   - ❌ `https://family-flow-55bc26d2.base44.app`

3. **Temporary Queries:** Use `--app-id` for one-off queries without switching:
   ```bash
   base44 app entities --app-id <other-app-id>
   ```

4. **View Current App:** Check which app you're currently working with:
   ```bash
   base44 config show
   ```

## Examples

### Example 1: Explore a New App
```bash
# Switch to the app
base44 app switch my-new-app.base44.app

# Get detailed info
base44 app details

# See available entities
base44 app entities

# List records from an entity
base44 entity list User --limit 10
```

### Example 2: Compare Two Apps
```bash
# Check entities in app 1
base44 app entities --app-id app-1-id

# Check entities in app 2
base44 app entities --app-id app-2-id

# View details of both
base44 app details --app-id app-1-id
base44 app details --app-id app-2-id
```

### Example 3: Multi-App Workflow
```bash
# Start with app 1
base44 app switch app1.base44.app

# Export data from app 1
base44 entity export Product --output app1-products.json

# Switch to app 2
base44 app switch app2.base44.app

# Import data to app 2
base44 entity import Product --file app1-products.json
```

## Troubleshooting

### "You must be logged in to access this app"
This means your API key doesn't have access to that app. Ensure:
1. You're using the correct API key
2. The app belongs to your organization
3. Your API key has the necessary permissions

### "App not found"
The domain might be incorrect. Double-check:
1. Domain spelling
2. Remove `https://` prefix
3. Ensure the app is published and accessible

### "Invalid app_id"
The app ID format is incorrect or the app doesn't exist. Get the correct app ID from:
- Base44 dashboard
- `base44 app switch <domain>` command
