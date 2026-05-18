import logging


# Object aproach for logger factory
@DeprecationWarning("Use get_logger function instead of LoggerFactory class")
class LoggerFactory:
    def __init__(self):
        logging.basicConfig(level=logging.ERROR)
        pass

    def get_logger(self, namespace: str) -> logging.Logger:
        return logging.getLogger(namespace)


# ------------------------------------------------------------------------
# Function Approach for logger factory

DEFAULT_LOGGING_LEVEL = logging.ERROR


def get_logger(namespace: str) -> logging.Logger:
    logging.basicConfig(level=DEFAULT_LOGGING_LEVEL)
    return logging.getLogger(namespace)
