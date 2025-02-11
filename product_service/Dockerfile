FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8002
CMD ["sh", "-c", "python create_buckets.py & python create_tables.py && uvicorn main:app --host 0.0.0.0 --port 8002"]
