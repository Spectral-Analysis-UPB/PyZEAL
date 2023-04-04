"""
Class `SettingsService` from the package `pyzeal_settings`.
This module defines a protocol for a generic settings provider.

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol, Tuple, runtime_checkable

from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.settings.core_settings_service import CoreSettingsService


@runtime_checkable
class SettingsService(CoreSettingsService, Protocol):
    """
    Class providing a layer of abstraction for storage and retrieval of PyZEAL
    related settings. Concrete `SettingService` implementations can choose
    freely their data model and persistence layer.
    """

    @property
    def logLevel(self) -> LogLevel:
        """
        Get the current LogLevel setting.

        :return: Current LogLevel
        """
        ...

    @logLevel.setter
    def logLevel(self, value: LogLevel) -> None:
        """
        Set the LogLevel to `value`.

        :param value: New LogLevel to use
        """
        ...

    @property
    def verbose(self) -> bool:
        """
        Get current verbosity setting.

        :return: True if verbose mode is enabled.
        """
        ...

    @verbose.setter
    def verbose(self, value: bool) -> None:
        """
        Set the default verbosity setting.

        :param value: New verbosity setting
        """
        ...

    @property
    def precision(self) -> Tuple[int, int]:
        """
        Get current precision level as a negative exponent, i.e. a precision
        of 10^(-3), in real and imaginary parts respectively, corresponds
        to a precision level of (3, 3).

        :return: Current precision level
        """
        ...

    @precision.setter
    def precision(self, value: Tuple[int, int]) -> None:
        """
        Set the default precision level to `value`.

        :param value: New precision level
        """
        ...
