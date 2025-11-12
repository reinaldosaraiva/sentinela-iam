"""
Seed database with sample data for testing
"""

import sys
import os
from datetime import datetime, timedelta
from uuid import uuid4

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy.orm import Session
from src.database_pg import SessionLocal, init_db
from src.models import Application, Resource, Action, APIKey


def clear_data(db: Session):
    """Clear existing data"""
    print("🗑️  Clearing existing data...")
    db.query(Action).delete()
    db.query(Resource).delete()
    db.query(APIKey).delete()
    db.query(Application).delete()
    db.commit()
    print("✅ Data cleared")


def seed_applications(db: Session):
    """Create sample applications"""
    print("\n📱 Creating sample applications...")

    applications = [
        {
            "id": uuid4(),
            "name": "E-Commerce Platform",
            "slug": "ecommerce-platform",
            "description": "Main e-commerce application for online shopping",
            "status": "active",
            "environment": "production",
            "logo_url": "https://example.com/logos/ecommerce.png",
            "website_url": "https://ecommerce.example.com"
        },
        {
            "id": uuid4(),
            "name": "Customer Portal",
            "slug": "customer-portal",
            "description": "Self-service portal for customers",
            "status": "active",
            "environment": "production",
            "logo_url": "https://example.com/logos/portal.png",
            "website_url": "https://portal.example.com"
        },
        {
            "id": uuid4(),
            "name": "Admin Dashboard",
            "slug": "admin-dashboard",
            "description": "Administrative dashboard for system management",
            "status": "active",
            "environment": "staging",
            "logo_url": "https://example.com/logos/admin.png",
            "website_url": "https://admin-dev.example.com"
        },
        {
            "id": uuid4(),
            "name": "Mobile App API",
            "slug": "mobile-app-api",
            "description": "Backend API for mobile applications",
            "status": "active",
            "environment": "production",
            "logo_url": "https://example.com/logos/mobile.png",
            "website_url": "https://api.mobile.example.com"
        },
        {
            "id": uuid4(),
            "name": "Analytics Service",
            "slug": "analytics-service",
            "description": "Data analytics and reporting service",
            "status": "paused",
            "environment": "development",
            "logo_url": "https://example.com/logos/analytics.png",
            "website_url": "https://analytics-dev.example.com"
        }
    ]

    app_objects = []
    for app_data in applications:
        app = Application(**app_data)
        db.add(app)
        app_objects.append(app)
        print(f"  ✓ Created: {app_data['name']} ({app_data['environment']})")

    db.commit()
    print(f"✅ Created {len(applications)} applications")
    return app_objects


def seed_resources(db: Session, applications: list):
    """Create sample resources for applications"""
    print("\n🗂️  Creating sample resources...")

    # E-Commerce Platform Resources
    ecommerce_app = applications[0]
    ecommerce_resources = [
        {
            "id": uuid4(),
            "resource_type": "products",
            "name": "Products",
            "description": "Product catalog and inventory",
            "application_id": ecommerce_app.id,
            "is_active": True
        },
        {
            "id": uuid4(),
            "resource_type": "orders",
            "name": "Orders",
            "description": "Customer orders and transactions",
            "application_id": ecommerce_app.id,
            "is_active": True
        },
        {
            "id": uuid4(),
            "resource_type": "customers",
            "name": "Customers",
            "description": "Customer accounts and profiles",
            "application_id": ecommerce_app.id,
            "is_active": True
        },
        {
            "id": uuid4(),
            "resource_type": "payments",
            "name": "Payments",
            "description": "Payment processing and transactions",
            "application_id": ecommerce_app.id,
            "is_active": True
        }
    ]

    # Customer Portal Resources
    portal_app = applications[1]
    portal_resources = [
        {
            "id": uuid4(),
            "resource_type": "profile",
            "name": "User Profile",
            "description": "User profile information",
            "application_id": portal_app.id,
            "is_active": True
        },
        {
            "id": uuid4(),
            "resource_type": "tickets",
            "name": "Support Tickets",
            "description": "Customer support tickets",
            "application_id": portal_app.id,
            "is_active": True
        }
    ]

    # Admin Dashboard Resources
    admin_app = applications[2]
    admin_resources = [
        {
            "id": uuid4(),
            "resource_type": "users",
            "name": "Users",
            "description": "System user management",
            "application_id": admin_app.id,
            "is_active": True
        },
        {
            "id": uuid4(),
            "resource_type": "settings",
            "name": "Settings",
            "description": "System configuration settings",
            "application_id": admin_app.id,
            "is_active": True
        },
        {
            "id": uuid4(),
            "resource_type": "reports",
            "name": "Reports",
            "description": "System reports and analytics",
            "application_id": admin_app.id,
            "is_active": True
        }
    ]

    all_resources = ecommerce_resources + portal_resources + admin_resources
    resource_objects = []

    for resource_data in all_resources:
        resource = Resource(**resource_data)
        db.add(resource)
        resource_objects.append(resource)
        app_name = next(app.name for app in applications if app.id == resource_data['application_id'])
        print(f"  ✓ Created: {resource_data['name']} → {app_name}")

    db.commit()
    print(f"✅ Created {len(all_resources)} resources")
    return resource_objects


