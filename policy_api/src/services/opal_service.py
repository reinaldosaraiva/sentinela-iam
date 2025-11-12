"""
OPAL Service for policy synchronization
"""

import httpx
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class OPALService:
    """Service for interacting with OPAL server"""
    
    def __init__(self, server_url: str, auth_token: str):
        self.server_url = server_url.rstrip('/')
        self.auth_token = auth_token
        self.client = httpx.AsyncClient(
            base_url=server_url,
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=30.0
        )
    
    async def health_check(self) -> bool:
        """Check if OPAL server is healthy"""
        try:
            response = await self.client.get("/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"OPAL health check failed: {e}")
            return False
    
    async def notify_policy_update(
        self, 
        policy_data: Dict[str, Any],
        topic: str = "policy_data"
    ) -> bool:
        """Notify OPAL server about policy updates"""
        try:
            payload = {
                "data": policy_data,
                "timestamp": datetime.utcnow().isoformat(),
                "topic": topic
            }
            
            response = await self.client.post(
                "/policy-updates",
                json=payload
            )
            
            if response.status_code == 200:
                logger.info(f"Policy update notification sent successfully")
                return True
            else:
                logger.error(f"Failed to notify policy update: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error notifying policy update: {e}")
            return False
    
    async def get_policy_data(self, path: str = "/") -> Optional[Dict[str, Any]]:
        """Get current policy data from OPAL server"""
        try:
            response = await self.client.get(f"/policy-data{path}")
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get policy data: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error getting policy data: {e}")
            return None
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()