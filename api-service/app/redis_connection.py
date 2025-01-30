import redis
import sys
from app.logger import storia_logger

# Configuração e verificação da conexão com Redis
try:
    redis_client = redis.Redis(
        host='redis',
        port=6379,
        db=0,
        socket_connect_timeout=2,
        socket_timeout=2
    )
    redis_client.ping()  # Testa a conexão
    storia_logger.info("Conexão com Redis estabelecida com sucesso")
except redis.RedisError as e:
    storia_logger.critical(f"Falha na conexão com Redis: {e}")
    sys.exit(1)