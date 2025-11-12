# Getting Started with Sentinela

Welcome to Sentinela! This guide will help you get up and running with modern authorization in minutes.

## 🎯 What You'll Learn

- How Sentinela works and why it's different
- Setting up your first authorization policy
- Integrating with your application
- Best practices for production deployment

## 🚀 What is Sentinela?

Sentinela is an **Authorization as Code** platform that helps you implement fine-grained access control using Cedar policies. Think of it as a "bouncer" for your applications - it decides who can access what, when, and how.

### Traditional vs Modern Authorization

| Traditional Approach | Sentinela Approach |
|---------------------|-------------------|
| Hard-coded roles in application logic | Declarative policies in Cedar |
| Database-driven permissions | Policy-as-code version control |
| Complex if/else statements | Simple, readable policies |
| Difficult to audit and test | Git-based policy management |
| Slow to change permissions | Instant policy updates |

## 🏗️ Core Concepts

### 1. Authentication vs Authorization

**Authentication (AuthN)**: "Who are you?"
- JWT tokens, OAuth, SAML
- User identity verification
- Login/logout functionality

**Authorization (AuthZ)**: "What can you do?"
- Policy evaluation and decisions
- Permission checking
- Access control enforcement

### 2. The PER Model

Sentinela evaluates requests using the **PER** model:

```
P = Principal (WHO)    // User, service, or API key
E = Entity (WHAT)       // Resource, data, or action target  
R = Request (HOW)       // Action, operation, or method
```

### 3. Cedar Policy Language

Cedar is a simple, expressive policy language inspired by AWS IAM:

```cedar
// Simple permit
permit(principal, action, resource);

// Conditional access
permit(
    principal in User::"alice",
    action in Action::"read",
    resource in Document::"confidential"
) when {
    principal.clearance >= resource.classification
};

// Group-based permissions
permit(
    principal in Group::"managers",
    action in Action::*,
    resource in Document::*
);
```

## 🛠️ Installation Options

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/sentinela.git
cd sentinela

# Start all services
docker-compose up -d

# Verify installation
curl http://localhost:8000/health/
```

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Start services individually
python mock_keycloak.py &          # Port 8081 - Identity
python working_policy_api_flask.py &  # Port 8000 - Policy Management  
python working_business_api_flask.py & # Port 8001 - Application

# Or use the web interface
python web_interface.py &           # Port 5000 - Admin UI
```

### Option 3: Cloud Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Or use Terraform
cd terraform/
terraform apply
```

## 🎯 Your First Policy

Let's create a simple document access policy:

### Step 1: Define the Policy

Create a file `document_policy.cedar`:

```cedar
policy DocumentAccess {
    // Alice can read public documents
    permit(
        principal in User::"alice",
        action in Action::"read",
        resource in Document::"public"
    );
    
    // Managers can do anything with any document
    permit(
        principal in Group::"managers",
        action in Action::*,
        resource in Document::*
    );
    
    // Employees can read HR documents if they're in HR department
    permit(
        principal in Group::"employees",
        action in Action::"read",
        resource in Document::"hr"
    ) when {
        principal.department == "HR"
    };
}
```

### Step 2: Upload the Policy

```bash
# Using the API
curl -X POST http://localhost:8000/policies \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "DocumentAccess",
    "description": "Document access control policy",
    "policy": "$(cat document_policy.cedar)"
  }'

# Using the web interface
# Open http://localhost:5000 and navigate to Policies tab
```

### Step 3: Test the Policy

```bash
# Test Alice accessing public document
curl -X POST http://localhost:8001/authorize \
  -H 'Content-Type: application/json' \
  -d '{
    "principal": "User::\"alice\"",
    "action": "Action::\"read\"",
    "resource": "Document::\"public\""
  }'

# Response: {"allow": true, "principal": "...", "action": "...", "resource": "..."}

# Test Bob accessing secret document
curl -X POST http://localhost:8001/authorize \
  -H 'Content-Type: application/json' \
  -d '{
    "principal": "User::\"bob\"",
    "action": "Action::\"read\"",
    "resource": "Document::\"secret\""
  }'

