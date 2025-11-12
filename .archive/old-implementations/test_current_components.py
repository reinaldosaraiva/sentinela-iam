#!/usr/bin/env python3
"""
Test current components to verify they work
"""

import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.join(os.getcwd(), 'policy_api', 'src'))
sys.path.insert(0, os.path.join(os.getcwd(), 'business_api_service', 'src'))

print("Testing individual components...")

# Test Cedar engine
try:
    from services.cedar_engine import CedarEngine
    cedar = CedarEngine()
    
    # Test a simple policy
    policy = """
    permit(
        principal in User::"alice",
        action in Action::"read",
        resource in Document::"public"
    );
    """
    
    result = cedar.evaluate_policy(policy, {
        "principal": "User::\"alice\"",
        "action": "Action::\"read\"", 
        "resource": "Document::\"public\""
    })
    
    print(f"✅ Cedar Engine: {result}")
except Exception as e:
    print(f"❌ Cedar Engine: {e}")

# Test OPAL client
try:
    from services.opal_client import OPALClient
    opal = OPALClient("http://localhost:7002")
    print(f"✅ OPAL Client: Created successfully")
except Exception as e:
    print(f"❌ OPAL Client: {e}")

# Test Keycloak service
try:
    from services.keycloak_service import KeycloakService
    keycloak = KeycloakService("http://localhost:8080", "my-app")
    print(f"✅ Keycloak Service: Created successfully")
except Exception as e:
    print(f"❌ Keycloak Service: {e}")

# Test Policy model
try:
    from models.policy import Policy, PolicyCreate, PolicyUpdate
    policy = Policy(
        id=1,
        name="Test Policy",
        description="Test",
        content="permit(...);",
        version="1.0.0",
        status="draft"
    )
    print(f"✅ Policy Model: {policy.name}")
except Exception as e:
    print(f"❌ Policy Model: {e}")

# Test Document model
try:
    from models.document import Document, DocumentCreate
    doc = Document(
        id=1,
        title="Test Doc",
        content="Test content",
        owner="User::\"alice\"",
        classification="public"
    )
    print(f"✅ Document Model: {doc.title}")
except Exception as e:
    print(f"❌ Document Model: {e}")

print("\nComponent testing complete!")