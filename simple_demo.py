#!/usr/bin/env python3
"""
Simple Sentinela MVP Demo
"""

import sys
import os
from datetime import datetime

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'policy_api/src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'business_api_service/src'))

def demo_policy_models():
    """Demonstrate policy data models"""
    print("📋 Policy API Models Demo")
    print("=" * 50)
    
    from models.policy import Policy, PolicyCreate, PolicyStatus
    
    # Test policy creation
    policy_data = PolicyCreate(
        name="Finance Document Access",
        description="Controls access to finance documents",
        content="permit(principal, action, resource);"
    )
    
    print(f"✅ Created policy: {policy_data.name}")
    print(f"   Description: {policy_data.description}")
    print(f"   Content: {policy_data.content[:50]}...")
    
    # Test full policy model
    full_policy = Policy(
        id="policy-123",
        name=policy_data.name,
        description=policy_data.description,
        content=policy_data.content,
        status=PolicyStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        version=1
    )
    
    print(f"\n✅ Full policy model:")
    print(f"   ID: {full_policy.id}")
    print(f"   Version: {full_policy.version}")
    print(f"   Status: {full_policy.status}")

def demo_cedar_engine():
    """Demonstrate Cedar policy evaluation"""
    print("\n🔐 Cedar Policy Engine Demo")
    print("=" * 50)
    
    from services.cedar_engine import CedarEngine, AuthorizationRequest
    
    # Create engine
    engine = CedarEngine()
    
    # Load sample policies
    policies = [
        """
        permit(
            principal,
            action == Action::"read",
            resource
        ) when {
            principal.department == "finance" &&
            resource.classification == "internal"
        };
        """
    ]
    
    engine.load_policies(policies)
    print(f"✅ Loaded {len(engine.compiled_policies)} policies")
    
    # Test authorization requests
    request = AuthorizationRequest(
        principal='User::"alice"',
        action='Action::"read"',
        resource='Document::"123"',
        context={"department": "finance", "roles": ["document_reader"]}
    )
    
    result = engine.evaluate(request)
    status = "✅ ALLOW" if result.allow else "❌ DENY"
    
    print(f"\n🧪 Authorization Test:")
    print(f"   Principal: {request.principal}")
    print(f"   Action: {request.action}")
    print(f"   Resource: {request.resource}")
    print(f"   Context: {request.context}")
    print(f"   Result: {status} - {result.reason}")

def main():
    """Run simple MVP demo"""
    print("🚀 Sentinela MVP Simple Demo")
    print("=" * 60)
    
    try:
        demo_policy_models()
        demo_cedar_engine()
        
        print("\n🎉 MVP Demo Completed Successfully!")
        print("\n📋 What was demonstrated:")
        print("   ✅ Policy data models with Pydantic validation")
        print("   ✅ Cedar policy engine with real evaluation")
        print("   ✅ Authorization decisions based on policies")
        print("   ✅ Context-aware access control")
        
        print("\n🏗️  Architecture Components Working:")
        print("   📊 Data Models: Pydantic models with validation")
        print("   ⚙️  Policy Engine: Cedar-style authorization")
        print("   🔐 Authorization: Context-based decisions")
        print("   📈 Business Logic: Department-based access")
        
        print("\n✅ Sentinela MVP Core Implementation Complete!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())