# Response: {"allow": false, "reason": "No matching policy rule"}
```

## 🔐 Adding Authentication

Sentinela integrates with any OIDC-compatible identity provider:

### Step 1: Configure Identity Provider

```bash
# Using mock Keycloak (for development)
curl -X POST http://localhost:8081/realms/my-app/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'client_id=sentinela-api&client_secret=sentinela-secret&username=alice&password=alice123&grant_type=password'

# Using real Keycloak
export KEYCLOAK_URL=https://auth.company.com
export KEYCLOAK_REALM=production
```

### Step 2: Protect Your Application

```python
from flask import Flask, request, jsonify
from sentinela import SentinelaMiddleware

app = Flask(__name__)

# Add Sentinela middleware
@app.before_request
def check_authorization():
    # Extract JWT token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    # Validate token with identity provider
    user_info = validate_jwt(token)
    
    # Check authorization with Sentinela
    auth_result = sentinela.authorize(
        principal=f"User::\"{user_info['sub']}\"",
        action=f"Action::\"{request.method.lower()}\"",
        resource=f"Document::\"{request.path}\""
    )
    
    if not auth_result.allow:
        return jsonify({"error": "Access denied"}), 403

@app.route('/documents/<doc_id>')
def get_document(doc_id):
    # Your business logic here
    return jsonify({"document": get_document_from_db(doc_id)})
```

## 🎛️ Using the Web Interface

Sentinela provides a beautiful web interface for managing authorization:

### Access the Interface

Open your browser and navigate to: `http://localhost:5000`

### Key Features

1. **Dashboard**: System health and metrics
2. **Policies**: Create, edit, and test policies
3. **Users**: Manage authentication and groups
4. **Audit**: View authorization decisions
5. **Testing**: Interactive policy testing

### Creating Policies in the UI

1. Navigate to **Policies** tab
2. Click **➕ Create Policy**
3. Fill in the details:
   - **Name**: Human-readable policy name
   - **Description**: What the policy does
   - **Policy**: Cedar policy code
4. Click **💾 Create Policy**

### Testing Policies

1. Go to **Authorization** tab
2. Select principal, action, and resource
3. Click **🛡️ Verify Authorization**
4. View the decision and reasoning

## 📊 Monitoring and Debugging

### Health Checks

```bash
# Check all services
curl http://localhost:8000/health/    # Policy API
curl http://localhost:8001/health      # Business API
curl http://localhost:8081/health      # Identity Provider
```

### Audit Logs

```bash
# View recent authorization decisions
curl http://localhost:8000/audit/logs \
  -H 'Authorization: Bearer <admin-token>'

# Filter by user
curl http://localhost:8000/audit/logs?user=alice \
  -H 'Authorization: Bearer <admin-token>'
```

### Debug Mode

```bash
# Enable debug logging
export SENTINELA_DEBUG=true
export SENTINELA_LOG_LEVEL=debug

# View detailed policy evaluation
curl -X POST http://localhost:8001/authorize \
  -H 'Content-Type: application/json' \
  -H 'X-Debug: true' \
  -d '{"principal": "...", "action": "...", "resource": "..."}'
```

## 🚀 Next Steps

Congratulations! You now have:

✅ **Working authorization system** with Cedar policies  
✅ **Identity integration** with JWT authentication  
✅ **Policy management** via API and web interface  
✅ **Real-time authorization** decisions  

### What to Explore Next

1. **Advanced Policies**: Learn complex Cedar patterns
2. **Production Deployment**: Kubernetes, monitoring, scaling
3. **Policy Distribution**: OPAL for dynamic policy updates
4. **SDK Integration**: Language-specific libraries
5. **Security Best Practices**: Hardening and compliance

### Continue Learning

- [Policy Language Reference](policy-language.md)
- [API Documentation](api-reference.md)
- [Deployment Guide](deployment.md)
- [Security Best Practices](security.md)

## 🆘 Need Help?

- 📖 [Documentation](https://docs.sentinela.io)
- 💬 [Discord Community](https://discord.gg/sentinela)
- 🐛 [GitHub Issues](https://github.com/your-org/sentinela/issues)
- 📧 [Support](mailto:support@sentinela.io)

---

**Happy authorizing! 🎉**