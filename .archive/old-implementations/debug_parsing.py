#!/usr/bin/env python3
"""
Debug policy parsing
"""

import re

def debug_policy_parsing():
    """Debug how policies are being parsed"""
    
    policies = [
        """
        policy AdminAccess {
            permit(
                principal in User::"admin",
                action in Action::*,
                resource in Document::*
            );
        }
        """
    ]
    
    for policy_text in policies:
        print("🔍 Debugging Policy:")
        print("=" * 50)
        print(f"Original: {policy_text.strip()}")
        
        # Extract permit statement
        permit_match = re.search(r'permit\s*\([^)]*(?:\{[^}]*\})?\)', policy_text, re.DOTALL)
        
        if permit_match:
            permit_statement = permit_match.group(0)
            print(f"Permit statement: {permit_statement}")
            
            # Extract principal condition
            principal_match = re.search(r'principal\s+(?:in\s+)?([^\s,)]+)', permit_statement)
            if principal_match:
                principal_value = principal_match.group(1)
                print(f"Principal condition: {principal_value}")
            
            # Extract action condition
            action_match = re.search(r'action\s+(?:in\s+)?([^\s,)]+)', permit_statement)
            if action_match:
                action_value = action_match.group(1)
                print(f"Action condition: {action_value}")
            
            # Extract resource condition
            resource_match = re.search(r'resource\s+(?:in\s+)?([^\s,)]+)', permit_statement)
            if resource_match:
                resource_value = resource_match.group(1)
                print(f"Resource condition: {resource_value}")
        
        print()

if __name__ == "__main__":
    debug_policy_parsing()