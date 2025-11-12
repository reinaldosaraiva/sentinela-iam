"""
Keycloak Service for JWT validation
"""

import jwt
import httpx
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class KeycloakService:
    """Service for validating JWT tokens from Keycloak"""
    
    def __init__(self, server_url: str, realm: str):
        self.server_url = server_url.rstrip('/')
        self.realm = realm
        self.client = httpx.AsyncClient(timeout=30.0)
        self.public_key_cache = None
        self.public_key_expires = None
    
    async def health_check(self) -> bool:
        """Check if Keycloak server is healthy"""
        try:
            response = await self.client.get(f"{self.server_url}/health/ready")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Keycloak health check failed: {e}")
            return False
    
    async def get_public_key(self) -> Optional[str]:
        """Get realm public key for JWT validation"""
        # Check cache first
        if (self.public_key_cache and 
            self.public_key_expires and 
            datetime.utcnow() < self.public_key_expires):
            return self.public_key_cache
        
        try:
            response = await self.client.get(
                f"{self.server_url}/realms/{self.realm}/protocol/openid-connect/certs"
            )
            
            if response.status_code == 200:
                certs = response.json()
                # Get first RSA key
                for key in certs.get("keys", []):
                    if key.get("kty") == "RSA":
                        # For MVP, we'll use a simplified approach
                        # In production, proper key conversion needed
                        self.public_key_cache = "mock-public-key"
                        self.public_key_expires = datetime.utcnow() + timedelta(hours=1)
                        return self.public_key_cache
                
                logger.error("No RSA key found in certs")
                return None
            else:
                logger.error(f"Failed to get public key: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting public key: {e}")
            return None
    
    async def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT token and return payload"""
        try:
            # For MVP, implement simple validation
            # In production, this would use proper JWT validation
            
            # Check if it's our mock token
            if token == "mock-token":
                return {
                    "sub": "alice-user-id",
                    "email": "alice@example.com",
                    "groups": ["employees"],
                    "name": "Alice Smith",
                    "preferred_username": "alice",
                    "iss": f"{self.server_url}/realms/{self.realm}",
                    "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp())
                }
            
            # Try to decode without verification for MVP
            try:
                payload = jwt.decode(
                    token,
                    options={"verify_signature": False},
                    algorithms=["RS256"]
                )
                
                # Check if token is for correct realm
                if payload.get("iss") != f"{self.server_url}/realms/{self.realm}":
                    logger.error("Invalid token issuer")
                    return None
                
                # Check expiration
                if payload.get("exp", 0) < datetime.utcnow().timestamp():
                    logger.error("Token expired")
                    return None
                
                return payload
                
            except jwt.ExpiredSignatureError:
                logger.error("Token has expired")
                return None
            except jwt.InvalidTokenError as e:
                logger.error(f"Invalid token: {e}")
                return None
            
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return None
    
    async def get_user_info(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user information from Keycloak"""
        try:
            response = await self.client.get(
                f"{self.server_url}/realms/{self.realm}/protocol/openid-connect/userinfo",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get user info: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()