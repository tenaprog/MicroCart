import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://dynamodb:8000",
    region_name="eu-north-1",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

table_name = "cart"


def create_product_table():
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]

    if table_name in existing_tables:
        print(f"Table '{table_name}' already exists.")
        return

    print(f"Creating table '{table_name}'...")

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "user_id", "AttributeType": "S"}
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )

    table.wait_until_exists()
    print(f"Table '{table_name}' created successfully.")


if __name__ == "__main__":
    create_product_table()
