#!/usr/bin/env python3
"""
Minimal Working Policy API
"""

from fastapi import FastAPI, HTTPException, status
import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Simple in-memory database for MVP
policies_db = []
policy_id_counter = 1

# Create FastAPI app
app = FastAPI(
    title="Sentinela Policy API",
    description="Policy Management Service for Authorization Control Plane",
    version="1.0.0"
)

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

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sentinela Policy API",
        "version": "1.0.0",
        "status": "running"
    }

# Policy endpoints
@app.get("/policies/")
async def list_policies(skip: int = 0, limit: int = 100):
    """List all policies"""
    return policies_db[skip:skip+limit]

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

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )