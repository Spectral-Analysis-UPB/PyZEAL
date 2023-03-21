"""
Timing benchmark suite for the simple argument (with and without numerical
quadrature) with Newton algorithm based root finding algorithm.

Authors:\n
- Luca Wasmuth\n
- Philipp Schuette\n
"""

from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.json_settings_service import JSONSettingsService
from pyzeal.tests.resources.testing_fixtures import (
    simpleArgumentNewtonRootFinder,
)
from pyzeal.tests.resources.testing_resources import IM_RAN, RE_RAN

benchmarkFunctions = [
    "x^2-1",
    "x^2+1",
    "x^4-1",
    "x^5-4x+2",
    "sin(x)",
    "exp(x)",
]
# disable progress bar
JSONSettingsService().verbose = False


class SimpleArgumentSuite:
    """
    Timing benchmarks for the simple argument principle based root finder with
    additional Newton algorithm once sufficient precision has been attained.
    Includes simple polynomials as well as trigonometric and exponential
    functions.
    """

    def TimeSimpleArgumentNewtonSummation(self) -> None:
        """
        Runs the simple argument version of the rootfinding algorithm with
        summation based argument estimation and non-parallel.
        """
        for caseName in benchmarkFunctions:
            hrf = simpleArgumentNewtonRootFinder(
                caseName,
                parallel=False,
                estimatorType=EstimatorTypes.SUMMATION_ESTIMATOR,
            )
            hrf.calculateRoots(RE_RAN, IM_RAN, (5, 5))

    def TimeSimpleArgumentNewtonQuadrature(self) -> None:
        """
        Analogous to `TimeSimpleArgumentSummation` but here the algorithm uses
        quadrature based argument estimation.
        """
        for caseName in benchmarkFunctions:
            hrf = simpleArgumentNewtonRootFinder(
                caseName,
                parallel=False,
                estimatorType=EstimatorTypes.QUADRATURE_ESTIMATOR,
            )
            hrf.calculateRoots(RE_RAN, IM_RAN, (5, 5))
