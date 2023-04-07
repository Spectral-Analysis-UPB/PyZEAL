"""
This module provides a straight-forward implementation of the `SettingsSerivce`
based on a `json` serialization backend.

Authors:\n
- Philipp Schuette\n
"""

from os.path import dirname, join
from typing import Dict, Final, Tuple, Union

from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.invalid_setting_exception import InvalidSettingException
from pyzeal.settings.json_core_settings import JSONCoreSettingsService
from pyzeal.settings.json_helper import JSONHelper
from pyzeal.settings.settings_service import SettingsService

# location where the default settings should be
DEFAULT_SETTINGS: Final[str] = join(dirname(__file__), "default_settings.json")
# default location where custom settings are saved
CUSTOM_SETTINGS: Final[str] = join(dirname(__file__), "custom_settings.json")


class JSONSettingsService(SettingsService):
    """
    This class provides a layer of abstraction for storage and retrieval of
    PyZEAL related settings using JSON for persistence. Any read and/or write
    access to settings must happen through a service like this one.
    """

    __slots__ = ("_coreSettings", "_level", "_verbose", "_precision")

    def __init__(self) -> None:
        """
        Create an instance of a new `SettingsService`. The basis for its
        properties are the currently persisted (user or default) settings.
        """
        self._coreSettings = JSONCoreSettingsService()
        currentSettings: Dict[str, Union[str, bool, Tuple[int, int]]] = {}
        # first load default settings (must always exist)...
        JSONHelper.loadSettingsFromFile(DEFAULT_SETTINGS, currentSettings)
        # ...then try to load custom settings (might not exist)
        JSONHelper.loadSettingsFromFile(CUSTOM_SETTINGS, currentSettings)

        # set default logging level
        for level in LogLevel:
            if level.name == currentSettings["logLevel"]:
                self._level = level

        # set default verbosity
        verbosity = currentSettings.get("verbose", None)
        if verbosity is not None:
            self._verbose = bool(verbosity)

        # set default precision
        precision = currentSettings.get("precision", None)
        if precision is not None:
            try:
                if isinstance(precision, tuple):
                    self._precision = (
                        precision[0],
                        precision[1],
                    )
            except ValueError:
                pass

        # check if required settings were loaded successfully
        for attr in self.__slots__:
            if not hasattr(self, attr):
                raise InvalidSettingException(attr[1:])

    def __str__(self) -> str:
        """
        A printable string representation of the currently active settings
        configuration.

        :return: string representation of current setting
        """
        return (
            f"Currently active settings configuration:\n{self._coreSettings}"
            f"-> default log level:   {self.logLevel.name}\n"
            f"-> default verbosity:   {self.verbose}\n"
            f"-> default precision:   {self.precision}"
        )

    # docstr-coverage:inherited
    @property
    def defaultContainer(self) -> ContainerTypes:
        return self._coreSettings.defaultContainer

    # docstr-coverage:inherited
    @defaultContainer.setter
    def defaultContainer(self, value: ContainerTypes) -> None:
        self._coreSettings.defaultContainer = value

    # docstr-coverage:inherited
    @property
    def defaultAlgorithm(self) -> AlgorithmTypes:
        return self._coreSettings.defaultAlgorithm

    # docstr-coverage:inherited
    @defaultAlgorithm.setter
    def defaultAlgorithm(self, value: AlgorithmTypes) -> None:
        self._coreSettings.defaultAlgorithm = value

    # docstr-coverage:inherited
    @property
    def defaultEstimator(self) -> EstimatorTypes:
        return self._coreSettings.defaultEstimator

    # docstr-coverage:inherited
    @defaultEstimator.setter
    def defaultEstimator(self, value: EstimatorTypes) -> None:
        self._coreSettings.defaultEstimator = value

    # docstr-coverage:inherited
    @property
    def logLevel(self) -> LogLevel:
        return self._level

    # docstr-coverage:inherited
    @logLevel.setter
    def logLevel(self, value: LogLevel) -> None:
        self._level = value
        JSONHelper.createOrUpdateSetting(CUSTOM_SETTINGS, "logLevel", value)

    # docstr-coverage:inherited
    @property
    def verbose(self) -> bool:
        return self._verbose

    # docstr-coverage:inherited
    @verbose.setter
    def verbose(self, value: bool) -> None:
        self._verbose = value
        JSONHelper.createOrUpdateSetting(CUSTOM_SETTINGS, "verbose", value)

    # docstr-coverage:inherited
    @property
    def precision(self) -> Tuple[int, int]:
        return self._precision

    # docstr-coverage:inherited
    @precision.setter
    def precision(self, value: Tuple[int, int]) -> None:
        self._precision = value
        JSONHelper.createOrUpdateSetting(CUSTOM_SETTINGS, "precision", value)
