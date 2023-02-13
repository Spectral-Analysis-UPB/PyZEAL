"""
Timing benchmark suite for the newton grid based root finding algorithm.

Authors:\n
- Luca Wasmuth\n
"""

from pyzeal_settings.json_settings_service import JSONSettingsService

from .resources.testing_fixtures import newtonGridFinder
from .resources.testing_resources import IM_RAN, RE_RAN

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


class NewtonGridSuite:
    """
    Timing benchmarks for the root finding algorithm which uses a grid of
    starting points for an ordinary Newton algorithm. Includes simple
    polynomials as well as trigonometric and exponential functions.
    """

    def TimeNewtonGridRootfinder(self) -> None:
        """
        Runs the Newton grid based version of the rootfinding algorithm for all
        test cases and non-parallel.
        """
        for caseName in benchmarkFunctions:
            gridRF = newtonGridFinder(
                caseName, numSamplePoints=50, parallel=False
            )
            gridRF.calculateRoots(IM_RAN, RE_RAN, precision=(5, 5))

    def TimeNewtonGridRootfinderDerivativeFree(self) -> None:
        """
        Runs the derivative-free version of the Newton grid based algorithm
        for all test cases and non-parallel.
        """
        for caseName in benchmarkFunctions:
            gridRF = newtonGridFinder(
                caseName,
                numSamplePoints=50,
                derivativeFree=True,
                parallel=False,
            )
            gridRF.calculateRoots(IM_RAN, RE_RAN, precision=(5, 5))
