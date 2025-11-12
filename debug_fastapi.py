#!/usr/bin/env python3
"""
Debug FastAPI middleware issue
"""

from fastapi import FastAPI
import uvicorn

# Test 1: Minimal app
app1 = FastAPI(title="Test App 1")

@app1.get("/")
async def root1():
    return {"message": "Test 1 working"}

# Test 2: App with basic middleware
app2 = FastAPI(title="Test App 2")

from fastapi.middleware.cors import CORSMiddleware
app2.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app2.get("/")
async def root2():
    return {"message": "Test 2 working"}

# Test 3: App with lifespan
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")

app3 = FastAPI(title="Test App 3", lifespan=lifespan)

@app3.get("/")
async def root3():
    return {"message": "Test 3 working"}

if __name__ == "__main__":
    import sys
    
    test_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    if test_num == 1:
        print("Testing minimal app...")
        uvicorn.run(app1, host="0.0.0.0", port=8000)
    elif test_num == 2:
        print("Testing app with CORS...")
        uvicorn.run(app2, host="0.0.0.0", port=8000)
    elif test_num == 3:
        print("Testing app with lifespan...")
        uvicorn.run(app3, host="0.0.0.0", port=8000)