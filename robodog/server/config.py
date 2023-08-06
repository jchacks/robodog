import logging
from typing import Optional

_LOGGER: Optional[logging.Logger] = None
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def configure_logging():
    global _LOGGER
    if _LOGGER is None:
        _LOGGER = logging.getLogger()
        streamhandler = logging.StreamHandler()
        formatter = logging.Formatter(LOGGING_FORMAT)
        streamhandler.setFormatter(formatter)
        _LOGGER.addHandler(streamhandler)
    return _LOGGER
