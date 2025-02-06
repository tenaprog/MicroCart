import json
import uuid
from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from models.userCreate import UserCreate
from models.userResponse import UserResponse
from utils.db import create_user, get_user_by_email
from utils.auth import hash_password, verify_password, create_access_token, verify_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register", response_model=UserResponse)
def register_user_route(user: UserCreate):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user.password)

    user_data = user.model_dump(exclude={"password"})
    user_data.update({
        "user_id": user_id,
        "password": hashed_password,
        "is_admin": user.is_admin if user.is_admin is not None else False
    })

    create_user(user_data)

    return UserResponse(**user_data)


@router.post("/login")
def login_user_route(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        user["user_id"], user.get("is_admin", False))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-token")
def verify_token_endpoint(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    user_data = verify_access_token(token)
    if not user_data:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")
    return {"message": "Token is valid", "user_data": json.dumps(user_data)}
