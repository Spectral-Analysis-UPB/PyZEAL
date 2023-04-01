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
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.pyzeal_types.settings_types import SettingsServicesTypes
from pyzeal.utils.factories.settings_factory import SettingsServiceFactory


class AlgorithmFactory:
    "Static factory class used to create instances of root finding algorithms."

    # initialize the module level logger
    logger = LogManager.initLogger(__name__.rsplit(".", maxsplit=1)[-1])

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
        """
        if algoType == AlgorithmTypes.NEWTON_GRID:
            AlgorithmFactory.logger.debug(
                "requested usage of a NewtonGridAlgorithm..."
            )
            if numSamplePoints:
                return NewtonGridAlgorithm(numSamplePoints=numSamplePoints)
            return NewtonGridAlgorithm()
        if algoType == AlgorithmTypes.SIMPLE_ARGUMENT:
            AlgorithmFactory.logger.debug(
                "requested usage of a SimpleArgumentAlgorithm..."
            )
            return SimpleArgumentAlgorithm(estimatorType=estimatorType)
        if algoType == AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON:
            AlgorithmFactory.logger.debug(
                "requested usage of a SimpleArgumentNewtonAlgorithm..."
            )
            return SimpleArgumentNewtonAlgorithm(estimatorType=estimatorType)
        if algoType == AlgorithmTypes.ASSOCIATED_POLYNOMIAL:
            AlgorithmFactory.logger.debug(
                "requested usage of an AssociatedPolynomialAlgorithm..."
            )
            return AssociatedPolynomialAlgorithm(estimatorType=estimatorType)

        # return the current default algorithm
        AlgorithmFactory.logger.debug(
            "requested usage of the default algorithm..."
        )
        return AlgorithmFactory.getConcreteAlgorithm(
            SettingsServiceFactory.getConcreteSettings(
                SettingsServicesTypes.DEFAULT
            ).defaultAlgorithm,
            numSamplePoints=numSamplePoints,
            estimatorType=estimatorType,
        )

    @staticmethod
    def setLevel(level: LogLevel) -> None:
        """
        Set the log level.

        :param level: the new log level
        """
        AlgorithmFactory.logger.setLevel(level=level.value)
