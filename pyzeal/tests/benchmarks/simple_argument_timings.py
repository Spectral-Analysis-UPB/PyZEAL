"""
Timing benchmark suite for the simple argument (with and without numerical
quadrature) based root finding algorithm.

Authors:\n
- Luca Wasmuth\n
- Philipp Schuette\n
"""

from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.tests.resources.finder_helpers import simpleArgumentRootFinder
from pyzeal.tests.resources.finder_test_cases import testFunctions
from pyzeal.utils.service_locator import ServiceLocator

benchmarkFunctions = [
    "x^2-1",
    "x^2+1",
    "x^4-1",
    "x^5-4x+2",
    "sin(x)",
    "exp(x)",
]

# disable progress bar
settingsService = RAMSettingsService(verbose=False)
ServiceLocator.registerAsSingleton(SettingsService, settingsService)


class SimpleArgumentSuite:
    """
    Timing benchmarks for the simple argument principle based root finder.
    Includes simple polynomials as well as trigonometric and exponential
    functions.
    """

    def TimeSimpleArgumentSummation(self) -> None:
        """
        Runs the simple argument version of the rootfinding algorithm with
        summation based argument estimation and non-parallel.
        """
        for caseName in benchmarkFunctions:
            hrf = simpleArgumentRootFinder(
                caseName,
                parallel=False,
                estimatorType=EstimatorTypes.SUMMATION_ESTIMATOR,
            )
            reRan = testFunctions[caseName].reRan
            imRan = testFunctions[caseName].imRan
            hrf.calculateRoots(reRan, imRan, precision=(5, 5))

    def TimeSimpleArgumentQuadrature(self) -> None:
        """
        Analogous to `TimeSimpleArgumentSummation` but here the algorithm uses
        quadrature based argument estimation.
        """
        for caseName in benchmarkFunctions:
            hrf = simpleArgumentRootFinder(
                caseName,
                parallel=False,
                estimatorType=EstimatorTypes.QUADRATURE_ESTIMATOR,
            )
            reRan = testFunctions[caseName].reRan
            imRan = testFunctions[caseName].imRan
            hrf.calculateRoots(reRan, imRan, precision=(5, 5))
