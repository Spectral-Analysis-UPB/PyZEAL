"""
Module initialization_handler.py from the package PyZEAL.
TODO

Authors:\n
- Philipp Schuette\n
"""

from pyzeal_algorithms.finder_algorithm import FinderAlgorithm
from pyzeal_algorithms.pyzeal_estimators.argument_estimator import (
    ArgumentEstimator,
)
from pyzeal_logging.config import initLogger
from pyzeal_plugins.plugin_loader import PluginLoader
from pyzeal_settings.settings_service import SettingsService
from pyzeal_utils.pyzeal_containers.root_container import RootContainer
from pyzeal_utils.pyzeal_factories.algorithm_factory import AlgorithmFactory
from pyzeal_utils.pyzeal_factories.container_factory import ContainerFactory
from pyzeal_utils.pyzeal_factories.estimator_factory import EstimatorFactory
from pyzeal_utils.pyzeal_factories.settings_factory import (
    SettingsServiceFactory,
)
from pyzeal_utils.service_locator import ServiceLocator


class PyZEALInitializationHandler:
    "Static initialization handler for PyZEAL services."

    # initialize the module level logger
    logger = initLogger(__name__.rsplit(".", maxsplit=1)[-1])

    @staticmethod
    def initPyZEALServices() -> None:
        """
        Register all relevant services with the ServiceLocator and initialize
        the available plugins.
        """
        PyZEALInitializationHandler.logger.info("initializing algorithms...")
        ServiceLocator.registerAsTransient(
            FinderAlgorithm, AlgorithmFactory.getConcreteAlgorithm
        )
        PyZEALInitializationHandler.logger.info("initializing containers...")
        ServiceLocator.registerAsTransient(
            RootContainer, ContainerFactory.getConcreteContainer
        )
        PyZEALInitializationHandler.logger.info("initializing estimators...")
        ServiceLocator.registerAsTransient(
            ArgumentEstimator, EstimatorFactory.getConcreteEstimator
        )
        PyZEALInitializationHandler.logger.info("initializing settings...")
        ServiceLocator.registerAsTransient(
            SettingsService, SettingsServiceFactory.getConcreteSettings
        )
        PyZEALInitializationHandler.logger.info("loading plugins...")
        PluginLoader.loadPlugins()
