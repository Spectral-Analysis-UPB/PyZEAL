"""
This module contains tests for the command-line interface, apart from the
parsing.
"""

from functools import partial
from typing import Dict, Tuple
from unittest.mock import PropertyMock, patch

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.cli.__main__ import PyZEALEntry
from pyzeal.cli.cli_parser import PyZEALParser
from pyzeal.cli.parse_results import PluginParseResults, SettingsParseResults
from pyzeal.cli.parser_facade import PyZEALParserInterface
from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.factories.algorithm_factory import AlgorithmFactory
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.factories.estimator_factory import EstimatorFactory
from pyzeal.utils.service_locator import ServiceLocator

ServiceLocator.registerAsSingleton(PyZEALParserInterface, PyZEALParser())
ServiceLocator.registerAsTransient(
    FinderAlgorithm, AlgorithmFactory.getConcreteAlgorithm
)
ServiceLocator.registerAsTransient(
    RootContainer, ContainerFactory.getConcreteContainer
)
ServiceLocator.registerAsTransient(
    ArgumentEstimator, EstimatorFactory.getConcreteEstimator
)


def mockArgs(
    setting: Dict[str, str]
) -> Tuple[SettingsParseResults, PluginParseResults]:
    """
    Generate `SettingsParseResults` and `PluginParseResults` instances
    containing the settings given by `setting`.

    :param setting: Dict of settings and values
    :return: ParseResults with appropriate settings
    """
    settingsParseResult = SettingsParseResults(
        doPrint=True,
        container=setting.get("container", ""),
        algorithm=setting.get("algorithm", ""),
        logLevel=setting.get("logLevel", ""),
        verbose=setting.get("verbose", ""),
    )
    pluginParseResult = PluginParseResults(
        listPlugins=False,
        listModules=False,
        install="",
        uninstall="",
    )
    return settingsParseResult, pluginParseResult


def testChangeAlgorithmCall() -> None:
    """
    Test if `changeAlgorithmSetting` gets called correctly.
    """
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(
            mockArgs, setting={"algorithm": "NEWTON_GRID"}
        )
        with patch(
            "pyzeal.cli.__main__.PyZEALEntry.changeAlgorithmSetting"
        ) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


def testChangeVerbosityCall() -> None:
    """
    Test if `changeVerbositySetting` gets called correctly.
    """
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting={"verbose": "True"})
        with patch(
            "pyzeal.cli.__main__.PyZEALEntry.changeVerbositySetting"
        ) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


def testChangeContainerCall() -> None:
    """
    Test if `changeContainerSetting` gets called correctly.
    """
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(
            mockArgs, setting={"container": "PLAIN_CONTAINER"}
        )
        with patch(
            "pyzeal.cli.__main__.PyZEALEntry.changeContainerSetting"
        ) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


def testChangeLogLevelCall() -> None:
    """
    Test if `changeLogLevelSetting` gets called correctly.
    """
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting={"logLevel": "INFO"})
        with patch(
            "pyzeal.cli.__main__.PyZEALEntry.changeLogLevelSetting"
        ) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


def testChangeAlgorithmSettingsCall() -> None:
    """
    Test if `changeAlgorithmSetting` correctly updates the setting.
    """
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(
            mockArgs, setting={"algorithm": "NEWTON_GRID"}
        )
        with patch(
            "pyzeal.settings.json_settings_service.JSONSettingsService.defaultAlgorithm",
            new_callable=PropertyMock,
        ) as mockedProp:
            mockedProp.return_value = AlgorithmTypes.SIMPLE_ARGUMENT
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            mockedProp.assert_called_with(AlgorithmTypes.NEWTON_GRID)


def testChangeVerbositySettingsCall() -> None:
    """
    Test if `changeVerbositySetting` correctly updates the setting.
    """
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting={"verbose": "True"})
        with patch(
            "pyzeal.settings.json_settings_service.JSONSettingsService.verbose",
            new_callable=PropertyMock,
        ) as mockedProp:
            mockedProp.return_value = False
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            mockedProp.assert_called_with(True)


def testChangeLogLevelSettingsCall() -> None:
    """
    Test if `changeLogLevelSetting` correctly updates the setting.
    """
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting={"logLevel": "INFO"})
        with patch(
            "pyzeal.settings.json_settings_service.JSONSettingsService.logLevel",
            new_callable=PropertyMock,
        ) as mockedProp:
            mockedProp.return_value = LogLevel.WARNING
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            mockedProp.assert_called_with(LogLevel.INFO)


def testChangeContainerSettingsCall() -> None:
    """
    Test if `changeContainerSetting` correctly updates the setting.
    """
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(
            mockArgs, setting={"container": "plain"}
        )
        with patch(
            "pyzeal.settings.json_settings_service.JSONSettingsService.defaultContainer",
            new_callable=PropertyMock,
        ) as mockedProp:
            mockedProp.return_value = ContainerTypes.ROUNDING_CONTAINER
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            mockedProp.assert_called_with(ContainerTypes.PLAIN_CONTAINER)
