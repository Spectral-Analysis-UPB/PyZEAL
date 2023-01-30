"""
Timing benchmark suite for the newton grid based root finding algorithm.
"""
from .testing_fixtures import newtonGridFinder

benchmarkFunctions = [
    "x^2-1",
    "x^2+1",
    "x^4-1",
    "x^5-4x+2",
    "sin(x)",
    "exp(x)",
]


class NewtonGridSuite:
    """
    Timing benchmarks for `NewtonGridRootFinder`.

    Includes simple polynomials and trigonometric functions.
    """

    def TimeNewtonGridRootfinder(self) -> None:
        r"""
        Runs the normal version of the rootfinding algorithm for all
        test cases
        """
        for caseName in benchmarkFunctions:
            gridRF = newtonGridFinder(caseName, numSamplePoints=50)
            gridRF.calculateRoots((-5, 5), (-5, 5), precision=(3, 3))

    def TimeNewtonGridRootfinderDerivativeFree(self) -> None:
        r"""
        Runs the derivative-free version of the algorithm
        """
        for caseName in benchmarkFunctions:
            gridRF = newtonGridFinder(
                caseName, numSamplePoints=50, derivativeFree=True
            )
            gridRF.calculateRoots((-5, 5), (-5, 5), precision=(3, 3))
