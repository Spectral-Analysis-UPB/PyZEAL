"""
Class JSONCoreSettingsService from the module `pyzeal.settings`.

This module provides a straight-forward implementation of the
`CoreSettingsSerivce` based on a `json` serialization backend.

Authors:\n
- Philipp Schuette\n
"""

from os.path import dirname, join
from typing import Dict, Final

from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.core_settings_service import CoreSettingsService
from pyzeal.settings.invalid_setting_exception import InvalidSettingException
from pyzeal.settings.json_helper import JSONHelper

# location where the default settings should be
DEFAULT_SETTINGS: Final[str] = join(dirname(__file__), "default_settings.json")
# default location where custom settings are saved
CUSTOM_SETTINGS: Final[str] = join(dirname(__file__), "custom_settings.json")


class JSONCoreSettingsService(CoreSettingsService):
    """
    This class provides a layer of abstraction for storage and retrieval of
    PyZEAL core settings using JSON for persistence. Any read and/or write
    access to (core) settings must happen through a service like this one.
    """

    __slots__ = ("_container", "_algorithm", "_estimator")

    def __init__(self) -> None:
        """
        Create an instance of a new `CoreSettingsService`. The basis for its
        properties are the currently persisted (user or default) settings.
        """
        currentSettings: Dict[str, str] = {}
        # first load default settings (must always exist)...
        JSONHelper.loadCoreSettingsFromFile(DEFAULT_SETTINGS, currentSettings)
        # ...then try to load custom settings (might not exist)
        JSONHelper.loadCoreSettingsFromFile(CUSTOM_SETTINGS, currentSettings)

        # set default container
        for container in ContainerTypes:
            if container.value == currentSettings["defaultContainer"]:
                self._container = container
                break

        # set default algorithm
        for algorithm in AlgorithmTypes:
            if algorithm.value == currentSettings["defaultAlgorithm"]:
                self._algorithm = algorithm
                break

        # set default estimator
        for estimator in EstimatorTypes:
            if estimator.value == currentSettings["defaultEstimator"]:
                self._estimator = estimator
                break

        # check if required defaults were loaded successfully
        for attr in self.__slots__:
            if not hasattr(self, attr):
                raise InvalidSettingException(attr[1:])

    def __str__(self) -> str:
        """
        A printable string representation of the currently active core settings
        configuration.

        :return: string representation of current core setting
        """
        return (
            f"-> default container:   {self.defaultContainer.value}\n"
            f"-> default algorithm:   {self.defaultAlgorithm.value}\n"
            f"-> default estimator:   {self.defaultEstimator.value}\n"
        )

    # docstr-coverage:inherited
    @property
    def defaultContainer(self) -> ContainerTypes:
        return self._container

    # docstr-coverage:inherited
    @defaultContainer.setter
    def defaultContainer(self, value: ContainerTypes) -> None:
        self._container = value
        JSONHelper.createOrUpdateCoreSetting(
            CUSTOM_SETTINGS, "defaultContainer", value
        )

    # docstr-coverage:inherited
    @property
    def defaultAlgorithm(self) -> AlgorithmTypes:
        return self._algorithm

    # docstr-coverage:inherited
    @defaultAlgorithm.setter
    def defaultAlgorithm(self, value: AlgorithmTypes) -> None:
        self._algorithm = value
        JSONHelper.createOrUpdateCoreSetting(
            CUSTOM_SETTINGS, "defaultAlgorithm", value
        )

    # docstr-coverage:inherited
    @property
    def defaultEstimator(self) -> EstimatorTypes:
        return self._estimator

    # docstr-coverage:inherited
    @defaultEstimator.setter
    def defaultEstimator(self, value: EstimatorTypes) -> None:
        self._estimator = value
        JSONHelper.createOrUpdateCoreSetting(
            CUSTOM_SETTINGS, "defaultEstimator", value
        )
