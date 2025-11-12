# Sentinela - Authorization as Code Platform

<div align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-green.svg" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-purple.svg" alt="License">
</div>

## 🎯 Overview

Sentinela is a modern **Authorization as Code** platform that helps developers implement fine-grained access control using Cedar policies. Inspired by AWS IAM and Cedar policy language, Sentinela provides a complete authorization solution for microservices and applications.

### 🚀 Why Sentinela?

- **Policy as Code**: Write authorization policies in Cedar - a simple, powerful policy language
- **Microservices Ready**: Built for distributed architectures with separate auth, policy, and business services
- **Developer Friendly**: RESTful APIs, SDKs, and intuitive web interface
- **Production Grade**: JWT authentication, audit logging, and monitoring capabilities
- **Open Source**: MIT licensed - deploy anywhere, customize everything

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Identity      │    │   Policy        │    │   Application   │
│   Provider      │    │   Engine        │    │   Services      │
│                 │    │                 │    │                 │
│ • Keycloak     │◄──►│ • Cedar PEP     │◄──►│ • Business API  │
│ • Auth0        │    │ • Policy Store   │    │ • Microservices│
│ • OIDC         │    │ • OPAL Sync     │    │ • Web Apps     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-org/sentinela.git
cd sentinela

# Start all services
docker-compose up -d

# Or run locally
python mock_keycloak.py &      # Port 8081
python working_policy_api_flask.py &  # Port 8000  
python working_business_api_flask.py & # Port 8001
```

### 2. First Authorization Policy

Create your first policy in Cedar:

```cedar
// Allow Alice to read public documents
policy PublicDocumentAccess {
    permit(
        principal in User::"alice",
        action in Action::"read",
        resource in Document::"public"
    );
}

// Allow managers to perform any action on any document
policy AdminAccess {
    permit(
        principal in Group::"managers",
        action in Action::*,
        resource in Document::*
    );
}
```

### 3. Test Authorization

```bash
# Get authentication token
curl -X POST http://localhost:8081/realms/my-app/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'client_id=sentinela-api&client_secret=sentinela-secret&username=alice&password=alice123&grant_type=password'

# Test authorization decision
curl -X POST http://localhost:8001/authorize \
  -H 'Content-Type: application/json' \
  -d '{
    "principal": "User::\"alice\"",
    "action": "Action::\"read\"",
    "resource": "Document::\"public\""
  }'
```

## 📚 Core Concepts

### 🔐 Authentication vs Authorization

**Authentication (AuthN)**: Who are you?
- JWT tokens from identity providers
- User authentication and session management
- Identity verification

**Authorization (AuthZ)**: What can you do?
- Policy evaluation and access decisions
- Permission checking and enforcement
- Access control

### 🎯 Policy Evaluation Request (PER)

Sentinela evaluates requests using the PER model:

```json
{
  "principal": "User::\"alice\"",           // WHO is making the request
  "action": "Action::\"read\"",            // WHAT they want to do
  "resource": "Document::\"public\"",       // WHAT they want to access
  "context": {                             // ADDITIONAL context
    "time": "2025-01-12T10:30:00Z",
    "location": "office",
    "device": "laptop"
  }
}
```

### 🌲 Cedar Policy Language

Cedar is a simple, expressive policy language:

```cedar
// Basic permit
permit(principal, action, resource);

// Conditional permit with when clause
permit(
    principal in User::"alice",
    action in Action::"read",
    resource in Document::"confidential"
) when {
    principal.hasClearance >= resource.classification
};

// Group-based access
permit(
    principal in Group::"employees",
    action in Action::"read",
    resource in Document::"hr"
) when {
    principal.department == "HR" || 
    resource.owner == principal
};

// Attribute-based access
permit(
    principal,
    action in Action::"access",
    resource in System::"database"
) when {
    principal.role in ["admin", "dba"] &&
    action.time >= "09:00" &&
    action.time <= "17:00"
};
```

## 🔧 Integration Guides

### 🐍 Python Integration

```python
from sentinela import SentinelaClient

# Initialize client
client = SentinelaClient(
    policy_api_url="http://localhost:8000",
    auth_api_url="http://localhost:8081"
)

# Check authorization
result = client.authorize(
    principal="User::\"alice\"",
    action="Action::\"read\"",
    resource="Document::\"public\""
)

if result.allowed:
    print("Access granted!")
    # Proceed with business logic
else:
    print("Access denied!")
    # Return 403 Forbidden
```

### 🌐 JavaScript/Node.js Integration

```javascript
import { SentinelaClient } from '@sentinela/sdk';

const client = new SentinelaClient({
  policyApiUrl: 'http://localhost:8000',
  authApiUrl: 'http://localhost:8081'
});

// Middleware for Express.js
app.use('/api/documents', sentinelaMiddleware({
  client,
  getResource: (req) => `Document::"${req.params.id}"`,
  getAction: () => 'Action::"read"'
}));

