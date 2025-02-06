import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, is_admin: bool, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + \
        (expires_delta if expires_delta else timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": user_id, "is_admin": is_admin, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    user_data = verify_access_token(token)
    if not user_data:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")
    return user_data


def check_permission(current_user: dict, user_id: str):
    if current_user.get("is_admin", True):
        return
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")


def check_admin(current_user: dict):
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=403, detail="Admin check failed: Missing 'is_admin' field")
