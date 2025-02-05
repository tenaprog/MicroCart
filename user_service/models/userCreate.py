from pydantic import EmailStr
from .userBase import UserBase


class UserCreate(UserBase):
    email: EmailStr
    password: str
