"""
JWT Authentication Module for Business API
Handles token generation and validation
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    Args:
        data: Dictionary with user data to encode
        expires_delta: Optional custom expiration time

    Returns:
        JWT token as string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict]:
    """
    Decode and validate a JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# Mock users database (for MVP)
# In production, this would come from Keycloak
MOCK_USERS = {
    "admin@sentinela.com": {
        "email": "admin@sentinela.com",
        "username": "admin",
        "full_name": "Administrator",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq9w5KS",  # Password: admin123
        "is_active": True,
        "is_superuser": True,
        "groups": ["admin", "developers"]
    },
    "alice@sentinela.com": {
        "email": "alice@sentinela.com",
        "username": "alice",
        "full_name": "Alice Smith",
        "hashed_password": "$2b$12$g9T/wN6Qd5xGBNHH1XjgQ.8m4JvJ5MqJqhN8/LewdBPj6hsxq9w5KS",  # Password: alice123
        "is_active": True,
        "is_superuser": False,
        "groups": ["employees"]
    },
    "bob@sentinela.com": {
        "email": "bob@sentinela.com",
        "username": "bob",
        "full_name": "Bob Johnson",
        "hashed_password": "$2b$12$hT8k9wN6Qd5xGBNHH1XjgQ.8m4JvJ5MqJqhN8/LewdBPj6hsxq9w5KS",  # Password: bob123
        "is_active": True,
        "is_superuser": False,
        "groups": ["managers", "employees"]
    }
}


def authenticate_user(email: str, password: str) -> Optional[Dict]:
    """
    Authenticate a user with email and password

    Args:
        email: User email
        password: Plain text password

    Returns:
        User data dictionary or None if authentication fails
    """
    user = MOCK_USERS.get(email)
    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    if not user["is_active"]:
        return None

    return user


def get_user_by_email(email: str) -> Optional[Dict]:
    """
    Get user data by email

    Args:
        email: User email

    Returns:
        User data dictionary or None if not found
    """
    return MOCK_USERS.get(email)