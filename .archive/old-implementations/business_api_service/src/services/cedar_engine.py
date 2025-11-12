"""
Cedar Policy Engine for authorization evaluation
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)


@dataclass
class AuthorizationRequest:
    """Authorization request for Cedar evaluation"""
    principal: str  # e.g., 'User::"alice-id"'
    action: str      # e.g., 'Action::"read"'
    resource: str    # e.g., 'Document::"123"'
    context: Dict[str, Any]  # Additional context like groups


@dataclass
class AuthorizationResponse:
    """Authorization response from Cedar evaluation"""
    allow: bool
    reason: Optional[str] = None


class CedarEngine:
    """Mock Cedar policy engine for MVP"""
    
    def __init__(self):
        self.policies: List[str] = []
        self.compiled_policies = []
    
    def load_policies(self, policies: List[str]):
        """Load Cedar policies"""
        self.policies = policies
        self.compiled_policies = []
        
        # Parse and compile policies (mock implementation)
        for policy in policies:
            try:
                compiled = self._parse_policy(policy)
                if compiled:
                    self.compiled_policies.append(compiled)
                    logger.info(f"Loaded policy: {compiled.get('name', 'unnamed')}")
            except Exception as e:
                logger.error(f"Failed to parse policy: {e}")
        
        logger.info(f"Loaded {len(self.compiled_policies)} policies")
    
    def _parse_policy(self, policy_text: str) -> Optional[Dict[str, Any]]:
        """Parse a Cedar policy (mock implementation)"""
        try:
            # Simple regex-based parsing for MVP
            # Look for permit(...) statements
            permit_match = re.search(r'permit\s*\([^)]*\)', policy_text, re.IGNORECASE)
            
            if permit_match:
                permit_statement = permit_match.group(0)
                
                # Extract conditions (mock)
                conditions = []
                
                # Check for principal condition
                if 'principal' in permit_statement:
                    conditions.append({'type': 'principal', 'operator': 'any'})
                
                # Check for action condition
                action_match = re.search(r'action\s*==\s*Action::"([^"]+)"', permit_statement)
                if action_match:
                    conditions.append({
                        'type': 'action',
                        'operator': 'equals',
                        'value': action_match.group(1)
                    })
                
                # Check for resource type condition
                resource_match = re.search(r'resource_type\s*==\s*"([^"]+)"', permit_statement)
                if resource_match:
                    conditions.append({
                        'type': 'resource_type',
                        'operator': 'equals',
                        'value': resource_match.group(1)
                    })
                
                return {
                    'name': f'policy_{len(self.compiled_policies) + 1}',
                    'type': 'permit',
                    'conditions': conditions,
                    'raw': policy_text
                }
        
        except Exception as e:
            logger.error(f"Policy parsing error: {e}")
        
        return None
    
    def evaluate(self, request: AuthorizationRequest) -> AuthorizationResponse:
        """Evaluate authorization request against loaded policies"""
        try:
            logger.info(f"Evaluating: {request.principal} {request.action} {request.resource}")
            
            # Check each policy
            for policy in self.compiled_policies:
                result = self._evaluate_policy(policy, request)
                if result.allow:
                    logger.info(f"Allowed by policy: {policy['name']}")
                    return result
            
            # Default deny
            logger.info("Denied: no matching policy found")
            return AuthorizationResponse(allow=False, reason="No matching policy")
            
        except Exception as e:
            logger.error(f"Policy evaluation error: {e}")
            return AuthorizationResponse(allow=False, reason="Evaluation error")
    
    def _evaluate_policy(self, policy: Dict[str, Any], request: AuthorizationRequest) -> AuthorizationResponse:
        """Evaluate a single policy against the request"""
        try:
            # For permit policies, all conditions must be satisfied
            if policy['type'] == 'permit':
                for condition in policy['conditions']:
                    if not self._evaluate_condition(condition, request):
                        return AuthorizationResponse(
                            allow=False,
                            reason=f"Condition failed: {condition['type']}"
                        )
                
                return AuthorizationResponse(allow=True)
            
            return AuthorizationResponse(allow=False, reason="Unknown policy type")
            
        except Exception as e:
            logger.error(f"Policy evaluation error: {e}")
            return AuthorizationResponse(allow=False, reason="Evaluation error")
    
    def _evaluate_condition(self, condition: Dict[str, Any], request: AuthorizationRequest) -> bool:
        """Evaluate a single condition"""
        try:
            condition_type = condition['type']
            operator = condition.get('operator', 'equals')
            
            if condition_type == 'principal':
                # For MVP, allow any principal
                return True
            
            elif condition_type == 'action':
                if operator == 'equals':
                    expected_action = f'Action::"{condition["value"]}"'
                    return request.action == expected_action
            
            elif condition_type == 'resource_type':
                if operator == 'equals':
                    # Extract resource type from request.resource
                    # Format: 'Document::"123"' -> 'Document'
                    resource_parts = request.resource.split('::')
                    if len(resource_parts) >= 2:
                        resource_type = resource_parts[0]
                        return resource_type == condition["value"]
            
            return False
            
        except Exception as e:
            logger.error(f"Condition evaluation error: {e}")
            return False
    
    def get_policy_count(self) -> int:
        """Get number of loaded policies"""
        return len(self.compiled_policies)
    
    def get_policies_info(self) -> List[Dict[str, Any]]:
        """Get information about loaded policies"""
        return [
            {
                'name': policy['name'],
                'type': policy['type'],
                'conditions_count': len(policy['conditions'])
            }
            for policy in self.compiled_policies
        ]