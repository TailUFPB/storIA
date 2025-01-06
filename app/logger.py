import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    logger = logging.getLogger("storIA_logger")
    logger.setLevel(logging.DEBUG) 

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    log_directory = "log"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory) 
    log_file = os.path.join(log_directory, "storia.log")

    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=1
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger

storia_logger = setup_logger()