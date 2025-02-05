from pydantic import EmailStr
from .userBase import UserBase


class UserResponse(UserBase):
    user_id: str
    email: EmailStr
