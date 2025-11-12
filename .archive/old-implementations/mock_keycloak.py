#!/usr/bin/env python3
"""
Mock Keycloak Service for Development and Testing
Simulates Keycloak token endpoints for testing the authorization system
"""

from flask import Flask, jsonify, request
import jwt
import datetime
import hashlib
import os

app = Flask(__name__)

# Mock secret key for JWT signing
app.config['SECRET_KEY'] = 'mock-keycloak-secret-key'

# Mock user database
MOCK_USERS = {
    'alice': {
        'password_hash': hashlib.sha256('alice123'.encode()).hexdigest(),
        'email': 'alice@company.com',
        'groups': ['employees'],
        'attributes': {'department': 'engineering'}
    },
    'bob': {
        'password_hash': hashlib.sha256('bob123'.encode()).hexdigest(),
        'email': 'bob@company.com', 
        'groups': ['employees'],
        'attributes': {'department': 'marketing'}
    },
    'admin': {
        'password_hash': hashlib.sha256('admin123'.encode()).hexdigest(),
        'email': 'admin@company.com',
        'groups': ['managers', 'employees'],
        'attributes': {'department': 'it', 'role': 'administrator'}
    }
}

# Mock client configuration
MOCK_CLIENTS = {
    'sentinela-api': {
        'secret': 'sentinela-secret',
        'redirect_uris': ['http://localhost:8000/*', 'http://localhost:8001/*']
    }
}

def generate_jwt_token(username, user_info):
    """Generate a JWT token for a user"""
    now = datetime.datetime.utcnow()
    
    payload = {
        'sub': username,
        'preferred_username': username,
        'email': user_info['email'],
        'groups': user_info['groups'],
        'attributes': user_info['attributes'],
        'iss': 'http://localhost:8081/realms/my-app',
        'aud': 'sentinela-api',
        'exp': now + datetime.timedelta(hours=1),
        'iat': now,
        'typ': 'Bearer',
        'azp': 'sentinela-api',
        'realm_access': {'roles': user_info['groups']},
        'resource_access': {'sentinela-api': {'roles': ['access']}}
    }
    
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

@app.route('/realms/my-app/.well-known/openid-configuration')
def openid_configuration():
    """OpenID Connect configuration endpoint"""
    return jsonify({
        'issuer': 'http://localhost:8081/realms/my-app',
        'authorization_endpoint': 'http://localhost:8081/realms/my-app/protocol/openid-connect/auth',
        'token_endpoint': 'http://localhost:8081/realms/my-app/protocol/openid-connect/token',
        'userinfo_endpoint': 'http://localhost:8081/realms/my-app/protocol/openid-connect/userinfo',
        'jwks_uri': 'http://localhost:8081/realms/my-app/protocol/openid-connect/certs',
        'end_session_endpoint': 'http://localhost:8081/realms/my-app/protocol/openid-connect/logout',
        'response_types_supported': ['code', 'id_token', 'token id_token'],
        'grant_types_supported': ['authorization_code', 'implicit', 'refresh_token', 'password', 'client_credentials'],
        'subject_types_supported': ['public'],
        'id_token_signing_alg_values_supported': ['RS256'],
        'token_endpoint_auth_methods_supported': ['client_secret_basic', 'client_secret_post']
    })

@app.route('/realms/my-app/protocol/openid-connect/token', methods=['POST'])
def token_endpoint():
    """Token endpoint for authentication"""
    
    # Get form data
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    grant_type = request.form.get('grant_type')
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Validate client
    if client_id not in MOCK_CLIENTS:
        return jsonify({'error': 'invalid_client'}), 401
    
    if MOCK_CLIENTS[client_id]['secret'] != client_secret:
        return jsonify({'error': 'invalid_client'}), 401
    
    # Handle different grant types
    if grant_type == 'password':
        # Validate user credentials
        if username not in MOCK_USERS:
            return jsonify({'error': 'invalid_grant'}), 400
        
        if not password:
            return jsonify({'error': 'invalid_grant'}), 400
        
        user = MOCK_USERS[username]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if user['password_hash'] != password_hash:
            return jsonify({'error': 'invalid_grant'}), 400
        
        # Generate tokens
        access_token = generate_jwt_token(username, user)
        refresh_token = generate_jwt_token(username + '_refresh', user)
        
        return jsonify({
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 3600,
            'refresh_token': refresh_token,
            'scope': 'openid profile email',
            'id_token': access_token  # Using same token for simplicity
        })
    
    elif grant_type == 'client_credentials':
        # Service account flow
        service_account_info = {
            'email': f'{client_id}@service-account.local',
            'groups': ['service-accounts'],
            'attributes': {'client_id': client_id}
        }
        
        access_token = generate_jwt_token(client_id, service_account_info)
        
        return jsonify({
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 3600,
            'scope': 'openid profile email'
        })
    
    else:
        return jsonify({'error': 'unsupported_grant_type'}), 400

@app.route('/realms/my-app/protocol/openid-connect/userinfo')
def userinfo_endpoint():
    """Userinfo endpoint"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'invalid_token'}), 401
    
    token = auth_header[7:]  # Remove 'Bearer ' prefix
    
    try:
        # Decode and validate token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload.get('sub')
        
        if username in MOCK_USERS:
            user = MOCK_USERS[username]
            return jsonify({
                'sub': username,
                'preferred_username': username,
                'email': user['email'],
                'groups': user['groups'],
                'attributes': user['attributes']
            })
        else:
            # Service account
            return jsonify({
                'sub': username,
                'preferred_username': username,
                'email': f'{username}@service-account.local',
                'groups': ['service-accounts'],
                'client_id': username
            })
            
    except jwt.InvalidTokenError:
        return jsonify({'error': 'invalid_token'}), 401

@app.route('/realms/my-app/protocol/openid-connect/logout', methods=['POST'])
def logout_endpoint():
    """Logout endpoint"""
    return jsonify({})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'mock-keycloak',
        'timestamp': datetime.datetime.utcnow().isoformat()
    })

@app.route('/admin/realms/my-app/users')
def admin_list_users():
    """Admin endpoint to list users"""
    users = []
    for username, user_data in MOCK_USERS.items():
        users.append({
            'id': hashlib.sha256(username.encode() if username else b'').hexdigest(),
            'username': username,
            'email': user_data['email'],
            'enabled': True,
            'groups': user_data['groups']
        })
    
    return jsonify(users)

@app.route('/admin/realms/my-app/clients')
def admin_list_clients():
    """Admin endpoint to list clients"""
    clients = []
    for client_id, client_data in MOCK_CLIENTS.items():
        clients.append({
            'id': hashlib.sha256(client_id.encode() if client_id else b'').hexdigest(),
            'clientId': client_id,
            'enabled': True,
            'clientAuthenticatorType': 'client-secret'
        })
    
    return jsonify(clients)

if __name__ == '__main__':
    print("🚀 Starting Mock Keycloak Service")
    print("=" * 50)
    print("📍 Endpoints:")
    print("   Token: http://localhost:8081/realms/my-app/protocol/openid-connect/token")
    print("   Config: http://localhost:8081/realms/my-app/.well-known/openid-configuration")
    print("   Health: http://localhost:8081/health")
    print("   Admin Users: http://localhost:8081/admin/realms/my-app/users")
    print()
    print("👥 Test Users:")
    print("   alice:alice123 (employees)")
    print("   bob:bob123 (employees)")
    print("   admin:admin123 (managers, employees)")
    print()
    print("🔐 Client Config:")
    print("   client_id: sentinela-api")
    print("   client_secret: sentinela-secret")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8081, debug=True)