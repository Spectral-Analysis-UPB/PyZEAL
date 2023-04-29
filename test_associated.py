"""
Tests of the improved implementation of associated polynomial root finding.
"""

from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.rootfinders import RootFinder

finder = RootFinder(
    lambda z: z**4 - 1,
    lambda z: 4 * z**3,
    algorithmType=AlgorithmTypes.ASSOCIATED_POLYNOMIAL,
    estimatorType=EstimatorTypes.QUADRATURE_ESTIMATOR,
)

finder.calculateRoots((-1, 1), (-1, 1), precision=(4, 4))
print(f"roots:   {finder.roots}")
print(f"orders:  {finder.orders}")
