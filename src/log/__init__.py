import logging
import logging.config

logging.config.fileConfig('src/log/logging.conf')

def getLogger(name: str):
    return logging.getLogger(name)