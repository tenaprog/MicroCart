FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sh -c "python create_buckets.py && python create_tables.py && uvicorn main:app --host 0.0.0.0 --port 8002"