"""
Authentication Pydantic Schemas
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: "UserResponse" = Field(..., description="User information")


class UserResponse(BaseModel):
    """User response schema"""
    email: EmailStr = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="User full name")
    is_active: bool = Field(..., description="User active status")
    is_superuser: bool = Field(..., description="Superuser status")
    groups: List[str] = Field(default=[], description="User groups")

    class Config:
        from_attributes = True


class CurrentUser(BaseModel):
    """Current authenticated user schema"""
    email: EmailStr
    username: str
    full_name: str
    is_active: bool
    is_superuser: bool
    groups: List[str] = []
