"""
Test the grid-based Newton algorithm implementation.
"""

from typing import Callable, List, Set
from rootfinder.newton_grid import NewtonGridRootFinder
import numpy as np


def test_newton_grid_rootfinder() -> None:
    r"""
    Run tests for the Newton-based root finder on a grid
    """
    testSuite: List[
        List[Callable[[float], float], Callable[[float], float], List[float]]
    ] = [
        [lambda x: x**2 - 1, lambda x: 2 * x, [-1, 1]],
        [lambda x: x**2 + 1, lambda x: 2 * x, [1j, -1j]],
        [lambda x: x**4 - 1, lambda x: 4 * x**3, [1, -1, 1j, -1j]],
        [np.sin, np.cos, [-1 * np.pi, 0, np.pi]],
        [np.exp, np.exp, []],
        [
            lambda x: x**5 - 4 * x + 2,
            lambda x: 5 * x**4 - 4,
            [
                0.508499484,
                -1.51851215,
                1.2435963,
                -0.116791 - 1.43844769j,
                -0.116791 + 1.43844769j,
            ],
        ],
    ]
    for t in testSuite:
        rf: NewtonGridRootFinder = NewtonGridRootFinder(t[0], t[1])
        atol: float = 10**-3
        rf.calcRoots([-5, 5], [-5, 5], epsCplx=atol)
        foundRoots: Set[complex] = set(rf.getRoots().flatten())
        expectedRoots: Set[complex] = set(t[2])
        assert rootsMatchClosely(foundRoots, expectedRoots, atol=atol)


def rootsMatchClosely(
    r1: Set[complex], r2: Set[complex], atol: float = 10**-6
) -> bool:
    r"""
    Test, if two sets contain the same roots, up to inaccuraccy of size atol
    :param r1: first set of roots
    :type r1: Set[complex]
    :param r2: second set of roots
    :type r2: Set[complex]
    :return: True if the number of zeroes in r1 and r2 is the same, and they lie at
      most atol apart
    :rtype: bool
    """

    # If the sets contain different amounts, they can't have the same zeroes
    if len(r1) != len(r2):
        return False

    noUnmatchedRoot: bool = True
    for z in r1:
        foundRootForZ: bool = False
        for root in r2:
            if np.abs(z - root) < atol:
                foundRootForZ = True
        if not foundRootForZ:
            noUnmatchedRoot = False

    return noUnmatchedRoot
