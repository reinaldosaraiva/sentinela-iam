# API Reference

Complete API documentation for Sentinela Authorization Platform.

## 🌐 Base URLs

| Environment | Base URL |
|-------------|-----------|
| Development | `http://localhost:8000` |
| Staging | `https://api-staging.sentinela.io` |
| Production | `https://api.sentinela.io` |

## 🔐 Authentication

All API requests require authentication using JWT tokens or API keys.

### JWT Authentication

```bash
# Get token from identity provider
curl -X POST http://localhost:8081/realms/my-app/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'client_id=sentinela-api&client_secret=sentinela-secret&username=alice&password=alice123&grant_type=password'

# Use token in API requests
curl -H 'Authorization: Bearer <your-jwt-token>' \
  http://localhost:8000/policies
```

### API Key Authentication

```bash
# Use API key
curl -H 'X-API-Key: <your-api-key>' \
  http://localhost:8000/policies
```

## 📋 Policy Management API

### List Policies

Retrieve all authorization policies.

```http
GET /policies
```

**Response:**
```json
{
  "policies": [
    {
      "id": "policy_123",
      "name": "DocumentAccess",
      "description": "Document access control policy",
      "policy": "permit(principal in User::\"alice\", action in Action::\"read\", resource in Document::\"public\");",
      "created_at": "2025-01-12T10:30:00Z",
      "updated_at": "2025-01-12T10:30:00Z",
      "version": 1,
      "status": "active"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20
}
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|--------|---------|-------------|
| page | integer | 1 | Page number for pagination |
| per_page | integer | 20 | Items per page (max 100) |
| search | string | - | Search policies by name or description |
| status | string | - | Filter by status (active, inactive) |

### Get Policy

Retrieve a specific policy by ID.

```http
GET /policies/{policy_id}
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|--------|-------------|
| policy_id | string | Unique policy identifier |

**Response:**
```json
{
  "id": "policy_123",
  "name": "DocumentAccess",
  "description": "Document access control policy",
  "policy": "permit(principal in User::\"alice\", action in Action::\"read\", resource in Document::\"public\");",
  "created_at": "2025-01-12T10:30:00Z",
  "updated_at": "2025-01-12T10:30:00Z",
  "version": 1,
  "status": "active",
  "metadata": {
    "author": "alice@company.com",
    "tags": ["documents", "access-control"]
  }
}
```

### Create Policy

Create a new authorization policy.

```http
POST /policies
```

**Request Body:**
```json
{
  "name": "DocumentAccess",
  "description": "Document access control policy",
  "policy": "permit(principal in User::\"alice\", action in Action::\"read\", resource in Document::\"public\");",
  "metadata": {
    "author": "alice@company.com",
    "tags": ["documents", "access-control"]
  }
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|--------|----------|-------------|
| name | string | ✅ | Human-readable policy name |
| description | string | ✅ | Policy description |
| policy | string | ✅ | Cedar policy code |
| metadata | object | ❌ | Additional metadata (author, tags, etc.) |

**Response:**
```json
{
  "id": "policy_456",
  "name": "DocumentAccess",
  "description": "Document access control policy",
  "policy": "permit(principal in User::\"alice\", action in Action::\"read\", resource in Document::\"public\");",
  "created_at": "2025-01-12T11:00:00Z",
  "updated_at": "2025-01-12T11:00:00Z",
  "version": 1,
  "status": "active"
}
```

### Update Policy

Update an existing policy.

```http
PUT /policies/{policy_id}
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|--------|-------------|
| policy_id | string | Unique policy identifier |

**Request Body:**
```json
{
  "name": "UpdatedDocumentAccess",
  "description": "Updated document access control policy",
  "policy": "permit(principal in User::\"alice\", action in Action::\"read\", resource in Document::\"public\");"
}
```

**Response:**
```json
{
  "id": "policy_123",
  "name": "UpdatedDocumentAccess",
  "description": "Updated document access control policy",
  "policy": "permit(principal in User::\"alice\", action in Action::\"read\", resource in Document::\"public\");",
  "updated_at": "2025-01-12T11:30:00Z",
  "version": 2,
  "status": "active"
}
```

### Delete Policy

Delete a policy.

```http
DELETE /policies/{policy_id}
```

