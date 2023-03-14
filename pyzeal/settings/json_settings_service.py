"""
This module provides a straight-forward implementation of the `SettingsSerivce`
based on a `json` serialization backend.

Authors:\n
- Philipp Schuette\n
"""

from json import dump, load
from os.path import dirname, join
from typing import Dict, Final, Literal, Tuple, Union

from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.settings.invalid_setting_exception import InvalidSettingException
from pyzeal.settings.settings_service import SettingsService

# location where the default settings should be
DEFAULT_SETTINGS: Final[str] = join(dirname(__file__), "default_settings.json")
# default location where custom settings are saved
CUSTOM_SETTINGS: Final[str] = join(dirname(__file__), "custom_settings.json")

# admissible keys when changing settings
tSettingsKey = Union[
    Literal["defaultContainer"],
    Literal["defaultAlgorithm"],
    Literal["logLevel"],
    Literal["verbose"],
    Literal["precision"],
]
# admissible types when assigning to settings properties
tSettingsPropertyType = Union[
    ContainerTypes, AlgorithmTypes, LogLevel, bool, Tuple[int, int]
]


class JSONSettingsService(SettingsService):
    """
    This class provides a layer of abstraction for storage and retrieval of
    PyZEAL related settings using JSON for persistence. Any read and/or write
    access to settings must happen through a service like this one.
    """

    __slots__ = (
        "_container",
        "_algorithm",
        "_level",
        "_verbose",
        "_precision",
    )

    def __init__(self) -> None:
        """
        Create an instance of a new `SettingsService`. The basis for its
        properties are the currently persisted (user or default) settings.
        """
        currentSettings: Dict[str, Union[str, bool, Tuple[int, int]]] = {}
        # first load default settings (must always exist)...
        JSONSettingsService.loadSettingsFromFile(
            DEFAULT_SETTINGS, currentSettings
        )
        # ...then try to load custom settings (might not exist)
        JSONSettingsService.loadSettingsFromFile(
            CUSTOM_SETTINGS, currentSettings
        )

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

        for attr in self.__slots__:
            if not hasattr(self, attr):
                raise InvalidSettingException(attr[1:])

    def __str__(self) -> str:
        """
        A printable string representation of the currently active settings
        configuration.

        :return: string representation of current setting
        :rtype: str
        """
        return (
            "Currently active settings configuration:\n"
            + f"-> default container:   {self.defaultContainer.value}\n"
            + f"-> default algorithm:   {self.defaultAlgorithm.value}\n"
            + f"-> default log level:   {self.logLevel.name}\n"
            + f"-> default verbosity:   {self.verbose}"
        )

    # docstr-coverage:inherited
    @property
    def defaultContainer(self) -> ContainerTypes:
        return self._container

    @defaultContainer.setter
    def defaultContainer(self, value: ContainerTypes) -> None:
        self._container = value
        JSONSettingsService.createOrUpdateSetting("defaultContainer", value)

    # docstr-coverage:inherited
    @property
    def defaultAlgorithm(self) -> AlgorithmTypes:
        return self._algorithm

    @defaultAlgorithm.setter
    def defaultAlgorithm(self, value: AlgorithmTypes) -> None:
        self._algorithm = value
        JSONSettingsService.createOrUpdateSetting("defaultAlgorithm", value)

    # docstr-coverage:inherited
    @property
    def logLevel(self) -> LogLevel:
        return self._level

    @logLevel.setter
    def logLevel(self, value: LogLevel) -> None:
        self._level = value
        JSONSettingsService.createOrUpdateSetting("logLevel", value)

    # docstr-coverage:inherited
    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self._verbose = value
        JSONSettingsService.createOrUpdateSetting("verbose", value)

    # docstr-coverage:inherited
    @property
    def precision(self) -> Tuple[int, int]:
        return self._precision

    @precision.setter
    def precision(self, value: Tuple[int, int]) -> None:
        self._precision = value
        JSONSettingsService.createOrUpdateSetting("precision", value)

    @staticmethod
    def createOrUpdateSetting(
        setting: tSettingsKey, value: tSettingsPropertyType
    ) -> None:
        """
        Update a setting or create a new setting if no value has been set
        yet.

        :param setting: setting to create/update
        :type setting: Union[ Literal["defaultContainer"],
                              Literal["defaultAlgorithm"],
                              Literal["logLevel"],
                              Literal["verbose"], ]
        :param value: New setting value
        :type value: Union[ContainerTypes, AlgorithmTypes, LogLevel, bool]
        :raises InvalidSettingException: If the given value is invalid for the
            specified setting, an `InvalidSettingException` is raised.
        """
        currentSettings: Dict[
            tSettingsKey, Union[str, bool, Tuple[int, int]]
        ] = {}
        try:
            with open(
                join(dirname(__file__), "custom_settings.json"),
                "r",
                encoding="utf-8",
            ) as custom:
                currentSettings = load(custom)
        except FileNotFoundError:
            pass

        if setting == "defaultContainer":
            if not isinstance(value, ContainerTypes):
                raise InvalidSettingException("default container")
            currentSettings["defaultContainer"] = value.value
        elif setting == "defaultAlgorithm":
            if not isinstance(value, AlgorithmTypes):
                raise InvalidSettingException("default algorithm")
            currentSettings["defaultAlgorithm"] = value.value
        elif setting == "logLevel":
            if not isinstance(value, LogLevel):
                raise InvalidSettingException("default algorithm")
            currentSettings["logLevel"] = value.name
        elif setting == "verbose":
            if not isinstance(value, bool):
                raise InvalidSettingException("default verbosity")
            currentSettings["verbose"] = value
        elif setting == "precision":
            if not (
                isinstance(value, tuple)
                and isinstance(value[0], int)
                and isinstance(value[1], int)
            ):
                raise InvalidSettingException("default precision")
            currentSettings["precision"] = (value[0], value[1])
        else:
            raise InvalidSettingException(f"key={setting}")

        with open(
            join(dirname(__file__), "custom_settings.json"),
            "w",
            encoding="utf-8",
        ) as custom:
            dump(currentSettings, custom, indent=4)

    @staticmethod
    def loadSettingsFromFile(
        filename: str, settings: Dict[str, Union[str, bool, Tuple[int, int]]]
    ) -> None:
        """
        Load the settings stored in `filename` into `settings`.

        :param filename: File to load
        :type filename: str
        :param settings: Dict to store the read settings in
        :type settings: Dict[str, Union[str, bool, Tuple[int, int]]]
        """
        try:
            with open(filename, "r", encoding="utf-8") as settingsFile:
                for key, value in load(settingsFile).items():
                    if isinstance(value, list):
                        value = tuple(value)
                    settings[key] = value
        except FileNotFoundError:
            pass
