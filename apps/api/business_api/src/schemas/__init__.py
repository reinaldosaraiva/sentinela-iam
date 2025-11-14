"""
Schemas package for Business API
"""

from .auth import (
    LoginRequest,
    TokenResponse,
    UserResponse,
)

from .document import (
    DocumentBase,
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentListResponse,
)

__all__ = [
    # Auth schemas
    'LoginRequest',
    'TokenResponse',
    'UserResponse',
    # Document schemas
    'DocumentBase',
    'DocumentCreate',
    'DocumentUpdate',
    'DocumentResponse',
    'DocumentListResponse',
]