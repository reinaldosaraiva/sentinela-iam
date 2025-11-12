#!/usr/bin/env python3
"""
Setup Keycloak realm for Sentinela
"""

import requests
import json
import time

def setup_keycloak():
    """Setup Keycloak realm and users"""
    
    # Keycloak admin URL
    admin_url = "http://localhost:8081/admin"
    token_url = "http://localhost:8081/realms/master/protocol/openid-connect/token"
    
    print("🔑 Setting up Keycloak for Sentinela")
    print("=" * 50)
    
    # Try to get admin token
    print("Getting admin token...")
    
    # First try without HTTPS requirement
    try:
        token_data = {
            "client_id": "admin-cli",
            "username": "admin",
            "password": "admin123",
            "grant_type": "password"
        }
        
        response = requests.post(token_url, data=token_data, verify=False)
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Admin token obtained successfully")
            
            # Create realm
            create_realm(token, admin_url)
            
        else:
            print(f"❌ Failed to get token: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error getting admin token: {e}")
    
    print("\nAlternative setup method:")
    print("1. Open http://localhost:8081/admin in browser")
    print("2. Login with admin/admin123")
    print("3. Create realm 'my-app' manually")
    print("4. Create users and groups as needed")

def create_realm(token, admin_url):
    """Create the my-app realm"""
    
    realm_config = {
        "realm": "my-app",
        "enabled": True,
        "displayName": "Sentinela Application",
        "registrationAllowed": False,
        "loginWithEmailAllowed": True,
        "duplicateEmailsAllowed": False,
        "resetPasswordAllowed": True,
        "editUsernameAllowed": True,
        "bruteForceProtected": True
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{admin_url}/console/realms",
            headers=headers,
            json=realm_config,
            verify=False
        )
        
        if response.status_code in [201, 409]:  # Created or Already Exists
            print("✅ Realm 'my-app' created successfully")
            create_clients(token, admin_url)
        else:
            print(f"❌ Failed to create realm: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error creating realm: {e}")

def create_clients(token, admin_url):
    """Create clients for the realm"""
    
    client_config = {
        "clientId": "sentinela-api",
        "name": "Sentinela API",
        "description": "API client for Sentinela authorization",
        "enabled": True,
        "clientAuthenticatorType": "client-secret",
        "secret": "sentinela-secret",
        "directAccessGrantsEnabled": True,
        "serviceAccountsEnabled": True,
        "authorizationServicesEnabled": True,
        "redirectUris": ["http://localhost:8000/*", "http://localhost:8001/*"],
        "webOrigins": ["http://localhost:8000", "http://localhost:8001"]
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{admin_url}/console/realms/my-app/clients",
            headers=headers,
            json=client_config,
            verify=False
        )
        
        if response.status_code in [201, 409]:
            print("✅ Client 'sentinela-api' created successfully")
            create_users(token, admin_url)
        else:
            print(f"❌ Failed to create client: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error creating client: {e}")

def create_users(token, admin_url):
    """Create test users"""
    
    users = [
        {
            "username": "alice",
            "firstName": "Alice",
            "lastName": "Smith",
            "email": "alice@company.com",
            "enabled": True,
            "credentials": [{
                "type": "password",
                "value": "alice123",
                "temporary": False
            }]
        },
        {
            "username": "bob",
            "firstName": "Bob", 
            "lastName": "Johnson",
            "email": "bob@company.com",
            "enabled": True,
            "credentials": [{
                "type": "password",
                "value": "bob123",
                "temporary": False
            }]
        },
        {
            "username": "admin",
            "firstName": "Admin",
            "lastName": "User",
            "email": "admin@company.com",
            "enabled": True,
            "credentials": [{
                "type": "password",
                "value": "admin123",
                "temporary": False
            }]
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    for user in users:
        try:
            response = requests.post(
                f"{admin_url}/console/realms/my-app/users",
                headers=headers,
                json=user,
                verify=False
            )
            
            if response.status_code == 201:
                print(f"✅ User '{user['username']}' created successfully")
            else:
                print(f"❌ Failed to create user '{user['username']}': {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error creating user '{user['username']}': {e}")

if __name__ == "__main__":
    setup_keycloak()