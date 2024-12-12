FROM python:3.9.1 AS builder

WORKDIR /app

# Copiar apenas o arquivo de dependências
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Passo 3: Copiar o restante do código
COPY . .

EXPOSE 5000

CMD ["python", "app/app.py"]
