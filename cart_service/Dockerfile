FROM python:3.8-slim

WORKDIR /app

COPY cart_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY cart_service/ .

ENV AWS_REGION=eu-north-1
ENV AWS_ACCESS_KEY_ID=dummy
ENV AWS_SECRET_ACCESS_KEY=dummy

EXPOSE 8003

CMD ["python", "main.py"]
