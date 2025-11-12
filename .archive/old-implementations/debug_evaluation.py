#!/usr/bin/env python3
"""
Debug policy evaluation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'business_api_service', 'src'))

from services.cedar_engine import CedarEngine, AuthorizationRequest

def debug_admin_evaluation():
    """Debug why admin policy is not working"""
    
    print("🔍 Debugging Admin Policy Evaluation")
    print("=" * 50)
    
    cedar = CedarEngine()
    
    # Load only admin policy
    admin_policy = """
        policy AdminAccess {
            permit(
                    principal in User::"admin",
                    action in Action::*,
                    resource in Document::*
                );
            }
        """
    
    cedar.load_policies([admin_policy])
    
    print(f"Loaded {len(cedar.compiled_policies)} policies")
    
    for i, policy in enumerate(cedar.compiled_policies):
        print(f"\nPolicy {i+1}: {policy['name']}")
        print(f"Type: {policy['type']}")
        print(f"Conditions: {len(policy['conditions'])}")
        for j, condition in enumerate(policy['conditions']):
            print(f"  {j+1}. {condition}")
    
    # Test admin request
    request = AuthorizationRequest(
        principal='User::"admin"',
        action='Action::"read"',
        resource='Document::"secret"',
        context={}
    )
    
    print(f"\n🎯 Testing Request:")
    print(f"Principal: {request.principal}")
    print(f"Action: {request.action}")
    print(f"Resource: {request.resource}")
    
    # Evaluate each condition manually
    if cedar.compiled_policies:
        policy = cedar.compiled_policies[0]
        print(f"\n📋 Evaluating Policy: {policy['name']}")
        
        for i, condition in enumerate(policy['conditions']):
            print(f"\nCondition {i+1}: {condition}")
            
            condition_type = condition['type']
            operator = condition.get('operator', 'equals')
            expected_value = condition.get('value')
            
            print(f"  Type: {condition_type}")
            print(f"  Operator: {operator}")
            print(f"  Expected Value: {expected_value}")
            
            if condition_type == 'principal':
                print(f"  Request Principal: {request.principal}")
                print(f"  Match: {request.principal == expected_value}")
                
            elif condition_type == 'action':
                print(f"  Request Action: {request.action}")
                if operator == 'in' and expected_value == 'Action::*':
                    print(f"  Wildcard match: True")
                else:
                    print(f"  Match: {request.action == expected_value}")
                    
            elif condition_type == 'resource':
                print(f"  Request Resource: {request.resource}")
                if operator == 'in' and expected_value == 'Document::*':
                    print(f"  Wildcard match: True")
                else:
                    print(f"  Match: {request.resource == expected_value}")
    
    # Get final result
    result = cedar.evaluate(request)
    print(f"\n🎯 Final Result: {'ALLOWED' if result.allow else 'DENIED'}")
    if result.reason:
        print(f"Reason: {result.reason}")

if __name__ == "__main__":
    debug_admin_evaluation()