import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.userCreate import UserCreate
from models.userResponse import UserResponse

from db_util import create_user, get_user_by_email
from auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user_route(user: UserCreate):
    """Registers a new user."""
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
