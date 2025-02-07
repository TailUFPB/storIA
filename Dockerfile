FROM python:3.9.1 AS builder

WORKDIR /api-service

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY api-service .

EXPOSE 5000

CMD ["python", "app/app.py"]