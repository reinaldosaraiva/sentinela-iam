"""
Keycloak Authentication Router
Provides endpoints for user authentication using Keycloak
"""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
import logging
import os
from sqlalchemy.orm import Session

from database_pg import get_db
from models.user import User
from auth.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas.auth import LoginRequest, TokenResponse, UserResponse
from services.keycloak_service import KeycloakService
from dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Initialize Keycloak service
keycloak_service = KeycloakService(
    server_url=os.getenv("KEYCLOAK_URL", "http://localhost:8080"),
    realm=os.getenv("KEYCLOAK_REALM", "sentinela")
)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with Keycloak and return JWT token
    """
    try:
        # Authenticate with Keycloak
        keycloak_auth = await keycloak_service.authenticate_user(
            username=credentials.email,
            password=credentials.password
        )
        
        if not keycloak_auth:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get or create user in local database
        user = db.query(User).filter(User.email == credentials.email).first()
        
        if not user:
            # Create user in local database if not exists
            user = User(
                email=keycloak_auth["user"]["email"],
                name=keycloak_auth["user"].get("name", ""),
                status="active",
                role="user"  # Default role
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create our own JWT token for API access
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role},
            expires_delta=access_token_expires
        )
        
        # Prepare user response
        user_response = UserResponse(
            email=user.email,
            username=keycloak_auth["user"].get("username", user.email.split("@")[0]),
            full_name=user.name,
            is_active=user.status == "active",
            is_superuser=user.role == "admin",
            groups=[]  # TODO: Get from Keycloak groups
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        )


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information
    """
    try:
        return UserResponse(
            email=current_user.email,
            username=current_user.email.split("@")[0],
            full_name=current_user.name,
            is_active=current_user.is_active,  # Use property that handles enum
            is_superuser=current_user.is_admin,  # Use property that handles enum
            groups=[]  # TODO: Get from Keycloak groups
        )
        
    except Exception as e:
        logger.error(f"Get current user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error getting user information"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout user
    """
    try:
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout"
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def auth_health():
    """
    Health check for authentication service
    """
    try:
        # Check Keycloak availability
        keycloak_healthy = await keycloak_service.health_check()
        
        return {
            "status": "healthy" if keycloak_healthy else "degraded",
            "keycloak": "connected" if keycloak_healthy else "disconnected",
            "timestamp": "2025-11-13T13:52:00Z"
        }
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "keycloak": "error",
            "error": str(e)
        }