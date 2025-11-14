"""
Sentinela Policy API
Policy Management Service for Authorization Control Plane
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global services
opal_service = None
keycloak_service = None

# Simple in-memory database for MVP
policies_db = []
policy_id_counter = 1


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Policy API...")
    
    # Initialize services (mock for MVP)
    global opal_service, keycloak_service
    opal_service = None  # Will be implemented later
    keycloak_service = None  # Will be implemented later
    
    logger.info("Services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Policy API...")


# Create FastAPI app
app = FastAPI(
    title="Sentinela Policy API",
    description="Policy Management Service for Authorization Control Plane",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3030",  # Frontend Next.js
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from routers import applications, resources, actions
try:
    from routers import auth_keycloak
    app.include_router(auth_keycloak.router, prefix="/api/v1")  # Keycloak auth router
    print("Keycloak auth router included successfully")
except Exception as e:
    print(f"Failed to include Keycloak auth router: {e}")
    # Fallback to regular auth
    from routers import auth
    app.include_router(auth.router, prefix="/api/v1")  # Regular auth router
app.include_router(applications.router, prefix="/api/v1")
app.include_router(resources.router, prefix="/api/v1")
app.include_router(actions.router, prefix="/api/v1")

# Include user router
try:
    from routers import users
    app.include_router(users.router)  # User router already has prefix
    print("User router included successfully")
except Exception as e:
    print(f"Failed to include user router: {e}")

# Include group router
try:
    from routers import groups
    app.include_router(groups.router)  # Group router already has prefix
    print("Group router included successfully")
except Exception as e:
    print(f"Failed to include group router: {e}")

# Include policies router
try:
    from routers import policies
    app.include_router(policies.router)  # Policies router already has prefix
    print("Policies router included successfully")
except Exception as e:
    print(f"Failed to include policies router: {e}")

# Include Keycloak user management router
try:
    from routers import keycloak_users
    app.include_router(keycloak_users.router)  # Keycloak users router
    print("Keycloak users router included successfully")
except Exception as e:
    print(f"Failed to include Keycloak users router: {e}")

# Include Keycloak group management router
try:
    from routers import keycloak_groups
    app.include_router(keycloak_groups.router)  # Keycloak groups router
    print("Keycloak groups router included successfully")
except Exception as e:
    print(f"Failed to include Keycloak groups router: {e}")


# Health endpoints
@app.get("/health/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": "2025-01-11T00:00:00Z",
        "services": {
            "database": "healthy",
            "opal": "not_initialized",
            "keycloak": "not_initialized"
        }
    }


@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check including external services"""
    return {
        "status": "healthy",
        "timestamp": "2025-01-11T00:00:00Z",
        "services": {
            "database": "healthy",
            "opal": "not_initialized",
            "keycloak": "not_initialized"
        }
    }


# Policy endpoints are now handled by the policies router


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sentinela Policy API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/info")
async def info():
    """API information endpoint"""
    return {
        "name": "Sentinela Policy API",
        "version": "1.0.0",
        "description": "Policy Management Service for Authorization Control Plane",
        "services": {
            "opal_server": "http://opal_publisher:7002",
            "keycloak_url": "http://keycloak:8080",
            "keycloak_realm": "my-app"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )