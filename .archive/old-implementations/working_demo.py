#!/usr/bin/env python3
"""
Working demo of the Sentinela authorization system
"""

import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.join(os.getcwd(), 'business_api_service', 'src'))

from services.cedar_engine import CedarEngine, AuthorizationRequest
from services.keycloak_service import KeycloakService
import json

def test_cedar_engine():
    """Test the Cedar policy engine"""
    print("🔐 Testing Cedar Policy Engine")
    print("=" * 50)
    
    # Create Cedar engine
    cedar = CedarEngine()
    
    # Define some test policies
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
        """
    ]
    
    # Load policies
    cedar.load_policies(policies)
    
    # Test cases
    test_cases = [
        {
            "name": "Alice reading public document",
            "principal": 'User::"alice"',
            "action": 'Action::"read"',
            "resource": 'Document::"public"',
            "context": {}
        },
        {
            "name": "Alice reading secret document",
            "principal": 'User::"alice"',
            "action": 'Action::"read"',
            "resource": 'Document::"secret"',
            "context": {}
        },
        {
            "name": "Admin reading any document",
            "principal": 'User::"admin"',
            "action": 'Action::"read"',
            "resource": 'Document::"secret"',
            "context": {}
        },
        {
            "name": "Bob reading public document",
            "principal": 'User::"bob"',
            "action": 'Action::"read"',
            "resource": 'Document::"public"',
            "context": {}
        }
    ]
    
    for test_case in test_cases:
        request = AuthorizationRequest(
            principal=test_case["principal"],
            action=test_case["action"],
            resource=test_case["resource"],
            context=test_case["context"]
        )
        
        result = cedar.evaluate(request)
        
        status = "✅ ALLOWED" if result.allow else "❌ DENIED"
        print(f"{status}: {test_case['name']}")
        if result.reason:
            print(f"   Reason: {result.reason}")
    
    print()

def test_keycloak_service():
    """Test the Keycloak service"""
    print("🔑 Testing Keycloak Service")
    print("=" * 50)
    
    try:
        # Create Keycloak service
        keycloak = KeycloakService("http://localhost:8081", "my-app")
        
        # Test getting OpenID config
        config = keycloak.get_openid_config()
        print(f"✅ Keycloak OpenID Config: {len(config)} fields retrieved")
        
        # Test getting public key (this might fail if Keycloak isn't fully configured)
        try:
            public_key = keycloak.get_public_key()
            print(f"✅ Keycloak Public Key: Retrieved successfully")
        except Exception as e:
            print(f"⚠️  Keycloak Public Key: {e}")
        
        # Test JWT validation with mock token
        mock_token = "mock.jwt.token"
        try:
            payload = keycloak.validate_token(mock_token)
            print(f"⚠️  JWT Validation: Mock token validation (expected to fail)")
        except Exception as e:
            print(f"⚠️  JWT Validation: {e}")
            
    except Exception as e:
        print(f"❌ Keycloak Service Error: {e}")
    
    print()

def test_authorization_flow():
    """Test complete authorization flow"""
    print("🚀 Testing Complete Authorization Flow")
    print("=" * 50)
    
    # Create services
    cedar = CedarEngine()
    keycloak = KeycloakService("http://localhost:8081", "my-app")
    
    # Load policies
    policies = [
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
        """,
        """
        policy ManagerDocumentAccess {
            permit(
                principal in User::"manager",
                action in Action::*,
                resource in Document::*
            ) when {
                principal.hasGroup == "managers"
            };
        }
        """
    ]
    
    cedar.load_policies(policies)
    
    # Simulate authorization request with JWT
    auth_header = "Bearer mock.jwt.token"
    
    try:
        # Extract token (mock)
        token = auth_header.split(" ")[1]
        
        # Validate token (mock - in real implementation this would validate with Keycloak)
        user_info = {
            "sub": "user123",
            "email": "employee@company.com",
            "groups": ["employees"]
        }
        
        # Create authorization request
        request = AuthorizationRequest(
            principal=f'User::"{user_info["sub"]}"',
            action='Action::"read"',
            resource='Document::"hr"',
            context={"groups": user_info["groups"]}
        )
        
        # Evaluate authorization
        result = cedar.evaluate(request)
        
        print(f"User: {user_info['email']}")
        print(f"Groups: {', '.join(user_info['groups'])}")
        print(f"Action: read")
        print(f"Resource: hr document")
        print(f"Result: {'✅ ALLOWED' if result.allow else '❌ DENIED'}")
        
        if result.reason:
            print(f"Reason: {result.reason}")
            
    except Exception as e:
        print(f"❌ Authorization Flow Error: {e}")
    
    print()

def main():
    """Main demo function"""
    print("🛡️  Sentinela Authorization System Demo")
    print("=" * 60)
    print()
    
    # Test individual components
    test_cedar_engine()
    test_keycloak_service()
    test_authorization_flow()
    
    print("🎉 Demo completed!")
    print()
    print("Next steps:")
    print("1. Configure Keycloak realm with proper users and groups")
    print("2. Set up OPAL server for policy distribution")
    print("3. Create FastAPI endpoints for the services")
    print("4. Add database persistence for policies and documents")

if __name__ == "__main__":
    main()