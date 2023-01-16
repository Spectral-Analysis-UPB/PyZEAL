"""
TODO
"""

from enum import Enum
import logging


class LogLevel(Enum):
    """
    Named constants for log levels. Simple wrapper for the constants defined in
    the standard library logging module.
    """

    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
