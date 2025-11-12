# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sentinela is a comprehensive Identity and Access Management (IAM) system featuring policy-based authorization using Cedar policies, user management, and a modern web interface. The system follows a microservices architecture with separate services for authentication, policy management, and business logic.

## Architecture

### Core Components

1. **Mock Keycloak Service** (Port 8080)
   - Handles authentication and JWT token generation
   - Mock implementation for development/testing
   - Located in: `mock_keycloak.py`

2. **Policy API Service** (Port 8001)
   - Manages Cedar policy CRUD operations
   - FastAPI-based service
   - Main entry: `policy_api/src/main.py`
   - Working Flask version: `working_policy_api_flask.py`

3. **Business API Service** (Port 8002)
   - Example business service with authorization
   - Integrates Cedar engine for authorization decisions
   - Main entry: `business_api_service/src/main.py`
   - Working Flask version: `working_business_api_flask.py`

4. **Next.js UI** (Port 3000)
   - Modern web interface with TypeScript and Tailwind CSS
   - Monaco-based policy editor with syntax highlighting
   - Located in: `sentinela-ui/`

5. **Cedar Policy Engine**
   - Core authorization engine implementing Cedar policy language
   - Located in: `final_cedar_engine.py`
   - Direct policy parsing with condition evaluation

### Service Architecture Pattern

```
User Request → Mock Keycloak (JWT) → Business API → Cedar Engine → Authorization Decision
                                           ↓
                                      Policy API (Policy Management)
```

## Development Commands

### Quick Start with Docker

**Development Environment:**
```bash
# Start all services
docker-compose -f docker-compose.dev.yml up --build

# Start in detached mode
docker-compose -f docker-compose.dev.yml up -d --build

# View logs
docker-compose logs -f
```

**Production Environment:**
```bash
docker-compose up --build
docker-compose up -d --build
```

### Local Development (Backend)

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Start Individual Services:**
```bash
# Mock Keycloak
python mock_keycloak.py

# Policy API (Flask version)
python working_policy_api_flask.py

# Business API (Flask version)
python working_business_api_flask.py

# Policy API (FastAPI version)
cd policy_api && uvicorn src.main:app --reload --port 8001

# Business API (FastAPI version)
cd business_api_service && uvicorn src.main:app --reload --port 8002
```

### Frontend Development

```bash
cd sentinela-ui
npm install
npm run dev       # Start development server
npm run build     # Build for production
npm run start     # Start production server
npm run lint      # Run ESLint
```

### Testing

**Integration Tests:**
```bash
# Complete end-to-end test suite
python final_integration_test.py

# Component-specific integration tests
python integration_test_complete.py
```

**Service Tests:**
```bash
# Test Policy API
python test_policy_api.py

# Test individual services
python test_services.py

# Test current components
python test_current_components.py
```

**Cedar Engine Tests:**
```bash
# Test Cedar policy evaluation (5/5 test cases)
python final_cedar_engine.py
```

**Setup Scripts:**
```bash
# Automated Keycloak setup
python auto_keycloak_setup.py

# Manual Keycloak setup
python manual_keycloak_setup.py
```

## Key Technical Concepts

### Cedar Policy Structure

Policies use Cedar syntax for declarative authorization:
```cedar
policy DocumentRead {
    permit(
        principal in User::"alice",
        action in Action::"read",
        resource in Document::"public"
    );
}
```

The engine evaluates:
- **Principal**: User or entity making the request (e.g., `User::"alice"`)
- **Action**: Operation being performed (e.g., `Action::"read"`)
- **Resource**: Target of the action (e.g., `Document::"public"`)
- **Context**: Additional data (e.g., user groups, attributes)

### Authorization Request Flow

1. Client obtains JWT token from Mock Keycloak
2. Client makes request to Business API with token
3. Business API validates token and extracts user info
4. Business API creates authorization request with principal, action, resource
5. Cedar engine evaluates request against loaded policies
6. Engine returns allow/deny decision
7. Business API enforces decision

### Policy Evaluation Logic

Located in `final_cedar_engine.py`:
- Policies are parsed and stored as condition lists
- Each condition checks principal, action, resource, or context
- All conditions must match for a policy to apply
- First matching permit policy grants access
- Default is deny if no policy matches

### Service Communication

Services use REST APIs with JSON:
- **Authentication**: JWT Bearer tokens in Authorization header
- **Policy Management**: RESTful CRUD operations
- **Authorization**: POST requests with authorization context
- **Health Checks**: GET endpoints returning service status

## Code Organization

### Backend Services

```
policy_api/
├── src/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models/              # Data models
│   ├── routers/             # API endpoints
│   └── services/            # External service clients
└── requirements.txt

business_api_service/
├── src/
│   ├── main.py              # FastAPI application
│   ├── models/              # Data models
│   ├── services/
│   │   ├── cedar_engine.py  # Authorization engine
│   │   ├── opal_client.py   # OPAL integration
│   │   └── keycloak_service.py
│   └── utils/               # Utilities
└── requirements.txt
```

### Frontend

```
sentinela-ui/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── dashboard/       # Dashboard page
│   │   ├── policies/        # Policy management
│   │   ├── users/           # User management
│   │   └── audit/           # Audit logs
│   ├── components/          # React components
│   │   ├── ui/              # Base UI components
│   │   └── features/        # Feature-specific components
│   └── lib/                 # Utilities and API client
└── package.json
```

## Important Implementation Details

### Mock Keycloak

- Stores users in memory during runtime
- Generates valid JWT tokens without signature verification
- Default users: alice (employee), bob (employee), admin (manager + employee)
- Client credentials: `sentinela-api` / `sentinela-secret`

### In-Memory Storage

Both Policy API and Business API use in-memory storage for MVP:
- **Policy API**: `policies_db` list with auto-incrementing IDs
- **Business API**: `documents_db` list with sample documents
- Data is lost on service restart
- Replace with PostgreSQL for production

### FastAPI vs Flask

The project has two implementations:
- **FastAPI versions**: `policy_api/src/main.py`, `business_api_service/src/main.py`
- **Flask versions**: `working_policy_api_flask.py`, `working_business_api_flask.py`
- Both are functional; FastAPI versions are more modern
- Docker setup uses Flask versions for simplicity

### Health Check Endpoints

All services expose health checks:
- `GET /health` - Basic health status
- `GET /health/detailed` - Detailed service status including dependencies

## Environment Configuration

### Backend Services

Create `.env` file with:
```env
FLASK_ENV=development
KEYCLOAK_URL=http://localhost:8080
POLICY_API_URL=http://localhost:8001
BUSINESS_API_URL=http://localhost:8002
```

### Frontend

Create `sentinela-ui/.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_POLICY_API_URL=http://localhost:8001
NEXT_PUBLIC_BUSINESS_API_URL=http://localhost:8002
NEXT_PUBLIC_KEYCLOAK_URL=http://localhost:8080
```

## Common Development Tasks

### Adding a New Policy

1. Use Policy API POST endpoint or UI
2. Cedar engine automatically loads policies on startup
3. Test policy with authorization requests

### Adding a New Resource Type

1. Define resource type in Cedar policies
2. Update Cedar engine to recognize resource type
3. Add business logic in Business API for resource
4. Implement UI components for resource management

### Modifying Authorization Logic

1. Update Cedar policies in Policy API
2. Modify policy evaluation in `final_cedar_engine.py` if needed
3. Update Business API authorization checks
4. Run integration tests to verify changes

### Debugging Authorization Issues

1. Check logs in Business API for authorization requests
2. Verify policy syntax in Cedar engine tests
3. Test policy evaluation with `final_cedar_engine.py`
4. Use health endpoints to verify service connectivity

## Production Considerations

Current MVP limitations requiring production fixes:

1. **Replace Mock Keycloak**: Use real Keycloak instance with proper JWT validation
2. **Add Database**: Replace in-memory storage with PostgreSQL
3. **OPAL Integration**: Implement OPAL for policy distribution (clients in `services/opal_*.py`)
4. **Security Hardening**: Add rate limiting, input validation, CORS restrictions
5. **Monitoring**: Add comprehensive logging, metrics, and alerting
6. **Performance**: Implement policy caching, connection pooling
7. **Multi-tenancy**: Add tenant isolation and resource scoping

## Testing Strategy

The codebase includes comprehensive testing:

- **Unit Tests**: Test individual components (Cedar engine, services)
- **Integration Tests**: Test service interactions end-to-end
- **Authorization Tests**: Verify Cedar policy evaluation correctness
- **Health Checks**: Verify service availability

Run tests before committing changes to ensure system integrity.
