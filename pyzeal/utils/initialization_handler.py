"""
Module initialization_handler.py from the package PyZEAL.
This module handles initialization for the default PyZEAL services.

Authors:\n
- Philipp Schuette\n
"""

from typing import Optional

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.cli.cli_controller import CLIController
from pyzeal.cli.cli_parser import PyZEALParser
from pyzeal.cli.controller_facade import CLIControllerFacade
from pyzeal.cli.parser_facade import PyZEALParserInterface
from pyzeal.plugins.plugin_loader import PluginLoader
from pyzeal.pyzeal_logging.log_manager import LogManager
from pyzeal.pyzeal_logging.logger_facade import PyZEALLogger
from pyzeal.pyzeal_types.init_modes import InitModes
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.factories.algorithm_factory import AlgorithmFactory
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.factories.estimator_factory import EstimatorFactory
from pyzeal.utils.factories.settings_factory import SettingsServiceFactory
from pyzeal.utils.install_test_facade import InstallTestingHandlerFacade
from pyzeal.utils.install_test_handler import InstallTestingHandler
from pyzeal.utils.service_locator import ServiceLocator


class PyZEALInitializationHandler:
    "Static initialization handler for PyZEAL services."

    # the module level logger
    _logger: Optional[PyZEALLogger] = None

    # protect from multiple initializations
    initialized = False

    @staticmethod
    def initPyZEALServices(mode: InitModes = InitModes.SCRIPT) -> None:
        """
        Register all relevant services with the ServiceLocator and initialize
        the available plugins.
        """
        # check for re-initialization
        if PyZEALInitializationHandler.initialized:
            if PyZEALInitializationHandler._logger is None:
                return
            PyZEALInitializationHandler._logger.warning(
                "re-initialization attempt with mode %s detected - skipped!",
                mode.name if mode.name else "[unknown]",
            )
            return

        # register settings service first so we can initialize logging
        if mode in (InitModes.CLI | InitModes.SCRIPT):
            ServiceLocator.registerAsTransient(
                SettingsService, SettingsServiceFactory.getConcreteSettings
            )
        PyZEALInitializationHandler._logger = LogManager.initLogger(
            __name__.rsplit(".", maxsplit=1)[-1],
            ServiceLocator.tryResolve(SettingsService).logLevel,
        )

        if mode in InitModes.SCRIPT:
            PyZEALInitializationHandler._logger.info(
                "initializing algorithms..."
            )
            ServiceLocator.registerAsTransient(
                FinderAlgorithm, AlgorithmFactory.getConcreteAlgorithm
            )
            PyZEALInitializationHandler._logger.info(
                "initializing containers..."
            )
            ServiceLocator.registerAsTransient(
                RootContainer, ContainerFactory.getConcreteContainer
            )
            PyZEALInitializationHandler._logger.info(
                "initializing estimators..."
            )
            ServiceLocator.registerAsTransient(
                ArgumentEstimator, EstimatorFactory.getConcreteEstimator
            )
        if mode in InitModes.CLI:
            PyZEALInitializationHandler._logger.info("initializing cli...")
            ServiceLocator.registerAsSingleton(
                PyZEALParserInterface, PyZEALParser()
            )
            ServiceLocator.registerAsTransient(
                CLIControllerFacade, CLIController
            )
            ServiceLocator.registerAsTransient(
                InstallTestingHandlerFacade, InstallTestingHandler
            )

        # plugins cannot be loaded in cli mode (plugins might be broken, ...)!
        if mode not in InitModes.CLI:
            PyZEALInitializationHandler._logger.info("loading plugins...")
            PluginLoader.loadPlugins()

        # initialization complete!
        PyZEALInitializationHandler.initialized = True
        PyZEALInitializationHandler._logger.info("initialization complete!")
