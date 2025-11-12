# Project Structure - Sentinela IAM

**Version:** v1.0.0
**Last Updated:** November 12, 2025
**Standards:** Clean Code (Robert C. Martin) + Martin Fowler principles

---

## 📋 Table of Contents
- [Current Issues](#current-issues)
- [New Structure](#new-structure)
- [Directory Explanation](#directory-explanation)
- [Migration Plan](#migration-plan)
- [Benefits](#benefits)

---

## ❌ Current Issues

### Problems with Current Structure:
- 🔴 **Root Directory Cluttered**: 60+ files in root
- 🔴 **Debug/Test Files Scattered**: test_*.py, debug_*.py everywhere
- 🔴 **Multiple Services Mixed**: business_api, policy_ui, policy_api
- 🔴 **Logs in Root**: *.log files polluting workspace
- 🔴 **Docker Files Scattered**: Dockerfiles not organized
- 🔴 **Documentation Fragmented**: Multiple README/MVP files
- 🔴 **No Clear App Boundaries**: Services mixed with tools

---

## ✅ New Structure (Monorepo - Best Practices 2025)

```
sentinela/
├── .github/                          # GitHub specific files
│   ├── workflows/                   # CI/CD workflows
│   │   ├── backend-ci.yml
│   │   ├── frontend-ci.yml
│   │   └── deploy.yml
│   └── ISSUE_TEMPLATE/              # Issue templates
│
├── apps/                            # Main applications
│   ├── api/                         # Backend FastAPI
│   │   ├── src/
│   │   │   ├── routers/
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   ├── auth/
│   │   │   ├── database_pg.py
│   │   │   └── main.py
│   │   ├── alembic/
│   │   ├── tests/
│   │   │   ├── unit/
│   │   │   ├── integration/
│   │   │   └── e2e/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   └── web/                         # Frontend Next.js
│       ├── src/
│       │   ├── app/
│       │   ├── components/
│       │   ├── contexts/
│       │   └── lib/
│       ├── public/
│       ├── tests/
│       │   ├── unit/
│       │   ├── integration/
│       │   └── e2e/
│       ├── Dockerfile
│       ├── package.json
│       ├── tsconfig.json
│       └── README.md
│
├── packages/                        # Shared code (monorepo)
│   ├── shared-types/               # TypeScript/Python types
│   │   ├── typescript/
│   │   └── python/
│   ├── utils/                      # Shared utilities
│   └── config/                     # Shared configurations
│
├── tools/                          # Development tools
│   ├── docker/                     # Docker configurations
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   ├── docker-compose.test.yml
│   │   └── README.md
│   ├── scripts/                    # Automation scripts
│   │   ├── setup/                  # Setup scripts
│   │   ├── seed/                   # Database seeding
│   │   ├── test/                   # Test helpers
│   │   └── deploy/                 # Deployment scripts
│   └── keycloak/                   # Keycloak configs
│
├── docs/                           # Documentation
│   ├── api/                        # API documentation
│   ├── architecture/               # Architecture docs
│   ├── guides/                     # How-to guides
│   └── assets/                     # Images, diagrams
│
├── tests/                          # E2E tests (cross-app)
│   ├── e2e/
│   ├── performance/
│   └── fixtures/
│
├── .archive/                       # Archived/deprecated code
│   └── old-implementations/
│
├── .temp/                          # Temporary files (gitignored)
│   ├── logs/
│   └── tokens/
│
├── .github/                        # GitHub configs
│   └── workflows/
│
├── .vscode/                        # VS Code settings (optional)
│   └── settings.json
│
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── .dockerignore                   # Docker ignore rules
├── docker-compose.yml              # Main docker compose
├── Makefile                        # Project automation
├── LICENSE                         # MIT License
├── README.md                       # Main documentation
├── ROADMAP.md                      # Product roadmap
├── IMPLEMENTATION.md               # Technical implementation
├── USER_STORIES.md                 # Feature specifications
├── CONTRIBUTING.md                 # Contribution guidelines
└── CHANGELOG.md                    # Version history
```

---

## 📁 Directory Explanation

### Root Level
**Purpose:** Only essential project files
- Configuration files (docker-compose, .env)
- Main documentation (README, ROADMAP, etc.)
- Project automation (Makefile)
- License and contribution guides

### `/apps`
**Purpose:** Deployable applications
- Each app is independently deployable
- Self-contained with own dependencies
- Has own Dockerfile and README
- Follows Single Responsibility Principle

### `/packages`
**Purpose:** Shared code across apps
- Reusable utilities
- Shared types/interfaces
- Common configurations
- Version controlled independently

### `/tools`
**Purpose:** Development tooling
- Docker configurations centralized
- Scripts organized by purpose
- Third-party service configs
- Not deployed to production

### `/docs`
**Purpose:** All documentation
- API specs (OpenAPI/Swagger)
- Architecture diagrams
- User guides
- Development docs

### `/tests`
**Purpose:** Cross-application tests
- E2E tests spanning multiple apps
- Performance/load tests
- Integration tests between services

### `/.archive`
**Purpose:** Historical code
- Deprecated implementations
- Migration artifacts
- Not actively maintained
- Kept for reference

### `/.temp`
**Purpose:** Temporary runtime files
- **Always in .gitignore**
- Logs during development
- Temporary tokens
- Build artifacts

---

## 🔄 Migration Plan

### Phase 1: Create New Structure (30 min)
```bash
# Create directory structure
mkdir -p apps/{api,web}
mkdir -p packages/{shared-types,utils,config}
mkdir -p tools/{docker,scripts,keycloak}
mkdir -p docs/{api,architecture,guides,assets}
mkdir -p tests/{e2e,performance,fixtures}
mkdir -p .archive/old-implementations
mkdir -p .temp/{logs,tokens}
```

### Phase 2: Move Applications (1 hour)
```bash
# Move backend
mv policy_api apps/api
mv test_*.py apps/api/tests/

# Move frontend
mv sentinela-ui apps/web
```

### Phase 3: Move Tools (30 min)
```bash
# Move Docker files
mv Dockerfile.* tools/docker/
mv docker-compose*.yml tools/docker/
mv docker tools/docker/configs

# Move scripts
mv scripts tools/scripts
mv setup tools/scripts/setup
```

### Phase 4: Move Documentation (20 min)
```bash
# Keep in root: README, ROADMAP, IMPLEMENTATION, USER_STORIES
# Move detailed docs
mv MVP_*.md .archive/
mv STATUS_*.md .archive/
```

### Phase 5: Archive Old Code (20 min)
```bash
# Archive deprecated code
mv *_demo.py .archive/old-implementations/
mv debug_*.py .archive/old-implementations/
mv working_*.py .archive/old-implementations/
mv minimal_*.py .archive/old-implementations/
mv test_*.py .archive/old-implementations/
```

### Phase 6: Move Temp Files (10 min)
```bash
# Move logs and tokens
mv *.log .temp/logs/
mv *_token.txt .temp/tokens/
```

### Phase 7: Update Configurations (30 min)
- Update docker-compose paths
- Update import paths in code
- Update CI/CD workflows
- Update documentation links

---

## 🎯 Benefits of New Structure

### 1. **Clean Code Principles**
- ✅ **Single Responsibility**: Each directory has one purpose
- ✅ **Open/Closed**: Easy to add new apps without changing structure
- ✅ **Dependency Inversion**: Apps depend on packages, not each other

### 2. **Developer Experience**
- 🚀 **Easy Navigation**: Logical directory structure
- 🔍 **Quick File Location**: Know where everything lives
- 📚 **Self-Documenting**: Structure explains itself
- 👥 **Team Friendly**: New developers onboard faster

### 3. **Maintainability**
- 🔧 **Isolated Changes**: Changes in one app don't affect others
- 🧪 **Testability**: Clear test organization
- 📦 **Deployability**: Each app independently deployable
- 🔄 **Scalability**: Easy to add new services

### 4. **Best Practices Compliance**
- ✅ **Martin Fowler**: Modular monolith approach
- ✅ **Clean Code**: Clear separation of concerns
- ✅ **12-Factor App**: Configuration separate from code
- ✅ **Monorepo 2025**: Modern tooling-ready structure

---

## 📝 Updated .gitignore

```gitignore
# Temporary directory (entire directory)
.temp/

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Testing
.coverage
htmlcov/
.pytest_cache/
coverage/

# Build
dist/
build/
*.egg-info/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Dependencies
node_modules/
venv/
__pycache__/
*.py[cod]

# Docker
.docker/

# Next.js
.next/
out/
```

---

## 🛠️ Development Workflow

### Starting Development
```bash
# One command to rule them all
make dev

# Or manually:
docker-compose -f tools/docker/docker-compose.dev.yml up
```

### Running Tests
```bash
# All tests
make test

# Specific tests
make test-api
make test-web
make test-e2e
```

### Deployment
```bash
# Production build
make build

# Deploy
make deploy-staging
make deploy-prod
```

---

## 📚 Additional Files to Create

### 1. `Makefile`
Centralize common commands:
```makefile
.PHONY: dev test build deploy

dev:
	docker-compose -f tools/docker/docker-compose.dev.yml up

test:
	cd apps/api && pytest
	cd apps/web && npm test

build:
	docker-compose -f tools/docker/docker-compose.yml build

deploy-staging:
	./tools/scripts/deploy/deploy-staging.sh

deploy-prod:
	./tools/scripts/deploy/deploy-prod.sh
```

### 2. `CONTRIBUTING.md`
Guidelines for contributors

### 3. `CHANGELOG.md`
Track version changes

### 4. `.github/workflows/`
CI/CD pipelines

---

## 🚀 Implementation Checklist

- [ ] Create new directory structure
- [ ] Move applications to `/apps`
- [ ] Move tools to `/tools`
- [ ] Archive old code
- [ ] Move temporary files to `.temp`
- [ ] Update `.gitignore`
- [ ] Update `docker-compose` paths
- [ ] Update import paths in code
- [ ] Create `Makefile`
- [ ] Create `CONTRIBUTING.md`
- [ ] Create `CHANGELOG.md`
- [ ] Update all documentation
- [ ] Test all functionality
- [ ] Commit and push changes

---

## 📖 References

### Clean Code & Architecture
- **Clean Code** by Robert C. Martin
- **Clean Architecture** by Robert C. Martin
- **Refactoring** by Martin Fowler
- **Patterns of Enterprise Application Architecture** by Martin Fowler

### Monorepo Best Practices
- [Monorepo Guide 2025](https://www.aviator.co/blog/monorepo-a-hands-on-guide-for-managing-repositories-and-microservices/)
- [The Ultimate Guide to Building a Monorepo in 2025](https://medium.com/@sanjaytomar717/the-ultimate-guide-to-building-a-monorepo-in-2025-sharing-code-like-the-pros-ee4d6d56abaa)
- [Martin Fowler: Monolith First](https://martinfowler.com/bliki/MonolithFirst.html)

---

**Status:** 📋 Planning Phase
**Next Step:** Execute Migration Plan
**Estimated Time:** 3-4 hours
**Risk Level:** Low (no code changes, only moves)

---

**Maintained by:** Development Team
**Last Review:** November 12, 2025
**Next Review:** After migration completion
