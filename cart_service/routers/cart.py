from fastapi import APIRouter, HTTPException, Depends

from fastapi.security import OAuth2PasswordBearer

from utils.db import add_to_cart, clear_cart, create_cart, get_cart, remove_from_cart
from models.cart import Cart
from models.cartItem import CartItem
from utils.auth import verify_token_from_user_service


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/cart", response_model=Cart)
def create_cart_route(token: str = Depends(oauth2_scheme)):
    user_id = verify_token_from_user_service(token)  # Fetch user_id from token
    cart = create_cart(user_id)
    return cart


@router.get("/cart", response_model=Cart)
def get_cart_route(token: str = Depends(oauth2_scheme)):
    user_id = verify_token_from_user_service(token)
    cart = get_cart(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/cart/add", response_model=Cart)
def add_to_cart_route(product: CartItem, token: str = Depends(oauth2_scheme)):
    user_id = verify_token_from_user_service(token)
    cart = add_to_cart(user_id, product.product_id, product.quantity)
    return cart


@router.post("/cart/remove", response_model=Cart)
def remove_from_cart_route(product: CartItem, token: str = Depends(oauth2_scheme)):
    user_id = verify_token_from_user_service(token)
    cart = remove_from_cart(user_id, product.product_id, product.quantity)
    return cart


@router.post("/cart/clear", response_model=Cart)
def clear_cart_route(token: str = Depends(oauth2_scheme)):
    user_id = verify_token_from_user_service(token)
    cart = clear_cart(user_id)
    return cart
