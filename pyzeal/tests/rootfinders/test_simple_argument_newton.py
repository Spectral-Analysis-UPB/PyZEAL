"""
This module contains tests of the SIMPLE_ARGUMENT_NEWTON implementation
of the root finding algorithm interface.
"""

from datetime import timedelta
from typing import List

import numpy as np
import pytest
from hypothesis import given, settings, strategies
from numpy.polynomial import Polynomial

from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.filter_types import FilterTypes
from pyzeal.rootfinders import RootFinder
from pyzeal.settings.json_settings_service import JSONSettingsService
from pyzeal.tests.resources.testing_fixtures import (
    simpleArgumentNewtonRootFinder,
)
from pyzeal.tests.resources.testing_resources import (
    IM_RAN,
    RE_RAN,
    testFunctions,
)
from pyzeal.tests.resources.testing_utils import rootsMatchClosely

# disable progress bar by default for tests
JSONSettingsService().verbose = False
# some test functions do not work due to algorithmic limitations
KNOWN_FAILURES = [
    "log and sin composition",  # see issue #12
    "x^100",  # roots of very high orders require too much z-refinement
    "1e6 * x^100",
]


@pytest.mark.parametrize("testName", testFunctions.keys())
@pytest.mark.parametrize("parallel", [False, True])
def testSimpleArgumentNewton(testName: str, parallel: bool) -> None:
    """
    Test the SIMPLE_ARGUMENT_NEWTON RootFinder with the test case given by
    `testName`

    :param testName: Name of the test case
    :type testName: str
    :param parallel: If roots should be searched in parallel
    :type parallel: bool
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()
    hrf = simpleArgumentNewtonRootFinder(testName, parallel=parallel)
    hrf.calculateRoots(RE_RAN, IM_RAN, precision=(5, 5))
    foundRoots = hrf.roots
    expectedRoots = np.sort_complex(np.array(testFunctions[testName][2]))
    assert rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)


@given(
    strategies.lists(
        strategies.complex_numbers(max_magnitude=10), min_size=1, max_size=10
    )
)
@settings(deadline=(timedelta(seconds=5)), max_examples=5)
def testSimpleArgumentNewtonHypothesis(roots: List[complex]) -> None:
    """
    Test the root finder algorithm based on a simple partial integration of the
    classical argument principle combined with a Newton algorithm upon
    sufficient refinement of the subdivision into rectangles. The testfunctions
    are polynomials whose roots are generated automatically using the
    hypothesis package.

    :param roots: Roots of a polynomial
    :type roots: List[complex]
    """
    f = Polynomial.fromroots(roots)
    hrf = RootFinder(
        f,
        None,
        algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON,
        containerType=ContainerTypes.ROUNDING_CONTAINER,
        verbose=False,
    )
    hrf.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    hrf.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)
    hrf.calculateRoots((-5.0, 5.01), (-5.0, 5.01), precision=(5, 5))
    foundRoots = np.sort_complex(hrf.roots)

    # We only find a higher-order zero once, so we have to remove duplicates
    uniqueRoots = list(set(roots))
    expectedRoots = np.sort_complex(np.array(uniqueRoots))
    assert rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)
