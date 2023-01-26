"""
This module provides the main CLI entry point of the PyZEAL project through the
function `mainPyZEAL`. At the moment it provides facilities to query the
currently installed PyZEAL version as well as view and manipulate settings.

Authors:\n
- Philipp Schuette\n
"""

from sys import argv
from typing import Optional

from pyzeal_cli.cli_parser import PyZEALParser
from pyzeal_logging.log_levels import LogLevel
from pyzeal_settings.json_settings_service import JSONSettingsService
from pyzeal_settings.settings_service import SettingsService
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes


def mainPyZEAL() -> None:
    """
    Main entry point for the CLI of the PyZEAL project.
    """
    parser = PyZEALParser()

    args = parser.parse_args()
    # check if any arguments were provided an respond with usage hint
    if len(argv) < 2:
        print("this is the CLI of the PyZEAL package. use '-h' for help.")

    # check if 'view' subcommand was selected and print current settings
    if getattr(args, "print", None) is True:
        print(JSONSettingsService())

    # check if 'change' subcommand was selected and change requested setting
    settingsService = JSONSettingsService()
    if getattr(args, "container", None) is not None:
        changeContainerSetting(args.container + "_container", settingsService)
    if getattr(args, "algorithm", None) is not None:
        changeAlgorithmSetting(args.algorithm, settingsService)
    if getattr(args, "log_level", None) is not None:
        changeLogLevelSetting(args.log_level, settingsService)

    # a valid subcommand was selected but no meaningful options were provided
    if len(argv) == 2:
        print("use '-h' with your subcommand for help.")


def changeContainerSetting(container: str, service: SettingsService) -> None:
    """
    TODO
    """
    oldContainer = service.defaultContainer
    newContainer: Optional[ContainerTypes] = None
    for containerType in ContainerTypes:
        if containerType.name == container.upper():
            newContainer = containerType
            break
    if newContainer is None:
        raise SystemExit(2)
    if newContainer != oldContainer:
        service.defaultContainer = newContainer
        print(
            "changed default container:   "
            + oldContainer.value
            + " --> "
            + oldContainer.value
        )


def changeAlgorithmSetting(algorithm: str, service: SettingsService) -> None:
    """
    TODO
    """
    oldAlgorithm = service.defaultAlgorithm
    newAlgorithm: Optional[AlgorithmTypes] = None
    for algorithmType in AlgorithmTypes:
        if algorithmType.name == algorithm.upper():
            newAlgorithm = algorithmType
            break
    if newAlgorithm is None:
        raise SystemExit(2)
    if newAlgorithm != oldAlgorithm:
        service.defaultAlgorithm = newAlgorithm
        print(
            "changed default algorithm:   "
            + oldAlgorithm.value
            + " --> "
            + newAlgorithm.value
        )


def changeLogLevelSetting(logLevel: str, service: SettingsService) -> None:
    """
    TODO
    """
    oldLevel = service.logLevel
    newLevel: Optional[LogLevel] = None
    for level in LogLevel:
        if level.name == logLevel.upper():
            newLevel = level
            break
    if newLevel is None:
        raise SystemExit(2)
    if newLevel != oldLevel:
        service.logLevel = newLevel
        print(
            "changed default log level:   "
            + oldLevel.name
            + " --> "
            + newLevel.name
        )
