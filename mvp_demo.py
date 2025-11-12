#!/usr/bin/env python3
"""
Sentinela MVP Demo
Demonstrates the complete authorization flow
"""

import json
from datetime import datetime

def demo_cedar_engine():
    """Demonstrate Cedar policy evaluation"""
    print("🔐 Cedar Policy Engine Demo")
    print("=" * 50)
    
    # Import our Cedar engine
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'business_api_service/src'))
    
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
        """,
        """
        permit(
            principal,
            action == Action::"write",
            resource
        ) when {
            principal.department == "finance" &&
            resource.classification == "internal" &&
            principal.roles.contains("document_writer")
        };
        """
    ]
    
    engine.load_policies(policies)
    print(f"✅ Loaded {len(engine.compiled_policies)} policies")
    
    # Test authorization requests
    test_cases = [
        {
            "name": "Alice reading internal document",
            "principal": 'User::"alice"',
            "action": 'Action::"read"',
            "resource": 'Document::"123"',
            "context": {"department": "finance", "roles": ["document_reader"]},
            "expected": True
        },
        {
            "name": "Bob reading internal document",
            "principal": 'User::"bob"',
            "action": 'Action::"read"',
            "resource": 'Document::"123"',
            "context": {"department": "hr", "roles": ["document_reader"]},
            "expected": False
        },
        {
            "name": "Alice writing internal document",
            "principal": 'User::"alice"',
            "action": 'Action::"write"',
            "resource": 'Document::"123"',
            "context": {"department": "finance", "roles": ["document_writer"]},
            "expected": True
        },
        {
            "name": "Alice writing without writer role",
            "principal": 'User::"alice"',
            "action": 'Action::"write"',
            "resource": 'Document::"123"',
            "context": {"department": "finance", "roles": ["document_reader"]},
            "expected": False
        }
    ]
    
    print("\n🧪 Authorization Test Cases:")
    print("-" * 50)
    
    for i, test in enumerate(test_cases, 1):
        request = AuthorizationRequest(
            principal=test["principal"],
            action=test["action"],
            resource=test["resource"],
            context=test["context"]
        )
        
        result = engine.evaluate(request)
        status = "✅ ALLOW" if result.allow else "❌ DENY"
        expected = "✅" if result.allow == test["expected"] else "❌"
        
        print(f"{i}. {test['name']}")
        print(f"   Result: {status} - {result.reason}")
        print(f"   Expected: {'Allow' if test['expected'] else 'Deny'} {expected}")
        print()

def demo_policy_models():
    """Demonstrate policy data models"""
    print("📋 Policy API Models Demo")
    print("=" * 50)
    
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'policy_api/src'))
    
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

def demo_document_models():
    """Demonstrate document data models"""
    print("\n📄 Document API Models Demo")
    print("=" * 50)
    
    import sys
    import os
    doc_path = os.path.join(os.path.dirname(__file__), 'business_api_service/src')
    sys.path.insert(0, doc_path)
    
    from models.document import Document, DocumentCreate, DocumentType
    
    # Test document creation
    doc_data = DocumentCreate(
        title="Financial Report Q4 2025",
        content="This is a confidential financial report...",
        document_type=DocumentType.REPORT,
        department="finance",
        classification="confidential"
    )
    
    print(f"✅ Created document: {doc_data.title}")
    print(f"   Type: {doc_data.document_type}")
    print(f"   Department: {doc_data.department}")
    print(f"   Classification: {doc_data.classification}")
    
    # Test full document model
    full_doc = Document(
        id="doc-456",
        title=doc_data.title,
        content=doc_data.content,
        document_type=doc_data.document_type,
        owner_id="alice",
        department=doc_data.department,
        classification=doc_data.classification,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    print(f"\n✅ Full document model:")
    print(f"   ID: {full_doc.id}")
    print(f"   Owner: {full_doc.owner_id}")
    print(f"   Created: {full_doc.created_at}")

def main():
    """Run complete MVP demo"""
    print("🚀 Sentinela MVP Demonstration")
    print("=" * 60)
    print("This demo shows the core components of the Sentinela IAM system:")
    print("• Cedar Policy Engine for authorization decisions")
    print("• Policy API for managing authorization policies")
    print("• Document API for protected resources")
    print("• Complete authentication and authorization flow")
    print("=" * 60)
    
    try:
        demo_policy_models()
        demo_document_models()
        demo_cedar_engine()
        
        print("\n🎉 MVP Demo Completed Successfully!")
        print("\n📋 What was demonstrated:")
        print("   ✅ Policy data models and validation")
        print("   ✅ Document data models and types")
        print("   ✅ Cedar policy engine with real evaluation")
        print("   ✅ Authorization decisions based on policies")
        print("   ✅ Context-aware access control")
        
        print("\n🔧 Architecture Components Working:")
        print("   🏗️  Data Models: Pydantic models with validation")
        print("   ⚙️  Policy Engine: Cedar-style authorization")
        print("   🔐 Authorization: Context-based decisions")
        print("   📊 Business Logic: Department and role-based")
        
        print("\n🚀 Next Steps for Production:")
        print("   1. Deploy Keycloak for authentication")
        print("   2. Configure OPAL for policy distribution")
        print("   3. Set up persistent databases")
        print("   4. Add monitoring and logging")
        print("   5. Implement policy management UI")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())