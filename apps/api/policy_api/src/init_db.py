#!/usr/bin/env python3
"""
Initialize database tables for Policy API
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from database import engine, Base
from models import *

def init_database():
    """Initialize all database tables"""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # List created tables
        from models.user import User
        from models.group import Group
        from models.policy import Policy
        from models.action import Action
        from models.resource import Resource
        from models.application import Application
        from models.api_key import APIKey
        from models.user_group import UserGroup
        
        print("Created tables:")
        print("- users")
        print("- groups") 
        print("- policies")
        print("- actions")
        print("- resources")
        print("- applications")
        print("- api_keys")
        print("- user_groups")
        
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)