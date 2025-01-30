from flask import render_template, request
from app.logger import storia_logger
import redis
from app.story import StoryGenerator
from app.redis_connection import redis_client 
from app.app_metrics import (
    REQUEST_COUNT,
    ERROR_COUNT,
    CACHE_HITS,
    CACHE_MISSES
)

# --- Função para Gerar Chave de Cache ---
def generate_cache_key(text, size, temperature):
    """
    Gera uma chave única para o cache com base no texto de entrada, tamanho e temperatura.
    
    Args:
        text (str): O texto inicial para gerar a história.
        size (int): O tamanho desejado da história.
        temperature (float): A temperatura para o modelo de geração de texto.
    
    Returns:
        str: Uma chave única para o cache.
    """
    return f"cache:{text}:{size}:{temperature}"

# --- Instanciar o Gerador de Histórias ---
story_generator = StoryGenerator()

# --- Rotas ---
def init_routes(app):
    @app.route("/")
    def hello():
        REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
        storia_logger.info("Rota '/' acessada")
        return render_template('index.html')

    @app.route("/submit", methods=["POST", "GET"])
    def submit():
        REQUEST_COUNT.labels(method=request.method, endpoint='/submit').inc()
        storia_logger.info(f"Rota '/submit' acessada com método {request.method}")

        # Processamento dos parâmetros
        data = request.form
        input_text = data.getlist('text[]')[0] if data.getlist('text[]') else None
        size = data.getlist('length[]')[0] if data.getlist('length[]') else 100
        temperature = data.getlist('temperature[]')[0] if data.getlist('temperature[]') else 1.0

        # Validação e conversão
        try:
            size = int(size)
            temperature = float(temperature)
        except (ValueError, TypeError) as e:
            ERROR_COUNT.labels(method=request.method, endpoint='/submit').inc()
            storia_logger.error(f"Parâmetros inválidos: {e}")
            return render_template('index.html', suggestion_text=f"Erro: Parâmetros inválidos - {e}")

        # Verificação de cache
        cache_key = generate_cache_key(input_text, size, temperature)
        try:
            cached_story = redis_client.get(cache_key)
            if cached_story:
                CACHE_HITS.inc()
                storia_logger.info("Cache hit para chave: " + cache_key)
                return render_template('index.html', suggestion_text=cached_story.decode())
            
            CACHE_MISSES.inc()
            storia_logger.debug("Cache miss para chave: " + cache_key)

        except redis.RedisError as e:
            storia_logger.error(f"Erro no Redis: {e} - Continuando sem cache")

        # Geração da história usando o StoryGenerator interno
        try:
            if not input_text:
                raise ValueError("Texto inicial não fornecido")

            story = story_generator.generate_story(input_text, size, temperature)
            
            # Armazenamento no cache
            try:
                redis_client.setex(cache_key, 3600, story)  # 1 hora de cache
                storia_logger.debug("Resultado armazenado no cache")
            except redis.RedisError as e:
                storia_logger.warning(f"Falha ao armazenar no cache: {e}")

            return render_template('index.html', suggestion_text=story)

        except Exception as e:
            ERROR_COUNT.labels(method=request.method, endpoint='/submit').inc()
            storia_logger.error(f"Erro na geração da história: {e}")
            return render_template('index.html', suggestion_text=f"Erro ao gerar história: {e}")

    @app.route("/health")
    def health():
        return "OK", 200

    # Rotas estáticas mantidas
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
