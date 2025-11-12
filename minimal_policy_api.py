#!/usr/bin/env python3
"""
Minimal Policy API for testing
"""

from fastapi import FastAPI
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Sentinela Policy API",
    description="Policy Management Service for Authorization Control Plane",
    version="1.0.0"
)

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

if __name__ == "__main__":
    print("Starting Minimal Policy API...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )