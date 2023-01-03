
import sys
import logging.config

LOGGING_DEFAULT_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGING_DEFAULT_LEVEL = logging.INFO


def setup(modeDebug=False):
    logLevel = LOGGING_DEFAULT_LEVEL
    logFormat = LOGGING_DEFAULT_FORMAT
    if modeDebug:
        logLevel = logging.DEBUG
    consolHandler = logging.StreamHandler(sys.stderr)

    logging.basicConfig(level=logLevel, format=logFormat, handlers=[consolHandler])
