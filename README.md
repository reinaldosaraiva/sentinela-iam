# Sentinela - Identity and Access Management Platform

<div align="center">

![Sentinela Logo](https://via.placeholder.com/150x150/4F46E5/FFFFFF?text=Sentinela)

**Modern identity management and access control platform**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.0-000000?style=flat&logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192?style=flat&logo=postgresql)](https://www.postgresql.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[Features](#features) •
[Demo](#demo) •
[Installation](#installation) •
[Documentation](#documentation) •
[Contributing](#contributing)

</div>

---

## About the Project

**Sentinela** is a complete IAM (Identity and Access Management) platform developed with modern technologies, offering centralized management of applications, resources, and access permissions.

### Why Sentinela?

- 🔐 **Security First**: Robust JWT authentication and password encryption
- 🚀 **Performance**: Asynchronous backend with FastAPI and optimized frontend with Next.js 14
- 📱 **Responsive**: Modern interface that works on all devices
- 🔧 **Extensible**: Modular architecture and well-documented RESTful APIs
- 🎯 **Easy to Use**: Intuitive interface for permission management

---

## Features

### Application Management
- ✅ Complete application registration
- ✅ Environment control (production, staging, development)
- ✅ Logo upload and visual information
- ✅ Status management (active, paused, inactive)
- ✅ Advanced search and filters

### Resource Management
- ✅ Resource definition per application
- ✅ Custom resource typing
- ✅ Linking with multiple actions
- ✅ Real-time action counters
- ✅ Safe cascade deletion

### Action Management
- ✅ Complete action CRUD
- ✅ Predefined types (read, write, update, delete, etc.)
- ✅ Dynamic activation/deactivation
- ✅ Filters by resource and status
- ✅ Colored grid visualization

### Authentication and Security
- ✅ Login with JWT tokens
- ✅ Automatic refresh token
- ✅ Frontend route protection
- ✅ Backend authentication middleware
- ✅ Password hashing with bcrypt
- ✅ Configured CORS

### Administrative Interface
- ✅ Dashboard with real-time metrics
- ✅ Responsive and modern layout
- ✅ Intuitive navigation with sidebar
- ✅ Visual themes (dark mode ready)
- ✅ Reusable components

### RESTful API
- ✅ 18 documented endpoints
- ✅ Integrated Swagger UI
- ✅ Automatic pagination
- ✅ Data validation with Pydantic
- ✅ Standardized error handling

---

## Technologies

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern and fast web framework
- **[PostgreSQL](https://www.postgresql.org/)** - Robust relational database
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Powerful Python ORM
- **[Alembic](https://alembic.sqlalchemy.org/)** - Migration management
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation
- **[python-jose](https://github.com/mpdavis/python-jose)** - JWT tokens
- **[passlib](https://passlib.readthedocs.io/)** - Password hashing

### Frontend
- **[Next.js 14](https://nextjs.org/)** - React framework with App Router
- **[TypeScript](https://www.typescriptlang.org/)** - Static typing
- **[TailwindCSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Lucide React](https://lucide.dev/)** - Modern icon library
- **[React Context API](https://react.dev/reference/react/useContext)** - State management

---

## Installation

### Prerequisites

- **Python** 3.11 or higher
- **Node.js** 18 or higher
- **PostgreSQL** 14 or higher
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/reinaldosaraiva/sentinela-iam.git
cd sentinela
```

### 2. Configure the Backend

```bash
# Enter the backend folder
cd policy_api

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
alembic upgrade head

# (Optional) Populate database with sample data
python seed_data.py

# Start the server
python -m uvicorn policy_api.src.main:app --port 8001 --reload
```

### 3. Configure the Frontend

```bash
# In another terminal, enter the frontend folder
cd sentinela-ui

# Install dependencies
npm install

# Start the development server
PORT=3030 npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:3030
- **Backend API**: http://localhost:8001
- **Swagger Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Demo Credentials
```
Email: admin@sentinela.com
Password: admin123
```

---

## Documentation

### Project Structure

```
sentinela/
├── policy_api/                 # FastAPI Backend
│   ├── src/
│   │   ├── routers/           # API Endpoints
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── database_pg.py     # Database configuration
│   │   └── main.py            # Main application
│   ├── alembic/               # Database migrations
│   ├── seed_data.py           # Seed script
│   └── requirements.txt       # Python dependencies
│
├── sentinela-ui/              # Next.js Frontend
│   ├── src/
│   │   ├── app/               # Pages (App Router)
│   │   ├── components/        # React components
│   │   ├── contexts/          # React Contexts
│   │   └── lib/               # Utilities
│   ├── public/                # Static files
│   └── package.json           # Node dependencies
│
├── docs/                      # Additional documentation
├── IMPLEMENTATION.md          # Implementation documentation
├── ROADMAP.md                 # Next steps
└── README.md                  # This file
```

### Detailed Documentation

- **[Complete Implementation](./IMPLEMENTATION.md)** - Technical details and architecture
- **[Roadmap](./ROADMAP.md)** - Future features and planned improvements
- **[API Reference](http://localhost:8001/docs)** - Interactive API documentation

---

## API Endpoints

### Authentication
```
POST   /api/v1/auth/login       - User login
GET    /api/v1/auth/me          - Current user data
POST   /api/v1/auth/logout      - Logout
```

### Applications
```
GET    /api/v1/applications/           - List applications
POST   /api/v1/applications/           - Create application
GET    /api/v1/applications/{id}       - Application details
PUT    /api/v1/applications/{id}       - Update application
DELETE /api/v1/applications/{id}       - Delete application
```

### Resources
```
GET    /api/v1/resources/              - List resources
POST   /api/v1/resources/              - Create resource
GET    /api/v1/resources/{id}          - Resource details
PUT    /api/v1/resources/{id}          - Update resource
DELETE /api/v1/resources/{id}          - Delete resource
```

### Actions
```
GET    /api/v1/actions/                - List actions
POST   /api/v1/actions/                - Create action
GET    /api/v1/actions/{id}            - Action details
PUT    /api/v1/actions/{id}            - Update action
DELETE /api/v1/actions/{id}            - Delete action
PATCH  /api/v1/actions/{id}/activate   - Activate action
PATCH  /api/v1/actions/{id}/deactivate - Deactivate action
```

---

## Contributing

Contributions are always welcome! Follow these steps:

1. **Fork the project**
2. **Create a branch for your feature** (`git checkout -b feature/MyFeature`)
3. **Commit your changes** (`git commit -m 'Add MyFeature'`)
4. **Push to the branch** (`git push origin feature/MyFeature`)
5. **Open a Pull Request**

### Contribution Guide

- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass
- Write clear and descriptive commit messages

---

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for planned features and future improvements.

### Next Features (v2.0)

- [ ] User and Group Management
- [ ] Policy System (RBAC/ABAC)
- [ ] Activity Audit and Logs
- [ ] Real-time Notifications
- [ ] Dashboard with Interactive Charts
- [ ] Report Export
- [ ] OAuth Provider Integration (Google, GitHub, etc.)
- [ ] Multi-tenancy
- [ ] API Rate Limiting
- [ ] E2E Tests with Playwright

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact and Support

- **Documentation**: [docs](./docs)
- **Issues**: [GitHub Issues](https://github.com/reinaldosaraiva/sentinela-iam/issues)
- **Discussions**: [GitHub Discussions](https://github.com/reinaldosaraiva/sentinela-iam/discussions)

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Amazing web framework
- [Next.js](https://nextjs.org/) - Modern React framework
- [TailwindCSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Lucide](https://lucide.dev/) - Beautiful and consistent icons

---

<div align="center">

**Developed with ❤️ using FastAPI + Next.js**

⭐ If this project was helpful, consider giving it a star on GitHub!

</div>
