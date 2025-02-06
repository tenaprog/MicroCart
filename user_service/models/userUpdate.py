from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    date_of_birth: Optional[str] = Field(
        None, description="Date of birth in YYYY-MM-DD format")
    gender: Optional[Literal['m', 'f', 'x']] = Field(
        None, description="Gender: 'm' for male, 'f' for female, 'x' for others")
    is_admin: Optional[bool] = Field(
        None, description="Whether the user has admin privileges")
