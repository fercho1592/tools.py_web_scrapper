import logging

class LoggerFactory:
    def __init__(self):
        logging.basicConfig(level= logging.ERROR)
        pass

    def get_logger(self, namespace:str) -> logging.Logger:
        return logging.getLogger(namespace)
