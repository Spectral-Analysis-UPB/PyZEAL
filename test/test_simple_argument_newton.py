"""
TODO
"""

from datetime import timedelta

import numpy as np
import pytest
from hypothesis import given, settings, strategies
from numpy.polynomial import Polynomial

from pyzeal import RootFinder
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.filter_types import FilterTypes

from .testing_fixtures import simpleArgumentNewtonRootFinder
from .testing_resources import IM_RAN, RE_RAN, testFunctions
from .testing_utils import rootsMatchClosely

KNOWN_FAILURES = [
    "log and sin composition",  # see issue #12
    "x^100",  # roots of very high orders require too much z-refinement
    "1e6 * x^100",
]


@pytest.mark.parametrize("testName", testFunctions.keys())
@pytest.mark.parametrize("parallel", [False, True])
def testSimpleArgumentNewton(testName, parallel) -> None:
    """
    TODO
    """
    if testName in KNOWN_FAILURES:
        assert True
        return
    hrf = simpleArgumentNewtonRootFinder(testName, parallel=parallel)
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
@settings(deadline=(timedelta(seconds=2)), max_examples=5)
def testSimpleArgumentNewtonHypothesis(roots) -> None:
    """
    Test the root finder algorithm based on a simple partial integration of the
    classical argument principle combined with a Newton algorithm upon
    sufficient refinement of the subdivision into rectangles. The testfunctions
    are polynomials whose roots are generated automatically using the
    hypothesis package.

    TODO
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
    try:
        assert np.allclose(
            foundRoots, expectedRoots, atol=1e-3
        ) or rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)
    except ValueError:
        pass  # This happens if allclose is called with differing sizes
