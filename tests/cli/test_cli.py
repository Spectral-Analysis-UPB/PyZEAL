from functools import partial

from pyzeal_cli.cli_parser import PyZEALParser, PyZEALParserInterface
from pyzeal_cli.parse_results import ParseResults
from pyzeal_logging.log_levels import LogLevel
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes
from pyzeal_utils.initialization_handler import PyZEALInitializationHandler
from pyzeal_utils.service_locator import ServiceLocator

PyZEALInitializationHandler.initPyZEALServices()
ServiceLocator.registerAsSingleton(PyZEALParserInterface, PyZEALParser())
from pyzeal_cli.__main__ import PyZEALEntry


def mockArgs(setting):
    """Generate `ParseResults` containing the settings given by `setting`-

    :param setting: Dict of settings and values
    :type setting: Dict[str, str]
    :return: ParseResults with appropriate settings
    :rtype: ParseResults
    """
    return ParseResults(
        doPrint=True,
        container=setting["container"]
        if "container" in setting.keys()
        else "",
        algorithm=setting["algorithm"]
        if "algorithm" in setting.keys()
        else "",
        logLevel=setting["logLevel"] if "logLevel" in setting.keys() else "",
        verbose=setting["verbose"] if "verbose" in setting.keys() else "",
        listPlugins=False,
        listModules=False,
        install="",
        uninstall="",
    )


def testChangeAlgorithmCall(mocker):
    """Test if `changeAlgorithmSetting` gets called correctly.

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
    mocked_property = mocker.patch(
        "pyzeal_settings.json_settings_service.JSONSettingsService.defaultAlgorithm",
        new_callable=mocker.PropertyMock,
        return_value=AlgorithmTypes.SIMPLE_ARGUMENT,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    mocked_property.assert_called_with(AlgorithmTypes.NEWTON_GRID)


def testChangeVerbositySettingsCall(mocker):
    """Test if `changeVerbositySetting` correctly updates the setting.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"verbose": "True"}),
    )
    mocked_property = mocker.patch(
        "pyzeal_settings.json_settings_service.JSONSettingsService.verbose",
        new_callable=mocker.PropertyMock,
        return_value=False,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    mocked_property.assert_called_with(True)


def testChangeLogLevelSettingsCall(mocker):
    """Test if `changeLogLevelSetting` correctly updates the setting.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"logLevel": "INFO"}),
    )
    mocked_property = mocker.patch(
        "pyzeal_settings.json_settings_service.JSONSettingsService.logLevel",
        new_callable=mocker.PropertyMock,
        return_value=LogLevel.WARNING,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    mocked_property.assert_called_with(LogLevel.INFO)


def testChangeContainerSettingsCall(mocker):
    """Test if `changeContainerSetting` correctly updates the setting.

    :param mocker: `pytest-mock` fixture
    """
    mocker.patch(
        "pyzeal_cli.cli_parser.PyZEALParser.parseArgs",
        partial(mockArgs, setting={"container": "plain"}),
    )
    mocked_property = mocker.patch(
        "pyzeal_settings.json_settings_service.JSONSettingsService.defaultContainer",
        new_callable=mocker.PropertyMock,
        return_value=ContainerTypes.ROUNDING_CONTAINER,
    )
    dut = PyZEALEntry()
    dut.mainPyZEAL()
    mocked_property.assert_called_with(ContainerTypes.PLAIN_CONTAINER)
