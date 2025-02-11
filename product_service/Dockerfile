FROM python:3.8-slim

WORKDIR /app

COPY ./product_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./product_service/ .

EXPOSE 800

CMD ["python", "main.py"]
