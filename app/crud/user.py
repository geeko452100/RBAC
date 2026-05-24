from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.schemas.user import UserCreate
from app.models.role import Role
from app.core.security import get_pwd_hsh

async def get_usr_by_usrname(db: AsyncSession, username: str) -> User | None:
    # Load the user's role and permissions pertaining to that role
    result = await db.execute(
        select(User)
        .where(User.username == username)
        #.options(selectinload(User.role).selectinload(Role.permissions))
    )
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    hashed_pwd = get_pwd_hsh(user_in.password)
    
    db_usr = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pwd,
        # role_id=user_in.role_id
    )   
    db.add(db_usr)
    await db.commit()
    await db.refresh(db_usr)
    return db_usr