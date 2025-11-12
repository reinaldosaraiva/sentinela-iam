from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, Optional
import jwt
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)


async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    """Extract and validate user from JWT token"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # For MVP, we'll decode without verification (in production, verify with Keycloak public key)
        payload = jwt.decode(credentials.credentials, options={"verify_signature": False})
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Extract user info
        user_info = {
            "user_id": user_id,
            "email": payload.get("email", ""),
            "name": payload.get("name", ""),
            "roles": payload.get("realm_access", {}).get("roles", []),
            "department": payload.get("department", "general"),
            "clearance_level": payload.get("clearance_level", "confidential")
        }
        
        logger.info(f"User authenticated: {user_id}")
        return user_info
        
    except jwt.PyJWTError as e:
        logger.error(f"Token validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user_from_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    """Alternative function to get user from token"""
    return await get_current_user(credentials)