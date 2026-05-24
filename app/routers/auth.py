from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud import user as usr
from app.schemas.user import UserCreate, UserResponse  # Cleaned duplicate import
from app.schemas.token import Token
from app.core.security import verify_pwd, create_tkn
from app.routers.dependencies import get_current_usr
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Register a fresh recruit, assigning them a base role ID 
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def new_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check to ensure the username doesn't already exist
    existing_user = await usr.get_usr_by_usrname(db, username=user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists."
        )
    
    # Upload the user's credentials to the database  
    return await usr.create_user(db=db, user_in=user_in)

# Endpoint to allow current employees to login 
@router.post("/login", response_model=Token)
async def returning_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # 1. Fetch user profile
    user = await usr.get_usr_by_usrname(db, username=form_data.username)
    
    # 2. Securely match credentials (Cleaned up the duplicate check)
    if not user or not verify_pwd(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is no longer active"
        )
    
    # 3. Build token authorization payload
    token_payload = {
        "sub": user.username,
        "role": user.role.name if user.role else "Employee"
    }
    
    # Generate and return signed JWT token
    access_tkn = create_tkn(data=token_payload)

    return {"access_token": access_tkn, "token_type": "bearer"}


# 🔒 ADD THIS TO THE BOTTOM: Guarded verification endpoint
@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_usr)
):
    """
    Guarded route that utilizes the get_current_usr dependency injection block.
    Extracts, decodes, and verifies the incoming bearer token context automatically.
    """
    return current_user