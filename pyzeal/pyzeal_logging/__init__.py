"""
Logging framework of the `PyZEAL` project.

This module exposes a simple logging facade and a `LogManager` which should be
used for any project-internal logging, e.g. in algorithms, root finders, or
plugins.
"""

from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_logging.logger_facade import PyZEALLogger

__all__ = [
    "LogLevel",
    "PyZEALLogger",
]
