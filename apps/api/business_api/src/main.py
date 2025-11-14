"""
Sentinela Business API
Business Logic Service with Authorization Control
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
keycloak_service = None
cedar_engine = None

# Simple in-memory database for MVP
documents_db = []
document_id_counter = 1


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Business API...")
    
    # Initialize services
    global keycloak_service, cedar_engine
    keycloak_service = None  # Will be implemented later
    cedar_engine = None  # Will be implemented later
    
    logger.info("Services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Business API...")


# Create FastAPI app
app = FastAPI(
    title="Sentinela Business API",
    description="Business Logic Service with Authorization Control",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - import directly to avoid package import issues
from routers.auth import router as auth_router
from routers.documents import router as documents_router
app.include_router(auth_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")


# Health endpoints
@app.get("/health/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": "2025-01-11T00:00:00Z",
        "services": {
            "keycloak": "not_initialized",
            "cedar_engine": "not_initialized"
        }
    }


@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check including external services"""
    return {
        "status": "healthy",
        "timestamp": "2025-01-11T00:00:00Z",
        "services": {
            "keycloak": "not_initialized",
            "cedar_engine": "not_initialized"
        }
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sentinela Business API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/info")
async def info():
    """API information endpoint"""
    return {
        "name": "Sentinela Business API",
        "version": "1.0.0",
        "description": "Business Logic Service with Authorization Control",
        "services": {
            "keycloak_url": "http://keycloak:8080",
            "keycloak_realm": "sentinela"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )