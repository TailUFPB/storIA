from flask import Flask
from views import init_routes
from metrics import start_metrics

app = Flask(__name__, template_folder='templates')

# Inicializar rotas e métricas
init_routes(app)
start_metrics(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
