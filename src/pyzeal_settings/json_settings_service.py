"""
This module provides a straight-forward implementation of the `SettingsSerivce`
based on a `json` serialization backend.

Authors:\n
- Philipp Schuette\n
"""

from json import dump, load
from os.path import dirname, join
from typing import Dict, Literal, Tuple, Union

from pyzeal_logging.log_levels import LogLevel
from pyzeal_settings.invalid_setting_exception import InvalidSettingException
from pyzeal_settings.settings_service import SettingsService
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes


class JSONSettingsService(SettingsService):
    """
    This class provides a layer of abstraction for storage and retrieval of
    PyZEAL related settings using JSON for persistence. Any read and/or write
    access to settings must happen through a service like this one.
    """

    slots = ("_container", "_algorithm", "_level", "_verbose", "_precision")

    def __init__(self) -> None:
        """
        Create an instance of a new `SettingsService`. The basis for its
        properties are the currently persisted (user or default) settings.
        """
        currentSettings: Dict[str, Union[str, bool, Tuple[int, int]]] = {}
        # first load default settings (must always exist)...
        JSONSettingsService.loadSettingsFromFile(
            join(dirname(__file__), "default_settings.json"), currentSettings
        )
        # ...then try to load custom settings (might not exist)
        JSONSettingsService.loadSettingsFromFile(
            join(dirname(__file__), "custom_settings.json"), currentSettings
        )

        # set default container
        for container in ContainerTypes:
            if container.value == currentSettings["defaultContainer"]:
                self._container = container
                break
        if not hasattr(self, "_container"):
            raise InvalidSettingException(
                "invalid setting for default container!"
            )
        # set default algorithm
        for algorithm in AlgorithmTypes:
            if algorithm.value == currentSettings["defaultAlgorithm"]:
                self._algorithm = algorithm
                break
        if not hasattr(self, "_algorithm"):
            raise InvalidSettingException(
                "invalid setting for default algorithm!"
            )
        # set default logging level
        for level in LogLevel:
            if level.name == currentSettings["logLevel"]:
                self._level = level
        if not hasattr(self, "_level"):
            raise InvalidSettingException(
                "invalid setting for default logging level!"
            )
        # set default verbosity
        verbosity = currentSettings.get("verbose", None)
        if verbosity is not None:
            self._verbose = bool(verbosity)
        # set default precision
        if "precision" in currentSettings:
            precision = currentSettings["precision"]
            if isinstance(precision, tuple):
                if isinstance(precision[0], int) and isinstance(
                    precision[1], int
                ):
                    self._precision = (
                        precision[0],
                        precision[1],
                    )
        if not hasattr(self, "_precision"):
            raise InvalidSettingException(
                "invalid setting for default precision!"
            )

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

    @property
    def defaultContainer(self) -> ContainerTypes:
        "Get the currently active default container."
        return self._container

    @defaultContainer.setter
    def defaultContainer(self, value: ContainerTypes) -> None:
        self._container = value
        JSONSettingsService.createOrUpdateSetting("defaultContainer", value)

    @property
    def defaultAlgorithm(self) -> AlgorithmTypes:
        "Get the currently active default algorithm."
        return self._algorithm

    @defaultAlgorithm.setter
    def defaultAlgorithm(self, value: AlgorithmTypes) -> None:
        self._algorithm = value
        JSONSettingsService.createOrUpdateSetting("defaultAlgorithm", value)

    @property
    def logLevel(self) -> LogLevel:
        "Get the currently active standard log level."
        return self._level

    @logLevel.setter
    def logLevel(self, value: LogLevel) -> None:
        self._level = value
        JSONSettingsService.createOrUpdateSetting("logLevel", value)

    @property
    def verbose(self) -> bool:
        "Get the currently active verbosity level."
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self._verbose = value
        JSONSettingsService.createOrUpdateSetting("verbose", value)

    @property
    def precision(self) -> Tuple[int, int]:
        return self._precision

    @precision.setter
    def precision(self, value: Tuple[int, int]):
        self._precision = value
        JSONSettingsService.createOrUpdateSetting("precision", value)

    @staticmethod
    def createOrUpdateSetting(
        setting: Union[
            Literal["defaultContainer"],
            Literal["defaultAlgorithm"],
            Literal["logLevel"],
            Literal["verbose"],
            Literal["precision"],
        ],
        value: Union[
            ContainerTypes, AlgorithmTypes, LogLevel, bool, Tuple[int, int]
        ],
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
        currentSettings: Dict[str, Union[str, bool, Tuple[int, int]]] = {}
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
            if isinstance(value, ContainerTypes):
                currentSettings["defaultContainer"] = value.value
            else:
                raise InvalidSettingException(
                    "setting invalid value for default container!"
                )
        elif setting == "defaultAlgorithm":
            if isinstance(value, AlgorithmTypes):
                currentSettings["defaultAlgorithm"] = value.value
            else:
                raise InvalidSettingException(
                    "setting invalid value for default algorithm!"
                )
        elif setting == "logLevel":
            if isinstance(value, LogLevel):
                currentSettings["logLevel"] = value.name
            else:
                raise InvalidSettingException(
                    "setting invalid value for default algorithm!"
                )
        elif setting == "verbose":
            if isinstance(value, bool):
                currentSettings["verbose"] = value
            else:
                raise InvalidSettingException(
                    "setting invalid value for default verbosity!"
                )
        elif setting == "precision":
            if isinstance(value, tuple):
                if isinstance(value[0], int) and isinstance(value[1], int):
                    currentSettings["precision"] = (value[0], value[1])
                else:
                    raise InvalidSettingException(
                        "setting invalid value for default precision!"
                    )
            else:
                raise InvalidSettingException(
                    "setting invalid value for default precision!"
                )
        else:
            raise InvalidSettingException("trying to set invalid setting key!")

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
                    if key == "precision":  # precision is loaded as a list
                        value = (value[0], value[1])  # convert to tuple
                    settings[key] = value
        except FileNotFoundError:
            pass
