"""
Class `SettingsService` from the package `pyzeal_settings`.
This module defines a protocol for a generic settings provider.

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol, Tuple, runtime_checkable

from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes


@runtime_checkable
class SettingsService(Protocol):
    """
    This class provides a layer of abstraction for storage and retrieval of
    PyZEAL related settings. Concrete `SettingService` implementations can
    choose freely their data model and persistence layer.
    """

    @property
    def defaultContainer(self) -> ContainerTypes:
        """
        Get the default container type.

        :return: Default container type
        """
        ...

    @defaultContainer.setter
    def defaultContainer(self, value: ContainerTypes) -> None:
        """
        Set the default container type to `value`.

        :param value: New default container type.
        """
        ...

    @property
    def defaultAlgorithm(self) -> AlgorithmTypes:
        """
        Get the default algorithm type.

        :return: Default algorithm type.
        """
        ...

    @defaultAlgorithm.setter
    def defaultAlgorithm(self, value: AlgorithmTypes) -> None:
        """
        Set the default algorithm type to `value`.

        :param value: New default algorithm type
        """
        ...

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
