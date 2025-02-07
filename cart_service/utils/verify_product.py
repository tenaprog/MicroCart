import os
import requests
from fastapi import HTTPException

from models.cartItem import CartItem

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")


def verify_product_availability(cart_item: CartItem):
    response = requests.put(
        f"{PRODUCT_SERVICE_URL}/products/{cart_item.product_id}/update_quantity?quantity={cart_item.quantity}"
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )
