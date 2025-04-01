import os
import redis
from rq import Worker, Queue
from app.logger import storia_logger
from urllib.parse import urlparse

# Configuração Redis usando URL completa
redis_url = os.environ.get("REDIS_URL", "redis://redis:6379")
parsed_url = urlparse(redis_url)

# Conexão usando from_url que aceita URLs completas
redis_conn = redis.Redis.from_url(redis_url)
q = Queue(connection=redis_conn)

if __name__ == '__main__':
    try:
        storia_logger.info(f"Conectando ao Redis em: {parsed_url.hostname}:{parsed_url.port}")
        # Teste de conexão
        redis_conn.ping()
        
        worker = Worker([q], connection=redis_conn)
        storia_logger.info("Worker iniciado com sucesso!")
        worker.work()
        
    except Exception as e:
        storia_logger.error(f"Falha ao iniciar worker: {str(e)}")
        raise