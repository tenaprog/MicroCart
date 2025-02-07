import boto3
import os

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

BUCKET_NAME = "images"


def create_bucket():
    s3.create_bucket(Bucket=BUCKET_NAME)
    print(f"Bucket {BUCKET_NAME} created successfully.")


if __name__ == "__main__":
    create_bucket()
