from flask import render_template, request, jsonify
from app.logger import storia_logger
import redis
from rq import Queue
from rq.job import Job
from app.tasks import generate_story_job
from app.redis_connection import redis_client
from app.app_metrics import (
    REQUEST_COUNT,
    ERROR_COUNT,
    CACHE_HITS,
    CACHE_MISSES
)

# Cria a fila usando a conexão Redis existente
q = Queue(connection=redis_client)

# --- Função para Gerar Chave de Cache ---
def generate_cache_key(text, size, temperature):
    """
    Gera uma chave única para o cache com base no texto de entrada, tamanho e temperatura.
    """
    return f"cache:{text}:{size}:{temperature}"

# --- Rotas ---
def init_routes(app):
    @app.route("/")
    def hello():
        REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
        storia_logger.info("Rota '/' acessada")
        return render_template('index.html')

    @app.route("/submit", methods=["POST"])
    def submit():
        REQUEST_COUNT.labels(method=request.method, endpoint='/submit').inc()
        storia_logger.info(f"Rota '/submit' acessada com método {request.method}")

        # Processamento dos parâmetros
        data = request.form
        input_text = data.getlist('text[]')[0] if data.getlist('text[]') else None
        storia_logger.info(f"Texto de entrada: {input_text}")
        size = data.getlist('length[]')[0] if data.getlist('length[]') else 100
        temperature = data.getlist('temperature[]')[0] if data.getlist('temperature[]') else 1.0

        try:
            size = int(size)
            temperature = float(temperature)
        except (ValueError, TypeError) as e:
            ERROR_COUNT.labels(method=request.method, endpoint='/submit').inc()
            storia_logger.error(f"Parâmetros inválidos: {e}")
            return jsonify({"error": f"Parâmetros inválidos: {e}"}), 400

        if not input_text:
            return jsonify({"error": "Texto inicial não fornecido"}), 400

        # Verificar cache – se achar o resultado, retorna imediatamente
        cache_key = generate_cache_key(input_text, size, temperature)
        try:
            cached_story = redis_client.get(cache_key)
            if cached_story:
                CACHE_HITS.inc()
                storia_logger.info("Cache hit para chave: " + cache_key)
                return jsonify({"job_finished": True, "result": cached_story.decode()})
        except redis.RedisError as e:
            storia_logger.error(f"Erro no Redis: {e} - Continuando sem cache")
        CACHE_MISSES.inc()

        # Enfileirar o job
        job = q.enqueue(generate_story_job, input_text, size, temperature, job_timeout=180)
        storia_logger.info(f"Requisição enfileirada com ID: {job.id}")

        # Retorna o job_id para que o front-end inicie o polling
        return jsonify({"job_finished": False, "job_id": job.id})
    
    @app.route("/result/<job_id>")
    def get_result(job_id):
        try:
            job = Job.fetch(job_id, connection=redis_client)
            if job.is_finished:
                # Armazena o resultado no cache
                redis_client.setex(generate_cache_key(job.args[0], job.args[1], job.args[2]), 3600, job.result)
                storia_logger.info(f"Resultado armazenado em cache para chave: {generate_cache_key(job.args[0], job.args[1], job.args[2])}")
                # Resultado da requisição
                storia_logger.info(f"Requisição {job.result} finalizada")
                return jsonify({"status": "finished", "result": job.result})
            elif job.is_queued:
                storia_logger.info(f"Requisição {job_id} enfileirada")
                return jsonify({"status": "queued"})
            elif job.is_started:
                storia_logger.info(f"Requisição {job_id} em processamento")
                return jsonify({"status": "processing"})
            else:
                storia_logger.info(f"Requisição {job_id} com status desconhecido")
                return jsonify({"status": job.get_status()})
        except Exception as e:
            storia_logger.error(f"Erro ao consultar a Requisição {job_id}: {e}")
            return jsonify({"error": f"Erro ao consultar a requisição: {e}"}), 500
        
    @app.route("/health")
    def health():
        return "OK", 200

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
