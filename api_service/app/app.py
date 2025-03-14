from flask import Flask
from app.views import init_routes
from app.metrics import start_metrics
from app.logger import storia_logger
from werkzeug.middleware.proxy_fix import ProxyFix  
from flask_cors import CORS
from flask import request
from flask import redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, template_folder='templates')
app.config['DEBUG'] = True

# --- uso de CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}}) # permissão de requisições a partir de todas as origens

# --- forçar requisições https (informações passadas no comando gunicorn para rodar)
@app.before_request # decorador para que a função execute antes de processar requisições
def force_https():
    if not request.is_secure: # is_secure() retorna True se requisição for HTTPS, False, HTTP
        return redirect(request.url.replace("http://", "https://"), code=301) # redireciona para usar HTTPS

# --- limitar requisições de único IP
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "40 per hour"]
)

# inicializa limiter com aplicação flask
limiter.init_app(app)

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