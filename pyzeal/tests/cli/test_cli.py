"""
This module contains tests for the command-line interface, apart from the
parsing.
"""

from functools import partial
from typing import Tuple, TypedDict
from unittest.mock import PropertyMock, patch

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.cli.__main__ import PyZEALEntry
from pyzeal.cli.cli_controller import CLIController
from pyzeal.cli.cli_parser import PyZEALParser
from pyzeal.cli.controller_facade import CLIControllerFacade
from pyzeal.cli.parse_results import PluginParseResults, SettingsParseResults
from pyzeal.cli.parser_facade import PyZEALParserInterface
from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
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
ServiceLocator.registerAsTransient(CLIControllerFacade, CLIController)


class SettingsDict(TypedDict, total=False):
    """
    Container class to ensure correct typing of settings options to be tested.
    """

    container: str
    algorithm: str
    logLevel: str
    verbose: str
    estimator: str
    precision: Tuple[int, int]


def mockArgs(
    setting: SettingsDict,
) -> Tuple[SettingsParseResults, PluginParseResults]:
    """
    Generate `SettingsParseResults` and `PluginParseResults` instances
    containing the settings given by `setting`.

    :param setting: Dict of settings and values
    :type setting: Dict[str, str]
    :return: ParseResults with appropriate settings
    :rtype: ParseResults
    """
    settingsParseResult = SettingsParseResults(
        doPrint=True,
        container=setting.get("container", ""),
        algorithm=setting.get("algorithm", ""),
        logLevel=setting.get("logLevel", ""),
        verbose=setting.get("verbose", ""),
        estimator=setting.get("estimator", ""),
        precision=setting.get("precision", None),
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
    setting: SettingsDict = {"algorithm": "NEWTON_GRID"}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.cli.cli_controller.CLIController.changeAlgorithmSetting"
        ) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


def testChangeVerbosityCall() -> None:
    """
    Test if `changeVerbositySetting` gets called correctly.
    """
    setting: SettingsDict = {"verbose": "True"}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.cli.cli_controller.CLIController.changeVerbositySetting"
        ) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


def testChangeContainerCall() -> None:
    """
    Test if `changeContainerSetting` gets called correctly.
    """
    setting: SettingsDict = {"container": "PLAIN_CONTAINER"}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.cli.cli_controller.CLIController.changeContainerSetting"
        ) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


def testChangeLogLevelCall() -> None:
    """
    Test if `changeLogLevelSetting` gets called correctly.
    """
    setting: SettingsDict = {"logLevel": "INFO"}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.cli.cli_controller.CLIController.changeLogLevelSetting"
        ) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


def testChangeEstimatorCall() -> None:
    """
    Test if `changeEstimatorSetting` gets called correctly.
    """
    setting: SettingsDict = {"estimator": "summation"}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.cli.cli_controller.CLIController.changeEstimatorSetting"
        ) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


def testChangePrecisionCall() -> None:
    """
    Test if `changePrecisionSetting` gets called correctly.
    """
    setting: SettingsDict = {"precision": (3, 3)}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.cli.cli_controller.CLIController.changePrecisionSetting"
        ) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


def testChangeAlgorithmSettingsCall() -> None:
    """
    Test if `changeAlgorithmSetting` correctly updates the setting.
    """
    setting: SettingsDict = {"algorithm": "NEWTON_GRID"}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.settings.json_settings_service."
            "JSONSettingsService.defaultAlgorithm",
            new_callable=PropertyMock,
        ) as mockedProp:
            mockedProp.return_value = AlgorithmTypes.SIMPLE_ARGUMENT
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            mockedProp.assert_called_with(AlgorithmTypes[setting["algorithm"]])


def testChangeVerbositySettingsCall() -> None:
    """
    Test if `changeVerbositySetting` correctly updates the setting.
    """
    setting: SettingsDict = {"verbose": "True"}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.settings.json_settings_service."
            "JSONSettingsService.verbose",
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
    setting: SettingsDict = {"logLevel": "INFO"}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.settings.json_settings_service."
            "JSONSettingsService.logLevel",
            new_callable=PropertyMock,
        ) as mockedProp:
            mockedProp.return_value = LogLevel.WARNING
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            mockedProp.assert_called_with(LogLevel[setting["logLevel"]])


def testChangeContainerSettingsCall() -> None:
    """
    Test if `changeContainerSetting` correctly updates the setting.
    """
    setting: SettingsDict = {"container": "plain"}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.settings.json_settings_service."
            "JSONSettingsService.defaultContainer",
            new_callable=PropertyMock,
        ) as mockedProp:
            mockedProp.return_value = ContainerTypes.ROUNDING_CONTAINER
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            mockedProp.assert_called_with(ContainerTypes.PLAIN_CONTAINER)


def testChangeEstimatorSettingsCall() -> None:
    """
    Test if `changeEstimatorSetting` correctly updates the setting.
    """
    setting: SettingsDict = {"estimator": "summation"}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.settings.json_settings_service."
            "JSONSettingsService.defaultEstimator",
            new_callable=PropertyMock,
        ) as mockedProp:
            mockedProp.return_value = EstimatorTypes.QUADRATURE_ESTIMATOR
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            mockedProp.assert_called_with(EstimatorTypes.SUMMATION_ESTIMATOR)


def testChangePrecisionSettingsCall() -> None:
    """
    Test if `changePrecisionSetting` correctly updates the setting.
    """
    setting: SettingsDict = {"precision": (3, 3)}
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(
            "pyzeal.settings.json_settings_service."
            "JSONSettingsService.precision",
            new_callable=PropertyMock,
        ) as mockedProp:
            mockedProp.return_value = (1, 1)
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            mockedProp.assert_called_with((3, 3))
