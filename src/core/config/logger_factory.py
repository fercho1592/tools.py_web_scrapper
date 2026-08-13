import logging

DEFAULT_LOGGING_LEVEL = logging.ERROR


def get_logger(namespace: str) -> logging.Logger:
    logging.basicConfig(level=DEFAULT_LOGGING_LEVEL)
    return logging.getLogger(namespace)
