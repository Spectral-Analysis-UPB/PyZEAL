"""
This module contains tests of the SIMPLE_ARGUMENT_NEWTON implementation
of the root finding algorithm interface.

Authors:\n
- Luca Wasmuth\n
"""

import numpy as np
import pytest

from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
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
# some test functions do not work due to z-refinement limitations
KNOWN_FAILURES = ["x^100", "1e6 * x^100"]


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.parametrize("testName", testFunctions.keys())
@pytest.mark.parametrize("parallel", [False, True])
@pytest.mark.parametrize(
    "estimator",
    [EstimatorTypes.SUMMATION_ESTIMATOR, EstimatorTypes.QUADRATURE_ESTIMATOR],
)
def testSimpleArgumentNewton(
    testName: str, parallel: bool, estimator: EstimatorTypes
) -> None:
    """
    Test the SIMPLE_ARGUMENT_NEWTON RootFinder with the test case given by
    `testName`.

    :param testName: Name of the test case
    :param parallel: If roots should be searched in parallel
    :param estimator: The type of estimator to use
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()
    hrf = simpleArgumentNewtonRootFinder(
        testName, parallel=parallel, estimatorType=estimator
    )
    hrf.calculateRoots(RE_RAN, IM_RAN, precision=(5, 5))
    foundRoots = hrf.roots
    expectedRoots = np.sort_complex(np.array(testFunctions[testName][2]))
    assert rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)
