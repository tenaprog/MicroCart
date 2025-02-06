from typing import Literal, Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    date_of_birth: str = Field(...,
                               description="Date of birth in YYYY-MM-DD format")
    gender: Literal['m', 'f', 'x'] = Field(
        'x', description="Gender: 'm' for male, 'f' for female, 'x' for others")
    is_admin: Optional[bool] = Field(
        False, description="Whether the user has admin privileges")
