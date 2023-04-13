"""
Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol

from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_logging.log_manager import LogManager
from pyzeal.pyzeal_logging.logger_facade import PyZEALLogger
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.service_locator import ServiceLocator


class Loggable(Protocol):
    """
    Mixin for combination with classes which support logging, in
    particular changing the logging level.
    """

    __slots__ = ("_logger",)

    _logger: PyZEALLogger

    @property
    def logger(self) -> PyZEALLogger:
        """
        The logger instance associated with this Loggable class. Instance
        creation happens upon first property access.

        :returns: the logger of this class
        """
        if not hasattr(self, "_logger"):
            self._logger = LogManager.initLogger(
                self.__module__.rsplit(".", maxsplit=1)[-1],
                ServiceLocator.tryResolve(SettingsService).logLevel,
            )
        return self._logger

    def setLevel(self, level: LogLevel) -> None:
        """
        Set the log level.

        :param level: the new log level
        """
        self.logger.setLevel(level=level.value)
