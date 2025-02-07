from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from utils.db import add_to_cart, clear_cart, create_cart, get_cart, remove_from_cart
from utils.verify_product import verify_product_availability
from utils.verify_user import verify_token_from_user_service

from models.cart import Cart
from models.cartItem import CartItem


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/cart", response_model=Cart)
def create_cart_route(token: str = Depends(oauth2_scheme)):
    user_id = verify_token_from_user_service(token)
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
def add_to_cart_route(cart_item: CartItem, token: str = Depends(oauth2_scheme)):
    user_id = verify_token_from_user_service(token)
    verify_product_availability(cart_item)
    cart = add_to_cart(user_id, cart_item.product_id, cart_item.quantity)
    return cart


@router.post("/cart/remove", response_model=Cart)
def remove_from_cart_route(cart_item: CartItem, token: str = Depends(oauth2_scheme)):
    user_id = verify_token_from_user_service(token)
    cart = remove_from_cart(user_id, cart_item.product_id, cart_item.quantity)
    return cart


@router.post("/cart/clear", response_model=Cart)
def clear_cart_route(token: str = Depends(oauth2_scheme)):
    user_id = verify_token_from_user_service(token)
    cart = clear_cart(user_id)
    return cart
