"""
Keycloak Admin API Service
Complete service for managing users and groups via Keycloak Admin REST API
"""

import httpx
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class KeycloakAdminService:
    """Service for Keycloak Admin REST API operations"""

    def __init__(self, server_url: str, realm: str, client_id: str, client_secret: str, admin_username: str = "admin", admin_password: str = "admin123"):
        self.server_url = server_url.rstrip('/')
        self.realm = realm
        self.client_id = client_id
        self.client_secret = client_secret
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.client = httpx.AsyncClient(timeout=30.0)
        self.admin_token = None
        self.token_expires = None

    async def get_admin_token(self) -> Optional[str]:
        """Get admin access token for Keycloak Admin API"""
        # Check if we have a valid cached token
        if self.admin_token and self.token_expires and datetime.utcnow() < self.token_expires:
            return self.admin_token

        try:
            # Get token using admin credentials
            data = {
                "grant_type": "password",
                "client_id": "admin-cli",
                "username": self.admin_username,
                "password": self.admin_password
            }

            response = await self.client.post(
                f"{self.server_url}/realms/master/protocol/openid-connect/token",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            if response.status_code == 200:
                token_data = response.json()
                self.admin_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 300)
                # Refresh 30 seconds before expiry
                self.token_expires = datetime.utcnow() + timedelta(seconds=expires_in - 30)
                return self.admin_token
            else:
                logger.error(f"Failed to get admin token: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error getting admin token: {e}")
            return None

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[httpx.Response]:
        """Make authenticated request to Keycloak Admin API"""
        token = await self.get_admin_token()
        if not token:
            raise Exception("Failed to get admin token")

        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Content-Type"] = "application/json"
        kwargs["headers"] = headers

        url = f"{self.server_url}/admin/realms/{self.realm}{endpoint}"

        try:
            response = await self.client.request(method, url, **kwargs)
            return response
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None

    # ==================== USER MANAGEMENT ====================

    async def list_users(
        self,
        search: Optional[str] = None,
        first: int = 0,
        max: int = 20,
        email: Optional[str] = None,
        username: Optional[str] = None,
        enabled: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """List users with optional filters"""
        params = {
            "first": first,
            "max": max
        }

        if search:
            params["search"] = search
        if email:
            params["email"] = email
        if username:
            params["username"] = username
        if enabled is not None:
            params["enabled"] = str(enabled).lower()

        response = await self._make_request("GET", "/users", params=params)

        if response and response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to list users: {response.status_code if response else 'No response'}")
            return []

    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        response = await self._make_request("GET", f"/users/{user_id}")

        if response and response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get user {user_id}")
            return None

    async def create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        enabled: bool = True,
        email_verified: bool = False,
        temporary_password: bool = False
    ) -> Optional[str]:
        """Create a new user and return the user ID"""
        user_data = {
            "username": username,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "enabled": enabled,
            "emailVerified": email_verified,
            "credentials": [{
                "type": "password",
                "value": password,
                "temporary": temporary_password
            }]
        }

        response = await self._make_request("POST", "/users", json=user_data)

        if response and response.status_code == 201:
            # Get user ID from Location header
            location = response.headers.get("Location")
            if location:
                user_id = location.split("/")[-1]
                logger.info(f"User created successfully: {user_id}")
                return user_id
            return None
        else:
            error_msg = response.json() if response else "No response"
            logger.error(f"Failed to create user: {response.status_code if response else 'No response'} - {error_msg}")
            return None

    async def update_user(
        self,
        user_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        enabled: Optional[bool] = None
    ) -> bool:
        """Update user information"""
        # Get current user data
        current_user = await self.get_user(user_id)
        if not current_user:
            return False

        # Update only provided fields
        if email is not None:
            current_user["email"] = email
        if first_name is not None:
            current_user["firstName"] = first_name
        if last_name is not None:
            current_user["lastName"] = last_name
        if enabled is not None:
            current_user["enabled"] = enabled

        response = await self._make_request("PUT", f"/users/{user_id}", json=current_user)

        if response and response.status_code == 204:
            logger.info(f"User {user_id} updated successfully")
            return True
        else:
            logger.error(f"Failed to update user {user_id}")
            return False

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        response = await self._make_request("DELETE", f"/users/{user_id}")

        if response and response.status_code == 204:
            logger.info(f"User {user_id} deleted successfully")
            return True
        else:
            logger.error(f"Failed to delete user {user_id}")
            return False

    async def reset_password(self, user_id: str, new_password: str, temporary: bool = False) -> bool:
        """Reset user password"""
        credential_data = {
            "type": "password",
            "value": new_password,
            "temporary": temporary
        }

        response = await self._make_request(
            "PUT",
            f"/users/{user_id}/reset-password",
            json=credential_data
        )

        if response and response.status_code == 204:
            logger.info(f"Password reset for user {user_id}")
            return True
        else:
            logger.error(f"Failed to reset password for user {user_id}")
            return False

    async def get_user_groups(self, user_id: str) -> List[Dict[str, Any]]:
        """Get groups that user belongs to"""
        response = await self._make_request("GET", f"/users/{user_id}/groups")

        if response and response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get groups for user {user_id}")
            return []

    async def get_user_count(self) -> int:
        """Get total user count"""
        response = await self._make_request("GET", "/users/count")

        if response and response.status_code == 200:
            try:
                # Try to parse as JSON first (newer Keycloak versions)
                data = response.json()
                if isinstance(data, dict) and 'count' in data:
                    return data['count']
                # Fallback to direct int conversion (older versions)
                return int(response.text)
            except (ValueError, KeyError):
                logger.error(f"Failed to parse user count: {response.text}")
                return 0
        else:
            logger.error("Failed to get user count")
            return 0

    # ==================== GROUP MANAGEMENT ====================

    async def list_groups(
        self,
        search: Optional[str] = None,
        first: int = 0,
        max: int = 20
    ) -> List[Dict[str, Any]]:
        """List groups with optional search"""
        params = {
            "first": first,
            "max": max
        }

        if search:
            params["search"] = search

        response = await self._make_request("GET", "/groups", params=params)

        if response and response.status_code == 200:
            return response.json()
        else:
            logger.error("Failed to list groups")
            return []

    async def get_group(self, group_id: str) -> Optional[Dict[str, Any]]:
        """Get group by ID"""
        response = await self._make_request("GET", f"/groups/{group_id}")

        if response and response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get group {group_id}")
            return None

    async def create_group(self, name: str, path: Optional[str] = None, attributes: Optional[Dict] = None) -> Optional[str]:
        """Create a new group and return the group ID"""
        group_data = {
            "name": name
        }

        if path:
            group_data["path"] = path
        if attributes:
            group_data["attributes"] = attributes

        response = await self._make_request("POST", "/groups", json=group_data)

        if response and response.status_code == 201:
            # Get group ID from Location header
            location = response.headers.get("Location")
            if location:
                group_id = location.split("/")[-1]
                logger.info(f"Group created successfully: {group_id}")
                return group_id
            return None
        else:
            logger.error(f"Failed to create group: {response.status_code if response else 'No response'}")
            return None

    async def update_group(
        self,
        group_id: str,
        name: Optional[str] = None,
        attributes: Optional[Dict] = None
    ) -> bool:
        """Update group information"""
        # Get current group data
        current_group = await self.get_group(group_id)
        if not current_group:
            return False

        # Update only provided fields
        if name is not None:
            current_group["name"] = name
        if attributes is not None:
            current_group["attributes"] = attributes

        response = await self._make_request("PUT", f"/groups/{group_id}", json=current_group)

        if response and response.status_code == 204:
            logger.info(f"Group {group_id} updated successfully")
            return True
        else:
            logger.error(f"Failed to update group {group_id}")
            return False

    async def delete_group(self, group_id: str) -> bool:
        """Delete a group"""
        response = await self._make_request("DELETE", f"/groups/{group_id}")

        if response and response.status_code == 204:
            logger.info(f"Group {group_id} deleted successfully")
            return True
        else:
            logger.error(f"Failed to delete group {group_id}")
            return False

    async def get_group_members(self, group_id: str, first: int = 0, max: int = 100) -> List[Dict[str, Any]]:
        """Get members of a group"""
        params = {
            "first": first,
            "max": max
        }

        response = await self._make_request("GET", f"/groups/{group_id}/members", params=params)

        if response and response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get members for group {group_id}")
            return []

    async def add_user_to_group(self, user_id: str, group_id: str) -> bool:
        """Add user to a group"""
        response = await self._make_request("PUT", f"/users/{user_id}/groups/{group_id}")

        if response and response.status_code == 204:
            logger.info(f"User {user_id} added to group {group_id}")
            return True
        else:
            logger.error(f"Failed to add user {user_id} to group {group_id}")
            return False

    async def remove_user_from_group(self, user_id: str, group_id: str) -> bool:
        """Remove user from a group"""
        response = await self._make_request("DELETE", f"/users/{user_id}/groups/{group_id}")

        if response and response.status_code == 204:
            logger.info(f"User {user_id} removed from group {group_id}")
            return True
        else:
            logger.error(f"Failed to remove user {user_id} from group {group_id}")
            return False

    async def get_group_count(self) -> int:
        """Get total group count"""
        response = await self._make_request("GET", "/groups/count")

        if response and response.status_code == 200:
            try:
                # Try to parse as JSON first (newer Keycloak versions)
                data = response.json()
                if isinstance(data, dict) and 'count' in data:
                    return data['count']
                # Fallback to direct int conversion (older versions)
                return int(response.text)
            except (ValueError, KeyError):
                logger.error(f"Failed to parse group count: {response.text}")
                return 0
        else:
            logger.error("Failed to get group count")
            return 0

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
