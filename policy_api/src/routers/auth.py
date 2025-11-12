"""
Authentication API Router
Provides endpoints for user authentication
"""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
import logging

from auth import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import LoginRequest, TokenResponse, UserResponse
from dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(credentials: LoginRequest):
    """
    Authenticate user and return JWT token

    **Credentials for testing:**
    - Admin: admin@sentinela.com / admin123
    - User: user@sentinela.com / user123
    """
    # Authenticate user
    user = authenticate_user(credentials.email, credentials.password)

    if not user:
        logger.warning(f"Failed login attempt for email: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user["email"],
        "email": user["email"],
        "username": user["username"],
        "full_name": user["full_name"],
        "is_superuser": user["is_superuser"],
        "groups": user["groups"]
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )

    logger.info(f"Successful login for user: {user['email']}")

    # Prepare user response (exclude sensitive data)
    user_response = UserResponse(
        email=user["email"],
        username=user["username"],
        full_name=user["full_name"],
        is_active=user["is_active"],
        is_superuser=user["is_superuser"],
        groups=user["groups"]
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        user=user_response
    )


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information

    Requires valid JWT token in Authorization header
    """
    return UserResponse(
        email=current_user["email"],
        username=current_user["username"],
        full_name=current_user["full_name"],
        is_active=True,
        is_superuser=current_user["is_superuser"],
        groups=current_user["groups"]
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
