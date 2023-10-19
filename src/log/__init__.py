import logging
import logging.config

logging.config.fileConfig('log/logging.conf')

def getLogger(name: str):
    return logging.getLogger(name)