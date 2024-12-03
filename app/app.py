from flask import Flask, render_template, request
from story import Story_generator
from prometheus_client import Counter, generate_latest, REGISTRY
import os


story_generator = Story_generator()

app = Flask(__name__, template_folder='templates')

# Métricas Prometheus
REQUEST_COUNT = Counter('flask_app_requests_total', 'Total de requisições para o app', ['method', 'endpoint'])
ERROR_COUNT = Counter('flask_app_errors_total', 'Total de erros', ['method', 'endpoint'])

# Endpoint principal
@app.route("/")
def hello():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return render_template('index.html')

# Endpoint para envio de dados
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

# Endpoint para página social
@app.route("/social")
def social():
    REQUEST_COUNT.labels(method='GET', endpoint='/social').inc()
    return render_template('social.html')

# Endpoint para página de membros
@app.route("/members")
def members():
    REQUEST_COUNT.labels(method='GET', endpoint='/members').inc()
    return render_template('members.html')

# Endpoint de métricas Prometheus
@app.route("/metrics")
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; charset=utf-8'}

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
