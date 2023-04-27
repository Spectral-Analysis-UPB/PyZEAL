"""
TODO.

Authors:\n
- Philipp Schuette\n
"""

from os.path import abspath
from typing import Optional, Tuple

from pyzeal.cli.controller_facade import CLIControllerFacade
from pyzeal.cli.parse_results import (
    InstallTestingParseResults,
    PluginParseResults,
    SettingsParseResults,
)
from pyzeal.plugins.installation_helper import InstallationHelper
from pyzeal.plugins.plugin_loader import PluginLoader
from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.install_test_facade import InstallTestingHandlerFacade


class CLIController(CLIControllerFacade):
    """
    Controller class handling the business logic of the `PyZEAL` command line
    interface.
    """

    def __init__(
        self,
        testingHandler: InstallTestingHandlerFacade,
        settings: SettingsService,
    ) -> None:
        """
        Initialize a new command line interface controller instance.
        """
        self.settingsService = settings
        self.testingHandler = testingHandler

    # docstr-coverage:inherited
    def handleViewSubcommand(self, args: SettingsParseResults) -> None:
        if args.doPrint:
            print(self.settingsService)

    # docstr-coverage:inherited
    def handleChangeSubcommand(self, args: SettingsParseResults) -> None:
        settingsService = self.settingsService
        if args.container:
            self.changeContainerSetting(
                args.container + "_container", settingsService
            )
        if args.algorithm:
            self.changeAlgorithmSetting(args.algorithm, settingsService)
        if args.estimator:
            self.changeEstimatorSetting(
                args.estimator + "_estimator", settingsService
            )
        if args.logLevel:
            self.changeLogLevelSetting(args.logLevel, settingsService)
        if args.verbose:
            self.changeVerbositySetting(args.verbose, settingsService)
        if args.precision:
            self.changePrecisionSetting(args.precision, settingsService)

    # docstr-coverage:inherited
    def handlePluginSubcommand(self, args: PluginParseResults) -> None:
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

    # docstr-coverage:inherited
    def handleTestingOption(self, args: InstallTestingParseResults) -> bool:
        if args.doTest:
            # right now we do not include root finder tests here to reduce
            # runtime; one could include those tests after performance increase
            modules = ["cli", "algorithms", "containers", "estimators"]
            for module in modules:
                self.testingHandler.testModule(module=module)
            return True
        return False

    @staticmethod
    def changeContainerSetting(
        container: str, service: SettingsService
    ) -> None:
        """
        Try to change the default container setting in `service` to
        `container`. If the container name is invalid, `SystemExit(2)` is
        raised.

        :param container: New default container name (case-insensitive).
        :param service: Settings service to update.
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
        :param service: Settings service to update.
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
    def changeEstimatorSetting(
        estimator: str, service: SettingsService
    ) -> None:
        """
        Try to change the default estimator setting in `service` to
        `estimator`. If the estimator name is invalid, `SystemExit(2)` is
        raised.

        :param estimator: New default estimator name (case-insensitive)
        :param service: Settings service to update.
        :raises SystemExit: Raised when no matching algorithm can be found.
        """
        oldEstimator = service.defaultEstimator
        newEstimator: Optional[EstimatorTypes] = None
        for estimatorType in EstimatorTypes:
            if estimatorType.name == estimator.upper():
                newEstimator = estimatorType
                break
        if newEstimator is None:
            raise SystemExit(2)
        if newEstimator != oldEstimator:
            service.defaultEstimator = newEstimator
            print(
                "changed default estimator:   "
                + oldEstimator.value
                + " --> "
                + newEstimator.value
            )

    @staticmethod
    def changeLogLevelSetting(logLevel: str, service: SettingsService) -> None:
        """
        Try to change the logLevel setting in `service` to `logLevel`.
        If the logLevel is invalid, `SystemExit(2)` is raised.

        :param logLevel: New log level (case-insensitive)
        :param service: Settings service to update.
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
        :param service: Setting service to update
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

    @staticmethod
    def changePrecisionSetting(
        precision: Tuple[int, int], service: SettingsService
    ) -> None:
        """
        Try to update the precision setting of `service`. If `precision` is not
        a pair of ints, `SystemExit(2)` is raised.

        :param precision: New precision setting
        :param service: Setting service to update
        """
        oldPrecision = service.precision
        newPrecision: Tuple[int, int] = precision
        if newPrecision != oldPrecision:
            service.precision = newPrecision
            print(
                "changed default precision:   "
                + str(oldPrecision)
                + " --> "
                + str(newPrecision)
            )
