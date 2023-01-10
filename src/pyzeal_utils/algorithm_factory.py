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


class AlgorithmFactory:
    "Static factory class used to create instances of root finding algorithms."
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
            if numSamplePoints:
                return NewtonGridAlgorithm(numSamplePoints=numSamplePoints)
            return NewtonGridAlgorithm()
        if algoType == AlgorithmTypes.SIMPLE_ARGUMENT:
            return SimpleArgumentAlgorithm()
        if algoType == AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON:
            return SimpleArgumentNewtonAlgorithm()

        # TODO: implement configuration mechanism for default algorithms
        return NewtonGridAlgorithm()
