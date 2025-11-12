#!/usr/bin/env python3
"""
Working Policy API using Flask
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Simple in-memory database for MVP
policies_db = []
policy_id_counter = 1

@app.route('/health/', methods=['GET'])
def health_check():
    """Basic health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": {
            "database": "healthy",
            "opal": "not_initialized",
            "keycloak": "not_initialized"
        }
    })

@app.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """Detailed health check including external services"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": {
            "database": "healthy",
            "opal": "not_initialized",
            "keycloak": "not_initialized"
        }
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        "message": "Sentinela Policy API",
        "version": "1.0.0",
        "status": "running"
    })

@app.route('/info', methods=['GET'])
def info():
    """API information endpoint"""
    return jsonify({
        "name": "Sentinela Policy API",
        "version": "1.0.0",
        "description": "Policy Management Service for Authorization Control Plane",
        "services": {
            "opal_server": "http://opal_publisher:7002",
            "keycloak_url": "http://keycloak:8080",
            "keycloak_realm": "my-app"
        }
    })

@app.route('/policies/', methods=['GET'])
def list_policies():
    """List all policies"""
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 100))
    
    return jsonify(policies_db[skip:skip+limit])

@app.route('/policies/<int:policy_id>', methods=['GET'])
def get_policy(policy_id):
    """Get a specific policy by ID"""
    for policy in policies_db:
        if policy["id"] == policy_id:
            return jsonify(policy)
    
    return jsonify({"error": "Policy not found"}), 404

@app.route('/policies/', methods=['POST'])
def create_policy():
    """Create a new policy"""
    global policy_id_counter
    
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400
    
    policy_data = request.get_json()
    
    new_policy = {
        "id": policy_id_counter,
        "name": policy_data.get("name"),
        "description": policy_data.get("description"),
        "content": policy_data.get("content"),
        "version": "1.0.0",
        "status": "draft",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    policies_db.append(new_policy)
    policy_id_counter += 1
    
    logger.info(f"Policy {new_policy['id']} created successfully")
    return jsonify(new_policy), 201

@app.route('/policies/<int:policy_id>', methods=['PUT'])
def update_policy(policy_id):
    """Update an existing policy"""
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400
    
    policy_data = request.get_json()
    
    for i, policy in enumerate(policies_db):
        if policy["id"] == policy_id:
            # Update policy fields
            for field, value in policy_data.items():
                if value is not None:
                    policy[field] = value
            
            policy["updated_at"] = datetime.utcnow().isoformat() + "Z"
            
            # Increment version if content changed
            if "content" in policy_data:
                current_version = policy["version"].split(".")
                current_version[-1] = str(int(current_version[-1]) + 1)
                policy["version"] = ".".join(current_version)
            
            logger.info(f"Policy {policy_id} updated successfully")
            return jsonify(policy)
    
    return jsonify({"error": "Policy not found"}), 404

@app.route('/policies/<int:policy_id>', methods=['DELETE'])
def delete_policy(policy_id):
    """Delete a policy"""
    for i, policy in enumerate(policies_db):
        if policy["id"] == policy_id:
            policies_db.pop(i)
            logger.info(f"Policy {policy_id} deleted successfully")
            return "", 204
    
    return jsonify({"error": "Policy not found"}), 404

@app.route('/policies/<int:policy_id>/publish', methods=['POST'])
def publish_policy(policy_id):
    """Publish a policy (make it active)"""
    for policy in policies_db:
        if policy["id"] == policy_id:
            policy["status"] = "active"
            policy["updated_at"] = datetime.utcnow().isoformat() + "Z"
            logger.info(f"Policy {policy_id} published successfully")
            return jsonify(policy)
    
    return jsonify({"error": "Policy not found"}), 404

if __name__ == "__main__":
    logger.info("Starting Sentinela Policy API...")
    app.run(host="0.0.0.0", port=8000, debug=True)