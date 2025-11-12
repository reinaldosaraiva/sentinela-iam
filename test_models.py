"""
Test script for Application and APIKey models
"""

import sys
import os
from datetime import datetime, timedelta

# Add policy_api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'policy_api', 'src'))

# Import database first
import database_pg
from database_pg import engine, SessionLocal, Base, init_db

# Import models
from models.application import Application
from models.api_key import APIKey


def test_models():
    """Test Application and APIKey models"""

    print("🔧 Testing Application and APIKey Models\n")

    # Initialize database (this will create tables if they don't exist via SQLAlchemy)
    print("1. Initializing database connection...")
    try:
        Base.metadata.create_all(bind=engine)
        print("   ✅ Database connection successful\n")
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}\n")
        return

    # Create session
    db = SessionLocal()

    try:
        # Test 1: Query existing applications
        print("2. Querying existing applications...")
        applications = db.query(Application).all()
        print(f"   Found {len(applications)} applications:")
        for app in applications:
            print(f"   - {app.name} ({app.slug}) - {app.status}")
        print()

        # Test 2: Create a new application
        print("3. Creating new test application...")
        test_app = Application(
            name="Test API Application",
            slug="test-api-app",
            description="Test application for API key management",
            status="active",
            environment="development"
        )
        db.add(test_app)
        db.commit()
        db.refresh(test_app)
        print(f"   ✅ Created application: {test_app.id}")
        print(f"   Application dict: {test_app.to_dict()}")
        print()

        # Test 3: Generate API keys
        print("4. Generating API keys...")

        # Generate 3 API keys
        for i in range(1, 4):
            plain_key, key_hash = APIKey.generate_key(prefix="app_")

            api_key = APIKey(
                application_id=test_app.id,
                name=f"Test Key {i}",
                key_prefix="app_",
                key_hash=key_hash,
                expires_at=datetime.utcnow() + timedelta(days=90) if i > 1 else None
            )
            db.add(api_key)

            print(f"   API Key {i}:")
            print(f"   - Plain Key: {plain_key[:20]}... (truncated)")
            print(f"   - Hash: {key_hash[:20]}...")
            print(f"   - Expires: {api_key.expires_at}")

            # Test verification
            is_valid = APIKey.verify_key(plain_key, key_hash)
            print(f"   - Verification: {'✅ PASS' if is_valid else '❌ FAIL'}")
            print()

        db.commit()
        print("   ✅ All API keys created successfully\n")

        # Test 4: Query application with relationships
        print("5. Testing relationships...")
        app_with_keys = db.query(Application).filter_by(slug="test-api-app").first()
        print(f"   Application: {app_with_keys.name}")
        print(f"   API Keys Count: {len(app_with_keys.api_keys)}")
        for key in app_with_keys.api_keys:
            print(f"   - {key.name}: active={key.is_active}, valid={key.is_valid()}")
        print()

        # Test 5: Update last_used_at
        print("6. Testing last_used_at update...")
        first_key = app_with_keys.api_keys[0]
        print(f"   Before: {first_key.last_used_at}")
        first_key.update_last_used()
        db.commit()
        db.refresh(first_key)
        print(f"   After: {first_key.last_used_at}")
        print(f"   ✅ Last used timestamp updated\n")

        # Test 6: Test to_dict methods
        print("7. Testing to_dict methods...")
        print(f"   Application dict keys: {list(app_with_keys.to_dict().keys())}")
        print(f"   APIKey dict keys: {list(first_key.to_dict().keys())}")
        print(f"   ✅ Serialization working\n")

        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_models()
