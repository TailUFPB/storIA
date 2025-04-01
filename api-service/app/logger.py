import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    logger = logging.getLogger("storIA_logger")
    log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
    logger.setLevel(getattr(logging, log_level, logging.DEBUG))

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    log_directory = os.environ.get("LOG_DIR", "/var/log/storia")
    os.makedirs(log_directory, exist_ok=True)
    log_file = os.path.join(log_directory, "storia.log")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=1
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, log_level, logging.DEBUG))

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(getattr(logging, log_level, logging.DEBUG))

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

storia_logger = setup_logger()
