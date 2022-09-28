"""
Test the grid-based Newton algorithm implementation.

Authors:\n
- Luca Wasmuth\n
"""

import numpy as np
import pytest

from rootfinder.newton_grid import NewtonGridRootFinder

polynomialFunctions = [
    (lambda x: x**2 - 1, lambda x: 2 * x, [-1, 1]),
    (lambda x: x**2 + 1, lambda x: 2 * x, [1j, -1j]),
    (lambda x: x**4 - 1, lambda x: 4 * x**3, [1, -1, 1j, -1j]),
    (lambda x: x**3 + x**2 + x + 1, lambda x: 3*x**2 + 2*x + 1, [-1, 1j, -1j]),
    (lambda x: x**2 + 26.01, lambda x: 2*x, []),
    (
        lambda x: (x-np.sqrt(2))*(x+np.sqrt(2))*(x-1.5)*(x+1.5),
        lambda x: 4*x**3 - 8.5*x,
        [
            np.sqrt(2),
            -np.sqrt(2),
            1.5,
            -1.5
        ]
    ),
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
    (
        lambda x: (x-0.1)*(x+0.1)*x,
        lambda x: 3*x**2 - 0.01,
        [
            0.1,
            0,
            -0.1
        ]
    ),
    (
        lambda x: x**30,
        lambda x: 30*x**29,
        [
            0
        ]
    ),
    (
        lambda x: x**100,
        lambda x: 100*x**99,
        [
            0
        ]
    ),
    (
        lambda x: 1e6*x**100,
        lambda x: 1e8*x**99,
        [
            0
        ]
    ),
    (
        lambda x: (x-5)*(x+5),
        lambda x: 2*x,
        [
            5,
            -5
        ]
    )
]
elementaryFunctions = [
    (np.sin, np.cos, [-1 * np.pi, 0, np.pi]),
    (np.exp, np.exp, []),
    (lambda x: np.tan(x/10), lambda x: 1/(10*np.cos(x)**2), [0]),
    (lambda x: np.tan(x/100), lambda x: 1/(100*np.cos(x)**2), [0]),
    (
        lambda x: np.log(np.sin(x)**2+1),
        lambda x: 2 * np.sin(x) * np.cos(x) / (np.sin(x)**2 + 1),
        [
            -np.pi,
            0,
            np.pi
        ]
    ),
    (
        lambda x: x**(1/7),
        lambda x: 1/7 * x**(-6/7),
        [
            0
        ]
    ),
    (
        lambda x: np.log(x**2+26),
        lambda x: 2*x/(x**2+26),
        [
            -5j,
            5j
        ]
    ),
    (
        lambda x: np.log(np.arctan(np.exp(x))),
        lambda x: np.exp(x)/((np.exp(2 * x) + 1) * np.arctan(np.exp(x))),
        [
            0.44302
        ]
    )
]

def test_newton_grid_rootfinder() -> None:
    r"""
    Run tests for the Newton-based root finder on a grid.
    """
    for tCase in polynomialFunctions:
        gridRF = NewtonGridRootFinder(tCase[0], tCase[1])
        gridRF.calcRoots([-5, 5], [-5, 5], precision=(3, 3))

        foundRoots = np.sort_complex(gridRF.getRoots())
        expectedRoots = np.sort_complex(np.array(tCase[2]))
        assert np.allclose(foundRoots, expectedRoots, atol=1e-3)

    for tCase in elementaryFunctions:
        gridRF = NewtonGridRootFinder(tCase[0], tCase[1])
        gridRF.calcRoots([-5, 5], [-5, 5], precision=(3, 3))

        foundRoots = np.sort_complex(gridRF.getRoots())
        expectedRoots = np.sort_complex(np.array(tCase[2]))
        assert np.allclose(foundRoots, expectedRoots, atol=1e-3)

    # Test exception throwing
    gridRF = NewtonGridRootFinder(lambda x: x, lambda x: 1)
    with pytest.raises(ValueError):
        gridRF.getRoots()
