"""
Schemas package for Policy API
"""

from .application import (
    ApplicationBase,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationListResponse
)

from .api_key import (
    APIKeyBase,
    APIKeyCreate,
    APIKeyCreateResponse,
    APIKeyResponse,
    APIKeyUpdate,
    APIKeyListResponse
)

from .resource import (
    ResourceBase,
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse,
    ResourceListResponse
)

from .action import (
    ActionBase,
    ActionCreate,
    ActionUpdate,
    ActionResponse,
    ActionListResponse
)

from .auth import (
    LoginRequest,
    TokenResponse,
    UserResponse,
    CurrentUser
)

__all__ = [
    # Application schemas
    'ApplicationBase',
    'ApplicationCreate',
    'ApplicationUpdate',
    'ApplicationResponse',
    'ApplicationListResponse',
    # APIKey schemas
    'APIKeyBase',
    'APIKeyCreate',
    'APIKeyCreateResponse',
    'APIKeyResponse',
    'APIKeyUpdate',
    'APIKeyListResponse',
    # Resource schemas
    'ResourceBase',
    'ResourceCreate',
    'ResourceUpdate',
    'ResourceResponse',
    'ResourceListResponse',
    # Action schemas
    'ActionBase',
    'ActionCreate',
    'ActionUpdate',
    'ActionResponse',
    'ActionListResponse',
    # Auth schemas
    'LoginRequest',
    'TokenResponse',
    'UserResponse',
    'CurrentUser',
]
