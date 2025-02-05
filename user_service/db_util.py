import boto3
import os
from config import AWS_REGION, DYNAMODB_TABLE_NAME

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "your_access_key_id")
AWS_SECRET_ACCESS_KEY = os.getenv(
    "AWS_SECRET_ACCESS_KEY", "your_secret_access_key")
DYNAMODB_ENDPOINT_URL = os.getenv(
    "DYNAMODB_ENDPOINT_URL", "http://host.docker.internal:8000")

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=DYNAMODB_ENDPOINT_URL,
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def create_user(user_data: dict):
    """Create a new user."""
    try:
        table.put_item(Item=user_data)
    except Exception as e:
        print(f"Error creating user: {e}")
        raise


def get_user_by_email(email: str):
    """Retrieve user by email."""
    try:
        response = table.scan(
            FilterExpression="email = :email",
            ExpressionAttributeValues={":email": email}
        )

        if response["Items"]:
            return response["Items"][0]
        return None
    except Exception as e:
        print(f"Error retrieving user by email: {e}")
        return None


def get_user_by_id(user_id: str):
    try:
        response = table.get_item(Key={"user_id": user_id})
        return response.get("Item")
    except Exception as e:
        print(f"Error retrieving user by user_id: {e}")
        return None


def update_user(user_id: str, update_expression: str, expression_attribute_values: dict):
    try:
        response = table.update_item(
            Key={"user_id": user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
        )
        return response.get("Attributes")
    except Exception as e:
        print(f"Error updating user {user_id}: {e}")
        raise


def delete_user(user_id: str):
    try:
        response = table.delete_item(Key={"user_id": user_id})
        return response
    except Exception as e:
        print(f"Error deleting user {user_id}: {e}")
        raise


def list_users():
    try:
        response = table.scan()
        return response.get("Items", [])
    except Exception as e:
        print(f"Error listing users: {e}")
        return []
