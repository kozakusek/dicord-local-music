import logging
import os
from time import strftime, gmtime
from uuid import uuid4

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("DCLMB")
    logger.setLevel(logging.DEBUG)
    
    _setup_console_logging(logger)
    _setup_file_logging(logger)
    
    return logger

def _setup_console_logging(logger: logging.Logger):
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s')
    )
    logger.addHandler(ch)

def _setup_file_logging(logger: logging.Logger):
    fh = logging.FileHandler(f"logs/{_get_file_for_logging()}.txt")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter(
            '%(asctime)s [%(levelname)s]-[%(funcName)s]: %(message)s'
        )
    )
    logger.addHandler(fh)

def _get_file_for_logging() -> str:
    os.makedirs("logs", exist_ok=True)
    name = strftime("%Y-%m-%d_%H-%M-%S_", gmtime()) + str(uuid4())[:4]
    with open(f"logs/{name}.txt", "x"): pass

    return name