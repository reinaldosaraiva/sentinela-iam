"""
Health check router
"""

import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import asyncio

import database

router = APIRouter()


@router.get("/")
async def health_check(db: Session = Depends(database.get_db)):
    """Basic health check"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": db_status
        }
    }


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(database.get_db)):
    """Detailed health check including external services"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    # Check database
    try:
        db.execute(text("SELECT 1"))
        health_status["services"]["database"] = "healthy"
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check OPAL service
    health_status["services"]["opal"] = "not_initialized"
    
    # Check Keycloak service
    health_status["services"]["keycloak"] = "not_initialized"
    
    return health_status