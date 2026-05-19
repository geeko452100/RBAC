from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud.user import get_usr_by_usrname
from app.models.user import User
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = settings.SECRET_KEY
ALG = "HS256"

class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
    
    async def __call__(self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
        creds_excpt = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not verify credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        # Decode Token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALG])
            username: str = payload.get("sub")
            if username is None:
                raise creds_excpt
        except jwt.PyJWTError:
            raise creds_excpt

        # Get user from database
        user = await get_usr_by_usrname(db, username=username)
        if user is None:
            raise HTTPException(status_code=404, detail="User Not Found")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        
        # Check permissions
        user_permissions = [perm.name for perm in user.role.permissions] 
        if self.required_permission not in user_permissions:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission: '{self.required_permission}'"
            )
        return user

