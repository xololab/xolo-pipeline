# content   = Events Handler 
# date      = 03.25.2026
# author    = Ronny Ascencio <ronnyascencio.com>

import logging
import sys

def setup_logger(*, debug: bool = False, quiet: bool = False) -> logging.Logger:
    """
    Central logger configuration for Ateru Pipeline using built-in logging.
    """

    logger = logging.getLogger("ateru")
    logger.handlers.clear()  
    logger.propagate = False  

    if quiet:
        logger.disabled = True
        return logger

    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)


    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)


    formatter = logging.Formatter(_log_format())
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def _log_format() -> str:
    """
    Custom log format for Ateru Pipeline.
    """
  
    return "%(asctime)s | %(levelname)-7s | %(message)s"



logger = setup_logger()

def debug(msg: str):
    logger.debug(msg)

def info(msg: str):
    logger.info(msg)

def success(msg: str):
 
    logger.info(msg)

def warning(msg: str):
    logger.warning(msg)

def error(msg: str):
    logger.error(msg)