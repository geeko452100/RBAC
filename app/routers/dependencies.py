import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.security import SECRET_KEY, ALG
from app.crud.user import get_usr_by_usrname
from app.models.user import User
from app.schemas.token import TokenData


# Tell FastApi to look for a token at the specified endpoint
oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_usr(
        token: str = Depends(oauth2),
        db: AsyncSession = Depends(get_db)
) -> User:
    """
    Decodes the JWT token, extracting the user identitiy, 
    as well as validating them against the live db
    """
    creds_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="We do not recognize that login. Do you have an account?",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try: 
        # Decode token using security config
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALG])
        username: str = payload.get("sub")
        if username is None:
            raise creds_exception
        
        token_data = TokenData(username=username)
    except (jwt.PyJWTError, ValueError):
        raise creds_exception

    # Check the user against the db
    user = await get_usr_by_usrname(db, username=token_data.username)
    if user is None:
        raise creds_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="We're sorry, but it seems as though that account is no longer active."
        )
    
    # Return the user object to grant the user access to their account and permissions
    print(f"Logged in successfully as user: {username}")
    return user