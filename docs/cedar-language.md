# Cedar Policy Language Reference

Complete guide to writing authorization policies in Cedar language.

## 🌲 What is Cedar?

Cedar is a simple, expressive policy language inspired by AWS IAM. It's designed for writing authorization policies that are easy to read, write, and maintain.

### Key Principles

- **Declarative**: Describe what should be allowed, not how to check it
- **Composable**: Build complex policies from simple rules  
- **Testable**: Policies can be unit tested
- **Versionable**: Store policies in git with your code

## 📝 Basic Syntax

### Policy Structure

```cedar
policy PolicyName {
    // Rules go here
    permit(principal, action, resource);
    
    // Or with conditions
    permit(principal, action, resource) when {
        // Conditions
    };
    
    // Or forbid specific cases
    forbid(principal, action, resource) when {
        // Forbidden conditions
    };
}
```

### Basic Elements

#### Principals (WHO)

```cedar
// Specific user
User::"alice"
User::"bob@company.com"

// Groups
Group::"managers"
Group::"employees"
Group::"admin"

// Services
Service::"payment-processor"
Service::"analytics-service"

// Any entity
principal
```

#### Actions (WHAT)

```cedar
// Specific actions
Action::"read"
Action::"write"
Action::"delete"
Action::"approve"

// Wildcard for any action
Action::"*

// Action sets
Action::["read", "write"]
Action::["approve", "reject"]
```

#### Resources (WHAT)

```cedar
// Specific resources
Document::"public"
Document::"confidential"
File::"salary-data"
API::"user-management"

// Resource patterns
Document::"public/*"
Document::"hr/*"

// Wildcard for any resource
Document::*
Resource::*
```

## 🔐 Core Policy Rules

### Simple Permit

Allow anyone to do anything:

```cedar
policy AllowAll {
    permit(principal, action, resource);
}
```

### Specific User Access

Allow Alice to read public documents:

```cedar
policy AliceReadPublic {
    permit(
        principal in User::"alice",
        action in Action::"read",
        resource in Document::"public"
    );
}
```

### Group-Based Access

Allow managers to perform any action on any document:

```cedar
policy ManagerAccess {
    permit(
        principal in Group::"managers",
        action in Action::*,
        resource in Document::*
    );
}
```

### Multiple Actions

Allow employees to read and write documents:

```cedar
policy EmployeeDocumentAccess {
    permit(
        principal in Group::"employees",
        action in Action::["read", "write"],
        resource in Document::"internal"
    );
}
```

## 🎯 Conditional Policies

### When Clauses

Add conditions using `when`:

```cedar
policy ConditionalAccess {
    permit(
        principal in User::"alice",
        action in Action::"read",
        resource in Document::"confidential"
    ) when {
        principal.clearance >= resource.classification &&
        resource.department == principal.department
    };
}
```

### Attribute-Based Conditions

Use resource and principal attributes:

```cedar
policy AttributeBasedAccess {
    permit(
        principal,
        action in Action::"read",
        resource in Document::"salary"
    ) when {
        principal.role in ["hr_manager", "finance_director"] &&
        principal.department == "HR" &&
        action.time >= "09:00" &&
        action.time <= "17:00"
    };
}
```

### Context-Based Conditions

Use request context for dynamic decisions:

```cedar
policy ContextAwareAccess {
    permit(
        principal,
        action in Action::"access",
        resource in System::"database"
    ) when {
        principal.role == "admin" ||
        (principal.role == "dba" && action.maintenance_window == true)
    };
}
```

## 🚫 Forbid Rules

### Explicit Forbid

Deny specific access patterns:

```cedar
policy DenyExternalAccess {
    forbid(
        principal,
        action in Action::"read",
        resource in Document::"confidential"
    ) when {
        principal.location != "office" &&
        principal.device != "corporate_laptop"
    };
}
```

### Time-Based Restrictions

```cedar
policy BusinessHoursOnly {
    forbid(
        principal in Group::"employees",
        action in Action::"access",
        resource in System::"financial"
    ) when {
        action.time < "09:00" || action.time > "17:00"
    };
}
```

## 🔧 Advanced Patterns

### Nested Conditions

```cedar
policy ComplexAccess {
    permit(
        principal,
        action in Action::"read",
        resource in Document::"medical"
    ) when {
        // Must be medical staff
        principal.role in ["doctor", "nurse", "medical_admin"] &&
        
        // Must have proper clearance
        principal.clearance >= resource.classification &&
        
        // Must be in authorized location
        principal.location in ["hospital", "clinic"] &&
        
        // Patient consent required for non-emergency
        (resource.emergency == true || principal.has_patient_consent == true)
    };
}
```

