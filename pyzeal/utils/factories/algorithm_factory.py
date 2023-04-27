"""
This module provides a static factory class which maps the algorithms available
in the `AlgorithmTypes` enumeration to appropriate members of the
`FinderAlgorithm` type.

Authors:\n
- Philipp Schuette\n
"""

from typing import Optional

from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.algorithms.newton_grid import NewtonGridAlgorithm
from pyzeal.algorithms.polynomial_holo import AssociatedPolynomialAlgorithm
from pyzeal.algorithms.simple_holo import SimpleArgumentAlgorithm
from pyzeal.algorithms.simple_holo_newton import SimpleArgumentNewtonAlgorithm
from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_logging.log_manager import LogManager
from pyzeal.pyzeal_logging.logger_facade import PyZEALLogger
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.service_locator import ServiceLocator


class AlgorithmFactory:
    "Static factory class used to create instances of root finding algorithms."

    # the module level logger
    _logger: Optional[PyZEALLogger] = None

    @staticmethod
    def getConcreteAlgorithm(
        algoType: AlgorithmTypes = AlgorithmTypes.DEFAULT,
        *,
        estimatorType: EstimatorTypes = EstimatorTypes.DEFAULT,
        numSamplePoints: Optional[int] = None,
    ) -> FinderAlgorithm:
        """
        Construct and return an algorithm instance based on the given type of
        algorithm `algoType`. Additional, algorithm specific configuration
        arguments are optional.

        :param algoType: type of algorithm to construct
        :param estimatorType: type of argument estimator to use
        :param numSamplePoints: sample point configuration for NewtonGridAlgo
        :return: a concrete `FinderAlgorithm` instance
        """
        if AlgorithmFactory._logger is None:
            AlgorithmFactory._logger = LogManager.initLogger(
                __name__.rsplit(".", maxsplit=1)[-1],
                ServiceLocator.tryResolve(SettingsService).logLevel,
            )
        if algoType == AlgorithmTypes.NEWTON_GRID:
            AlgorithmFactory._logger.debug(
                "requested usage of a NewtonGridAlgorithm..."
            )
            if numSamplePoints:
                return NewtonGridAlgorithm(numSamplePoints=numSamplePoints)
            return NewtonGridAlgorithm()
        if algoType == AlgorithmTypes.SIMPLE_ARGUMENT:
            AlgorithmFactory._logger.debug(
                "requested usage of a SimpleArgumentAlgorithm..."
            )
            return SimpleArgumentAlgorithm(estimatorType=estimatorType)
        if algoType == AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON:
            AlgorithmFactory._logger.debug(
                "requested usage of a SimpleArgumentNewtonAlgorithm..."
            )
            return SimpleArgumentNewtonAlgorithm(estimatorType=estimatorType)
        if algoType == AlgorithmTypes.ASSOCIATED_POLYNOMIAL:
            AlgorithmFactory._logger.debug(
                "requested usage of an AssociatedPolynomialAlgorithm..."
            )
            return AssociatedPolynomialAlgorithm(estimatorType=estimatorType)

        # return the current default algorithm
        AlgorithmFactory._logger.debug(
            "requested usage of the default algorithm..."
        )
        settings = ServiceLocator.tryResolve(SettingsService)
        return AlgorithmFactory.getConcreteAlgorithm(
            settings.defaultAlgorithm,
            numSamplePoints=numSamplePoints,
            estimatorType=estimatorType,
        )

    @staticmethod
    def setLevel(level: LogLevel) -> None:
        """
        Set the log level.

        :param level: the new log level
        """
        if AlgorithmFactory._logger is not None:
            AlgorithmFactory._logger.setLevel(level=level.value)
