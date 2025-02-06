import os
import requests
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_token_from_user_service(token: str, is_admin_check: bool):
    response = requests.get(
        f"{USER_SERVICE_URL}/verify-token", headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")

    user_data = response.json()

    if is_admin_check and not user_data.get("is_admin", True):
        raise HTTPException(status_code=403, detail="Not authorized as admin")

    return user_data
