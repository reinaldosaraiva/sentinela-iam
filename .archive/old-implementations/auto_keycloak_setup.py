#!/usr/bin/env python3
"""
Automated Keycloak Setup using REST API
"""

import requests
import time
import json
from requests.auth import HTTPBasicAuth

class KeycloakSetup:
    def __init__(self):
        self.base_url = "http://localhost:8081"
        self.admin_url = f"{self.base_url}/admin"
        self.realm_url = f"{self.base_url}/realms"
        self.admin_token = None
        self.session = requests.Session()
        
    def get_admin_token(self):
        """Get admin token for API access"""
        print("🔑 Getting admin token...")
        
        token_data = {
            "client_id": "admin-cli",
            "username": "admin",
            "password": "admin123",
            "grant_type": "password"
        }
        
        response = requests.post(
            f"{self.realm_url}/master/protocol/openid-connect/token",
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            self.admin_token = token_data.get("access_token")
            self.session.headers.update({"Authorization": f"Bearer {self.admin_token}"})
            print("✅ Admin token obtained successfully")
            return True
        else:
            print(f"❌ Failed to get admin token: {response.status_code} - {response.text}")
            return False
    
    def wait_for_keycloak(self):
        """Wait for Keycloak to be ready"""
        print("⏳ Waiting for Keycloak to be ready...")
        for i in range(30):
            try:
                response = requests.get(f"{self.realm_url}/master/.well-known/openid-configuration", timeout=5)
                if response.status_code == 200:
                    print("✅ Keycloak is ready!")
                    return self.get_admin_token()
            except:
                pass
            time.sleep(2)
            print(f"   Attempt {i+1}/30...")
        
        print("❌ Keycloak not ready after 60 seconds")
        return False
    
    def create_realm(self):
        """Create the my-app realm"""
        print("🏗️  Creating realm 'my-app'...")
        
        realm_data = {
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
        
        response = self.session.post(
            f"{self.admin_url}/realms",
            json=realm_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [201, 204, 409]:  # Created or No Content or Already Exists
            print("✅ Realm 'my-app' created successfully")
            return True
        else:
            print(f"❌ Failed to create realm: {response.status_code} - {response.text}")
            return False
    
    def create_client(self):
        """Create the sentinela-api client"""
        print("🔐 Creating client 'sentinela-api'...")
        
        client_data = {
            "clientId": "sentinela-api",
            "name": "Sentinela API Client",
            "description": "Client for Sentinela API services",
            "enabled": True,
            "clientAuthenticatorType": "client-secret",
            "secret": "sentinela-secret",
            "redirectUris": ["http://localhost:8000/*", "http://localhost:8001/*"],
            "webOrigins": ["http://localhost:8000", "http://localhost:8001"],
            "protocol": "openid-connect",
            "publicClient": False,
            "standardFlowEnabled": True,
            "directAccessGrantsEnabled": True,
            "serviceAccountsEnabled": True,
            "authorizationServicesEnabled": True,
            "fullScopeAllowed": False
        }
        
        response = self.session.post(
            f"{self.admin_url}/realms/my-app/clients",
            json=client_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [201, 204]:
            print("✅ Client 'sentinela-api' created successfully")
            return True
        else:
            print(f"❌ Failed to create client: {response.status_code} - {response.text}")
            return False
    
    def create_users(self):
        """Create users"""
        print("👥 Creating users...")
        
        users = [
            {
                "username": "alice",
                "email": "alice@company.com",
                "firstName": "Alice",
                "lastName": "Smith",
                "enabled": True,
                "credentials": [{"type": "password", "value": "alice123", "temporary": False}],
                "groups": ["employees"]
            },
            {
                "username": "bob", 
                "email": "bob@company.com",
                "firstName": "Bob",
                "lastName": "Johnson",
                "enabled": True,
                "credentials": [{"type": "password", "value": "bob123", "temporary": False}],
                "groups": ["employees"]
            },
            {
                "username": "admin",
                "email": "admin@company.com", 
                "firstName": "Admin",
                "lastName": "User",
                "enabled": True,
                "credentials": [{"type": "password", "value": "admin123", "temporary": False}],
                "groups": ["managers", "employees"]
            }
        ]
        
        for user in users:
            # Create user
            user_data = {
                "username": user["username"],
                "email": user["email"],
                "firstName": user["firstName"],
                "lastName": user["lastName"],
                "enabled": True
            }
            
            response = self.session.post(
                f"{self.admin_url}/realms/my-app/users",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [201, 204]:
                print(f"✅ User '{user['username']}' created")
                
                # Get user ID
                user_response = self.session.get(
                    f"{self.admin_url}/realms/my-app/users?username={user['username']}"
                )
                if user_response.status_code == 200:
                    users_list = user_response.json()
                    if users_list:
                        user_id = users_list[0]["id"]
                        
                        # Set password
                        password_data = {
                            "type": "password",
                            "value": user["credentials"][0]["value"],
                            "temporary": False
                        }
                        
                        password_response = self.session.put(
                            f"{self.admin_url}/realms/my-app/users/{user_id}/reset-password",
                            json=password_data,
                            headers={"Content-Type": "application/json"}
                        )
                        
                        if password_response.status_code in [201, 204]:
                            print(f"✅ Password set for '{user['username']}'")
                        else:
                            print(f"❌ Failed to set password for '{user['username']}': {password_response.status_code}")
                
            else:
                print(f"❌ Failed to create user '{user['username']}': {response.status_code}")
    
    def create_groups(self):
        """Create groups"""
        print("🏢 Creating groups...")
        
        groups = [
            {"name": "employees"},
            {"name": "managers"}
        ]
        
        group_ids = {}
        
        for group in groups:
            response = self.session.post(
                f"{self.admin_url}/realms/my-app/groups",
                json=group,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [201, 204]:
                print(f"✅ Group '{group['name']}' created")
                
                # Get group ID
                groups_response = self.session.get(
                    f"{self.admin_url}/realms/my-app/groups?search={group['name']}"
                )
                if groups_response.status_code == 200:
                    groups_list = groups_response.json()
                    for g in groups_list:
                        if g["name"] == group["name"]:
                            group_ids[group["name"]] = g["id"]
                            break
            else:
                print(f"❌ Failed to create group '{group['name']}': {response.status_code}")
        
        return group_ids
    
    def assign_users_to_groups(self, group_ids):
        """Assign users to groups"""
        print("🔗 Assigning users to groups...")
        
        # Get all users
        users_response = self.session.get(f"{self.admin_url}/realms/my-app/users")
        if users_response.status_code != 200:
            print("❌ Failed to get users")
            return
        
        users = users_response.json()
        user_assignments = {
            "alice": ["employees"],
            "bob": ["employees"], 
            "admin": ["managers", "employees"]
        }
        
        for user in users:
            username = user["username"]
            if username in user_assignments:
                user_id = user["id"]
                
                for group_name in user_assignments[username]:
                    if group_name in group_ids:
                        group_id = group_ids[group_name]
                        
                        response = self.session.put(
                            f"{self.admin_url}/realms/my-app/users/{user_id}/groups/{group_id}"
                        )
                        
                        if response.status_code in [201, 204]:
                            print(f"✅ {username} added to {group_name}")
                        else:
                            print(f"❌ Failed to add {username} to {group_name}: {response.status_code}")
    
    def test_setup(self):
        """Test the complete setup"""
        print("\n🧪 Testing Keycloak Setup")
        print("=" * 50)
        
        # Test realm configuration
        try:
            response = requests.get(f"{self.realm_url}/my-app/.well-known/openid-configuration", timeout=5)
            
            if response.status_code == 200:
                config = response.json()
                print("✅ Realm 'my-app' is accessible")
                print(f"   Issuer: {config.get('issuer', 'N/A')}")
                print(f"   Token endpoint: {config.get('token_endpoint', 'N/A')}")
                
                # Test user authentication
                self.test_user_auth(config.get('token_endpoint'))
                
            else:
                print(f"❌ Realm 'my-app' not accessible: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing realm: {e}")
    
    def test_user_auth(self, token_endpoint):
        """Test user authentication"""
        print("\n🔐 Testing User Authentication")
        print("-" * 30)
        
        users = [
            {"username": "alice", "password": "alice123"},
            {"username": "bob", "password": "bob123"},
            {"username": "admin", "password": "admin123"}
        ]
        
        for user in users:
            try:
                auth_data = {
                    "client_id": "sentinela-api",
                    "client_secret": "sentinela-secret",
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
                    
                    # Store token for later use
                    with open(f"{user['username']}_token.txt", "w") as f:
                        f.write(token_data.get('access_token', ''))
                    
                else:
                    error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                    print(f"❌ {user['username']}: Authentication failed")
                    print(f"   Error: {error_data}")
                    
            except Exception as e:
                print(f"❌ {user['username']}: Error - {e}")
    
    def run_complete_setup(self):
        """Run the complete setup process"""
        print("🚀 Starting Automated Keycloak Setup")
        print("=" * 50)
        
        if not self.wait_for_keycloak():
            return False
        
        if not self.create_realm():
            return False
            
        if not self.create_client():
            return False
        
        group_ids = self.create_groups()
        
        self.create_users()
        
        if group_ids:
            self.assign_users_to_groups(group_ids)
        
        # Wait a bit for everything to settle
        time.sleep(3)
        
        self.test_setup()
        
        print("\n🎉 Keycloak Setup Complete!")
        print("=" * 50)
        print("📋 Summary:")
        print("   ✅ Realm: my-app")
        print("   ✅ Client: sentinela-api (secret: sentinela-secret)")
        print("   ✅ Users: alice, bob, admin")
        print("   ✅ Groups: employees, managers")
        print("   ✅ Tokens saved as: alice_token.txt, bob_token.txt, admin_token.txt")
        
        print("\n🔗 URLs:")
        print(f"   Admin Console: {self.admin_url}")
        print(f"   Realm Config: {self.realm_url}/my-app/.well-known/openid-configuration")
        
        return True

if __name__ == "__main__":
    setup = KeycloakSetup()
    setup.run_complete_setup()