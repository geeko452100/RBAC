from pydantic import BaseModel, Field
from typing import Optional

class PermissionBase(BaseModel):
    name: str = Field(..., max_length=50, description="Unique identifier for the permissions")
    description: Optional[str] = Field(None, max_length=200)

class PermissionResponse(PermissionBase):
    id: int

    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str = Field(..., max_length=50, description="Unique identifier for the role")
    
class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    permissions: list[PermissionResponse] = []

    class Config:
        from_attributes = True