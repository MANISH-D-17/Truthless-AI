from datetime import datetime, timedelta
from typing import Optional, Any
import hashlib
import hmac
import os
from jose import jwt
from app.core.config import settings

try:
    import bcrypt
    _HAS_BCRYPT = True
except ImportError:
    _HAS_BCRYPT = False

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        if hashed_password.startswith("$2b$") or hashed_password.startswith("$2a$"):
            if _HAS_BCRYPT:
                pwd_bytes = plain_password.encode('utf-8')[:72]
                return bcrypt.checkpw(pwd_bytes, hashed_password.encode('utf-8'))
            return False
        elif hashed_password.startswith("sha256$"):
            parts = hashed_password.split("$")
            salt, digest = parts[1], parts[2]
            calculated = hashlib.sha256(f"{salt}{plain_password}".encode('utf-8')).hexdigest()
            return hmac.compare_digest(calculated, digest)
        else:
            return False
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    if _HAS_BCRYPT:
        pwd_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')
    else:
        salt = os.urandom(16).hex()
        digest = hashlib.sha256(f"{salt}{password}".encode('utf-8')).hexdigest()
        return f"sha256${salt}${digest}"

def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