// Manual check
const result = await client.authorize({
  principal: `User::"${user.id}"`,
  action: 'Action::"read"',
  resource: 'Document::"secret"'
});
```

### 🐳 Docker Integration

```dockerfile
FROM node:18-alpine

# Install Sentinela sidecar
RUN npm install -g @sentinela/sidecar

# Your application
COPY . /app
WORKDIR /app
RUN npm install

# Start both services
CMD ["sentinela-sidecar", "--", "node", "server.js"]
```

## 📋 Policy Management

### 🎛️ Web Interface

Access the web interface at `http://localhost:5000`:

- **Dashboard**: System status and metrics
- **Policies**: Create, edit, and manage policies
- **Users**: Manage user authentication and groups
- **Audit**: View authorization decisions and logs
- **Testing**: Test policies and authorization decisions

### 🔌 API Management

```bash
# List all policies
curl http://localhost:8000/policies

# Create new policy
curl -X POST http://localhost:8000/policies \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "DocumentAccess",
    "description": "Document access control",
    "policy": "permit(principal in User::\"alice\", action in Action::\"read\", resource in Document::\"public\");"
  }'

# Update policy
curl -X PUT http://localhost:8000/policies/123 \
  -H 'Content-Type: application/json' \
  -d '{"policy": "permit(principal, action, resource);"}'

# Delete policy
curl -X DELETE http://localhost:8000/policies/123
```

## 🛡️ Advanced Features

### 🔄 Policy Distribution with OPAL

```yaml
# opal-config.yaml
policy_sources:
  - url: "http://localhost:8000/policies"
    polling_interval: 30
    data_type: "cedar"

data_sources:
  - url: "http://localhost:8001/users"
    polling_interval: 60
    data_type: "json"
```

### 📊 Audit and Monitoring

```bash
# Enable audit logging
export SENTINELA_AUDIT_ENABLED=true
export SENTINELA_AUDIT_DESTINATION="http://localhost:9090"

# View audit logs
curl http://localhost:8000/audit/logs \
  -H 'Authorization: Bearer <admin-token>'
```

### 🔍 Policy Testing

```python
# Test policy suite
from sentinela.testing import PolicyTest

test = PolicyTest()

# Add test cases
test.add_case(
    principal="User::\"alice\"",
    action="Action::\"read\"",
    resource="Document::\"public\"",
    expected=True,
    description="Alice can read public documents"
)

test.add_case(
    principal="User::\"bob\"",
    action="Action::\"delete\"",
    resource="Document::\"secret\"",
    expected=False,
    description="Bob cannot delete secret documents"
)

# Run tests
results = test.run()
print(f"Passed: {results.passed}/{results.total}")
```

## 🏢 Production Deployment

### 🚀 Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentinela-policy-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentinela-policy-api
  template:
    metadata:
      labels:
        app: sentinela-policy-api
    spec:
      containers:
      - name: policy-api
        image: sentinela/policy-api:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: sentinela-secrets
              key: database-url
        - name: KEYCLOAK_URL
          value: "http://keycloak:8080"
```

### 📈 Monitoring and Observability

```yaml
# Prometheus metrics
monitoring:
  enabled: true
  metrics_port: 9090
  metrics_path: /metrics
  
# Health checks
health:
  endpoint: /health
  interval: 30s
  timeout: 10s
  retries: 3
```

## 🔧 Configuration

### 📄 Environment Variables

```bash
# Core Configuration
SENTINELA_ENV=production
SENTINELA_LOG_LEVEL=info
SENTINELA_PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/sentinela
DATABASE_POOL_SIZE=20

# Authentication
KEYCLOAK_URL=https://auth.company.com
KEYCLOAK_REALM=production
JWT_SECRET=your-secret-key

# Policy Engine
CEDAR_TIMEOUT=5000
POLICY_CACHE_TTL=300
POLICY_VALIDATION_ENABLED=true

# Monitoring
AUDIT_ENABLED=true
AUDIT_DESTINATION=elasticsearch
METRICS_ENABLED=true
```

### 🔒 Security Best Practices

1. **Use HTTPS in production**
2. **Rotate JWT secrets regularly**
3. **Implement rate limiting**
4. **Enable audit logging**
5. **Use least privilege principle**
6. **Validate all inputs**
7. **Monitor for anomalies**

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-org/sentinela.git
cd sentinela

# Setup development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Start development services
make dev
```

## 📖 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [Policy Language Reference](docs/cedar-language.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Security Best Practices](docs/security.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🆘 Support

- 📧 Email: support@sentinela.io
- 💬 Discord: [Join our community](https://discord.gg/sentinela)
- 📖 Documentation: [docs.sentinela.io](https://docs.sentinela.io)
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/sentinela/issues)

## 📄 License

Sentinela is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <p>Built with ❤️ by the Sentinela team</p>
  <p>Empowering developers with modern authorization</p>
</div>