**Response:**
```json
{
  "message": "Policy deleted successfully",
  "id": "policy_123"
}
```

### Validate Policy

Validate Cedar policy syntax without creating it.

```http
POST /policies/validate
```

**Request Body:**
```json
{
  "policy": "permit(principal in User::\"alice\", action in Action::\"read\", resource in Document::\"public\");"
}
```

**Response:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

## 🛡️ Authorization API

### Check Authorization

Evaluate an authorization request against all active policies.

```http
POST /authorize
```

**Request Body:**
```json
{
  "principal": "User::\"alice\"",
  "action": "Action::\"read\"",
  "resource": "Document::\"public\"",
  "context": {
    "time": "2025-01-12T10:30:00Z",
    "location": "office",
    "device": "laptop",
    "ip_address": "192.168.1.100"
  }
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|--------|----------|-------------|
| principal | string | ✅ | Entity making the request |
| action | string | ✅ | Action being performed |
| resource | string | ✅ | Resource being accessed |
| context | object | ❌ | Additional context for evaluation |

**Response:**
```json
{
  "allow": true,
  "principal": "User::\"alice\"",
  "action": "Action::\"read\"",
  "resource": "Document::\"public\"",
  "reason": "Policy 'DocumentAccess' permits this request",
  "policies_evaluated": [
    {
      "policy_id": "policy_123",
      "policy_name": "DocumentAccess",
      "decision": "permit",
      "matched_rules": ["permit(principal in User::\"alice\", action in Action::\"read\", resource in Document::\"public\")"]
    }
  ],
  "evaluation_time_ms": 15,
  "request_id": "req_789"
}
```

### Batch Authorization

Check multiple authorization requests in a single call.

```http
POST /authorize/batch
```

**Request Body:**
```json
{
  "requests": [
    {
      "principal": "User::\"alice\"",
      "action": "Action::\"read\"",
      "resource": "Document::\"public\""
    },
    {
      "principal": "User::\"bob\"",
      "action": "Action::\"read\"",
      "resource": "Document::\"secret\""
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "allow": true,
      "principal": "User::\"alice\"",
      "action": "Action::\"read\"",
      "resource": "Document::\"public\""
    },
    {
      "allow": false,
      "principal": "User::\"bob\"",
      "action": "Action::\"read\"",
      "resource": "Document::\"secret\"",
      "reason": "No matching policy rule"
    }
  ],
  "total_evaluated": 2
}
```

## 📊 Audit API

### List Audit Logs

Retrieve authorization decision logs.

```http
GET /audit/logs
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|--------|---------|-------------|
| from | string | - | Start date (ISO 8601) |
| to | string | - | End date (ISO 8601) |
| principal | string | - | Filter by principal |
| resource | string | - | Filter by resource |
| decision | string | - | Filter by decision (allow, deny) |
| page | integer | 1 | Page number |
| per_page | integer | 50 | Items per page |

**Response:**
```json
{
  "logs": [
    {
      "id": "log_123",
      "timestamp": "2025-01-12T10:30:00Z",
      "principal": "User::\"alice\"",
      "action": "Action::\"read\"",
      "resource": "Document::\"public\"",
      "decision": "allow",
      "reason": "Policy 'DocumentAccess' permits this request",
      "policies_evaluated": ["policy_123"],
      "evaluation_time_ms": 15,
      "request_id": "req_789",
      "user_agent": "Mozilla/5.0...",
      "ip_address": "192.168.1.100"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 50
}
```

### Get Audit Log

Retrieve a specific audit log entry.

```http
GET /audit/logs/{log_id}
```

## 🏥 Health API

### System Health

