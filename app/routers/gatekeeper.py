from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.routers.dependencies import get_current_usr

class PermissionChecker:
    def __init__(self, required_perm: str):
        """
        Accepts the specific permission string required to access an endpoint.
        Example: "employee:create", "payroll:view" 
        """
        self.required_perm = required_perm

    def __call__(self, current_usr: User = Depends(get_current_usr)) -> User:
        """
        Executes during the request lifecycle to evaluate users's RBAC matrix
        """
        # Fallback security: If the user somehow has no role, deny access immediately
        if not current_usr.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Denied: User has no role assigned. Please contact your supervisor for more information."
            )
        
        # Admin Bypass: GOD-Mode check. Admin get's full access
        if current_usr.role.name == "Admin":
            return current_usr
        
        # Extract all permissions assigned to the user's role
        assigned_perms = {perm.name for perm in current_usr.role.permissions}

        # Enforce boundaries
        if self.required_perm not in assigned_perms:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access Denied: Missing required permission '{self.required_perm}'."
            )
        
        return current_usr
