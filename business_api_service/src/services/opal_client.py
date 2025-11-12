"""
OPAL Client for policy synchronization
"""

import httpx
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import json

logger = logging.getLogger(__name__)


class OPALClient:
    """Client for connecting to OPAL server and receiving policy updates"""
    
    def __init__(self, server_url: str, auth_token: str):
        self.server_url = server_url.rstrip('/')
        self.auth_token = auth_token
        self.client = httpx.AsyncClient(
            base_url=server_url,
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=30.0
        )
        self.policies = []
        self.last_update = None
        self.running = False
    
    async def health_check(self) -> bool:
        """Check if OPAL server is healthy"""
        try:
            response = await self.client.get("/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"OPAL health check failed: {e}")
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
    
    async def subscribe_to_policy_updates(self, callback=None):
        """Subscribe to policy updates from OPAL server"""
        self.running = True
        logger.info("Starting OPAL policy subscription...")
        
        while self.running:
            try:
                # Get latest policies
                policy_data = await self.get_policy_data()
                if policy_data:
                    # Check if policies have changed
                    if self.policies != policy_data:
                        logger.info("Policy update detected")
                        self.policies = policy_data
                        self.last_update = datetime.utcnow()
                        
                        # Call callback if provided
                        if callback:
                            await callback(policy_data)
                
                # Wait before next check
                await asyncio.sleep(30)  # Poll every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in policy subscription: {e}")
                await asyncio.sleep(5)  # Wait before retry
    
    def stop_subscription(self):
        """Stop policy subscription"""
        self.running = False
        logger.info("Stopping OPAL policy subscription...")
    
    async def get_policies(self) -> List[str]:
        """Get current policies"""
        return self.policies if isinstance(self.policies, list) else []
    
    def get_last_update(self) -> Optional[datetime]:
        """Get timestamp of last policy update"""
        return self.last_update
    
    async def close(self):
        """Close HTTP client"""
        self.stop_subscription()
        await self.client.aclose()