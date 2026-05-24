from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.role import Role, Permission

# Define initial system permissions
DEFAULT_PERMISSIONS = [
    {"name": "user:read", "description": "Can only view his/her personal profile"},
    {"name": "user:write", "description": "Can create/edit employee profiles"},
    {"name": "user:delete", "description": "Can remove user accounts"},
]

# Define default system roles
DEFAULT_ROLES = ['Admin', 'HR', 'Employee']

async def init_db(db: AsyncSession) -> None:
    """Seeds default permissions and roles on startup"""

    # Seed Permissions
    permission_records = {}
    for perm_data in DEFAULT_PERMISSIONS:
        result = await db.execute(select(Permission).where(Permission.name == perm_data["name"]))
        perm = result.scalar_one_or_none()
         
        if not perm:
            perm = Permission(name=perm_data["name"], description=perm_data["description"])
            db.add(perm)
            await db.commit()
            await db.refresh(perm)

        permission_records[perm.name] = perm

    # Seed Roles and Link Permissions
    for role_name in DEFAULT_ROLES:
        result = await db.execute(select(Role).where(Role.name == role_name))
        role = result.scalar_one_or_none()

        if not role:
            role = Role(name=role_name)

            # Assign Admin relative permissions
            if role_name == "Super Admin":
                role.permissions.extend(permission_records.values())

            ## ---> Assign more permissions here <--- ##

            db.add(role)
            await db.commit()