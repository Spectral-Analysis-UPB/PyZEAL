"""
Timing benchmark suite for the NewtonGrid root finder strategy.
"""

from typing import List, Tuple, Callable
import numpy as np
from deprecated.newton_grid import NewtonGridRootFinder
from functools import partial

testSuite: List[
    Tuple[
        Callable[[complex], complex],
        Callable[[complex], complex],
        List[complex],
    ]
] = [
    (lambda x: x**2 - 1, lambda x: 2 * x, [-1, 1]),
    (lambda x: x**2 + 1, lambda x: 2 * x, [1j, -1j]),
    (lambda x: x**4 - 1, lambda x: 4 * x**3, [1, -1, 1j, -1j]),
    (np.sin, np.cos, [-1 * np.pi, 0, np.pi]),
    (np.exp, np.exp, []),
    (
        lambda x: x**5 - 4 * x + 2,
        lambda x: 5 * x**4 - 4,
        [
            0.508499484,
            -1.51851215,
            1.2435963,
            -0.116791 - 1.43844769j,
            -0.116791 + 1.43844769j,
        ],
    ),
]


def f(n, x):
    return testSuite[n][0](x)


def df(n, x):
    return testSuite[n][1](x)


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
        for tCase in range(len(testSuite)):
            gridRF = NewtonGridRootFinder(
                partial(f, tCase), partial(df, tCase)
            )
            gridRF.calcRoots((-5, 5), (-5, 5), precision=(3, 3))

    def TimeNewtonGridRootfinderDerivativeFree(self) -> None:
        r"""
        Runs the derivative-free version of the algorithm
        """
        for tCase in range(len(testSuite)):
            gridRF = NewtonGridRootFinder(partial(f, tCase), df=None)
            gridRF.calcRoots((-5, 5), (-5, 5), precision=(3, 3))
