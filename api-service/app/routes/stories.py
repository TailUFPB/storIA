from flask import Blueprint, request, render_template, g
from app.logger import storia_logger
from app.models.story import StoryGenerator
from app.utils.cache import redis_client
from app.metrics.request_metrics import REQUEST_COUNT, ERROR_COUNT, CACHE_HITS, CACHE_MISSES
import sys

# Cria um Blueprint para rotas de histórias
stories_bp = Blueprint('stories', __name__)

# Instância do gerador de histórias (singleton)
story_generator = StoryGenerator()

def generate_cache_key(text: str, size: int, temperature: float) -> str:
    """Gera chave única para cache (mantida aqui por ser específica desta funcionalidade)"""
    return f"cache:{text}:{size}:{temperature}"

@stories_bp.route("/submit", methods=["POST", "GET"])
def submit():
    """Rota principal para geração de histórias"""
    # Métricas
    REQUEST_COUNT.labels(method=request.method, endpoint='/submit').inc()
    storia_logger.info(f"Rota '/submit' acessada com método {request.method}")

    # Processamento dos parâmetros
    try:
        data = request.form
        input_text = data.getlist('text[]')[0] if data.getlist('text[]') else None
        size = int(data.getlist('length[]')[0]) if data.getlist('length[]') else 100
        temperature = float(data.getlist('temperature[]')[0]) if data.getlist('temperature[]') else 1.0
    except (ValueError, TypeError, IndexError) as e:
        ERROR_COUNT.labels(method=request.method, endpoint='/submit').inc()
        storia_logger.error(f"Parâmetros inválidos: {e}")
        return render_template('index.html', suggestion_text=f"Erro: Parâmetros inválidos - {e}")

    # Lógica de Cache
    cache_key = generate_cache_key(input_text, size, temperature)
    try:
        cached_story = redis_client.get(cache_key)
        if cached_story:
            CACHE_HITS.inc()
            storia_logger.info(f"Cache hit para chave: {cache_key}")
            return render_template('index.html', suggestion_text=cached_story.decode())
        
        CACHE_MISSES.inc()
        storia_logger.debug(f"Cache miss para chave: {cache_key}")
    except Exception as e:
        storia_logger.error(f"Erro no Redis: {e} - Continuando sem cache")

    # Geração da História
    try:
        if not input_text or input_text.strip() == "":
            raise ValueError("Texto inicial não pode ser vazio")

        story = story_generator.generate_story(input_text, size, temperature)
        
        # Armazenamento no Cache
        try:
            redis_client.setex(cache_key, 3600, story)  # 1 hora de expiração
            storia_logger.debug(f"História armazenada no cache: {cache_key}")
        except Exception as e:
            storia_logger.warning(f"Falha ao armazenar no cache: {e}")

        return render_template('index.html', suggestion_text=story)

    except Exception as e:
        ERROR_COUNT.labels(method=request.method, endpoint='/submit').inc()
        storia_logger.error(f"Erro na geração: {e}")
        return render_template('index.html', suggestion_text=f"Erro crítico: {str(e)}")