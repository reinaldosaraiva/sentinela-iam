"""
Authentication API Router
Provides endpoints for user authentication
"""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
import logging
import bcrypt
from sqlalchemy.orm import Session

from database_pg import get_db
from models.user import User
from auth.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas.auth import LoginRequest, TokenResponse, UserResponse
from dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def authenticate_user_db(email: str, password: str, db: Session) -> User:
    """Authenticate user against database"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token (with Keycloak integration)
    """
    try:
        # First try Keycloak authentication
        import requests
        import os
        
        keycloak_url = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
        realm = os.getenv("KEYCLOAK_REALM", "sentinela")
        client_id = os.getenv("KEYCLOAK_CLIENT_ID", "sentinela-api")
        client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET", "sentinela-secret")
        
        # Try Keycloak authentication
        try:
            data = {
                "grant_type": "password",
                "client_id": client_id,
                "client_secret": client_secret,
                "username": credentials.email,
                "password": credentials.password
            }
            
            response = requests.post(
                f"{keycloak_url}/realms/{realm}/protocol/openid-connect/token",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=5
            )
            
            if response.status_code == 200:
                # Keycloak authentication successful
                token_data = response.json()
                
                # Get or create user in local database
                user = db.query(User).filter(User.email == credentials.email).first()
                
                if not user:
                    # Create user in local database if not exists
                    user = User(
                        email=credentials.email,
                        name=credentials.email.split("@")[0],  # Extract name from email
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
                    username=user.email.split("@")[0],
                    full_name=user.name,
                    is_active=user.status == "active",
                    is_superuser=user.role == "admin",
                    groups=[]
                )
                
                return TokenResponse(
                    access_token=access_token,
                    token_type="bearer",
                    expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    user=user_response
                )
        
        except Exception as e:
            logger.warning(f"Keycloak authentication failed: {e}")
        
        # Fallback to database authentication
        user = authenticate_user_db(credentials.email, credentials.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role},
            expires_delta=access_token_expires
        )
        
        # Prepare user response
        user_response = UserResponse(
            email=user.email,
            username=user.email.split("@")[0],  # Extract username from email
            full_name=user.name,
            is_active=user.status == "active",
            is_superuser=user.role == "admin",
            groups=[]  # TODO: Get from groups
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

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user.email,
        "email": user.email,
        "user_id": user.id,
        "role": user.role.value
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )

    logger.info(f"Successful login for user: {user.email}")

    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()

    # Prepare user response (exclude sensitive data)
    user_response = UserResponse(
        email=user.email,
        username=user.email.split('@')[0],  # Use email prefix as username
        full_name=user.name,
        is_active=user.is_active,
        is_superuser=user.role.value == 'admin',
        groups=[]  # TODO: Load from user_groups table
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        user=user_response
    )


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information

    Requires valid JWT token in Authorization header
    """
    return UserResponse(
        email=current_user.email,
        username=current_user.email.split('@')[0],
        full_name=current_user.name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_admin,
        groups=[]  # TODO: Load from user_groups table
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    """
    Logout endpoint (client-side token removal)

    Since JWT is stateless, actual logout happens on the client side
    by removing the token from storage.
    """
    return {
        "message": "Logout successful. Please remove the token from client storage."
    }
