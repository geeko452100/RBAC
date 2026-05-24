from pydantic import BaseModel

#  CORRECT SCHEMA
class RoleResponse(BaseModel):
    id: int   
    name: str 

    class Config:
        from_attributes = True