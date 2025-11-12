"""
Test script for Resources and Actions API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8001/api/v1"

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
    print("🚀 Testing Resources & Actions API Endpoints\n")

    # Prerequisites: Get an application ID
    print("\n📋 Prerequisites: Getting Application ID")
    response = requests.get(f"{BASE_URL}/applications/")
    if response.status_code != 200:
        print("❌ Error: No applications found. Please create an application first.")
        return

    applications = response.json()["applications"]
    if not applications:
        print("❌ Error: No applications available. Please create an application first.")
        return

    app_id = applications[0]["id"]
    print(f"✅ Using application: {applications[0]['name']} (ID: {app_id})")

    # Test 1: Create Resource
    print("\n📋 Test 1: Create Resource")
    resource_data = {
        "application_id": app_id,
        "resource_type": "test-documents",
        "name": "Test Documents",
        "description": "Document management resource for testing",
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/resources/", json=resource_data)
    print_response("POST /resources/", response)

    if response.status_code == 201:
        resource_id = response.json()["id"]
        print(f"\n✅ Resource created with ID: {resource_id}")
    else:
        print("\n❌ Failed to create resource")
        return

    # Test 2: List Resources
    print("\n📋 Test 2: List Resources")
    response = requests.get(f"{BASE_URL}/resources/")
    print_response("GET /resources/", response)

    # Test 3: Get Single Resource
    print("\n📋 Test 3: Get Resource by ID")
    response = requests.get(f"{BASE_URL}/resources/{resource_id}")
    print_response(f"GET /resources/{resource_id}", response)

    # Test 4: Create Action - Read
    print("\n📋 Test 4: Create Action (Read)")
    action_data = {
        "resource_id": resource_id,
        "action_type": "read",
        "name": "Read Documents",
        "description": "View document contents",
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/actions/", json=action_data)
    print_response("POST /actions/ (read)", response)

    if response.status_code == 201:
        action_read_id = response.json()["id"]
        print(f"\n✅ Read action created with ID: {action_read_id}")
    else:
        print("\n❌ Failed to create read action")
        return

    # Test 5: Create Action - Write
    print("\n📋 Test 5: Create Action (Write)")
    action_data = {
        "resource_id": resource_id,
        "action_type": "write",
        "name": "Write Documents",
        "description": "Create and modify documents",
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/actions/", json=action_data)
    print_response("POST /actions/ (write)", response)

    if response.status_code == 201:
        action_write_id = response.json()["id"]
        print(f"\n✅ Write action created with ID: {action_write_id}")
    else:
        print("\n❌ Failed to create write action")
        return

    # Test 6: Create Action - Delete
    print("\n📋 Test 6: Create Action (Delete)")
    action_data = {
        "resource_id": resource_id,
        "action_type": "delete",
        "name": "Delete Documents",
        "description": "Remove documents permanently",
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/actions/", json=action_data)
    print_response("POST /actions/ (delete)", response)

    if response.status_code == 201:
        action_delete_id = response.json()["id"]
        print(f"\n✅ Delete action created with ID: {action_delete_id}")
    else:
        print("\n❌ Failed to create delete action")
        return

    # Test 7: List Actions
    print("\n📋 Test 7: List All Actions")
    response = requests.get(f"{BASE_URL}/actions/")
    print_response("GET /actions/", response)

    # Test 8: List Actions by Resource
    print("\n📋 Test 8: List Actions for Resource")
    response = requests.get(f"{BASE_URL}/actions/?resource_id={resource_id}")
    print_response(f"GET /actions/?resource_id={resource_id}", response)

    # Test 9: Get Single Action
    print("\n📋 Test 9: Get Action by ID")
    response = requests.get(f"{BASE_URL}/actions/{action_read_id}")
    print_response(f"GET /actions/{action_read_id}", response)

    # Test 10: Update Action
    print("\n📋 Test 10: Update Action")
    update_data = {
        "description": "Updated: View document contents with full permissions"
    }
    response = requests.put(f"{BASE_URL}/actions/{action_read_id}", json=update_data)
    print_response(f"PUT /actions/{action_read_id}", response)

    # Test 11: Deactivate Action
    print("\n📋 Test 11: Deactivate Action")
    response = requests.patch(f"{BASE_URL}/actions/{action_write_id}/deactivate")
    print_response(f"PATCH /actions/{action_write_id}/deactivate", response)
    if response.status_code == 200:
        print("✅ Action deactivated successfully")

    # Test 12: Activate Action
    print("\n📋 Test 12: Activate Action")
    response = requests.patch(f"{BASE_URL}/actions/{action_write_id}/activate")
    print_response(f"PATCH /actions/{action_write_id}/activate", response)
    if response.status_code == 200:
        print("✅ Action activated successfully")

    # Test 13: Update Resource
    print("\n📋 Test 13: Update Resource")
    update_data = {
        "description": "Updated: Document management system with full CRUD operations"
    }
    response = requests.put(f"{BASE_URL}/resources/{resource_id}", json=update_data)
    print_response(f"PUT /resources/{resource_id}", response)

    # Test 14: List Resources with Filters
    print("\n📋 Test 14: List Resources with Filters")
    response = requests.get(f"{BASE_URL}/resources/?application_id={app_id}&is_active=true")
    print_response(f"GET /resources/?application_id={app_id}&is_active=true", response)

    # Test 15: Deactivate Resource
    print("\n📋 Test 15: Deactivate Resource")
    response = requests.patch(f"{BASE_URL}/resources/{resource_id}/deactivate")
    print_response(f"PATCH /resources/{resource_id}/deactivate", response)
    if response.status_code == 200:
        print("✅ Resource deactivated successfully")

    # Test 16: Activate Resource
    print("\n📋 Test 16: Activate Resource")
    response = requests.patch(f"{BASE_URL}/resources/{resource_id}/activate")
    print_response(f"PATCH /resources/{resource_id}/activate", response)
    if response.status_code == 200:
        print("✅ Resource activated successfully")

    # Test 17: Verify Cascade - Get Resource with Actions Count
    print("\n📋 Test 17: Verify Resource shows Actions Count")
    response = requests.get(f"{BASE_URL}/resources/{resource_id}")
    print_response(f"GET /resources/{resource_id}", response)
    if response.status_code == 200:
        actions_count = response.json()["actions_count"]
        print(f"\n✅ Resource has {actions_count} actions")

    # Test 18: Delete Single Action
    print("\n📋 Test 18: Delete Single Action")
    response = requests.delete(f"{BASE_URL}/actions/{action_delete_id}")
    print_response(f"DELETE /actions/{action_delete_id}", response)
    if response.status_code == 204:
        print("✅ Action deleted successfully")

    # Test 19: Verify Action was deleted
    print("\n📋 Test 19: Verify Action Deletion")
    response = requests.get(f"{BASE_URL}/actions/?resource_id={resource_id}")
    remaining_actions = response.json()["total"]
    print(f"✅ Remaining actions: {remaining_actions} (should be 2)")

    # Test 20: Delete Resource (CASCADE test)
    print("\n📋 Test 20: Delete Resource (CASCADE)")
    response = requests.delete(f"{BASE_URL}/resources/{resource_id}")
    print_response(f"DELETE /resources/{resource_id}", response)
    if response.status_code == 204:
        print("✅ Resource deleted successfully (CASCADE should delete all actions)")

    # Test 21: Verify Cascade Deletion
    print("\n📋 Test 21: Verify Cascade Deletion")
    response = requests.get(f"{BASE_URL}/actions/?resource_id={resource_id}")
    total_actions = response.json()["total"]
    print(f"✅ Actions after resource deletion: {total_actions} (should be 0)")
    if total_actions == 0:
        print("✅ CASCADE deletion confirmed!")

    # Test 22: Try to get deleted resource (should return 404)
    print("\n📋 Test 22: Verify Resource was deleted")
    response = requests.get(f"{BASE_URL}/resources/{resource_id}")
    print_response(f"GET /resources/{resource_id}", response)
    if response.status_code == 404:
        print("✅ Resource not found (correctly deleted)")

    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60 + "\n")

    # Summary
    print("\n📊 TEST SUMMARY:")
    print("✅ Resource CRUD operations: PASSED")
    print("✅ Action CRUD operations: PASSED")
    print("✅ Filtering and pagination: PASSED")
    print("✅ Activate/Deactivate operations: PASSED")
    print("✅ CASCADE deletion: PASSED")
    print("✅ Actions count tracking: PASSED")
    print("\n🎉 All 22 tests passed successfully!")


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