Check the health of all system components.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-12T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": {
      "status": "healthy",
      "response_time_ms": 5,
      "connections": 10
    },
    "policy_engine": {
      "status": "healthy",
      "policies_loaded": 25,
      "evaluation_time_avg_ms": 12
    },
    "identity_provider": {
      "status": "healthy",
      "url": "http://localhost:8081"
    },
    "opal_client": {
      "status": "healthy",
      "last_sync": "2025-01-12T10:25:00Z"
    }
  }
}
```

### Component Health

Check health of a specific component.

```http
GET /health/{component}
```

**Path Parameters:**

| Parameter | Description |
|-----------|-------------|
| component | Component name (database, policy_engine, identity_provider, opal_client) |

## 📈 Metrics API

### System Metrics

Retrieve system performance metrics.

```http
GET /metrics
```

**Response:**
```json
{
  "timestamp": "2025-01-12T10:30:00Z",
  "authorization": {
    "total_requests": 10000,
    "allowed_requests": 8500,
    "denied_requests": 1500,
    "avg_response_time_ms": 12,
    "p95_response_time_ms": 25
  },
  "policies": {
    "total_policies": 25,
    "active_policies": 23,
    "inactive_policies": 2
  },
  "errors": {
    "error_rate": 0.02,
    "total_errors": 200,
    "last_error": "2025-01-12T09:45:00Z"
  }
}
```

## 🔧 Configuration API

### Get Configuration

Retrieve system configuration.

```http
GET /config
```

**Response:**
```json
{
  "cedar": {
    "timeout_ms": 5000,
    "max_policy_size": 10000,
    "cache_ttl_seconds": 300
  },
  "authentication": {
    "jwt_expiry_hours": 24,
    "refresh_token_days": 30,
    "allowed_issuers": ["http://localhost:8081"]
  },
  "audit": {
    "enabled": true,
    "retention_days": 90,
    "log_level": "info"
  }
}
```

### Update Configuration

Update system configuration.

```http
PUT /config
```

## 🚨 Error Responses

All API endpoints return consistent error responses.

### Standard Error Format

```json
{
  "error": {
    "code": "POLICY_NOT_FOUND",
    "message": "Policy with ID 'policy_123' not found",
    "details": {
      "policy_id": "policy_123",
      "timestamp": "2025-01-12T10:30:00Z"
    },
    "request_id": "req_456"
  }
}
```

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Entity |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

### Error Codes

| Error Code | Description |
|-------------|-------------|
| POLICY_NOT_FOUND | Policy does not exist |
| INVALID_POLICY_SYNTAX | Cedar policy syntax error |
| UNAUTHORIZED | Invalid or missing authentication |
| FORBIDDEN | Insufficient permissions |
| RATE_LIMITED | Too many requests |
| VALIDATION_ERROR | Request validation failed |
| INTERNAL_ERROR | Server error |

## 🔄 Rate Limiting

API requests are rate limited to prevent abuse.

| Tier | Requests per Minute | Burst |
|-------|-------------------|--------|
| Free | 100 | 200 |
| Pro | 1000 | 2000 |
| Enterprise | 10000 | 20000 |

Rate limit headers are included in responses:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642694400
```

## 🧪 SDKs and Libraries

### Python SDK

```python
from sentinela import SentinelaClient

client = SentinelaClient(
    base_url="http://localhost:8000",
    api_key="your-api-key"
)

# Check authorization
result = client.authorize(
    principal="User::\"alice\"",
    action="Action::\"read\"",
    resource="Document::\"public\""
)

if result.allow:
    print("Access granted!")
```

### JavaScript SDK

```javascript
import { SentinelaClient } from '@sentinela/sdk';

const client = new SentinelaClient({
  baseUrl: 'http://localhost:8000',
  apiKey: 'your-api-key'
});

const result = await client.authorize({
  principal: 'User::"alice"',
  action: 'Action::"read"',
  resource: 'Document::"public"'
});
```

### Go SDK

```go
import "github.com/sentinela/go-sdk"

client := sentinela.NewClient("http://localhost:8000", "your-api-key")

result, err := client.Authorize(sentinela.AuthzRequest{
    Principal: "User::\"alice\"",
    Action:    "Action::\"read\"",
    Resource:  "Document::\"public\"",
})
```

## 📚 Additional Resources

- [Getting Started Guide](getting-started.md)
- [Policy Language Reference](policy-language.md)
- [SDK Documentation](sdks.md)
- [Deployment Guide](deployment.md)
- [Best Practices](best-practices.md)

## 🆘 Support

- 📧 Email: api-support@sentinela.io
- 💬 Discord: [API Support Channel](https://discord.gg/sentinela)
- 📖 Documentation: [docs.sentinela.io](https://docs.sentinela.io)
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/sentinela/issues)