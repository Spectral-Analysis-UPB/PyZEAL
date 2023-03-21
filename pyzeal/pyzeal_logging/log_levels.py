"""
Module exposing named constants for log levels.

The constants in this module just act as a facade to their counterparts in the
standard library `logging` module.
"""

import logging
from enum import Enum


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
