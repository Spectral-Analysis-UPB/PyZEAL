"""
This module contains tests for the command-line interface, apart from the
parsing.
"""

from functools import partial
from typing import Dict, Tuple

from pyzeal.cli.cli_parser import PyZEALParser
from pyzeal.cli.parse_results import PluginParseResults, SettingsParseResults
from pyzeal.cli.parser_facade import PyZEALParserInterface
from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.utils.initialization_handler import PyZEALInitializationHandler
from pyzeal.utils.service_locator import ServiceLocator

PyZEALInitializationHandler.initPyZEALServices()
ServiceLocator.registerAsSingleton(PyZEALParserInterface, PyZEALParser())
from pyzeal.cli.__main__ import PyZEALEntry


def mockArgs(
    setting: Dict[str, str]
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
    )
    pluginParseResult = PluginParseResults(
        listPlugins=False,
        listModules=False,
        install="",
        uninstall="",
    )
    return settingsParseResult, pluginParseResult


def testChangeAlgorithmCall(mocker):
    """
    Test if `changeAlgorithmSetting` gets called correctly.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"algorithm": "NEWTON_GRID"}),
    )
    changeSettingStub = mocker.stub(name="changeSettingStub")
    mocker.patch(
        "pyzeal_cli.__main__.PyZEALEntry.changeAlgorithmSetting",
        changeSettingStub,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    changeSettingStub.assert_called()


def testChangeVerbosityCall(mocker):
    """Test if `changeVerbositySetting` gets called correctly.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"verbose": "True"}),
    )
    changeSettingStub = mocker.stub(name="changeSettingStub")
    mocker.patch(
        "pyzeal_cli.__main__.PyZEALEntry.changeVerbositySetting",
        changeSettingStub,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    changeSettingStub.assert_called()


def testChangeContainerCall(mocker):
    """Test if `changeContainerSetting` gets called correctly.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"container": "PLAIN_CONTAINER"}),
    )
    changeSettingStub = mocker.stub(name="changeSettingStub")
    mocker.patch(
        "pyzeal_cli.__main__.PyZEALEntry.changeContainerSetting",
        changeSettingStub,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    changeSettingStub.assert_called()


def testChangeLogLevelCall(mocker):
    """Test if `changeLogLevelSetting` gets called correctly.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"logLevel": "INFO"}),
    )
    changeSettingStub = mocker.stub(name="changeSettingStub")
    mocker.patch(
        "pyzeal_cli.__main__.PyZEALEntry.changeLogLevelSetting",
        changeSettingStub,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    changeSettingStub.assert_called()


def testChangeAlgorithmSettingsCall(mocker):
    """Test if `changeAlgorithmSetting` correctly updates the setting.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"algorithm": "NEWTON_GRID"}),
    )
    mockedProperty = mocker.patch(
        "pyzeal.settings.json_settings_service."
        "JSONSettingsService.defaultAlgorithm",
        new_callable=mocker.PropertyMock,
        return_value=AlgorithmTypes.SIMPLE_ARGUMENT,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    mockedProperty.assert_called_with(AlgorithmTypes.NEWTON_GRID)


def testChangeVerbositySettingsCall(mocker):
    """
    Test if `changeVerbositySetting` correctly updates the setting.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"verbose": "True"}),
    )
    mockedProperty = mocker.patch(
        "pyzeal_settings.json_settings_service.JSONSettingsService.verbose",
        new_callable=mocker.PropertyMock,
        return_value=False,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    mockedProperty.assert_called_with(True)


def testChangeLogLevelSettingsCall(mocker):
    """Test if `changeLogLevelSetting` correctly updates the setting.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"logLevel": "INFO"}),
    )
    mockedProperty = mocker.patch(
        "pyzeal_settings.json_settings_service.JSONSettingsService.logLevel",
        new_callable=mocker.PropertyMock,
        return_value=LogLevel.WARNING,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    mockedProperty.assert_called_with(LogLevel.INFO)


def testChangeContainerSettingsCall(mocker):
    """Test if `changeContainerSetting` correctly updates the setting.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"container": "plain"}),
    )
    mockedProperty = mocker.patch(
        "pyzeal_settings.json_settings_service."
        "JSONSettingsService.defaultContainer",
        new_callable=mocker.PropertyMock,
        return_value=ContainerTypes.ROUNDING_CONTAINER,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    mockedProperty.assert_called_with(ContainerTypes.PLAIN_CONTAINER)
