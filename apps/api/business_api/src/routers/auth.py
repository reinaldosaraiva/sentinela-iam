"""
Authentication API Router for Business API
Provides endpoints for user authentication
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta, datetime
import logging
from typing import Optional
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr, Field

# Mock users database (same as in jwt.py)
MOCK_USERS = {
    "admin@sentinela.com": {
        "email": "admin@sentinela.com",
        "username": "admin",
        "full_name": "Administrator",
        "hashed_password": "$2b$12$yjTfQPpdisLuQcs0uny2hO1bXo9DecmZjZqU67zpJIdd/o0sQBwDW",  # Password: admin123
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

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Schemas
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")

class UserResponse(BaseModel):
    email: EmailStr = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="User full name")
    is_active: bool = Field(..., description="User active status")
    is_superuser: bool = Field(..., description="Superuser status")
    groups: list[str] = Field(default=[], description="User groups")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: UserResponse = Field(..., description="User information")

logger = logging.getLogger(__name__)

security = HTTPBearer()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticate a user with email and password"""
    user = MOCK_USERS.get(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    if not user["is_active"]:
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
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

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[dict]:
    """Extract and validate JWT token from Authorization header"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        
        user = MOCK_USERS.get(email)
        if user is None:
            return None
            
        return user
    except JWTError:
        return None

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(credentials: LoginRequest):
    """
    Authenticate user and return JWT token

    **Credentials for testing:**
    - Admin: admin@sentinela.com / admin123
    - Alice: alice@sentinela.com / alice123
    - Bob: bob@sentinela.com / bob123
    """
    user = authenticate_user(credentials.email, credentials.password)

    if not user:
        logger.warning(f"Failed login attempt for email: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user_response
    )

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_me(current_user: Optional[dict] = Depends(get_current_user)):
    """
    Get current authenticated user information

    Requires valid JWT token in Authorization header
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return UserResponse(
        email=current_user["email"],
        username=current_user["username"],
        full_name=current_user["full_name"],
        is_active=current_user["is_active"],
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