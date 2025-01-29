# app/routes/main.py
from flask import Blueprint, render_template
from app.logger import storia_logger
from app.metrics.request_metrics import REQUEST_COUNT  # Métricas compartilhadas

# Cria um Blueprint para agrupar as rotas principais
main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def hello():
    """Rota principal que renderiza a página inicial."""
    # Incrementa o contador de requisições para a rota '/'
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    storia_logger.info("Rota '/' acessada")
    return render_template('index.html')

@main_bp.route("/health")
def health():
    """Rota de verificação de saúde da aplicação."""
    return "OK", 200