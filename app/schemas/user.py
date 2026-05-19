from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role_id: int # Assign every user a unique ID to thier specific role

class UserResponse(UserBase):
    id: int
    is_active: bool
    role_id: int

    class Config:
        from_attributes = True # Allow Pydantic to parse the SQLAlchemy Objects