from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from app.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcript"], depreceated="auto")

# Import Constants
SECRET_KEY = settings.SECRET_KEY
ALG = "HS256"
ACCESS_TKN_EXPRY = settings.ACCESS_TKN_EXPRY

def verify_pwd(plain_pwd: str, hash_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hash_pwd)

# Generate the hashed password
def get_pwd_hsh(pwd: str) -> str:
    return pwd_context.hash(pwd)

# Create a perishable token that expires after a set timeframe if not 
def create_tkn(data: dict, expr_dlta: timedelta | None = None) -> str:
    to_encde = data.copy()
    if expr_dlta:
        expr = datetime.now(timezone.utc) + expr_dlta
    else: 
        expr = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TKN_EXPRY)
    to_encde.update({"exp": expr})
    return jwt.encode(to_encde, SECRET_KEY, algorithm=ALG)