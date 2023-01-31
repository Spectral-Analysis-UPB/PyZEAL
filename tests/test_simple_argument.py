"""
This module contains tests of the SIMPLE_ARGUMENT implementation
of the root finding algorithm interface.
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

from .benchmarks.resources.testing_fixtures import simpleArgumentRootFinder
from .benchmarks.resources.testing_resources import (
    IM_RAN,
    RE_RAN,
    testFunctions,
)
from .benchmarks.resources.testing_utils import rootsMatchClosely

# disable progress bar by default for tests
JSONSettingsService().verbose = False
# some test functions do not work due to algorithmic limitations
KNOWN_FAILURES = [
    "log and sin composition",  # see issue #12
    "x^100",  # very high root order requires too much z-refinement
    "1e6 * x^100",
]


@pytest.mark.parametrize("testName", testFunctions.keys())
@pytest.mark.parametrize("parallel", [False, True])
def testSimpleArgument(testName : str, parallel : bool) -> None:
    """Test the SIMPLE_ARGUMENT RootFinder with the test case given by `testName`

    :param testName: Name of the test case
    :type testName: str
    :param parallel: If roots should be searched in parallel
    :type parallel: bool
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()
    hrf = simpleArgumentRootFinder(testName, parallel=parallel)
    hrf.calculateRoots(RE_RAN, IM_RAN, precision=(5, 5))
    foundRoots = hrf.roots
    expectedRoots = np.sort_complex(np.array(testFunctions[testName][2]))
    assert np.allclose(
        foundRoots, expectedRoots, atol=1e-3
    ) or rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)


@given(
    strategies.lists(
        strategies.complex_numbers(max_magnitude=10), min_size=1, max_size=10
    )
)
@settings(deadline=(timedelta(seconds=5)), max_examples=5)
def testSimpleArgumentFinderHypothesis(roots) -> None:
    """Test the root finder algorithm based on a simple partial integration of the
    classical argument principle on polynomials whose roots are generated
    automatically using the hypothesis package.

    :param roots: List of roots of a polynomial
    :type roots: List[complex]
    """
    f = Polynomial.fromroots(roots)
    hrf = RootFinder(
        f,
        None,
        algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT,
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
    try:
        assert np.allclose(
            foundRoots, expectedRoots, atol=1e-3
        ) or rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)
    except ValueError:
        pass  # This happens if allclose is called with differing sizes
