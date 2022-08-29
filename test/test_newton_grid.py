"""
Test the grid-based Newton algorithm implementation.

Authors:\n
- Luca Wasmuth\n
"""

from typing import Callable, List, Tuple
import numpy as np

from rootfinder.newton_grid import NewtonGridRootFinder


def test_newton_grid_rootfinder() -> None:
    r"""
    Run tests for the Newton-based root finder on a grid.
    """
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

    for tCase in testSuite:
        gridRF = NewtonGridRootFinder(tCase[0], tCase[1])
        gridRF.calcRoots([-5, 5], [-5, 5], precision=(3, 3))

        foundRoots = np.sort_complex(gridRF.getRoots())
        expectedRoots = np.sort_complex(np.array(tCase[2]))
        assert np.allclose(foundRoots, expectedRoots, atol=1e-3)