### Resource Ownership

```cedar
policy OwnerAccess {
    permit(
        principal,
        action in Action::["read", "write", "delete"],
        resource in Document::*
    ) when {
        resource.owner == principal ||
        principal.role == "admin"
    };
}
```

### Delegation

```cedar
policy DelegatedAccess {
    permit(
        principal,
        action in Action::"read",
        resource in Document::*
    ) when {
        // Direct access
        resource.owner == principal ||
        
        // Delegated access
        principal in resource.delegated_to &&
        principal.delegation_expiry > resource.current_time ||
        
        // Manager override
        principal.role == "manager" &&
        principal.department == resource.department
    };
}
```

## 📊 Data Types and Operations

### Supported Data Types

```cedar
// Strings
principal.name == "Alice"
resource.type == "document"

// Numbers
principal.clearance >= 3
resource.size < 1024

// Booleans
principal.enabled == true
resource.public == false

// Lists/Arrays
principal.role in ["admin", "manager"]
action.type in ["read", "write"]

// Sets
principal.permissions.contains("read")
resource.tags.contains("confidential")
```

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|----------|
| == | Equal to | `principal.role == "admin"` |
| != | Not equal to | `principal.role != "guest"` |
| > | Greater than | `principal.clearance > 3` |
| >= | Greater than or equal | `principal.clearance >= 3` |
| < | Less than | `resource.size < 1024` |
| <= | Less than or equal | `resource.size <= 1024` |
| in | Member of | `principal.role in ["admin", "manager"]` |
| contains | Contains element | `principal.permissions.contains("read")` |

### Logical Operators

| Operator | Description | Example |
|----------|-------------|----------|
| && | Logical AND | `principal.admin == true && principal.enabled == true` |
| || | Logical OR | `principal.role == "admin" || principal.role == "manager"` |
| ! | Logical NOT | `!principal.suspended` |

## 🏗️ Policy Composition

### Multiple Policies

Policies are evaluated independently:

```cedar
// Policy 1: Basic read access
policy BasicReadAccess {
    permit(
        principal in Group::"employees",
        action in Action::"read",
        resource in Document::"public"
    );
}

// Policy 2: Admin override
policy AdminOverride {
    permit(
        principal in Group::"admin",
        action in Action::*,
        resource in Document::*
    );
}

// Policy 3: Deny external access
policy DenyExternal {
    forbid(
        principal,
        action in Action::"read",
        resource in Document::"confidential"
    ) when {
        principal.location != "office"
    );
}
```

### Policy Precedence

1. **Forbid rules** take precedence over permit rules
2. **More specific** rules take precedence over general rules
3. **Policies are evaluated** in alphabetical order by name

## 🧪 Testing Policies

### Unit Test Structure

```python
# Test policy evaluation
test_cases = [
    {
        "principal": "User::\"alice\"",
        "action": "Action::\"read\"",
        "resource": "Document::\"public\"",
        "expected": True,
        "description": "Alice can read public documents"
    },
    {
        "principal": "User::\"bob\"",
        "action": "Action::\"delete\"",
        "resource": "Document::\"confidential\"",
        "expected": False,
        "description": "Bob cannot delete confidential documents"
    }
]
```

### Test with Context

```cedar
policy TimeBasedAccess {
    permit(
        principal,
        action in Action::"access",
        resource in System::"database"
    ) when {
        principal.role == "admin" ||
        (action.time >= "09:00" && action.time <= "17:00")
    };
}

// Test cases
// 1. Admin at 2 AM -> Should ALLOW
// 2. Employee at 10 AM -> Should ALLOW  
// 3. Employee at 2 AM -> Should DENY
```

## 🔍 Best Practices

### 1. Principle of Least Privilege

```cedar
// Good: Specific permissions
policy SpecificDocumentAccess {
    permit(
        principal in User::"alice",
        action in Action::"read",
        resource in Document::"alice_reports"
    );
}

// Avoid: Overly broad permissions
policy TooBroadAccess {
    permit(
        principal in User::"alice",
        action in Action::*,
        resource in Document::*
    );
}
```

### 2. Use Descriptive Names

```cedar
// Good: Clear, descriptive names
policy HrDocumentReadAccess {
    permit(
        principal in Group::"hr_staff",
        action in Action::"read",
        resource in Document::"hr_records"
    ) when {
        principal.department == "HR"
    };
}

// Avoid: Vague names
policy Policy1 {
    permit(principal, action, resource);
}
```

