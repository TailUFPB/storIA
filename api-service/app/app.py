import os
from flask import Flask
from app.views import init_routes
from app.metrics import start_metrics
from app.logger import storia_logger
from werkzeug.middleware.proxy_fix import ProxyFix  

app = Flask(__name__, template_folder='templates')

# Configura o ProxyFix conforme necessário
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

# Inicializa as rotas e as métricas
init_routes(app)
start_metrics(app)

if __name__ == "__main__":
    try:
        storia_logger.info("Iniciando a aplicação Flask")
        host = os.environ.get("FLASK_HOST", "0.0.0.0")
        port = int(os.environ.get("FLASK_PORT", 5000))
        app.run(host=host, port=port)
    except Exception as e:
        storia_logger.error(f"Erro ao iniciar a aplicação Flask: {e}")
