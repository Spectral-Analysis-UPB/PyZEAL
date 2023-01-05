"""
This module provides a static factory class which maps the algorithms available
in the `AlgorithmType` enumeration to appropriate members of the
`FinderAlgorithm` type.

Authors:\n
- Philipp Schuette\n
"""

from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_algorithms.finder_algorithm import FinderAlgorithm
from pyzeal_algorithms.newton_grid import NewtonGridAlgorithm
from pyzeal_algorithms.simple_holo import SimpleArgumentAlgorithm
from pyzeal_algorithms.simple_holo_newton import SimpleArgumentNewtonAlgorithm


class AlgorithmFactory:
    "Static factory class used to create instances of root finding algorithms."
    @staticmethod
    def getConcreteAlgorithm(
        algoType: AlgorithmTypes,
    ) -> FinderAlgorithm:
        """
        Construct and return an algorithm instance based on the given type of
        algorithm `algoType`.

        :param type: Type of algorithm to construct
        :type type: AlgorithmType
        """
        if algoType == AlgorithmTypes.NEWTON_GRID:
            return NewtonGridAlgorithm()
        elif algoType == AlgorithmTypes.SIMPLE_ARGUMENT:
            return SimpleArgumentAlgorithm()
        elif algoType == AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON:
            return SimpleArgumentNewtonAlgorithm()
        else:
            # TODO: implement configuration mechanism for default algorithms
            return None
