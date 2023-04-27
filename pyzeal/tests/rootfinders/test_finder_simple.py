"""
This module contains tests of the SIMPLE_ARGUMENT implementation
of the root finding algorithm interface.

Authors:\n
- Luca Wasmuth\n
"""

import numpy as np
import pytest

from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.tests.resources.finder_helpers import simpleArgumentRootFinder
from pyzeal.tests.resources.finder_test_cases import testFunctions
from pyzeal.tests.resources.utils import rootsMatchClosely
from pyzeal.utils.service_locator import ServiceLocator

# disable progress bar by default for tests
settingsService = RAMSettingsService(verbose=False)
ServiceLocator.registerAsSingleton(SettingsService, settingsService)

# some test functions do not work due to z-refinement limitations
KNOWN_FAILURES = ["poly", "x^100", "1e6 * x^100"]


@pytest.mark.parametrize("testName", sorted(testFunctions.keys()))
@pytest.mark.parametrize("parallel", [False, True])
@pytest.mark.parametrize(
    "estimator",
    [EstimatorTypes.SUMMATION_ESTIMATOR, EstimatorTypes.QUADRATURE_ESTIMATOR],
)
def testSimpleArgument(
    testName: str, parallel: bool, estimator: EstimatorTypes
) -> None:
    """
    Test the SIMPLE_ARGUMENT RootFinder with the test case given by
    `testName`.

    :param testName: Name of the test case
    :param parallel: If roots should be searched in parallel
    :param estimator: The type of estimator to use
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()

    reRan = testFunctions[testName].reRan
    imRan = testFunctions[testName].imRan
    if testName == "x^5-4x+2":
        reRan = (-5, 5)
        imRan = (-5, 5)

    hrf = simpleArgumentRootFinder(
        testName, parallel=parallel, estimatorType=estimator
    )
    precision = testFunctions[testName].precision
    hrf.calculateRoots(reRan, imRan, precision=precision)
    foundRoots = hrf.roots
    expectedRoots = np.array(testFunctions[testName].expectedRoots)

    assert rootsMatchClosely(foundRoots, expectedRoots, precision=precision)
