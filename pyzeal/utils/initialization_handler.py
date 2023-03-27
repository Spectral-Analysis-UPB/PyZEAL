"""
Module initialization_handler.py from the package PyZEAL.
This module handles initialization for the default PyZEAL services.

Authors:\n
- Philipp Schuette\n
"""

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.cli.cli_controller import CLIController
from pyzeal.cli.cli_parser import PyZEALParser
from pyzeal.cli.controller_facade import CLIControllerFacade
from pyzeal.cli.parser_facade import PyZEALParserInterface
from pyzeal.plugins.plugin_loader import PluginLoader
from pyzeal.pyzeal_logging.log_manager import LogManager
from pyzeal.pyzeal_types.init_modes import InitModes
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.factories.algorithm_factory import AlgorithmFactory
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.factories.estimator_factory import EstimatorFactory
from pyzeal.utils.factories.settings_factory import SettingsServiceFactory
from pyzeal.utils.service_locator import ServiceLocator


class PyZEALInitializationHandler:
    "Static initialization handler for PyZEAL services."

    # initialize the module level logger
    logger = LogManager.initLogger(__name__.rsplit(".", maxsplit=1)[-1])

    # protect from multiple initializations
    initialized = False

    @staticmethod
    def initPyZEALServices(mode: InitModes = InitModes.SCRIPT) -> None:
        """
        Register all relevant services with the ServiceLocator and initialize
        the available plugins.
        """
        if PyZEALInitializationHandler.initialized:
            PyZEALInitializationHandler.logger.warning(
                "re-initialization attempt with mode %s detected - skipped!",
                mode.name if mode.name else "[unknown]",
            )
            return
        if mode in InitModes.SCRIPT:
            PyZEALInitializationHandler.logger.info(
                "initializing algorithms..."
            )
            ServiceLocator.registerAsTransient(
                FinderAlgorithm, AlgorithmFactory.getConcreteAlgorithm
            )
            PyZEALInitializationHandler.logger.info(
                "initializing containers..."
            )
            ServiceLocator.registerAsTransient(
                RootContainer, ContainerFactory.getConcreteContainer
            )
            PyZEALInitializationHandler.logger.info(
                "initializing estimators..."
            )
            ServiceLocator.registerAsTransient(
                ArgumentEstimator, EstimatorFactory.getConcreteEstimator
            )
        if mode in (InitModes.CLI | InitModes.SCRIPT):
            PyZEALInitializationHandler.logger.info("initializing settings...")
            ServiceLocator.registerAsTransient(
                SettingsService, SettingsServiceFactory.getConcreteSettings
            )
        if mode in InitModes.CLI:
            PyZEALInitializationHandler.logger.info("initializing cli...")
            ServiceLocator.registerAsSingleton(
                PyZEALParserInterface, PyZEALParser()
            )
            settings = ServiceLocator.tryResolve(SettingsService)
            ServiceLocator.registerAsSingleton(
                CLIControllerFacade, CLIController(settings)
            )

        # plugins cannot be loaded in cli mode (plugins might be broken, ...)!
        if mode not in InitModes.CLI:
            PyZEALInitializationHandler.logger.info("loading plugins...")
            PluginLoader.loadPlugins()

        # initialization complete!
        PyZEALInitializationHandler.initialized = True
        PyZEALInitializationHandler.logger.info("initialization complete!")
