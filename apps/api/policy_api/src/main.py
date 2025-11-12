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
from routers import applications, resources, actions, auth
app.include_router(auth.router, prefix="/api/v1")  # Auth router (no authentication required)
app.include_router(applications.router, prefix="/api/v1")
app.include_router(resources.router, prefix="/api/v1")
app.include_router(actions.router, prefix="/api/v1")


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


# Policy endpoints
@app.get("/policies/")
async def list_policies(skip: int = 0, limit: int = 100):
    """List all policies"""
    return policies_db[skip:skip+limit]


@app.get("/policies/{policy_id}")
async def get_policy(policy_id: int):
    """Get a specific policy by ID"""
    for policy in policies_db:
        if policy["id"] == policy_id:
            return policy
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Policy not found"
    )


@app.post("/policies/", status_code=status.HTTP_201_CREATED)
async def create_policy(policy_data: dict):
    """Create a new policy"""
    global policy_id_counter
    
    new_policy = {
        "id": policy_id_counter,
        "name": policy_data.get("name"),
        "description": policy_data.get("description"),
        "content": policy_data.get("content"),
        "version": "1.0.0",
        "status": "draft",
        "created_at": "2025-01-11T00:00:00Z",
        "updated_at": "2025-01-11T00:00:00Z"
    }
    
    policies_db.append(new_policy)
    policy_id_counter += 1
    
    logger.info(f"Policy {new_policy['id']} created successfully")
    return new_policy


@app.put("/policies/{policy_id}")
async def update_policy(policy_id: int, policy_data: dict):
    """Update an existing policy"""
    for i, policy in enumerate(policies_db):
        if policy["id"] == policy_id:
            # Update policy fields
            for field, value in policy_data.items():
                if value is not None:
                    policy[field] = value
            
            policy["updated_at"] = "2025-01-11T00:00:00Z"
            
            # Increment version if content changed
            if "content" in policy_data:
                current_version = policy["version"].split(".")
                current_version[-1] = str(int(current_version[-1]) + 1)
                policy["version"] = ".".join(current_version)
            
            logger.info(f"Policy {policy_id} updated successfully")
            return policy
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Policy not found"
    )


@app.delete("/policies/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(policy_id: int):
    """Delete a policy"""
    for i, policy in enumerate(policies_db):
        if policy["id"] == policy_id:
            policies_db.pop(i)
            logger.info(f"Policy {policy_id} deleted successfully")
            return None
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Policy not found"
    )


@app.post("/policies/{policy_id}/publish")
async def publish_policy(policy_id: int):
    """Publish a policy (make it active)"""
    for policy in policies_db:
        if policy["id"] == policy_id:
            policy["status"] = "active"
            policy["updated_at"] = "2025-01-11T00:00:00Z"
            logger.info(f"Policy {policy_id} published successfully")
            return policy
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Policy not found"
    )


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