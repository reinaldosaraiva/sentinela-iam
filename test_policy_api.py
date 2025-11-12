#!/usr/bin/env python3
"""
Simple test script to run Policy API
"""

import sys
import os

# Add the policy_api/src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'policy_api', 'src'))

from fastapi import FastAPI
import uvicorn

# Import the app
from main import app

if __name__ == "__main__":
    print("Starting Policy API...")
    print(f"App title: {app.title}")
    print(f"App routes: {[route.path for route in app.routes]}")
    
    # Run the app
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )