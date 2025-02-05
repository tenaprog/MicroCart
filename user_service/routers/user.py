from fastapi import APIRouter, HTTPException, Depends
from typing import List

from models.userResponse import UserResponse
from models.userUpdate import UserUpdate

from db_util import get_user_by_id, update_user, delete_user, list_users

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_data(user_id: str, user: UserUpdate):
    update_expression = []
    expression_attribute_values = {}

    for key, value in user.dict(exclude_unset=True).items():
        update_expression.append(f"{key} = :{key}")
        expression_attribute_values[f":{key}"] = value

    if not update_expression:
        raise HTTPException(
            status_code=400, detail="No data provided for update")

    update_expression = f"SET {', '.join(update_expression)}"
    update_user(user_id, update_expression, expression_attribute_values)

    return get_user_by_id(user_id)


@router.delete("/users/{user_id}", status_code=204)
def delete_user_data(user_id: str):
    delete_user(user_id)
    return {}


@router.get("/users", response_model=List[UserResponse])
def list_users_data():
    users = list_users()
    return users
