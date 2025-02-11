FROM python:3.8-slim

WORKDIR /app

COPY ./cart_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./cart_service/ .

EXPOSE 8003

CMD ["python", "main.py"]
