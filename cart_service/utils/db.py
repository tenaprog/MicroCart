import uuid
import boto3
import os
from typing import Dict, Optional

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL")

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=DYNAMODB_ENDPOINT_URL,
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def get_cart(user_id: str) -> Optional[Dict]:
    response = table.get_item(Key={"user_id": user_id})
    return response.get("Item")


def create_cart(user_id: str) -> Dict:
    cart = {"user_id": user_id, "cart_items": []}
    table.put_item(Item=cart)
    return cart


def add_to_cart(user_id: str, product_id: str, quantity: int) -> Dict:
    cart = get_cart(user_id)
    if not cart:
        cart = create_cart(user_id)

    existing_item = next(
        (item for item in cart["cart_items"] if item["product_id"] == product_id), None)
    if existing_item:
        existing_item["quantity"] += quantity
    else:
        cart["cart_items"].append(
            {"product_id": product_id, "quantity": quantity})

    table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET cart_items = :cart_items",
        ExpressionAttributeValues={":cart_items": cart["cart_items"]}
    )

    return cart


def remove_from_cart(user_id: str, product_id: str, quantity: int) -> Dict:
    cart = get_cart(user_id)
    if not cart:
        return {"message": "Cart not found"}

    existing_item = next(
        (item for item in cart["cart_items"] if item["product_id"] == product_id), None)

    if not existing_item:
        return {"message": "Product not found in cart"}

    if quantity >= existing_item["quantity"]:
        cart["cart_items"] = [item for item in cart["cart_items"]
                              if item["product_id"] != product_id]
    else:
        existing_item["quantity"] -= quantity

    table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET cart_items = :cart_items",
        ExpressionAttributeValues={":cart_items": cart["cart_items"]}
    )

    return cart


def clear_cart(user_id: str) -> Dict:
    cart = get_cart(user_id)
    if not cart:
        return {"message": "Cart not found"}

    cart["cart_items"] = []

    table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET cart_items = :cart_items",
        ExpressionAttributeValues={":cart_items": cart["cart_items"]}
    )

    return cart
