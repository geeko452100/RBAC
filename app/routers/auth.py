from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud import user as usr
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.core.security import verify_pwd, create_tkn

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Login endpoint
@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await usr.get_usr_by_usrname(db, username=form_data.username)
    if not user or not verify_pwd(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate and return signed JWT token
    access_tkn = create_tkn(data={"sub": user.username})

    return Token(access_token=access_tkn, token_type="bearer")

