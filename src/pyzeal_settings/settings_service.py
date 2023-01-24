"""
TODO

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
        TODO
        """
        ...

    @defaultContainer.setter
    def defaultContainer(self, value: ContainerTypes) -> None:
        """
        TODO
        """
        ...

    @property
    def defaultAlgorithm(self) -> AlgorithmTypes:
        """
        TODO
        """
        ...

    @defaultAlgorithm.setter
    def defaultAlgorithm(self, value: AlgorithmTypes) -> None:
        """
        TODO
        """
        ...

    @property
    def logLevel(self) -> LogLevel:
        """
        TODO
        """
        ...

    @logLevel.setter
    def logLevel(self, value: LogLevel) -> None:
        """
        TODO
        """
        ...
