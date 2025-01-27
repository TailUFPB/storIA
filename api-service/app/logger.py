import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    logger = logging.getLogger("storIA_logger")
    logger.setLevel(logging.DEBUG)

    # Formatação padrão dos logs
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Cria diretório de logs, se não existir
    log_directory = "log"
    os.makedirs(log_directory, exist_ok=True)  # equivale a if not exists

    # Configura arquivo de log com rodízio (10 MB, 1 backup)
    log_file = os.path.join(log_directory, "storia.log")
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
    # Se quiser menos verbosidade no stdout, pode usar INFO ou WARNING
    stream_handler.setLevel(logging.INFO)

    # Garante que não adicionamos vários handlers duplicados caso setup_logger seja chamado mais de uma vez
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

# Logger pronto para uso em todo o projeto
storia_logger = setup_logger()
