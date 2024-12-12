from flask import render_template, request
from story import Story_generator
from prometheus_client import Counter

# Criar instância do gerador de histórias
story_generator = Story_generator()

# Criar contadores de métricas Prometheus
REQUEST_COUNT = Counter('flask_app_requests_total', 'Total de requisições para o app', ['method', 'endpoint'])
ERROR_COUNT = Counter('flask_app_errors_total', 'Total de erros', ['method', 'endpoint'])

def init_routes(app):
    """Função para registrar as rotas no Flask"""

    @app.route("/")
    def hello():
        REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
        return render_template('index.html')

    @app.route("/submit", methods=["POST", "GET"])
    def submit():
        REQUEST_COUNT.labels(method=request.method, endpoint='/submit').inc()

        data = request.form
        input_text = data.get('text[]')
        size = int(data.get('length[]'))
        temperature = float(data.get('temperature[]'))

        try:
            story = story_generator.generate_story(input_text, size, temperature)
            return render_template('index.html', suggestion_text=story)
        except Exception as e:
            ERROR_COUNT.labels(method=request.method, endpoint='/submit').inc()
            return render_template('index.html', suggestion_text=f"Error generating story:\n{e}")

    @app.route("/social")
    def social():
        REQUEST_COUNT.labels(method='GET', endpoint='/social').inc()
        return render_template('social.html')

    @app.route("/members")
    def members():
        REQUEST_COUNT.labels(method='GET', endpoint='/members').inc()
        return render_template('members.html')
