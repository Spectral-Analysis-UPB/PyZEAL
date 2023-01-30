"""
Timing benchmark suite for the simple argument (no numerical quadrature) based
root finding algorithm.
"""
from .testing_fixtures import simpleArgumentRootFinder

benchmarkFunctions = [
    "x^2-1",
    "x^2+1",
    "x^4-1",
    "x^5-4x+2",
    "sin(x)",
    "exp(x)",
]


class SimpleArgumentSuite:
    """
    Timing benchmarks for `NewtonGridRootFinder`.

    Includes simple polynomials and trigonometric functions.
    """

    def TimeSimpleArgument(self) -> None:
        r"""
        Runs the normal version of the rootfinding algorithm for all
        test cases
        """
        for caseName in benchmarkFunctions:
            hrf = simpleArgumentRootFinder(caseName)
            hrf.calculateRoots((-5, 5), (-5, 5))
