import redis
from rq import Worker, Queue
from app.logger import storia_logger

# Conexão com o Redis 
redis_conn = redis.Redis(host='redis', port=6379, db=0)
q = Queue(connection=redis_conn)

if __name__ == '__main__':
    # Cria o worker passando a lista de filas e a conexão
    worker = Worker([q], connection=redis_conn)
    storia_logger.info("Worker iniciado...")
    worker.work()
