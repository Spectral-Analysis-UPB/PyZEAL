"""
Timing benchmark suite for the simple argument (no numerical quadrature)
variant which calls an ordinary Newton algorithm as soon as sufficient
refinement has been reached.
"""
from .testing_fixtures import simpleArgumentNewtonRootFinder

benchmarkFunctions = [
    "x^2-1",
    "x^2+1",
    "x^4-1",
    "x^5-4x+2",
    "sin(x)",
    "exp(x)"
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
            hrf = simpleArgumentNewtonRootFinder(caseName)
            hrf.calculateRoots((-5, 5), (-5, 5), (3,3))
