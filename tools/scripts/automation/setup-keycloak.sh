#!/bin/bash

# Keycloak Setup Script for Sentinela MVP
# This script configures Keycloak with the required realm, user, and client

set -e

KEYCLOAK_URL=${KEYCLOAK_URL:-"http://localhost:8080"}
ADMIN_USER=${KEYCLOAK_ADMIN:-"admin"}
ADMIN_PASSWORD=${KEYCLOAK_ADMIN_PASSWORD:-"admin123"}

REALM_NAME="my-app"
CLIENT_ID="business-api"
USER_NAME="alice"
USER_PASSWORD="password123"

echo "🔧 Setting up Keycloak for Sentinela MVP..."

# Wait for Keycloak to be ready
echo "⏳ Waiting for Keycloak to be ready..."
until curl -f "$KEYCLOAK_URL/health/ready" &> /dev/null; do
    echo "   Keycloak not ready yet, waiting..."
    sleep 5
done

echo "✅ Keycloak is ready!"

# Get admin token
echo "🔑 Getting admin token..."
ADMIN_TOKEN=$(curl -s -X POST "$KEYCLOAK_URL/realms/master/protocol/openid-connect/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$ADMIN_USER" \
    -d "password=$ADMIN_PASSWORD" \
    -d "grant_type=password" \
    -d "client_id=admin-cli" | jq -r '.access_token')

if [ "$ADMIN_TOKEN" == "null" ]; then
    echo "❌ Failed to get admin token"
    exit 1
fi

echo "✅ Admin token obtained!"

# Create realm
echo "🏗️  Creating realm '$REALM_NAME'..."
curl -s -X POST "$KEYCLOAK_URL/admin/realms" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "realm": "'$REALM_NAME'",
        "enabled": true,
        "displayName": "Sentinela MVP Application",
        "registrationAllowed": false,
        "loginWithEmailAllowed": false,
        "duplicateEmailsAllowed": false,
        "resetPasswordAllowed": true,
        "editUsernameAllowed": true,
        "bruteForceProtected": true
    }' > /dev/null

echo "✅ Realm created!"

# Create client for Business API
echo "🔗 Creating client '$CLIENT_ID'..."
curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/clients" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "clientId": "'$CLIENT_ID'",
        "name": "Business API Service",
        "description": "Client for Business API Service",
        "enabled": true,
        "clientAuthenticatorType": "client-secret",
        "secret": "business-api-secret",
        "redirectUris": ["http://localhost:8001/*"],
        "webOrigins": ["http://localhost:8001"],
        "publicClient": false,
        "protocol": "openid-connect",
        "standardFlowEnabled": true,
        "directAccessGrantsEnabled": true,
        "serviceAccountsEnabled": true,
        "authorizationServicesEnabled": false
    }' > /dev/null

echo "✅ Client created!"

# Create user group
echo "👥 Creating group 'employees'..."
GROUP_ID=$(curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/groups" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "employees",
        "path": "/employees"
    }' | jq -r '.id')

echo "✅ Group created!"

# Create user alice
echo "👤 Creating user '$USER_NAME'..."
USER_ID=$(curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM_NAME/users" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "'$USER_NAME'",
        "firstName": "Alice",
        "lastName": "Smith",
        "email": "alice@example.com",
        "enabled": true,
        "emailVerified": true,
        "credentials": [{
            "type": "password",
            "value": "'$USER_PASSWORD'",
            "temporary": false
        }]
    }' | jq -r '.id')

# Add user to group
echo "🔗 Adding user to group..."
curl -s -X PUT "$KEYCLOAK_URL/admin/realms/$REALM_NAME/users/$USER_ID/groups/$GROUP_ID" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" > /dev/null

echo "✅ User created and added to group!"

# Get realm public key
echo "🔑 Getting realm public key..."
REALM_KEYS=$(curl -s -X GET "$KEYCLOAK_URL/admin/realms/$REALM_NAME/keys" \
    -H "Authorization: Bearer $ADMIN_TOKEN")

PUBLIC_KEY=$(echo "$REALM_KEYS" | jq -r '.keys[] | select(.type=="RSA") | .publicKey')

# Save public key to file for Business API
mkdir -p ../config
echo "$PUBLIC_KEY" > ../config/keycloak-public-key.pem

echo "✅ Public key saved to config/keycloak-public-key.pem!"

echo ""
echo "🎉 Keycloak setup completed successfully!"
echo ""
echo "📋 Configuration Summary:"
echo "   Realm:           $REALM_NAME"
echo "   Client ID:       $CLIENT_ID"
echo "   User:            $USER_NAME"
echo "   Password:        $USER_PASSWORD"
echo "   Group:           employees"
echo ""
echo "🔗 Useful URLs:"
echo "   Admin Console:   $KEYCLOAK_URL/admin"
echo "   Realm Console:   $KEYCLOAK_URL/admin/master/console/#/realms/$REALM_NAME"
echo "   Account URL:     $KEYCLOAK_URL/realms/$REALM_NAME/account"
echo ""
echo "🧪 Test Token Request:"
echo "   curl -X POST \"$KEYCLOAK_URL/realms/$REALM_NAME/protocol/openid-connect/token\" \\"
echo "     -H \"Content-Type: application/x-www-form-urlencoded\" \\"
echo "     -d \"username=$USER_NAME\" \\"
echo "     -d \"password=$USER_PASSWORD\" \\"
echo "     -d \"grant_type=password\" \\"
echo "     -d \"client_id=$CLIENT_ID\""
echo ""