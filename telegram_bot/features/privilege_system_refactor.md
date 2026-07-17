# Privilege System Refactoring Proposal

## Current System Issues

The current privilege system has several limitations:

1. Using bit flags directly in code makes it hard to understand what privileges a user has
2. Privileges are directly assigned to users without a role abstraction
3. The hierarchy structure is complex and makes privilege checks expensive
4. No clear documentation on what each privilege allows a user to do
5. Limited auditing of privilege changes

## Proposed Solution: Role-Based Access Control

### Roles and Permissions Architecture

```python
# New permission enums with clear names and descriptions
class Permission(enum.IntFlag):
    NONE = 0
    
    # Admin permissions
    MANAGE_USERS = 1 << 0       # Can edit/view users
    MANAGE_ROLES = 1 << 1       # Can assign/remove roles
    MANAGE_EVENTS = 1 << 2      # Can create/edit events
    MANAGE_PROMOCODES = 1 << 3  # Can create/edit promocodes
    MANAGE_SHOP = 1 << 4        # Can manage shop items
    MANAGE_APPLICATIONS = 1 << 5 # Can approve/reject applications
    
    # Event permissions
    GIVE_EVENT_POINTS = 1 << 10  # Can award points for events
    ATTEND_EVENTS = 1 << 11      # Can mark attendance
    
    # Root permission (has all permissions)
    ALL = (1 << 16) - 1
```

### Role Definitions

```python
# Pre-defined roles with clear permissions
class Role:
    def __init__(self, name: str, permissions: Permission, description: str = ""):
        self.name = name
        self.permissions = permissions
        self.description = description

# Example role definitions
ROLES = {
    "admin": Role(
        name="Administrator",
        permissions=Permission.ALL,
        description="Full system access"
    ),
    "event_manager": Role(
        name="Event Manager",
        permissions=Permission.MANAGE_EVENTS | Permission.GIVE_EVENT_POINTS,
        description="Can manage events and give points"
    ),
    "shop_manager": Role(
        name="Shop Manager",
        permissions=Permission.MANAGE_SHOP,
        description="Can manage shop items"
    ),
    "moderator": Role(
        name="Moderator", 
        permissions=Permission.MANAGE_APPLICATIONS | Permission.GIVE_EVENT_POINTS,
        description="Can moderate applications and give points"
    ),
    "user": Role(
        name="User",
        permissions=Permission.NONE,
        description="Regular user with no special permissions"
    )
}
```

### Database Schema Changes

```sql
-- Roles table
CREATE TABLE roles
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE,
    permissions INTEGER     NOT NULL DEFAULT 0,
    description TEXT,
    created_at  TIMESTAMP   NOT NULL DEFAULT NOW(),
    is_system   BOOLEAN     NOT NULL DEFAULT FALSE
);

-- User-Role assignments
CREATE TABLE user_roles
(
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER REFERENCES users (id) ON DELETE CASCADE,
    role_id    INTEGER REFERENCES roles (id) ON DELETE CASCADE,
    granted_by INTEGER REFERENCES users (id),
    granted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP,
    UNIQUE (user_id, role_id)
);

-- Audit log for role changes
CREATE TABLE role_audit_log
(
    id                   SERIAL PRIMARY KEY,
    user_id              INTEGER REFERENCES users (id),
    role_id              INTEGER REFERENCES roles (id),
    action               VARCHAR(20) NOT NULL, -- 'GRANT', 'REVOKE', etc.
    performed_by         INTEGER REFERENCES users (id),
    performed_at         TIMESTAMP   NOT NULL DEFAULT NOW(),
    previous_permissions INTEGER,
    new_permissions      INTEGER
);
```

### Helper Functions

```python
async def has_permission(user_id: int, permission: Permission) -> bool:
    """Check if a user has a specific permission."""
    # Get cached user permissions first
    cached_permissions = await get_cached_permissions(user_id)
    if cached_permissions is not None:
        return bool(cached_permissions & permission)

    # If not cached, load from database
    async with async_session() as session:
        query = select(
            func.bit_or(Role.permissions).label('permissions')
        ).select_from(UserRole).join(
            Role, UserRole.role_id == Role.id
        ).where(
            UserRole.user_id == user_id,
            (UserRole.expires_at.is_(None) | (UserRole.expires_at > datetime.now()))
        )
        result = await session.execute(query)
        user_permissions = result.scalar() or 0

        # Cache for future checks
        await cache_permissions(user_id, user_permissions)

        return bool(user_permissions & permission)


async def grant_role(
        user_id: int,
        role_id: int,
        granted_by: int,
        expires_at: Optional[datetime] = None
) -> bool:
    """Grant a role to a user."""
    async with async_session() as session:
        # Check if granter has permission
        granter_has_permission = await has_permission(granted_by, Permission.MANAGE_ROLES)
        if not granter_has_permission:
            return False

        # Add role
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            granted_by=granted_by,
            expires_at=expires_at
        )
        session.add(user_role)

        # Add audit log
        audit = RoleAuditLog(
            user_id=user_id,
            role_id=role_id,
            action="GRANT",
            performed_by=granted_by
        )
        session.add(audit)

        await session.commit()

        # Invalidate permissions cache
        await invalidate_permissions_cache(user_id)

        return True
```

## Implementation Plan

1. **Phase 1: Database Migration**
    - Create new tables for roles and permissions
    - Add a migration script to transfer existing privileges

2. **Phase 2: Core Logic Implementation**
    - Implement permission check functions
    - Add caching for permission checks
    - Create role management functions

3. **Phase 3: Admin UI Updates**
    - Update admin privilege UI to use roles
    - Add role management interface
    - Add audit log viewer

4. **Phase 4: Handler Updates**
    - Update all handlers to use the new permission system
    - Deprecate old PrivilegeFilter and replace with PermissionFilter

## Benefits

1. **Clearer Permission Management**: Role-based system is easier to understand
2. **Better Performance**: Cached permission checks are faster
3. **Improved Auditability**: All changes are tracked in the audit log
4. **Simpler Administration**: Managing roles is easier than individual permissions
5. **Flexible Role Expiration**: Roles can be granted temporarily with expiration

## Migration Strategy

1. Create default roles matching current privilege masks
2. Map existing users to appropriate roles based on current privileges
3. Update handlers gradually, supporting both systems during transition
4. Once all handlers are updated, remove the old privilege system 