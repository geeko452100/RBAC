from datetime import datetime, timedelta, timezone
import hashlib
import secrets
import jwt 
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALG = "HS256"
ACCESS_TKN_EXPRY = settings.ACCESS_TKN_EXPRY

# 🛠️ Hashing algorithim using Python's standard library
def get_pwd_hsh(pwd: str) -> str:
    # Hash the password securely using pbkdf2 with sha-256 and a random salt
    salt =secrets.token_hex(16)
    pwd_bytes = pwd.encode("utf-8")

    # Run 600,000 iterations of SHA-256 to create the industry-standard security the application needs
    db_hash = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt.encode('utf-8'), 600000).hex()

    # Store BOTH the salt and the hash together in the string
    return f"{salt}:{db_hash}"

def verify_pwd(plain_pwd: str, hash_pwd: str) -> bool:
    # Verify an incoming password against the stored salt:hash string
    try:
        # Split the stored string back into the original salt:hash
        salt, stored_hash = hash_pwd.split(":")

        pwd_bytes = plain_pwd.encode("utf-8")
        # Hash the incoming logic passwd using the very same salt
        new_hash = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt.encode('utf-8'), 600000).hex()

        # Compare the two securely
        return secrets.compare_digest(new_hash, stored_hash)
    except (ValueError, AttributeError):
        return False

def create_tkn(data: dict, expr_dlta: timedelta | None = None) -> str:
    to_encde = data.copy()
    if expr_dlta:
        expr = datetime.now(timezone.utc) + expr_dlta
    else: 
        expr = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TKN_EXPRY)
    to_encde.update({"exp": expr})
    return jwt.encode(to_encde, SECRET_KEY, algorithm=ALG)