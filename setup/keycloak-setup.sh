#!/bin/bash

# Keycloak Setup Script for Sentinela MVP
# This script configures Keycloak realm, client, and test user

set -e

KEYCLOAK_URL="http://localhost:8081"
ADMIN_USER="admin"
ADMIN_PASSWORD="admin"
REALM_NAME="sentinela"
CLIENT_ID="sentinela-api"
CLIENT_SECRET="sentinela-secret"
TEST_USER="alice"
TEST_USER_PASSWORD="alice123"

echo "🔧 Setting up Keycloak for Sentinela MVP..."

# Wait for Keycloak to be ready
echo "⏳ Waiting for Keycloak to be ready..."
until curl -s "$KEYCLOAK_URL/health/ready" > /dev/null; do
    echo "Waiting for Keycloak..."
    sleep 5
done

echo "✅ Keycloak is ready!"

# Get admin token
echo "🔑 Getting admin token..."
ADMIN_TOKEN=$(curl -s -X POST "$KEYCLOAK_URL/realms/master/protocol/openid-connect/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$ADMIN_USER&password=$ADMIN_PASSWORD&grant_type=password&client_id=admin-cli" | \
    jq -r '.access_token')

if [ "$ADMIN_TOKEN" == "null" ]; then
    echo "❌ Failed to get admin token"
    exit 1
fi

echo "✅ Admin token obtained"

# Create realm
echo "🌍 Creating realm: $REALM_NAME"
curl -s -X POST "$KEYCLOAK_URL/admin/realms" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "realm": "'$REALM_NAME'",
        "enabled": true,
        "displayName": "Sentinela IAM",
        "registrationAllowed": false,
        "loginWithEmailAllowed": true,
        "duplicateEmailsAllowed": false,
        "resetPasswordAllowed": true,
        "editUsernameAllowed": true,
        "bruteForceProtected": true
    }' > /dev/null

echo "✅ Realm created"

# Create client
echo "🔗 Creating client: $CLIENT_ID"
curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/clients" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "clientId": "'$CLIENT_ID'",
        "name": "Sentinela API",
        "description": "API client for Sentinela authorization system",
        "enabled": true,
        "clientAuthenticatorType": "client-secret",
        "secret": "'$CLIENT_SECRET'",
        "redirectUris": ["http://localhost:3000/*", "http://localhost:8000/*"],
        "webOrigins": ["http://localhost:3000", "http://localhost:8000"],
        "publicClient": false,
        "protocol": "openid-connect",
        "standardFlowEnabled": true,
        "directAccessGrantsEnabled": true,
        "serviceAccountsEnabled": true,
        "authorizationServicesEnabled": false,
        "fullScopeAllowed": true
    }' > /dev/null

echo "✅ Client created"

# Create test user 'alice'
echo "👤 Creating test user: $TEST_USER"
curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/users" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "'$TEST_USER'",
        "firstName": "Alice",
        "lastName": "Smith",
        "email": "'$TEST_USER'@sentinela.local",
        "enabled": true,
        "emailVerified": true,
        "credentials": [{
            "type": "password",
            "value": "'$TEST_USER_PASSWORD'",
            "temporary": false
        }],
        "attributes": {
            "department": ["finance"],
            "clearance_level": ["confidential"],
            "employee_id": ["EMP001"]
        }
    }' > /dev/null

echo "✅ Test user created"

# Get user ID to assign roles
USER_ID=$(curl -s -X GET "$KEYCLOAK_URL/admin/realms/$REALM_NAME/users?username=$TEST_USER" \
    -H "Authorization: Bearer $ADMIN_TOKEN" | \
    jq -r '.[0].id')

# Create roles
echo "🔐 Creating roles..."

# Create finance role
curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/roles" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "finance",
        "description": "Finance department access"
    }' > /dev/null

# Create document_reader role
curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/roles" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "document_reader",
        "description": "Can read documents"
    }' > /dev/null

# Create document_writer role
curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/roles" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "document_writer",
        "description": "Can write documents"
    }' > /dev/null

echo "✅ Roles created"

# Assign roles to user
echo "👥 Assigning roles to user..."

# Assign finance role
curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/users/$USER_ID/role-mappings/realm" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '[{
        "id": "'$(curl -s -X GET "$KEYCLOAK_URL/admin/realms/$REALM_NAME/roles/finance" \
            -H "Authorization: Bearer $ADMIN_TOKEN" | jq -r '.id')'",
        "name": "finance",
        "description": "Finance department access"
    }]'

# Assign document_reader role
curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/users/$USER_ID/role-mappings/realm" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '[{
        "id": "'$(curl -s -X GET "$KEYCLOAK_URL/admin/realms/$REALM_NAME/roles/document_reader" \
            -H "Authorization: Bearer $ADMIN_TOKEN" | jq -r '.id')'",
        "name": "document_reader",
        "description": "Can read documents"
    }]'

# Assign document_writer role
curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/users/$USER_ID/role-mappings/realm" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '[{
        "id": "'$(curl -s -X GET "$KEYCLOAK_URL/admin/realms/$REALM_NAME/roles/document_writer" \
            -H "Authorization: Bearer $ADMIN_TOKEN" | jq -r '.id')'",
        "name": "document_writer",
        "description": "Can write documents"
    }]'

echo "✅ Roles assigned to user"

# Get realm public key for JWT validation
echo "🔑 Getting realm public key..."
REALM_PUBLIC_KEY=$(curl -s -X GET "$KEYCLOAK_URL/admin/realms/$REALM_NAME/keys" \
    -H "Authorization: Bearer $ADMIN_TOKEN" | \
    jq -r '.keys[] | select(.type=="RSA") | .publicKey')

echo "✅ Setup completed successfully!"
echo ""
echo "📋 Configuration Summary:"
echo "   Realm: $REALM_NAME"
echo "   Client ID: $CLIENT_ID"
echo "   Client Secret: $CLIENT_SECRET"
echo "   Test User: $TEST_USER"
echo "   Test Password: $TEST_USER_PASSWORD"
echo "   Keycloak URL: $KEYCLOAK_URL"
echo ""
echo "🔗 Useful URLs:"
echo "   Admin Console: $KEYCLOAK_URL/admin"
echo "   Account Console: $KEYCLOAK_URL/realms/$REALM_NAME/account"
echo "   Token Endpoint: $KEYCLOAK_URL/realms/$REALM_NAME/protocol/openid-connect/token"
echo ""
echo "🧪 Test Commands:"
echo "   # Get user token:"
echo "   curl -X POST \"$KEYCLOAK_URL/realms/$REALM_NAME/protocol/openid-connect/token\" \\"
echo "     -H \"Content-Type: application/x-www-form-urlencoded\" \\"
echo "     -d \"username=$TEST_USER&password=$TEST_USER_PASSWORD&grant_type=password&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET\""
echo ""
echo "   # Test API with token:"
echo "   curl -H \"Authorization: Bearer <TOKEN>\" http://localhost:8000/documentos/"