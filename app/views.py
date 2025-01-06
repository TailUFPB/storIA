from flask import render_template, request
from story import StoryGenerator  
from prometheus_client import Counter
from logger import storia_logger  # Importar o logger
import sys

# Criar instância do gerador de histórias
try:
    story_generator = StoryGenerator()
    storia_logger.info("Instância de Story_generator criada com sucesso")
except Exception as e:
    storia_logger.critical(f"Falha ao inicializar Story_generator: {e}")
    sys.exit(1)  # Interrompe a aplicação se o modelo não puder ser carregado

# Criar contadores de métricas Prometheus
REQUEST_COUNT = Counter(
    'flask_app_requests_total',
    'Total de requisições para o app',
    ['method', 'endpoint']
)
ERROR_COUNT = Counter(
    'flask_app_errors_total',
    'Total de erros',
    ['method', 'endpoint']
)

def init_routes(app):
    """Função para registrar as rotas no Flask"""

    @app.route("/")
    def hello():
        REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
        storia_logger.info("Rota '/' acessada")
        return render_template('index.html')

    @app.route("/submit", methods=["POST", "GET"])
    def submit():
        REQUEST_COUNT.labels(method=request.method, endpoint='/submit').inc()
        storia_logger.info(f"Rota '/submit' acessada com método {request.method}")

        data = request.form
        input_text_list = data.getlist('text[]')  # Obtém a lista de textos
        size_list = data.getlist('length[]')      # Obtém a lista de tamanhos
        temperature_list = data.getlist('temperature[]')  # Obtém a lista de temperaturas

        # Pega o primeiro valor de cada lista (assumindo que há pelo menos um valor)
        input_text = input_text_list[0] if input_text_list else None
        size = size_list[0] if size_list else None
        temperature = temperature_list[0] if temperature_list else None

        # Log recebimento dos dados
        storia_logger.debug(f"Dados recebidos: text='{input_text}', length='{size}', temperature='{temperature}'")

        # Tratamento de erros nas conversões
        try:
            size = int(size)
        except (TypeError, ValueError):
            size = 100  # Valor padrão
            storia_logger.warning(
                f"Valor inválido para 'length': {size}. Usando padrão: 100"
            )

        try:
            temperature = float(temperature)
        except (TypeError, ValueError):
            temperature = 1.0  # Valor padrão
            storia_logger.warning(
                f"Valor inválido para 'temperature': {temperature}. Usando padrão: 1.0"
            )

        try:
            if not input_text:
                raise ValueError("Texto inicial não fornecido.")

            story = story_generator.generate_story(input_text, size, temperature)
            storia_logger.info("História gerada com sucesso")
            return render_template('index.html', suggestion_text=story)
        except Exception as e:
            ERROR_COUNT.labels(method=request.method, endpoint='/submit').inc()
            storia_logger.error(f"Erro na rota '/submit': {e}")
            return render_template(
                'index.html',
                suggestion_text=f"Error generating story:\n{e}"
            )

    @app.route("/social")
    def social():
        REQUEST_COUNT.labels(method='GET', endpoint='/social').inc()
        storia_logger.info("Rota '/social' acessada")
        return render_template('social.html')

    @app.route("/members")
    def members():
        REQUEST_COUNT.labels(method='GET', endpoint='/members').inc()
        storia_logger.info("Rota '/members' acessada")
        return render_template('members.html')
