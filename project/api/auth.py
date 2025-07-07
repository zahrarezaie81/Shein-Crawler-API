import os
from datetime import datetime, timedelta
from typing import Union, Any
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt, JWTError

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "narscbjim@$@&^@&%^&RFghgjvbdsha")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY", "13ugfdfgh@#$%^@&jkl45678902")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: Union[str, int],
    expires_delta: timedelta = None
) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"exp": expire, "sub": str(subject), "role": str(role)}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(
    subject: Union[str, int],
    expires_delta: timedelta = None
) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    payload = {"exp": expire, "sub": str(subject)}
    return jwt.encode(payload, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, refresh: bool = False) -> dict | None:
    key = JWT_REFRESH_SECRET_KEY if refresh else JWT_SECRET_KEY
    try:
        return jwt.decode(token, key, algorithms=[ALGORITHM])
    except JWTError:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        cred: HTTPAuthorizationCredentials = await super().__call__(request)

        if not cred or cred.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme."
            )

        payload = decode_token(cred.credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is invalid or has expired."
            )

        return payload

    def verify_jwt(self, token: str) -> bool:
        return bool(decode_token(token))