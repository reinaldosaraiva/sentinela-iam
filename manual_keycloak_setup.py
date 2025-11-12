#!/usr/bin/env python3
"""
Manual Keycloak Setup Guide and Automation
"""

import webbrowser
import time
import requests
from requests.auth import HTTPBasicAuth

def setup_keycloak_manual():
    """Provide manual setup instructions and automate where possible"""
    
    print("🔑 Keycloak Setup for Sentinela")
    print("=" * 50)
    
    # Open admin console
    admin_url = "http://localhost:8081/admin"
    print(f"1. Opening Keycloak Admin Console: {admin_url}")
    print("   Login with: admin / admin123")
    
    try:
        webbrowser.open(admin_url)
        print("   ✅ Browser opened")
    except:
        print("   ⚠️  Could not open browser automatically")
        print(f"   Please manually open: {admin_url}")
    
    print("\n2. Create Realm:")
    print("   - Click 'Add realm'")
    print("   - Name: my-app")
    print("   - Enable realm")
    print("   - Click 'Create'")
    
    print("\n3. Create Client:")
    print("   - Go to Clients → Create client")
    print("   - Client ID: sentinela-api")
    print("   - Client protocol: openid-connect")
    print("   - Access type: confidential")
    print("   - Service Accounts Enabled: ON")
    print("   - Authorization Enabled: ON")
    print("   - Valid Redirect URIs: http://localhost:8000/*, http://localhost:8001/*")
    print("   - Web Origins: http://localhost:8000, http://localhost:8001")
    print("   - Click 'Save'")
    
    print("\n4. Create Users:")
    users = [
        {"username": "alice", "email": "alice@company.com", "password": "alice123"},
        {"username": "bob", "email": "bob@company.com", "password": "bob123"},
        {"username": "admin", "email": "admin@company.com", "password": "admin123"}
    ]
    
    for user in users:
        print(f"   - Go to Users → Add user")
        print(f"   - Username: {user['username']}")
        print(f"   - Email: {user['email']}")
        print(f"   - Enabled: ON")
        print(f"   - Click 'Save'")
        print(f"   - Go to Credentials → Set password")
        print(f"   - Password: {user['password']}")
        print(f"   - Temporary: OFF")
        print(f"   - Click 'Save'")
        print()
    
    print("5. Create Groups:")
    print("   - Go to Groups → New")
    print("   - Name: employees")
    print("   - Click 'Create'")
    print("   - Name: managers")
    print("   - Click 'Create'")
    
    print("\n6. Add Users to Groups:")
    print("   - Go to Users → View all users")
    print("   - Click on 'alice'")
    print("   - Go to Groups tab")
    print("   - Join 'employees' group")
    print("   - Click on 'admin'")
    print("   - Go to Groups tab")
    print("   - Join 'managers' group")
    
    print("\n7. Test Configuration:")
    print("   After setup, test with:")
    print("   curl -X POST http://localhost:8081/realms/my-app/protocol/openid-connect/token \\")
    print("     -H 'Content-Type: application/x-www-form-urlencoded' \\")
    print("     -d 'client_id=sentinela-api&client_secret=YOUR_SECRET&username=alice&password=alice123&grant_type=password'")
    
    print("\n" + "=" * 50)
    print("⏱️  Waiting for you to complete setup...")
    print("Press Enter when you're ready to test the configuration")
    
    input()
    
    # Test the setup
    test_keycloak_setup()

def test_keycloak_setup():
    """Test if Keycloak realm is properly configured"""
    
    print("\n🧪 Testing Keycloak Configuration")
    print("=" * 50)
    
    # Test realm exists
    try:
        response = requests.get("http://localhost:8081/realms/my-app/.well-known/openid-configuration", timeout=5)
        
        if response.status_code == 200:
            config = response.json()
            print("✅ Realm 'my-app' is accessible")
            print(f"   Issuer: {config.get('issuer', 'N/A')}")
            print(f"   Auth endpoint: {config.get('authorization_endpoint', 'N/A')}")
            print(f"   Token endpoint: {config.get('token_endpoint', 'N/A')}")
            
            # Test user authentication
            test_user_auth(config.get('token_endpoint'))
            
        else:
            print(f"❌ Realm 'my-app' not accessible: {response.status_code}")
            print("   Make sure you created the realm correctly")
            
    except Exception as e:
        print(f"❌ Error testing realm: {e}")
        print("   Make sure Keycloak is running and realm is created")

def test_user_auth(token_endpoint):
    """Test user authentication"""
    
    print("\n🔐 Testing User Authentication")
    print("-" * 30)
    
    # Test with different users
    users = [
        {"username": "alice", "password": "alice123"},
        {"username": "bob", "password": "bob123"},
        {"username": "admin", "password": "admin123"}
    ]
    
    for user in users:
        try:
            auth_data = {
                "client_id": "sentinela-api",
                "client_secret": "sentinela-secret",  # Default secret, may need to be updated
                "username": user["username"],
                "password": user["password"],
                "grant_type": "password"
            }
            
            response = requests.post(token_endpoint, data=auth_data, timeout=5)
            
            if response.status_code == 200:
                token_data = response.json()
                print(f"✅ {user['username']}: Authentication successful")
                print(f"   Access token: {token_data.get('access_token', '')[:50]}...")
                print(f"   Expires in: {token_data.get('expires_in', 'N/A')} seconds")
                
                # Test JWT validation
                test_jwt_validation(token_data.get('access_token', ''))
                
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                print(f"❌ {user['username']}: Authentication failed")
                print(f"   Error: {error_data}")
                
        except Exception as e:
            print(f"❌ {user['username']}: Error - {e}")

def test_jwt_validation(access_token):
    """Test JWT token validation"""
    
    try:
        # Simple JWT parsing (header.payload.signature)
        parts = access_token.split('.')
        if len(parts) == 3:
            import base64
            import json
            
            # Decode payload (add padding if needed)
            payload = parts[1]
            padding = '=' * (-len(payload) % 4)
            decoded = base64.urlsafe_b64decode(payload + padding)
            payload_data = json.loads(decoded)
            
            print(f"   JWT Subject: {payload_data.get('sub', 'N/A')}")
            print(f"   JWT Email: {payload_data.get('email', 'N/A')}")
            print(f"   JWT Groups: {payload_data.get('groups', 'N/A')}")
            
    except Exception as e:
        print(f"   JWT parsing error: {e}")

if __name__ == "__main__":
    setup_keycloak_manual()