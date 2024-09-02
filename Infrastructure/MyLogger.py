import logging

logging.basicConfig(level= logging.INFO)

def GetLogger(name):
    logger = logging.getLogger(name)

    return logger