def seed_actions(db: Session, resources: list):
    """Create sample actions for resources"""
    print("\n⚡ Creating sample actions...")

    # Standard CRUD actions for each resource
    action_types = [
        {"action_type": "read", "name": "Read", "description": "View and retrieve data"},
        {"action_type": "create", "name": "Create", "description": "Create new records"},
        {"action_type": "update", "name": "Update", "description": "Modify existing records"},
        {"action_type": "delete", "name": "Delete", "description": "Remove records"},
    ]

    # Special actions for specific resources
    special_actions = {
        "products": [
            {"action_type": "publish", "name": "Publish", "description": "Publish product to catalog"},
            {"action_type": "unpublish", "name": "Unpublish", "description": "Remove product from catalog"}
        ],
        "orders": [
            {"action_type": "cancel", "name": "Cancel", "description": "Cancel an order"},
            {"action_type": "refund", "name": "Refund", "description": "Process order refund"},
            {"action_type": "fulfill", "name": "Fulfill", "description": "Mark order as fulfilled"}
        ],
        "payments": [
            {"action_type": "process", "name": "Process", "description": "Process payment transaction"},
            {"action_type": "refund", "name": "Refund", "description": "Refund payment"}
        ],
        "tickets": [
            {"action_type": "assign", "name": "Assign", "description": "Assign ticket to agent"},
            {"action_type": "close", "name": "Close", "description": "Close support ticket"}
        ],
        "users": [
            {"action_type": "activate", "name": "Activate", "description": "Activate user account"},
            {"action_type": "deactivate", "name": "Deactivate", "description": "Deactivate user account"},
            {"action_type": "reset_password", "name": "Reset Password", "description": "Reset user password"}
        ],
        "reports": [
            {"action_type": "generate", "name": "Generate", "description": "Generate report"},
            {"action_type": "export", "name": "Export", "description": "Export report data"}
        ]
    }

    action_count = 0
    for resource in resources:
        # Add standard CRUD actions
        for action_data in action_types:
            action = Action(
                id=uuid4(),
                resource_id=resource.id,
                action_type=action_data["action_type"],
                name=action_data["name"],
                description=action_data["description"],
                is_active=True
            )
            db.add(action)
            action_count += 1

        # Add special actions if available
        if resource.resource_type in special_actions:
            for action_data in special_actions[resource.resource_type]:
                action = Action(
                    id=uuid4(),
                    resource_id=resource.id,
                    action_type=action_data["action_type"],
                    name=action_data["name"],
                    description=action_data["description"],
                    is_active=True
                )
                db.add(action)
                action_count += 1

        print(f"  ✓ Created actions for: {resource.name}")

    db.commit()
    print(f"✅ Created {action_count} actions")


def seed_api_keys(db: Session, applications: list):
    """Create sample API keys for applications"""
    print("\n🔑 Creating sample API keys...")

    key_count = 0
    for app in applications[:3]:  # Only for first 3 apps
        # Create production key
        plain_key, key_hash = APIKey.generate_key(prefix="app_")
        api_key = APIKey(
            id=uuid4(),
            application_id=app.id,
            name=f"{app.name} - Production Key",
            key_prefix="app_",
            key_hash=key_hash,
            expires_at=datetime.utcnow() + timedelta(days=365),
            is_active=True
        )
        db.add(api_key)
        print(f"  ✓ Created key for: {app.name}")
        print(f"    🔐 Key: {plain_key} (save this!)")
        key_count += 1

    db.commit()
    print(f"✅ Created {key_count} API keys")


def main():
    """Main seed function"""
    print("\n" + "="*60)
    print("🌱 SEEDING DATABASE WITH SAMPLE DATA")
    print("="*60)

    # Initialize database
    print("\n🔧 Initializing database...")
    init_db()
    print("✅ Database initialized")

    # Create session
    db = SessionLocal()

    try:
        # Clear existing data
        clear_data(db)

        # Seed data in order (applications -> resources -> actions)
        applications = seed_applications(db)
        resources = seed_resources(db, applications)
        seed_actions(db, resources)
        seed_api_keys(db, applications)

        print("\n" + "="*60)
        print("✅ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  • Applications: {db.query(Application).count()}")
        print(f"  • Resources: {db.query(Resource).count()}")
        print(f"  • Actions: {db.query(Action).count()}")
        print(f"  • API Keys: {db.query(APIKey).count()}")
        print("\n🚀 You can now test the API endpoints!")

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
