"""
Authors:\n
- Philipp Schuette\n
"""

import logging
from typing import Protocol

from .log_levels import LogLevel
from .config import initLogger


class Loggable(Protocol):
    """
    Mixin for combination with classes which support logging, in
    particular changing the logging level.
    """

    _logger: logging.Logger

    @property
    def logger(self) -> logging.Logger:
        """
        The logger instance associated with this Loggable class.

        :returns: the logger of this class
        :rtype: logging.Logger
        """
        if not hasattr(self, "_logger"):
            self._logger = initLogger(
                self.__module__.rsplit(".", maxsplit=1)[-1]
            )
            return self._logger
        return self._logger

    def setLevel(self, level: LogLevel) -> None:
        """
        Set the log level.

        :param level: the new log level
        :type level: pyzeal_logging.log_levels.LogLevel
        """
        self.logger.setLevel(level=level.value)
