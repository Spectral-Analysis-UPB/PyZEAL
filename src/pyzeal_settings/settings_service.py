"""
Class `SettingsService` from the package `pyzeal_settings`.
This module defines a protocol for a generic settings provider.

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol

from pyzeal_logging.log_levels import LogLevel
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes


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
        :rtype: ContainerTypes
        """
        ...

    @defaultContainer.setter
    def defaultContainer(self, value: ContainerTypes) -> None:
        """
        Set the default container type to `value`.

        :param value: New default container type.
        :type value: ContainerTypes
        """
        ...

    @property
    def defaultAlgorithm(self) -> AlgorithmTypes:
        """
        Get the default algorithm type.

        :return: Default algorithm type.
        :rtype: AlgorithmTypes
        """
        ...

    @defaultAlgorithm.setter
    def defaultAlgorithm(self, value: AlgorithmTypes) -> None:
        """
        Set the default algorithm type to `value`.

        :param value: New default algorithm type
        :type value: AlgorithmTypes
        """
        ...

    @property
    def logLevel(self) -> LogLevel:
        """
        Get the current LogLevel setting.

        :return: Current LogLevel
        :rtype: LogLevel
        """
        ...

    @logLevel.setter
    def logLevel(self, value: LogLevel) -> None:
        """
        Set the LogLevel to `value`.

        :param value: New LogLevel to use
        :type value: LogLevel
        """
        ...

    @property
    def verbose(self) -> bool:
        """
        Get current verbosity setting.

        :return: True if verbose mode is enabled.
        :rtype: bool
        """
        ...

    @verbose.setter
    def verbose(self, value: bool) -> None:
        """
        Set the verbosity setting

        :param value: New verbosity setting
        :type value: bool
        """
        ...
