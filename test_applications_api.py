"""
Test script for Applications API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001/api/v1/applications"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"🔵 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")


def main():
    print("🚀 Testing Applications API Endpoints\n")

    # Test 1: Create Application
    print("\n📋 Test 1: Create Application")
    application_data = {
        "name": "Test API Client",
        "slug": "test-api-client",
        "description": "Testing application for API endpoints",
        "status": "active",
        "environment": "development"
    }
    response = requests.post(BASE_URL, json=application_data)
    print_response("POST /applications", response)

    if response.status_code == 201:
        app_id = response.json()["id"]
        print(f"\n✅ Application created with ID: {app_id}")
    else:
        print("\n❌ Failed to create application")
        return

    # Test 2: List Applications
    print("\n📋 Test 2: List Applications")
    response = requests.get(BASE_URL)
    print_response("GET /applications", response)

    # Test 3: Get Single Application
    print("\n📋 Test 3: Get Application by ID")
    response = requests.get(f"{BASE_URL}/{app_id}")
    print_response(f"GET /applications/{app_id}", response)

    # Test 4: Create API Key
    print("\n📋 Test 4: Create API Key")
    api_key_data = {
        "name": "Production API Key",
        "application_id": app_id,
        "expires_at": (datetime.now() + timedelta(days=90)).isoformat()
    }
    response = requests.post(f"{BASE_URL}/{app_id}/api-keys", json=api_key_data)
    print_response("POST /applications/{id}/api-keys", response)

    if response.status_code == 201:
        api_key_id = response.json()["id"]
        plain_key = response.json()["plain_key"]
        print(f"\n✅ API Key created!")
        print(f"🔑 Plain Key (SAVE THIS): {plain_key}")
        print(f"⚠️  This is the ONLY time you'll see the plain key!")
    else:
        print("\n❌ Failed to create API key")
        return

    # Test 5: List API Keys
    print("\n📋 Test 5: List API Keys")
    response = requests.get(f"{BASE_URL}/{app_id}/api-keys")
    print_response(f"GET /applications/{app_id}/api-keys", response)

    # Test 6: Deactivate API Key
    print("\n📋 Test 6: Deactivate API Key")
    response = requests.patch(f"{BASE_URL}/{app_id}/api-keys/{api_key_id}/deactivate")
    print_response(f"PATCH /applications/{app_id}/api-keys/{api_key_id}/deactivate", response)

    # Test 7: Update Application
    print("\n📋 Test 7: Update Application")
    update_data = {
        "status": "paused",
        "description": "Updated description for testing"
    }
    response = requests.put(f"{BASE_URL}/{app_id}", json=update_data)
    print_response(f"PUT /applications/{app_id}", response)

    # Test 8: List with filters
    print("\n📋 Test 8: List Applications with Filters")
    response = requests.get(f"{BASE_URL}?status=active&environment=development")
    print_response("GET /applications?status=active&environment=development", response)

    # Test 9: Delete API Key
    print("\n📋 Test 9: Delete API Key")
    response = requests.delete(f"{BASE_URL}/{app_id}/api-keys/{api_key_id}")
    print_response(f"DELETE /applications/{app_id}/api-keys/{api_key_id}", response)
    if response.status_code == 204:
        print("✅ API Key deleted successfully")

    # Test 10: Delete Application
    print("\n📋 Test 10: Delete Application")
    response = requests.delete(f"{BASE_URL}/{app_id}")
    print_response(f"DELETE /applications/{app_id}", response)
    if response.status_code == 204:
        print("✅ Application deleted successfully")

    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server")
        print("Make sure the Policy API is running on http://localhost:8001")
        print("\nTo start the API:")
        print("  cd policy_api")
        print("  python -m uvicorn src.main:app --port 8001 --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
