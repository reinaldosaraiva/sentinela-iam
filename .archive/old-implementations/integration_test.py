#!/usr/bin/env python3
"""
Integration test for Sentinela MVP
Tests the complete authorization flow
"""

import requests
import json
import time
import sys

def test_policy_api():
    """Test Policy API endpoints"""
    print("🧪 Testing Policy API...")
    
    try:
        # Test health
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Policy API health check passed")
        else:
            print(f"❌ Policy API health failed: {response.status_code}")
            return False
            
        # Test policy creation
        policy_data = {
            "name": "Test Policy",
            "description": "Integration test policy",
            "content": "permit(principal, action == Action::\"read\", resource);"
        }
        
        response = requests.post("http://localhost:8000/policies/", 
                             json=policy_data, timeout=5)
        if response.status_code in [200, 201]:
            print("✅ Policy creation successful")
            policy_id = response.json().get("id")
            return policy_id
        else:
            print(f"❌ Policy creation failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Policy API test failed: {e}")
        return False

def test_business_api():
    """Test Business API endpoints"""
    print("\n🧪 Testing Business API...")
    
    try:
        # Test health (without auth first)
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Business API health check passed")
        else:
            print(f"❌ Business API health failed: {response.status_code}")
            return False
            
        # Test document creation (should fail without auth)
        doc_data = {
            "title": "Test Document",
            "content": "This is a test document",
            "document_type": "contract",
            "department": "finance"
        }
        
        response = requests.post("http://localhost:8001/documentos/", 
                             json=doc_data, timeout=5)
        if response.status_code == 401:
            print("✅ Business API correctly requires authentication")
        else:
            print(f"❌ Business API auth check failed: {response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Business API test failed: {e}")
        return False

def test_keycloak():
    """Test Keycloak availability"""
    print("\n🧪 Testing Keycloak...")
    
    try:
        # Test master realm
        response = requests.get("http://localhost:8081/realms/master/.well-known/openid_configuration", 
                            timeout=5)
        if response.status_code == 200:
            print("✅ Keycloak is responding")
            return True
        else:
            print(f"❌ Keycloak not responding: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Keycloak test failed: {e}")
        return False

def main():
    """Run integration tests"""
    print("🚀 Sentinela MVP Integration Test\n")
    
    # Test individual components
    keycloak_ok = test_keycloak()
    policy_api_ok = test_policy_api() is not False
    business_api_ok = test_business_api()
    
    print(f"\n📊 Component Status:")
    print(f"   Keycloak: {'✅' if keycloak_ok else '❌'}")
    print(f"   Policy API: {'✅' if policy_api_ok else '❌'}")
    print(f"   Business API: {'✅' if business_api_ok else '❌'}")
    
    if keycloak_ok and policy_api_ok and business_api_ok:
        print("\n🎉 All components are working!")
        print("\n📋 Next Steps:")
        print("   1. Set up Keycloak realm with ./setup/keycloak-setup.sh")
        print("   2. Create test user 'alice' with appropriate roles")
        print("   3. Test complete authorization flow")
        print("   4. Configure OPAL policy synchronization")
        return 0
    else:
        print("\n⚠️  Some components need attention")
        return 1

if __name__ == "__main__":
    exit(main())