FROM python:3.9-slim

WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --retries 5 --timeout 100 -r requirements.txt

# Instalar Gunicorn
RUN pip install gunicorn

# Copiar o código da API
COPY app/ ./app

# Ajustar PYTHONPATH para incluir o diretório /app
ENV PYTHONPATH="/app"

# Expor a porta
EXPOSE 5000

# Comando de inicialização
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]