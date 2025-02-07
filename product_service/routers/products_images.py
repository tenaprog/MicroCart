import io
import boto3
import os
from fastapi import APIRouter, UploadFile, File, HTTPException

# TODO: from utils.verify_user import verify_token_from_user_service

router = APIRouter()

AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = "images"

s3 = boto3.client(
    "s3",
    endpoint_url=AWS_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


# curl.exe -X POST "http://localhost:8002/upload/" -F "file=@C:\Users\...\Screenshot.png"
@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    #    verify_token_from_user_service(token, True)
    try:
        file_content = await file.read()  # Read the file contents
        s3.upload_fileobj(io.BytesIO(file_content), BUCKET_NAME, file.filename)
        file_url = f"{AWS_ENDPOINT_URL}/{BUCKET_NAME}/{file.filename}"
        return {"message": "File uploaded successfully", "url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# curl.exe -X GET "http://localhost:8002/list/"
@router.get("/list/")
def list_images():
    #    verify_token_from_user_service(token, True)
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        files = [item["Key"] for item in response.get("Contents", [])]
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{filename}")
def delete_image(filename: str):
    #    verify_token_from_user_service(token, True)
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
