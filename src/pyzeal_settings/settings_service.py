"""
TODO

Authors:\n
- Philipp Schuette\n
"""

from json import dump, load
from os.path import dirname, join
from typing import Dict, Literal, Union

from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_logging.log_levels import LogLevel
from pyzeal_settings.invalid_setting_exception import InvalidSettingException


class SettingsService:
    """
    This class provides a layer of abstraction for storage and retrieval of
    PyZEAL related settings.
    """

    slots = ("_container", "_algorithm", "_level")

    def __init__(self) -> None:
        """
        Create an instance of a new `SettingsSerive`. The basis for its
        properties are the currently persisted (user or default) settings.
        """
        currentSettings: Dict[str, str] = {}
        # first load default settings (must always exist)...
        SettingsService.loadSettingsFromFile(
            join(dirname(__file__), "default_settings.json"), currentSettings
        )
        # ...then try to load custom settings (might not exist)
        SettingsService.loadSettingsFromFile(
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

    @property
    def defaultContainer(self) -> ContainerTypes:
        """
        TODO
        """
        return self._container

    @defaultContainer.setter
    def defaultContainer(self, value: ContainerTypes) -> None:
        """
        TODO
        """
        self._container = value
        SettingsService.createOrUpdateSetting("defaultContainer", value)

    @property
    def defaultAlgorithm(self) -> AlgorithmTypes:
        """
        TODO
        """
        return self._algorithm

    @defaultAlgorithm.setter
    def defaultAlgorithm(self, value: AlgorithmTypes) -> None:
        """
        TODO
        """
        self._algorithm = value
        SettingsService.createOrUpdateSetting("defaultAlgorithm", value)

    @property
    def logLevel(self) -> LogLevel:
        """
        TODO
        """
        return self._level

    @logLevel.setter
    def logLevel(self, value: LogLevel) -> None:
        """
        TODO
        """
        self._level = value
        SettingsService.createOrUpdateSetting("logLevel", value)

    @staticmethod
    def createOrUpdateSetting(
        setting: Union[
            Literal["defaultContainer"],
            Literal["defaultAlgorithm"],
            Literal["logLevel"],
        ],
        value: Union[ContainerTypes, AlgorithmTypes, LogLevel],
    ) -> None:
        """
        TODO
        """
        currentSettings: Dict[str, str] = {}
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
        else:
            raise InvalidSettingException("trying to set invalid setting key!")

        with open(
            join(dirname(__file__), "custom_settings.json"),
            "w",
            encoding="utf-8",
        ) as custom:
            dump(currentSettings, custom)

    @staticmethod
    def loadSettingsFromFile(filename: str, settings: Dict[str, str]) -> None:
        """
        TODO
        """
        try:
            with open(filename, "r", encoding="utf-8") as settingsFile:
                for key, value in load(settingsFile).items():
                    settings[key] = value
        except FileNotFoundError:
            pass
