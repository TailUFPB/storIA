import redis
import sys
from app.logger import storia_logger
import os

try:
    redis_host = os.environ.get("REDIS_HOST", "redis")
    redis_port = int(os.environ.get("APP_REDIS_PORT", 6379))
    redis_client = redis.Redis(
        host=redis_host,
        port=redis_port,
        db=0,
        socket_connect_timeout=2,
        socket_timeout=2
    )
    redis_client.ping()  # Testa a conexão
    storia_logger.info("Conexão com Redis estabelecida com sucesso")
except redis.RedisError as e:
    storia_logger.critical(f"Falha na conexão com Redis: {e}")
    sys.exit(1)
