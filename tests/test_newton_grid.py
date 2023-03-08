"""
This module contains tests of the grid-based Newton algorithm implementation
of the root finding algorithm interface.

Authors:\n
- Luca Wasmuth\n
"""

from datetime import timedelta

import numpy as np
import pytest
from hypothesis import given, settings, strategies
from numpy.polynomial import Polynomial

from pyzeal import RootFinder
from pyzeal_settings.json_settings_service import JSONSettingsService
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.filter_types import FilterTypes

from .benchmarks.resources.testing_fixtures import newtonGridFinder
from .benchmarks.resources.testing_resources import (
    IM_RAN,
    RE_RAN,
    testFunctions,
)
from .benchmarks.resources.testing_utils import rootsMatchClosely

# 20 is enough to pass all tests while still running faster than the default 50
NUM_SAMPLE_POINTS = 20
# disable progress bar by default for tests
JSONSettingsService().verbose = False
# some test functions do not work due to algorithmic limitations
KNOWN_FAILURES = ["log and sin composition", "x^100", "1e6 * x^100"]


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.parametrize("testName", testFunctions.keys())
@pytest.mark.parametrize("parallel", [False, True])
def testNewtonGridRootFinder(testName: str, parallel: bool) -> None:
    """Test the Newton-Grid-Rootfinder with the function given by `testName`

    :param testName: Name of the test case
    :type testName: str
    :param parallel: If roots should be searched in parallel
    :type parallel: bool
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()
    for numSamplePoints in [20, 100]:
        gridRF = newtonGridFinder(testName, numSamplePoints, parallel=parallel)
        gridRF.calculateRoots(RE_RAN, IM_RAN, (5, 5))
        print(gridRF.roots)
        foundRoots = np.sort_complex(gridRF.roots)
        expectedRoots = np.sort_complex(np.array(testFunctions[testName][2]))
        assert rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)


@given(
    strategies.lists(
        strategies.complex_numbers(max_magnitude=10), min_size=1, max_size=10
    )
)
@settings(deadline=(timedelta(seconds=5)), max_examples=5)
def testNewtonGridRootFinderHypothesis(roots) -> None:
    """Test the grid-based Newton rootfinder on polynomials whose roots are
    generated automatically using the hypothesis package.

    :param roots: Roots of a polynomial
    :type roots: List[complex]
    """
    f = Polynomial.fromroots(roots)
    df = f.deriv()
    gridRF = RootFinder(
        f,
        df=df,
        numSamplePoints=NUM_SAMPLE_POINTS,
        containerType=ContainerTypes.ROUNDING_CONTAINER,
        algorithmType=AlgorithmTypes.NEWTON_GRID,
    )
    gridRF.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    gridRF.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)
    gridRF.calculateRoots((-10, 10), (-10, 10), (5, 5))
    foundRoots = np.sort_complex(gridRF.roots)
    # We only find a higher-order zero once, so we remove duplicates
    uniqueRoots = list(set(roots))
    expectedRoots = np.sort_complex(np.array(uniqueRoots))
    assert rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)
