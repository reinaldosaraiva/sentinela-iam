# Changelog - Sentinela IAM

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2025-11-14

### 🎉 Major Release: Epic 1 & 2 Implementation

This release implements **Epic 1 (User and Group Management)** and **Epic 2 (UX Improvements)** from USER_STORIES.md.

---

### ✨ Added

#### Backend - User Management (Epic 1.1)
- **User Model** with status (ACTIVE/INACTIVE/BLOCKED) and role (ADMIN/USER/VIEWER) enums
- **Group Model** with hierarchical support (parent/child relationships)
- **UserGroup association** table for many-to-many relationships
- **Keycloak Admin Service** with 23 methods for complete user/group management
- **Keycloak authentication** router with JWT token generation
- **User CRUD endpoints**: `/api/v1/keycloak/users/` (list, get, create, update, delete)
- **Group CRUD endpoints**: `/api/v1/keycloak/groups/` (list, get, create, update, delete)
- **Password reset** endpoint: `/api/v1/keycloak/users/{id}/reset-password`
- **User statistics** endpoint: `/api/v1/keycloak/users/stats/summary`
- **Group statistics** endpoint: `/api/v1/keycloak/groups/stats/summary`
- **Member management**: Add/remove users from groups
- **Alembic migrations** for all database tables
- Token caching for Keycloak Admin API (improved performance)

#### Frontend - UX Improvements (Epic 2)
- **Toast Notifications** (Epic 2.1) ✅
  - react-hot-toast integration
  - 4 types: success, error, warning, info
  - Auto-dismiss, stackable, smooth animations
  - Replaced all `alert()` calls

- **Loading States** (Epic 2.2) ✅
  - Skeleton loaders for initial page load
  - Spinner for form submissions
  - Button disabled states during operations
  - Loading states for tables and cards

- **Modern Confirmations** (Epic 2.3) ✅
  - ConfirmationModal component
  - Replaced all `confirm()` calls
  - Keyboard navigation (Enter/Escape)
  - Click outside to cancel
  - Smooth animations

#### Frontend - User Management (Epic 1.1)
- **Complete UserManagement.tsx** implementation
  - 100% Keycloak integration (removed ALL mock data)
  - Create, edit, delete user operations
  - Real-time search and filtering
  - Pagination with stats cards
  - Confirmation modals for destructive actions
  - Toast notifications for all operations
  - Loading states during API calls

- **Keycloak API Client** (`keycloak-api.ts`)
  - TypeScript interfaces for all entities
  - 15+ methods for user/group operations
  - Query parameter support
  - Token persistence from localStorage

- **API Client improvements** (`api.ts`)
  - Query parameter support
  - Token refresh on every request
  - Proper error handling
  - TypeScript types

---

### 🔧 Fixed

#### Backend
- **Authentication dependencies** - Proper token validation without bypass
- **Enum values** - Fixed User status/role to use UPPERCASE (PostgreSQL constraint)
- **Keycloak count parsing** - Support for newer Keycloak JSON responses
- **Token refresh** - Fixed token persistence across page reloads

#### Frontend
- **URL construction** - Removed duplicate BASE_URL in API calls
- **Token management** - apiClient now reads from localStorage on initialization
- **Authentication flow** - Fixed refresh behavior
- **Enum comparisons** - Use model properties instead of string comparison

---

### 📝 Changed

#### Backend
- Updated all router registrations in `main.py`
- Improved error handling for router imports
- Enhanced logging for authentication flow

#### Frontend
- Replaced all `alert()` with toast notifications
- Replaced all `confirm()` with ConfirmationModal
- Updated all pages with new UX patterns
- Improved TypeScript typing throughout

---

### 🔐 Security

- Maintained authentication requirement on ALL endpoints (no bypass)
- Proper JWT token validation
- Token expiration handling
- Secure password reset flow

---

### 📊 Implementation Status

#### ✅ Epic 2: UX Improvements - **100% COMPLETE**
- [x] User Story 2.1: Toast Notifications
- [x] User Story 2.2: Loading States
- [x] User Story 2.3: Modern Confirmations

#### 🟡 Epic 1: User and Group Management - **55% COMPLETE**

**User Story 1.1: User CRUD Operations - 70% Complete**
- [x] Backend CRUD endpoints
- [x] Frontend user list
- [x] Create user modal
- [x] Edit user modal
- [x] Delete with confirmation
- [x] Search and filtering
- [x] Pagination
- [x] Stats cards
- [ ] Photo upload (pending)

**User Story 1.2: Group CRUD Operations - 40% Complete**
- [x] Backend CRUD endpoints
- [ ] Frontend group list (pending)
- [ ] Create group modal (pending)
- [ ] Edit group modal (pending)
- [ ] Delete with confirmation (pending)
- [ ] Group hierarchy tree (pending)

**User Story 1.3: User-Group Association - 50% Complete**
- [x] Backend endpoints (add/remove members)
- [ ] Frontend member management UI (pending)
- [ ] Batch operations (pending)

#### ❌ Epic 3: Advanced Filters - **0% COMPLETE**
- [ ] Multi-filter support
- [ ] Date range filters
- [ ] URL parameter persistence
- [ ] Filter presets

---

### 🎯 Next Steps

1. **High Priority** (Week 2)
   - Complete Groups page (frontend)
   - Implement User-Group association UI
   - Add batch operations

2. **Medium Priority** (Week 3)
   - Photo upload functionality
   - Group hierarchy tree view
   - Advanced filters

---

### 🐛 Known Issues

None at this time.

---

### 💻 Technical Details

#### Dependencies Added
```json
{
  "dependencies": {
    "react-hot-toast": "^2.4.1"
  }
}
```

#### Database Changes
- Added `users` table with status/role enums
- Added `groups` table with parent_id for hierarchy
- Added `user_groups` junction table
- Updated existing tables with proper constraints

#### API Endpoints Added
- 15+ Keycloak user management endpoints
- 10+ Keycloak group management endpoints
- Authentication endpoints with JWT
- Statistics endpoints

---

### 📚 Documentation

- Updated USER_STORIES.md with implementation status
- Added comprehensive commit messages
- Documented all new API endpoints
- Added TypeScript interfaces for all entities

---

### 🙏 Contributors

- Implementation: Claude Code + User collaboration
- Architecture: Based on USER_STORIES.md specifications
- Testing: Manual testing with Keycloak integration

---

## [1.1.0] - 2025-11-12

### Added
- Professional project structure reorganization
- Comprehensive User Stories with flow diagrams
- Documentation translated to English

---

## [1.0.0] - 2025-11-12

### Added
- Initial commit - Sentinela IAM Platform
- Basic project structure
- Docker setup
- Keycloak integration

---

[Unreleased]: https://github.com/yourusername/sentinela/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/yourusername/sentinela/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/yourusername/sentinela/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/yourusername/sentinela/releases/tag/v1.0.0
