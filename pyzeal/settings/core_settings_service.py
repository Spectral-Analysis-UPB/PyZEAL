"""
Class `CoreSettingsService` from the package `pyzeal_settings`.
This module defines a protocol for a generic settings provider pertaining to
the core features of `PyZEAL`.

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol, runtime_checkable

from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes


@runtime_checkable
class CoreSettingsService(Protocol):
    """
    Class providing a layer of abstraction for storage and retrieval of PyZEAL
    core settings. Concrete `SettingService` implementations can choose freely
    their data model and persistence layer.
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

        :param value: New default algorithm type.
        """
        ...

    @property
    def defaultEstimator(self) -> EstimatorTypes:
        """
        Get the default estimator type.

        :return: Default estimator type.
        """
        ...

    @defaultEstimator.setter
    def defaultEstimator(self, value: EstimatorTypes) -> None:
        """
        Set the default estimator type.

        :param value: New default estimator type.
        """
        ...
