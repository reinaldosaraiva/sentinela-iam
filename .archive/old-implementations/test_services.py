#!/usr/bin/env python3
"""
Simple test script to verify Sentinela services work independently
"""

import sys
import os

# Add paths for imports
policy_api_path = os.path.join(os.path.dirname(__file__), 'policy_api', 'src')
business_api_path = os.path.join(os.path.dirname(__file__), 'business_api_service', 'src')

sys.path.insert(0, policy_api_path)
sys.path.insert(0, business_api_path)

def test_policy_api():
    """Test Policy API components"""
    print("🧪 Testing Policy API components...")
    
    try:
        sys.path.insert(0, policy_api_path)
        from models.policy import Policy, PolicyCreate
        print("✅ Policy models imported successfully")
        
        # Test policy creation
        policy_data = PolicyCreate(
            name="Test Policy",
            description="Test policy for verification",
            content="permit(principal, action, resource);"
        )
        print(f"✅ PolicyCreate model works: {policy_data.name}")
        
        return True
    except Exception as e:
        print(f"❌ Policy API test failed: {e}")
        return False

def test_business_api():
    """Test Business API components"""
    print("\n🧪 Testing Business API components...")
    
    try:
        # Clear and set path
        sys.path = [business_api_path] + [p for p in sys.path if business_api_path not in p]
        from models.document import Document, DocumentCreate
        print("✅ Document models imported successfully")
        
        # Test document creation
        doc_data = DocumentCreate(
            title="Test Document",
            content="This is a test document",
            document_type="contract",
            department="finance"
        )
        print(f"✅ DocumentCreate model works: {doc_data.title}")
        
        return True
    except Exception as e:
        print(f"❌ Business API test failed: {e}")
        return False

def test_services():
    """Test service components"""
    print("\n🧪 Testing Service components...")
    
    try:
        sys.path.insert(0, business_api_path)
        from services.cedar_engine import CedarEngine
        from services.opal_client import OPALClient
        from services.keycloak_service import KeycloakService
        
        print("✅ All service modules imported successfully")
        
        # Test Cedar Engine
        from services.cedar_engine import AuthorizationRequest
        engine = CedarEngine()
        engine.load_policies(["permit(principal, action, resource);"])
        
        request = AuthorizationRequest(
            principal='User::"alice"',
            action='Action::"read"',
            resource='Document::"123"',
            context={"department": "finance"}
        )
        result = engine.evaluate(request)
        print(f"✅ Cedar engine evaluation: {result.allow} - {result.reason}")
        
        return True
    except Exception as e:
        print(f"❌ Services test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Sentinela Service Tests\n")
    
    results = []
    results.append(test_policy_api())
    results.append(test_business_api())
    results.append(test_services())
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! The services are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())