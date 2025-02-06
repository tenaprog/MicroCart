from typing import List
from pydantic import BaseModel

from .cartItem import CartItem


class Cart(BaseModel):
    user_id: str
    cart_items: List[CartItem] = []
