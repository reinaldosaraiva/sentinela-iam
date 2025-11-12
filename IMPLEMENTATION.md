# Implementation Documentation - Sentinela IAM

**Date:** November 12, 2025
**Version:** 1.0.0

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Implemented Features](#implemented-features)
- [Technologies Used](#technologies-used)
- [Configuration and Execution](#configuration-and-execution)
- [Project Structure](#project-structure)

---

## Overview

**Sentinela** is a complete Identity and Access Management (IAM) platform developed with modern architecture, separating backend (FastAPI) and frontend (Next.js 14).

### Project Objectives
- Centralized management of applications, resources, and actions
- Policy-Based Access Control
- Modern and responsive administration interface
- Complete and documented RESTful API
- Secure JWT authentication

---

## Architecture

### Backend (Policy API)
```
FastAPI + PostgreSQL + SQLAlchemy
├── JWT Authentication
├── CORS configured
├── ORM with SQLAlchemy
└── Automatic documentation (Swagger/OpenAPI)
```

### Frontend (Sentinela UI)
```
Next.js 14 (App Router) + TypeScript + TailwindCSS
├── Modern React components
├── Authentication with Context API
├── Centralized HTTP client (apiClient)
└── Protected routes
```

---

## Implemented Features

### 1. Authentication and Authorization
- [x] **JWT Login System**
  - Endpoint: `POST /api/v1/auth/login`
  - JWT token with configurable expiration
  - Refresh token support
  - Secure logout

- [x] **Route Protection**
  - `ProtectedRoute` component in frontend
  - Authentication middleware in backend
  - Automatic token verification
  - Redirect to login when unauthenticated

- [x] **Session Management**
  - Global AuthContext in frontend
  - Token persistence in memory
  - Auto-logout on invalid token

### 2. Application Management
- [x] **Complete Application CRUD**
  - Paginated listing with filters
  - Create new applications
  - Edit existing applications
  - Delete applications
  - Logo upload (URL)

- [x] **Application Fields**
  - Unique Name and Slug
  - Description
  - Logo URL
  - Website URL
  - Status (active/inactive/paused)
  - Environment (production/staging/development)
  - Automatic timestamps

- [x] **Application Interface**
  - Responsive grid view
  - Real-time search
  - Filters by status and environment
  - Cards with visual preview
  - Per-application statistics

### 3. Resource Management
- [x] **Complete Resource CRUD**
  - Listing with associated action count
  - Creation linked to applications
  - Resource editing
  - Cascade deletion (removes associated actions)

- [x] **Resource Fields**
  - Name and resource type
  - Optional description
  - Link to application
  - Active/inactive status
  - Action count

- [x] **Resource Interface**
  - Expandable list showing actions
  - Type validation (lowercase, hyphens)
  - Application dropdown
  - Inline action preview

### 4. Action Management
- [x] **Complete Action CRUD**
  - Listing with resource information
  - Creation linked to resources
  - Active/inactive toggle
  - Action deletion

- [x] **Action Fields**
  - Action type (read, write, update, delete, etc.)
  - Descriptive name
  - Optional description
  - Active/inactive status
  - Link to resource

- [x] **Action Interface**
  - Grid view with cards colored by type
  - Filters by resource and status
  - Multi-field search
  - Visual status badges
  - Link to associated resource

### 5. Administrative Dashboard
- [x] **Main Dashboard**
  - Real-time statistics
  - Cards with key metrics
  - Distribution charts
  - Quick navigation

- [x] **Responsive Layout**
  - Sidebar with navigation
  - Header with user profile
  - Full mobile support
  - Dark mode ready (structure prepared)

### 6. Backend API

#### Authentication Endpoints
```
POST   /api/v1/auth/login       - Authenticate user
GET    /api/v1/auth/me          - Current user data
POST   /api/v1/auth/logout      - Logout
```

#### Application Endpoints
```
GET    /api/v1/applications/           - List applications
POST   /api/v1/applications/           - Create application
GET    /api/v1/applications/{id}       - Application details
PUT    /api/v1/applications/{id}       - Update application
DELETE /api/v1/applications/{id}       - Delete application
```

#### Resource Endpoints
```
GET    /api/v1/resources/              - List resources
POST   /api/v1/resources/              - Create resource
GET    /api/v1/resources/{id}          - Resource details
PUT    /api/v1/resources/{id}          - Update resource
DELETE /api/v1/resources/{id}          - Delete resource (cascade)
```

#### Action Endpoints
```
GET    /api/v1/actions/                - List actions
POST   /api/v1/actions/                - Create action
GET    /api/v1/actions/{id}            - Action details
PUT    /api/v1/actions/{id}            - Update action
DELETE /api/v1/actions/{id}            - Delete action
PATCH  /api/v1/actions/{id}/activate   - Activate action
PATCH  /api/v1/actions/{id}/deactivate - Deactivate action
```

### 7. Database and Models

#### Database Schema
- **Applications**: Applications registered in the system
- **Resources**: Resources managed per application
- **Actions**: Available actions per resource
- **Users**: System users
- **API Keys**: API keys for applications

#### Relationships
```
Application 1 ──→ N Resources
Resource    1 ──→ N Actions
Application 1 ──→ N API Keys
```

### 8. Development Tools

- [x] **Seed Data Script**
  - Python script to populate database with example data
  - 5 demo applications
  - 9 distributed resources
  - ~50 actions with various types
  - 3 example API Keys
  - Execution: `python seed_data.py`

- [x] **Automatic Documentation**
  - Swagger UI at `/docs`
  - ReDoc at `/redoc`
  - OpenAPI 3.0 schemas
  - Request examples

---

## Technologies Used

### Backend
| Technology | Version | Usage |
|------------|---------|-------|
| Python | 3.11+ | Main language |
| FastAPI | 0.104+ | Web framework |
| PostgreSQL | 14+ | Database |
| SQLAlchemy | 2.0+ | ORM |
| Alembic | 1.12+ | Migrations |
| Pydantic | 2.0+ | Data validation |
| python-jose | 3.3+ | JWT tokens |
| passlib | 1.7+ | Password hashing |
| uvicorn | 0.24+ | ASGI server |

### Frontend
| Technology | Version | Usage |
|------------|---------|-------|
| Next.js | 14.0.0 | React framework |
| React | 18.2+ | UI library |
| TypeScript | 5.0+ | Static typing |
| TailwindCSS | 3.3+ | Styling |
| Lucide React | 0.292+ | Icons |

---

## Configuration and Execution

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Backend Setup

1. **Create virtual environment:**
```bash
cd policy_api
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
# .env
DATABASE_URL=postgresql://user:password@localhost/sentinela
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. **Run migrations:**
```bash
alembic upgrade head
```

5. **Populate database with example data:**
```bash
python seed_data.py
```

6. **Start server:**
```bash
python -m uvicorn policy_api.src.main:app --port 8001 --reload
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd sentinela-ui
npm install
```

2. **Start development server:**
```bash
PORT=3030 npm run dev
```

3. **Access application:**
- Frontend: http://localhost:3030
- Backend API: http://localhost:8001
- Swagger Docs: http://localhost:8001/docs

### Default Credentials
```
Email: admin@sentinela.com
Password: admin123
```

---

## Project Structure

```
sentinela/
├── policy_api/                 # FastAPI Backend
│   ├── src/
│   │   ├── routers/           # API Endpoints
│   │   │   ├── auth.py
│   │   │   ├── applications.py
│   │   │   ├── resources.py
│   │   │   └── actions.py
│   │   ├── models/            # SQLAlchemy Models
│   │   │   ├── application.py
│   │   │   ├── resource.py
│   │   │   ├── action.py
│   │   │   └── user.py
│   │   ├── schemas/           # Pydantic Schemas
│   │   ├── database_pg.py     # DB Configuration
│   │   └── main.py            # Main App
│   ├── alembic/               # Migrations
│   ├── seed_data.py           # Seed Script
│   └── requirements.txt
│
├── sentinela-ui/              # Next.js Frontend
│   ├── src/
│   │   ├── app/               # Pages (App Router)
│   │   │   ├── login/
│   │   │   ├── applications/
│   │   │   ├── resources/
│   │   │   ├── actions/
│   │   │   └── dashboard/
│   │   ├── components/        # React Components
│   │   │   ├── DashboardLayout.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── contexts/          # React Contexts
│   │   │   └── AuthContext.tsx
│   │   └── lib/               # Utilities
│   │       ├── api.ts         # HTTP Client
│   │       └── auth.ts        # Auth Services
│   ├── public/
│   └── package.json
│
├── IMPLEMENTATION.md          # This file
├── ROADMAP.md                 # Next steps
└── README.md                  # Main documentation
```

---

## Technical Highlights

### 1. Secure JWT Authentication
- Tokens signed with HS256
- Configurable expiration
- Validation on all protected routes
- Logout with token invalidation

### 2. Configured CORS
- Allows communication between frontend (port 3030) and backend (port 8001)
- Support for credentials
- Custom headers allowed

### 3. Centralized HTTP Client
- `apiClient` with automatic token injection
- Centralized error handling
- Request logging
- Retry logic prepared

### 4. Data Validation
- Pydantic schemas in backend
- TypeScript interfaces in frontend
- Real-time validation in forms
- User-friendly error messages

### 5. Database with Relationships
- Foreign keys with CASCADE
- Indexes for performance
- Automatic timestamps
- Soft delete prepared

---

## Problems Resolved

### 1. CORS Authentication Blocking
**Problem:** Frontend couldn't authenticate due to CORS
**Solution:** Added `http://localhost:3030` to allowed origins

### 2. AuthContext Not Updating
**Problem:** Login page not updating React context
**Solution:** Migrated from `authService.login()` to `AuthContext.login()`

### 3. Unauthenticated API Calls
**Problem:** Resources/Actions pages using fetch() without authentication
**Solution:** Migrated all endpoints to use centralized `apiClient`

### 4. Next.js Cache Corruption
**Problem:** False compilation errors due to corrupted cache
**Solution:** Clear `.next/` folder and complete rebuild

---

## Project Metrics

- **Lines of Code (Backend):** ~2,500
- **Lines of Code (Frontend):** ~3,500
- **API Endpoints:** 18
- **React Components:** 12
- **Data Models:** 5
- **Development Time:** 1 intensive day

---

## Next Steps

See [ROADMAP.md](./ROADMAP.md) for planned features and future improvements.

---

**Developed with ❤️ using FastAPI + Next.js**