### 3. Document Complex Logic

```cedar
policy ComplexMedicalAccess {
    permit(
        principal,
        action in Action::"read",
        resource in Document::"medical_record"
    ) when {
        // Medical staff with proper clearance
        (principal.role in ["doctor", "nurse"] && 
         principal.clearance >= resource.classification &&
         principal.department == "Medical")
        
        // OR patient accessing their own records
        || (principal.role == "patient" && 
            resource.patient_id == principal.id)
            
        // OR emergency access
        || (resource.emergency == true && 
            principal.role in ["doctor", "nurse", "paramedic"])
    };
}
```

### 4. Handle Edge Cases

```cedar
policy RobustDocumentAccess {
    permit(
        principal,
        action in Action::"read",
        resource in Document::*
    ) when {
        // Valid user
        principal.enabled == true &&
        principal.suspended != true &&
        
        // Resource exists and is accessible
        resource.exists == true &&
        resource.archived != true &&
        
        // Permission check
        (resource.owner == principal ||
         principal.role in ["admin", "manager"] ||
         principal.department == resource.department)
    };
    
    // Explicitly forbid deleted/archived resources
    forbid(
        principal,
        action,
        resource
    ) when {
        resource.deleted == true || resource.archived == true
    );
}
```

## 🚨 Common Pitfalls

### 1. Missing Resource Attributes

```cedar
// Wrong: Resource doesn't have 'owner' attribute
permit(principal, action, resource) when {
    resource.owner == principal  // Error if owner doesn't exist
}

// Right: Check attribute exists
permit(principal, action, resource) when {
    resource.hasAttribute("owner") && resource.owner == principal
}
```

### 2. Infinite Recursion

```cedar
// Wrong: Can cause infinite loop
policy RecursivePolicy {
    permit(principal, action, resource) when {
        principal.canAccess(resource) &&  // Calls itself
        resource.isAccessible
    };
}

// Right: Use direct attribute checks
policy NonRecursivePolicy {
    permit(principal, action, resource) when {
        principal.clearance >= resource.required_clearance &&
        principal.department == resource.allowed_department
    };
}
```

### 3. Type Mismatches

```cedar
// Wrong: Comparing string with number
permit(principal, action, resource) when {
    principal.clearance == "high"  // clearance is number, high is string
}

// Right: Compare matching types
permit(principal, action, resource) when {
    principal.clearance >= 4  // Both numbers
}
```

## 📚 Examples Library

### Document Management

```cedar
policy DocumentReadAccess {
    permit(
        principal,
        action in Action::"read",
        resource in Document::*
    ) when {
        // Owner can always read
        resource.owner == principal ||
        
        // Managers can read department documents
        (principal.role == "manager" && 
         principal.department == resource.department) ||
         
        // HR can read HR documents
        (principal.department == "HR" && 
         resource.type == "hr") ||
         
        // Public documents accessible to all
        resource.classification == "public"
    };
}
```

### API Access Control

```cedar
policy APIAccess {
    permit(
        principal,
        action in Action::["read", "write", "delete"],
        resource in API::*
    ) when {
        // Service-to-service access
        (principal.type == "service" && 
         resource.allowed_services.contains(principal.name)) ||
         
        // User access with proper role
        (principal.type == "user" && 
         principal.api_permissions.contains(resource.name)) ||
         
        // Admin override
        principal.role == "admin"
    );
}
```

### Multi-Tenant Access

```cedar
policy TenantAccess {
    permit(
        principal,
        action in Action::*,
        resource in Resource::*
    ) when {
        // Same tenant
        principal.tenant_id == resource.tenant_id &&
        
        // Proper permissions within tenant
        (principal.role == "tenant_admin" ||
         (principal.role == "user" && 
          action in Action::["read"] &&
          resource.owner == principal))
    };
}
```

## 🔧 Tools and IDE Support

### VS Code Extension

Install Cedar language support:
- Syntax highlighting
- Error detection
- Auto-completion
- Policy validation

### CLI Tools

```bash
# Validate policy syntax
cedar validate policy.cedar

# Test policy with data
cedar test policy.cedar --data test_data.json

# Format policy
cedar format policy.cedar

# Analyze policy coverage
cedar coverage policy.cedar --test-cases tests.json
```

## 📖 Additional Resources

- [Cedar Language Specification](https://cedar.dev/spec)
- [Policy Testing Guide](policy-testing.md)
- [Best Practices](best-practices.md)
- [Example Policies](examples/)
- [Community Forum](https://community.sentinela.io)

---

**Ready to write powerful authorization policies! 🚀**