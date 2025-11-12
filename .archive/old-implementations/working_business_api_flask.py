#!/usr/bin/env python3
"""
Working Business API using Flask with Cedar integration
"""

import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

# Import Cedar engine directly
from final_cedar_engine import FinalCedarEngine, AuthorizationRequest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)

# Initialize Cedar Engine
cedar_engine = FinalCedarEngine()

# Load default policies
default_policies = [
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
    """,
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
    """
]

cedar_engine.load_policies(default_policies)

# Mock documents database
documents_db = [
    {
        "id": 1,
        "title": "Public Document",
        "content": "This is a public document",
        "owner": "User::\"alice\"",
        "document_type": "public",
        "classification": "public",
        "department": "General",
        "created_at": "2025-01-11T00:00:00Z",
        "updated_at": "2025-01-11T00:00:00Z"
    },
    {
        "id": 2,
        "title": "HR Policy Document",
        "content": "Internal HR policies",
        "owner": "User::\"hr_manager\"",
        "document_type": "hr",
        "classification": "internal",
        "department": "HR",
        "created_at": "2025-01-11T00:00:00Z",
        "updated_at": "2025-01-11T00:00:00Z"
    },
    {
        "id": 3,
        "title": "Secret Document",
        "content": "Confidential information",
        "owner": "User::\"admin\"",
        "document_type": "secret",
        "classification": "confidential",
        "department": "Executive",
        "created_at": "2025-01-11T00:00:00Z",
        "updated_at": "2025-01-11T00:00:00Z"
    }
]

@app.route('/health', methods=['GET'])
def health_check():
    """Basic health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": {
            "cedar_engine": "healthy",
            "policies_loaded": len(cedar_engine.policies),
            "keycloak": "not_initialized"
        }
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        "message": "Sentinela Business API",
        "version": "1.0.0",
        "status": "running"
    })

@app.route('/info', methods=['GET'])
def info():
    """API information endpoint"""
    return jsonify({
        "name": "Sentinela Business API",
        "version": "1.0.0",
        "description": "Business API with Cedar authorization engine",
        "services": {
            "cedar_engine": "operational",
            "policies_loaded": len(cedar_engine.compiled_policies),
            "keycloak_url": "http://keycloak:8080",
            "keycloak_realm": "my-app"
        }
    })

@app.route('/documents', methods=['GET'])
def list_documents():
    """List all documents (with authorization check)"""
    # Get authorization header
    auth_header = request.headers.get('Authorization', '')
    
    # Mock user info for demo
    if auth_header:
        # In real implementation, validate JWT with Keycloak
        user_info = {
            "sub": "alice",
            "email": "alice@company.com",
            "groups": ["employees"]
        }
    else:
        user_info = {
            "sub": "anonymous",
            "email": "anonymous@company.com",
            "groups": []
        }
    
    # Filter documents based on authorization
    authorized_docs = []
    
    for doc in documents_db:
        # Create authorization request
        auth_request = AuthorizationRequest(
            principal=f'User::"{user_info["sub"]}"',
            action='Action::"read"',
            resource=f'Document::"{doc["document_type"]}"',
            context={"groups": user_info["groups"]}
        )
        
        # Evaluate authorization
        result = cedar_engine.evaluate(auth_request)
        
        if result.allow:
            authorized_docs.append(doc)
            logger.info(f"Authorized {user_info['sub']} to read {doc['title']}")
        else:
            logger.info(f"Denied {user_info['sub']} access to {doc['title']}")
    
    return jsonify({
        "documents": authorized_docs,
        "user": user_info,
        "total": len(authorized_docs)
    })

@app.route('/documents/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    """Get a specific document (with authorization check)"""
    # Find document
    document = None
    for doc in documents_db:
        if doc["id"] == doc_id:
            document = doc
            break
    
    if not document:
        return jsonify({"error": "Document not found"}), 404
    
    # Get authorization header
    auth_header = request.headers.get('Authorization', '')
    
    # Mock user info for demo
    if auth_header:
        user_info = {
            "sub": "alice",
            "email": "alice@company.com",
            "groups": ["employees"]
        }
    else:
        return jsonify({"error": "Authorization required"}), 401
    
    # Create authorization request
    auth_request = AuthorizationRequest(
        principal=f'User::"{user_info["sub"]}"',
        action='Action::"read"',
        resource=f'Document::"{document["document_type"]}"',
        context={"groups": user_info["groups"]}
    )
    
    # Evaluate authorization
    result = cedar_engine.evaluate(auth_request)
    
    if result.allow:
        logger.info(f"Authorized {user_info['sub']} to read {document['title']}")
        return jsonify({
            "document": document,
            "user": user_info,
            "authorization": "allowed"
        })
    else:
        logger.info(f"Denied {user_info['sub']} access to {document['title']}")
        return jsonify({
            "error": "Access denied",
            "reason": result.reason or "Insufficient permissions"
        }), 403

@app.route('/authorize', methods=['POST'])
def authorize():
    """Authorization check endpoint"""
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['principal', 'action', 'resource']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Create authorization request
    auth_request = AuthorizationRequest(
        principal=data['principal'],
        action=data['action'],
        resource=data['resource'],
        context=data.get('context', {})
    )
    
    # Evaluate authorization
    result = cedar_engine.evaluate(auth_request)
    
    response = {
        "allow": result.allow,
        "principal": data['principal'],
        "action": data['action'],
        "resource": data['resource']
    }
    
    if result.reason:
        response["reason"] = result.reason
    
    logger.info(f"Authorization decision: {result.allow} for {data['principal']} {data['action']} {data['resource']}")
    
    return jsonify(response)

@app.route('/policies', methods=['GET'])
def list_policies():
    """List loaded policies"""
    policies_info = []
    for i, policy in enumerate(cedar_engine.compiled_policies):
        policies_info.append({
            "id": i + 1,
            "name": policy.get('name', f'policy_{i+1}'),
            "type": policy.get('type', 'unknown'),
            "conditions_count": len(policy.get('conditions', [])),
            "raw": policy.get('raw', '')
        })
    
    return jsonify({
        "policies": policies_info,
        "total": len(policies_info)
    })

@app.route('/policies/reload', methods=['POST'])
def reload_policies():
    """Reload policies (for demo purposes)"""
    cedar_engine.load_policies(default_policies)
    logger.info("Policies reloaded")
    
    return jsonify({
        "message": "Policies reloaded successfully",
        "policies_loaded": len(cedar_engine.policies)
    })

if __name__ == "__main__":
    logger.info("Starting Sentinela Business API...")
    logger.info(f"Loaded {len(cedar_engine.policies)} policies")
    app.run(host="0.0.0.0", port=8002, debug=True)