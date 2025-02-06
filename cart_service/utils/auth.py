import json
import os
import requests
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_token_from_user_service(token: str):
    response = requests.get(
        f"{USER_SERVICE_URL}/verify-token", headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")

    response_data = response.json()
    user_data = json.loads(response_data["user_data"])
    user_id = user_data.get("sub")

    return user_id
