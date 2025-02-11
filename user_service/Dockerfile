FROM python:3.8-slim

WORKDIR /app

COPY user_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY user_service/ .

ENV AWS_REGION=eu-north-1
ENV AWS_ACCESS_KEY_ID=dummy
ENV AWS_SECRET_ACCESS_KEY=dummy

EXPOSE 8001

CMD ["python", "main.py"] 
