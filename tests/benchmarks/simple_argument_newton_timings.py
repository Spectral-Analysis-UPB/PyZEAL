"""
Timing benchmark suite for the simple argument (no numerical quadrature)
variant which calls an ordinary Newton algorithm as soon as sufficient
refinement has been reached.
"""

from .resources.testing_fixtures import simpleArgumentNewtonRootFinder
from pyzeal_settings.json_settings_service import JSONSettingsService
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
JSONSettingsService.verbose = False

class SimpleArgumentSuite:
    """
    Timing benchmarks for `NewtonGridRootFinder`.

    Includes simple polynomials and trigonometric functions.
    """

    def TimeSimpleArgument(self) -> None:
        """
        Runs the normal version of the rootfinding algorithm for all
        test cases
        """
        for caseName in benchmarkFunctions:
            hrf = simpleArgumentNewtonRootFinder(caseName)
            hrf.calculateRoots(RE_RAN, IM_RAN, (3, 3))
