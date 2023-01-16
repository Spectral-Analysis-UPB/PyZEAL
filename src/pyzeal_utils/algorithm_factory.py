"""
This module provides a static factory class which maps the algorithms available
in the `AlgorithmTypes` enumeration to appropriate members of the
`FinderAlgorithm` type.

Authors:\n
- Philipp Schuette\n
"""

from typing import Optional

from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_algorithms.finder_algorithm import FinderAlgorithm
from pyzeal_algorithms.newton_grid import NewtonGridAlgorithm
from pyzeal_algorithms.simple_holo import SimpleArgumentAlgorithm
from pyzeal_algorithms.simple_holo_newton import SimpleArgumentNewtonAlgorithm
from pyzeal_logging.config import initLogger
from pyzeal_logging.log_levels import LogLevel


class AlgorithmFactory:
    "Static factory class used to create instances of root finding algorithms."

    # initialize the module level logger
    logger = initLogger(__name__.rsplit(".", maxsplit=1)[-1])

    @staticmethod
    def getConcreteAlgorithm(
        algoType: AlgorithmTypes, *, numSamplePoints: Optional[int] = None
    ) -> FinderAlgorithm:
        """
        Construct and return an algorithm instance based on the given type of
        algorithm `algoType`. Additional, algorithm specific configuration
        arguments are optional.

        :param algoType: type of algorithm to construct
        :type algoType: AlgorithmType
        :param numSamplePoints: sample point configuration for NewtonGridAlgo
        :type numSamplePoints: int
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
            return SimpleArgumentAlgorithm()
        if algoType == AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON:
            AlgorithmFactory.logger.debug(
                "requested usage of a SimpleArgumentNewtonAlgorithm..."
            )
            return SimpleArgumentNewtonAlgorithm()

        # TODO: implement configuration mechanism for default algorithms
        AlgorithmFactory.logger.debug(
            "requested usage of the default algorithm..."
        )
        return NewtonGridAlgorithm()

    @staticmethod
    def setLevel(level: LogLevel) -> None:
        """
        Set the log level.

        :param level: the new log level
        :type level: pyzeal_logging.log_levels.LogLevel
        """
        AlgorithmFactory.logger.setLevel(level=level.value)
