"""
This module provides the main CLI entry point of the PyZEAL project through the
function `mainPyZEAL`. At the moment it provides facilities to query the
currently installed PyZEAL version as well as view and manipulate settings.

Authors:\n
- Philipp Schuette\n
"""

from os.path import abspath
from sys import argv
from typing import Optional

from pyzeal_cli.parse_results import PluginParseResults, SettingsParseResults
from pyzeal_cli.parser_facade import PyZEALParserInterface
from pyzeal_logging.log_levels import LogLevel
from pyzeal_plugins.installation_helper import InstallationHelper
from pyzeal_plugins.plugin_loader import PluginLoader
from pyzeal_settings.settings_service import SettingsService
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.init_modes import InitModes
from pyzeal_utils.initialization_handler import PyZEALInitializationHandler
from pyzeal_utils.service_locator import ServiceLocator


class PyZEALEntry:
    """
    TODO
    """

    PyZEALInitializationHandler.initPyZEALServices(InitModes.CLI)

    parser = ServiceLocator.tryResolve(PyZEALParserInterface)
    settingsService = ServiceLocator.tryResolve(SettingsService)

    @staticmethod
    def mainPyZEAL() -> None:
        """
        Main entry point for the CLI of the PyZEAL project.
        """

        settingsArgs, pluginArgs = PyZEALEntry.parser.parseArgs()

        # check if any arguments were provided and respond with usage hint
        if len(argv) < 2:
            print("this is the CLI of the PyZEAL package. use '-h' for help.")

        PyZEALEntry.handleViewSubcommand(settingsArgs)
        PyZEALEntry.handleChangeSubcommand(settingsArgs)
        PyZEALEntry.handlePluginSubcommand(pluginArgs)

        # a valid subcommand was selected but with no meaningful options
        if len(argv) == 2:
            print("use '-h' with your subcommand for help.")

    @staticmethod
    def handleViewSubcommand(args: SettingsParseResults) -> None:
        """
        Check if the 'view' subcommand was selected and print current settings.

        :param args: _description_
        :type args: _type_
        """
        if args.doPrint:
            print(PyZEALEntry.settingsService)

    @staticmethod
    def handleChangeSubcommand(args: SettingsParseResults) -> None:
        """
        Check if the 'change' subcommand was selected and change settings
        accordingly.

        :param args: _description_
        :type args: _type_
        """
        settingsService = PyZEALEntry.settingsService
        if args.container:
            PyZEALEntry.changeContainerSetting(
                args.container + "_container", settingsService
            )
        if args.algorithm:
            PyZEALEntry.changeAlgorithmSetting(args.algorithm, settingsService)
        if args.logLevel:
            PyZEALEntry.changeLogLevelSetting(args.logLevel, settingsService)
        if args.verbose:
            PyZEALEntry.changeVerbositySetting(args.verbose, settingsService)

    @staticmethod
    def handlePluginSubcommand(args: PluginParseResults) -> None:
        """
        Check if the 'plugin' subcommand was selected and manipulate plugins
        accordingly.

        :param args: _description_
        :type args: _type_
        :raises SystemExit: _description_
        :raises SystemExit: _description_
        """
        if args.listPlugins:
            print("currently installed Plugins:")
            print("----------------------------")
            for plugin in PluginLoader.loadPlugins():
                print(plugin)

        if args.listModules:
            print("installation directory contents:")
            print("--------------------------------")
            for module in PluginLoader.discoverModules():
                print(module)

        if args.install:
            print(f"installing plugin {args.install}...")
            if InstallationHelper.installPlugin(abspath(args.install)):
                print("[success] plugin was installed!")
            else:
                print("[error] the requested plugin does not exist - abort!")
                raise SystemExit(2)

        if args.uninstall:
            print(f"uninstalling plugin {args.uninstall}...")
            if InstallationHelper.uninstallPlugin(args.uninstall):
                print("[success] plugin was uninstalled!")
            else:
                print("[error] the requested plugin does not exist - abort!")
                raise SystemExit(2)

    @staticmethod
    def changeContainerSetting(
        container: str, service: SettingsService
    ) -> None:
        """
        Try to change the default container setting in `service` to
        `container`. If the container name is invalid, `SystemExit(2)` is
        raised.

        :param container: New default container name (case-insensitive).
        :type container: str
        :param service: Settings service to update.
        :type service: SettingsService
        :raises SystemExit: Raised when no matching container can be found.
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

    @staticmethod
    def changeAlgorithmSetting(
        algorithm: str, service: SettingsService
    ) -> None:
        """
        Try to change the default algorithm setting in `service` to
        `algorithm`. If the algorithm name is invalid, `SystemExit(2)` is
        raised.

        :param algorithm: New default algorithm name (case-insensitive)
        :type algorithm: str
        :param service: Settings service to update.
        :type service: SettingsService
        :raises SystemExit: Raised when no matching algorithm can be found.
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

    @staticmethod
    def changeLogLevelSetting(logLevel: str, service: SettingsService) -> None:
        """
        Try to change the logLevel setting in `service` to `logLevel`.
        If the logLevel is invalid, `SystemExit(2)` is raised.

        :param logLevel: New log level (case-insensitive)
        :type logLevel: str
        :param service: Settings service to update.
        :type service: SettingsService
        :raises SystemExit: Raised when the log level is invalid.
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

    @staticmethod
    def changeVerbositySetting(verbose: str, service: SettingsService) -> None:
        """
        Try to update the verbosity setting of `service`. If `verbose` is not
        "true" or "false", `SystemExit(2)` is raised.

        :param verbose: New verbosity setting
        :type verbose: str
        :param service: Setting service to update
        :type service: SettingsService
        :raises SystemExit: Raised when an invalid verbosity setting is given.
        """
        oldVerbosity = service.verbose
        newVerbosity: bool = verbose.lower() == "true"
        if newVerbosity != oldVerbosity:
            service.verbose = newVerbosity
            print(
                "changed default verbosity:   "
                + str(oldVerbosity)
                + " --> "
                + str(newVerbosity)
            )
