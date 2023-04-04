"""
This module contains tests for the command-line interface, apart from the
parsing.
"""

from functools import partial
from typing import Tuple, TypedDict
from unittest.mock import PropertyMock, patch, create_autospec
import pytest

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
from pyzeal.settings.settings_service import SettingsService

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


testPairs = [
    (
        {"algorithm": "NEWTON_GRID"},
        "pyzeal.cli.cli_controller.CLIController.changeAlgorithmSetting",
        "pyzeal.settings.json_settings_service.JSONSettingsService.defaultAlgorithm",
        AlgorithmTypes.SIMPLE_ARGUMENT,
        AlgorithmTypes.NEWTON_GRID,
    ),
    (
        {"verbose": "True"},
        "pyzeal.cli.cli_controller.CLIController.changeVerbositySetting",
        "pyzeal.settings.json_settings_service.JSONSettingsService.verbose",
        False,
        True,
    ),
    (
        {"container": "plain"},
        "pyzeal.cli.cli_controller.CLIController.changeContainerSetting",
        "pyzeal.settings.json_settings_service.JSONSettingsService.defaultContainer",
        ContainerTypes.ROUNDING_CONTAINER,
        ContainerTypes.PLAIN_CONTAINER,
    ),
    (
        {"logLevel": "INFO"},
        "pyzeal.cli.cli_controller.CLIController.changeLogLevelSetting",
        "pyzeal.settings.json_settings_service.JSONSettingsService.logLevel",
        LogLevel.WARNING,
        LogLevel.INFO,
    ),
    (
        {"estimator": "summation"},
        "pyzeal.cli.cli_controller.CLIController.changeEstimatorSetting",
        "pyzeal.settings.json_settings_service.JSONSettingsService.defaultEstimator",
        EstimatorTypes.QUADRATURE_ESTIMATOR,
        EstimatorTypes.SUMMATION_ESTIMATOR,
    ),
    (
        {"precision": (3, 3)},
        "pyzeal.cli.cli_controller.CLIController.changePrecisionSetting",
        "pyzeal.settings.json_settings_service.JSONSettingsService.precision",
        (1, 1),
        (3, 3),
    ),
]


@pytest.mark.parametrize("pair", testPairs)
def testChangeCall(pair) -> None:
    """
    Test if `change...Setting` gets called correctly.
    """
    setting: SettingsDict = pair[0]
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(pair[1]) as doNothing:
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            doNothing.assert_called()


@pytest.mark.parametrize("pair", testPairs)
def testChangeSettingsCall(pair) -> None:
    """
    Test if `change...Setting` correctly updates the setting.
    """
    setting: SettingsDict = pair[0]
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, setting=setting)
        with patch(pair[2], new_callable=PropertyMock) as mockedProp:
            mockedProp.return_value = pair[3]
            dut = PyZEALEntry()
            dut.mainPyZEAL()
            mockedProp.assert_called_with(pair[4])


@pytest.mark.parametrize(
    "changeFunction",
    [
        CLIController.changeAlgorithmSetting,
        CLIController.changeContainerSetting,
        CLIController.changeEstimatorSetting,
        CLIController.changeLogLevelSetting,
    ],
)
def testCLIControllerInvalidName(changeFunction) -> None:
    """
    Test if CLIController correctly exits when an invalid name is given
    for a setting.

    :param changeFunction: Function to test, parametrized by pytest
    """
    mockSettings = create_autospec(SettingsService, spec_set=True)
    with pytest.raises(SystemExit):
        changeFunction("THIS_DOES_NOT_EXIST", mockSettings)
