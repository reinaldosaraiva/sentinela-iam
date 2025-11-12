#!/usr/bin/env python3
"""
Improved Cedar Policy Engine for authorization evaluation
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


class ImprovedCedarEngine:
    """Improved Cedar policy engine with proper evaluation logic"""
    
    def __init__(self):
        self.policies: List[str] = []
        self.compiled_policies = []
    
    def load_policies(self, policies: List[str]):
        """Load Cedar policies"""
        self.policies = policies
        self.compiled_policies = []
        
        # Parse and compile policies
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
        """Parse a Cedar policy with improved logic"""
        try:
            # Extract policy name
            policy_name_match = re.search(r'policy\s+(\w+)\s*{', policy_text)
            policy_name = policy_name_match.group(1) if policy_name_match else f'policy_{len(self.compiled_policies) + 1}'
            
            # Extract permit statement
            permit_match = re.search(r'permit\s*\([^)]*(?:\{[^}]*\})?\)', policy_text, re.DOTALL)
            
            if permit_match:
                permit_statement = permit_match.group(0)
                
                # Parse conditions more accurately
                conditions = []
                
                # Extract all conditions more comprehensively
                lines = permit_statement.split('\n')
                for line in lines:
                    line = line.strip()
                    
                    # Extract principal condition
                    principal_match = re.search(r'principal\s+(?:in\s+)?([^\s,)]+)', line)
                    if principal_match:
                        principal_value = principal_match.group(1)
                        conditions.append({
                            'type': 'principal',
                            'operator': 'equals',
                            'value': principal_value
                        })
                    
                    # Extract action condition
                    action_match = re.search(r'action\s+(?:in\s+)?([^\s,)]+)', line)
                    if action_match:
                        action_value = action_match.group(1)
                        conditions.append({
                            'type': 'action',
                            'operator': 'equals',
                            'value': action_value
                        })
                    
                    # Extract resource condition
                    resource_match = re.search(r'resource\s+(?:in\s+)?([^\s,)]+)', line)
                    if resource_match:
                        resource_value = resource_match.group(1)
                        conditions.append({
                            'type': 'resource',
                            'operator': 'equals',
                            'value': resource_value
                        })
                
                # Extract when conditions
                when_match = re.search(r'when\s*\{([^}]+)\}', permit_statement, re.DOTALL)
                if when_match:
                    when_conditions = self._parse_when_conditions(when_match.group(1))
                    conditions.extend(when_conditions)
                
                return {
                    'name': policy_name,
                    'type': 'permit',
                    'conditions': conditions,
                    'raw': policy_text
                }
        
        except Exception as e:
            logger.error(f"Policy parsing error: {e}")
        
        return None
    
    def _parse_when_conditions(self, when_text: str) -> List[Dict[str, Any]]:
        """Parse when clause conditions"""
        conditions = []
        
        # Parse principal.hasGroup condition
        group_match = re.search(r'principal\.hasGroup\s*==\s*"([^"]+)"', when_text)
        if group_match:
            conditions.append({
                'type': 'group',
                'operator': 'equals',
                'value': group_match.group(1)
            })
        
        # Parse other conditions as needed
        # Add more parsing logic here for complex conditions
        
        return conditions
    
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
            
            # Default deny if no policy allows
            logger.info("Denied: no matching policy found")
            return AuthorizationResponse(allow=False, reason="No matching policy")
            
        except Exception as e:
            logger.error(f"Policy evaluation error: {e}")
            return AuthorizationResponse(allow=False, reason="Evaluation error")
    
    def _evaluate_policy(self, policy: Dict[str, Any], request: AuthorizationRequest) -> AuthorizationResponse:
        """Evaluate a single policy against request"""
        try:
            # For permit policies, all conditions must be satisfied
            if policy['type'] == 'permit':
                for condition in policy['conditions']:
                    if not self._evaluate_condition(condition, request):
                        return AuthorizationResponse(
                            allow=False,
                            reason=f"Condition failed: {condition['type']} {condition.get('operator', '')} {condition.get('value', '')}"
                        )
                
                return AuthorizationResponse(allow=True)
            
            return AuthorizationResponse(allow=False, reason="Unknown policy type")
            
        except Exception as e:
            logger.error(f"Policy evaluation error: {e}")
            return AuthorizationResponse(allow=False, reason="Evaluation error")
    
    def _evaluate_condition(self, condition: Dict[str, Any], request: AuthorizationRequest) -> bool:
        """Evaluate a single condition with proper logic"""
        try:
            condition_type = condition['type']
            operator = condition.get('operator', 'equals')
            expected_value = condition.get('value')
            
            if condition_type == 'principal':
                # Check if principal matches expected value
                if operator == 'equals':
                    return request.principal == expected_value
                elif operator == 'in':
                    # Handle "in" operator for multiple values
                    if expected_value and expected_value.startswith('User::'):
                        return request.principal == expected_value
                    # Add more complex "in" logic if needed
                return False
            
            elif condition_type == 'action':
                # Check if action matches expected value
                if operator == 'equals':
                    return request.action == expected_value
                elif operator == 'in':
                    # Handle wildcard actions
                    if expected_value == 'Action::*':
                        return True
                    elif expected_value and expected_value.startswith('Action::'):
                        return request.action == expected_value
                return False
            
            elif condition_type == 'resource':
                # Check if resource matches expected value
                if operator == 'equals':
                    return request.resource == expected_value
                elif operator == 'in':
                    # Handle wildcard resources
                    if expected_value == 'Document::*':
                        return True
                    elif expected_value and expected_value.startswith('Document::'):
                        return request.resource == expected_value
                return False
            
            elif condition_type == 'group':
                # Check if user has required group
                if operator == 'equals':
                    user_groups = request.context.get('groups', [])
                    return expected_value in user_groups
                return False
            
            return False
            
        except Exception as e:
            logger.error(f"Condition evaluation error: {e}")
            return False


def test_improved_engine():
    """Test the improved Cedar engine"""
    print("🔐 Testing Improved Cedar Engine")
    print("=" * 50)
    
    engine = ImprovedCedarEngine()
    
    # Test policies
    policies = [
        """
        policy DocumentRead {
            permit(
                principal in User::"alice",
                action in Action::"read",
                resource in Document::"public"
            );
        }
        """,
        """
        policy AdminAccess {
            permit(
                principal in User::"admin",
                action in Action::*,
                resource in Document::*
            );
        }
        """,
        """
        policy EmployeeDocumentAccess {
            permit(
                principal in User::"employee",
                action in Action::"read",
                resource in Document::"hr"
            ) when {
                principal.hasGroup == "employees"
            };
        }
        """
    ]
    
    engine.load_policies(policies)
    
    # Test cases
    test_cases = [
        {
            "name": "Alice reading public document",
            "principal": 'User::"alice"',
            "action": 'Action::"read"',
            "resource": 'Document::"public"',
            "context": {},
            "expected": True
        },
        {
            "name": "Alice reading secret document",
            "principal": 'User::"alice"',
            "action": 'Action::"read"',
            "resource": 'Document::"secret"',
            "context": {},
            "expected": False
        },
        {
            "name": "Admin reading any document",
            "principal": 'User::"admin"',
            "action": 'Action::"read"',
            "resource": 'Document::"secret"',
            "context": {},
            "expected": True
        },
        {
            "name": "Employee reading HR document with group",
            "principal": 'User::"employee"',
            "action": 'Action::"read"',
            "resource": 'Document::"hr"',
            "context": {"groups": ["employees"]},
            "expected": True
        },
        {
            "name": "Employee reading HR document without group",
            "principal": 'User::"employee"',
            "action": 'Action::"read"',
            "resource": 'Document::"hr"',
            "context": {"groups": ["managers"]},
            "expected": False
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        request = AuthorizationRequest(
            principal=test_case["principal"],
            action=test_case["action"],
            resource=test_case["resource"],
            context=test_case["context"]
        )
        
        result = engine.evaluate(request)
        
        status = "✅ ALLOWED" if result.allow else "❌ DENIED"
        expected_status = "✅ ALLOWED" if test_case["expected"] else "❌ DENIED"
        
        correct = result.allow == test_case["expected"]
        if correct:
            passed += 1
            marker = "✅"
        else:
            marker = "❌"
        
        print(f"{marker} {status}: {test_case['name']}")
        print(f"   Expected: {expected_status}")
        if result.reason:
            print(f"   Reason: {result.reason}")
        print()
    
    print(f"Test Results: {passed}/{total} passed")
    return passed == total


if __name__ == "__main__":
    test_improved_engine()