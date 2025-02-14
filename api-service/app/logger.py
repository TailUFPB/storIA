import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    logger = logging.getLogger("storIA_logger")
    logger.setLevel(logging.DEBUG)  # Em produção, considere usar INFO

    # Formatação padrão dos logs
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Criação do diretório de logs (garante que o diretório exista)
    log_directory = "/var/log/storIA"
    os.makedirs(log_directory, exist_ok=True)
    log_file = os.path.join(log_directory, "storia.log")

    # RotatingFileHandler para gravar logs em arquivo
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=1
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # StreamHandler para enviar logs ao stdout (útil em contêineres)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)

    # Garante que não adicionamos handlers duplicados se setup_logger for chamado mais de uma vez
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

# Logger pronto para uso em todo o projeto
storia_logger = setup_logger()
