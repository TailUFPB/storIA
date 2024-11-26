FROM python:3.9.1

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app/app.py"]
