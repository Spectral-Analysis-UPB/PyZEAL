"""
This module contains tests for the command-line interface, apart from the
parsing.
"""

from functools import partial
from typing import Callable, Tuple, TypedDict, Union
from unittest.mock import PropertyMock, create_autospec, patch

import pytest

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.cli.__main__ import PyZEALEntry
from pyzeal.cli.cli_controller import CLIController
from pyzeal.cli.cli_parser import PyZEALParser
from pyzeal.cli.controller_facade import CLIControllerFacade
from pyzeal.cli.parse_results import (
    InstallTestingParseResults,
    PluginParseResults,
    SettingsParseResults,
)
from pyzeal.cli.parser_facade import PyZEALParserInterface
from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.factories.algorithm_factory import AlgorithmFactory
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.factories.estimator_factory import EstimatorFactory
from pyzeal.utils.install_test_facade import InstallTestingHandlerFacade
from pyzeal.utils.install_test_handler import InstallTestingHandler
from pyzeal.utils.service_locator import ServiceLocator

ServiceLocator.registerAsSingleton(
    PyZEALParserInterface, PyZEALParser()
).registerAsTransient(
    FinderAlgorithm, AlgorithmFactory.getConcreteAlgorithm
).registerAsTransient(
    RootContainer, ContainerFactory.getConcreteContainer
).registerAsTransient(
    ArgumentEstimator, EstimatorFactory.getConcreteEstimator
).registerAsTransient(
    CLIControllerFacade, CLIController
).registerAsTransient(
    InstallTestingHandlerFacade, InstallTestingHandler
).registerAsSingleton(
    SettingsService, RAMSettingsService()
)


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
    newSetting: SettingsDict,
) -> Tuple[
    SettingsParseResults, PluginParseResults, InstallTestingParseResults
]:
    """
    Generate `SettingsParseResults` and `PluginParseResults` instances
    containing the settings given by `newSetting`.

    :param newSetting: Dict of settings and values
    :return: ParseResults with appropriate settings
    """
    settingsParseResult = SettingsParseResults(
        doPrint=True,
        container=newSetting.get("container", ""),
        algorithm=newSetting.get("algorithm", ""),
        logLevel=newSetting.get("logLevel", ""),
        verbose=newSetting.get("verbose", ""),
        estimator=newSetting.get("estimator", ""),
        precision=newSetting.get("precision", None),
    )
    pluginParseResult = PluginParseResults(
        listPlugins=False,
        listModules=False,
        install="",
        uninstall="",
    )
    testingParseResult = InstallTestingParseResults(doTest=False)
    return settingsParseResult, pluginParseResult, testingParseResult


tSettingsTypes = Union[
    AlgorithmTypes,
    bool,
    ContainerTypes,
    LogLevel,
    EstimatorTypes,
    Tuple[int, int],
]

newSettings: Tuple[SettingsDict, ...] = (
    {"algorithm": "NEWTON_GRID"},
    {"verbose": "True"},
    {"container": "plain"},
    {"logLevel": "INFO"},
    {"estimator": "summation"},
    {"precision": (3, 3)},
)
changeMethods: Tuple[str, ...] = (
    "changeAlgorithmSetting",
    "changeVerbositySetting",
    "changeContainerSetting",
    "changeLogLevelSetting",
    "changeEstimatorSetting",
    "changePrecisionSetting",
)
defaultSettingProperties: Tuple[str, ...] = (
    "defaultAlgorithm",
    "verbose",
    "defaultContainer",
    "logLevel",
    "defaultEstimator",
    "precision",
)
beforeValues: Tuple[tSettingsTypes, ...] = (
    AlgorithmTypes.SIMPLE_ARGUMENT,
    False,
    ContainerTypes.ROUNDING_CONTAINER,
    LogLevel.WARNING,
    EstimatorTypes.QUADRATURE_ESTIMATOR,
    (1, 1),
)
afterValues: Tuple[tSettingsTypes, ...] = (
    AlgorithmTypes.NEWTON_GRID,
    True,
    ContainerTypes.PLAIN_CONTAINER,
    LogLevel.INFO,
    EstimatorTypes.SUMMATION_ESTIMATOR,
    (3, 3),
)


@pytest.mark.parametrize("testSetup", zip(newSettings, changeMethods))
def testChangeCall(testSetup: Tuple[SettingsDict, str]) -> None:
    """
    Test if `change...Setting` gets called correctly.
    """
    newSetting: SettingsDict = testSetup[0]
    changeMethod = "pyzeal.cli.cli_controller.CLIController." + testSetup[1]
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, newSetting=newSetting)
        with patch(changeMethod) as doNothing:
            entry = PyZEALEntry()
            entry.mainPyZEAL()
            doNothing.assert_called_once()


@pytest.mark.parametrize(
    "testSetup",
    zip(newSettings, defaultSettingProperties, beforeValues, afterValues),
)
def testChangeSettingsCall(
    testSetup: Tuple[
        SettingsDict,
        str,
        tSettingsTypes,
        tSettingsTypes,
    ]
) -> None:
    """
    Test if `change...Setting` correctly updates the newSetting.
    """
    newSetting: SettingsDict = testSetup[0]
    defaultSettingProperty = (
        "pyzeal.settings.ram_settings_service.RAMSettingsService."
        + testSetup[1]
    )
    beforeValue = testSetup[2]
    afterValue = testSetup[3]
    with patch("pyzeal.cli.cli_parser.PyZEALParser.parseArgs") as mockParse:
        mockParse.side_effect = partial(mockArgs, newSetting=newSetting)
        with patch(
            defaultSettingProperty, new_callable=PropertyMock
        ) as mockedProp:
            mockedProp.return_value = beforeValue
            entry = PyZEALEntry()
            entry.mainPyZEAL()
            mockedProp.assert_called_with(afterValue)


@pytest.mark.parametrize(
    "changeFunction",
    [
        CLIController.changeAlgorithmSetting,
        CLIController.changeContainerSetting,
        CLIController.changeEstimatorSetting,
        CLIController.changeLogLevelSetting,
    ],
)
def testCLIControllerInvalidName(
    changeFunction: Callable[[str, SettingsService], None]
) -> None:
    """
    Test if CLIController correctly exits when an invalid name is given
    for a newSetting.

    :param changeFunction: Function to test, parametrized by pytest
    """
    mockSettings = create_autospec(
        SettingsService, spec_set=True, instance=True
    )
    with pytest.raises(SystemExit):
        changeFunction("THIS_DOES_NOT_EXIST", mockSettings)
