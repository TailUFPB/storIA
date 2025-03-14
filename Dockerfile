# dockerfile para aplicação em si
FROM python:3.9-slim

WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --retries 5 --timeout 100 -r requirements.txt

# Instalar Gunicorn
RUN pip install gunicorn

# Instalar flask-limiter
RUN pip install flask-limiter

# Copiar o código da API
COPY /api_service/app/ ./app
COPY /api_service/cert.pem .
COPY /api_service/key.pem .

# Ajustar PYTHONPATH para incluir o diretório /app
ENV PYTHONPATH="/app"

# Expor a porta
EXPOSE 5000

# Comando de inicialização
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app.app:app"]
# CMD ["gunicorn", "--certfile", "cert.pem", "--keyfile", "key.pem", "--bind", "0.0.0.0:5000", "--timeout", "120", "app.app:app"]
