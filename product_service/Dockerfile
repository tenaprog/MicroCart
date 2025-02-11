FROM python:3.8-slim

WORKDIR /app

COPY product_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY product_service/ .

ENV AWS_REGION=eu-north-1
ENV AWS_ACCESS_KEY_ID=dummy
ENV AWS_SECRET_ACCESS_KEY=dummy
ENV AWS_ENDPOINT_URL=http://localstack:4566

EXPOSE 8002

CMD ["python", "main.py"]
