from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # bcrypt.checkpw requires bytes
        plain_pwd_bytes = plain_password.encode('utf-8')
        hashed_pwd_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_pwd_bytes, hashed_pwd_bytes)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    # bcrypt.hashpw requires bytes and returns bytes
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_pwd_bytes.decode('utf-8')


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload.get("sub")
    except JWTError:
        return None
