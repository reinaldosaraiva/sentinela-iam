"""
Sentinela Business API Service
Example Business Service with Authorization (Data Plane)
"""

import sys
import os

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer(auto_error=False)

# Import services properly
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from services.opal_client import OPALClient
from services.cedar_engine import CedarEngine
from services.keycloak_service import KeycloakService

# Global services
opal_client = None
cedar_engine = None
keycloak_service = None

# In-memory database for MVP
documents_db = []
document_id_counter = 1
current_policies = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Business API Service...")
    
    # Initialize services
    global opal_client, cedar_engine, keycloak_service
    opal_client = OPALClient(
        server_url="http://opal_publisher:7002",
        auth_token="super-secret-token"
    )
    cedar_engine = CedarEngine()
    keycloak_service = KeycloakService(
        server_url="http://keycloak:8080",
        realm="my-app"
    )
    
    # Load sample policies into Cedar engine
    sample_policies = [
        """
        permit(
          principal,
          action == Action::"read",
          resource_type == "Document"
        );
        """
    ]
    cedar_engine.load_policies(sample_policies)
    
    logger.info("Services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Business API Service...")
    if opal_client:
        await opal_client.close()
    if keycloak_service:
        await keycloak_service.close()


# Create FastAPI app
app = FastAPI(
    title="Sentinela Business API Service",
    description="Example Business Service with Authorization",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current user from JWT token"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # For MVP, mock token validation
        # In production, this will validate with Keycloak
        if credentials.credentials == "mock-token":
            return {
                "sub": "alice-user-id",
                "email": "alice@example.com",
                "groups": ["employees"],
                "name": "Alice Smith"
            }
        else:
            # Try to decode as JWT (mock)
            return {
                "sub": "user-from-token",
                "email": "user@example.com",
                "groups": ["employees"],
                "name": "User"
            }
    except Exception as e:
        logger.error(f"Token validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_authorization(user: dict, action: str, resource: dict) -> bool:
    """Check authorization using Cedar policies"""
    try:
        # Mock Cedar evaluation for MVP
        # In production, this will use actual Cedar engine
        
        principal = f'User::"{user["sub"]}"'
        action_enum = f'Action::"{action}"'
        resource_type = resource.get("type", "Unknown")
        resource_id = resource.get("id", "unknown")
        resource_entity = f'{resource_type}::"{resource_id}"'
        
        context = {
            "groups": user.get("groups", [])
        }
        
        logger.info(f"Authorization check: {principal} {action_enum} {resource_entity} with context {context}")
        
        # Simple mock logic: allow read for employees, deny everything else
        if action == "read" and "employees" in user.get("groups", []):
            logger.info("Authorization: ALLOW (mock logic)")
            return True
        elif action == "read":
            logger.info("Authorization: DENY (not in employees group)")
            return False
        else:
            logger.info("Authorization: DENY (action not allowed)")
            return False
            
    except Exception as e:
        logger.error(f"Authorization check failed: {e}")
        return False


# Health endpoints
@app.get("/health/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": "2025-01-11T00:00:00Z",
        "services": {
            "opal_client": "not_initialized",
            "cedar_engine": "not_initialized",
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
            "opal_client": "not_initialized",
            "cedar_engine": "not_initialized",
            "keycloak": "not_initialized"
        },
        "policies_loaded": len(current_policies)
    }


# Document endpoints
@app.get("/documentos/")
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """List all documents (requires read authorization)"""
    # Check authorization for listing documents
    resource = {"type": "Document", "id": "list"}
    if not check_authorization(current_user, "read", resource):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return documents_db[skip:skip+limit]


@app.get("/documentos/{document_id}")
async def get_document(
    document_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific document (requires read authorization)"""
    # Check authorization
    resource = {"type": "Document", "id": str(document_id)}
    if not check_authorization(current_user, "read", resource):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    for document in documents_db:
        if document["id"] == document_id:
            return document
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found"
    )


@app.post("/documentos/", status_code=status.HTTP_201_CREATED)
async def create_document(
    document_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Create a new document (requires create authorization)"""
    # Check authorization
    resource = {"type": "Document", "id": "new"}
    if not check_authorization(current_user, "create", resource):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    global document_id_counter
    
    new_document = {
        "id": document_id_counter,
        "title": document_data.get("title"),
        "content": document_data.get("content"),
        "author": current_user.get("sub"),
        "created_at": "2025-01-11T00:00:00Z",
        "updated_at": "2025-01-11T00:00:00Z"
    }
    
    documents_db.append(new_document)
    document_id_counter += 1
    
    logger.info(f"Document {new_document['id']} created by {current_user.get('sub')}")
    return new_document


@app.put("/documentos/{document_id}")
async def update_document(
    document_id: int,
    document_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Update a document (requires update authorization)"""
    # Check authorization
    resource = {"type": "Document", "id": str(document_id)}
    if not check_authorization(current_user, "update", resource):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    for document in documents_db:
        if document["id"] == document_id:
            # Update document fields
            for field, value in document_data.items():
                if value is not None:
                    document[field] = value
            
            document["updated_at"] = "2025-01-11T00:00:00Z"
            
            logger.info(f"Document {document_id} updated by {current_user.get('sub')}")
            return document
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found"
    )


@app.delete("/documentos/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete a document (requires delete authorization)"""
    # Check authorization
    resource = {"type": "Document", "id": str(document_id)}
    if not check_authorization(current_user, "delete", resource):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    for i, document in enumerate(documents_db):
        if document["id"] == document_id:
            documents_db.pop(i)
            logger.info(f"Document {document_id} deleted by {current_user.get('sub')}")
            return None
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found"
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sentinela Business API Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/info")
async def info():
    """API information endpoint"""
    return {
        "name": "Sentinela Business API Service",
        "version": "1.0.0",
        "description": "Example Business Service with Authorization",
        "services": {
            "opal_server": "http://opal_publisher:7002",
            "keycloak_url": "http://keycloak:8080",
            "keycloak_realm": "my-app"
        },
        "policies_loaded": len(current_policies)
    }


# Add some sample documents
documents_db = [
    {
        "id": 1,
        "title": "Relatório Trimestral",
        "content": "Conteúdo do relatório Q1 2025...",
        "author": "admin",
        "created_at": "2025-01-11T00:00:00Z",
        "updated_at": "2025-01-11T00:00:00Z"
    },
    {
        "id": 2,
        "title": "Política de Segurança",
        "content": "Documento de políticas de segurança...",
        "author": "admin",
        "created_at": "2025-01-11T00:00:00Z",
        "updated_at": "2025-01-11T00:00:00Z"
    }
]
document_id_counter = 3


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )