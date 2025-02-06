import uuid
import boto3
import os
from typing import List, Optional

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


def create_product(product_data: dict) -> dict:
    product_id = str(uuid.uuid4())
    product_data["product_id"] = product_id
    table.put_item(Item=product_data)
    return product_data


def get_product_by_id(product_id: str) -> Optional[dict]:
    response = table.get_item(Key={"product_id": product_id})
    return response.get("Item")


def get_all_products() -> List[dict]:
    response = table.scan()
    return [item for item in response.get("Items", [])]


def update_product(product_id: str, update_expression: str, expression_attribute_values: dict):
    table.update_item(
        Key={"product_id": product_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW",
    )


def delete_product(product_id: str):
    table.delete_item(Key={"product_id": product_id})
