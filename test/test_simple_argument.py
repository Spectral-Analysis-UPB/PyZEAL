from datetime import timedelta
from functools import partial
import numpy as np
import pytest

from hypothesis import given, strategies, settings
from numpy.polynomial import Polynomial
from pyzeal.simple_argument import HoloRootFinder

def polynomial(n, x):
    """Evaluates the nth polynomial test case at x"""
    return polynomialFunctions[n][0](x)


def polynomialD(n, x):
    """Evaluates the nth polynomials derivative at x"""
    return polynomialFunctions[n][1](x)


def elementary(n, x):
    """Evaluates the nth elementary function test case at x"""
    return elementaryFunctions[n][0](x)


def elementaryD(n, x):
    """Evaluates the nth elementary functions derivative at x"""
    return elementaryFunctions[n][1](x)


polynomialFunctions = [
    (lambda x: x**2 - 1, lambda x: 2 * x, [-1, 1]), #0
    (lambda x: x**2 + 1, lambda x: 2 * x, [1j, -1j]), #1
    (lambda x: x**4 - 1, lambda x: 4 * x**3, [1, -1, 1j, -1j]), #2
    (
        lambda x: x**3 + x**2 + x + 1,
        lambda x: 3 * x**2 + 2 * x + 1,
        [-1, 1j, -1j],
    ), #3
    (lambda x: x**2 + 26.01, lambda x: 2 * x, []), #4
    (
        lambda x: (x - np.sqrt(2)) * (x + np.sqrt(2)) * (x - 1.5) * (x + 1.5),
        lambda x: 4 * x**3 - 8.5 * x,
        [np.sqrt(2), -np.sqrt(2), 1.5, -1.5],
    ), #5
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
    ), #6
    (
        lambda x: (x - 0.1) * (x + 0.1) * x,
        lambda x: 3 * x**2 - 0.01,
        [0.1, 0, -0.1],
    ), #7
    (lambda x: x**30, lambda x: 30 * x**29, [0]), #8
    (lambda x: x**100, lambda x: 100 * x**99, [0]), #9
    (lambda x: 1e6 * x**100, lambda x: 1e8 * x**99, [0]), #10
    (lambda x: (x - 5) * (x + 5), lambda x: 2 * x, [5, -5]), #11
    (
        lambda x: x * (x + 0.000024414 - 1j),
        lambda x: 2 * x + 0.000024414 - 1j,
        [0, -0.000024414 + 1j],
    ), #12
]
elementaryFunctions = [
    (np.sin, np.cos, [-1 * np.pi, 0, np.pi]),
    (np.exp, np.exp, []),
    (lambda x: np.tan(x / 10), lambda x: 1 / (10 * np.cos(x / 10) ** 2), [0]),
    (
        lambda x: np.tan(x / 100),
        lambda x: 1 / (100 * np.cos(x / 100) ** 2),
        [0],
    ),
    (
        lambda x: np.log(np.sin(x) ** 2 + 1),
        lambda x: 2 * np.sin(x) * np.cos(x) / (np.sin(x) ** 2 + 1),
        [-np.pi, 0, np.pi],
    ),
    (lambda x: x ** (1 / 7), lambda x: 1 / 7 * x ** (-6 / 7), [0]),
    (
        lambda x: np.log(x**2 + 26),
        lambda x: 2 * x / (x**2 + 26),
        [-5j, 5j],
    ),
    (
        lambda x: np.log(np.arctan(np.exp(x))),
        lambda x: np.exp(x) / ((np.exp(2 * x) + 1) * np.arctan(np.exp(x))),
        [0.44302],
    ),
]
elementaryFunctions = [
    (np.sin, np.cos, [-1 * np.pi, 0, np.pi]),
    (np.exp, np.exp, []),
    (lambda x: np.tan(x / 10), lambda x: 1 / (10 * np.cos(x / 10) ** 2), [0]),
    (
        lambda x: np.tan(x / 100),
        lambda x: 1 / (100 * np.cos(x / 100) ** 2),
        [0],
    ),
    (
        lambda x: np.log(np.sin(x) ** 2 + 1),
        lambda x: 2 * np.sin(x) * np.cos(x) / (np.sin(x) ** 2 + 1),
        [-np.pi, 0, np.pi],
    ),
    (lambda x: x ** (1 / 7), lambda x: 1 / 7 * x ** (-6 / 7), [0]),
    (
        lambda x: np.log(x**2 + 26),
        lambda x: 2 * x / (x**2 + 26),
        [-5j, 5j],
    ),
    (
        lambda x: np.log(np.arctan(np.exp(x))),
        lambda x: np.exp(x) / ((np.exp(2 * x) + 1) * np.arctan(np.exp(x))),
        [0.44302],
    ),
]


@pytest.mark.parametrize("testID", range(len(polynomialFunctions)))
def testSimpleArgumentPolynomials(testID) -> None:
    hrf = HoloRootFinder(partial(polynomial, testID), epsCplx=1e-5 * (1+1j))
    hrf.calcRoots((-5,5),(-5,5))
    foundRoots = hrf.res
    expectedRoots = np.sort_complex(polynomialFunctions[testID][2])
    assert np.allclose(foundRoots, expectedRoots, atol=1e-3) or rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)


@pytest.mark.parametrize("testID", range(len(elementaryFunctions)))
def testSimpleArgumentElementary(testID) -> None:
    hrf = HoloRootFinder(partial(elementary, testID), epsCplx=1e-5 * (1+1j))
    hrf.calcRoots((-5,5),(-5,5))
    foundRoots = hrf.res
    expectedRoots = np.sort_complex(elementaryFunctions[testID][2])
    assert np.allclose(foundRoots, expectedRoots, atol=1e-3) or rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)


def rootsMatchClosely(r1, r2, atol) -> bool:
    r"""
    Test, if two sets contain the same roots, up to inaccuraccy of size atol
    :param r1: first set of roots
    :type r1: Set[complex]
    :param r2: second set of roots
    :type r2: Set[complex]
    :return: True if the number of zeroes in r1 and r2 is the same, and they
    lie at most atol apart
    :rtype: bool
    """
    noUnmatchedRoot: bool = True
    for z in r1:
        foundRootForZ: bool = False
        for root in r2:
            if np.abs(z - root) < atol:
                foundRootForZ = True
        if not foundRootForZ:
            noUnmatchedRoot = False

    return noUnmatchedRoot