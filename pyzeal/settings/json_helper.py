"""
TODO.

Authors:\n
- Philipp Schuette\n
"""

from json import JSONDecodeError, dump, load
from typing import Dict, Literal, Set, Tuple, Type, Union

from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.invalid_setting_exception import InvalidSettingException

# admissible keys when changing settings
tCoreSettingsKey = Union[
    Literal["defaultContainer"],
    Literal["defaultAlgorithm"],
    Literal["defaultEstimator"],
]
tSettingsKey = Union[
    Literal["logLevel"],
    Literal["verbose"],
    Literal["precision"],
]
# admissible types when assigning to settings properties
tCoreSettingsPropertyType = Union[
    ContainerTypes, AlgorithmTypes, EstimatorTypes
]
tSettingsPropertyType = Union[LogLevel, bool, Tuple[int, int]]


class JSONHelper:
    """
    Static helper class providing methods to read and manipulate json settings.
    """

    _coreSettings: Dict[
        tCoreSettingsKey,
        Union[
            Type[AlgorithmTypes], Type[ContainerTypes], Type[EstimatorTypes]
        ],
    ] = {
        "defaultAlgorithm": AlgorithmTypes,
        "defaultContainer": ContainerTypes,
        "defaultEstimator": EstimatorTypes,
    }
    _settings: Set[tSettingsKey] = {"logLevel", "verbose", "precision"}

    @staticmethod
    def createOrUpdateCoreSetting(
        filename: str,
        setting: tCoreSettingsKey,
        value: tCoreSettingsPropertyType,
    ) -> None:
        """
        Update a core setting or create a new one if no value had previously
        been set.

        :param filename: the json file to update
        :param setting: setting to create or update
        :param value: New setting value
        :raises InvalidSettingException: If the given value is invalid for the
            specified setting, an `InvalidSettingException` is raised.
        """
        currentSettings: Dict[tCoreSettingsKey, str] = {}
        try:
            with open(filename, "r", encoding="utf-8") as custom:
                currentSettings = load(custom)
        except FileNotFoundError:
            pass
        except JSONDecodeError as exc:
            raise InvalidSettingException(f"{filename=}") from exc

        if setting in JSONHelper._coreSettings:
            if not isinstance(value, JSONHelper._coreSettings[setting]):
                raise InvalidSettingException(setting)
            currentSettings[setting] = value.value
        else:
            raise InvalidSettingException(f"key={setting}")

        with open(filename, "w", encoding="utf-8") as custom:
            dump(currentSettings, custom, indent=4)

    @staticmethod
    def loadCoreSettingsFromFile(
        filename: str, settings: Dict[str, str]
    ) -> None:
        """
        Load the settings stored in `filename` into `settings`.

        :param filename: Settings file to load
        :param settings: Dict to store the read settings in
        """
        try:
            with open(filename, "r", encoding="utf-8") as settingsFile:
                for key, value in load(settingsFile).items():
                    if key not in JSONHelper._coreSettings:
                        continue
                    settings[key] = value
        except FileNotFoundError:
            pass

    @staticmethod
    def createOrUpdateSetting(
        filename: str, setting: tSettingsKey, value: tSettingsPropertyType
    ) -> None:
        """
        Update a setting or create a new setting if no value has been set yet.

        :param filename: the json file to update
        :param setting: setting to create or update
        :param value: New setting value
        :raises InvalidSettingException: If the given value is invalid for the
            specified setting, an `InvalidSettingException` is raised.
        """
        currentSettings: Dict[
            tSettingsKey, Union[str, bool, Tuple[int, int]]
        ] = {}
        try:
            with open(filename, "r", encoding="utf-8") as custom:
                currentSettings = load(custom)
        except FileNotFoundError:
            pass
        except JSONDecodeError as exc:
            raise InvalidSettingException(f"{filename=}") from exc

        if setting == "logLevel":
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

        with open(filename, "w", encoding="utf-8") as custom:
            dump(currentSettings, custom, indent=4)

    @staticmethod
    def loadSettingsFromFile(
        filename: str, settings: Dict[str, Union[str, bool, Tuple[int, int]]]
    ) -> None:
        """
        Load the settings stored in `filename` into `settings`.

        :param filename: File to load
        :param settings: Dict to store the read settings in
        """
        try:
            with open(filename, "r", encoding="utf-8") as settingsFile:
                for key, value in load(settingsFile).items():
                    if key not in JSONHelper._settings:
                        continue
                    if isinstance(value, list):
                        value = tuple(value)
                    settings[key] = value
        except FileNotFoundError:
            pass
