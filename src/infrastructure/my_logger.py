'''Logger setup'''

import logging

logging.basicConfig(level= logging.DEBUG)

def get_logger(name):
  logger = logging.getLogger(name)

  return logger
