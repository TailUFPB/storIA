from flask import Flask
from app.views import init_routes
from app.metrics import start_metrics
from app.logger import storia_logger
from werkzeug.middleware.proxy_fix import ProxyFix  

app = Flask(__name__, template_folder='templates')

# Esses parâmetros indicam quantos valores de cada cabeçalho o ProxyFix deve confiar.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

# Inicializar rotas e métricas
init_routes(app)
start_metrics(app)

if __name__ == "__main__":
    try:
        storia_logger.info("Iniciando a aplicação Flask")
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        storia_logger.error(f"Erro ao iniciar a aplicação Flask: {e}")
