from pydantic import BaseModel, EmailStr

# The fundamental user model
class UserBase(BaseModel):
    username: str
    email: EmailStr

# The User model for creating permissions
class UserCreate(UserBase):
    password: str
    role_id: int # Assign every user a unique ID to thier specific role

# The User model for retrieving permissions 
class UserResponse(UserBase):
    id: int
    is_active: bool
    role_id: int

    class Config:
        from_attributes = True # Parse the SQLAlchemy Objects